from __future__ import annotations

from pathlib import Path

from ttc.assurance.catalog import load_catalog

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_oracle_files_exist() -> None:
    catalog = load_catalog()
    for item in catalog["properties"]:
        for ref in item["oracle_refs"]:
            path = ROOT / ref.split("::", 1)[0]
            assert path.exists(), f"missing oracle {ref}"
        for scope in item["mutation_scope"]:
            assert (ROOT / scope).exists(), f"missing mutation scope {scope}"
