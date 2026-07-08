"""Chat model abstractions for the insurance assistant."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


class ChatModel:
    """A lightweight chat interface placeholder for future LLM integration."""

    def __init__(self, system_prompt: Optional[str] = None) -> None:
        self.system_prompt = system_prompt or "You are a helpful insurance assistant."

    def generate(self, messages: List[ChatMessage]) -> str:
        if not messages:
            return "I can help with insurance questions and claims."

        last_message = messages[-1]
        if "Context:" in last_message.content and "Question:" in last_message.content:
            question = last_message.content.split("Question:", 1)[1].strip()
            return f"Based on the retrieved context, I can help with: {question}"

        last_user_message = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return f"Assistant response to: {last_user_message}".strip()
