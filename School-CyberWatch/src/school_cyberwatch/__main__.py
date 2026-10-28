"""Run School-CyberWatch operations from the command line."""

import argparse
from pathlib import Path

from .demo import render_demo
from .integrity_monitor import check_file_integrity, create_baseline
from .incidents import build_incidents
from .login_detection import find_suspicious_logins
from .presentation import export_report, render_dashboard
from .sample_data import load_sample_events
from .source_activity_detection import find_sources_targeting_multiple_users


def main() -> None:
    """Show that the fictional local sample data can be read safely."""
    parser = argparse.ArgumentParser(description="Safe local School CyberWatch demo")
    parser.add_argument(
        "action",
        nargs="?",
        choices=("baseline", "check", "report", "demo"),
        help="create/check the baseline, export a report, or run safe demo scenarios",
    )
    arguments = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    log_path = project_root / "data" / "sample_logs" / "auth_events.jsonl"
    monitored_file = (
        project_root / "data" / "monitored_files" / "student_records_demo.txt"
    )
    baseline_file = project_root / "data" / "file_integrity_baseline.json"

    if arguments.action == "baseline":
        create_baseline(monitored_file, baseline_file)
        print(f"Saved a baseline fingerprint for: {monitored_file.name}")
        return

    if arguments.action == "demo":
        print(render_demo())
        return

    integrity_status = check_file_integrity(monitored_file, baseline_file)
    if arguments.action == "check":
        print(
            f"Integrity check for {integrity_status['file_name']}: "
            f"{integrity_status['message']}"
        )
        return

    events = load_sample_events(log_path)
    alerts = find_suspicious_logins(events)
    source_alerts = find_sources_targeting_multiple_users(events)
    incidents = build_incidents(events, alerts, source_alerts, integrity_status)

    if arguments.action == "report":
        report_path = project_root / "reports" / "incident_report.json"
        export_report(incidents, report_path)
        print(f"Exported local incident report to: {report_path}")
        return

    print(render_dashboard(incidents))
    print("No network connection or live-system monitoring was used.")


if __name__ == "__main__":
    main()
