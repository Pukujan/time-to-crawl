from __future__ import annotations

from pathlib import Path

from ttc.adapters.html import HtmlExtractor
from ttc.adapters.memory import load_profile
from ttc.domain.identity import evidence_id_for
from ttc.domain.models import Evidence

ROOT = Path(__file__).resolve().parents[1]


def test_html_extractor_reads_json_ld() -> None:
    profile = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    body = (ROOT / "tests" / "fixtures" / "widget.html").read_bytes()
    digest = "e" * 64
    evidence = Evidence(
        evidence_id=evidence_id_for(digest),
        content_sha256=digest,
        fetched_url="https://html.example/widget",
        captured_at="2026-08-19T00:00:00Z",
        content_type="text/html",
        body=body,
        engine_id="fake",
        engine_version="0.0.0-fake",
        profile_id=profile.profile_id,
        run_id="run_1",
    )
    records = HtmlExtractor().extract(evidence, profile)
    assert len(records) == 1
    assert records[0].payload["title"] == "Acme Widget"
    assert records[0].payload["seller_id"] == "seller_html"
    assert "seller_html" in records[0].identity_key
