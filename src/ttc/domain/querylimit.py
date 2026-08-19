from __future__ import annotations


def clamp_limit(limit: int | None, *, default: int = 50, maximum: int = 200) -> int:
    if limit is None:
        return default
    if limit < 1:
        raise PermissionError("limit_too_small")
    if limit > maximum:
        raise PermissionError("limit_too_large")
    return limit
