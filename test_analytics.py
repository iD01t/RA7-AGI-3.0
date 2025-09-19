import json

import analytics


def test_event_and_revenue_logging(tmp_path, monkeypatch):
    file = tmp_path / "analytics.json"
    monkeypatch.setattr(analytics, "ANALYTICS_FILE", str(file))
    analytics.log_event("login")
    analytics.log_revenue(5.0)
    data = json.loads(file.read_text())
    assert data["revenue"] == 5.0
    assert "login" in next(iter(data["daily"].values()))


def test_referral_code_format():
    code = analytics.generate_referral_code()
    assert len(code) >= 10
