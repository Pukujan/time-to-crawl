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


def test_too_many_redirects_do_not_persist() -> None:
    hops = tuple(f"https://fixture.time-to-crawl.test/h{i}" for i in range(6)) + (PRODUCT_URL,)
    allowed = frozenset(hops)
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(allowed),
        engine=FakeCrawlerEngine(
            {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"},
            redirects={PRODUCT_URL: hops},
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
    )
    with pytest.raises(PermissionError, match="too_many_redirects"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
    assert catalog.list_by_profile("products-and-offers") == ()
