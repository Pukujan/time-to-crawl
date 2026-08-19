from __future__ import annotations

import pytest

from ttc.domain.capability_check import granted_or_empty, unknown_capabilities


def test_unknown_capabilities_fail_closed() -> None:
    assert unknown_capabilities(("fetch_public", "not_a_real_cap")) == frozenset({"not_a_real_cap"})
    with pytest.raises(PermissionError, match="unknown_capability"):
        granted_or_empty(("shell_exec",))
    assert "fetch_public" in granted_or_empty(("fetch_public",))
