from __future__ import annotations

from ttc.domain.failures import classify_status, should_retry


def test_blocked_statuses_do_not_retry_without_capability() -> None:
    assert classify_status(200) == "success"
    assert classify_status(429) == "retryable"
    assert classify_status(403) == "blocked"
    assert should_retry(429, anti_block=False) is True
    assert should_retry(403, anti_block=False) is False
    assert should_retry(403, anti_block=True) is False
    assert classify_status(418) == "fail_closed"
