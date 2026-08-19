from __future__ import annotations

from pathlib import Path

from ttc.ops.sbom import write_sbom


def test_sbom_lists_declared_dependencies(tmp_path: Path) -> None:
    path = tmp_path / "sbom.json"
    write_sbom(path)
    text = path.read_text(encoding="utf-8")
    assert "jsonschema" in text
    assert "zstandard" in text
