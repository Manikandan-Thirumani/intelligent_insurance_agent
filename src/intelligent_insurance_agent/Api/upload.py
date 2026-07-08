from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from .rag import rag_app

router = APIRouter()


class DocumentSummary(BaseModel):
    filename: str
    size: int
    path: str


@router.post("/upload", response_model=DocumentSummary)
async def upload(file: UploadFile = File(...)) -> DocumentSummary:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    safe_name = Path(file.filename).name
    from .. import api

    destination = api.UPLOAD_DIR / safe_name
    with destination.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    rag_app.ingest_documents([destination])

    return DocumentSummary(
        filename=safe_name,
        size=destination.stat().st_size,
        path=str(destination.resolve()),
    )
