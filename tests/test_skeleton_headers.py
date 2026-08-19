from __future__ import annotations

from ttc.cli import PRODUCT_URL, build_skeleton


def test_skeleton_evidence_headers_are_redacted() -> None:
    skeleton = build_skeleton()
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    assert ("authorization", "[redacted]") in result.headers
    assert not any("Bearer" in value for _, value in result.headers)
    assert all(link.evidence_id == result.evidence_id for link in result.provenance)
