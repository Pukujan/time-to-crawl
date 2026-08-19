from __future__ import annotations

from ttc.cli import PRODUCT_URL, build_skeleton
from ttc.domain.receipts import mint_receipt


def test_run_receipt_binds_evidence() -> None:
    skeleton = build_skeleton()
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    assert result.receipt is not None
    assert result.receipt.evidence_id == result.evidence_id
    assert result.receipt.record_count == 2
    assert result.receipt.receipt_id.startswith("rcpt_")
    assert result.receipt.robots_compliant is True
    extra = mint_receipt(
        run_id=result.run_id,
        profile_id=result.profile_id,
        url=PRODUCT_URL,
        policy_reason="allowlisted",
        engine_id="fake",
        evidence_id=result.evidence_id,
        record_count=len(result.records),
    )
    assert extra.evidence_id == result.evidence_id
