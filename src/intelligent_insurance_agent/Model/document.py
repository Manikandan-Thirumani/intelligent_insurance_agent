"""Document model abstractions for the insurance assistant."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union


@dataclass
class Document:
    id: str
    content: str
    source: Optional[str] = None
    metadata: Optional[dict] = None

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "Document":
        path = Path(path)
        if not path.exists():
            return cls(id=path.name, content="", source=str(path))

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_bytes().decode("utf-8", errors="ignore")

        return cls(id=path.name, content=content, source=str(path))
