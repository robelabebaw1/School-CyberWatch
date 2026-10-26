import unittest
from pathlib import Path

from school_cyberwatch.sample_data import load_sample_events


class SampleDataTests(unittest.TestCase):
    def test_authorized_sample_log_loads(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        events = load_sample_events(
            project_root / "data" / "sample_logs" / "auth_events.jsonl"
        )

        self.assertEqual(len(events), 5)
        self.assertEqual(events[0]["user"], "amina")
        self.assertTrue(all("password" not in event for event in events))
