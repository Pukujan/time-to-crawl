from __future__ import annotations

from pathlib import Path

from ttc.cli import doctor, main


def test_doctor_reports_fixture_gate_green() -> None:
    report = doctor()
    assert report["ok"] is True
    assert report["live_crawl"] is False
    assert report["live_engines_enabled"] == []
    assert "jobs" in report["profiles"]
    assert report["property_count"] >= 14
    assert report["missing_files"] == []


def test_doctor_command_prints_ok(capsys) -> None:
    main(["doctor"])
    out = capsys.readouterr().out
    assert '"ok": true' in out
    assert '"live_crawl": false' in out


def test_doctor_fails_closed_when_contracts_missing(tmp_path: Path) -> None:
    report = doctor(root=tmp_path)
    assert report["ok"] is False
    assert "AGENTS.md" in report["missing_files"]
    assert "ARCHITECTURE.md" in report["missing_files"]
