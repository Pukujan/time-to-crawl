from __future__ import annotations

from ttc.adapters.documents import TextDocumentExtractor
from ttc.adapters.memory import load_profile
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_text_document_extractor_preserves_source() -> None:
    profile = load_profile(ROOT / "contracts" / "profiles" / "legal-documents.v1.json")
    body = b"Opinion text for Example v. Example."
    digest = "f" * 64
    evidence = Evidence(
        evidence_id=evidence_id_for(digest),
        content_sha256=digest,
        fetched_url="https://fixture.time-to-crawl.test/legal",
        captured_at="2026-08-19T00:00:00Z",
        content_type="text/plain",
        body=body,
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id=profile.profile_id,
        run_id="run_1",
    )
    records = TextDocumentExtractor().extract(evidence, profile)
    assert records[0].payload["text"].startswith("Opinion text")
    assert records[0].evidence_id == evidence.evidence_id
