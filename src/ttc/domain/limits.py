from __future__ import annotations

from ttc.domain.models import CrawlResult


def max_redirects_ok(result: CrawlResult, limit: int = 5) -> bool:
    return len(result.redirect_chain) <= limit
