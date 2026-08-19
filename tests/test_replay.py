from __future__ import annotations

from pathlib import Path

from ttc.application.skeleton import WalkingSkeleton
from ttc.assurance.replay import ReplayStore
from ttc.cli import JOB_URL, PRODUCT_URL, build_skeleton

ROOT = Path(__file__).resolve().parents[1]


def test_replay_store_is_deterministic() -> None:
    store = ReplayStore(
        {
            PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json",
            JOB_URL: ROOT / "tests" / "fixtures" / "job.json",
        }
    )
    assert store.bytes_for(PRODUCT_URL) == store.bytes_for(PRODUCT_URL)
    skeleton: WalkingSkeleton = build_skeleton()
    first = skeleton.run(PRODUCT_URL, "products-and-offers")
    again = build_skeleton().run(PRODUCT_URL, "products-and-offers")
    assert first.profile_id == again.profile_id
    assert len(first.records) == len(again.records)
