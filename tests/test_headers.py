from __future__ import annotations

from ttc.domain.headers import sanitize_headers


def test_secret_headers_are_redacted() -> None:
    headers = (
        ("Content-Type", "text/html"),
        ("Authorization", "Bearer secret"),
        ("Cookie", "session=abc"),
        ("X-Api-Key", "k"),
    )
    cleaned = sanitize_headers(headers)
    assert ("Content-Type", "text/html") in cleaned
    assert ("Authorization", "[redacted]") in cleaned
    assert ("Cookie", "[redacted]") in cleaned
    assert ("X-Api-Key", "[redacted]") in cleaned
