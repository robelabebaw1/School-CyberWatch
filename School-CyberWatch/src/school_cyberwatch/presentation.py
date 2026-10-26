"""Readable local dashboard and JSON report export for fictional incidents."""

import json
from pathlib import Path
from typing import Any


def render_dashboard(incidents: list[dict[str, Any]]) -> str:
    """Create a compact text dashboard suitable for a local terminal."""
    lines = ["School CyberWatch - Local Incident Dashboard", "=" * 47]
    if not incidents:
        lines.append("No incidents were found in the fictional local data.")
        return "\n".join(lines)

    for incident in incidents:
        lines.extend(
            [
                f"{incident['id']} | {incident['risk_level']} risk "
                f"({incident['risk_score']}/100)",
                f"Source: {incident['source']}",
                "Why: " + "; ".join(incident["risk_explanation"]),
                "Timeline:",
            ]
        )
        lines.extend(
            f"  - {entry['timestamp']}: {entry['description']}"
            for entry in incident["timeline"]
        )
        lines.append("-" * 47)
    return "\n".join(lines)


def export_report(incidents: list[dict[str, Any]], report_path: Path) -> None:
    """Write the current fictional incidents as an easy-to-read JSON report."""
    report = {
        "title": "School CyberWatch Local Incident Report",
        "scope": "Fictional local sample data only",
        "incident_count": len(incidents),
        "incidents": incidents,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
