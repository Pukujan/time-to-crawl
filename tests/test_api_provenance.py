from __future__ import annotations

from ttc.api.provenance import expand_provenance
from ttc.cli import PRODUCT_URL, build_skeleton


def test_provenance_expansion_requires_evidence() -> None:
    skeleton = build_skeleton()
    skeleton.run(PRODUCT_URL, "products-and-offers")
    record = skeleton.query("products-and-offers")[0]
    expanded = expand_provenance(record)
    assert expanded["evidence_id"] == record.evidence_id
    assert expanded["profile_id"] == "products-and-offers"
