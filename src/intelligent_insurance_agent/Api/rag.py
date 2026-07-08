"""RAG chat endpoint using the shared InsuranceRAGApp."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..main import InsuranceRAGApp

router = APIRouter()
rag_app = InsuranceRAGApp()


class RAGChatRequest(BaseModel):
    prompt: str


class RAGChatResponse(BaseModel):
    response: str


@router.post("/rag-chat", response_model=RAGChatResponse)
def rag_chat(req: RAGChatRequest) -> RAGChatResponse:
    response = rag_app.answer_query(req.prompt)
    return RAGChatResponse(response=response)


def ingest_existing_documents(upload_dir: Path) -> int:
    file_paths = [path for path in upload_dir.iterdir() if path.is_file()]
    return rag_app.ingest_documents(file_paths)
