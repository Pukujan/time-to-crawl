from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker
from ttc.domain.robots import robots_allows

ROBOTS = """
User-agent: *
Disallow: /secret
Allow: /public
"""


def test_robots_disallow_is_visible_on_decision() -> None:
    broker = PolicyBroker(
        frozenset({"https://example.com/secret", "https://example.com/public"}),
        DEFAULT_GRANTED,
        robots_txt=ROBOTS,
    )
    denied = broker.authorize("https://example.com/secret", profile_id="jobs")
    allowed = broker.authorize("https://example.com/public", profile_id="jobs")
    assert denied.allowed is False
    assert denied.robots_compliant is False
    assert denied.reason == "robots_disallow"
    assert allowed.allowed is True
    assert allowed.robots_compliant is True


def test_robots_parser_matches_path_prefix() -> None:
    assert robots_allows(ROBOTS, "/secret") is False
    assert robots_allows(ROBOTS, "/public") is True
