"""Independent balance identities, limiting cases and event-map checks."""
from dataclasses import replace
import unittest

import numpy as np

from model import (MOIETIES, NAMES, Parameters, bulk_curve, bulk_curves,
                   competent_inventory, dissociate_complexes, exchange, fresh,
                   initial, initial_complexes, rates, react, reporter,
                   reporter_product, serial, single_cycle)


def state(**values):
    x = np.zeros((1, len(NAMES)))
    for name, value in values.items():
        x[0, NAMES.index(name)] = value
    return x


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.p = Parameters(kf=.1, kh=.001, ka=.2, krh=.003, kd=.02,
                            turnover=True, kbind=.5, krel=.03)
        self.x = np.array([[2, 1, 5, .2, .1, .3, .1, .2, .3, .1, .2, .1]])

    def test_all_channels_conserve_moieties_and_nonnegativity(self):
        for regeneration in (True, False):
            for turnover in (True, False):
                y = react(self.x, 60, replace(self.p, turnover=turnover),
                          regeneration, times=[0, 1, 15, 60])
                expected = np.repeat((self.x@MOIETIES.T)[None], 4, axis=0)
                np.testing.assert_allclose(y@MOIETIES.T, expected, atol=1e-7)
                self.assertTrue(np.all(y >= 0))

    def test_occupied_catalyst_requires_release(self):
        x = state(A=2, R=1, B=5, QFF=1, QFP=1, QFD=1)
        p = Parameters(turnover=True, kh=0, krel=0)
        np.testing.assert_allclose(react(x, 60, p), x, atol=1e-12)
        y = react(x, 60, replace(p, krel=.1))
        self.assertLess(y[0, 1], x[0, 1])
        self.assertGreater(reporter_product(y)[0], reporter_product(x)[0])

    def test_irreversible_turnover_has_one_reporter_hit_per_initial_free_catalyst(self):
        x = state(R=5, B=10, F=1)
        p = Parameters(kf=1, kh=0, turnover=True, krel=0)
        y = react(x, 60, p)
        self.assertAlmostEqual(y[0, 7], 1., places=8)
        self.assertAlmostEqual(y[0, 1], 4., places=8)
        self.assertEqual(y[0, 4], 0)
        self.assertAlmostEqual(reporter(y, [1]), 20., places=7)
        self.assertAlmostEqual(competent_inventory(y)[0], 1., places=9)

    def test_no_regeneration_ligation_sequesters_founder_with_inactive_product(self):
        x = state(A=5, B=10, F=1)
        p = Parameters(kf=0, ka=1, kh=0, turnover=True)
        y = react(x, 60, p, regeneration=False)
        self.assertAlmostEqual(y[0, 8], 1., places=8)
        self.assertAlmostEqual(y[0, 0], 4., places=8)
        self.assertEqual(y[0, 6], 0)
        self.assertAlmostEqual(competent_inventory(y)[0], 1., places=9)

    def test_precursor_ligation_produces_free_monomers(self):
        x = state(A=2, R=1, B=5)
        p = Parameters(kf=0, ka=0, kh=.01, krh=.02, turnover=True)
        for regeneration in (True, False):
            y = react(x, 60, p, regeneration)
            self.assertGreater(y[0, 3 if regeneration else 5], 0)
            self.assertGreater(y[0, 4], 0)
            self.assertEqual(y[0, 6:].sum(), 0)
            np.testing.assert_allclose(y@MOIETIES.T, x@MOIETIES.T, atol=1e-8)

    def test_zero_b_and_inactive_strands_disable_ligation(self):
        p = Parameters(turnover=True, kh=0)
        for x in (state(A=2, R=1, B=0, F=.2), state(A=2, R=1, B=5, P=2, D=3)):
            np.testing.assert_allclose(react(x, 60, p), x)

    def test_per_strand_inactivation_has_binomial_ff_products_without_release(self):
        p = Parameters(kf=0, kh=0, kd=.03, turnover=True)
        x = state(F=1, QFF=1, QFD=1, QFP=1)
        t = 20.
        q = np.exp(-p.kd*t)
        y = react(x, t, p, rtol=1e-10)
        expected = state(F=q, D=1-q, QFF=q*q, QFD=2*q*(1-q)+q,
                         QDD=(1-q)**2+(1-q), QFP=q, QDP=1-q)
        np.testing.assert_allclose(y, expected, atol=1e-9)
        self.assertAlmostEqual(competent_inventory(y)[0], 5*q, places=8)

    def test_no_regeneration_total_competence_follows_uniform_hazard(self):
        times = np.array([0, 1, 15, 60])
        for p in (self.p, replace(self.p, turnover=False), replace(self.p, kbind=100, krel=.001)):
            y = react(self.x, 60, p, regeneration=False, times=times)
            np.testing.assert_allclose(competent_inventory(y)[:, 0],
                                       competent_inventory(self.x)[0]*np.exp(-p.kd*times), atol=1e-7)

    def test_binding_is_invariant_under_strand_label_permutation(self):
        p = replace(self.p, kf=0, ka=0, kh=0, krh=0, kd=0)
        y = react(self.x, 20, p)
        for permutation in ([0, 1, 2, 3, 5, 4, 6, 8, 7, 11, 10, 9],
                            [0, 1, 2, 5, 4, 3, 9, 10, 8, 6, 7, 11]):
            permuted = react(self.x[:, permutation], 20, p)
            np.testing.assert_allclose(permuted, y[:, permutation], atol=1e-8)

    def test_page_counts_every_bound_reporter_strand_and_uses_weighted_amounts(self):
        x = state(R=2, P=1, QFP=2, QDP=1, QPP=2)
        self.assertEqual(reporter_product(x)[0], 8.)
        self.assertEqual(reporter(x, [1]), 80.)
        joined = np.vstack((x, state(R=30)))
        self.assertAlmostEqual(reporter(joined, [.75, .25]), 40.)
        self.assertIs(type(reporter(x, [1])), float)
        self.assertEqual(reporter(state(), [1]), 0.)
        p = replace(self.p, kf=0, ka=0, kh=0, krh=0)
        self.assertAlmostEqual(reporter(react(x, 60, p), [1]), 80., places=8)

    def test_initial_equilibrium_conserves_and_balances_all_pairs(self):
        p = replace(self.p, equilibrated=True)
        x = np.vstack((self.x, state(F=1), state(), state(D=2, P=3)))
        y = initial_complexes(x, p)
        np.testing.assert_allclose(y@MOIETIES.T, x@MOIETIES.T, atol=1e-12)
        free = y[:, 3:6]
        f, product, inactive = free.T
        forward = p.kbind*np.array([.5*f*f, f*product, f*inactive,
                                   .5*inactive*inactive, inactive*product, .5*product*product]).T
        np.testing.assert_allclose(forward, p.krel*y[:, 6:], atol=1e-12)
        np.testing.assert_allclose(initial_complexes(y, p), y, atol=1e-12)
        p = replace(p, kf=0, ka=0, kh=0, krh=0, kd=0)
        np.testing.assert_allclose(react(y, 60, p), y, atol=1e-9)
        self.assertGreater(y[1, 6], 0)
        self.assertAlmostEqual(y[1, 3]+p.kbind/p.krel*y[1, 3]**2, 1.)
        np.testing.assert_allclose(fresh(p), fresh(replace(p, equilibrated=False)))

    def test_seed_is_equilibrated_once_without_reequilibration_after_transport(self):
        p = replace(self.p, equilibrated=True, mixing=0)
        x, w = initial(2, p)
        self.assertLess(x[0, 3], 2.)
        self.assertAlmostEqual(competent_inventory(x)[0], 2.)
        y, _, _ = exchange(x, w, p, 3)
        np.testing.assert_allclose(y, .55*x, atol=1e-12)
        self.assertGreater(np.max(np.abs(initial_complexes(y, p)-y)), .01)

    def test_fast_release_limit_matches_instantaneous_baseline(self):
        p = Parameters(kf=.1, ka=.2, kh=.001, krh=.003, kd=.02)
        seeds, hypers = [0, .5, 2, .2], [5, 0, 0, 2]
        baseline = bulk_curves(p, seeds, hypers)
        fast = bulk_curves(replace(p, turnover=True, krel=1e5), seeds, hypers)
        np.testing.assert_allclose(fast, baseline, atol=5e-4, rtol=1e-5)

    def test_zero_rebinding_only_releases_existing_complexes_without_ligation(self):
        p = Parameters(kf=0, kh=0, turnover=True, krel=.2)
        x = self.x.copy()
        y = react(x, 10, p)
        np.testing.assert_allclose(y[:, 6:], x[:, 6:]*np.exp(-2), atol=1e-8)
        np.testing.assert_allclose(dissociate_complexes(y), dissociate_complexes(x), atol=1e-8)
        free = dissociate_complexes(x)
        np.testing.assert_allclose(react(free, 10, p), free, atol=1e-12)

    def test_saturation_and_default_ka(self):
        x = state(A=2, R=1, B=1e12, F=.2)
        p = Parameters(kf=.1, kh=.001, krh=.003)
        va, vr = rates(x, p)
        self.assertAlmostEqual(va[0], .1*.2*2+.001*4, places=10)
        self.assertAlmostEqual(vr[0], .1*.2+.003*2, places=10)
        np.testing.assert_allclose(rates(x, p), rates(x, replace(p, ka=.1)))

    def test_saved_prior_baseline_equivalence(self):
        p = Parameters(kf=1.5191726905179304, kh=.0003697516065118584, kb=99.99999973874252)
        expected = [[0, .0007120556382792167, .003927462720972346, .012684238255465472, .03370191930406673],
                    [0, 4.3349684307212275, 67.00967324833181, 74.18776403949185, 74.90397571685995],
                    [0, 48.02348231855159, 68.2848769535631, 79.08118336379185, 85.57320821365938],
                    [0, 97.7817255640697, 99.86761167049542, 99.99179826856198, 99.99949073107722]]
        np.testing.assert_allclose(bulk_curves(p, [0, 0, .5, 5], [.5, 5, 0, 0]), expected, atol=2e-5, rtol=2e-6)

    def test_batched_matches_separate_and_tolerance_refinement(self):
        seeds, hypers = [0, .1, 1, 0], [.5, 0, 0, 5]
        for p in (self.p, replace(self.p, kbind=100, krel=.001), replace(self.p, equilibrated=True)):
            batch = bulk_curves(p, seeds, hypers)
            separate = np.array([bulk_curve(p, f, a) for f, a in zip(seeds, hypers)])
            fine = bulk_curves(p, seeds, hypers, rtol=1e-10)
            np.testing.assert_allclose(batch, separate, atol=3e-5, rtol=1e-5)
            np.testing.assert_allclose(batch, fine, atol=3e-5, rtol=1e-5)
            coarse = react(self.x, 60, p, times=[0, 1, 15, 60])
            fine = react(self.x, 60, p, rtol=1e-10, times=[0, 1, 15, 60])
            np.testing.assert_allclose(coarse, fine, atol=2e-7, rtol=1e-5)

    def test_transport_preserves_volume_and_retains_same_weighted_inventory(self):
        x = np.vstack((self.x, self.x*2))
        w = np.array([.25, .75])
        for transport in ("fractional", "contact"):
            for loss in ("uniform", "all_or_none"):
                p = replace(self.p, transport=transport, loss=loss)
                y, v, lost = exchange(x, w, p, 3)
                np.testing.assert_allclose(v@y, (w@x)*.55, atol=1e-12)
                np.testing.assert_allclose(v@y+lost, w@x, atol=1e-12)
                self.assertAlmostEqual(v.sum(), 1)
                self.assertTrue(np.all(v >= 0))
        np.testing.assert_allclose(x, np.vstack((self.x, self.x*2)))

    def test_all_or_none_retains_survivor_concentration_and_merges_empty_cohorts(self):
        p = replace(self.p, mixing=0, loss="all_or_none")
        x, w, _ = exchange(self.x, [1], p, 30)
        self.assertEqual(len(w), 2)
        np.testing.assert_equal(x[0], self.x[0])
        np.testing.assert_equal(x[1], 0)
        self.assertAlmostEqual(w[0], .55**10)
        self.assertAlmostEqual(w[1], 1-.55**10)

    def test_loss_closures_have_same_inventory_but_different_kinetics(self):
        for transport in ("fractional", "contact"):
            p = replace(self.p, transport=transport, mixing=.4)
            a = single_cycle(p, 2, 3)
            b = single_cycle(replace(p, loss="all_or_none"), 2, 3)
            self.assertGreater(abs(a-b), .01)

    def test_reset_preserves_page_competence_moieties_and_event_loss(self):
        reset = dissociate_complexes(self.x)
        np.testing.assert_allclose(reset@MOIETIES.T, self.x@MOIETIES.T)
        np.testing.assert_allclose(competent_inventory(reset), competent_inventory(self.x))
        self.assertEqual(reporter(reset, [1]), reporter(self.x, [1]))
        self.assertEqual(reset[:, 6:].sum(), 0)
        for loss in ("uniform", "all_or_none"):
            p = replace(self.p, loss=loss, complex_reset=True)
            y, w, lost = exchange(self.x, [1], p, 3)
            self.assertEqual(y[:, 6:].sum(), 0)
            np.testing.assert_allclose(MOIETIES@(w@y), .55*(MOIETIES@self.x[0]), atol=1e-12)
            np.testing.assert_allclose(MOIETIES@(w@y+lost), MOIETIES@self.x[0], atol=1e-12)
            self.assertAlmostEqual(reporter(y, w), reporter(self.x, [1]))

    def test_mixing_limits_and_zero_exchange(self):
        for mixing in (0, 1):
            for loss in ("uniform", "all_or_none"):
                p = replace(self.p, mixing=mixing, loss=loss)
                self.assertAlmostEqual(single_cycle(p, 1, 3),
                                       single_cycle(replace(p, transport="contact"), 1, 3), places=7)
                if mixing == 0:
                    self.assertEqual(single_cycle(p, 1, 3), 0)
        y, w, lost = exchange(self.x, [1], replace(self.p, complex_reset=True), 0)
        np.testing.assert_equal(y, self.x)
        np.testing.assert_equal(w, [1])
        np.testing.assert_equal(lost, 0)

    def test_serial_founder_total_and_moiety_ledger(self):
        for transport in ("fractional", "contact"):
            for loss in ("uniform", "all_or_none"):
                for reset in (False, True):
                    p = replace(self.p, transport=transport, loss=loss, complex_reset=reset,
                                equilibrated=True)
                    rows = serial(p, 2, generations=4, regeneration=False)
                    initial_source = np.array(rows[0]["source_moiety_uM"])
                    per_feed = MOIETIES@(.25*fresh(p).sum(axis=0))
                    for row in rows:
                        g = row["generation"]
                        expected = 2/3 if g == 0 else 2/3*.55**g*.5**(g-1)*np.exp(-60*p.kd*g)
                        self.assertAlmostEqual(row["competent_total_model_uM"], expected, places=8)
                        self.assertAlmostEqual(row["founder_competent_model_uM"], expected, places=12)
                        self.assertLess(row["newly_generated_competent_model_uM"], 1e-8)
                        self.assertLess(row["moiety_balance_max_error_uM"], 1e-7)
                        np.testing.assert_allclose(row["source_moiety_uM"], initial_source+max(0, g-1)*per_feed)
                        self.assertTrue(0 <= row["yield_percent"] <= 100)
                        self.assertLessEqual(row["F_uM"], row["competent_total_model_uM"])

    def test_initial_state_and_zero_duration(self):
        x, w = initial(1, self.p)
        self.assertEqual(x.shape, (3, 12))
        self.assertAlmostEqual((w@x)[1], 2.5/3)
        np.testing.assert_equal(react(x, 0, self.p), x)
        np.testing.assert_equal(react(x, 0, self.p, times=[0]), x[None])

    def test_invalid_parameters_and_inputs(self):
        for changes in ({"kf": -1}, {"kh": np.nan}, {"ka": -1}, {"kb": 0}, {"kd": np.inf},
                        {"kbind": -1}, {"krel": -1}, {"mixing": np.nan}, {"mixing": 2},
                        {"retention_f": 0}, {"retention_fragments": np.inf}, {"retention_f": .8},
                        {"transport": "bad"}, {"loss": "bad"}, {"complex_reset": 1},
                        {"turnover": 1}, {"equilibrated": True, "kbind": 0}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(self.p, **changes)
        for x in (np.zeros((1, 11)), np.zeros((0, 12)), np.full((1, 12), -1.), np.full((1, 12), np.nan)):
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
