from __future__ import annotations

from ttc.domain.change import detect_change
from ttc.domain.models import TypedRecord


def _record(payload: dict[str, object], evidence_id: str) -> TypedRecord:
    return TypedRecord(
        record_id="rec_1",
        profile_id="jobs",
        record_type="job",
        payload=payload,
        evidence_id=evidence_id,
        identity_key="REQ-441|https://jobs.example/req-441",
    )


def test_change_detection_uses_profile_payload_not_similarity() -> None:
    previous = _record({"title": "Staff Engineer", "embedding": [0.1, 0.2]}, "ev_1")
    same = _record({"title": "Staff Engineer", "embedding": [0.9, 0.1]}, "ev_2")
    changed = _record({"title": "Principal Engineer", "embedding": [0.1, 0.2]}, "ev_3")
    assert detect_change(previous, same).changed is False
    assert detect_change(previous, changed).changed is True
    assert detect_change(None, changed).changed is True
