from __future__ import annotations

from typing import Protocol

from ttc.domain.models import TypedRecord


class QueryViewPort(Protocol):
    def list_records(self, profile_id: str) -> tuple[TypedRecord, ...]:
        """Harness-neutral typed query. No storage credentials leak through this surface."""
