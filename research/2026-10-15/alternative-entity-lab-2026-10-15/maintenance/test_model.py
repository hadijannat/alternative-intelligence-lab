from dataclasses import replace
import math
import random
import unittest

from maintenance.model import Params, debit_work, initialise, step, validate


class MaintenanceTests(unittest.TestCase):
    def test_decay_matches_analytic_solution(self):
        state = initialise(fuel=0, structure=2, energy=0)
        for _ in range(100):
            state = step(state, 0, 0, 0.1).state
        self.assertAlmostEqual(state.structure, 2 * math.exp(-0.04 * 10), places=12)
        self.assertAlmostEqual(state.waste, 2 - state.structure, places=12)

    def test_finite_fuel_and_energy_cannot_be_overspent(self):
        state = initialise(fuel=0.4, structure=1, energy=0.2)
        params = Params(decay_rate=0, energy_leak_rate=0, renewal=False)
        state = step(state, 0, 100, 10, params).state
        self.assertEqual(state.fuel, 0)
        self.assertAlmostEqual(state.spent, 1)
        state, paid = debit_work(state, 100)
        self.assertEqual(paid, 0)
        self.assertEqual(state.structure, 1)
        self.assertAlmostEqual(state.waste, 0.4)

    def test_zero_fuel_zero_energy_never_renews_or_works(self):
        state = initialise(fuel=0, structure=1, energy=0)
        result = step(state, 0, 10, 1)
        self.assertEqual(result.actual_work, 0)
        self.assertEqual(result.renewed, 0)
        self.assertEqual(result.state.new_structure, 0)

    def test_random_finite_reservoir_accounting(self):
        rng = random.Random(731)
        state = initialise()
        reservoir = initial_reservoir = 3.0
        total_paid = 0.0
        for _ in range(1000):
            offered = min(reservoir, rng.random() / 50)
            result = step(state, offered, rng.random(), 0.1)
            state = result.state
            reservoir -= result.accepted_influx
            total_paid += result.actual_work
            validate(state)
            self.assertAlmostEqual(reservoir + state.fed_total, initial_reservoir, places=10)
            self.assertAlmostEqual(state.energy_generated, 2 * (0.5 + state.fed_total - state.fuel), places=10)
        self.assertAlmostEqual(total_paid, state.spent, places=10)

    def test_zero_structure_cannot_catalyse(self):
        result = step(initialise(fuel=2, structure=0, energy=0), 1, 1, 10)
        self.assertEqual(result.converted, 0)
        self.assertEqual(result.state.fuel, 3)
        self.assertEqual(result.state.structure, 0)

    def test_work_debit_is_immutable(self):
        state = initialise()
        updated, paid = debit_work(state, 0.1)
        self.assertEqual(state.energy, 0.25)
        self.assertEqual(paid, 0.1)
        self.assertAlmostEqual(updated.energy, 0.15)

    def test_renewal_requires_available_work(self):
        params = Params(conversion_rate=1, structure_yield=1, energy_yield=0, renewal_energy_cost=1, decay_rate=0)
        result = step(initialise(fuel=1, structure=1, energy=0), 0, 0, 1, params)
        self.assertEqual(result.renewed, 0)
        self.assertEqual(result.state.waste, 1)

    def test_energy_limited_fractional_renewal_stays_nonnegative(self):
        rng = random.Random(1729)
        for _ in range(250):
            params = Params(conversion_rate=10**rng.uniform(-4, 3), structure_yield=rng.random(),
                            energy_yield=10**rng.uniform(-4, 3), renewal_energy_cost=10**rng.uniform(-4, 3),
                            decay_rate=rng.random(), energy_leak_rate=rng.random())
            state = initialise(fuel=rng.random() * 10, structure=rng.random() * 10, energy=rng.random())
            result = step(state, rng.random(), rng.random(), rng.random(), params)
            validate(result.state)
            self.assertGreaterEqual(result.state.energy, 0)

    def test_rejects_invalid_inputs_and_broken_ledgers(self):
        for value in (-1, float("nan"), float("inf"), True, "1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    initialise(fuel=value)
                with self.assertRaises(ValueError):
                    step(initialise(), value, 0, 0.1)
                with self.assertRaises(ValueError):
                    debit_work(initialise(), value)
        for dt in (0, -1, float("nan")):
            with self.assertRaises(ValueError):
                step(initialise(), 0, 0, dt)
        with self.assertRaises(ValueError):
            Params(structure_yield=1.01)
        with self.assertRaises(ValueError):
            Params(renewal=1)
        with self.assertRaises(ValueError):
            validate(replace(initialise(), fuel=100))


if __name__ == "__main__":
    unittest.main()
