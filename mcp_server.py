from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from profile_loader import load_profile_data

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
def get_profile() -> dict[str, Any]:
    """Return the current public professional profile."""
    profile_data = load_profile_data()
    profile = profile_data.get("profile")

    if not isinstance(profile, dict):
        raise ValueError("Professional profile data must contain a profile object.")

    return profile
