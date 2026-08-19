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
    load_profile,
)
from ttc.application.skeleton import WalkingSkeleton
from ttc.cli import PRODUCT_URL
from ttc.domain.models import Profile

ROOT = Path(__file__).resolve().parents[1]


def test_profile_requesting_anti_block_cannot_crawl() -> None:
    base = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    hostile = Profile(
        profile_id=base.profile_id,
        version=base.version,
        title=base.title,
        output_schema=base.output_schema,
        identity_keys=base.identity_keys,
        requested_capabilities=("fetch_public", "anti_block"),
        allowed_content_types=base.allowed_content_types,
        refresh_interval_seconds=base.refresh_interval_seconds,
    )
    catalog = MemoryCatalog()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=FakeCrawlerEngine({PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"}),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry({hostile.profile_id: hostile}),
        query=MemoryQuery(catalog),
    )
    with pytest.raises(PermissionError, match="capability_denied"):
        skeleton.run(PRODUCT_URL, hostile.profile_id)
    assert catalog.list_by_profile(hostile.profile_id) == ()
