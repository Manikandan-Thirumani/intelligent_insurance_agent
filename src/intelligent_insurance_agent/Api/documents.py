from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DocumentSummary(BaseModel):
    filename: str
    size: int
    path: str


@router.get("/documents", response_model=List[DocumentSummary])
def documents() -> List[DocumentSummary]:
    from .. import api

    files = []
    for path in sorted(api.UPLOAD_DIR.iterdir()):
        if path.is_file():
            files.append(
                DocumentSummary(
                    filename=path.name,
                    size=path.stat().st_size,
                    path=str(path.resolve()),
                )
            )
    return files
