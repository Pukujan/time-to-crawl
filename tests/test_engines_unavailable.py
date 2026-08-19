from __future__ import annotations

import pytest

from ttc.adapters.engines import UnavailableEngine
from ttc.domain.models import CrawlWork


def test_real_engines_fail_closed_until_issue_4() -> None:
    work = CrawlWork(url="https://example.com", profile_id="jobs", run_id="run_1")
    for engine_id in ("crawlee", "scrapy"):
        with pytest.raises(PermissionError, match="live_crawl_blocked_until_issue_4"):
            UnavailableEngine(engine_id).crawl(work)
