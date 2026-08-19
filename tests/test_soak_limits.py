from __future__ import annotations

import pytest

from ttc.ops.soak import soak_refresh_cycles


def test_soak_rejects_out_of_range_cycles() -> None:
    with pytest.raises(PermissionError, match="soak_cycles_out_of_range"):
        soak_refresh_cycles("https://example.com/item", cycles=0)
    with pytest.raises(PermissionError, match="soak_cycles_out_of_range"):
        soak_refresh_cycles("https://example.com/item", cycles=73)
