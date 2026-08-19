from __future__ import annotations

from ttc.cli import PRODUCT_URL, build_skeleton


def test_skeleton_provenance_records_robots_compliant() -> None:
    skeleton = build_skeleton()
    result = skeleton.run(PRODUCT_URL, "products-and-offers")
    assert result.provenance
    assert all(link.robots_compliant is True for link in result.provenance)
    assert all(link.policy_reason == "allowlisted" for link in result.provenance)
