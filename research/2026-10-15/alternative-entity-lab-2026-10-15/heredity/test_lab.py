import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from lab import assay, exchange, mutate_counts, partition_counts, purge_founders, run, simulate_arm, validate_config


class HeredityTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((Path(__file__).parent/"config.json").read_text())
        self.c.update(seeds=[101], compartments=4, passages=5, founder_purge_passage=2,
                      final_passages=2, mutation_probabilities=[0.03], resource_budgets=[16])

    def test_partition_conservation_and_input_unchanged(self):
        counts = np.array([100, 25], dtype=np.int64)
        for seed in range(20):
            a, b = partition_counts(counts, np.random.default_rng(seed))
            np.testing.assert_array_equal(a+b, counts)
            self.assertTrue(np.all(a >= 0) and np.all(b >= 0))
        np.testing.assert_array_equal(counts, [100, 25])

    def test_mutation_conservation_and_endpoints(self):
        counts = np.array([17, 4], dtype=np.int64)
        rng = np.random.default_rng(3)
        np.testing.assert_array_equal(mutate_counts(counts, 0, rng), counts)
        np.testing.assert_array_equal(mutate_counts(counts, 1, rng), counts[::-1])
        self.assertEqual(int(mutate_counts(counts, .7, rng).sum()), 21)
        np.testing.assert_array_equal(counts, [17, 4])

    def test_interface_invalid_inputs(self):
        rng = np.random.default_rng(2)
        for bad in ([-1, 2], [1.0, 2.0], [1, 2, 3], [True, False]):
            with self.assertRaises(ValueError):
                partition_counts(np.asarray(bad), rng)
        for bad in (-.1, 1.1, float("nan"), True, "0.5"):
            with self.assertRaises(ValueError):
                mutate_counts(np.array([1, 2]), bad, rng)

    def test_purge_removes_only_founders(self):
        state = np.array([[[3, 2], [6, 8]], [[1, 1], [0, 5]]])
        purged, removed = purge_founders(state)
        np.testing.assert_array_equal(purged[:, 0], 0)
        np.testing.assert_array_equal(purged[:, 1], state[:, 1])
        np.testing.assert_array_equal(removed, [5, 2])
        self.assertEqual(int(state[:, 0].sum()), 7)

    def test_exchange_conserves_types_tags_and_recipient_counts(self):
        state = np.array([[[9, 1], [6, 2]], [[1, 9], [2, 6]], [[0, 0], [7, 1]]])
        swapped = exchange(state, np.random.default_rng(3))
        np.testing.assert_array_equal(swapped.sum(axis=0), state.sum(axis=0))
        np.testing.assert_array_equal(swapped.sum(axis=2), state.sum(axis=2))

    def test_no_synthesis_carryover_then_exact_extinction(self):
        records, summary, _ = simulate_arm(self.c, 91, 16, .03, "no_synthesis")
        self.assertTrue(any(r["founder_A"]+r["founder_B"] for r in records if r["passage"] == 1))
        for r in records:
            self.assertEqual(r["births"]+r["new_A"]+r["new_B"], 0)
            if r["passage"] >= 2:
                self.assertEqual(r["founder_A"]+r["founder_B"]+r["X_events"]+r["Y_events"], 0)
        self.assertEqual(summary["final_extinct_compartments"], 4)

    def test_active_counts_match_and_births_are_paid(self):
        reference = None
        for arm in ("faithful", "exchanged", "neutral"):
            records, _, counts = simulate_arm(self.c, 92, 16, .03, arm)
            if reference is None:
                reference = counts
            self.assertEqual(counts, reference)
            for r in records:
                self.assertEqual(r["balance_residual"], 0)
                self.assertEqual(r["births"], r["synthesis_feed_used"])
                self.assertEqual(r["births"], r["synthesis_fuel_used"])
                self.assertLessEqual(r["births"], 16)
                if r["passage"] >= 2:
                    self.assertEqual(r["founder_events"], 0)

    def test_zero_budget_cannot_renew(self):
        records, summary, _ = simulate_arm(self.c, 93, 0, .03, "faithful")
        self.assertTrue(all(r["births"] == 0 for r in records))
        self.assertEqual(summary["final_extinct_compartments"], 4)

    def test_empty_assay_has_no_activity(self):
        result = assay(np.zeros((4, 2, 2), dtype=int), self.c, np.random.default_rng(3))
        self.assertTrue(all(np.all(x == 0) for x in result.values()))

    def test_invalid_config(self):
        changes = [{"compartments": 3}, {"degradation_probability": -1}, {"final_passages": 4},
                   {"seeds": [1, 1]}, {"resource_budgets": [True]}, {"assay_rate": float("inf")},
                   {"founder_counts": [1.5, 2]}, {"unknown": 0}]
        for change in changes:
            invalid = copy.deepcopy(self.c)
            invalid.update(change)
            with self.assertRaises(ValueError):
                validate_config(invalid)

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory)/"sentinel.txt"
            sentinel.write_text("preserve")
            with self.assertRaises(FileExistsError):
                run(self.c, Path(directory))
            self.assertEqual(sentinel.read_text(), "preserve")


if __name__ == "__main__":
    unittest.main()
