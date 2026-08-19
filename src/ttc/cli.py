from __future__ import annotations

import json
from pathlib import Path

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

ROOT = Path(__file__).resolve().parents[2]
PRODUCT_URL = "https://fixture.time-to-crawl.test/widget"
JOB_URL = "https://fixture.time-to-crawl.test/job"
PROVIDER_URL = "https://fixture.time-to-crawl.test/provider"
LEGAL_URL = "https://fixture.time-to-crawl.test/legal"


def load_reference_profiles() -> dict:
    names = (
        "products-and-offers.v1.json",
        "jobs.v1.json",
        "inference-providers.v1.json",
        "legal-documents.v1.json",
    )
    loaded = [load_profile(ROOT / "contracts" / "profiles" / name) for name in names]
    return {profile.profile_id: profile for profile in loaded}


def build_skeleton(*, engine_id: str = "fake") -> WalkingSkeleton:
    catalog = MemoryCatalog()
    profiles = load_reference_profiles()
    return WalkingSkeleton(
        policy=AllowlistPolicy(frozenset({PRODUCT_URL, JOB_URL, PROVIDER_URL, LEGAL_URL})),
        engine=FakeCrawlerEngine(
            {
                PRODUCT_URL: ROOT / "tests" / "fixtures" / "widget.json",
                JOB_URL: ROOT / "tests" / "fixtures" / "job.json",
                PROVIDER_URL: ROOT / "tests" / "fixtures" / "provider.json",
                LEGAL_URL: ROOT / "tests" / "fixtures" / "legal.json",
            },
            engine_id=engine_id,
        ),
        evidence=MemoryEvidenceStore(),
        extractor=SchemaGuidedExtractor(),
        identity=KeyIdentityResolver(),
        catalog=catalog,
        profiles=FileProfileRegistry(profiles),
        query=MemoryQuery(catalog),
    )


def main() -> None:
    skeleton = build_skeleton()
    products = skeleton.run(PRODUCT_URL, "products-and-offers")
    jobs = skeleton.run(JOB_URL, "jobs")
    providers = skeleton.run(PROVIDER_URL, "inference-providers")
    legal = skeleton.run(LEGAL_URL, "legal-documents")
    print(
        json.dumps(
            {
                "products": {
                    "profile_id": products.profile_id,
                    "evidence_id": products.evidence_id,
                    "record_count": len(products.records),
                },
                "jobs": {
                    "profile_id": jobs.profile_id,
                    "evidence_id": jobs.evidence_id,
                    "record_count": len(jobs.records),
                },
                "providers": {
                    "profile_id": providers.profile_id,
                    "evidence_id": providers.evidence_id,
                    "record_count": len(providers.records),
                },
                "legal": {
                    "profile_id": legal.profile_id,
                    "evidence_id": legal.evidence_id,
                    "record_count": len(legal.records),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
