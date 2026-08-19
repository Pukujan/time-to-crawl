from __future__ import annotations

from ttc.domain.scheduler import KIND_REFRESH, Scheduler
from ttc.ops.health import probe


def test_health_probe_degrades_when_evidence_fails() -> None:
    scheduler = Scheduler()
    scheduler.enqueue("https://example.com/x", KIND_REFRESH)
    ok = probe(scheduler=scheduler, evidence_ok=True, policy_ok=True)
    bad = probe(scheduler=scheduler, evidence_ok=False, policy_ok=True)
    assert ok.status == "ok"
    assert ok.scheduler_items == 1
    assert bad.status == "degraded"
