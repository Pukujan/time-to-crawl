from __future__ import annotations

from dataclasses import dataclass

from ttc.domain.models import CrawlResult, CrawlWork
from ttc.ports.crawler import CrawlerEnginePort


@dataclass(frozen=True)
class BakeoffCase:
    case_id: str
    work: CrawlWork
    expect_status: int
    expect_forbidden_outlink: bool = False


@dataclass(frozen=True)
class BakeoffReceipt:
    engine_id: str
    case_id: str
    passed: bool
    reason: str


def run_case(engine: CrawlerEnginePort, case: BakeoffCase) -> BakeoffReceipt:
    result = engine.crawl(case.work)
    if result.status != case.expect_status:
        return BakeoffReceipt(engine.engine_id if hasattr(engine, "engine_id") else "unknown", case.case_id, False, "status")
    if result.requested_url != case.work.url:
        return BakeoffReceipt(_engine_id(engine), case.case_id, False, "requested_url")
    if not result.engine_version:
        return BakeoffReceipt(_engine_id(engine), case.case_id, False, "engine_version")
    return BakeoffReceipt(_engine_id(engine), case.case_id, True, "ok")


def compare(left: tuple[BakeoffReceipt, ...], right: tuple[BakeoffReceipt, ...]) -> bool:
    left_map = {item.case_id: item.passed for item in left}
    right_map = {item.case_id: item.passed for item in right}
    return left_map == right_map


def _engine_id(engine: CrawlerEnginePort) -> str:
    return getattr(engine, "engine_id", "unknown")
