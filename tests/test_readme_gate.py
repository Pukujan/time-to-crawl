from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_and_agents_forbid_live_crawl_until_issue_4() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "#4" in readme
    assert "No live Web crawling" in readme or "no live" in readme.lower()
    assert "No live autonomous Web crawling until issue #4" in agents
    assert "Do not implement a custom generic crawler" in agents
