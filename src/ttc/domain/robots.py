from __future__ import annotations

from urllib.parse import urlparse


def robots_allows(robots_txt: str, path: str, user_agent: str = "*") -> bool:
    rules = _rules_for(robots_txt, user_agent)
    matches = [(kind, value) for kind, value in rules if path.startswith(value)]
    if not matches:
        return True
    kind, _value = max(matches, key=lambda item: (len(item[1]), item[0] == "allow"))
    return kind == "allow"


def _rules_for(robots_txt: str, user_agent: str) -> list[tuple[str, str]]:
    current: list[str] = []
    matching = False
    rules: list[tuple[str, str]] = []
    for raw in robots_txt.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "user-agent":
            current = [value.lower()]
            matching = value == "*" or value.lower() == user_agent.lower()
            continue
        if not matching:
            continue
        if key in {"allow", "disallow"} and value:
            rules.append((key, value))
    _ = current
    return rules


def path_of(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path or "/"
