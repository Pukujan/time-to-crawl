from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.models import TypedRecord


@dataclass(frozen=True)
class Change:
    identity_key: str
    changed: bool
    previous_evidence_id: str | None
    current_evidence_id: str


def payload_for_change(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if key != "embedding"}


def detect_change(previous: TypedRecord | None, current: TypedRecord) -> Change:
    if previous is None:
        return Change(
            identity_key=current.identity_key,
            changed=True,
            previous_evidence_id=None,
            current_evidence_id=current.evidence_id,
        )
    if previous.identity_key != current.identity_key:
        raise ValueError("identity_mismatch")
    changed = payload_for_change(previous.payload) != payload_for_change(current.payload)
    return Change(
        identity_key=current.identity_key,
        changed=changed,
        previous_evidence_id=previous.evidence_id,
        current_evidence_id=current.evidence_id,
    )
