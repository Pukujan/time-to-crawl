from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProvenanceLink:
    record_id: str
    evidence_id: str
    activity: str
    engine_id: str
    engine_version: str
    profile_id: str
    run_id: str
    fetched_url: str
    policy_reason: str


def bind(
    *,
    record_id: str,
    evidence_id: str,
    engine_id: str,
    engine_version: str,
    profile_id: str,
    run_id: str,
    fetched_url: str,
    policy_reason: str,
    activity: str = "extract",
) -> ProvenanceLink:
    if not evidence_id:
        raise ValueError("evidence_required")
    if not engine_id or not engine_version:
        raise ValueError("engine_identity_required")
    if not run_id:
        raise ValueError("run_required")
    return ProvenanceLink(
        record_id=record_id,
        evidence_id=evidence_id,
        activity=activity,
        engine_id=engine_id,
        engine_version=engine_version,
        profile_id=profile_id,
        run_id=run_id,
        fetched_url=fetched_url,
        policy_reason=policy_reason,
    )
