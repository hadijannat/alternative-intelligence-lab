"""Tampering/edge checks for the independent verification code."""
import copy
import json
import numpy as np
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from verify_results import (DIFFERENCES, PARAMETERS, STARTS, WORKSPACE, SOURCE_NAME, check_evaluation,
                            check_fit, check_inventories, check_mixing, check_score, check_trajectory,
                            challenge_rows, choose, close, compare, compare_refit, inventories,
                            scenarios, score, source_rows)
from model import Parameters, serial
from dataclasses import asdict


class VerifierTests(unittest.TestCase):
    def test_tolerance_never_accepts_nonfinite_or_changes_discrete_ids(self):
        DIFFERENCES.clear()
        close(1+1e-8, 1)
        close(2., 2., "Refit synthetic")
        self.assertEqual(DIFFERENCES["replay_and_independent_arithmetic"]["comparisons"], 1)
        self.assertAlmostEqual(DIFFERENCES["replay_and_independent_arithmetic"]["maximum_absolute_difference"], 1e-8)
        self.assertEqual(DIFFERENCES["fresh_refit"]["maximum_absolute_difference"], 0.)
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
        scores = [{"candidate": "release", "resolved": True, "rmse_pp": 2.},
                  {"candidate": "baseline", "resolved": True, "rmse_pp": 2.25},
                  {"candidate": "reversible_free", "resolved": False, "rmse_pp": .01}]
        self.assertEqual(choose(scores), "baseline")
        scores[1]["rmse_pp"] = 2.25001
        self.assertEqual(choose(scores), "release")
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

    def test_joint_challenge_excludes_high_doses_and_late_training(self):
        bulk = [r for r in source_rows(WORKSPACE/SOURCE_NAME) if r["dataset"].startswith("S13")]
        train, held = challenge_rows(bulk, "joint")
        self.assertEqual((len(train), len(held)), (12, 4))
        self.assertFalse({r["group_id"] for r in train} & {r["group_id"] for r in held})
        self.assertTrue(all(r["x"] in (15, 30) and r["seed_uM"] != 1 and r["hyper_a_uM"] != 2.5 for r in train))
        self.assertTrue(all(r["x"] in (45, 60) and (r["seed_uM"] == 1 or r["hyper_a_uM"] == 2.5) for r in held))
        with self.assertRaises(AssertionError):
            challenge_rows(bulk[:-1], "joint")

    def test_scenario_matrix_does_not_select_transport_winner(self):
        base = scenarios("baseline")
        self.assertEqual(len(base), 16)
        extra = scenarios("reversible_free")
        self.assertEqual(len(extra), 20)
        self.assertEqual({r["candidate"] for r in extra.values() if r["complex_reset"]}, {"reversible_free"})
        self.assertEqual(set(base), {k for k, v in extra.items() if not v["complex_reset"]})
        self.assertEqual(len(scenarios(None)), 16)

    def test_bound_reporter_and_competence_are_distinct(self):
        state = np.zeros(12)
        state[[3, 4, 6, 7, 8, 10, 11]] = [1, 2, 3, 5, 7, 11, 13]
        competent, product = inventories(state)
        self.assertEqual(competent, 19)
        self.assertEqual(product, 44)
        with self.assertRaises(AssertionError):
            check_inventories([{"F_uM": "-1"}], [{"F_uM": -1.}])
        with self.assertRaises(AssertionError):
            check_inventories([], [{"F_uM": 0.}])

    def test_serial_arithmetic_detects_founder_subtraction_from_free_only(self):
        p = Parameters(turnover=True, krel=.1, kbind=.2, kd=.01)
        rows = serial(p, 2)
        check_trajectory(rows, p, 2)
        tampered = copy.deepcopy(rows)
        tampered[1]["newly_generated_competent_model_uM"] = max(0, tampered[1]["F_uM"]-tampered[1]["founder_competent_model_uM"])
        with self.assertRaises(AssertionError):
            check_trajectory(tampered, p, 2)

    def test_every_start_objective_and_residual_receipt_are_checked(self):
        names = PARAMETERS["baseline"]
        training = [{"row_id": "a", "group_id": "g", "x": 15, "value_percent": 0.}]
        starts = [{"start_id": i+1, "log10_start": [float(t[n]) for n in names],
                   "log10_parameters": [float(t[n]) for n in names], "success": False,
                   "status": 0, "sse": 1., "nfev": 160, "njev": 1, "message": "budget exhausted",
                   "active_bounds": [0]*len(names), "elapsed_seconds": .1, "residual_evaluations": 160}
                  for i, t in enumerate(STARTS)]
        detail = {"candidate": "baseline", "training_row_ids": ["a"], "training_groups": ["g"],
                  "fixed_parameters": {}, "free_parameters": list(names), "complete": True,
                  "max_nfev": 160, "n_observations": 1, "starts": starts, "resolved": False,
                  "residual_evaluations": 960}
        with patch("verify_results.prediction", return_value=[1.]):
            self.assertFalse(check_fit(detail, "baseline", training))
            detail["starts"][3]["sse"] = 2.
            with self.assertRaises(AssertionError):
                check_fit(detail, "baseline", training)
            detail["starts"][3]["sse"] = 1.
            detail["residual_evaluations"] = 959
            with self.assertRaises(AssertionError):
                check_fit(detail, "baseline", training)

    def test_mixing_cannot_change_chemistry_and_failed_receipt_must_replay(self):
        p = Parameters()
        training = [{"row_id": str(i), "seed_uM": i%2, "x": i%3+1, "value_percent": 0.} for i in range(18)]
        detail = {"complete": True, "resolved": True, "success": True, "nfev": 1,
                  "training_row_ids": [r["row_id"] for r in training], "fitted_parameters": ["mixing"],
                  "bounds": [0, 1], "frozen_chemistry_parameters": asdict(p), "n": 18,
                  "mixing": .2, "sse": 18., "rmse_pp": 1.,
                  "evaluations": [{"mixing": .2, "sse": 18., "resolved": True}]}
        with patch("verify_results.single_cycle", return_value=1.):
            check_mixing(detail, p, training)
            detail["frozen_chemistry_parameters"]["kd"] = .1
            with self.assertRaises(AssertionError):
                check_mixing(detail, p, training)
            detail["frozen_chemistry_parameters"] = asdict(p)
            detail["evaluations"][0] = {"mixing": .2, "resolved": False, "error": "ArithmeticError: synthetic"}
            with self.assertRaises(AssertionError):
                check_mixing(detail, p, training)

    def test_refit_rejects_numeric_looking_identifier_and_missing_negative_scenario(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory)/"a", Path(directory)/"b"
            for path in (a, b):
                path.mkdir()
                (path/"freeze.json").write_text(json.dumps({"files": {"source": "hash"}}))
                (path/"transport.json").write_text(json.dumps({"baseline|contact|uniform|reset-0": {"resolved": False}}))
                (path/"values.csv").write_text("row_id,predicted_percent\n1,2.0\n")
            self.assertEqual(compare_refit(a, b), 2)
            (b/"values.csv").write_text("row_id,predicted_percent\n1.0,2.0\n")
            with self.assertRaises(AssertionError):
                compare_refit(a, b)
            (b/"values.csv").write_text("row_id,predicted_percent\n1,2.0\n")
            (b/"transport.json").write_text("{}")
            with self.assertRaises(AssertionError):
                compare_refit(a, b)


if __name__ == "__main__":
    unittest.main()
