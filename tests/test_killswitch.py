from __future__ import annotations

import pytest

from ttc.domain.killswitch import disable, enable, is_enabled


def test_live_engines_cannot_be_enabled_yet() -> None:
    assert is_enabled("fake") is True
    disable("fake")
    assert is_enabled("fake") is False
    enable("fake")
    with pytest.raises(PermissionError, match="engine_enable_blocked_until_issue_4"):
        enable("crawlee")
    with pytest.raises(PermissionError, match="engine_enable_blocked_until_issue_4"):
        enable("scrapy")
    enable("fake")
