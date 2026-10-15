"""Validation checks protect informative denominators, group splits and failure propagation."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from run import (PARAMETERS, STARTS, START_NAMES, aggregate, assert_split, decode, evaluate, fit, groups,
                 load, metrics, select_family, split_record)


class ValidationTests(unittest.TestCase):
    def test_positive_time_denominator_excludes_known_zero(self):
        result = metrics([{"x": 0, "error_pp": 0}, {"x": 15, "error_pp": 3}, {"x": 30, "error_pp": 4}])
        self.assertEqual(result["n_positive"], 2)
        self.assertAlmostEqual(result["rmse_pp"], np.sqrt(12.5))
        self.assertAlmostEqual(result["historical_all_rows_rmse_pp"], np.sqrt(25/3))
        self.assertFalse(result["adequate"])
        self.assertFalse(metrics([])["resolved"])
        with self.assertRaises(ValueError):
            metrics([{"x": 15, "error_pp": np.nan}])

    def test_simplicity_unresolved_and_lexical_selection(self):
        scores = [{"candidate": "independent", "resolved": True, "rmse_pp": 5},
                  {"candidate": "revised", "resolved": True, "rmse_pp": 5.25},
                  {"candidate": "inactivation", "resolved": False, "rmse_pp": .1}]
        self.assertEqual(select_family(scores), "revised")
        scores[1]["rmse_pp"] = 5.250001
        self.assertEqual(select_family(scores), "independent")
        self.assertIsNone(select_family([{"candidate": "revised", "resolved": False, "rmse_pp": None}]))
        self.assertEqual(select_family([{"candidate": c, "resolved": True, "rmse_pp": 1}
                                        for c in ("trapping_free", "trapping_equilibrium")]), "trapping_equilibrium")

    def test_actual_source_nested_splits_and_held_labels_independence(self):
        rows = [r for r in load() if r["dataset"].startswith("S13")]
        dose_groups = groups(rows)
        self.assertEqual(len(dose_groups), 8)
        pair_training = set()
        for outer in dose_groups:
            fixed = split_record(rows, outer)
            self.assertEqual(len(fixed["training_row_ids"]), 28)
            for inner in dose_groups:
                if inner == outer:
                    continue
                record = split_record(rows, outer, inner)
                self.assertEqual(len(record["training_row_ids"]), 24)
                self.assertEqual(len(record["evaluation_row_ids"]), 5)
                pair_training.add(tuple(record["training_row_ids"]))
                changed = deepcopy(rows)
                for r in changed:
                    if r["group_id"] in (outer, inner):
                        r["value_percent"] = -100000
                self.assertEqual(record, split_record(changed, outer, inner))
                before = [r["value_percent"] for r in rows if r["row_id"] in record["training_row_ids"]]
                after = [r["value_percent"] for r in changed if r["row_id"] in record["training_row_ids"]]
                self.assertEqual(before, after)
        self.assertEqual(len(pair_training), 28)
        broken = split_record(rows, dose_groups[0], dose_groups[1])
        broken["training_row_ids"].append(broken["outer_row_ids"][0])
        with self.assertRaises(AssertionError):
            assert_split(broken)

    def test_unresolved_fold_cannot_produce_partial_score(self):
        result = aggregate("revised", [{"resolved": True}, {"resolved": False}], [{"x": 15, "error_pp": 0}])
        self.assertFalse(result["resolved"])
        self.assertIsNone(result["rmse_pp"])
        self.assertFalse(result["adequate"])

    def test_all_start_failures_preserved_without_retry(self):
        rows = [{"x": 15, "group_id": "a", "row_id": "a15", "value_percent": 1, "seed_uM": 1, "hyper_a_uM": 0}]
        with tempfile.TemporaryDirectory() as directory, patch("run.least_squares", side_effect=ArithmeticError("synthetic integration failure")) as optimizer:
            result = fit("revised", rows, Path(directory)/"fit.json")
            self.assertEqual(optimizer.call_count, 6)
            self.assertFalse(result["resolved"])
            self.assertTrue(result["complete"])
            self.assertEqual(len(result["starts"]), 6)
            self.assertTrue(all("synthetic integration failure" in s["message"] for s in result["starts"]))
            self.assertTrue((Path(directory)/"fit.json").stat().st_size > 0)

    def test_held_prediction_failure_is_unresolved(self):
        detail = {"resolved": True, "parameters": {}}
        with patch("run.predict", side_effect=ArithmeticError("held integration failure")):
            result, predictions = evaluate(detail, [])
        self.assertFalse(result["resolved"])
        self.assertIn("held integration failure", result["error"])
        self.assertEqual(predictions, [])

    def test_registered_parameters_and_fixed_profile_value(self):
        self.assertEqual(len(STARTS), 6)
        self.assertTrue(all(set(start) == set(START_NAMES) for start in STARTS))
        self.assertEqual(len(PARAMETERS), 6)
        p = decode("independent_inactivation", [-1, -3, -2, -4, -2], {"kb": 100})
        self.assertEqual(p.kb, 100)
        self.assertEqual(p.ka, .01)
        self.assertAlmostEqual(p.kd, .01)
        self.assertFalse(p.equilibrated)
        p = decode("trapping_equilibrium", [-1, -3, 0, -2, -1])
        self.assertTrue(p.equilibrated)


if __name__ == "__main__":
    unittest.main()
