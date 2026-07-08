"""Retrieval helpers for the in-memory vector store."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from .embedding import generate_embedding
from .vectorstore import VectorStore


def retrieve_similar_chunks(query: str, store: VectorStore, top_k: int = 3) -> List[Tuple[str, List[float]]]:
    query_embedding = generate_embedding(query)
    scored_items = []
    for chunk, embedding in store.list():
        score = sum(abs(q - e) for q, e in zip(query_embedding, embedding)) if query_embedding and embedding else 0.0
        scored_items.append((score, chunk, embedding))
    scored_items.sort(key=lambda item: item[0])
    return [(chunk, embedding) for _, chunk, embedding in scored_items[:top_k]]
