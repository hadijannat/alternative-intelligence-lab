import unittest

from openpyxl import Workbook

from analysis import POTENTIAL, RATE, RESCUE_HEADERS, analyze, checked_bytes, deposition_rows, ion_addition_response


class SourceAnalysisTests(unittest.TestCase):
    def sheet(self):
        sheet = Workbook().active
        sheet.title = "Figure 1c"
        sheet.append([POTENTIAL, RATE])
        sheet.append([1.6, 0])
        sheet.append([1.7, 9.6])
        return sheet

    def test_units_and_panel_labels_fail_closed(self):
        for cell, value in [("A1", "Time (h)"), ("B1", "Deposition rate (mg cm-2 min-1)")]:
            with self.subTest(cell=cell):
                sheet = self.sheet()
                sheet[cell] = value
                with self.assertRaises(ValueError):
                    deposition_rows(sheet)
        sheet = self.sheet()
        sheet.title = "Figure 2e"
        with self.assertRaises(ValueError):
            deposition_rows(sheet)

    def test_invalid_numeric_data_rejected(self):
        for cell, value in [("B3", None), ("B3", True), ("B3", "9.6"), ("B3", float("nan")),
                            ("B3", float("inf")), ("B3", -1), ("A3", 1.6), ("A3", 1.5)]:
            with self.subTest(cell=cell, value=value):
                sheet = self.sheet()
                sheet[cell] = value
                with self.assertRaises(ValueError):
                    deposition_rows(sheet)

    def test_zero_and_missing_uncertainty_are_distinct(self):
        row = deposition_rows(self.sheet())[0]
        self.assertEqual(row["deposition_rate_ng_cm-2_min-1"], 0)
        self.assertIsNone(row["uncertainty"])
        self.assertIsNone(row["mean"])
        self.assertEqual(row["source_cells"], ["A2", "B2"])

    def test_modified_source_rejected(self):
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            checked_bytes(b"changed source", "article.xml")

    def rescue_sheet(self):
        sheet = Workbook().active
        sheet.title = "Figure 2e"
        for cell, value in RESCUE_HEADERS.items():
            sheet[cell] = value
        sheet.append([0.5, 1.7, 0.5, 1.6, 0.5, 1.8])
        sheet.append([2, 1.72, 2, 1.57, 2, 1.71])
        return sheet

    def test_ion_response_uses_exact_shared_times(self):
        result = ion_addition_response(self.rescue_sheet())
        self.assertEqual(result["common_endpoint_time_h"], 2)
        self.assertEqual([r["endpoint_minus_reference_mV"] for r in result["responses"]], [20, -30, -90])
        self.assertEqual(result["responses"][2]["reference"]["source_cells"], ["E3", "F3"])

    def test_ion_response_rejects_invalid_labels_values_or_unshared_times(self):
        for cell, value in [("E1", "Fe(III)"), ("B2", "Potential (mV vs. RHE)"),
                            ("F4", float("nan")), ("C3", 0.49), ("E4", 1.9), ("A4", 0.5)]:
            with self.subTest(cell=cell, value=value):
                sheet = self.rescue_sheet()
                sheet[cell] = value
                with self.assertRaises(ValueError):
                    ion_addition_response(sheet)

    def test_actual_pinned_source_and_unavailable_comparator(self):
        result, inventory = analyze()
        rows = result["fig1c"]["observations"]
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[-1]["source_cells"], ["A13", "B13"])
        self.assertEqual(rows[-1]["deposition_rate_ng_cm-2_min-1"], 16)
        self.assertEqual(rows[8]["potential_V_vs_RHE"], 1.7)
        self.assertEqual(rows[8]["deposition_rate_ng_cm-2_min-1"], 9.6)
        self.assertEqual(len(inventory["workbooks"]), 5)
        self.assertIsNone(result["matched_Co_assisted_vs_unassisted_EQCM"]["common_potential_comparisons"])
        self.assertEqual(result["source_label_conflict"]["workbook_label_verbatim"], "with 50 mM Fe(II)")
        self.assertFalse(result["target_renewal_demonstrated"])
        self.assertEqual(result["separate_text_observations"]["no_added_Fe_film_loss"]["net_loss_nmol_cm-2"], 5)
        response = result["fig2e"]["descriptive_potential_response"]
        self.assertEqual(response["common_endpoint_time_h"], 2)
        self.assertEqual([r["endpoint_minus_reference_mV"] for r in response["responses"]], [20.25, -31.47, -88.13])
        self.assertEqual(response["responses"][2]["endpoint"]["source_cells"], ["E7202", "F7202"])


if __name__ == "__main__":
    unittest.main()
