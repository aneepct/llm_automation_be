import json
import logging
import os

from openai import OpenAI

from .models import AgentTask, ChatMessage, LlmAgent
from .tools.registry import execute_tool, get_openai_tools, reload_registry
from .vector_store import (
    fetch_documents_by_metadata,
    is_inventory_query,
    search_agent_context,
)

MAX_TOOL_ITERATIONS = 10
logger = logging.getLogger(__name__)

RAG_CONTEXT_TEMPLATE = """## Retrieved knowledge (vector database)
Answer ONLY using facts from the excerpts below.
- For project names and counts, use ONLY names listed in project_catalog and project_record sections.
- If the excerpts do not contain enough information, say you do not have that data — do NOT invent project names.
- Prefer retrieved knowledge for task-specific and project-specific facts.

{context}"""


class LlmAgentService:
    @staticmethod
    def build_client(agent: LlmAgent) -> OpenAI:
        if agent.use_other_agent:
            return OpenAI(base_url=agent.base_url, api_key=agent.api_key)
        return OpenAI(api_key=agent.api_key)

    @staticmethod
    def build_system_message(agent: LlmAgent) -> str:
        system_content = agent.role.strip()
        if agent.context.strip():
            system_content = f"{system_content}\n\n{agent.context.strip()}"
        return system_content

    @classmethod
    def _is_rag_enabled(cls) -> bool:
        return os.getenv("CHAT_RAG_ENABLED", "true").lower() not in (
            "false",
            "0",
            "no",
        )

    @classmethod
    def _resolve_project_id(
        cls,
        agent_task_id: int | None,
        project_id: int | None = None,
    ) -> int | None:
        if project_id is not None:
            return project_id
        if agent_task_id is None:
            return None
        return (
            AgentTask.objects.filter(pk=agent_task_id)
            .values_list("project_id", flat=True)
            .first()
        )

    @classmethod
    def _build_rag_context_block(
        cls,
        agent_id: int,
        query: str,
        agent_task_id: int | None = None,
        project_id: int | None = None,
        exclude_task_id: int | None = None,
    ) -> str:
        if not cls._is_rag_enabled():
            return ""

        resolved_project_id = cls._resolve_project_id(agent_task_id, project_id)

        try:
            if is_inventory_query(query):
                documents = search_agent_context(agent_id, query)
            else:
                documents = search_agent_context(
                    agent_id,
                    query,
                    agent_task_id=agent_task_id,
                    project_id=resolved_project_id,
                    exclude_task_id=exclude_task_id,
                    doc_types=["task_description", "task_result", "project_record", "admin_knowledge"],
                )
                catalog_docs = fetch_documents_by_metadata(
                    agent_id,
                    doc_types=["project_catalog", "project_record"],
                    project_id=resolved_project_id,
                )
                seen_content = {document.page_content for document in documents}
                for document in catalog_docs:
                    if document.page_content not in seen_content:
                        documents.insert(0, document)
                        seen_content.add(document.page_content)
        except Exception as exc:
            logger.warning("RAG retrieval failed for agent %s: %s", agent_id, exc)
            return ""

        if not documents:
            return ""

        parts: list[str] = []
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            header = (
                f"[{index}] project={metadata.get('project_name', '')} "
                f"task_id={metadata.get('agent_task_id', '')} "
                f"type={metadata.get('doc_type', '')} "
                f"title={metadata.get('title', '')}"
            )
            parts.append(f"{header}\n{document.page_content}")

        return RAG_CONTEXT_TEMPLATE.format(context="\n\n---\n\n".join(parts))

    @classmethod
    def _build_system_content(
        cls,
        agent: LlmAgent,
        prompt: str,
        agent_task_id: int | None = None,
        project_id: int | None = None,
        exclude_task_id: int | None = None,
    ) -> str:
        system_content = cls.build_system_message(agent)
        rag_block = cls._build_rag_context_block(
            agent.id,
            prompt,
            agent_task_id=agent_task_id,
            project_id=project_id,
            exclude_task_id=exclude_task_id,
        )
        if rag_block:
            system_content = f"{system_content}\n\n{rag_block}"
        return system_content

    @classmethod
    def get_agent_tool_names(cls, agent: LlmAgent) -> list[str]:
        return list(
            agent.tools.filter(active=True, file_generated=True).values_list("name", flat=True)
        )

    @classmethod
    def build_openai_tools(cls, agent: LlmAgent) -> list[dict]:
        tool_names = cls.get_agent_tool_names(agent)
        if not tool_names:
            return []
        reload_registry()
        return get_openai_tools(tool_names)

    @classmethod
    def build_messages(
        cls,
        agent: LlmAgent,
        prompt: str,
        event_id: str,
        agent_task_id: int | None = None,
    ) -> list[dict]:
        messages: list[dict] = [
            {
                "role": "system",
                "content": cls._build_system_content(
                    agent,
                    prompt,
                    agent_task_id=agent_task_id,
                ),
            }
        ]

        history = ChatMessage.objects.filter(
            event_id=event_id,
            agent=agent,
        ).order_by("created_at")

        for message in history:
            messages.append({"role": message.role, "content": message.content})

        messages.append({"role": "user", "content": prompt})
        return messages

    @classmethod
    def _message_to_dict(cls, message) -> dict:
        data = {
            "role": message.role,
            "content": message.content or "",
        }
        if message.tool_calls:
            data["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in message.tool_calls
            ]
        return data

    @classmethod
    def _complete_with_tools(
        cls,
        client: OpenAI,
        agent: LlmAgent,
        messages: list[dict],
    ) -> str:
        tools = cls.build_openai_tools(agent)
        kwargs: dict = {
            "model": agent.model.name,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        for _ in range(MAX_TOOL_ITERATIONS):
            response = client.chat.completions.create(**kwargs)
            message = response.choices[0].message

            if not message.tool_calls:
                return message.content or ""

            messages.append(cls._message_to_dict(message))

            for tool_call in message.tool_calls:
                arguments = json.loads(tool_call.function.arguments or "{}")
                result = execute_tool(tool_call.function.name, arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        return "Error: tool loop exceeded maximum iterations."

    @classmethod
    def run(cls, agent: LlmAgent, prompt: str, event_id: str, agent_task_id: int | None = None) -> str:
        client = cls.build_client(agent)
        messages = cls.build_messages(agent, prompt, event_id, agent_task_id)
        content = cls._complete_with_tools(client, agent, messages)
        cls._save_exchange(agent, event_id, prompt, content)
        return content

    @classmethod
    def run_task(
        cls,
        agent: LlmAgent,
        prompt: str,
        *,
        project_id: int | None = None,
        exclude_task_id: int | None = None,
    ) -> str:
        client = cls.build_client(agent)
        system_content = cls._build_system_content(
            agent,
            prompt,
            project_id=project_id,
            exclude_task_id=exclude_task_id,
        )
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ]
        return cls._complete_with_tools(client, agent, messages)

    @classmethod
    def run_stream(
        cls,
        agent: LlmAgent,
        prompt: str,
        event_id: str,
        agent_task_id: int | None = None,
    ):
        client = cls.build_client(agent)
        messages = cls.build_messages(agent, prompt, event_id, agent_task_id)
        content = cls._complete_with_tools(client, agent, messages)

        chunk_size = 24
        for index in range(0, len(content), chunk_size):
            yield content[index : index + chunk_size]

        cls._save_exchange(agent, event_id, prompt, content)

    @staticmethod
    def _save_exchange(
        agent: LlmAgent,
        event_id: str,
        prompt: str,
        content: str,
    ) -> None:
        ChatMessage.objects.create(
            event_id=event_id,
            agent=agent,
            role=ChatMessage.Role.USER,
            content=prompt,
        )
        ChatMessage.objects.create(
            event_id=event_id,
            agent=agent,
            role=ChatMessage.Role.ASSISTANT,
            content=content,
        )
                                                                  