"""Tampering/edge checks for the independent verification code."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from verify_results import check_evaluation, check_score, choose, close, compare, compare_refit, score


class VerifierTests(unittest.TestCase):
    def test_tolerance_never_accepts_nonfinite_or_changes_discrete_ids(self):
        close(1+1e-8, 1)
        for value in (float("nan"), float("inf"), 1.001):
            with self.assertRaises(AssertionError):
                close(value, 1)
        with self.assertRaises(AssertionError):
            compare({"start_id": 1.0}, {"start_id": 1})
        with self.assertRaises(AssertionError):
            compare({"resolved": 1}, {"resolved": True})

    def test_score_excludes_time_zero_and_preserves_high_residual(self):
        rows = [{"x": 0, "error_pp": 0}, {"x": 15, "error_pp": 3}, {"x": 30, "error_pp": 4}]
        result = score(rows)
        self.assertEqual(result["n_positive"], 2)
        self.assertAlmostEqual(result["rmse_pp"], (12.5)**.5)
        self.assertFalse(result["adequate"])
        rows.append({"x": 60, "error_pp": float("nan")})
        with self.assertRaises(AssertionError):
            score(rows)

    def test_selection_excludes_unresolved_and_applies_simplicity(self):
        scores = [{"candidate": "independent", "resolved": True, "rmse_pp": 2.},
                  {"candidate": "revised", "resolved": True, "rmse_pp": 2.25},
                  {"candidate": "inactivation", "resolved": False, "rmse_pp": .01}]
        self.assertEqual(choose(scores), "revised")
        scores[1]["rmse_pp"] = 2.25001
        self.assertEqual(choose(scores), "independent")
        self.assertIsNone(choose([]))

    def test_refit_allows_clock_change_but_rejects_missing_failed_start(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory)/"a", Path(directory)/"b"
            for i, path in enumerate((first, second)):
                path.mkdir()
                (path/"freeze.json").write_text(json.dumps({"utc_before_fit": str(i), "files": {"data": "hash"}}))
                (path/"fit.json").write_text(json.dumps({"elapsed_seconds": i, "starts": [{"success": False, "sse": None}]}))
                (path/"values.csv").write_text("row_id,predicted_percent\na,1.0\n")
            self.assertEqual(compare_refit(first, second), 2)
            (second/"fit.json").write_text(json.dumps({"elapsed_seconds": 2, "starts": []}))
            with self.assertRaises(AssertionError):
                compare_refit(first, second)

    def test_transport_screen_uses_group_means_and_all_replicates(self):
        rows = [{"dataset": "Figure_2", "seed_uM": 2, "x": 1, "error_pp": e} for e in (-3., 0., 3.)]
        result = score(rows, transport=True)
        self.assertEqual(result["maximum_absolute_group_mean_error_pp"], 0)
        self.assertFalse(result["adequate"])

    def test_threshold_pass_cannot_override_failed_numerical_gate(self):
        rows = [{"x": 15, "error_pp": 1.}]
        saved = {**score(rows), "threshold_screen_pass": True, "numerical_eligible": False, "adequate": False}
        check_score(saved, rows, "synthetic gate")
        saved["adequate"] = True
        with self.assertRaises(AssertionError):
            check_score(saved, rows, "synthetic gate")

    def test_held_prediction_failure_is_preserved_and_must_reproduce(self):
        detail = {"resolved": True, "parameters": {}}
        failure = {"resolved": False, "error": "Prediction failed: synthetic integration error"}
        with patch("verify_results.prediction", side_effect=ArithmeticError("synthetic integration error")):
            check_evaluation(detail, failure, [])
        with patch("verify_results.prediction", return_value=[]):
            with self.assertRaises(AssertionError):
                check_evaluation(detail, failure, [])
        with self.assertRaises(AssertionError):
            check_evaluation({"resolved": False}, {"resolved": True}, [])


if __name__ == "__main__":
    unittest.main()
