from __future__ import annotations

from typing import Protocol

from ttc.domain.models import CrawlResult, CrawlWork


class CrawlerEnginePort(Protocol):
    def crawl(self, work: CrawlWork) -> CrawlResult:
        """Execute already-authorized work. Must not decide source authority or persist durable truth."""
