from __future__ import annotations

from ttc.domain.models import TypedRecord


def expand_provenance(record: TypedRecord) -> dict[str, object]:
    if not record.evidence_id:
        raise ValueError("evidence_required")
    return {
        "record_id": record.record_id,
        "profile_id": record.profile_id,
        "identity_key": record.identity_key,
        "evidence_id": record.evidence_id,
        "record_type": record.record_type,
    }
