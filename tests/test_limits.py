from __future__ import annotations

from ttc.domain.limits import max_redirects_ok
from ttc.domain.models import CrawlResult


def test_redirect_chain_limit() -> None:
    short = CrawlResult(
        requested_url="https://example.com/a",
        final_url="https://example.com/b",
        status=200,
        headers=(),
        body=b"ok",
        content_type="text/html",
        captured_at="2026-08-19T00:00:00Z",
        engine_id="fake",
        engine_version="0.0.0-fake",
        redirect_chain=("https://example.com/a",),
    )
    long = CrawlResult(
        requested_url="https://example.com/a",
        final_url="https://example.com/z",
        status=200,
        headers=(),
        body=b"ok",
        content_type="text/html",
        captured_at="2026-08-19T00:00:00Z",
        engine_id="fake",
        engine_version="0.0.0-fake",
        redirect_chain=tuple(f"https://example.com/{i}" for i in range(8)),
    )
    assert max_redirects_ok(short, 5) is True
    assert max_redirects_ok(long, 5) is False
