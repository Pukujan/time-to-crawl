from __future__ import annotations

from ttc.domain.models import CrawlResult
from ttc.domain.receipt_headers import receipt_headers


def test_receipt_headers_never_keep_bearer_tokens() -> None:
    result = CrawlResult(
        requested_url="https://example.com",
        final_url="https://example.com",
        status=200,
        headers=(("Authorization", "Bearer abc"), ("Accept", "text/html")),
        body=b"ok",
        content_type="text/html",
        captured_at="2026-08-19T00:00:00Z",
        engine_id="fake",
        engine_version="0.0.0-fake",
    )
    cleaned = receipt_headers(result)
    assert ("Authorization", "[redacted]") in cleaned
    assert ("Accept", "text/html") in cleaned
