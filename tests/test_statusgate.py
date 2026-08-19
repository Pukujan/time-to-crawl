from __future__ import annotations

import pytest

from ttc.domain.statusgate import blocked_body_must_not_succeed


def test_non_success_statuses_fail_closed() -> None:
    blocked_body_must_not_succeed(200, b"ok")
    with pytest.raises(PermissionError, match="status_blocked"):
        blocked_body_must_not_succeed(403, b"forbidden")
    with pytest.raises(PermissionError, match="status_retryable"):
        blocked_body_must_not_succeed(429, b"slow down")
    with pytest.raises(PermissionError, match="empty_body"):
        blocked_body_must_not_succeed(200, b"")
