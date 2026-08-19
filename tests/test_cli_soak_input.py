from __future__ import annotations

import pytest

from ttc.cli import main


def test_soak_rejects_non_integer_cycles() -> None:
    with pytest.raises(PermissionError, match="soak_cycles_not_int"):
        main(["soak", "forever"])
    with pytest.raises(PermissionError, match="soak_cycles_out_of_range"):
        main(["soak", "1000"])
