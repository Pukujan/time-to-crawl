from __future__ import annotations

from pathlib import Path

from ttc.adapters.receipts import ReceiptLog
from ttc.cli import PRODUCT_URL, build_skeleton


def test_receipt_log_appends_evidence_bound_rows(tmp_path: Path) -> None:
    log = ReceiptLog(tmp_path / "receipts.jsonl")
    skeleton = build_skeleton()
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    assert result.receipt is not None
    log.append(result.receipt)
    rows = log.load()
    assert len(rows) == 1
    assert rows[0]["evidence_id"] == result.evidence_id
    assert rows[0]["robots_compliant"] is True
