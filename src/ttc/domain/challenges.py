from __future__ import annotations

from ttc.domain.capabilities import DEFAULT_GRANTED


CHALLENGE_MARKERS = ("captcha", "access denied", "please verify you are human", "cf-challenge")
FORM_MARKERS = ("<form", "type=\"password\"")


def is_challenge(body: bytes | str) -> bool:
    text = body.decode("utf-8", errors="replace") if isinstance(body, bytes) else body
    lowered = text.lower()
    return any(marker in lowered for marker in CHALLENGE_MARKERS)


def wants_form_submit(body: bytes | str) -> bool:
    text = body.decode("utf-8", errors="replace") if isinstance(body, bytes) else body
    lowered = text.lower()
    return any(marker in lowered for marker in FORM_MARKERS)


def fail_closed_on_challenge(body: bytes | str, granted: frozenset[str] = DEFAULT_GRANTED) -> None:
    if is_challenge(body):
        raise PermissionError("challenge_fail_closed")
    if wants_form_submit(body) and "form_action" not in granted:
        raise PermissionError("form_action_denied")
