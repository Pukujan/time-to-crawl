from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker
from ttc.domain.registry import SourceRegistry


def test_require_source_auth_blocks_until_human_capability() -> None:
    registry = SourceRegistry()
    url = "https://example.com/item"
    registry.propose(url, proposed_by="agent", profile_id="jobs")
    broker = PolicyBroker(
        frozenset({url}),
        DEFAULT_GRANTED,
        source_registry=registry,
        require_source_auth=True,
    )
    denied = broker.authorize(url, profile_id="jobs")
    assert denied.allowed is False
    assert denied.reason == "source_unauthorized"
    registry.authorize(url, actor="human", capability="source_authorize")
    allowed = broker.authorize(url, profile_id="jobs")
    assert allowed.allowed is True
