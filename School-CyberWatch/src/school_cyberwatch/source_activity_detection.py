"""Safe local rules for unusual activity from one source in sample login data."""

from collections import defaultdict


DISTINCT_USERNAME_THRESHOLD = 2


def find_sources_targeting_multiple_users(
    events: list[dict[str, str]], threshold: int = DISTINCT_USERNAME_THRESHOLD
) -> list[dict[str, str | int]]:
    """Flag sources with failed logins for several different usernames.

    This is separate from the repeated-failed-login rule. It reads only the
    event records given to it and never contacts accounts, networks, or devices.
    """
    failed_users_by_source: defaultdict[str, set[str]] = defaultdict(set)
    for event in events:
        if event.get("result") == "failed":
            failed_users_by_source[event["source"]].add(event["user"])

    alerts = [
        {
            "source": source,
            "targeted_usernames": len(usernames),
            "reason": (
                f"failed login attempts for {len(usernames)} different usernames"
            ),
        }
        for source, usernames in failed_users_by_source.items()
        if len(usernames) >= threshold
    ]
    return sorted(alerts, key=lambda alert: str(alert["source"]))
