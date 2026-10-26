# School CyberWatch

## Overview

School CyberWatch is a small Python learning prototype for defensive security
monitoring. It reads only the fictional data included in this repository and
turns simple alerts into an easy-to-read incident timeline and risk score.

The project is designed for demonstration and coursework. It does not connect
to networks, access real accounts, scan devices, or take automatic action.

## Features

- Detects repeated failed logins for the same fictional user and source.
- Detects one fictional source making failed attempts for multiple usernames.
- Checks whether the included harmless practice file has changed from its
  saved SHA-256 baseline fingerprint.
- Correlates related alerts into a timeline-based incident.
- Calculates a transparent, rule-based risk score:
  - repeated failed login: 45 points;
  - multiple usernames from one source: 35 points;
  - changed practice file: 20 points.
- Displays a readable terminal dashboard.
- Exports the current local incidents as a JSON report.
- Includes a safe Demo/Evaluation Mode and automated tests.

## Project Structure

```text
School CyberWatch/
├── data/
│   ├── file_integrity_baseline.json      # Saved fingerprint for the practice file
│   ├── monitored_files/
│   │   └── student_records_demo.txt      # Harmless fictional file to monitor
│   └── sample_logs/
│       └── auth_events.jsonl             # Fictional login events
├── reports/
│   └── incident_report.json              # Example exported report
├── src/school_cyberwatch/
│   ├── __main__.py                       # Command-line entry point
│   ├── demo.py                           # Safe temporary demo scenarios
│   ├── incidents.py                      # Incident correlation and risk scoring
│   ├── integrity_monitor.py              # File fingerprint and comparison tools
│   ├── login_detection.py                # Repeated-login detection rule
│   ├── presentation.py                   # Dashboard and JSON report export
│   ├── sample_data.py                    # Reads fictional sample logs
│   └── source_activity_detection.py      # Multiple-username detection rule
├── tests/                                # Automated tests
├── requirements.txt                      # No external packages are required
└── README.md
```

## Run Instructions

### Requirements

Install Python 3.14 or a compatible recent Python version. This project uses
only the Python standard library, so no package installation is needed.

Open PowerShell in the project folder and run this once per PowerShell window:

```powershell
$env:PYTHONPATH = "src"
```

Run the normal local incident dashboard:

```powershell
python -m school_cyberwatch
```

The included fictional sample data produces one High-risk incident for
`lab-pc-02`, with a score of 80/100.

Check the included harmless practice file against its saved baseline:

```powershell
python -m school_cyberwatch check
```

Create a new baseline only after you intentionally change the included
practice file:

```powershell
python -m school_cyberwatch baseline
```

Export the current local incidents to `reports/incident_report.json`:

```powershell
python -m school_cyberwatch report
```

## Tests

Run all automated tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

The current suite contains 14 tests. A successful run ends with `OK`.

## Demo/Evaluation Mode

Run the full safe demonstration:

```powershell
$env:PYTHONPATH = "src"
python -m school_cyberwatch demo
```

The demo uses a temporary fictional log and a temporary fictional practice
file. It shows all core behaviors:

1. Repeated failed-login detection.
2. Failed attempts for multiple usernames from one source.
3. A detected change to a fictional practice file.
4. The correlated timeline and explainable risk scores.
5. A JSON incident-report preview.

The temporary fictional files and report are removed when the demo ends.

## Safety and Limitations

- All bundled logs, usernames, computer names, and files are fictional.
- The prototype makes no network connections and does not monitor real
  accounts, folders, devices, or systems.
- It does not scan, block, modify, or respond to any external target.
- A risk score or alert is a prompt for review in this demonstration; it is
  not evidence of malicious activity.
- The rules use fixed thresholds and are intentionally simple.
- The terminal dashboard and JSON export are basic local outputs, not a
  full security operations platform.

## Future Improvements

- Let a user choose clearly documented thresholds through configuration.
- Add more fictional evaluation scenarios and measure false-positive results.
- Add a simple local HTML view for the already-generated incident data.
- Add CSV export alongside the existing JSON report.
- Improve input validation and error messages for missing local sample files.
