from __future__ import annotations

from typing import Protocol

LEASE_TTL = 120


class _Leased(Protocol):
    state: str
    claimed_at: int | None


def lease_expired(item: _Leased, *, now: int, ttl: int = LEASE_TTL) -> bool:
    if item.state != "LEASED" or item.claimed_at is None:
        return False
    return now - item.claimed_at > ttl
