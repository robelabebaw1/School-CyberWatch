"""Simple, local rules for spotting suspicious login patterns in sample logs."""

from collections import Counter


FAILED_LOGIN_THRESHOLD = 3


def find_suspicious_logins(
    events: list[dict[str, str]], threshold: int = FAILED_LOGIN_THRESHOLD
) -> list[dict[str, str | int]]:
    """Return an alert for each user/source pair with repeated failed logins.

    This function only examines log entries already supplied by the caller. It
    does not contact accounts, devices, networks, or external services.
    """
    failed_pairs = Counter(
        (event["user"], event["source"])
        for event in events
        if event.get("result") == "failed"
    )

    alerts = [
        {
            "user": user,
            "source": source,
            "failed_attempts": attempts,
            "reason": f"{attempts} failed login attempts from the same source",
        }
        for (user, source), attempts in failed_pairs.items()
        if attempts >= threshold
    ]
    return sorted(alerts, key=lambda alert: str(alert["user"]))
