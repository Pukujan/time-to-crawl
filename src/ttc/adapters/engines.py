from __future__ import annotations

from ttc.domain.models import CrawlResult, CrawlWork


class UnavailableEngine:
    """Fail-closed Crawlee/Scrapy placeholder. Real adapters wait on #4/#8."""

    def __init__(self, engine_id: str) -> None:
        self.engine_id = engine_id

    def crawl(self, work: CrawlWork) -> CrawlResult:
        raise PermissionError(f"engine_unavailable:{self.engine_id}:live_crawl_blocked_until_issue_4")
