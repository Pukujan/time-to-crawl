from __future__ import annotations

from ttc.cli import PRODUCT_URL, build_skeleton
from ttc.domain.receipts import mint_receipt


def test_run_receipt_binds_evidence() -> None:
    skeleton = build_skeleton()
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    receipt = mint_receipt(
        run_id=result.run_id,
        profile_id=result.profile_id,
        url=PRODUCT_URL,
        policy_reason="allowlisted",
        engine_id="fake",
        evidence_id=result.evidence_id,
        record_count=len(result.records),
    )
    assert receipt.evidence_id == result.evidence_id
    assert receipt.record_count == 2
    assert receipt.receipt_id.startswith("rcpt_")
