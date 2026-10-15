"""Conservation, limiting cases and numerical regression checks for the engine."""
from dataclasses import replace
import unittest

import numpy as np

from model import (MOIETIES, Parameters, bulk_curve, bulk_curves, exchange, fresh,
                   initial, initial_complexes, rates, react, reporter, serial, single_cycle)


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.p = Parameters(kf=.1, kh=.001, ka=.2, krh=.003, kd=.02, kon=.5, koff=.03)
        self.x = np.array([[2, 1, 5, .2, .1, .3, .1, .2]], float)

    def test_moieties_and_nonnegative_with_all_channels(self):
        for regeneration in (True, False):
            y = react(self.x, 60, self.p, regeneration, times=[0, 1, 15, 60])
            np.testing.assert_allclose(y@MOIETIES.T, np.repeat((self.x@MOIETIES.T)[None], 4, axis=0), atol=1e-7)
            self.assertTrue(np.all(y >= 0))
            self.assertGreater(y[-1, 0, 5], self.x[0, 5])

    def test_zero_b_disables_ligation_without_complex_reservoir(self):
        x = np.array([[2, 1, 0, .2, 0, 0, 0, 0]], float)
        y = react(x, 60, replace(self.p, kd=0))
        np.testing.assert_allclose(y, x, atol=1e-12)

    def test_inactive_f_and_reporter_do_not_catalyze(self):
        x = np.array([[0, 1, 5, 0, 2, 3, 0, 0]], float)
        np.testing.assert_allclose(react(x, 60, Parameters()), x)

    def test_disabled_and_independent_ligation_channels(self):
        x = np.array([[2, 1, 5, 0, 0, 0, 0, 0]], float)
        np.testing.assert_allclose(react(x, 60, Parameters(kh=0)), x)
        y = react(x, 60, Parameters(kh=0, krh=.02))
        self.assertEqual(y[0, 3], 0)
        self.assertGreater(y[0, 4], 0)
        x[0, 3] = 1
        y = react(x, 60, Parameters(kf=0, ka=.2, kh=0))
        self.assertEqual(y[0, 4], 0)
        self.assertGreater(y[0, 3], 1)

    def test_no_regeneration_routes_product_to_inactive_f(self):
        x = np.array([[2, 1, 5, .2, 0, 0, 0, 0]], float)
        y = react(x, 60, self.p, regeneration=False)
        self.assertAlmostEqual(y[0, 3], .2*np.exp(-1.2), places=8)
        self.assertGreater(y[0, 5], .2-y[0, 3])

    def test_saturation_and_default_ka(self):
        x = np.array([[2, 1, 1e12, .2, 0, 0, 0, 0]], float)
        p = Parameters(kf=.1, kh=.001, krh=.003)
        va, vr = rates(x, p)
        self.assertAlmostEqual(va[0], .1*.2*2+.001*4, places=10)
        self.assertAlmostEqual(vr[0], .1*.2+.003*2, places=10)
        np.testing.assert_allclose(rates(x, p), rates(x, replace(p, ka=.1)))

    def test_equilibrated_initial_complexes_conserve_and_balance(self):
        p = replace(self.p, equilibrated=True)
        x = np.array([[2, 5, 7.5, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 15, 0, 0, 0, 0, 0], [10, 2, 1, 0, 0, 0, 0, 0]], float)
        y = initial_complexes(x, p)
        np.testing.assert_allclose(y@MOIETIES.T, x@MOIETIES.T, atol=1e-12)
        np.testing.assert_allclose(p.kon*y[:, 0]*y[:, 2], p.koff*y[:, 6], atol=1e-12)
        np.testing.assert_allclose(p.kon*y[:, 1]*y[:, 2], p.koff*y[:, 7], atol=1e-12)
        self.assertGreater(y[0, 6], 0)
        self.assertGreater(y[0, 7], 0)
        np.testing.assert_allclose(initial_complexes(y, p), y, atol=1e-12)
        binding_only = replace(p, kf=0, ka=0, kh=0, krh=0, kd=0)
        np.testing.assert_allclose(react(y, 60, binding_only), y, atol=1e-9)
        np.testing.assert_allclose(fresh(p), fresh(replace(p, equilibrated=False)))

    def test_complex_is_denatured_reporter_substrate_in_observer(self):
        x = np.array([[0, 1, 0, 0, 7, 0, 0, 2]], float)
        self.assertEqual(reporter(x, [1]), 70.)
        self.assertIs(type(reporter(x, [1])), float)
        self.assertEqual(reporter(np.zeros((1, 8)), [1]), 0.)

    def test_saved_prior_baseline_equivalence(self):
        # Prior DOP853 engine, results-v2 saved parameters with q=1 and hroute=0.
        p = Parameters(kf=1.5191726905179304, kh=.0003697516065118584, kb=99.99999973874252)
        expected = [[0, .0007120556382792167, .003927462720972346, .012684238255465472, .03370191930406673],
                    [0, 4.3349684307212275, 67.00967324833181, 74.18776403949185, 74.90397571685995],
                    [0, 48.02348231855159, 68.2848769535631, 79.08118336379185, 85.57320821365938],
                    [0, 97.7817255640697, 99.86761167049542, 99.99179826856198, 99.99949073107722]]
        np.testing.assert_allclose(bulk_curves(p, [0, 0, .5, 5], [.5, 5, 0, 0]), expected, atol=2e-5, rtol=2e-6)

    def test_f_times_t_collapse_and_distinct_mechanism_breaks(self):
        p = Parameters()
        times = np.array([0, 5, 10, 20, 40.])
        a, b = bulk_curve(p, 1, times=times), bulk_curve(p, 2, times=times/2)
        np.testing.assert_allclose(a, b, atol=1e-5)
        for alternative in (replace(p, kd=.04), replace(p, kon=.1, koff=.01)):
            a = bulk_curve(alternative, 1, times=times)
            b = bulk_curve(alternative, 2, times=times/2)
            self.assertGreater(np.max(np.abs(a-b)), 1.)

    def test_batched_matches_separate_and_refinement(self):
        seeds, hypers = [0, .1, 1, 0], [.5, 0, 0, 5]
        for p in (self.p, replace(self.p, kon=100, koff=.001), replace(self.p, equilibrated=True)):
            batch = bulk_curves(p, seeds, hypers)
            separate = np.array([bulk_curve(p, f, a) for f, a in zip(seeds, hypers)])
            np.testing.assert_allclose(batch, separate, atol=3e-5, rtol=1e-5)
            coarse = react(self.x, 60, p, times=[0, 1, 15, 60])
            fine = react(self.x, 60, p, rtol=1e-10, times=[0, 1, 15, 60])
            np.testing.assert_allclose(coarse, fine, atol=2e-7, rtol=1e-5)

    def test_exchange_species_conservation_and_retention(self):
        for transport in ("fractional", "contact"):
            p = replace(self.p, transport=transport, retention_f=.8)
            x = np.vstack((self.x, self.x*2))
            w = np.array([.25, .75])
            y, v, lost = exchange(x, w, p, 3)
            expected = (w@x)*.55
            expected[[3, 5]] = (w@x)[[3, 5]]*.8
            np.testing.assert_allclose(v@y, expected, atol=1e-12)
            np.testing.assert_allclose(v@y+lost, w@x, atol=1e-12)
            self.assertAlmostEqual(v.sum(), 1)
            np.testing.assert_allclose(x, np.vstack((self.x, self.x*2)))

    def test_transport_limits_and_no_exchange(self):
        for mixing in (0, 1):
            p = replace(self.p, mixing=mixing)
            a = single_cycle(p, 1, 3)
            b = single_cycle(replace(p, transport="contact"), 1, 3)
            self.assertAlmostEqual(a, b, places=7)
            if mixing == 0:
                self.assertEqual(a, 0)

    def test_serial_founder_feed_and_moiety_balances(self):
        for transport in ("fractional", "contact"):
            p = replace(self.p, transport=transport, retention_f=.8)
            rows = serial(p, 2, regeneration=False)
            initial_source = np.array(rows[0]["source_moiety_uM"])
            per_feed = MOIETIES@(.25*fresh(p).sum(axis=0))
            for row in rows:
                g = row["generation"]
                expected = 2/3 if g == 0 else 2/3*.8**g*.5**(g-1)*np.exp(-60*p.kd*g)
                self.assertAlmostEqual(row["F1_uM"], expected, places=8)
                self.assertAlmostEqual(row["founder_F1_model_uM"], expected, places=12)
                self.assertLess(row["newly_generated_F1_model_uM"], 1e-8)
                self.assertLess(row["moiety_balance_max_error_uM"], 1e-7)
                np.testing.assert_allclose(row["source_moiety_uM"], initial_source+max(0, g-1)*per_feed)
                self.assertTrue(0 <= row["yield_percent"] <= 100)

    def test_initial_state_and_zero_duration(self):
        x, w = initial(1, self.p)
        self.assertEqual(x.shape, (3, 8))
        self.assertAlmostEqual((w@x)[1], 2.5/3)
        np.testing.assert_equal(react(x, 0, self.p), x)
        np.testing.assert_equal(react(x, 0, self.p, times=[0]), x[None])

    def test_invalid_parameters_and_inputs(self):
        for changes in ({"kf": -1}, {"kh": np.nan}, {"ka": -1}, {"kb": 0}, {"kd": np.inf},
                        {"kon": -1}, {"koff": -1}, {"mixing": np.nan}, {"mixing": 2},
                        {"retention_f": 0}, {"retention_fragments": np.inf}, {"transport": "bad"},
                        {"equilibrated": True, "kon": 0}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(self.p, **changes)
        for x in (np.zeros((1, 7)), np.zeros((0, 8)), np.full((1, 8), -1.), np.full((1, 8), np.nan)):
            with self.assertRaises(ValueError):
                react(x, 60, self.p)
        for times in ([], [10, 5], [-1, 0], [0, 61], [0, np.nan], [0, 0]):
            with self.assertRaises(ValueError):
                react(self.x, 60, self.p, times=times)
        for value in (-1, np.inf):
            with self.assertRaises(ValueError):
                react(self.x, value, self.p)
        for value in (0, -1, np.nan):
            with self.assertRaises(ValueError):
                react(self.x, 60, self.p, rtol=value)
        with self.assertRaises(ValueError):
            bulk_curves(self.p, [1, 2], [0])
        with self.assertRaises(ValueError):
            bulk_curve(self.p, seed=-1)
        for n in (-1, 1.5, np.nan):
            with self.assertRaises(ValueError):
                exchange(self.x, [1], self.p, n)
            with self.assertRaises(ValueError):
                serial(self.p, 1, generations=n)
        for w in ([.5], [-1], [1, 0], [np.nan]):
            with self.assertRaises(ValueError):
                exchange(self.x, w, self.p, 1)


if __name__ == "__main__":
    unittest.main()
