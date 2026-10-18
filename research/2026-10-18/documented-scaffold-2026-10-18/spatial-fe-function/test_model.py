import unittest
import io
from fractions import Fraction
from pathlib import Path

from analyze import allocation, feasible_bounds


class IdentifiabilityTests(unittest.TestCase):
    def test_attainable_bounds_and_same_observations(self):
        values = tuple(map(Fraction, ("0.7", "0.3", "0.4", "10", "1", "0.2")))
        lo, hi, lower, upper = feasible_bounds(*values)
        self.assertEqual((lo, hi, lower, upper), tuple(map(Fraction, ("0.1", "0.4", "1.3", "4"))))
        worlds = [allocation(*values, x) for x in (lo, hi)]
        self.assertEqual(worlds[0]["total_current"], worlds[1]["total_current"])
        self.assertEqual(worlds[0]["total_current"], 7.5)
        self.assertNotEqual(worlds[0]["new_current"], worlds[1]["new_current"])

    def test_reversed_site_competence_and_equal_control(self):
        self.assertEqual(feasible_bounds(1, 1, 1, 1, 10)[2:], (1, 10))
        self.assertEqual(feasible_bounds(1, 1, 1, 3, 3)[2:], (3, 3))

    def test_invalid_inputs_and_allocations(self):
        for position in range(6):
            for bad in (-1, float("nan"), float("inf"), -float("inf")):
                values = [1, 1, 1, 10, 1, 0.2]
                values[position] = bad
                with self.subTest(position=position, bad=bad), self.assertRaises(ValueError):
                    feasible_bounds(*values)
        with self.assertRaises(ValueError):
            feasible_bounds(0, 0, 1, 1, 1)
        for bad in (-0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(allocation=bad), self.assertRaises(ValueError):
                allocation(1, 1, 1, 10, 1, 0.2, bad)


if __name__ == "__main__":
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(IdentifiabilityTests))
    output = stream.getvalue()
    path = Path(__file__).resolve().parent / "results" / "test-output.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text(output)
    print(output, end="")
    raise SystemExit(0 if result.wasSuccessful() else 1)
