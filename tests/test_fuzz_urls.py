from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from ttc.domain.netpolicy import classify_url, is_forbidden_class

HOSTS = st.sampled_from(
    [
        "127.0.0.1",
        "127.0.0.2",
        "10.0.0.1",
        "10.255.255.254",
        "192.168.0.1",
        "172.16.0.1",
        "172.31.255.1",
        "169.254.1.1",
        "169.254.169.254",
        "0.0.0.0",
        "localhost",
        "[::1]",
        "metadata.google.internal",
    ]
)
SCHEMES = st.sampled_from(["http", "https"])


@given(SCHEMES, HOSTS)
@settings(max_examples=40)
def test_fuzz_forbidden_hosts_never_classify_public(scheme: str, host: str) -> None:
    url = f"{scheme}://{host}/path"
    assert is_forbidden_class(classify_url(url))
