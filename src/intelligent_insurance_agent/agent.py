"""Simple insurance assistant helpers."""

from __future__ import annotations

import os
from typing import Optional

from .llm import OllamaLLMClient


def classify_intent(message: str) -> str:
    """Classify a user message into a simple intent bucket."""
    lowered = message.lower()

    if any(keyword in lowered for keyword in ("claim", "accident", "damage", "incident")):
        return "claim"
    if any(keyword in lowered for keyword in ("quote", "premium", "price", "cost", "coverage")):
        return "quote"
    if any(keyword in lowered for keyword in ("policy", "benefit", "deductible", "exclusion")):
        return "policy_info"
    return "general"


def generate_response(message: str, llm_client: Optional[object] = None) -> str:
    """Create a helpful response using Llama when enabled, else fall back to canned responses."""
    use_ollama = os.getenv("USE_OLLAMA", "false").lower() in ("1", "true", "yes")

    if llm_client is None and use_ollama:
        try:
            llm_client = OllamaLLMClient()
        except Exception:
            llm_client = None

    if llm_client is not None:
        try:
            prompt = (
                "You are a helpful insurance assistant. Respond briefly and clearly to the user's request: "
                f"{message}"
            )
            llm_reply = llm_client.generate(prompt)
            if llm_reply:
                return llm_reply
        except Exception:
            pass

    intent = classify_intent(message)

    if intent == "claim":
        return "I can help you start a claim. Please share the date of the incident and a brief description."
    if intent == "quote":
        return "I can help with a quote. Tell me your coverage needs, location, and relevant policy details."
    if intent == "policy_info":
        return "I can explain your policy coverage, deductibles, and exclusions in more detail."
    return "Hello! I can help with claims, policy questions, or quotes."


def main() -> None:
    """Run a small command-line demo of the assistant."""
    user_input = input("You: ")
    print(f"Assistant: {generate_response(user_input)}")


if __name__ == "__main__":
    main()
