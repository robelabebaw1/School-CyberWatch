import unittest

from school_cyberwatch.demo import render_demo, run_demo


class DemoModeTests(unittest.TestCase):
    def test_demo_runs_all_fictional_detection_scenarios(self) -> None:
        demo = run_demo()

        self.assertEqual(len(demo["repeated_alerts"]), 1)
        self.assertEqual(len(demo["multi_username_alerts"]), 1)
        self.assertFalse(demo["integrity_status"]["matches_baseline"])
        self.assertEqual(demo["report"]["incident_count"], 2)

    def test_demo_output_contains_dashboard_and_report_preview(self) -> None:
        output = render_demo()

        self.assertIn("Scenario 1 - Repeated failed logins:", output)
        self.assertIn("Scenario 2 - One source targeting multiple usernames:", output)
        self.assertIn("Scenario 3 - File integrity change:", output)
        self.assertIn("School CyberWatch - Local Incident Dashboard", output)
        self.assertIn("Fictional local report preview:", output)
