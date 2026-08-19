from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED, KNOWN_CAPABILITIES


def unknown_capabilities(requested: tuple[str, ...]) -> frozenset[str]:
    return frozenset(requested) - KNOWN_CAPABILITIES


def granted_or_empty(requested: tuple[str, ...]) -> frozenset[str]:
    unknown = unknown_capabilities(requested)
    if unknown:
        raise PermissionError("unknown_capability:" + ",".join(sorted(unknown)))
    return DEFAULT_GRANTED & frozenset(requested)
