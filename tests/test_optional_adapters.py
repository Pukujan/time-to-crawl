from __future__ import annotations

import pytest

from ttc.adapters.optional import UnavailableBrowser, UnavailableTika
from ttc.domain.models import CrawlWork


def test_optional_live_adapters_fail_closed() -> None:
    work = CrawlWork(url="https://example.com", profile_id="jobs", run_id="run_1")
    with pytest.raises(PermissionError, match="browser_blocked_until_issue_4"):
        UnavailableBrowser().crawl(work)
    with pytest.raises(PermissionError, match="tika_blocked_until_issue_4"):
        UnavailableTika().extract(None, None)
