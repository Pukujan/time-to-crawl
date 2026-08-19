from __future__ import annotations

from ttc.domain.models import CrawlResult


MAX_HTML_BYTES = 2_000_000


def body_within_limit(result: CrawlResult, limit: int = MAX_HTML_BYTES) -> bool:
    return len(result.body) <= limit
