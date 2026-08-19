from __future__ import annotations

from ttc.application.discover import run_discover
from ttc.cli import PRODUCT_URL, build_skeleton
from ttc.domain.scheduler import KIND_DISCOVER, STATE_DONE, Scheduler


def test_discover_loop_returns_filtered_outlinks() -> None:
    skeleton = build_skeleton()
    scheduler = Scheduler()
    evidence_id, outlinks = run_discover(skeleton, scheduler, PRODUCT_URL, "products-and-offers")
    done = scheduler.get(PRODUCT_URL, KIND_DISCOVER)
    assert done.state == STATE_DONE
    assert done.evidence_id == evidence_id
    assert "http://127.0.0.1" not in outlinks
