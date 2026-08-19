from __future__ import annotations


class LiveSearchAdapter:
    """Tavily/Exa/SearXNG/Brave live search. Fail-closed until #4."""

    def __init__(self, provider: str) -> None:
        self.provider = provider

    def discover(self, query: str, *, profile_id: str) -> tuple[str, ...]:
        raise PermissionError(f"live_search_blocked_until_issue_4:{self.provider}")
