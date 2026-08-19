from __future__ import annotations

LIVE_ENGINES = frozenset({"crawlee", "scrapy"})
ENABLED: set[str] = {"fake"}
DISABLED: set[str] = set()


def enable(engine_id: str) -> None:
    if engine_id in LIVE_ENGINES:
        raise PermissionError("engine_enable_blocked_until_issue_4")
    DISABLED.discard(engine_id)
    ENABLED.add(engine_id)


def disable(engine_id: str) -> None:
    ENABLED.discard(engine_id)
    DISABLED.add(engine_id)


def is_enabled(engine_id: str) -> bool:
    if engine_id in LIVE_ENGINES:
        return False
    if engine_id in DISABLED:
        return False
    return True
