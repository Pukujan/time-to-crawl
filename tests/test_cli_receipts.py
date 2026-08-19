from __future__ import annotations

from pathlib import Path

from ttc.cli import main


def test_receipts_command_reads_log(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    main([])
    capsys.readouterr()
    main(["receipts"])
    out = capsys.readouterr().out
    assert "rcpt_" in out
    assert "products-and-offers" in out
    assert "legal-documents" in out
