from __future__ import annotations

import pytest

from ttc.adapters.discovery import FixtureDiscovery
from ttc.domain.registry import SourceRegistry


def test_discovery_candidates_are_not_authorized() -> None:
    discovery = FixtureDiscovery(
        {
            "widget": (
                "https://alpha.example/widget",
                "http://127.0.0.1/admin",
                "http://169.254.169.254/latest/meta-data/",
            )
        }
    )
    found = discovery.discover("widget", profile_id="products-and-offers")
    assert found == ("https://alpha.example/widget",)


def test_source_proposal_is_unauthorized_until_explicit_capability() -> None:
    registry = SourceRegistry()
    record = registry.propose(
        "https://alpha.example/widget",
        proposed_by="agent",
        profile_id="products-and-offers",
    )
    assert record.authorized is False
    assert registry.is_authorized("https://alpha.example/widget") is False
    with pytest.raises(PermissionError, match="capability_denied"):
        registry.authorize(
            "https://alpha.example/widget",
            actor="agent",
            capability="fetch_public",
        )
    authorized = registry.authorize(
        "https://alpha.example/widget",
        actor="human",
        capability="source_authorize",
    )
    assert authorized.authorized is True


def test_source_registry_rejects_forbidden_proposals() -> None:
    registry = SourceRegistry()
    with pytest.raises(PermissionError, match="forbidden_network"):
        registry.propose("http://127.0.0.1/", proposed_by="agent", profile_id="jobs")
