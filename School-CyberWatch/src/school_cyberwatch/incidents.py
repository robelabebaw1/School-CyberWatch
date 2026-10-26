"""Correlate local fictional alerts into small, explainable incidents."""

from typing import Any


RISK_POINTS = {
    "repeated_failed_login": 45,
    "multiple_usernames": 35,
    "file_changed": 20,
}


def calculate_risk(alert_types: list[str]) -> dict[str, Any]:
    """Calculate a transparent score from the alert types in an incident."""
    score = sum(RISK_POINTS[alert_type] for alert_type in alert_types)
    level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
    reasons = [
        f"{alert_type.replace('_', ' ')} (+{RISK_POINTS[alert_type]})"
        for alert_type in alert_types
    ]
    return {"score": score, "level": level, "reasons": reasons}


def build_incidents(
    events: list[dict[str, str]],
    repeated_login_alerts: list[dict[str, str | int]],
    multi_username_alerts: list[dict[str, str | int]],
    integrity_status: dict[str, str | bool],
) -> list[dict[str, Any]]:
    """Group alerts from the same fictional source into timeline incidents."""
    repeated_sources = {str(alert["source"]) for alert in repeated_login_alerts}
    multi_username_sources = {str(alert["source"]) for alert in multi_username_alerts}
    sources = sorted(repeated_sources | multi_username_sources)
    incidents: list[dict[str, Any]] = []

    for number, source in enumerate(sources, start=1):
        alert_types = []
        if source in repeated_sources:
            alert_types.append("repeated_failed_login")
        if source in multi_username_sources:
            alert_types.append("multiple_usernames")

        timeline = [
            {
                "timestamp": event["timestamp"],
                "description": (
                    f"{event['result']} login for {event['user']} from {source}"
                ),
            }
            for event in events
            if event["source"] == source
        ]
        risk = calculate_risk(alert_types)
        incidents.append(
            {
                "id": f"INC-{number:03d}",
                "source": source,
                "alert_types": alert_types,
                "timeline": timeline,
                "risk_score": risk["score"],
                "risk_level": risk["level"],
                "risk_explanation": risk["reasons"],
            }
        )

    if not bool(integrity_status["matches_baseline"]):
        risk = calculate_risk(["file_changed"])
        incidents.append(
            {
                "id": f"INC-{len(incidents) + 1:03d}",
                "source": "local practice file",
                "alert_types": ["file_changed"],
                "timeline": [
                    {
                        "timestamp": "local check",
                        "description": str(integrity_status["message"]),
                    }
                ],
                "risk_score": risk["score"],
                "risk_level": risk["level"],
                "risk_explanation": risk["reasons"],
            }
        )

    return incidents
