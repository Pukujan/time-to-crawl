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
from ttc.domain.hostslots import HostSlotMap

ROOT = Path(__file__).resolve().parents[1]


def test_host_slot_blocks_second_url_on_same_host() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    host_slots = HostSlotMap(per_host=1)
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=FakeCrawlerEngine({PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"}),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
        host_slots=host_slots,
    )
    host_slots.acquire(PRODUCT_URL)
    with pytest.raises(PermissionError, match="concurrency_limit"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
    host_slots.release(PRODUCT_URL)
    skeleton.run(PRODUCT_URL, "products-and-offers")
    assert catalog.list_by_profile("products-and-offers")
