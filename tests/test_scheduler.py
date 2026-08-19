from __future__ import annotations

import pytest

from ttc.domain.scheduler import (
    KIND_REFRESH,
    STATE_DONE,
    Scheduler,
    engine_seen_cannot_suppress_refresh,
)


def test_engine_dedup_cannot_suppress_refresh() -> None:
    scheduler = Scheduler()
    url = "https://example.com/item"
    first = scheduler.enqueue(url, KIND_REFRESH)
    claimed = scheduler.claim(url, KIND_REFRESH)
    scheduler.complete(claimed, "ev_1")
    seen: set[str] = {url}
    due = engine_seen_cannot_suppress_refresh(seen, url, scheduler)
    assert url in seen
    assert due.due is True
    assert due.state != STATE_DONE
    assert scheduler.get(url, KIND_REFRESH).due is True
    assert first.url == url


def test_stale_lease_cannot_complete() -> None:
    scheduler = Scheduler()
    url = "https://example.com/item"
    scheduler.enqueue(url, KIND_REFRESH)
    first = scheduler.claim(url, KIND_REFRESH)
    scheduler.cancel(url, KIND_REFRESH)
    with pytest.raises(PermissionError, match="stale_lease|cancelled"):
        scheduler.complete(first, "ev_1")
    scheduler.enqueue(url, KIND_REFRESH)
    second = scheduler.claim(url, KIND_REFRESH)
    with pytest.raises(PermissionError, match="stale_lease"):
        scheduler.complete(first, "ev_2")
    done = scheduler.complete(second, "ev_3")
    assert done.evidence_id == "ev_3"


def test_complete_requires_evidence() -> None:
    scheduler = Scheduler()
    scheduler.enqueue("https://example.com/x", KIND_REFRESH)
    leased = scheduler.claim("https://example.com/x", KIND_REFRESH)
    with pytest.raises(PermissionError, match="evidence_required"):
        scheduler.complete(leased, "")
