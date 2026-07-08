"""A simple in-memory vector store for RAG."""

from __future__ import annotations

from typing import List, Tuple


class VectorStore:
    def __init__(self) -> None:
        self._items: List[Tuple[str, List[float]]] = []

    def add(self, chunk: str, embedding: List[float]) -> None:
        self._items.append((chunk, embedding))

    def add_many(self, items: List[Tuple[str, List[float]]]) -> None:
        for chunk, embedding in items:
            self.add(chunk, embedding)

    def list(self) -> List[Tuple[str, List[float]]]:
        return list(self._items)
