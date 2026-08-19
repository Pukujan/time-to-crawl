from __future__ import annotations

from ttc.adapters.clock import FrozenClock
from ttc.adapters.memory import FileProfileRegistry
from ttc.application.refresh import run_refresh
from ttc.cli import PRODUCT_URL, build_skeleton, load_reference_profiles
from ttc.domain.scheduler import KIND_REFRESH, Scheduler


def test_frozen_clock_drives_refresh_without_wall_time() -> None:
    clock = FrozenClock(10)
    skeleton = build_skeleton()
    scheduler = Scheduler()
    profiles = FileProfileRegistry(load_reference_profiles())
    first = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        clock=clock,
        profiles=profiles,
    )
    assert first
    skipped = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        clock=clock,
        profiles=profiles,
    )
    assert skipped is None
    clock.advance(86400)
    second = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        clock=clock,
        profiles=profiles,
    )
    assert second
    assert scheduler.get(PRODUCT_URL, KIND_REFRESH).evidence_id == second
