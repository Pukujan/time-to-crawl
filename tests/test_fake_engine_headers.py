from __future__ import annotations

from pathlib import Path

from ttc.adapters.memory import FakeCrawlerEngine
from ttc.domain.models import CrawlWork

ROOT = Path(__file__).resolve().parents[1]
URL = "https://fixture.time-to-crawl.test/widget"


def test_fake_engine_redacts_authorization_header() -> None:
    result = FakeCrawlerEngine({URL: ROOT / "tests" / "fixtures" / "widget.json"}).crawl(
        CrawlWork(url=URL, profile_id="products-and-offers", run_id="run_1")
    )
    assert ("authorization", "[redacted]") in result.headers
    assert not any(value == "Bearer secret" for _, value in result.headers)
