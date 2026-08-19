from __future__ import annotations

from ttc.domain.hosts import same_registrable_host


def test_same_host_ignores_path_and_port_defaults() -> None:
    assert same_registrable_host("https://Example.com/a", "https://example.com/b")
    assert same_registrable_host("https://example.com:443/a", "https://example.com/b")
    assert not same_registrable_host("https://a.example/x", "https://b.example/x")
