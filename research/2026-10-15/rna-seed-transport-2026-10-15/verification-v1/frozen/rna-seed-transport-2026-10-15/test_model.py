"""Synthetic chemistry, transport, observation and serial-accounting checks."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

import numpy as np

from model import (CHEMISTRY, CHEMISTRY_SOURCE, CHEMISTRY_SOURCE_SHA256,
                   MOIETIES, NAMES, exchange, feed, fresh, initial, permeability,
                   react, reporter, serial, single_cycle)

ROOT = Path(__file__).resolve().parent.parent


def prior_model():
    spec = importlib.util.spec_from_file_location("seed_test_prior_model",
                                                 ROOT / "rna-turnover-tests-2026-10-15/model.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def state(**values):
    x = np.zeros((1, len(NAMES)))
    for name, value in values.items():
        x[0, NAMES.index(name)] = value
    return x


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.x = np.array([[2, 1, 5, .2, .1, .3, .15],
                           [1, 2, 3, .4, .2, .1, .1],
                           [3, 1, 2, .1, .3, .5, .02]])
        self.e = self.x[::-1] * .2
        self.w = np.array([.2, .3, .5])

    def test_chemistry_constants_and_source_hash_are_frozen(self):
        raw = (ROOT / CHEMISTRY_SOURCE).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), CHEMISTRY_SOURCE_SHA256)
        old_parameters = json.loads(raw)["parameters"]
        for name, value in CHEMISTRY.items():
            self.assertEqual(value, old_parameters[name])
        self.assertFalse(old_parameters["turnover"])
        self.assertEqual(old_parameters["krel"], 0)
        self.assertEqual(old_parameters["kbind"], 0)

    def test_chemistry_conserves_three_moieties_and_positivity(self):
        y = react(self.x, 60, rtol=1e-10)
        np.testing.assert_allclose(y @ MOIETIES.T, self.x @ MOIETIES.T, atol=1e-9)
        self.assertTrue(np.all(y >= 0))
        self.assertTrue(np.all(y[:, 6] <= y[:, 3]+1e-10))

    def test_prior_six_species_chemistry_equivalence(self):
        old = prior_model()
        x12 = np.column_stack((self.x[:, :6], np.zeros((len(self.x), 6))))
        for minutes in (0, 15, 60):
            expected = old.react(x12, minutes, old.Parameters(**CHEMISTRY), rtol=1e-10)
            np.testing.assert_allclose(react(self.x, minutes, rtol=1e-10)[:, :6],
                                       expected[:, :6], atol=2e-8, rtol=2e-8)

    def test_founder_is_passive_competent_tag_without_resynthesis(self):
        for x in (state(A=2, R=1, B=5, F=.2, H=.2), state(F=.2, H=.2)):
            y = react(x, 60, rtol=1e-10)
            self.assertAlmostEqual(y[0, 6], .2*np.exp(-CHEMISTRY["kd"]*60), places=13)
            self.assertGreaterEqual(y[0, 3]+1e-10, y[0, 6])
        self.assertGreater(react(state(A=2, B=5), 60)[0, 3], 0)
        self.assertEqual(react(state(A=2, B=5), 60)[0, 6], 0)

    def test_zero_b_blocks_ligation_and_preserves_reporter(self):
        x = state(A=2, R=3, F=1, P=.5, H=.4)
        y = react(x, 60, rtol=1e-10)
        np.testing.assert_allclose(y[:, [0, 1, 2, 4]], x[:, [0, 1, 2, 4]], atol=1e-12)
        self.assertAlmostEqual(y[0, 3]+y[0, 5], 1, places=10)

    def test_finite_exchange_conserves_every_species_and_tag(self):
        for family, params, e in (("bath", {"nu": 1}, np.tile(self.w@self.e, (3, 1))),
                                  ("bath", {"nu": 30}, np.tile(self.w@self.e, (3, 1))),
                                  ("patch", {"nu": 2, "diffusion": .3}, self.e)):
            y, z, lost = exchange(self.x, e, self.w, family, params, 3)
            np.testing.assert_allclose(self.w@y+params["nu"]*(self.w@z),
                                       self.w@self.x+params["nu"]*(self.w@e), atol=1e-12)
            self.assertTrue(np.all(y >= 0) and np.all(z >= 0))
            self.assertTrue(np.all(y[:, 6] <= y[:, 3]+1e-12))
            np.testing.assert_array_equal(lost, np.zeros(len(NAMES)))

    def test_uniform_initial_passive_tracer_has_55_percent_inside_after_three_ft(self):
        x = np.tile(state(A=1), (3, 1))
        for nu in (1, 2, 30):
            self.assertGreater(permeability(nu), 0)
            for family, params in (("bath", {"nu": nu}),
                                   ("patch", {"nu": nu, "diffusion": 0}),
                                   ("patch", {"nu": nu, "diffusion": 5})):
                y, z, _ = exchange(x, np.zeros_like(x), self.w, family, params, 3)
                self.assertAlmostEqual((self.w@y)[0], .55, places=12)
                self.assertAlmostEqual(nu*(self.w@z)[0], .45, places=12)

    def test_retention_is_not_reset_to_55_percent_at_later_cycles(self):
        x = state(A=1)
        y, e, _ = exchange(x, np.zeros_like(x), [1], "bath", {"nu": 2}, 3)
        z, _, _ = exchange(y, e, [1], "bath", {"nu": 2}, 3)
        self.assertGreater(z[0, 0], .55*y[0, 0])

    def test_ft_map_semigroup_keeps_exterior_between_cycles(self):
        for family, params in (("bath", {"nu": 2}),
                               ("patch", {"nu": 2, "diffusion": .3})):
            e = np.tile(self.w@self.e, (3, 1))
            once_x, once_e, _ = exchange(self.x, e, self.w, family, params, 3)
            step_x, step_e = self.x.copy(), e.copy()
            for _ in range(3):
                step_x, step_e, _ = exchange(step_x, step_e, self.w, family, params, 1)
            np.testing.assert_allclose(step_x, once_x, atol=1e-12)
            np.testing.assert_allclose(step_e, once_e, atol=1e-12)

    def test_zero_permeability_and_zero_time_preserve_inside(self):
        for family, params in (("bath", {"nu": 2}),
                               ("patch", {"nu": 2, "diffusion": .3})):
            e = np.tile(self.w@self.e, (3, 1))
            y, z, _ = exchange(self.x, e, self.w, family, params, 3, kappa_override=0)
            np.testing.assert_allclose(y, self.x, atol=1e-12)
            np.testing.assert_allclose(z, e, atol=1e-12)
            y, z, _ = exchange(self.x, e, self.w, family, params, 0)
            np.testing.assert_array_equal(y, self.x)
            np.testing.assert_array_equal(z, e)

    def test_exterior_rna_can_reenter_empty_inside(self):
        x = state()
        e = state(F=1, H=.5, R=1)
        for family, params in (("bath", {"nu": 2}),
                               ("patch", {"nu": 2, "diffusion": .3})):
            y, z, _ = exchange(x, e, [1], family, params, 1)
            self.assertGreater(y[0, 3], 0)
            self.assertGreater(y[0, 6], 0)
            self.assertLess(z[0, 3], e[0, 3])

    def test_zero_patch_diffusion_prevents_transfer_between_different_cohorts(self):
        x, e, w = initial(2)
        y, _, _ = exchange(x, e, w, "patch", {"nu": 2, "diffusion": 0}, 3)
        np.testing.assert_allclose(y, x*.55, atol=1e-12)
        self.assertEqual(reporter(react(y), w), 0)

    def test_fast_patch_diffusion_approaches_common_bath(self):
        e = np.tile(self.w@self.e, (3, 1))
        bath_x, bath_e, _ = exchange(self.x, e, self.w, "bath", {"nu": 2}, 3)
        patch_x, patch_e, _ = exchange(self.x, e, self.w, "patch",
                                      {"nu": 2, "diffusion": 1e6}, 3)
        np.testing.assert_allclose(patch_x, bath_x, atol=3e-7)
        np.testing.assert_allclose(patch_e, bath_e, atol=3e-7)

    def test_bath_relaxes_to_finite_volume_equilibrium(self):
        e = np.tile(self.w@self.e, (3, 1))
        y, z, _ = exchange(self.x, e, self.w, "bath", {"nu": 2}, 10000)
        expected = (self.w@self.x + 2*(self.w@e))/3
        np.testing.assert_allclose(y, np.tile(expected, (3, 1)), atol=1e-12)
        np.testing.assert_allclose(z, np.tile(expected, (3, 1)), atol=1e-12)

    def test_legacy_exactly_matches_prior_event_map(self):
        old = prior_model()
        x12 = np.column_stack((self.x[:, :6], np.zeros((len(self.x), 6))))
        for mixing in (0, .1, 1):
            for cycles in (0, 1, 3):
                y, e, lost = exchange(self.x, np.zeros_like(self.x), self.w,
                                      "legacy", {"mixing": mixing}, cycles)
                expected, weights, expected_lost = old.exchange(x12, self.w,
                                        old.Parameters(**CHEMISTRY, mixing=mixing), cycles)
                np.testing.assert_allclose(y[:, :6], expected[:, :6], atol=1e-12)
                np.testing.assert_allclose(lost[:6], expected_lost[:6], atol=1e-12)
                np.testing.assert_array_equal(e, np.zeros_like(e))
                np.testing.assert_array_equal(weights, self.w)

    def test_legacy_serial_matches_prior_baseline(self):
        old = prior_model()
        for seed in (0, 1, 2):
            expected = old.serial(old.Parameters(**CHEMISTRY, mixing=.17), seed, rtol=1e-10)
            actual = serial(seed, "legacy", {"mixing": .17}, rtol=1e-10)
            np.testing.assert_allclose([r["yield_percent"] for r in actual],
                                       [r["yield_percent"] for r in expected], atol=2e-7)
            np.testing.assert_allclose([r["founder_inside_uM"] for r in actual],
                                       [r["founder_competent_model_uM"] for r in expected], atol=1e-12)

    def test_feed_exactly_accounts_for_both_pools_and_source_cohorts(self):
        x, e, w, removed, added = feed(self.x, self.e, self.w, 2)
        np.testing.assert_allclose(removed, .5*(self.w@self.x+2*(self.w@self.e)))
        np.testing.assert_allclose(w@x+2*(w@e)+removed,
                                   self.w@self.x+2*(self.w@self.e)+added, atol=1e-12)
        np.testing.assert_array_equal(x[:3], self.x)
        np.testing.assert_array_equal(x[-2:], fresh())
        np.testing.assert_allclose(e, np.tile(.5*(self.w@self.e), (5, 1)))
        np.testing.assert_allclose(w, [.1, .15, .25, .25, .25])
        np.testing.assert_array_equal(added, [2.5, .625, 3.75, 0, 0, 0, 0])

    def test_page_is_pure_weighted_intracellular_observer(self):
        x = np.vstack((state(R=2, P=1), state(R=30)))
        original = x.copy()
        self.assertAlmostEqual(reporter(x, [.75, .25]), 100*.75/(.75*3+.25*30))
        np.testing.assert_array_equal(x, original)
        self.assertEqual(reporter(state(), [1]), 0)

    def test_single_cycle_inside_is_identical_across_exterior_sensitivities(self):
        for family, params in (("bath", {"nu": 2}),
                               ("patch", {"nu": 2, "diffusion": .3})):
            observations = [single_cycle(1, family, params, 3,
                             exterior_reactive=reactive, exterior_carried=carried)
                            for reactive in (False, True) for carried in (False, True)]
            for key in ("yield_percent", "inside_F_uM", "new_reporter_inside_uM"):
                self.assertEqual(len({row[key] for row in observations}), 1)
            self.assertEqual(observations[0]["new_reporter_outside_uM"], 0)
            self.assertGreater(observations[-1]["new_reporter_outside_uM"], 0)

    def test_discard_follows_measurement_and_changes_later_generation(self):
        carried = serial(1, "bath", {"nu": 2})
        discarded, stages = serial(1, "bath", {"nu": 2},
                                   exterior_carried=False, return_stages=True)
        self.assertEqual(carried[1]["yield_percent"], discarded[1]["yield_percent"])
        self.assertNotAlmostEqual(carried[2]["yield_percent"], discarded[2]["yield_percent"], places=4)
        g1 = [row for row in stages if row["generation"] == 1]
        self.assertEqual([r["stage"] for r in g1], ["exchange", "warm_start", "measurement", "discard"])
        self.assertGreater(g1[-2]["outside_F_uM"], 0)
        self.assertEqual(g1[-1]["outside_F_uM"], 0)
        self.assertEqual(g1[-1]["yield_percent"], g1[-2]["yield_percent"])

    def test_inert_exterior_preserves_founder_during_warm_and_still_homogenizes(self):
        _, stages = serial(2, "patch", {"nu": 2, "diffusion": .3}, generations=1,
                           exterior_reactive=False, return_stages=True)
        start, measured = stages[-2:]
        self.assertEqual(start["stage"], "warm_start")
        self.assertEqual(measured["outside_H_uM"], start["outside_H_uM"])
        self.assertEqual(measured["outside_F_uM"], start["outside_F_uM"])
        self.assertLess(measured["inside_H_uM"], start["inside_H_uM"])

    def test_serial_ledgers_balance_and_new_reporter_is_incremental(self):
        for family, params in (("legacy", {"mixing": .17}),
                               ("bath", {"nu": 2}),
                               ("patch", {"nu": 2, "diffusion": .3})):
            for reactive in (False, True):
                for carried in (False, True):
                    rows, stages = serial(2, family, params, exterior_reactive=reactive,
                                           exterior_carried=carried, return_stages=True)
                    self.assertEqual([r["generation"] for r in rows], list(range(8)))
                    self.assertEqual(rows[-1]["cohorts"], 15)
                    self.assertLess(max(r["moiety_balance_max_error_uM"] for r in stages), 1e-7)
                    for row in rows[1:]:
                        start = next(s for s in stages if s["generation"] == row["generation"]
                                     and s["stage"] == "warm_start")
                        self.assertAlmostEqual(row["new_reporter_inside_uM"],
                                               row["inside_P_uM"]-start["inside_P_uM"], places=12)
                        self.assertGreaterEqual(row["new_reporter_inside_uM"], -1e-12)
                        self.assertGreaterEqual(row["new_reporter_outside_uM"], -1e-12)

    def test_tighter_numerical_replay_preserves_predictions(self):
        for family, params in (("legacy", {"mixing": .17}),
                               ("bath", {"nu": 2}),
                               ("patch", {"nu": 2, "diffusion": .3})):
            coarse = serial(2, family, params)
            fine = serial(2, family, params, rtol=1e-10)
            for key in ("yield_percent", "competent_inside_uM", "competent_outside_uM"):
                np.testing.assert_allclose([r[key] for r in coarse], [r[key] for r in fine], atol=2e-6)

    def test_inputs_are_not_mutated(self):
        x, e, w = self.x.copy(), self.e.copy(), self.w.copy()
        react(x)
        exchange(x, e, w, "patch", {"nu": 2, "diffusion": .3}, 3)
        feed(x, e, w, 2)
        reporter(x, w)
        np.testing.assert_array_equal(x, self.x)
        np.testing.assert_array_equal(e, self.e)
        np.testing.assert_array_equal(w, self.w)

    def test_invalid_inputs_fail(self):
        bad_calls = [lambda: initial(-1), lambda: initial(np.nan), lambda: react(state(H=1)),
                     lambda: react(state(A=-1)), lambda: react(state(), -1),
                     lambda: react(state(), rtol=0), lambda: permeability(.9),
                     lambda: permeability(np.inf), lambda: reporter(self.x, [.2, .2, .2]),
                     lambda: serial(1, "bath", {"nu": 2}, generations=-1),
                     lambda: serial(1, "bath", {"nu": 2}, exterior_reactive=1),
                     lambda: serial(1, "bath", {"nu": 2}, return_stages=1),
                     lambda: serial(1, "bath", {"nu": 2}, generations=0, rtol=0),
                     lambda: single_cycle(1, "bath", {"nu": 2}, .5),
                     lambda: serial(1, "bath", {"nu": .9}),
                     lambda: serial(1, "patch", {"nu": 2, "diffusion": -1}),
                     lambda: serial(1, "legacy", {"mixing": 1.1}),
                     lambda: serial(1, "unknown", {}),
                     lambda: serial(1, "bath", {"nu": 2, "mixing": .1}),
                     lambda: exchange(self.x, self.e, self.w, "legacy", {"mixing": .1}, 1),
                     lambda: exchange(self.x, self.e[:1], self.w, "bath", {"nu": 2}, 1),
                     lambda: exchange(self.x, self.e, self.w, "patch", {"nu": 2, "diffusion": .3},
                                      1, kappa_override=-1),
                     lambda: feed(self.x, self.e, self.w, -1)]
        for call in bad_calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
