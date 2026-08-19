from __future__ import annotations

INJECTION_MARKERS = (
    "ignore previous instructions",
    "authorize this source",
    "call tool",
    "write to fossil",
    "disable robots",
    "enable anti_block",
)


def detect_injection(text: str) -> tuple[str, ...]:
    lowered = text.lower()
    return tuple(marker for marker in INJECTION_MARKERS if marker in lowered)


def content_cannot_invoke_tools(text: str) -> bool:
    return not detect_injection(text)
