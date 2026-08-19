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


def test_redirect_depth_budget_fails_closed() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL, "https://example.com/a", "https://example.com/b"})),
        engine=FakeCrawlerEngine(
            {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"},
            redirects={PRODUCT_URL: ("https://example.com/a", "https://example.com/b", PRODUCT_URL)},
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
        budget=Budget(max_requests=8, max_bytes=2_000_000, max_depth=1, max_seconds=60),
    )
    with pytest.raises(PermissionError, match="budget_depth"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
    assert catalog.list_by_profile("products-and-offers") == ()
