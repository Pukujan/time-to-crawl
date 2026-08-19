from __future__ import annotations

import pytest

from ttc.adapters.memory import FileProfileRegistry, MemoryCatalog
from ttc.api.gateway import BoundedGateway
from ttc.cli import load_reference_profiles


def test_gateway_denies_arbitrary_browser_and_fetch() -> None:
    profiles = load_reference_profiles()
    gateway = BoundedGateway(MemoryCatalog(), FileProfileRegistry(profiles))
    with pytest.raises(PermissionError, match="action_denied"):
        gateway.invoke("fetch")
    with pytest.raises(PermissionError, match="action_denied"):
        gateway.invoke("browser")
    with pytest.raises(PermissionError, match="source_propose_is_not_authorize"):
        gateway.invoke("source_propose", url="https://example.com")
    profile = gateway.invoke("get_profile", profile_id="jobs")
    assert profile.profile_id == "jobs"
