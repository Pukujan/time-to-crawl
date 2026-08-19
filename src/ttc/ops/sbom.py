from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def write_sbom(path: Path) -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    deps = []
    for line in pyproject.splitlines():
        stripped = line.strip().strip(",")
        if stripped.startswith('"') and any(name in stripped for name in ("jsonschema", "zstandard", "pytest", "hypothesis")):
            deps.append(stripped.strip('"'))
    payload = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "components": [{"name": item, "type": "library"} for item in deps],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
