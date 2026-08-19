from __future__ import annotations

from ttc.adapters.env_discovery import EnvDiscovery


def test_env_discovery_is_offline_and_filters_forbidden(monkeypatch) -> None:
    monkeypatch.setenv(
        "TTC_DISCOVERY_FIXTURES",
        "https://example.com/a,http://127.0.0.1/x,https://example.com/b",
    )
    found = EnvDiscovery("TTC_DISCOVERY_FIXTURES").discover("q", profile_id="jobs")
    assert found == ("https://example.com/a", "https://example.com/b")
    monkeypatch.delenv("TTC_DISCOVERY_FIXTURES")
    assert EnvDiscovery("TTC_DISCOVERY_FIXTURES").discover("q", profile_id="jobs") == ()
