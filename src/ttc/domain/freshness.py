from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Clock:
    now: int


def is_due(last_completed_at: int | None, now: int, interval: int) -> bool:
    if last_completed_at is None:
        return True
    return now - last_completed_at >= interval
