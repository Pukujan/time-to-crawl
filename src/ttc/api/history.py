from __future__ import annotations

from ttc.domain.models import TypedRecord


def current_and_history(
    current: tuple[TypedRecord, ...],
    history: tuple[TypedRecord, ...],
) -> dict[str, object]:
    return {
        "current": [
            {
                "record_id": record.record_id,
                "identity_key": record.identity_key,
                "evidence_id": record.evidence_id,
                "payload": record.payload,
            }
            for record in current
        ],
        "history": [
            {
                "record_id": record.record_id,
                "identity_key": record.identity_key,
                "evidence_id": record.evidence_id,
            }
            for record in history
        ],
    }
