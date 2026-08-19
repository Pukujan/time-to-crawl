from __future__ import annotations

import pytest

from ttc.domain.killswitch import disable, enable, is_enabled


def test_live_engines_cannot_be_enabled_yet() -> None:
    assert is_enabled("fake") is True
    disable("fake")
    assert is_enabled("fake") is False
    enable("fake")
    for engine_id in ("crawlee", "scrapy", "firecrawl", "browsertrix", "playwright"):
        with pytest.raises(PermissionError, match="engine_enable_blocked_until_issue_4"):
            enable(engine_id)
        assert is_enabled(engine_id) is False
    enable("fake")
