from __future__ import annotations

import pytest

from ttc.domain.capabilities import DEFAULT_GRANTED
from ttc.domain.netpolicy import PolicyBroker, classify_url, is_forbidden_class


@pytest.mark.parametrize(
    "url",
    [
        "http://[::1]/",
        "http://[0:0:0:0:0:0:0:1]/",
        "http://[::ffff:7f00:1]/",
        "http://0177.0.0.1/",
        "http://127.0.0.1.nip.io/",
    ],
)
def test_more_loopback_encodings(url: str) -> None:
    if url.endswith("nip.io/"):
        pytest.xfail("DNS rebinding needs #4 external resolver policy")
    assert is_forbidden_class(classify_url(url))
    broker = PolicyBroker(frozenset({url}), DEFAULT_GRANTED)
    assert broker.authorize(url, profile_id="jobs").allowed is False
