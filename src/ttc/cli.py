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


def build_skeleton(*, engine_id: str = "fake") -> WalkingSkeleton:
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


def main() -> None:
    skeleton = build_skeleton()
    products = skeleton.run(PRODUCT_URL, "products-and-offers")
    jobs = skeleton.run(JOB_URL, "jobs")
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
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
