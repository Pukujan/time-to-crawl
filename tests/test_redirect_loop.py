from __future__ import annotations

from ttc.domain.redirects import detect_redirect_loop


def test_redirect_loop_is_detected() -> None:
    hops = (
        "https://example.com/a",
        "https://example.com/b",
        "https://example.com/a/#frag",
    )
    assert detect_redirect_loop(hops) is True
    assert detect_redirect_loop(("https://example.com/a", "https://example.com/b")) is False
