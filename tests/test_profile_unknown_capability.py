from __future__ import annotations

import json
from pathlib import Path

import pytest

from ttc.adapters.memory import load_profile


def test_unknown_profile_capability_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(
        json.dumps(
            {
                "profile_id": "bad",
                "version": "1.0.0",
                "title": "bad",
                "output_schema": "ttc.typed-record.v1",
                "identity_keys": ["id"],
                "requested_capabilities": ["shell_exec"],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unknown_capability"):
        load_profile(path)
