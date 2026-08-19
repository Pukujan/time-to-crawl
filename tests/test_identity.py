from __future__ import annotations

from pathlib import Path

from ttc.adapters.memory import (
    FileProfileRegistry,
    KeyIdentityResolver,
    SchemaGuidedExtractor,
    load_profile,
)
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence

ROOT = Path(__file__).resolve().parents[1]


def test_identity_uses_profile_keys_not_similarity() -> None:
    profile = load_profile(ROOT / "contracts" / "profiles" / "jobs.v1.json")
    body = (ROOT / "tests" / "fixtures" / "job.json").read_bytes()
    evidence = Evidence(
        evidence_id=evidence_id_for("b" * 64),
        content_sha256="b" * 64,
        fetched_url="https://fixture.time-to-crawl.test/job",
        captured_at="2026-08-19T00:00:00Z",
        content_type="application/json",
        body=body,
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id=profile.profile_id,
        run_id="run_1",
    )
    extracted = SchemaGuidedExtractor().extract(evidence, profile)
    resolved = KeyIdentityResolver().resolve(extracted)
    assert resolved[0].identity_key == "REQ-441|https://jobs.example/req-441"
    near = dict(resolved[0].payload)
    near["title"] = "Almost the same job"
    near["embedding"] = [0.99, 0.01]
    second = SchemaGuidedExtractor().extract(
        Evidence(
            evidence_id=evidence.evidence_id,
            content_sha256=evidence.content_sha256,
            fetched_url=evidence.fetched_url,
            captured_at=evidence.captured_at,
            content_type=evidence.content_type,
            body=__import__("json").dumps({"records": [near]}).encode("utf-8"),
            engine_id=evidence.engine_id,
            engine_version=evidence.engine_version,
            profile_id=evidence.profile_id,
            run_id=evidence.run_id,
        ),
        profile,
    )
    assert second[0].identity_key == resolved[0].identity_key
    _ = FileProfileRegistry({profile.profile_id: profile})
