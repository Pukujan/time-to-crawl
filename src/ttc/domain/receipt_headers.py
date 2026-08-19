from __future__ import annotations

from ttc.domain.models import CrawlResult
from ttc.domain.headers import sanitize_headers


def receipt_headers(result: CrawlResult) -> tuple[tuple[str, str], ...]:
    return sanitize_headers(result.headers)
