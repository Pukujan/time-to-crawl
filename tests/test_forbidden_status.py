from __future__ import annotations

import pytest

from ttc.adapters.memory import (
    AllowlistPolicy,
    FileProfileRegistry,
    KeyIdentityResolver,
    MemoryCatalog,
    MemoryEvidenceStore,
    MemoryQuery,
    SchemaGuidedExtractor,
)
from ttc.application.skeleton import WalkingSkeleton
from ttc.cli import PRODUCT_URL, load_reference_profiles
from ttc.domain.models import CrawlResult, CrawlWork


class ForbiddenEngine:
    engine_id = "fake"

    def crawl(self, work: CrawlWork) -> CrawlResult:
        return CrawlResult(
            requested_url=work.url,
            final_url=work.url,
            status=403,
            headers=(),
            body=b"forbidden",
            content_type="text/html",
            captured_at="2026-08-19T00:00:00Z",
            engine_id="fake",
            engine_version="0.0.0-fake",
        )


def test_forbidden_status_does_not_persist() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=ForbiddenEngine(),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
    )
    with pytest.raises(PermissionError, match="status_blocked"):
        skeleton.run(PRODUCT_URL, "products-and-offers")
    assert catalog.list_by_profile("products-and-offers") == ()
