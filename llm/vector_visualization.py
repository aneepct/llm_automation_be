from __future__ import annotations

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sqlalchemy import select

from .vector_store import collection_name_for_agent, get_vector_store

DOC_TYPE_COLORS = {
    "project_record": "#8b5cf6",
    "project_catalog": "#f59e0b",
    "task_description": "#3b82f6",
    "task_result": "#22c55e",
}
DEFAULT_COLOR = "#94a3b8"


def _embedding_to_list(embedding) -> list[float]:
    if embedding is None:
        return []
    if isinstance(embedding, (list, tuple)):
        return [float(value) for value in embedding]
    if isinstance(embedding, np.ndarray):
        return embedding.astype(float).tolist()
    if isinstance(embedding, str):
        stripped = embedding.strip("[]")
        if not stripped:
            return []
        return [float(part) for part in stripped.split(",")]
    return [float(value) for value in list(embedding)]


def fetch_collection_rows(agent_id: int) -> list[dict]:
    vector_store = get_vector_store(agent_id)
    with vector_store._make_sync_session() as session:
        collection = vector_store.get_collection(session)
        if collection is None:
            return []

        rows = session.execute(
            select(
                vector_store.EmbeddingStore.embedding,
                vector_store.EmbeddingStore.document,
                vector_store.EmbeddingStore.cmetadata,
            ).where(vector_store.EmbeddingStore.collection_id == collection.uuid)
        ).all()

    results: list[dict] = []
    for embedding, document, metadata in rows:
        meta = metadata or {}
        doc_type = meta.get("doc_type", "unknown")
        preview = (document or "")[:100]
        if document and len(document) > 100:
            preview += "..."

        results.append(
            {
                "embedding": _embedding_to_list(embedding),
                "document": document or "",
                "doc_type": doc_type,
                "color": DOC_TYPE_COLORS.get(doc_type, DEFAULT_COLOR),
                "agent_task_id": meta.get("agent_task_id", ""),
                "title": meta.get("title", ""),
                "hover_text": f"Type: {doc_type}<br>Text: {preview}",
            }
        )
    return results


def _pad_components(reduced: np.ndarray, n_components: int) -> np.ndarray:
    if reduced.shape[1] >= n_components:
        return reduced[:, :n_components]
    padding = np.zeros((reduced.shape[0], n_components - reduced.shape[1]))
    return np.hstack([reduced, padding])


def reduce_dimensions(vectors: np.ndarray, n_components: int) -> np.ndarray:
    count = vectors.shape[0]
    if count == 0:
        return np.empty((0, n_components))
    if count == 1:
        return np.zeros((1, n_components))
    if count <= 3:
        pca = PCA(n_components=min(n_components, count))
        return _pad_components(pca.fit_transform(vectors), n_components)

    perplexity = min(30, count - 1)
    tsne = TSNE(
        n_components=n_components,
        random_state=42,
        perplexity=perplexity,
        init="pca",
        learning_rate="auto",
    )
    return tsne.fit_transform(vectors)


def build_visualization(agent_id: int, dims: int) -> dict:
    if dims not in (2, 3):
        raise ValueError("dims must be 2 or 3")

    rows = fetch_collection_rows(agent_id)
    collection_name = collection_name_for_agent(agent_id)

    if not rows:
        return {
            "dims": dims,
            "collection_name": collection_name,
            "point_count": 0,
            "points": [],
        }

    vectors = np.array([row["embedding"] for row in rows], dtype=float)
    reduced = reduce_dimensions(vectors, dims)

    points = []
    for index, row in enumerate(rows):
        point = {
            "x": float(reduced[index, 0]),
            "y": float(reduced[index, 1]),
            "doc_type": row["doc_type"],
            "color": row["color"],
            "hover_text": row["hover_text"],
            "agent_task_id": row["agent_task_id"],
            "title": row["title"],
        }
        if dims == 3:
            point["z"] = float(reduced[index, 2])
        points.append(point)

    return {
        "dims": dims,
        "collection_name": collection_name,
        "point_count": len(points),
        "points": points,
    }


def build_plotly_html(agent_id: int, dims: int) -> tuple[str, int]:
    import plotly.graph_objects as go

    data = build_visualization(agent_id, dims)
    collection_name = data["collection_name"]
    points = data["points"]
    point_count = data["point_count"]

    if not points:
        return "", 0

    hover_texts = [point["hover_text"] for point in points]
    colors = [point["color"] for point in points]

    if dims == 2:
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=[point["x"] for point in points],
                    y=[point["y"] for point in points],
                    mode="markers",
                    marker=dict(size=8, color=colors, opacity=0.85),
                    text=hover_texts,
                    hoverinfo="text",
                )
            ]
        )
        fig.update_layout(
            title=f"2D PGVector — {collection_name}",
            xaxis_title="x",
            yaxis_title="y",
            width=900,
            height=600,
            margin=dict(r=20, b=40, l=40, t=48),
        )
    else:
        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=[point["x"] for point in points],
                    y=[point["y"] for point in points],
                    z=[point.get("z", 0) for point in points],
                    mode="markers",
                    marker=dict(size=4, color=colors, opacity=0.85),
                    text=hover_texts,
                    hoverinfo="text",
                )
            ]
        )
        fig.update_layout(
            title=f"3D PGVector — {collection_name}",
            scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
            width=900,
            height=700,
            margin=dict(r=10, b=10, l=10, t=48),
        )

    return fig.to_html(full_html=False, include_plotlyjs="cdn"), point_count
