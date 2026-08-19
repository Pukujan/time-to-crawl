from __future__ import annotations

from typing import Protocol

from ttc.domain.models import TypedRecord


class IdentityResolverPort(Protocol):
    def resolve(self, records: tuple[TypedRecord, ...]) -> tuple[TypedRecord, ...]:
        """Assign stable record ids from profile identity keys. Must not merge distinct keys."""
