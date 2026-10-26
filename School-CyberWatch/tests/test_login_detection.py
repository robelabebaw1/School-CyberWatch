import unittest
from pathlib import Path

from school_cyberwatch.login_detection import find_suspicious_logins
from school_cyberwatch.sample_data import load_sample_events


class SuspiciousLoginDetectionTests(unittest.TestCase):
    def test_repeated_failed_logins_create_an_alert(self) -> None:
        events = load_sample_events(
            Path("data/sample_logs/auth_events.jsonl")
        )

        alerts = find_suspicious_logins(events)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["user"], "brian")
        self.assertEqual(alerts[0]["source"], "lab-pc-02")
        self.assertEqual(alerts[0]["failed_attempts"], 3)

    def test_fewer_failures_than_the_threshold_do_not_create_an_alert(self) -> None:
        events = [
            {"user": "amina", "source": "lab-pc-01", "result": "failed"},
            {"user": "amina", "source": "lab-pc-01", "result": "failed"},
            {"user": "amina", "source": "lab-pc-01", "result": "success"},
        ]

        self.assertEqual(find_suspicious_logins(events), [])
