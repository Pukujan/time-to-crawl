from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src" / "ttc"

FORBIDDEN = (
    "crawlee",
    "scrapy",
    "playwright",
    "browsertrix",
    "crawl4ai",
    "firecrawl",
    "searxng",
    "tavily",
    "exa",
    "tika",
    "psycopg",
    "pgvector",
    "fossil_core",
    "graphiti",
    "neo4j",
)

DOMAIN_FORBIDDEN = FORBIDDEN + ("jsonschema", "zstandard")

LAYER_RULES = {
    "domain": {"allowed_prefixes": ("ttc.domain",)},
    "ports": {"allowed_prefixes": ("ttc.domain", "ttc.ports")},
    "application": {"allowed_prefixes": ("ttc.domain", "ttc.ports", "ttc.application")},
    "api": {"allowed_prefixes": ("ttc.domain", "ttc.ports", "ttc.api")},
    "profiles": {"allowed_prefixes": ("ttc.domain", "ttc.profiles")},
    "ops": {"allowed_prefixes": ("ttc.domain", "ttc.ops")},
    "assurance": {"allowed_prefixes": ("ttc.domain", "ttc.ports", "ttc.assurance")},
}


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def _layer_files(layer: str) -> list[Path]:
    return [path for path in (ROOT / layer).rglob("*.py") if path.name != "__pycache__"]


def test_forbidden_vendor_imports_are_absent() -> None:
    for path in ROOT.rglob("*.py"):
        forbidden = DOMAIN_FORBIDDEN if "domain" in path.parts or "ports" in path.parts else FORBIDDEN
        for name in _imports(path):
            root = name.split(".")[0]
            assert root not in forbidden, f"{path} imports {name}"


def test_layer_import_direction() -> None:
    for layer, rule in LAYER_RULES.items():
        for path in _layer_files(layer):
            for name in _imports(path):
                if not name.startswith("ttc."):
                    continue
                assert any(
                    name == prefix or name.startswith(prefix + ".")
                    for prefix in rule["allowed_prefixes"]
                ), f"{path} imports {name}"


def test_adapters_do_not_import_other_adapter_packages() -> None:
    adapter_root = ROOT / "adapters"
    for path in adapter_root.rglob("*.py"):
        for name in _imports(path):
            if name.startswith("ttc.adapters.") and name.count(".") > 2:
                raise AssertionError(f"{path} imports adapter internals {name}")
