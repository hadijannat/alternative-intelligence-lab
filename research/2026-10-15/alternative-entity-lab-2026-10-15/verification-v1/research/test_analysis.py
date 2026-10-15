import math
import unittest

from analyze_data import finite, halfpeak_time, interpolate, summary


class AnalysisChecks(unittest.TestCase):
    def test_interpolated_peak_crossing(self):
        self.assertEqual(halfpeak_time([(0, 2), (1, 4), (3, 0)]), 2)
        self.assertIsNone(halfpeak_time([(0, 4), (1, 3)]))

    def test_reject_invalid_order(self):
        with self.assertRaises(ValueError):
            halfpeak_time([(0, 2), (0, 1)])

    def test_reject_nonfinite(self):
        for value in [math.nan, math.inf, -math.inf]:
            with self.assertRaises(ValueError):
                finite(value)

    def test_sample_summary(self):
        result = summary([2, 4])
        self.assertEqual(result["mean"], 3)
        self.assertAlmostEqual(result["sample_sd"], math.sqrt(2))

    def test_interpolation_never_extrapolates(self):
        self.assertEqual(interpolate([(0, 4), (2, 2)], 1), 3)
        with self.assertRaises(ValueError):
            interpolate([(0, 4), (2, 2)], 3)


if __name__ == "__main__":
    unittest.main()
