from __future__ import annotations

from ttc.adapters.memory import load_profile
from ttc.domain.profile_policy import refresh_interval
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_default_refresh_interval_is_one_day() -> None:
    jobs = load_profile(ROOT / "contracts" / "profiles" / "jobs.v1.json")
    assert refresh_interval(jobs) == 86400
