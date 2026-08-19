from __future__ import annotations

from pathlib import Path

from ttc.adapters.sqlite_catalog import SqliteCatalog
from ttc.domain.models import TypedRecord


def test_sqlite_catalog_keeps_history(tmp_path: Path) -> None:
    catalog = SqliteCatalog(tmp_path / "catalog.sqlite")
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
    current = catalog.list_by_profile("jobs")
    assert len(current) == 1
    assert current[0].payload["title"] == "Principal"
    assert catalog.history_for(first.identity_key) == ("ev_1", "ev_2")
