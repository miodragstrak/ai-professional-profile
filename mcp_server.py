from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "AI Professional Profile",
    stateless_http=True,
    json_response=True,
)

@mcp.tool()
def get_profile() -> dict[str, str]:
    """Return the temporary MVP profile used for MCP connectivity testing."""
    return {
        "name": "Miodrag Strak",
        "profile_status": "Professional profile data will be added in a later step.",
    }
