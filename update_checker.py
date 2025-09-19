"""Remote update checker for RA7 Premium App."""
from __future__ import annotations
import json
import urllib.request

RELEASE_API = "https://api.github.com/repos/unknown/RA7-AGI-3.0/releases/latest"


def fetch_latest_version() -> str:
    """Return the latest version tag from the GitHub releases API."""
    try:
        with urllib.request.urlopen(RELEASE_API, timeout=5) as resp:
            data = json.load(resp)
        return str(data.get("tag_name", ""))
    except Exception:
        return ""


def is_update_available(current_version: str) -> bool:
    latest = fetch_latest_version().lstrip("v")
    return bool(latest and latest != current_version)
