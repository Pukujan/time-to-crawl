from __future__ import annotations

from ttc.adapters.memory import AllowlistPolicy
from ttc.application.outlinks import enqueue_authorized_outlinks
from ttc.domain.scheduler import KIND_DISCOVER, Scheduler


def test_outlink_enqueue_requires_policy_and_drops_forbidden() -> None:
    scheduler = Scheduler()
    policy = AllowlistPolicy(frozenset({"https://example.com/a", "https://example.com/b"}))
    accepted = enqueue_authorized_outlinks(
        scheduler,
        (
            "https://example.com/a",
            "http://127.0.0.1/admin",
            "https://evil.example/x",
            "https://example.com/b",
        ),
        policy=policy,
        profile_id="jobs",
    )
    assert accepted == ("https://example.com/a", "https://example.com/b")
    assert scheduler.get("https://example.com/a", KIND_DISCOVER).due is True
    assert scheduler.get("https://example.com/b", KIND_DISCOVER).due is True


def test_outlink_enqueue_respects_limit() -> None:
    scheduler = Scheduler()
    policy = AllowlistPolicy(
        frozenset({"https://example.com/a", "https://example.com/b", "https://example.com/c"})
    )
    accepted = enqueue_authorized_outlinks(
        scheduler,
        (
            "https://example.com/a",
            "https://example.com/b",
            "https://example.com/c",
        ),
        policy=policy,
        profile_id="jobs",
        limit=2,
    )
    assert accepted == ("https://example.com/a", "https://example.com/b")
