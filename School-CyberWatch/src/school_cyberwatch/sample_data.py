"""Helpers for reading the project's authorized, fictional sample logs."""

import json
from pathlib import Path


def load_sample_events(log_path: Path) -> list[dict[str, str]]:
    """Read one JSON object per line from a local sample log file.

    This helper accepts only a path supplied by the local project. It does not
    contact computers, networks, accounts, or external services.
    """
    with log_path.open(encoding="utf-8") as log_file:
        return [json.loads(line) for line in log_file if line.strip()]
