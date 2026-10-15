import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pilot import monitored_run


class SupervisorChecks(unittest.TestCase):
    def run_child(self, code, seconds, memory):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            result = monitored_run([sys.executable, "-c", code], path, seconds, memory)
            self.assertEqual(json.loads((path / "supervisor.json").read_text()), result)
            self.assertTrue((path / "stdout.txt").exists())
            self.assertTrue((path / "stderr.txt").exists())
            return result

    def test_normal_child_finishes(self):
        result = self.run_child("print('reference child')", 5, 2**30)
        self.assertEqual(result["returncode"], 0)
        self.assertIsNone(result["termination_reason"])

    def test_timeout_terminates_owned_child(self):
        result = self.run_child("import time; time.sleep(30)", 0.3, 2**30)
        self.assertEqual(result["termination_reason"], "WALL_LIMIT")
        self.assertNotEqual(result["returncode"], 0)
        self.assertLess(result["wall_seconds"], 6)

    def test_observed_rss_terminates_owned_child(self):
        result = self.run_child("import time; time.sleep(30)", 5, 1)
        self.assertEqual(result["termination_reason"], "RSS_LIMIT")
        self.assertGreater(result["sampled_max_rss_bytes"], 1)
        self.assertNotEqual(result["returncode"], 0)

    def test_monitor_failure_terminates_child_and_records_result(self):
        for error in (subprocess.TimeoutExpired(["ps"], 3), OSError("ps unavailable")):
            with self.subTest(error=type(error).__name__), patch("pilot.subprocess.run", side_effect=error):
                result = self.run_child("import time; time.sleep(30)", 5, 2**30)
                self.assertEqual(result["termination_reason"], "RSS_MONITOR_UNAVAILABLE")
                self.assertEqual(result["monitor_error"], f"{type(error).__name__}: {error}")
                self.assertNotEqual(result["returncode"], 0)
                self.assertLess(result["wall_seconds"], 6)


if __name__ == "__main__":
    unittest.main()
