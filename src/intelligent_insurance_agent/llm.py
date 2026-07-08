"""Lightweight Llama/Ollama client for the insurance assistant."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Optional


class OllamaLLMClient:
    """Call a local Ollama-compatible Llama server."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None) -> None:
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2:latest")

    def generate(self, prompt: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            raise RuntimeError(f"Unable to reach Ollama at {self.base_url}: {exc}") from exc

        data = json.loads(body)
        reply = data.get("response", "")
        return reply.strip()
