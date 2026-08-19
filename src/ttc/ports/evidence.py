from __future__ import annotations

from typing import Protocol

from ttc.domain.models import Evidence


class EvidenceStorePort(Protocol):
    def put(self, evidence: Evidence) -> Evidence:
        """Persist immutable evidence. Same bytes, same identity."""

    def get(self, evidence_id: str) -> Evidence:
        """Resolve accepted evidence by id. Missing evidence is a hard error."""
