from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker


def test_default_port_and_fragment_still_match_allowlist() -> None:
    broker = PolicyBroker(frozenset({"https://example.com/a"}), DEFAULT_GRANTED)
    decision = broker.authorize("HTTPS://Example.COM:443/a/#frag", profile_id="jobs")
    assert decision.allowed is True
    assert decision.url == "https://example.com/a"
