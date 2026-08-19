from __future__ import annotations

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
