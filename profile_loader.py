import json
import sys
from pathlib import Path
from typing import Any


def find_profile_path() -> Path:
    """Return the first available professional profile data file."""
    candidates = (
        Path(__file__).with_name("profile.json"),
        Path(sys.prefix) / "profile.json",
    )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    searched_paths = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(
        f"Professional profile data file was not found. Searched: {searched_paths}"
    )


def load_profile_data() -> dict[str, Any]:
    """Load and return the professional profile data."""
    profile_path = find_profile_path()

    with profile_path.open(encoding="utf-8") as profile_file:
        profile_data = json.load(profile_file)

    if not isinstance(profile_data, dict):
        raise ValueError("Professional profile data must be a JSON object.")

    return profile_data
