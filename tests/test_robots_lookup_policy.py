from __future__ import annotations

from pathlib import Path

from ttc.adapters.robots_store import FixtureRobots
from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker

ROOT = Path(__file__).resolve().parents[1]


def test_per_origin_robots_lookup_gates_policy() -> None:
    lookup = FixtureRobots(
        {"https://example.com": ROOT / "tests" / "fixtures" / "robots.txt"}
    )
    broker = PolicyBroker(
        frozenset({"https://example.com/private", "https://example.com/public"}),
        DEFAULT_GRANTED,
        robots_lookup=lookup,
    )
    denied = broker.authorize("https://example.com/private", profile_id="jobs")
    allowed = broker.authorize("https://example.com/public", profile_id="jobs")
    assert denied.allowed is False
    assert denied.reason == "robots_disallow"
    assert allowed.allowed is True
