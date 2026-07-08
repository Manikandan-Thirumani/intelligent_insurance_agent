"""Chat model abstractions for the insurance assistant."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import List, Optional

from ..llm import OllamaLLMClient

STOP_WORDS = {
    "the",
    "is",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "in",
    "for",
    "with",
    "on",
    "that",
    "this",
    "it",
    "as",
    "are",
    "be",
    "can",
    "any",
    "please",
}


@dataclass
class ChatMessage:
    role: str
    content: str


class ChatModel:
    """A lightweight chat interface with optional local Ollama integration."""

    def __init__(self, system_prompt: Optional[str] = None, llm_client: Optional[object] = None) -> None:
        self.system_prompt = system_prompt or "You are a helpful insurance assistant."
        self.llm_client = llm_client
        if self.llm_client is None and os.getenv("USE_OLLAMA", "false").lower() in {"1", "true", "yes"}:
            try:
                self.llm_client = OllamaLLMClient()
            except Exception:
                self.llm_client = None

    def generate(self, messages: List[ChatMessage]) -> str:
        if not messages:
            return "I can help with insurance questions and claims."

        last_message = messages[-1]
        if "Context:" in last_message.content and "Question:" in last_message.content:
            question = last_message.content.split("Question:", 1)[1].strip()
            context = last_message.content.split("Context:", 1)[1].rsplit("Question:", 1)[0].strip()
            llm_reply = self._generate_with_llm(question, context)
            if llm_reply:
                return llm_reply
            answer = self._answer_from_context(question, context)
            if answer:
                return answer
            return "I found information in the documents but could not answer your question directly."

        last_user_message = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return f"Assistant response to: {last_user_message}".strip()

    def _generate_with_llm(self, question: str, context: str) -> str:
        if self.llm_client is None:
            return ""

        try:
            prompt = (
                f"{self.system_prompt}\n\n"
                "Use the context below to answer the user's question. "
                "If the answer is not explicitly present in the context, say that you cannot find it there.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {question}"
            )
            reply = self.llm_client.generate(prompt)
            if reply:
                return reply.strip()
        except Exception:
            return ""
        return ""

    def _answer_from_context(self, question: str, context: str) -> str:
        if not context:
            return "I could not find any document content to answer your question."

        sentences = re.split(r"(?<=[.!?])\s+|\n+", context)
        question_words = [
            word
            for word in re.findall(r"\w+", question.lower())
            if word not in STOP_WORDS
        ]

        scored_sentences = []
        for sentence in sentences:
            sentence_words = set(re.findall(r"\w+", sentence.lower()))
            overlap = sum(1 for word in question_words if word in sentence_words)
            if overlap > 0:
                scored_sentences.append((overlap, sentence.strip()))

        if scored_sentences:
            best_match = max(scored_sentences, key=lambda item: item[0])[1]
            return best_match

        keyword_snippet = self._find_keyword_snippet(question_words, context)
        if keyword_snippet:
            return keyword_snippet

        return self._summarize_context(context)

    def _find_keyword_snippet(self, question_words: List[str], context: str) -> str:
        lower_context = context.lower()
        for word in question_words:
            idx = lower_context.find(word)
            if idx != -1:
                start = max(0, idx - 80)
                end = min(len(context), idx + 220)
                snippet = context[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(context):
                    snippet = snippet + "..."
                return f"I found this information in your documents: {snippet}"
        return ""

    def _summarize_context(self, context: str) -> str:
        sentences = re.split(r"(?<=[.!?])\s+|\n+", context)
        if sentences:
            snippet = sentences[0].strip()
            return f"I found this information in your documents: {snippet}"
        return "I found content in the documents but could not generate a concise answer."
