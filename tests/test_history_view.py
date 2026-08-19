from __future__ import annotations

from ttc.adapters.catalog import HistoryCatalog
from ttc.api.history import current_and_history
from ttc.domain.models import TypedRecord


def test_history_view_keeps_current_and_prior_evidence() -> None:
    catalog = HistoryCatalog()
    first = TypedRecord(
        record_id="rec_1",
        profile_id="jobs",
        record_type="job",
        payload={"title": "Staff"},
        evidence_id="ev_1",
        identity_key="REQ-1|https://jobs.example/1",
    )
    second = TypedRecord(
        record_id="rec_2",
        profile_id="jobs",
        record_type="job",
        payload={"title": "Principal"},
        evidence_id="ev_2",
        identity_key="REQ-1|https://jobs.example/1",
    )
    catalog.persist((first,))
    catalog.persist((second,))
    view = current_and_history(
        catalog.list_by_profile("jobs"),
        catalog.history_for(first.identity_key),
    )
    assert view["current"][0]["payload"]["title"] == "Principal"
    assert [row.evidence_id for row in catalog.history_for(first.identity_key)] == ["ev_1", "ev_2"]
