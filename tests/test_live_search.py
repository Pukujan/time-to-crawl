from __future__ import annotations

import pytest

from ttc.adapters.search import LiveSearchAdapter


def test_live_search_adapters_fail_closed() -> None:
    for provider in ("tavily", "exa", "searxng", "brave"):
        with pytest.raises(PermissionError, match="live_search_blocked_until_issue_4"):
            LiveSearchAdapter(provider).discover("query", profile_id="jobs")
