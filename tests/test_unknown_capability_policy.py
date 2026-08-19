from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker


def test_unknown_capability_is_denied_by_policy() -> None:
    broker = PolicyBroker(frozenset({"https://example.com/x"}), DEFAULT_GRANTED)
    decision = broker.authorize(
        "https://example.com/x",
        profile_id="jobs",
        requested_capabilities=("shell_exec",),
    )
    assert decision.allowed is False
    assert decision.reason.startswith("unknown_capability")
