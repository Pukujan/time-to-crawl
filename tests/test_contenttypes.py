from __future__ import annotations

from ttc.adapters.memory import load_profile
from ttc.domain.contenttypes import content_type_allowed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_profile_content_types() -> None:
    products = load_profile(ROOT / "contracts" / "profiles" / "products-and-offers.v1.json")
    legal = load_profile(ROOT / "contracts" / "profiles" / "legal-documents.v1.json")
    assert content_type_allowed(products, "application/json")
    assert content_type_allowed(products, "text/html; charset=utf-8")
    assert not content_type_allowed(products, "application/pdf")
    assert content_type_allowed(legal, "application/pdf")
