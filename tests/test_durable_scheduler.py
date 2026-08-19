from __future__ import annotations

from pathlib import Path

from ttc.adapters.scheduler import DurableScheduler
from ttc.domain.scheduler import KIND_REFRESH, STATE_DONE


def test_durable_scheduler_survives_restart(tmp_path: Path) -> None:
    path = tmp_path / "scheduler.json"
    first = DurableScheduler(path)
    url = "https://example.com/item"
    first.enqueue(url, KIND_REFRESH)
    claimed = first.claim(url, KIND_REFRESH)
    first.complete(claimed, "ev_1")
    second = DurableScheduler(path)
    restored = second.get(url, KIND_REFRESH)
    assert restored.state == STATE_DONE
    assert restored.evidence_id == "ev_1"
    due = second.due_refresh(url)
    assert due.due is True
    assert due.state != STATE_DONE
