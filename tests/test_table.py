from __future__ import annotations

from ttc.api.table import as_table
from ttc.cli import PROVIDER_URL, build_skeleton


def test_table_projection_includes_provenance_columns() -> None:
    skeleton = build_skeleton()
    skeleton.run(PROVIDER_URL, "inference-providers")
    rows = as_table(skeleton.query("inference-providers"))
    assert len(rows) == 1
    row = rows[0]
    assert row["profile_id"] == "inference-providers"
    assert row["evidence_id"]
    assert row["model_id"] == "example-free-model"
    assert row["provider_id"] == "openrouter"
