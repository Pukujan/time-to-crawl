from __future__ import annotations

RETRYABLE = frozenset({429, 500, 502, 503, 504})
BLOCKED = frozenset({401, 403, 407})
NOT_FOUND = frozenset({404, 410})


def classify_status(status: int) -> str:
    if status in RETRYABLE:
        return "retryable"
    if status in BLOCKED:
        return "blocked"
    if status in NOT_FOUND:
        return "not_found"
    if 200 <= status < 300:
        return "success"
    if 300 <= status < 400:
        return "redirect"
    return "fail_closed"


def should_retry(status: int, *, anti_block: bool) -> bool:
    kind = classify_status(status)
    if kind == "blocked" and not anti_block:
        return False
    return kind == "retryable"
