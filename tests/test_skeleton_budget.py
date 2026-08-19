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
from ttc.domain.budget import Budget

ROOT = Path(__file__).resolve().parents[1]


def test_tiny_budget_blocks_second_fetch() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=FakeCrawlerEngine({PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"}),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
        budget=Budget(max_requests=1, max_bytes=2_000_000, max_depth=1, max_seconds=60),
    )
    skeleton.run(PRODUCT_URL, "products-and-offers")
    with pytest.raises(PermissionError, match="budget_requests"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
