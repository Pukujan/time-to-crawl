from __future__ import annotations

from typing import Protocol

from ttc.domain.models import TypedRecord


class OperationalCatalogPort(Protocol):
    def persist(self, records: tuple[TypedRecord, ...]) -> None:
        """Write operational typed records. Does not own evidence bytes."""

    def list_by_profile(self, profile_id: str) -> tuple[TypedRecord, ...]:
        """Return current records for one profile."""
