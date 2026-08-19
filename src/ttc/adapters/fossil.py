from __future__ import annotations

from ttc.ports.knowledge import KnowledgePort


class FossilStub:
    """Selected durable lessons only. Cannot write operational evidence."""

    def __init__(self) -> None:
        self._lessons: dict[str, tuple[str, str, str]] = {}

    def record_lesson(self, profile_id: str, statement: str, evidence_id: str) -> str:
        if not evidence_id:
            raise PermissionError("evidence_required")
        if statement.startswith("OVERWRITE_EVIDENCE:"):
            raise PermissionError("knowledge_cannot_overwrite_evidence")
        key = f"{profile_id}:{evidence_id}"
        self._lessons[key] = (profile_id, statement, evidence_id)
        return key
