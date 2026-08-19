from __future__ import annotations

from typing import Protocol


class ClockPort(Protocol):
    def now(self) -> int:
        """Return a monotonic-ish unix epoch used by scheduler freshness and leases."""
