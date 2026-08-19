from __future__ import annotations

import pytest

from ttc.domain.querylimit import clamp_limit


def test_query_limit_is_clamped() -> None:
    assert clamp_limit(None) == 50
    assert clamp_limit(10) == 10
    with pytest.raises(PermissionError, match="limit_too_small"):
        clamp_limit(0)
    with pytest.raises(PermissionError, match="limit_too_large"):
        clamp_limit(201)
