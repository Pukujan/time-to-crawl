from __future__ import annotations

from ttc.domain.models import CrawlResult, CrawlWork


class UnavailableBrowser:
    def __init__(self, engine_id: str = "playwright") -> None:
        self.engine_id = engine_id

    def crawl(self, work: CrawlWork) -> CrawlResult:
        raise PermissionError("browser_blocked_until_issue_4")


class UnavailableTika:
    def extract(self, evidence: object, profile: object) -> tuple:
        raise PermissionError("tika_blocked_until_issue_4")
