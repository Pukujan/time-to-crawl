from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HoldoutReceipt:
    suite_id: str
    ran: bool
    cases_visible_to_agent: bool
    aggregate: str


def run_public_interface(*, private_suite_present: bool) -> HoldoutReceipt:
    """Public interface only. Exact holdout cases stay outside this repository."""
    if not private_suite_present:
        return HoldoutReceipt(
            suite_id="ttc.holdout.v1",
            ran=False,
            cases_visible_to_agent=False,
            aggregate="NOT_CONFIGURED",
        )
    return HoldoutReceipt(
        suite_id="ttc.holdout.v1",
        ran=True,
        cases_visible_to_agent=False,
        aggregate="SEALED",
    )
