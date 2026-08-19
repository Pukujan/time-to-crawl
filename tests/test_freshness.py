from __future__ import annotations

from ttc.domain.freshness import is_due


def test_refresh_interval_is_due_after_window() -> None:
    assert is_due(None, now=10, interval=5) is True
    assert is_due(0, now=4, interval=5) is False
    assert is_due(0, now=5, interval=5) is True
