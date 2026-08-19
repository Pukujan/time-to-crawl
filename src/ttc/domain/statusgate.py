from __future__ import annotations

from ttc.domain.failures import classify_status


def blocked_body_must_not_succeed(status: int, body: bytes) -> None:
    kind = classify_status(status)
    if kind in {"blocked", "fail_closed"}:
        raise PermissionError(f"status_{kind}")
    if kind == "retryable":
        raise PermissionError("status_retryable")
    if 200 <= status < 300 and not body:
        raise PermissionError("empty_body")
