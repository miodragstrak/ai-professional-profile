import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_BASE_URL = "https://api.github.com"
DEFAULT_USERNAME = "miodragstrak"
DEFAULT_OUTPUT_PATH = Path("snapshots/github.json")

REQUEST_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "AI-Professional-Profile/0.1",
    "X-GitHub-Api-Version": "2026-03-10",
}

PROFILE_FIELDS = (
    "login",
    "name",
    "bio",
    "company",
    "location",
    "blog",
    "html_url",
    "public_repos",
    "followers",
    "following",
    "created_at",
    "updated_at",
)

REPOSITORY_FIELDS = (
    "name",
    "full_name",
    "html_url",
    "description",
    "homepage",
    "language",
    "topics",
    "fork",
    "archived",
    "disabled",
    "visibility",
    "stargazers_count",
    "forks_count",
    "open_issues_count",
    "default_branch",
    "created_at",
    "updated_at",
    "pushed_at",
)


def fetch_json(url: str) -> Any:
    """Fetch and decode a JSON document from the GitHub API."""
    request = Request(url, headers=REQUEST_HEADERS)

    with urlopen(request, timeout=30) as response:
        return json.load(response)


def select_fields(
    source: dict[str, Any],
    fields: tuple[str, ...],
) -> dict[str, Any]:
    """Return only approved fields from a GitHub API object."""
    return {
        field: source.get(field)
        for field in fields
    }


def normalize_profile(profile_data: Any) -> dict[str, Any]:
    """Normalize the public GitHub profile response."""
    if not isinstance(profile_data, dict):
        raise ValueError("GitHub profile response must be a JSON object.")

    return select_fields(profile_data, PROFILE_FIELDS)


def normalize_repository(repository_data: Any) -> dict[str, Any]:
    """Normalize one public GitHub repository response."""
    if not isinstance(repository_data, dict):
        raise ValueError("GitHub repository response must be a JSON object.")

    return select_fields(repository_data, REPOSITORY_FIELDS)


def fetch_repositories(username: str) -> list[dict[str, Any]]:
    """Fetch all public repositories owned by the specified user."""
    encoded_username = quote(username, safe="")
    repositories: list[dict[str, Any]] = []
    page = 1

    while True:
        query = urlencode(
            {
                "type": "owner",
                "sort": "updated",
                "direction": "desc",
                "per_page": 100,
                "page": page,
            }
        )

        response_data = fetch_json(
            f"{API_BASE_URL}/users/{encoded_username}/repos?{query}"
        )

        if not isinstance(response_data, list):
            raise ValueError(
                "GitHub repositories response must be a JSON array."
            )

        repositories.extend(
            normalize_repository(repository)
            for repository in response_data
        )

        if len(response_data) < 100:
            break

        page += 1

    return repositories


def build_snapshot(
    username: str,
    profile_data: Any,
    repositories: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a reviewable GitHub source snapshot."""
    return {
        "snapshot_version": "0.1",
        "source_id": "github",
        "source_url": f"https://github.com/{username}",
        "retrieved_at": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "retrieval_status": "retrieved",
        "approval_status": "not_reviewed",
        "source_data": {
            "profile": normalize_profile(profile_data),
            "repositories": repositories,
        },
        "candidate_updates": {
            "profile": {},
            "projects": [],
            "skills": [],
        },
    }


def write_snapshot(
    snapshot: dict[str, Any],
    output_path: Path,
) -> None:
    """Write the snapshot atomically as formatted JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = output_path.with_suffix(
        f"{output_path.suffix}.tmp"
    )

    temporary_path.write_text(
        json.dumps(
            snapshot,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    temporary_path.replace(output_path)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch a reviewable public GitHub profile snapshot."
    )

    parser.add_argument(
        "--username",
        default=DEFAULT_USERNAME,
        help="GitHub username to retrieve.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Snapshot JSON output path.",
    )

    return parser.parse_args()


def main() -> None:
    """Fetch public GitHub data and write the source snapshot."""
    args = parse_args()
    username = args.username.strip()

    if not username:
        raise ValueError("GitHub username must not be empty.")

    encoded_username = quote(username, safe="")

    profile_data = fetch_json(
        f"{API_BASE_URL}/users/{encoded_username}"
    )

    repositories = fetch_repositories(username)

    snapshot = build_snapshot(
        username=username,
        profile_data=profile_data,
        repositories=repositories,
    )

    write_snapshot(snapshot, args.output)

    print("GitHub snapshot written:")
    print(args.output)
    print("Repositories retrieved:")
    print(len(repositories))


if __name__ == "__main__":
    main()
