from __future__ import annotations

from ttc.domain.models import CrawlResult, CrawlWork, Evidence, Profile, TypedRecord


class UnavailableFirecrawl:
    engine_id = "firecrawl"

    def crawl(self, work: CrawlWork) -> CrawlResult:
        raise PermissionError("firecrawl_blocked_until_issue_4")


class UnavailableBrowsertrix:
    engine_id = "browsertrix"

    def crawl(self, work: CrawlWork) -> CrawlResult:
        raise PermissionError("browsertrix_blocked_until_issue_4")


class UnavailableCrawl4AI:
    def extract(self, evidence: Evidence, profile: Profile) -> tuple[TypedRecord, ...]:
        raise PermissionError("crawl4ai_blocked_until_issue_4")
