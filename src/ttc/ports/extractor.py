from __future__ import annotations

from typing import Protocol

from ttc.domain.models import Evidence, Profile, TypedRecord


class ContentExtractorPort(Protocol):
    def extract(self, evidence: Evidence, profile: Profile) -> tuple[TypedRecord, ...]:
        """Extract typed records using the profile schema. Never invent identity or grant capabilities."""
