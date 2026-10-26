"""Self-contained fictional scenarios for demonstrating School CyberWatch."""

import json
import tempfile
from pathlib import Path
from typing import Any

from .incidents import build_incidents
from .integrity_monitor import check_file_integrity, create_baseline
from .login_detection import find_suspicious_logins
from .presentation import export_report, render_dashboard
from .source_activity_detection import find_sources_targeting_multiple_users


def run_demo() -> dict[str, Any]:
    """Run only temporary fictional scenarios and return their results.

    The temporary log data, monitored file, baseline, and report are deleted
    automatically when this function finishes. Nothing outside the temporary
    folder is inspected or changed.
    """
    events = [
        {
            "timestamp": "2026-10-25T09:00:00Z",
            "user": "dina",
            "source": "demo-pc-01",
            "result": "failed",
        },
        {
            "timestamp": "2026-10-25T09:01:00Z",
            "user": "dina",
            "source": "demo-pc-01",
            "result": "failed",
        },
        {
            "timestamp": "2026-10-25T09:02:00Z",
            "user": "dina",
            "source": "demo-pc-01",
            "result": "failed",
        },
        {
            "timestamp": "2026-10-25T09:03:00Z",
            "user": "eli",
            "source": "demo-pc-01",
            "result": "failed",
        },
    ]
    repeated_alerts = find_suspicious_logins(events)
    multi_username_alerts = find_sources_targeting_multiple_users(events)

    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        practice_file = folder / "fictional_practice_file.txt"
        baseline_file = folder / "fictional_baseline.json"
        report_file = folder / "fictional_demo_report.json"
        practice_file.write_text("original fictional text", encoding="utf-8")
        create_baseline(practice_file, baseline_file)
        practice_file.write_text("changed fictional text", encoding="utf-8")
        integrity_status = check_file_integrity(practice_file, baseline_file)

        incidents = build_incidents(
            events, repeated_alerts, multi_username_alerts, integrity_status
        )
        export_report(incidents, report_file)
        report = json.loads(report_file.read_text(encoding="utf-8"))

    return {
        "repeated_alerts": repeated_alerts,
        "multi_username_alerts": multi_username_alerts,
        "integrity_status": integrity_status,
        "incidents": incidents,
        "report": report,
    }


def render_demo() -> str:
    """Create the terminal text for the safe, local evaluation demonstration."""
    demo = run_demo()
    lines = [
        "School CyberWatch - Safe Demo/Evaluation Mode",
        "=" * 47,
        "Scenario 1 - Repeated failed logins:",
        f"  Alerts found: {len(demo['repeated_alerts'])}",
        "Scenario 2 - One source targeting multiple usernames:",
        f"  Alerts found: {len(demo['multi_username_alerts'])}",
        "Scenario 3 - File integrity change:",
        f"  {demo['integrity_status']['message']}",
        "",
        render_dashboard(demo["incidents"]),
        "",
        "Fictional local report preview:",
        json.dumps(demo["report"], indent=2),
        "",
        "The temporary fictional files and report were removed after this demo.",
    ]
    return "\n".join(lines)
