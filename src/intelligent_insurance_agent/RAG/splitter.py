"""Text chunking utilities for RAG."""

from __future__ import annotations

from typing import List

from ..Model.document import Document


def split_document(document: Document, chunk_size: int = 300) -> List[str]:
    text = document.content or ""
    if not text:
        return []
    words = text.split()
    chunks: List[str] = []
    for index in range(0, len(words), chunk_size):
        chunk = " ".join(words[index:index + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
