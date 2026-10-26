import json
import tempfile
import unittest
from pathlib import Path

from school_cyberwatch.presentation import export_report, render_dashboard


class PresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.incidents = [
            {
                "id": "INC-001",
                "source": "lab-pc-02",
                "risk_score": 80,
                "risk_level": "High",
                "risk_explanation": ["repeated failed login (+45)"],
                "timeline": [
                    {"timestamp": "2026-10-17T08:20:00Z", "description": "failed"}
                ],
            }
        ]

    def test_dashboard_displays_incident_and_timeline(self) -> None:
        dashboard = render_dashboard(self.incidents)

        self.assertIn("INC-001 | High risk (80/100)", dashboard)
        self.assertIn("Timeline:", dashboard)

    def test_report_export_writes_local_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "report.json"

            export_report(self.incidents, report_path)

            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["incident_count"], 1)
            self.assertEqual(report["incidents"][0]["id"], "INC-001")
