from __future__ import annotations

from pathlib import Path

from ttc.adapters.memory import FakeCrawlerEngine
from ttc.domain.models import CrawlWork

ROOT = Path(__file__).resolve().parents[1]
URL = "https://fixture.time-to-crawl.test/widget"
FIXTURE = ROOT / "tests" / "fixtures" / "widget.json"


def test_two_fakes_preserve_receipt_semantics() -> None:
    work = CrawlWork(url=URL, profile_id="products-and-offers", run_id="run_1")
    a = FakeCrawlerEngine({URL: FIXTURE}, engine_id="fake-a").crawl(work)
    b = FakeCrawlerEngine({URL: FIXTURE}, engine_id="fake-b").crawl(work)
    assert a.requested_url == b.requested_url == URL
    assert a.final_url == b.final_url
    assert a.status == b.status == 200
    assert a.body == b.body
    assert a.engine_id != b.engine_id
    assert a.engine_version
    assert b.engine_version
