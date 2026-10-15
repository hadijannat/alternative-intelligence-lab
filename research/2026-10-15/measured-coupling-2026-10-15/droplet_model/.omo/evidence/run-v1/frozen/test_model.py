import unittest
import numpy as np
from model import AZIDE, Q, VOLUME, initial, integrate, passages, total_product, transfer


class ChemicalLedgerTests(unittest.TestCase):
    def test_analytic_matches_chemical_ode(self):
        for seed in (0, .02):
            for kcat in (0, 3):
                for time in (.2, 2, 16):
                    end = integrate(initial(seed), time, .04, kcat, .3, .8, .2)
                    self.assertAlmostEqual(sum(end[2:]) / VOLUME,
                                           float(total_product(time, .04, kcat, seed=seed)), places=8)

    def test_stoichiometry_and_nonnegativity(self):
        start = initial(.03, .4)
        end = integrate(start, 30, .01, 8, .6, 2, .3)
        formed = sum(end[4:])
        self.assertLess(max(abs((start[0]-end[0])-formed),
                            abs((start[1]-end[1])-3*formed)), 1e-7)
        self.assertAlmostEqual(sum(end[2:4]), sum(start[2:4]), places=8)
        self.assertGreaterEqual(min(end), -1e-8)

    def test_absent_baseline_and_seed_cannot_regenerate(self):
        end = integrate(initial(), 100, 0, 5)
        np.testing.assert_allclose(end, initial(), atol=1e-12)

    def test_identical_bulk_opposite_retention(self):
        inside = integrate(initial(), 2, .04, 3, 1)
        outside = integrate(initial(), 2, .04, 3, 0)
        self.assertAlmostEqual(sum(inside[4:]), sum(outside[4:]), places=8)
        self.assertGreater(inside[4], 1)
        self.assertEqual(outside[4], 0)

    def test_transfer_accounting_all_modes(self):
        state = integrate(initial(.02, .5), 2, .04, 3, .8, 1)
        for mode in ("selected", "bulk", "pooled"):
            kept, discarded, feed = transfer(state, .7, mode)
            np.testing.assert_allclose(kept[:2] + discarded[:2], state[:2] + feed)
            self.assertAlmostEqual(sum(kept[2:4])+discarded[2], sum(state[2:4]))
            self.assertAlmostEqual(sum(kept[4:])+discarded[3], sum(state[4:]))

    def test_full_passage_balance_and_refinement(self):
        for mode in ("selected", "bulk", "pooled"):
            for control in ("regeneration", "baseline_only", "no_regeneration"):
                rows, balance = passages(.04, 3, .6, .5, .8, .7, control, mode)
                self.assertLess(max(map(abs, balance.values())), 1e-6)
                refined, _ = passages(.04, 3, .6, .5, .8, .7, control, mode, rtol=1e-11)
                np.testing.assert_allclose(rows[-1]["state_nmol"], refined[-1]["state_nmol"],
                                           rtol=1e-7, atol=1e-8)
                if control == "no_regeneration":
                    self.assertEqual(sum(x["newly_formed_nmol"] for x in rows), 0)
                    self.assertFalse(rows[-1]["conditional_function_pass"])

    def test_well_mixed_founders_dilute_geometrically(self):
        rows, _ = passages(.04, 3, 1, .5, 0, 1, "no_regeneration", "bulk")
        for row in rows:
            self.assertAlmostEqual(row["retained_founder_nmol"], .02*VOLUME*0.5**row["passage"])

    def test_boundary_validation(self):
        with self.assertRaises(ValueError):
            integrate(initial(), 2, .04, 3, localization=2)
        with self.assertRaises(ValueError):
            transfer(initial(), -.1)
        with self.assertRaises(ValueError):
            integrate([float("nan")]*6, 2, .04, 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
