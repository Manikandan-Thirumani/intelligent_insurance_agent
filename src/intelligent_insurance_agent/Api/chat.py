from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from ..agent import generate_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    reply = generate_response(req.message)
    return ChatResponse(reply=reply)
