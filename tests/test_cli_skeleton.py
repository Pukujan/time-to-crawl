from __future__ import annotations

from ttc.cli import main


def test_cli_skeleton_prints_receipt_ids(capsys) -> None:
    main([])
    out = capsys.readouterr().out
    assert '"receipt_id"' in out
    assert "rcpt_" in out
    assert "products-and-offers" in out
    assert "legal-documents" in out
