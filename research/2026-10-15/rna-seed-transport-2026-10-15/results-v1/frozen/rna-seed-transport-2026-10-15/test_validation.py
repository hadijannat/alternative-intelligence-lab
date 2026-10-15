"""Checks protect the frozen split, fit failures, and informative error screens."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from run import (BOUNDS, STARTS, calibration_predictions, contrasts, decode, fit,
                 load, metrics, scenarios, scenario_name, split)


class ValidationTests(unittest.TestCase):
    def test_disjoint_18_72_split_and_held_labels_cannot_change_training(self):
        rows = load()
        train, held = split(rows)
        self.assertEqual((len(train), len(held)), (18, 72))
        self.assertFalse({r["row_id"] for r in train} & {r["row_id"] for r in held})
        self.assertTrue(all(r["x"] > 0 for r in train + held))
        changed = deepcopy(rows)
        train_ids = {r["row_id"] for r in train}
        for row in changed:
            if row["row_id"] not in train_ids:
                row["value_percent"] = -1e9
        self.assertEqual(split(changed)[0], train)
        with self.assertRaises(ValueError):
            split([r for r in rows if r["row_id"] != train[0]["row_id"]])

    def test_condition_mean_maximum_and_replicate_rmse_are_distinct(self):
        rows = [{"dataset": "Figure_2", "seed_uM": 2, "x": 1, "error_pp": e} for e in (-3, 0, 3)]
        result = metrics(rows)
        self.assertAlmostEqual(result["rmse_pp"], np.sqrt(6))
        self.assertEqual(result["max_absolute_condition_mean_error_pp"], 0)
        self.assertEqual(result["max_absolute_replicate_error_pp"], 3)
        self.assertFalse(result["adequate"])
        for r in rows:
            r["error_pp"] = 1
        self.assertTrue(metrics(rows)["adequate"])
        self.assertFalse(metrics(rows, qualified=False)["adequate"])
        self.assertFalse(metrics([])["resolved"])
        rows[0]["error_pp"] = np.nan
        with self.assertRaises(ValueError):
            metrics(rows)

    def test_parameter_scales_and_fixed_profile_are_preserved(self):
        self.assertEqual(decode("legacy", [.2]), {"mixing": .2})
        self.assertEqual(decode("bath", [1]), {"nu": 10})
        self.assertEqual(decode("patch", [-1], {"nu": 4}), {"nu": 4, "diffusion": .1})
        self.assertEqual(len(STARTS), 6)
        self.assertEqual(BOUNDS["mixing"], (0, 1))

    def test_all_nine_scenarios_are_predeclared(self):
        values = list(scenarios())
        self.assertEqual(len(values), 9)
        self.assertEqual(len({scenario_name(*s) for s in values}), 9)
        self.assertEqual(sum(s[0] == "legacy" for s in values), 1)
        self.assertEqual(sum(s[0] == "bath" for s in values), 4)

    def test_failed_starts_retained_without_retry_or_false_success(self):
        rows = [{"row_id": "synthetic", "seed_uM": 0, "x": 1, "value_percent": 0}]
        with tempfile.TemporaryDirectory() as directory, patch("run.least_squares", side_effect=ArithmeticError("synthetic failure")) as optimizer:
            path = Path(directory)/"fit.json"
            result = fit("bath", rows, path)
            self.assertEqual(optimizer.call_count, 6)
            self.assertEqual(json.loads(path.read_text()), result)
        self.assertFalse(result["resolved"])
        self.assertFalse(result["qualified"])
        self.assertTrue(result["complete"])
        self.assertEqual(len(result["starts"]), 6)
        self.assertTrue(all("synthetic failure" in r["message"] for r in result["starts"]))

    def test_exhausted_start_scores_remain_recorded_but_unresolved(self):
        rows = [{"row_id": "synthetic", "seed_uM": 0, "x": 1, "value_percent": 0}]
        capped = SimpleNamespace(success=False, status=0, nfev=120, njev=110,
                                 fun=np.array([.1]), x=np.array([.5]), active_mask=np.array([0]), message="budget exhausted")
        with tempfile.TemporaryDirectory() as directory, patch("run.least_squares", return_value=capped):
            result = fit("bath", rows, Path(directory)/"fit.json")
        self.assertFalse(result["resolved"])
        self.assertTrue(all(r["nfev"] == 120 and r["sse"] > 0 for r in result["starts"]))

    def test_single_success_does_not_qualify_multistart_fit(self):
        rows = [{"row_id": "synthetic", "seed_uM": 0, "x": 1, "value_percent": 0}]
        success = SimpleNamespace(success=True, status=1, nfev=1, njev=1, jac=np.array([[1.]]),
                                  fun=np.array([.1]), x=np.array([.5]), active_mask=np.array([0]), message="success")
        with tempfile.TemporaryDirectory() as directory, patch("run.least_squares", side_effect=[success] + [ArithmeticError("failure")]*5):
            result = fit("bath", rows, Path(directory)/"fit.json")
        self.assertTrue(result["resolved"])
        self.assertFalse(result["qualified"])
        self.assertEqual(result["successful_starts"], 1)

    def test_direct_bath_profile_is_objective_only_and_failure_is_retained(self):
        rows = [{"row_id": "synthetic", "seed_uM": 0, "x": 1, "value_percent": 2}]
        with tempfile.TemporaryDirectory() as directory, patch("run.single_cycle", return_value={"yield_percent": 3}), patch("run.least_squares") as optimizer:
            result = fit("bath", rows, Path(directory)/"profile.json", {"nu": 4})
        self.assertEqual(optimizer.call_count, 0)
        self.assertEqual(result["sse"], 1)
        self.assertEqual(result["starts"], [])
        with tempfile.TemporaryDirectory() as directory, patch("run.single_cycle", side_effect=ArithmeticError("profile failure")):
            result = fit("bath", rows, Path(directory)/"profile.json", {"nu": 4})
        self.assertFalse(result["resolved"])
        self.assertIn("profile failure", result["error"])

    def test_predictions_deduplicate_replicates_and_reject_nonfinite_values(self):
        rows = [{"seed_uM": 0, "x": 1}, {"seed_uM": 0, "x": 1}, {"seed_uM": 1, "x": 2}]
        with patch("run.single_cycle", return_value={"yield_percent": 3}) as model:
            self.assertEqual(calibration_predictions("bath", {"nu": 4}, rows).tolist(), [3, 3, 3])
            self.assertEqual(model.call_count, 2)
        with patch("run.single_cycle", return_value={"yield_percent": np.nan}):
            with self.assertRaises(ArithmeticError):
                calibration_predictions("bath", {"nu": 4}, rows)

    def test_seed_contrasts_include_new_production_and_active_inventory(self):
        rows = [{"generation": g, "seed_uM": s, "stage": "warm", "yield_percent": s,
                 "new_reporter_inside_uM": s*.1, "competent_inside_uM": s*.01}
                for g in range(8) for s in (0, 1, 2)]
        result = contrasts(rows)
        self.assertEqual(len(result), 16)
        self.assertEqual(result[1]["contrast"], "2-0")
        self.assertEqual(result[1]["new_reporter_inside_uM"], .2)
        self.assertEqual(result[1]["competent_inside_uM"], .02)


if __name__ == "__main__":
    unittest.main()
