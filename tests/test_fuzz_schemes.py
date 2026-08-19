from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from ttc.domain.netpolicy import classify_url, is_forbidden_class

SCHEMES = st.sampled_from(["ftp", "file", "javascript", "data", "gopher", "ws"])


@given(SCHEMES)
@settings(max_examples=20)
def test_non_http_schemes_are_forbidden(scheme: str) -> None:
    assert is_forbidden_class(classify_url(f"{scheme}://example.com/x"))
    assert classify_url(f"{scheme}://example.com/x") == "disallowed_scheme"


def test_missing_host_is_forbidden() -> None:
    assert is_forbidden_class(classify_url("http:///nohost"))
