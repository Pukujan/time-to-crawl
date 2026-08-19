from __future__ import annotations

SECRET_HEADER_NAMES = frozenset(
    {
        "authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
        "proxy-authorization",
    }
)


def sanitize_headers(headers: tuple[tuple[str, str], ...]) -> tuple[tuple[str, str], ...]:
    cleaned: list[tuple[str, str]] = []
    for name, value in headers:
        if name.lower() in SECRET_HEADER_NAMES:
            cleaned.append((name, "[redacted]"))
        else:
            cleaned.append((name, value))
    return tuple(cleaned)
