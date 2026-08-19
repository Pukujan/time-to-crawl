from __future__ import annotations

from pathlib import Path

from ttc.adapters.memory import FakeCrawlerEngine
from ttc.assurance.bakeoff import BakeoffCase, compare, run_case
from ttc.domain.models import CrawlWork

ROOT = Path(__file__).resolve().parents[1]
URL = "https://fixture.time-to-crawl.test/widget"
FIXTURE = ROOT / "tests" / "fixtures" / "widget.json"


def test_two_fake_engines_match_on_static_fixture() -> None:
    work = CrawlWork(url=URL, profile_id="products-and-offers", run_id="run_1")
    case = BakeoffCase(case_id="static-html", work=work, expect_status=200)
    left = run_case(FakeCrawlerEngine({URL: FIXTURE}, engine_id="crawlee-fake"), case)
    right = run_case(FakeCrawlerEngine({URL: FIXTURE}, engine_id="scrapy-fake"), case)
    assert left.passed and right.passed
    assert compare((left,), (right,))
    assert left.engine_id != right.engine_id
