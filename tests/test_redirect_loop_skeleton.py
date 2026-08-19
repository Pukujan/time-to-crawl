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

ROOT = Path(__file__).resolve().parents[1]


def test_redirect_loop_does_not_persist() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=FakeCrawlerEngine(
            {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"},
            redirects={PRODUCT_URL: (PRODUCT_URL, PRODUCT_URL)},
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
    )
    with pytest.raises(PermissionError, match="redirect_loop"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
    assert catalog.list_by_profile("products-and-offers") == ()
