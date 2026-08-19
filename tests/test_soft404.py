from __future__ import annotations

from ttc.domain.models import CrawlResult
from ttc.domain.soft404 import is_soft_404


def _result(status: int, body: bytes) -> CrawlResult:
    return CrawlResult(
        requested_url="https://example.com/x",
        final_url="https://example.com/x",
        status=status,
        headers=(),
        body=body,
        content_type="text/html",
        captured_at="2026-08-19T00:00:00Z",
        engine_id="fake",
        engine_version="0.0.0-fake",
    )


def test_soft_404_detects_not_found_pages() -> None:
    assert is_soft_404(_result(200, b"<title>404 Not Found</title><p>not found</p>"))
    assert not is_soft_404(_result(200, b'{"records":[{"title":"Staff"}]}'))
    assert not is_soft_404(_result(404, b"not found"))
