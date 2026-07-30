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
        "mcp.mstrak.online",
    ],
    allowed_origins=[
        "http://127.0.0.1:*",
        "http://localhost:*",
        "http://[::1]:*",
        "https://ai-professional-profile.onrender.com",
        "https://mcp.mstrak.online",
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


@mcp.tool()
def get_skills() -> dict[str, Any]:
    """Return approved professional skills and industry domains."""
    profile_data = load_profile_data()
    skills = profile_data.get("skills")
    domains = profile_data.get("domains")

    if not isinstance(skills, dict):
        raise ValueError(
            "Professional profile data must contain a skills object."
        )

    expected_categories = (
        "core",
        "supporting",
        "technologies",
    )

    for category in expected_categories:
        category_skills = skills.get(category)

        if not isinstance(category_skills, list):
            raise ValueError(
                f"Skills category {category!r} must be an array."
            )

        if not all(
            isinstance(skill, str)
            for skill in category_skills
        ):
            raise ValueError(
                f"Every skill in category {category!r} "
                "must be a string."
            )

    if not isinstance(domains, list):
        raise ValueError(
            "Professional profile data must contain a domains array."
        )

    if not all(isinstance(domain, str) for domain in domains):
        raise ValueError(
            "Every professional domain must be a string."
        )

    return {
        "skills": skills,
        "domains": domains,
    }


@mcp.tool()
def get_links() -> dict[str, list[dict[str, Any]]]:
    """Return approved public professional links."""
    profile_data = load_profile_data()
    links = profile_data.get("links")

    if not isinstance(links, list):
        raise ValueError(
            "Professional profile data must contain a links array."
        )

    if not all(isinstance(link, dict) for link in links):
        raise ValueError(
            "Every professional link must be a JSON object."
        )

    required_fields = (
        "id",
        "label",
        "type",
        "url",
        "source_id",
        "verification_status",
    )

    for link in links:
        for field in required_fields:
            if field not in link:
                raise ValueError(
                    f"Professional link is missing field {field!r}."
                )

        if not isinstance(link["id"], str):
            raise ValueError(
                "Every professional link id must be a string."
            )

        if not isinstance(link["label"], str):
            raise ValueError(
                "Every professional link label must be a string."
            )

        if not isinstance(link["type"], str):
            raise ValueError(
                "Every professional link type must be a string."
            )

        if not isinstance(link["url"], str):
            raise ValueError(
                "Every professional link URL must be a string."
            )

        if (
            link["source_id"] is not None
            and not isinstance(link["source_id"], str)
        ):
            raise ValueError(
                "Professional link source_id must be a string or null."
            )

        if not isinstance(link["verification_status"], str):
            raise ValueError(
                "Every link verification status must be a string."
            )

    return {"links": links}
