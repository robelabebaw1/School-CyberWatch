import unittest

from school_cyberwatch.incidents import build_incidents, calculate_risk


class IncidentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.events = [
            {
                "timestamp": "2026-10-17T08:20:00Z",
                "user": "brian",
                "source": "lab-pc-02",
                "result": "failed",
            },
            {
                "timestamp": "2026-10-17T08:23:00Z",
                "user": "chloe",
                "source": "lab-pc-02",
                "result": "failed",
            },
        ]

    def test_related_source_alerts_become_one_high_risk_incident(self) -> None:
        incidents = build_incidents(
            self.events,
            [{"source": "lab-pc-02", "user": "brian", "failed_attempts": 3}],
            [{"source": "lab-pc-02", "targeted_usernames": 2}],
            {"matches_baseline": True, "message": "File matches the saved baseline."},
        )

        self.assertEqual(len(incidents), 1)
        self.assertEqual(incidents[0]["risk_score"], 80)
        self.assertEqual(incidents[0]["risk_level"], "High")
        self.assertEqual(len(incidents[0]["timeline"]), 2)

    def test_changed_practice_file_becomes_a_low_risk_incident(self) -> None:
        incidents = build_incidents(
            [], [], [], {"matches_baseline": False, "message": "File has changed."}
        )

        self.assertEqual(incidents[0]["risk_score"], 20)
        self.assertEqual(incidents[0]["risk_level"], "Low")

    def test_risk_calculation_is_explainable(self) -> None:
        risk = calculate_risk(["repeated_failed_login"])

        self.assertEqual(risk["score"], 45)
        self.assertEqual(risk["reasons"], ["repeated failed login (+45)"])
