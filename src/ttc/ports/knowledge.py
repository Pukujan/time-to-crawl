from __future__ import annotations

from typing import Protocol


class KnowledgePort(Protocol):
    def record_lesson(self, profile_id: str, statement: str, evidence_id: str) -> str:
        """Store selected durable learned knowledge. Must not overwrite operational evidence."""
