from __future__ import annotations

from ttc.adapters.catalog import HistoryCatalog
from ttc.domain.models import TypedRecord


def test_history_preserves_prior_observations() -> None:
    catalog = HistoryCatalog()
    first = TypedRecord(
        record_id="rec_1",
        profile_id="products-and-offers",
        record_type="offer",
        payload={"price_minor": 1999},
        evidence_id="ev_1",
        identity_key="seller_alpha|https://alpha.example/widget",
    )
    second = TypedRecord(
        record_id="rec_2",
        profile_id="products-and-offers",
        record_type="offer",
        payload={"price_minor": 1499},
        evidence_id="ev_2",
        identity_key="seller_alpha|https://alpha.example/widget",
    )
    catalog.persist((first,))
    catalog.persist((second,))
    current = catalog.list_by_profile("products-and-offers")
    assert len(current) == 1
    assert current[0].payload["price_minor"] == 1499
    history = catalog.history_for(first.identity_key)
    assert [row.evidence_id for row in history] == ["ev_1", "ev_2"]
