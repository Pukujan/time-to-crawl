from __future__ import annotations

from ttc.cli import main, status


def test_status_reports_live_crawl_blocked() -> None:
    payload = status()
    assert payload["live_crawl"] is False
    assert payload["robots_default"] == "on"
    assert payload["anti_block_default"] == "off"
    assert payload["same_host_default"] is True
    assert "jobs" in payload["profiles"]
    assert payload["engines"]["crawlee"] == "blocked_until_issue_4"
    assert payload["property_count"] >= 14


def test_properties_command_lists_ids(capsys) -> None:
    main(["properties"])
    out = capsys.readouterr().out
    assert "TTC-NET-001" in out
    assert "TTC-DEAL-001" in out
