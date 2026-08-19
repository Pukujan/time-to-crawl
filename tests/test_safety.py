from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker
from ttc.domain.safety import default_anti_block_is_off, engine_config_cannot_enable_anti_block


def test_anti_block_defaults_off_and_needs_capability() -> None:
    assert default_anti_block_is_off()
    broker = PolicyBroker(frozenset({"https://example.com/x"}), DEFAULT_GRANTED)
    denied = engine_config_cannot_enable_anti_block(
        {"retry_on_blocked": True}, broker, "https://example.com/x"
    )
    allowed = engine_config_cannot_enable_anti_block({}, broker, "https://example.com/x")
    assert denied.allowed is False
    assert "capability_denied" in denied.reason
    assert allowed.allowed is True
