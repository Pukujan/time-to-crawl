from __future__ import annotations

from ttc.domain.loops import due_kinds
from ttc.domain.scheduler import KIND_DISCOVER, KIND_REFRESH, Scheduler, engine_seen_cannot_suppress_refresh


def test_discover_and_refresh_are_independent() -> None:
    scheduler = Scheduler()
    url = "https://example.com/item"
    scheduler.enqueue(url, KIND_DISCOVER)
    discover = scheduler.claim(url, KIND_DISCOVER)
    scheduler.complete(discover, "ev_discover")
    assert due_kinds(scheduler, url) == ()
    engine_seen: set[str] = {url}
    engine_seen_cannot_suppress_refresh(engine_seen, url, scheduler)
    assert KIND_REFRESH in due_kinds(scheduler, url)
    assert scheduler.get(url, KIND_DISCOVER).evidence_id == "ev_discover"
