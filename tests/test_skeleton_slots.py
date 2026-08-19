from __future__ import annotations

from pathlib import Path

import pytest

from ttc.adapters.memory import (
    AllowlistPolicy,
    FakeCrawlerEngine,
    FileProfileRegistry,
    KeyIdentityResolver,
    MemoryCatalog,
    MemoryEvidenceStore,
    MemoryQuery,
    SchemaGuidedExtractor,
)
from ttc.application.skeleton import WalkingSkeleton
from ttc.cli import PRODUCT_URL, load_reference_profiles
from ttc.domain.concurrency import SlotPool

ROOT = Path(__file__).resolve().parents[1]


def test_slot_pool_blocks_third_concurrent_skeleton() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    slots = SlotPool(limit=1)
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=FakeCrawlerEngine({PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"}),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
        slots=slots,
    )
    slots.acquire()
    with pytest.raises(PermissionError, match="concurrency_limit"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
    slots.release()
    skeleton.run(PRODUCT_URL, "products-and-offers")
    assert slots.in_use == 0
    assert catalog.list_by_profile("products-and-offers")
