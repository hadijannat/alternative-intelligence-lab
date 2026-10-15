"""Validation checks protect informative denominators, group splits and failure propagation."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import numpy as np

from model import Parameters
from run import (challenge_split, fit_transport, scenario_metadata, transport_scenarios, PARAMETERS, STARTS, START_NAMES, aggregate, assert_split, decode, evaluate, fit, groups,
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
        scores = [{"candidate": "release", "resolved": True, "rmse_pp": 5},
                  {"candidate": "baseline", "resolved": True, "rmse_pp": 5.25},
                  {"candidate": "reversible_free", "resolved": False, "rmse_pp": .1}]
        self.assertEqual(select_family(scores), "baseline")
        scores[1]["rmse_pp"] = 5.250001
        self.assertEqual(select_family(scores), "release")
        self.assertIsNone(select_family([{"candidate": "baseline", "resolved": False, "rmse_pp": None}]))
        self.assertEqual(select_family([{"candidate": c, "resolved": True, "rmse_pp": 1}
                                        for c in ("reversible_free", "reversible_equilibrium")]), "reversible_equilibrium")

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
        result = aggregate("baseline", [{"resolved": True}, {"resolved": False}], [{"x": 15, "error_pp": 0}])
        self.assertFalse(result["resolved"])
        self.assertIsNone(result["rmse_pp"])
        self.assertFalse(result["adequate"])

    def test_all_start_failures_preserved_without_retry(self):
        rows = [{"x": 15, "group_id": "a", "row_id": "a15", "value_percent": 1, "seed_uM": 1, "hyper_a_uM": 0}]
        with tempfile.TemporaryDirectory() as directory, patch("run.least_squares", side_effect=ArithmeticError("synthetic integration failure")) as optimizer:
            result = fit("baseline", rows, Path(directory)/"fit.json")
            self.assertEqual(optimizer.call_count, 6)
            self.assertFalse(result["resolved"])
            self.assertTrue(result["complete"])
            self.assertEqual(len(result["starts"]), 6)
            self.assertTrue(all("synthetic integration failure" in s["message"] for s in result["starts"]))
            self.assertTrue((Path(directory)/"fit.json").stat().st_size > 0)

    def test_exhausted_starts_retain_finite_score_without_becoming_resolved(self):
        rows = [{"x": 15, "group_id": "a", "row_id": "a15", "value_percent": 1,
                 "seed_uM": 1, "hyper_a_uM": 0}]
        exhausted = SimpleNamespace(success=False, status=0, nfev=160, njev=120,
                                    fun=np.array([.1]), x=np.zeros(6), active_mask=np.zeros(6),
                                    message="Maximum function evaluations exceeded")
        with tempfile.TemporaryDirectory() as directory, patch("run.least_squares", return_value=exhausted):
            result = fit("baseline", rows, Path(directory)/"fit.json")
        self.assertFalse(result["resolved"])
        self.assertTrue(result["complete"])
        self.assertEqual(len(result["starts"]), 6)
        self.assertTrue(all(r["nfev"] == 160 and r["status"] == 0 for r in result["starts"]))
        self.assertTrue(all(r["sse"] > 0 for r in result["starts"]))

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
        self.assertEqual(len(PARAMETERS), 4)
        p = decode("baseline", [-1, -3, -2, -4, -2], {"kb": 100})
        self.assertEqual(p.kb, 100)
        self.assertEqual(p.ka, .01)
        self.assertAlmostEqual(p.kd, .01)
        self.assertFalse(p.equilibrated)
        self.assertFalse(p.turnover)
        self.assertEqual(p.krel, 0)
        self.assertEqual(p.kbind, 0)
        p = decode("reversible_equilibrium", [-1, -3, 0, -2, -1, -2, -1, -2])
        self.assertTrue(p.equilibrated)
        self.assertTrue(p.turnover)
        release = decode("release", [-1, -3, 0, -2, -1, -2, -1])
        self.assertEqual(release.kbind, 0)
        self.assertTrue(release.turnover)

    def test_fixed_joint_challenge_excludes_high_dose_at_all_training_times(self):
        rows = [r for r in load() if r["dataset"].startswith("S13")]
        early, late = challenge_split(rows)
        self.assertEqual((len(early), len(late)), (16, 16))
        train, held = challenge_split(rows, joint=True)
        self.assertEqual((len(train), len(held)), (12, 4))
        self.assertEqual({r["x"] for r in train}, {15, 30})
        self.assertEqual({r["x"] for r in held}, {45, 60})
        self.assertTrue(all(r["seed_uM"] <= .5 and r["hyper_a_uM"] <= 2 for r in train))
        self.assertEqual({r["group_id"] for r in held}, {"S13_F1|1|0", "S13_HyperA|0|2.5"})
        changed = deepcopy(rows)
        for row in changed:
            if row["seed_uM"] == 1 or row["hyper_a_uM"] == 2.5:
                row["value_percent"] = -100000
        self.assertEqual(train, challenge_split(changed, joint=True)[0])

    def test_all_families_transport_with_reset_only_for_selected_turnover(self):
        scenarios = list(transport_scenarios("reversible_free"))
        self.assertEqual(len(scenarios), 20)
        self.assertEqual(len({tuple(s) for s in scenarios}), 20)
        for family in PARAMETERS:
            self.assertEqual(sum(c == family and not reset for c, _, _, reset in scenarios), 4)
        self.assertTrue(all(c == "reversible_free" for c, _, _, reset in scenarios if reset))
        self.assertEqual(len(list(transport_scenarios("baseline"))), 16)
        self.assertEqual(len(list(transport_scenarios(None))), 16)
        p = Parameters(transport="contact", loss="all_or_none", complex_reset=True)
        self.assertEqual(scenario_metadata("release", p)["scenario"], "release|contact|all_or_none|reset-1")

    def test_transport_failure_records_attempt_without_refitting_chemistry(self):
        rows = [r for r in load() if r["dataset"] == "Figure_2"]
        with tempfile.TemporaryDirectory() as directory, patch("run.single_cycle", side_effect=ArithmeticError("synthetic transport failure")):
            path = Path(directory)/"mixing.json"
            with self.assertRaises(ArithmeticError):
                fit_transport(Parameters(), rows, path)
            import json
            saved = json.loads(path.read_text())
        self.assertTrue(saved["complete"])
        self.assertFalse(saved["resolved"])
        self.assertEqual(saved["fitted_parameters"], ["mixing"])
        self.assertEqual(len(saved["evaluations"]), 1)
        self.assertEqual(saved["n"], 18)
        self.assertIn("synthetic transport failure", saved["error"])
        self.assertEqual(saved["frozen_chemistry_parameters"]["retention_f"], .55)


if __name__ == "__main__":
    unittest.main()
