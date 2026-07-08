"""Embedding utilities for RAG chunks."""

from __future__ import annotations

from typing import List, Sequence, Tuple


def generate_embedding(text: str) -> List[float]:
    """Return a simple deterministic pseudo-embedding for local development."""
    words = text.lower().split()
    if not words:
        return []
    vector = [float(sum(ord(char) for char in word) % 97) / 100.0 for word in words[:10]]
    return vector


def embed_chunks(chunks: Sequence[str]) -> List[Tuple[str, List[float]]]:
    return [(chunk, generate_embedding(chunk)) for chunk in chunks]
