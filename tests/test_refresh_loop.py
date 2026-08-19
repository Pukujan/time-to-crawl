from __future__ import annotations

from ttc.adapters.memory import FileProfileRegistry
from ttc.application.refresh import run_refresh
from ttc.cli import PRODUCT_URL, build_skeleton, load_reference_profiles
from ttc.domain.scheduler import KIND_REFRESH, STATE_DONE, Scheduler


def test_refresh_loop_requires_evidence_before_done() -> None:
    skeleton = build_skeleton()
    scheduler = Scheduler()
    profiles = FileProfileRegistry(load_reference_profiles())
    evidence_id = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        now=10,
        profiles=profiles,
    )
    done = scheduler.get(PRODUCT_URL, KIND_REFRESH)
    assert evidence_id
    assert done.state == STATE_DONE
    assert done.evidence_id == evidence_id
    assert skeleton.query("products-and-offers")
    skipped = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        now=11,
        profiles=profiles,
    )
    assert skipped is None
