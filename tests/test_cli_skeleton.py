from __future__ import annotations

from pathlib import Path

from ttc.cli import main


def test_cli_skeleton_prints_receipt_ids(capsys, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    main([])
    out = capsys.readouterr().out
    assert '"receipt_id"' in out
    assert "rcpt_" in out
    assert "products-and-offers" in out
    assert "legal-documents" in out
    log = tmp_path / "receipts.jsonl"
    assert log.exists()
    assert log.read_text(encoding="utf-8").count("rcpt_") == 4
