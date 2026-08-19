from __future__ import annotations

from ttc.adapters.html import HtmlExtractor
from ttc.adapters.memory import load_profile
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_malformed_json_ld_does_not_crash() -> None:
    profile = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    body = b'<title>Broken</title><script type="application/ld+json">{not json}</script>'
    digest = "1" * 64
    evidence = Evidence(
        evidence_id=evidence_id_for(digest),
        content_sha256=digest,
        fetched_url="https://html.example/broken",
        captured_at="2026-08-19T00:00:00Z",
        content_type="text/html",
        body=body,
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id=profile.profile_id,
        run_id="run_1",
    )
    records = HtmlExtractor().extract(evidence, profile)
    assert records[0].payload["title"] == "Broken"
    assert "json_ld" not in records[0].payload
