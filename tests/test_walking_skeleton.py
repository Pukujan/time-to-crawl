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
from ttc.ports.catalog import OperationalCatalogPort
from ttc.ports.crawler import CrawlerEnginePort
from ttc.ports.evidence import EvidenceStorePort
from ttc.ports.extractor import ContentExtractorPort
from ttc.ports.identity import IdentityResolverPort
from ttc.ports.policy import PolicyDecisionPort
from ttc.ports.profiles import ProfileRegistryPort
from ttc.ports.query import QueryViewPort

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_URL = "https://fixture.time-to-crawl.test/widget"
JOB_URL = "https://fixture.time-to-crawl.test/job"


def _system(*, engine_id: str = "fake") -> WalkingSkeleton:
    catalog = MemoryCatalog()
    products = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    jobs = load_profile(ROOT / "contracts" / "profiles" / "jobs.v1.json")
    return WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL, JOB_URL})),
        engine=FakeCrawlerEngine(
            {
                PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json",
                JOB_URL: ROOT / "tests" / "fixtures" / "job.json",
            },
            engine_id=engine_id,
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(
            {products.profile_id: products, jobs.profile_id: jobs}
        ),
        query=MemoryQuery(catalog),
    )


def test_products_profile_extracts_two_independent_offers() -> None:
    skeleton = _system()
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    records = skeleton.query("products-and-offers")
    assert result.profile_id == "products-and-offers"
    assert len(records) == 2
    sellers = {row.payload["seller_id"] for row in records}
    assert sellers == {"seller_alpha", "seller_beta"}
    assert all(row.evidence_id == result.evidence_id for row in records)


def test_jobs_profile_uses_same_engine_path() -> None:
    skeleton = _system()
    result = skeleton.run(JOB_URL, "jobs")
    records = skeleton.query("jobs")
    assert result.profile_id == "jobs"
    assert len(records) == 1
    assert records[0].payload["requisition_id"] == "REQ-441"


def test_second_profile_does_not_change_crawler_or_domain() -> None:
    first = _system(engine_id="fake-a")
    second = _system(engine_id="fake-b")
    products = first.run(PRODUCT_URL, "products-and-offers")
    jobs = second.run(JOB_URL, "jobs")
    assert products.profile_id != jobs.profile_id
    assert len(first.query("products-and-offers")) == 2
    assert len(second.query("jobs")) == 1


def test_policy_blocks_unknown_url() -> None:
    skeleton = _system()
    with pytest.raises(PermissionError):
        skeleton.run("https://evil.example/widget", "products-and-offers")


def test_crawler_engine_can_be_replaced_by_another_fake() -> None:
    catalog: OperationalCatalogPort = MemoryCatalog()
    products = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    jobs = load_profile(ROOT / "contracts" / "profiles" / "jobs.v1.json")
    engine: CrawlerEnginePort = FakeCrawlerEngine(
        {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"},
        engine_id="alternate-fake",
    )
    skeleton = WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL})),
        engine=engine,
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry({products.profile_id: products, jobs.profile_id: jobs}),
        query=MemoryQuery(catalog),
    )
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    assert catalog.list_by_profile("products-and-offers")
    assert result.records[0].evidence_id


def test_ports_are_satisfied_by_fakes() -> None:
    policy: PolicyDecisionPort = AllowlistPolicy(frozenset({PRODUCT_URL}))
    engine: CrawlerEnginePort = FakeCrawlerEngine(
        {PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json"}
    )
    evidence: EvidenceStorePort = MemoryEvidenceStore()
    extractor: ContentExtractorPort = SchemaGuidedExtractor()
    identity: IdentityResolverPort = KeyIdentityResolver()
    catalog: OperationalCatalogPort = MemoryCatalog()
    profiles: ProfileRegistryPort = FileProfileRegistry(
        {
            "products-and-offers": load_profile(
                ROOT / "contracts" / "profiles" / "products-and-offers.v1.json"
            )
        }
    )
    query: QueryViewPort = MemoryQuery(catalog)
    assert policy.authorize(PRODUCT_URL, profile_id="products-and-offers").allowed
    assert engine.crawl
    _ = (evidence, extractor, identity, catalog, profiles, query)
