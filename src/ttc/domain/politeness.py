from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Politeness:
    min_delay_ms: int
    last_fetch_at: int | None = None


def next_allowed_at(politeness: Politeness) -> int:
    if politeness.last_fetch_at is None:
        return 0
    return politeness.last_fetch_at + politeness.min_delay_ms


def can_fetch(politeness: Politeness, *, now: int) -> bool:
    return now >= next_allowed_at(politeness)
