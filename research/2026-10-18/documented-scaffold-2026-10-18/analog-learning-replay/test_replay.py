"""Synthetic verification only: these tests never open the native archive."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from replay import analyze, baselines, logical, overlap, result_path


def fixture(differential=1, snapshots=5):
    sources = np.array([[0, 0, 1, 1], [0, 1, 0, 1], [0.7] * 4])
    labels = np.array([[0, 1, 1, 0]], dtype=float)
    targets = np.vstack((np.full((1, 4), 0.2), 0.2 + labels)) if differential else labels
    task = np.vstack((sources, targets))
    target_locs = np.array([[1, 3], [3, 1]]) if differential else np.array([[1, 3]])
    source_locs = np.array([[0, 3], [2, 0], [3, 3]])
    free = np.zeros((4, 4, snapshots, 4))
    for i in range(snapshots):
        free[source_locs[:, 0], source_locs[:, 1], i, :] = sources
        free[target_locs[:, 0], target_locs[:, 1], i, :] = targets + (snapshots - 1 - i) * np.arange(1, len(target_locs) + 1)[:, None] * 0.1
    props = dict(MES=np.array([[snapshots]]), TRA=np.array([[4]]), TST=np.array([[4]]),
        SOR=np.array([[3]]), TAR=np.array([[len(target_locs)]]), DEL=np.array([[differential]]),
        NODEMULT=np.array([[2.0]]), GATEMULT=np.array([[10.0]]), TRAIN=task.copy(), TEST=task.copy(),
        TLOC=target_locs, SLOC=source_locs, TestFreeState=free,
        TestMeasurements=free[target_locs[:, 0], target_locs[:, 1]].transpose(0, 2, 1).copy(),
        TestMSE=np.zeros((1, snapshots)), DOTEST=np.arange(1, snapshots + 1, dtype=float)[None, :],
        LearnTimes=np.array([[0] + [1e6] * (snapshots - 1)]),
        HorizontalCapacitors=np.repeat(np.arange(snapshots)[None, None, :], 16, axis=0).reshape(4, 4, snapshots),
        VerticalCapacitors=np.zeros((4, 4, snapshots)))
    return props


class ReplayTests(unittest.TestCase):
    def test_asymmetric_axis_mapping_and_differential_sign(self):
        p = fixture()
        r = analyze(p)
        self.assertEqual(r["status"], "replayed")
        self.assertEqual([row["scheduled_training_step"] for row in r["snapshots"]], [1, 2, 3, 4, 5])
        self.assertEqual(r["snapshots"][-1]["mse_volts2"], 0)
        self.assertAlmostEqual(r["snapshots"][0]["mse_volts2"], 0.64)
        self.assertEqual(logical(np.array([[3.0], [1.0], [5.0], [8.0]]), 1).tolist(), [[-2], [3]])
        p["TestMeasurements"][0, 2, 3] += 0.01
        r = analyze(p)
        self.assertEqual(r["status"], "failed_mapping")
        self.assertEqual(r["mapping_mismatch_indices"], [3])
        self.assertNotIn("endpoints", r)
        self.assertFalse(any("mse_volts2" in row for row in r["snapshots"]))

    def test_single_ended_output_and_full_grid_finiteness(self):
        p = fixture(0)
        p["TestFreeState"][2, 2, 2, 1] = np.nan
        r = analyze(p)
        self.assertEqual(r["status"], "replayed")
        self.assertEqual(r["snapshots"][2]["validity_reasons"], ["nonfinite_free_state"])
        self.assertEqual(r["snapshots"][-1]["mse_volts2"], 0)

    def test_placeholder_is_structural_not_zero_error_or_output(self):
        p = fixture()
        p["TestFreeState"][:, :, 0, :] = 0
        p["TestMeasurements"][:, :, 0] = 9  # ignored only because raw snapshot is structurally absent
        p["TestFreeState"][:, :, 2, :] = np.nan
        p["TestFreeState"][:, :, 4, :] = 0
        r = analyze(p)
        self.assertEqual(r["structurally_complete_indices"], [1, 3])
        self.assertEqual(len(r["snapshots"]), 5)
        self.assertEqual(r["endpoints"]["earliest_available_measured_snapshot"], 1)
        self.assertEqual(r["endpoints"]["final_complete_snapshot"], 3)
        self.assertFalse(r["native_first_snapshot_complete"])
        self.assertFalse(r["native_final_snapshot_complete"])
        self.assertEqual(r["endpoints"]["earliest_learning_seconds"], 1)
        self.assertAlmostEqual(r["capacitor_first_to_final"]["rms_change_volts"], 20 / np.sqrt(2))
        # A genuine zero state remains eligible if every specified input is zero.
        p = fixture(0, 1)
        p["TRAIN"][:3] = p["TEST"][:3] = 0
        p["TestFreeState"][:] = p["TestMeasurements"][:] = 0
        self.assertEqual(analyze(p)["structurally_complete_indices"], [0])

    def test_endpoints_never_select_best_epoch(self):
        p = fixture(0)
        p["TestFreeState"][1, 3, 2, :] = p["TEST"][3:][0]
        p["TestMeasurements"] = p["TestFreeState"][p["TLOC"][:, 0], p["TLOC"][:, 1]].transpose(0, 2, 1).copy()
        p["TestFreeState"][1, 3, 4, :] += 0.3
        p["TestMeasurements"][0, :, 4] += 0.3
        r = analyze(p)
        self.assertEqual(r["endpoints"]["final_complete_snapshot"], 4)
        self.assertGreater(r["endpoints"]["final_mse_volts2"], r["snapshots"][2]["mse_volts2"])
        self.assertEqual(r["baselines"]["frozen_earliest_observed"]["mse_volts2"], r["snapshots"][0]["mse_volts2"])
        self.assertAlmostEqual(r["capacitor_first_to_final"]["rms_change_volts"], 40 / np.sqrt(2))

    def test_overlap_includes_fixed_boundary_and_target_conflicts(self):
        train = np.array([[0, 0, 1], [0.5, 0.5, 0.5]])
        test = np.array([[0, 1 + 0.5e-12, 0], [0.5, 0.5, 0.6]])
        r = overlap(train, test, np.array([[0, 1, 2]]), np.array([[1, 2, 0]]), 0)
        self.assertEqual(len(r["exact"]["test_to_train"][0]["matches"]), 2)
        self.assertTrue(r["exact"]["train_duplicates"][0]["native_target_conflict"])
        self.assertEqual(r["exact"]["test_to_train"][1]["matches"], [])
        self.assertEqual(len(r["max_coordinate_tolerance_1e_12"]["test_to_train"][1]["matches"]), 1)
        self.assertEqual(r["exact"]["test_to_train"][2]["matches"], [])

    def test_xor_affine_baseline_is_train_only(self):
        p = fixture()
        x = p["TRAIN"][:3] * 2
        y = logical(p["TRAIN"][3:], 1) * 2
        result = baselines(x, x, y, y)
        self.assertEqual(result["affine"]["source_coordinate_indices"], [0, 1])
        self.assertEqual(result["affine"]["rank"], 3)
        self.assertEqual(result["affine"]["feature_count"], 3)
        self.assertAlmostEqual(result["affine"]["mse_volts2"], 1)
        np.testing.assert_allclose(result["affine"]["weights"], [[1], [0], [0]], atol=1e-12)
        changed = baselines(x, x, y, y + 100)
        self.assertEqual(result["affine"]["weights"], changed["affine"]["weights"])
        self.assertEqual(result["training_mean"]["fitted_mean_volts"], changed["training_mean"]["fitted_mean_volts"])

    def test_rank_deficiency_and_logically_equal_native_target_conflict(self):
        x = np.array([[0., 1., 2.], [0., 1., 2.]])
        result = baselines(x, x, np.array([[0., 2., 4.]]), np.array([[0., 2., 4.]]))
        self.assertEqual(result["affine"]["rank"], 2)
        self.assertEqual(result["affine"]["feature_count"], 3)
        self.assertLess(result["affine"]["mse_volts2"], 1e-25)
        r = overlap(np.zeros((1, 1)), np.zeros((1, 1)),
                    np.array([[0.], [1.]]), np.array([[2.], [3.]]), 1)
        match = r["exact"]["test_to_train"][0]["matches"][0]
        self.assertTrue(match["native_target_conflict"])
        self.assertFalse(match["logical_target_conflict"])

    def test_time_failures_and_zero_baseline_ratio(self):
        for invalid in (-1.0, np.nan, np.inf):
            p = fixture()
            p["LearnTimes"] = p["LearnTimes"].astype(float)
            p["LearnTimes"][0, 2] = invalid
            with np.errstate(invalid="ignore"):
                r = analyze(p)
            self.assertEqual(r["status"], "failed_time")
            self.assertEqual(len(r["snapshots"]), 5)
            self.assertNotIn("endpoints", r)
        p = fixture(0, 1)
        r = analyze(p)
        self.assertEqual(r["snapshots"][0]["learning_seconds"], 0)
        self.assertIsNone(r["endpoint_comparisons"]["final"]["frozen_earliest_observed"]["observed_over_baseline_mse"])

    def test_source_drift_is_diagnostic_and_no_complete_is_explicit(self):
        p = fixture()
        p["TestFreeState"][0, 3, -1, :] += 0.1
        r = analyze(p)
        self.assertEqual(r["status"], "replayed")
        self.assertAlmostEqual(r["snapshots"][-1]["source_program_mismatch_rms_volts"], 0.2 / np.sqrt(3))
        self.assertAlmostEqual(r["source_first_to_final_drift"]["max_abs_volts"], 0.2)
        p["TestFreeState"][:] = np.nan
        r = analyze(p)
        self.assertEqual(r["status"], "failed_no_complete_snapshot")
        self.assertEqual(len(r["snapshots"]), 5)
        self.assertEqual(r["structurally_complete_indices"], [])

    def test_invalid_counts_locations_and_caps_remain_explicit(self):
        p = fixture()
        p["TLOC"][0, 0] = -1
        with self.assertRaisesRegex(ValueError, "grid location"):
            analyze(p)
        p = fixture()
        p["HorizontalCapacitors"] = p["HorizontalCapacitors"].astype(float)
        p["HorizontalCapacitors"][0, 0, -1] = np.nan
        r = analyze(p)
        self.assertFalse(r["capacitor_first_to_final"]["endpoints_finite"])
        self.assertIsNone(r["capacitor_first_to_final"]["rms_change_volts"])
        p["DEL"] = np.array([[2]])
        with self.assertRaisesRegex(ValueError, "DEL"):
            analyze(p)

    def test_test_schedule_is_positive_integral_strictly_increasing(self):
        for invalid in (0.0, -1.0, np.nan, np.inf, 2.0, 2.5, 6.0):
            p = fixture()
            p["DOTEST"][0, 2] = invalid
            with self.assertRaisesRegex(ValueError, "DOTEST"):
                analyze(p)
        p = fixture()
        p["DOTEST"] = np.array([[1., 10., 25., 100., 1000.]])
        self.assertEqual([row["scheduled_training_step"] for row in analyze(p)["snapshots"]],
                         [1, 10, 25, 100, 1000])

    def test_output_name_is_fresh_json_basename(self):
        with tempfile.TemporaryDirectory() as directory, patch("replay.ROOT", Path(directory)):
            self.assertEqual(result_path("replay-schedule.json"), Path(directory) / "results/replay-schedule.json")
            for invalid in ("../replay.json", "/tmp/replay.json", "nested/replay.json", "nested\\replay.json", "replay.txt", ".json"):
                with self.assertRaisesRegex(ValueError, "JSON basename"):
                    result_path(invalid)
            previous = result_path("replay.json")
            previous.parent.mkdir()
            previous.write_text("preserved\n")
            with self.assertRaises(FileExistsError):
                result_path("replay.json")
            self.assertEqual(previous.read_text(), "preserved\n")


if __name__ == "__main__":
    unittest.main()
