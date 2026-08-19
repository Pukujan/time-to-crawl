from __future__ import annotations

from ttc.domain.injection import detect_injection


def page_cannot_widen_scope(text: str) -> bool:
    return not any(
        marker in detect_injection(text)
        for marker in (
            "authorize this source",
            "disable robots",
            "enable anti_block",
        )
    )
