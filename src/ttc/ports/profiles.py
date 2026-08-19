from __future__ import annotations

from typing import Protocol

from ttc.domain.models import Profile


class ProfileRegistryPort(Protocol):
    def get(self, profile_id: str) -> Profile:
        """Load a versioned, non-executable profile. Missing profile is a hard error."""

    def list_ids(self) -> tuple[str, ...]:
        """Return registered profile ids."""
