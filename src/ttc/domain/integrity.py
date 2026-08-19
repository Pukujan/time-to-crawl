from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.models import TypedRecord


@dataclass(frozen=True)
class IntegritySignal:
    record_id: str
    code: str
    severity: str
    detail: str


def inspect(record: TypedRecord) -> tuple[IntegritySignal, ...]:
    signals: list[IntegritySignal] = []
    if not record.evidence_id:
        signals.append(_signal(record, "missing_evidence", "critical", "record has no evidence"))
    payload = record.payload
    if not payload:
        signals.append(_signal(record, "empty_payload", "high", "payload is empty"))
    if "price_minor" in payload:
        price = payload["price_minor"]
        if not isinstance(price, int) or price < 0:
            signals.append(_signal(record, "invalid_price", "high", "price_minor is not a non-negative int"))
    if payload.get("citation") and not record.evidence_id:
        signals.append(_signal(record, "model_citation", "critical", "citation without evidence"))
    return tuple(signals)


def _signal(record: TypedRecord, code: str, severity: str, detail: str) -> IntegritySignal:
    return IntegritySignal(record_id=record.record_id, code=code, severity=severity, detail=detail)
