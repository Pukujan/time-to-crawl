from __future__ import annotations

import pytest

from ttc.adapters.memory import SchemaGuidedExtractor, load_profile
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_missing_identity_key_fails_closed() -> None:
    profile = load_profile(ROOT / "contracts" / "profiles" / "jobs.v1.json")
    body = b'{"records":[{"title":"Staff"}]}'
    digest = "2" * 64
    evidence = Evidence(
        evidence_id=evidence_id_for(digest),
        content_sha256=digest,
        fetched_url="https://jobs.example/x",
        captured_at="2026-08-19T00:00:00Z",
        content_type="application/json",
        body=body,
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id=profile.profile_id,
        run_id="run_1",
    )
    with pytest.raises(ValueError, match="missing_identity_key"):
        SchemaGuidedExtractor().extract(evidence, profile)
