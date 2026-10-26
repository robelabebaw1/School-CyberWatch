import unittest
from pathlib import Path

from school_cyberwatch.sample_data import load_sample_events
from school_cyberwatch.source_activity_detection import (
    find_sources_targeting_multiple_users,
)


class SourceActivityDetectionTests(unittest.TestCase):
    def test_one_source_failing_for_multiple_users_creates_an_alert(self) -> None:
        events = load_sample_events(Path("data/sample_logs/auth_events.jsonl"))

        alerts = find_sources_targeting_multiple_users(events)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["source"], "lab-pc-02")
        self.assertEqual(alerts[0]["targeted_usernames"], 2)

    def test_one_source_failing_for_one_user_does_not_create_an_alert(self) -> None:
        events = [
            {"user": "amina", "source": "lab-pc-01", "result": "failed"},
            {"user": "amina", "source": "lab-pc-01", "result": "failed"},
            {"user": "amina", "source": "lab-pc-01", "result": "failed"},
        ]

        self.assertEqual(find_sources_targeting_multiple_users(events), [])
