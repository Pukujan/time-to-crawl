from __future__ import annotations

from ttc.domain.models import TypedRecord
from ttc.profiles.deals import rank_offers


def _offer(record_id: str, price: int, condition: str = "new") -> TypedRecord:
    return TypedRecord(
        record_id=record_id,
        profile_id="products-and-offers",
        record_type="offer",
        payload={"price_minor": price, "condition": condition},
        evidence_id="ev_1",
        identity_key=record_id,
    )


def test_deal_ranking_is_profile_extension_not_engine() -> None:
    records = (
        _offer("cheap", 1000),
        _offer("over", 5000),
        _offer("used", 900, condition="used"),
    )
    ranked = rank_offers(records, max_price_minor=2000, required_condition="new")
    assert [item.record_id for item in ranked] == ["cheap"]
    assert ranked[0].reasons == ("in_budget",)
