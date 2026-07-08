from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

from .Api import UPLOAD_DIR
from .Api.chat import router as chat_router
from .Api.documents import router as documents_router
from .Api.health import router as health_router
from .Api.rag import ingest_existing_documents, router as rag_router
from .Api.upload import router as upload_router

app = FastAPI(title="Intelligent Insurance Agent API")
static_path = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(rag_router)


@app.on_event("startup")
def startup_event() -> None:
    ingest_existing_documents(UPLOAD_DIR)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")


def main() -> None:
    uvicorn.run("intelligent_insurance_agent.api:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
