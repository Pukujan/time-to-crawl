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
from ttc.adapters.receipts import ReceiptLog
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


def status() -> dict[str, object]:
    from ttc.assurance.catalog import property_ids

    profiles = load_reference_profiles()
    return {
        "live_crawl": False,
        "robots_default": "on",
        "anti_block_default": "off",
        "profiles": sorted(profiles),
        "property_count": len(property_ids()),
        "engines": {
            "fake": "available",
            "crawlee": "blocked_until_issue_4",
            "scrapy": "blocked_until_issue_4",
            "playwright": "blocked_until_issue_4",
            "firecrawl": "blocked_until_issue_4",
            "browsertrix": "blocked_until_issue_4",
        },
        "issue_gate": "#4 isolation before real Web",
    }


def main(argv: list[str] | None = None) -> None:
    import sys

    args = argv if argv is not None else sys.argv[1:]
    if args and args[0] == "status":
        print(json.dumps(status(), indent=2))
        return
    if args and args[0] == "properties":
        from ttc.assurance.catalog import property_ids

        print(json.dumps(list(property_ids()), indent=2))
        return
    if args and args[0] == "receipts":
        path = Path(args[1] if len(args) > 1 else "receipts.jsonl")
        print(json.dumps(list(ReceiptLog(path).load()), indent=2))
        return
    if args and args[0] == "profiles":
        print(json.dumps([profile.to_record() for profile in load_reference_profiles().values()], indent=2))
        return
    skeleton = build_skeleton()
    products = skeleton.run(PRODUCT_URL, "products-and-offers")
    jobs = skeleton.run(JOB_URL, "jobs")
    providers = skeleton.run(PROVIDER_URL, "inference-providers")
    legal = skeleton.run(LEGAL_URL, "legal-documents")
    receipt_path = Path("receipts.jsonl")
    log = ReceiptLog(receipt_path)
    for result in (products, jobs, providers, legal):
        if result.receipt is not None:
            log.append(result.receipt)
    print(
        json.dumps(
            {
                "products": {
                    "profile_id": products.profile_id,
                    "evidence_id": products.evidence_id,
                    "receipt_id": products.receipt.receipt_id if products.receipt else None,
                    "record_count": len(products.records),
                },
                "jobs": {
                    "profile_id": jobs.profile_id,
                    "evidence_id": jobs.evidence_id,
                    "receipt_id": jobs.receipt.receipt_id if jobs.receipt else None,
                    "record_count": len(jobs.records),
                },
                "providers": {
                    "profile_id": providers.profile_id,
                    "evidence_id": providers.evidence_id,
                    "receipt_id": providers.receipt.receipt_id if providers.receipt else None,
                    "record_count": len(providers.records),
                },
                "legal": {
                    "profile_id": legal.profile_id,
                    "evidence_id": legal.evidence_id,
                    "receipt_id": legal.receipt.receipt_id if legal.receipt else None,
                    "record_count": len(legal.records),
                },
                "receipt_log": str(receipt_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
