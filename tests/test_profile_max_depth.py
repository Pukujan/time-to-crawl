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


def test_profile_max_depth_fails_closed() -> None:
    base = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    shallow = Profile(
        profile_id=base.profile_id,
        version=base.version,
        title=base.title,
        output_schema=base.output_schema,
        identity_keys=base.identity_keys,
        requested_capabilities=base.requested_capabilities,
        allowed_content_types=base.allowed_content_types,
        refresh_interval_seconds=base.refresh_interval_seconds,
        max_depth=1,
    )
    hops = ("https://example.com/a", "https://example.com/b", PRODUCT_URL)
    catalog = MemoryCatalog()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset(hops)),
        engine=FakeCrawlerEngine(
            {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"},
            redirects={PRODUCT_URL: hops},
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry({shallow.profile_id: shallow}),
        query=MemoryQuery(catalog),
    )
    with pytest.raises(PermissionError, match="profile_max_depth"):
        skeleton.run(PRODUCT_URL, shallow.profile_id)
    assert catalog.list_by_profile(shallow.profile_id) == ()
