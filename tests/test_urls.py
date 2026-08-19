from __future__ import annotations

from ttc.domain.urls import canonicalize


def test_canonicalize_strips_default_ports_and_fragments() -> None:
    assert canonicalize("HTTPS://Example.COM:443/a/#frag") == "https://example.com/a"
    assert canonicalize("http://example.com:80/a/") == "http://example.com/a"
    assert canonicalize("http://example.com:8080/a") == "http://example.com:8080/a"
