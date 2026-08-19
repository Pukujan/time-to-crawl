from __future__ import annotations

import pytest

from ttc.adapters.vendors import UnavailableBrowsertrix, UnavailableCrawl4AI, UnavailableFirecrawl
from ttc.domain.models import CrawlWork, Evidence, Profile


def test_optional_vendors_fail_closed() -> None:
    work = CrawlWork(url="https://example.com", profile_id="jobs", run_id="run_1")
    with pytest.raises(PermissionError, match="firecrawl_blocked_until_issue_4"):
        UnavailableFirecrawl().crawl(work)
    with pytest.raises(PermissionError, match="browsertrix_blocked_until_issue_4"):
        UnavailableBrowsertrix().crawl(work)
    with pytest.raises(PermissionError, match="crawl4ai_blocked_until_issue_4"):
        UnavailableCrawl4AI().extract(
            Evidence(
                evidence_id="ev_1",
                content_sha256="a" * 64,
                fetched_url="https://example.com",
                captured_at="2026-08-19T00:00:00Z",
                content_type="text/html",
                body=b"<html></html>",
                engine_id="fake",
                engine_version="0.0.0-fake",
                profile_id="jobs",
                run_id="run_1",
            ),
            Profile(
                profile_id="jobs",
                version="1.0.0",
                title="Jobs",
                output_schema="ttc.typed-record.v1",
                identity_keys=("id",),
            ),
        )
