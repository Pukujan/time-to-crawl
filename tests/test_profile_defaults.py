from __future__ import annotations

from ttc.cli import load_reference_profiles


def test_all_reference_profiles_default_to_same_host_and_fetch_public() -> None:
    profiles = load_reference_profiles()
    assert set(profiles) == {
        "products-and-offers",
        "jobs",
        "inference-providers",
        "legal-documents",
    }
    for profile in profiles.values():
        assert profile.same_host_only is True
        assert "fetch_public" in profile.requested_capabilities
        assert "anti_block" not in profile.requested_capabilities
        assert profile.max_outlinks > 0
        assert profile.max_depth >= 0
