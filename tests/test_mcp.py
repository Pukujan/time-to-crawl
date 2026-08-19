from __future__ import annotations

from ttc.api.mcp import DENIED_MCP_TOOLS, catalog, is_allowed


def test_mcp_catalog_excludes_fetch_browser_authorize() -> None:
    names = {tool.name for tool in catalog()}
    assert "ttc.list_records" in names
    assert "ttc.source_propose" in names
    for denied in DENIED_MCP_TOOLS:
        assert denied not in names
        assert is_allowed(denied) is False
    assert is_allowed("ttc.source_propose") is True
    assert is_allowed("ttc.source_authorize") is False
