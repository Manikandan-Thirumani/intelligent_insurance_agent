"""Loading utilities for RAG documents."""

from __future__ import annotations

from pathlib import Path
from typing import List

from ..Model.document import Document


def load_documents(paths: List[str | Path]) -> List[Document]:
    documents: List[Document] = []
    for path in paths:
        document_path = Path(path)
        if document_path.exists():
            documents.append(Document.from_file(document_path))
    return documents
