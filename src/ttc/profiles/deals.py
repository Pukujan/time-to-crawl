from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.models import TypedRecord


@dataclass(frozen=True)
class RankedDeal:
    record_id: str
    score: int
    reasons: tuple[str, ...]


def rank_offers(
    records: tuple[TypedRecord, ...],
    *,
    max_price_minor: int | None = None,
    required_condition: str | None = None,
) -> tuple[RankedDeal, ...]:
    ranked: list[RankedDeal] = []
    for record in records:
        reasons: list[str] = []
        price = record.payload.get("price_minor")
        if not isinstance(price, int):
            continue
        if max_price_minor is not None and price > max_price_minor:
            reasons.append("over_budget")
            continue
        condition = record.payload.get("condition")
        if required_condition and condition != required_condition:
            reasons.append("condition_mismatch")
            continue
        ranked.append(
            RankedDeal(
                record_id=record.record_id,
                score=max_price_minor - price if max_price_minor is not None else -price,
                reasons=tuple(reasons) or ("in_budget",),
            )
        )
    return tuple(sorted(ranked, key=lambda item: item.score, reverse=True))
