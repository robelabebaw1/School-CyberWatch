import tempfile
import unittest
from pathlib import Path

from school_cyberwatch.integrity_monitor import (
    check_file_integrity,
    create_baseline,
)


class FileIntegrityMonitorTests(unittest.TestCase):
    def test_unchanged_file_matches_its_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            monitored_file = folder / "practice_file.txt"
            baseline_file = folder / "baseline.json"
            monitored_file.write_text("fictional practice data", encoding="utf-8")

            create_baseline(monitored_file, baseline_file)
            status = check_file_integrity(monitored_file, baseline_file)

            self.assertTrue(status["matches_baseline"])

    def test_changed_file_does_not_match_its_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            monitored_file = folder / "practice_file.txt"
            baseline_file = folder / "baseline.json"
            monitored_file.write_text("original fictional data", encoding="utf-8")
            create_baseline(monitored_file, baseline_file)
            monitored_file.write_text("changed fictional data", encoding="utf-8")

            status = check_file_integrity(monitored_file, baseline_file)

            self.assertFalse(status["matches_baseline"])
            self.assertEqual(status["message"], "File has changed since the saved baseline.")
