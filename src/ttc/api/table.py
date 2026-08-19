from __future__ import annotations

from ttc.domain.models import TypedRecord


def as_table(records: tuple[TypedRecord, ...]) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for record in records:
        row = {
            "record_id": record.record_id,
            "profile_id": record.profile_id,
            "record_type": record.record_type,
            "identity_key": record.identity_key,
            "evidence_id": record.evidence_id,
        }
        row.update(record.payload)
        rows.append(row)
    return tuple(rows)
