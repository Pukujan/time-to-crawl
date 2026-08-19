from __future__ import annotations

from ttc.domain.netpolicy import classify_url, is_forbidden_class
from ttc.domain.urls import canonicalize


def test_whitespace_and_uppercase_hosts_canonicalize() -> None:
    assert canonicalize("  HTTPS://EXAMPLE.COM/A  ") == "https://example.com/A"
    assert canonicalize("https://EXAMPLE.com/A") == "https://example.com/A"


def test_blank_url_is_forbidden() -> None:
    assert is_forbidden_class(classify_url(""))
