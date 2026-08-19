from __future__ import annotations

from ttc.cli import status


def test_status_reports_live_crawl_blocked() -> None:
    payload = status()
    assert payload["live_crawl"] is False
    assert "jobs" in payload["profiles"]
    assert payload["engines"]["crawlee"] == "blocked_until_issue_4"
