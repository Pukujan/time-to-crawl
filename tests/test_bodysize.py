from __future__ import annotations

from ttc.domain.bodysize import body_within_limit
from ttc.domain.models import CrawlResult


def test_oversized_body_is_rejected() -> None:
    small = CrawlResult(
        requested_url="https://example.com",
        final_url="https://example.com",
        status=200,
        headers=(),
        body=b"ok",
        content_type="text/html",
        captured_at="2026-08-19T00:00:00Z",
        engine_id="fake",
        engine_version="0.0.0-fake",
    )
    huge = CrawlResult(
        requested_url="https://example.com",
        final_url="https://example.com",
        status=200,
        headers=(),
        body=b"x" * 2_000_001,
        content_type="text/html",
        captured_at="2026-08-19T00:00:00Z",
        engine_id="fake",
        engine_version="0.0.0-fake",
    )
    assert body_within_limit(small) is True
    assert body_within_limit(huge) is False
