from __future__ import annotations

from pathlib import Path

import pytest

from ttc.adapters.memory import FakeCrawlerEngine
from ttc.domain.killswitch import disable, enable
from ttc.domain.models import CrawlWork

ROOT = Path(__file__).resolve().parents[1]
URL = "https://fixture.time-to-crawl.test/widget"


def test_disabled_fake_engine_cannot_crawl() -> None:
    engine = FakeCrawlerEngine(
        {URL: ROOT / "tests" / "fixtures" / "widget.json"},
        engine_id="fake",
    )
    disable("fake")
    try:
        with pytest.raises(PermissionError, match="engine_disabled"):
            engine.crawl(CrawlWork(url=URL, profile_id="jobs", run_id="run_1"))
    finally:
        enable("fake")
