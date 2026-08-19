from __future__ import annotations

from typing import Protocol

from ttc.domain.models import PolicyDecision


class PolicyDecisionPort(Protocol):
    def authorize(
        self,
        url: str,
        *,
        profile_id: str,
        requested_capabilities: tuple[str, ...] = (),
    ) -> PolicyDecision:
        """Authorize a destination. Every redirect must be re-authorized independently."""
