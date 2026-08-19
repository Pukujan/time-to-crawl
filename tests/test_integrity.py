from __future__ import annotations

from ttc.domain.integrity import inspect
from ttc.domain.models import TypedRecord


def test_integrity_flags_invalid_price() -> None:
    record = TypedRecord(
        record_id="rec_1",
        profile_id="products-and-offers",
        record_type="offer",
        payload={"price_minor": -1},
        evidence_id="ev_1",
        identity_key="seller|url",
    )
    codes = {signal.code for signal in inspect(record)}
    assert "invalid_price" in codes


def test_integrity_accepts_valid_offer() -> None:
    record = TypedRecord(
        record_id="rec_2",
        profile_id="products-and-offers",
        record_type="offer",
        payload={"price_minor": 1999},
        evidence_id="ev_1",
        identity_key="seller|url",
    )
    assert inspect(record) == ()
