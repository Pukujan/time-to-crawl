from __future__ import annotations

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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_outlinks_are_filtered_not_auto_authorized() -> None:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=FakeCrawlerEngine(
            {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"},
            outlinks={
                PRODUCT_URL: (
                    PRODUCT_URL,
                    "http://127.0.0.1/secret",
                    "https://evil.example/x",
                )
            },
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
    )
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    assert PRODUCT_URL in result.outlinks
    assert "http://127.0.0.1/secret" not in result.outlinks
    assert "https://evil.example/x" not in result.outlinks
    assert result.provenance
    assert all(link.evidence_id == result.evidence_id for link in result.provenance)
    assert all(link.engine_id for link in result.provenance)
