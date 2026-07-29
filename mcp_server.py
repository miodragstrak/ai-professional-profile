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


@mcp.tool()
def get_projects() -> dict[str, list[dict[str, Any]]]:
    """Return the approved public professional projects."""
    profile_data = load_profile_data()
    projects = profile_data.get("projects")

    if not isinstance(projects, list):
        raise ValueError(
            "Professional profile data must contain a projects array."
        )

    if not all(isinstance(project, dict) for project in projects):
        raise ValueError(
            "Every professional project must be a JSON object."
        )

    return {"projects": projects}


@mcp.tool()
def get_experience() -> dict[str, list[dict[str, Any]]]:
    """Return the approved public professional experience."""
    profile_data = load_profile_data()
    experience = profile_data.get("experience")

    if not isinstance(experience, list):
        raise ValueError(
            "Professional profile data must contain an experience array."
        )

    if not all(
        isinstance(experience_item, dict)
        for experience_item in experience
    ):
        raise ValueError(
            "Every professional experience item must be a JSON object."
        )

    return {"experience": experience}
