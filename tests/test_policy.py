from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from ttc.domain.capabilities import DEFAULT_GRANTED, profile_cannot_grant
from ttc.domain.netpolicy import PolicyBroker, classify_url

PUBLIC = "https://example.com/page"
LOOPBACKS = (
    "http://127.0.0.1/",
    "http://localhost/admin",
    "http://[::1]/",
    "http://0.0.0.0/",
)
PRIVATES = (
    "http://10.0.0.1/",
    "http://192.168.1.1/",
    "http://172.16.0.1/",
)
METADATA = (
    "http://169.254.169.254/latest/meta-data/",
    "http://metadata.google.internal/",
)


@pytest.mark.parametrize("url", LOOPBACKS + PRIVATES + METADATA)
def test_forbidden_network_classes(url: str) -> None:
    broker = PolicyBroker(frozenset({url}), DEFAULT_GRANTED)
    decision = broker.authorize(url, profile_id="jobs")
    assert decision.allowed is False
    assert decision.reason.startswith("forbidden_network:")


def test_redirect_hops_are_reauthorized() -> None:
    broker = PolicyBroker(frozenset({PUBLIC}), DEFAULT_GRANTED)
    decision = broker.authorize_chain(
        (PUBLIC, "http://127.0.0.1/secret", PUBLIC),
        profile_id="jobs",
    )
    assert decision.allowed is False
    assert "forbidden_network" in decision.reason


def test_profile_cannot_self_grant_capabilities() -> None:
    denied = profile_cannot_grant(("anti_block", "ops_admin"), DEFAULT_GRANTED)
    assert denied == frozenset({"anti_block", "ops_admin"})
    broker = PolicyBroker(frozenset({PUBLIC}), DEFAULT_GRANTED)
    decision = broker.authorize(
        PUBLIC,
        profile_id="jobs",
        requested_capabilities=("anti_block",),
    )
    assert decision.allowed is False
    assert decision.reason.startswith("capability_denied")


def test_authorization_is_explicit() -> None:
    broker = PolicyBroker(frozenset({PUBLIC}), DEFAULT_GRANTED)
    allowed = broker.authorize(PUBLIC, profile_id="jobs")
    denied = broker.authorize("https://other.example/x", profile_id="jobs")
    assert allowed.allowed is True
    assert allowed.reason == "allowlisted"
    assert denied.allowed is False
    assert denied.reason == "not_allowlisted"


@given(st.sampled_from(["http://127.0.0.1/a", "http://10.1.2.3/", "http://169.254.169.254/"]))
@settings(max_examples=20)
def test_generated_forbidden_urls_stay_blocked(url: str) -> None:
    assert classify_url(url) != "public"
