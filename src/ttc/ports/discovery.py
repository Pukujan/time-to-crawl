from __future__ import annotations

from typing import Protocol


class DiscoveryProviderPort(Protocol):
    def discover(self, query: str, *, profile_id: str) -> tuple[str, ...]:
        """Return candidate URLs. Candidates are not authorized by discovery."""
