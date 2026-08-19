from __future__ import annotations

ENABLED: set[str] = {"fake"}


def enable(engine_id: str) -> None:
    if engine_id in {"crawlee", "scrapy"}:
        raise PermissionError("engine_enable_blocked_until_issue_4")
    ENABLED.add(engine_id)


def disable(engine_id: str) -> None:
    ENABLED.discard(engine_id)


def is_enabled(engine_id: str) -> bool:
    return engine_id in ENABLED
