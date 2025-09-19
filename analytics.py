"""Usage analytics tracker for RA7 Premium App."""
import json
import os
from base64 import urlsafe_b64encode
from datetime import date

ANALYTICS_FILE = os.environ.get("RA7_ANALYTICS_FILE", "analytics.json")


def _load() -> dict:
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"daily": {}, "revenue": 0.0}


def _save(data: dict) -> None:
    with open(ANALYTICS_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def log_event(event: str) -> None:
    data = _load()
    today = date.today().isoformat()
    daily = data["daily"].setdefault(today, {})
    daily[event] = daily.get(event, 0) + 1
    _save(data)


def log_revenue(amount: float) -> None:
    data = _load()
    data["revenue"] = round(data.get("revenue", 0.0) + amount, 2)
    _save(data)


def generate_referral_code() -> str:
    """Return a short, URL-safe referral code."""
    return urlsafe_b64encode(os.urandom(9)).decode("ascii").rstrip("=")
