from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        "127.0.0.1:*",
        "localhost:*",
        "[::1]:*",
        "ai-professional-profile.onrender.com",
    ],
    allowed_origins=[
        "http://127.0.0.1:*",
        "http://localhost:*",
        "http://[::1]:*",
        "https://ai-professional-profile.onrender.com",
    ],
)

mcp = FastMCP(
    "AI Professional Profile",
    stateless_http=True,
    json_response=True,
    transport_security=transport_security,
)

@mcp.tool()
def get_profile() -> dict[str, str]:
    """Return the temporary MVP profile used for MCP connectivity testing."""
    return {
        "name": "Miodrag Strak",
        "profile_status": "Professional profile data will be added in a later step.",
    }
