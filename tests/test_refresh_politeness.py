from __future__ import annotations

from ttc.adapters.memory import FileProfileRegistry
from ttc.application.refresh import run_refresh
from ttc.cli import PRODUCT_URL, build_skeleton, load_reference_profiles
from ttc.domain.politeness import Politeness
from ttc.domain.scheduler import Scheduler


def test_refresh_respects_politeness_window() -> None:
    skeleton = build_skeleton()
    scheduler = Scheduler()
    profiles = FileProfileRegistry(load_reference_profiles())
    first = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        now=10,
        profiles=profiles,
        politeness=Politeness(min_delay_ms=1000),
    )
    assert first
    skipped = run_refresh(
        skeleton,
        scheduler,
        PRODUCT_URL,
        "products-and-offers",
        now=10 + 86400,
        profiles=profiles,
        politeness=Politeness(min_delay_ms=1000, last_fetch_at=10 + 86400 - 1),
    )
    assert skipped is None
