from __future__ import annotations

from ttc.domain.scheduler import KIND_REFRESH, Scheduler


def test_scheduler_respects_freshness_window() -> None:
    scheduler = Scheduler()
    url = "https://example.com/item"
    scheduler.enqueue(url, KIND_REFRESH)
    claimed = scheduler.claim(url, KIND_REFRESH)
    scheduler.complete(claimed, "ev_1", now=10)
    assert scheduler.maybe_due_refresh(url, now=12, interval=5) is None
    due = scheduler.maybe_due_refresh(url, now=16, interval=5)
    assert due is not None
    assert due.due is True
