from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from ttc.domain.identity import new_id


@dataclass(frozen=True)
class RunReceipt:
    receipt_id: str
    run_id: str
    profile_id: str
    url: str
    policy_reason: str
    engine_id: str
    evidence_id: str
    record_count: int
    created_at: str


def mint_receipt(
    *,
    run_id: str,
    profile_id: str,
    url: str,
    policy_reason: str,
    engine_id: str,
    evidence_id: str,
    record_count: int,
) -> RunReceipt:
    if not evidence_id:
        raise ValueError("evidence_required")
    return RunReceipt(
        receipt_id=new_id("rcpt"),
        run_id=run_id,
        profile_id=profile_id,
        url=url,
        policy_reason=policy_reason,
        engine_id=engine_id,
        evidence_id=evidence_id,
        record_count=record_count,
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
