from __future__ import annotations

from ttc.domain.urls import canonicalize


def detect_redirect_loop(hops: tuple[str, ...]) -> bool:
    seen: set[str] = set()
    for hop in hops:
        canonical = canonicalize(hop)
        if canonical in seen:
            return True
        seen.add(canonical)
    return False
