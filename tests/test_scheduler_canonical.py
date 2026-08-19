from __future__ import annotations

from ttc.domain.scheduler import KIND_REFRESH, Scheduler


def test_scheduler_canonicalizes_duplicate_urls() -> None:
    scheduler = Scheduler()
    first = scheduler.enqueue("HTTPS://Example.COM/item/#x", KIND_REFRESH)
    second = scheduler.enqueue("https://example.com/item", KIND_REFRESH)
    assert first.url == "https://example.com/item"
    assert second.url == "https://example.com/item"
    stored = scheduler.get("HTTPS://Example.COM/item/#frag", KIND_REFRESH)
    assert stored.url == "https://example.com/item"
