from __future__ import annotations

from pathlib import Path

from ttc.adapters.scheduler import DurableScheduler
from ttc.adapters.sqlite_catalog import SqliteCatalog
from ttc.domain.models import TypedRecord
from ttc.domain.scheduler import KIND_REFRESH, STATE_DONE


def test_chaos_restart_restores_scheduler_and_catalog(tmp_path: Path) -> None:
    sched_path = tmp_path / "sched.json"
    catalog_path = tmp_path / "catalog.sqlite"
    scheduler = DurableScheduler(sched_path)
    catalog = SqliteCatalog(catalog_path)
    url = "https://example.com/item"
    scheduler.enqueue(url, KIND_REFRESH)
    claimed = scheduler.claim(url, KIND_REFRESH)
    record = TypedRecord(
        record_id="rec_1",
        profile_id="jobs",
        record_type="job",
        payload={"title": "Staff"},
        evidence_id="ev_1",
        identity_key="REQ-1|https://example.com/item",
    )
    catalog.persist((record,))
    scheduler.complete(claimed, "ev_1")
    restored_sched = DurableScheduler(sched_path)
    restored_catalog = SqliteCatalog(catalog_path)
    assert restored_sched.get(url, KIND_REFRESH).state == STATE_DONE
    assert restored_sched.get(url, KIND_REFRESH).evidence_id == "ev_1"
    assert restored_catalog.list_by_profile("jobs")[0].evidence_id == "ev_1"
    assert restored_catalog.history_for(record.identity_key) == ("ev_1",)
