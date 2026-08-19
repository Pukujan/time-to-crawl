from __future__ import annotations

from pathlib import Path

from ttc.adapters.robots_store import FixtureRobots

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_robots_store_denies_private_path() -> None:
    store = FixtureRobots(
        {"https://example.com": ROOT / "tests" / "fixtures" / "robots.txt"}
    )
    assert store.allows("https://example.com", "/public") is True
    assert store.allows("https://example.com", "/private") is False
    assert store.allows("https://other.example", "/private") is True
