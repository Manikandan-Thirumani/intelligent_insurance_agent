"""Combining chat history with retrieved context for a simple RAG chain."""

from __future__ import annotations

from typing import Optional, Sequence

from ..Model.chat import ChatMessage, ChatModel
from .retriever import retrieve_similar_chunks
from .vectorstore import VectorStore


class RAGChain:
    def __init__(self, chat_model: Optional[ChatModel] = None) -> None:
        self.chat_model = chat_model or ChatModel()

    def run(self, query: str, history: Sequence[ChatMessage], vector_store: VectorStore) -> str:
        retrieved = retrieve_similar_chunks(query, vector_store)
        context = "\n".join(chunk for chunk, _ in retrieved)
        messages = list(history) + [ChatMessage(role="user", content=query)]
        prompt = f"Context:\n{context}\n\nConversation:\n"
        for message in messages:
            prompt += f"{message.role}: {message.content}\n"
        return self.chat_model.generate([ChatMessage(role="assistant", content=prompt)])
