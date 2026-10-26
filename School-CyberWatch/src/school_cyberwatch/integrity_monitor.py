"""Local file-integrity checks for the project's harmless practice file."""

import hashlib
import json
from pathlib import Path


def fingerprint_file(file_path: Path) -> str:
    """Return a SHA-256 fingerprint for one local file.

    The file is opened only for reading. No network, account, device, or other
    folder is contacted.
    """
    digest = hashlib.sha256()
    with file_path.open("rb") as monitored_file:
        for block in iter(lambda: monitored_file.read(8192), b""):
            digest.update(block)
    return digest.hexdigest()


def create_baseline(file_path: Path, baseline_path: Path) -> dict[str, str]:
    """Save the current fingerprint of a local practice file as its baseline."""
    baseline = {
        "file_name": file_path.name,
        "sha256": fingerprint_file(file_path),
    }
    baseline_path.write_text(
        json.dumps(baseline, indent=2) + "\n", encoding="utf-8"
    )
    return baseline


def check_file_integrity(file_path: Path, baseline_path: Path) -> dict[str, str | bool]:
    """Compare the current local fingerprint with the saved baseline."""
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    current_fingerprint = fingerprint_file(file_path)
    matches_baseline = current_fingerprint == baseline["sha256"]
    return {
        "file_name": file_path.name,
        "matches_baseline": matches_baseline,
        "message": (
            "File matches the saved baseline."
            if matches_baseline
            else "File has changed since the saved baseline."
        ),
    }
