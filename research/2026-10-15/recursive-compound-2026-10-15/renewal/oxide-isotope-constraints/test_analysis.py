import csv
import shutil
import tempfile
import unittest
from pathlib import Path

import analysis


class SourceConstraints(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "raw").mkdir()
        shutil.copyfile(analysis.BASE / "raw/ja905166c_si_001.pdf", self.base / "raw/ja905166c_si_001.pdf")
        shutil.copyfile(analysis.BASE / "rates.csv", self.base / "rates.csv")

    def mutate(self, index, **changes):
        rows = analysis.load_rows(analysis.BASE / "rates.csv")
        rows[index].update(changes)
        with (self.base / "rates.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=analysis.FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_complete_table_and_matched_ratios(self):
        result = analysis.analyze(self.base)
        self.assertEqual((result["row_count"], result["reported_rate_count"], result["not_reported_count"]), (17, 74, 42))
        self.assertEqual(result["reported_rate_count_by_site"], dict(zip("ABCDEFG", (3, 3, 12, 13, 9, 17, 17))))
        self.assertEqual([r["reported_log_difference"] for r in result["F_over_A"]], [2.98, 3.18, 3.33])
        self.assertEqual([r["reported_log_difference"] for r in result["D_over_E"]], [3.97, 4.03])
        self.assertAlmostEqual(result["F_over_A"][0]["conditional_point_ratio_if_base10"], 954.9925860214359)
        self.assertEqual([r["concentration_mM"] for r in result["D_over_E"]], [2.81, 2.81])

    def test_endpoint_and_claim_boundaries(self):
        result = analysis.analyze(self.base)
        self.assertEqual(result["site_endpoints"]["A"], "molecular_transformation")
        self.assertTrue(all(r["denominator_endpoint"] == "molecular_transformation" for r in result["F_over_A"]))
        self.assertTrue(all(r["confidence_interval"] is None for r in result["F_over_A"] + result["D_over_E"]))
        self.assertIsNone(result["uncertainty"]["confidence_level"])
        self.assertFalse(result["log_base"]["source_explicitly_defines_base"])
        self.assertEqual(result["log_base"]["arithmetic_assumption"], 10)
        self.assertTrue(all(value in (False, 0) for value in result["inference_limits"].values()))

    def test_changed_primary_source_rejected(self):
        with (self.base / "raw/ja905166c_si_001.pdf").open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(ValueError, "SI bytes changed"):
            analysis.analyze(self.base)

    def test_changed_reported_value_rejected(self):
        self.mutate(0, F_log_k="-2.44")
        with self.assertRaisesRegex(ValueError, "transcription changed"):
            analysis.analyze(self.base)

    def test_invalid_units_values_and_uncertainties_rejected(self):
        for change in ({"rate_unit": "min^-1"}, {"log_base": "e"}, {"F_log_k": "NaN"}, {"F_uncertainty": "-0.1"}, {"concentration_mM": "0"}, {"pH": "inf"}):
            with self.subTest(change=change):
                self.mutate(0, **change)
                with self.assertRaises(ValueError):
                    analysis.load_rows(self.base / "rates.csv")

    def test_censored_rate_cannot_be_zero_or_uncensored(self):
        for change in ({"D_log_k": "0"}, {"D_status": "reported", "D_log_k": "0", "D_uncertainty": "0"}, {"D_status": "not_reported"}):
            with self.subTest(change=change):
                self.mutate(0, **change)
                with self.assertRaises(ValueError):
                    analysis.load_rows(self.base / "rates.csv")
        rows = analysis.load_rows(analysis.BASE / "rates.csv")
        with self.assertRaises(ValueError):
            analysis.ratio(rows[0], "D", "E")
        with self.assertRaises(ValueError):
            analysis.ratio(rows[3], "F", "A")

    def test_missing_rows_and_missing_values_rejected(self):
        self.mutate(3, A_log_k="0")
        with self.assertRaises(ValueError):
            analysis.load_rows(self.base / "rates.csv")
        lines = (analysis.BASE / "rates.csv").read_text().splitlines()
        (self.base / "rates.csv").write_text("\n".join(lines[:-1]) + "\n")
        with self.assertRaisesRegex(ValueError, "17 source rows"):
            analysis.load_rows(self.base / "rates.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
