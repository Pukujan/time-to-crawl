from __future__ import annotations

from ttc.api.queryops import filter_records, sort_records
from ttc.domain.models import TypedRecord


def _job(record_id: str, title: str, rank: int) -> TypedRecord:
    return TypedRecord(
        record_id=record_id,
        profile_id="jobs",
        record_type="job",
        payload={"title": title, "rank": rank},
        evidence_id="ev_1",
        identity_key=record_id,
    )


def test_filter_and_sort_are_profile_neutral() -> None:
    records = (
        _job("a", "Staff", 2),
        _job("b", "Staff", 1),
        _job("c", "Principal", 3),
    )
    staff = filter_records(records, field="title", equals="Staff")
    assert {row.record_id for row in staff} == {"a", "b"}
    ordered = sort_records(staff, field="rank")
    assert [row.record_id for row in ordered] == ["b", "a"]
