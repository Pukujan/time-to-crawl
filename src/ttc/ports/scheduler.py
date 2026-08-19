from __future__ import annotations

from typing import Protocol

from ttc.domain.scheduler import WorkItem


class SchedulerPort(Protocol):
    def enqueue(self, url: str, kind: str) -> WorkItem:
        """Enqueue DISCOVER or REFRESH work. Engine URL-seen must not hide REFRESH."""

    def claim(self, url: str, kind: str) -> WorkItem:
        """Lease work. Stale generations cannot complete."""

    def complete(self, item: WorkItem, evidence_id: str) -> WorkItem:
        """Complete only with evidence and a live lease."""
