import os
import re
from functools import lru_cache

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from sqlalchemy import delete, select

from .models import AgentTask, Project, slugify_task_name

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
MAX_SECTION_SIZE = 1500

_vector_stores: dict[str, PGVector] = {}

INVENTORY_QUERY_PATTERN = re.compile(
    r"\b(how many|list|names only|all projects|which projects|project names|"
    r"what projects|name of.*projects|projects.*running)\b",
    re.IGNORECASE,
)


def collection_name_for_agent(agent_id: int) -> str:
    return f"agent_{agent_id}"


@lru_cache(maxsize=1)
def _get_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=os.getenv("OLLAMA_EMBEDDING_MODEL", "qwen3-embedding:4b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )


def _connection_string() -> str:
    return os.getenv(
        "VECTOR_DATABASE_URL",
        "postgresql+psycopg://a.tandel@localhost:5433/llm_automation",
    )


def get_vector_store(agent_id: int) -> PGVector:
    collection_name = collection_name_for_agent(agent_id)
    if collection_name not in _vector_stores:
        _vector_stores[collection_name] = PGVector(
            connection=_connection_string(),
            collection_name=collection_name,
            embeddings=_get_embeddings(),
            use_jsonb=True,
            create_extension=False,
        )
    return _vector_stores[collection_name]


def evict_vector_store_cache(agent_id: int) -> None:
    collection_name = collection_name_for_agent(agent_id)
    _vector_stores.pop(collection_name, None)


def _delete_by_source_id(agent_id: int, source_id: str) -> int:
    vector_store = get_vector_store(agent_id)
    with vector_store._make_sync_session() as session:
        collection = vector_store.get_collection(session)
        if collection is None:
            return 0

        stmt = (
            delete(vector_store.EmbeddingStore)
            .where(vector_store.EmbeddingStore.collection_id == collection.uuid)
            .where(vector_store.EmbeddingStore.cmetadata["source_id"].astext == source_id)
        )
        result = session.execute(stmt)
        session.commit()
        return result.rowcount or 0


def clear_agent_collection(agent_id: int) -> int:
    vector_store = get_vector_store(agent_id)
    with vector_store._make_sync_session() as session:
        collection = vector_store.get_collection(session)
        if collection is None:
            evict_vector_store_cache(agent_id)
            return 0

        stmt = delete(vector_store.EmbeddingStore).where(
            vector_store.EmbeddingStore.collection_id == collection.uuid
        )
        result = session.execute(stmt)
        session.commit()
        deleted = result.rowcount or 0

    evict_vector_store_cache(agent_id)
    return deleted


def reset_agent_task_vector_flags(agent_id: int) -> int:
    return AgentTask.objects.filter(agent_id=agent_id).update(
        vd_processed=False,
        processed=False,
    )


def _base_metadata(
    *,
    doc_type: str,
    source_id: str,
    title: str,
    project_id: int | None = None,
    project_name: str = "",
    agent_task_id: int | None = None,
    task_name: str = "",
) -> dict:
    metadata = {
        "doc_type": doc_type,
        "source_id": source_id,
        "version": 1,
        "is_latest": True,
        "title": title,
        "project_name": project_name,
    }
    if project_id is not None:
        metadata["project_id"] = str(project_id)
    if agent_task_id is not None:
        metadata["agent_task_id"] = str(agent_task_id)
    if task_name:
        metadata["task_name"] = task_name
    return metadata


def _document_header(
    *,
    project_name: str,
    project_id: int,
    task_name: str = "",
    task_id: int | None = None,
    doc_type: str,
) -> str:
    lines = [
        f"Project: {project_name} (id={project_id})",
    ]
    if task_name:
        task_line = f"Task: {task_name}"
        if task_id is not None:
            task_line += f" (id={task_id})"
        lines.append(task_line)
    lines.append(f"Document type: {doc_type}")
    lines.append("---")
    return "\n".join(lines)


def _split_task_result(text: str) -> list[str]:
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )
    sections = header_splitter.split_text(text)
    if not sections:
        sections = [Document(page_content=text)]

    fallback_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks: list[str] = []
    for section in sections:
        content = section.page_content.strip()
        if not content:
            continue
        if len(content) <= MAX_SECTION_SIZE:
            chunks.append(content)
        else:
            chunks.extend(
                document.page_content
                for document in fallback_splitter.create_documents([content])
            )
    return chunks or [text.strip()]


def _prepare_chunks(text: str, doc_type: str) -> list[str]:
    if not text.strip():
        return []
    if doc_type == "task_description":
        return [text.strip()]
    if doc_type == "task_result":
        return _split_task_result(text)
    if doc_type == "admin_knowledge":
        return _split_task_result(text)
    return [text.strip()]


def ingest_document(
    *,
    agent_id: int,
    source_id: str,
    doc_type: str,
    text: str,
    title: str,
    project_id: int | None = None,
    project_name: str = "",
    agent_task_id: int | None = None,
    task_name: str = "",
) -> None:
    chunks = _prepare_chunks(text, doc_type)
    if not chunks:
        return

    _delete_by_source_id(agent_id, source_id)
    vector_store = get_vector_store(agent_id)
    metadata = _base_metadata(
        doc_type=doc_type,
        source_id=source_id,
        title=title,
        project_id=project_id,
        project_name=project_name,
        agent_task_id=agent_task_id,
        task_name=task_name,
    )

    documents: list[Document] = []
    for index, chunk in enumerate(chunks):
        body = chunk
        if project_id is not None:
            header = _document_header(
                project_name=project_name,
                project_id=project_id,
                task_name=task_name,
                task_id=agent_task_id,
                doc_type=doc_type,
            )
            body = f"{header}\n{chunk}"

        chunk_metadata = {
            **metadata,
            "chunk_index": index,
        }
        documents.append(Document(page_content=body, metadata=chunk_metadata))

    vector_store.add_documents(documents)


def ingest_project_record(*, agent_id: int, project: Project) -> None:
    text = (
        f"Project: {project.name}\n"
        f"ID: {project.id}\n"
        f"Description: {project.description.strip() or '(none)'}"
    )
    ingest_document(
        agent_id=agent_id,
        source_id=f"project_{project.id}",
        doc_type="project_record",
        text=text,
        title=project.name,
        project_id=project.id,
        project_name=project.name,
    )


def rebuild_project_catalog(*, agent_id: int) -> None:
    projects = (
        Project.objects.filter(tasks__agent_id=agent_id, active=True)
        .distinct()
        .order_by("name")
    )
    lines = [f"Projects for this agent ({projects.count()} total):"]
    for project in projects:
        lines.append(f"- {project.name} (id={project.id})")

    ingest_document(
        agent_id=agent_id,
        source_id=f"agent_{agent_id}:project_catalog",
        doc_type="project_catalog",
        text="\n".join(lines),
        title="Project catalog",
    )


def ingest_task_description(*, task: AgentTask) -> None:
    ingest_document(
        agent_id=task.agent_id,
        source_id=f"{task.id}:task_description",
        doc_type="task_description",
        text=task.description,
        title=task.name,
        project_id=task.project_id,
        project_name=task.project.name,
        agent_task_id=task.id,
        task_name=task.name,
    )


def ingest_task_result(*, task: AgentTask) -> None:
    if not task.result.strip():
        return
    ingest_document(
        agent_id=task.agent_id,
        source_id=f"{task.id}:task_result",
        doc_type="task_result",
        text=task.result,
        title=task.name,
        project_id=task.project_id,
        project_name=task.project.name,
        agent_task_id=task.id,
        task_name=task.name,
    )


def admin_knowledge_source_id(title: str) -> str:
    return f"knowledge:{slugify_task_name(title)}"


def ingest_admin_knowledge(
    *,
    agent_id: int,
    title: str,
    text: str,
) -> int:
    title = title.strip()
    text = text.strip()
    if not title or not text:
        return 0

    chunks = _prepare_chunks(text, "admin_knowledge")
    source_id = admin_knowledge_source_id(title)
    _delete_by_source_id(agent_id, source_id)

    vector_store = get_vector_store(agent_id)
    metadata = _base_metadata(
        doc_type="admin_knowledge",
        source_id=source_id,
        title=title,
    )

    documents: list[Document] = []
    for index, chunk in enumerate(chunks):
        header_lines = [
            f"Knowledge: {title}",
            "Document type: admin_knowledge",
            "---",
        ]
        body = "\n".join(header_lines) + f"\n{chunk}"
        documents.append(
            Document(
                page_content=body,
                metadata={**metadata, "chunk_index": index},
            )
        )

    vector_store.add_documents(documents)
    return len(chunks)


def delete_admin_knowledge(*, agent_id: int, source_id: str) -> int:
    return _delete_by_source_id(agent_id, source_id)


def ingest_task_document(
    *,
    agent_id: int,
    agent_task_id: int,
    doc_type: str,
    text: str,
    title: str,
    version: int = 1,
) -> None:
    task = AgentTask.objects.select_related("project").get(pk=agent_task_id)
    if doc_type == "task_description":
        ingest_task_description(task=task)
        return
    if doc_type == "task_result":
        ingest_task_result(task=task)
        return

    ingest_document(
        agent_id=agent_id,
        source_id=f"{agent_task_id}:{doc_type}",
        doc_type=doc_type,
        text=text,
        title=title,
        project_id=task.project_id,
        project_name=task.project.name,
        agent_task_id=agent_task_id,
        task_name=task.name,
    )


def fetch_documents_by_metadata(
    agent_id: int,
    *,
    doc_types: list[str] | None = None,
    project_id: int | None = None,
    limit: int = 100,
) -> list[Document]:
    vector_store = get_vector_store(agent_id)
    with vector_store._make_sync_session() as session:
        collection = vector_store.get_collection(session)
        if collection is None:
            return []

        stmt = select(
            vector_store.EmbeddingStore.document,
            vector_store.EmbeddingStore.cmetadata,
        ).where(vector_store.EmbeddingStore.collection_id == collection.uuid)

        if doc_types:
            stmt = stmt.where(
                vector_store.EmbeddingStore.cmetadata["doc_type"].astext.in_(doc_types)
            )
        if project_id is not None:
            stmt = stmt.where(
                vector_store.EmbeddingStore.cmetadata["project_id"].astext
                == str(project_id)
            )

        stmt = stmt.limit(limit)
        rows = session.execute(stmt).all()

    documents: list[Document] = []
    for document, metadata in rows:
        documents.append(
            Document(page_content=document or "", metadata=metadata or {})
        )
    return documents


def list_admin_knowledge(agent_id: int) -> list[dict]:
    documents = fetch_documents_by_metadata(
        agent_id,
        doc_types=["admin_knowledge"],
        limit=500,
    )
    grouped: dict[str, dict] = {}
    for document in documents:
        metadata = document.metadata or {}
        source_id = metadata.get("source_id", "")
        if not source_id:
            continue
        if source_id not in grouped:
            grouped[source_id] = {
                "source_id": source_id,
                "title": metadata.get("title", source_id),
                "chunk_count": 0,
            }
        grouped[source_id]["chunk_count"] += 1

    return sorted(grouped.values(), key=lambda item: item["title"].lower())


def is_inventory_query(query: str) -> bool:
    return bool(INVENTORY_QUERY_PATTERN.search(query))


def search_agent_context(
    agent_id: int,
    query: str,
    *,
    agent_task_id: int | None = None,
    project_id: int | None = None,
    exclude_task_id: int | None = None,
    doc_types: list[str] | None = None,
    k: int | None = None,
) -> list[Document]:
    if k is None:
        k = int(os.getenv("CHAT_RAG_TOP_K", "8"))

    if is_inventory_query(query):
        return fetch_documents_by_metadata(
            agent_id,
            doc_types=["project_catalog", "project_record"],
        )

    vector_store = get_vector_store(agent_id)
    metadata_filter: dict = {"is_latest": True}
    if agent_task_id is not None:
        metadata_filter["agent_task_id"] = str(agent_task_id)
    if project_id is not None:
        metadata_filter["project_id"] = str(project_id)
    if doc_types:
        metadata_filter["doc_type"] = {"$in": doc_types}

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": k,
            "filter": metadata_filter,
        }
    )
    documents = retriever.invoke(query)

    if exclude_task_id is not None:
        exclude = str(exclude_task_id)
        documents = [
            document
            for document in documents
            if (document.metadata or {}).get("agent_task_id") != exclude
        ]

    if documents:
        return documents

    if doc_types:
        return documents

    return fetch_documents_by_metadata(
        agent_id,
        doc_types=["project_catalog", "project_record"],
        project_id=project_id,
        limit=5,
    ) + vector_store.similarity_search(
        query,
        k=k,
        filter={
            **metadata_filter,
            "doc_type": {"$in": ["task_description", "task_result", "admin_knowledge"]},
        },
    )


def search_task_context(
    agent_id: int,
    agent_task_id: int,
    query: str,
    doc_types: list[str] | None = None,
    k: int = 5,
) -> list[Document]:
    return search_agent_context(
        agent_id,
        query,
        agent_task_id=agent_task_id,
        doc_types=doc_types,
        k=k,
    )


def reindex_agent_task(task: AgentTask) -> None:
    task = AgentTask.objects.select_related("project", "agent").get(pk=task.pk)
    ingest_project_record(agent_id=task.agent_id, project=task.project)
    rebuild_project_catalog(agent_id=task.agent_id)
    ingest_task_description(task=task)
    if task.result.strip():
        ingest_task_result(task=task)
