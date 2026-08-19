from __future__ import annotations

from dataclasses import dataclass

ALLOWED_MCP_TOOLS = (
    "ttc.list_records",
    "ttc.get_profile",
    "ttc.source_propose",
    "ttc.list_provenance",
)

DENIED_MCP_TOOLS = (
    "ttc.fetch",
    "ttc.browser",
    "ttc.source_authorize",
    "ttc.write_fossil",
    "ttc.admin",
)


@dataclass(frozen=True)
class McpTool:
    name: str
    description: str
    mutating: bool


def catalog() -> tuple[McpTool, ...]:
    return (
        McpTool("ttc.list_records", "List typed records for a profile", False),
        McpTool("ttc.get_profile", "Load a versioned profile", False),
        McpTool("ttc.source_propose", "Propose a source; does not authorize", True),
        McpTool("ttc.list_provenance", "Expand provenance for a record", False),
    )


def is_allowed(name: str) -> bool:
    return name in ALLOWED_MCP_TOOLS and name not in DENIED_MCP_TOOLS
