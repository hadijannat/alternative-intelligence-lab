import hashlib
import json
import math
import re
import statistics
from fractions import Fraction as F
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = "7fb77831963fcd4e25a5f62f454cbc8412525628f0e3286fa12f4f984b20f955"


def text(node):
    return " ".join("".join(node.itertext()).split())


def passage_bounds(rejection):
    # A conditional rounding envelope, not a source-reported error bar.
    return F(199 - 2 * rejection, 200), F(201 - 2 * rejection, 200)


def common_w_interval(te, v, w, te_ratio, v_ratio, ratio_halfwidth=F(0)):
    """Intersect W passage fractions required by Te/V/W ratios normalized W=3."""
    assert te_ratio > ratio_halfwidth and v_ratio > ratio_halfwidth
    low = max(w[0], te[0] / (te_ratio + ratio_halfwidth),
              3 * v[0] / (v_ratio + ratio_halfwidth))
    high = min(w[1], te[1] / (te_ratio - ratio_halfwidth),
               3 * v[1] / (v_ratio - ratio_halfwidth))
    return {"low_exact": str(low), "high_exact": str(high),
            "compatible_with_closed_envelope": low <= high}


def self_check():
    q = (F(1, 100), F(1, 100))
    assert common_w_interval(q, q, q, F(1), F(3))["compatible_with_closed_envelope"]
    assert not common_w_interval(q, q, q, F(20), F(3))["compatible_with_closed_envelope"]
    # Each separate ratio can fit some W, but they cannot share one W value.
    assert not common_w_interval((F(1), F(1)), (F(2), F(2)),
                                 (F(1), F(2)), F(1), F(3))["compatible_with_closed_envelope"]
    assert passage_bounds(99) == (F(1, 200), F(3, 200))
    return 4


def main():
    raw = (HERE / "raw/article.xml").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "Source changed"
    root = ET.fromstring(raw)
    tables, observations, ratios = [], [], []
    for number in (1, 2, 3):
        table = root.find(f".//table-wrap[@id='tbl{number}']")
        cells = [[text(c) for c in row.findall("td")]
                 for row in table.findall(".//tbody/tr")]
        assert len(cells) == 5
        tables.append({"source_id": f"tbl{number}", "title": text(table.find("caption")),
                       "headers": [text(c) for c in table.findall(".//thead/tr/th")],
                       "source_cells": cells, "conditions": text(table.find("table-wrap-foot"))})
        for index, row in enumerate(cells):
            item = {"source_table": number, "source_row": index + 1,
                    "retrospective": True, "target_compound_tested": False}
            if number < 3:
                item.update(membrane=row[0], concentration_mM=5,
                            structure="Lindqvist" if number == 1 else "Anderson-Evans",
                            cutoff_Da_source=row[1], pore_radius_nm_source=row[-1])
                elements = ("W", "V") if number == 1 else ("Te", "W", "V")
                item["elemental_rejection_percent"] = dict(zip(elements, map(int, row[2:-2])))
                item["permeate_flux_L_m2_h"] = int(row[-2])
            else:
                item.update(membrane="TS-80", concentration_mM=int(row[0]),
                            structure="Anderson-Evans",
                            elemental_rejection_percent=dict(zip(("Te", "W", "V"), map(int, row[1:4]))),
                            permeate_flux_L_m2_h=int(row[4]), permeate_ratio_Te_V_W_source=row[5])
                r = item["elemental_rejection_percent"]
                te, v, w = (passage_bounds(r[e]) for e in ("Te", "V", "W"))
                rt, rv, rw = map(F, row[5].split("/"))
                assert rw == 3
                ratios.append({"concentration_mM": int(row[0]), "source_ratio": row[5],
                    "central_predicted_ratio_W_normalized_to_3":
                        [str(F(100-r["Te"], 100-r["W"])),
                         str(3*F(100-r["V"], 100-r["W"])), "3"],
                    "Te_ratio_closed_envelope": [str(te[0]/w[1]), str(te[1]/w[0])],
                    "V_ratio_closed_envelope": [str(3*v[0]/w[1]), str(3*v[1]/w[0])],
                    "joint_exact_reported_ratio": common_w_interval(te, v, w, rt, rv),
                    "joint_ratio_also_rounded_half_unit": common_w_interval(te, v, w, rt, rv, F(1, 2))})
            observations.append(item)
    assert len(observations) == 15
    assert [r["joint_exact_reported_ratio"]["compatible_with_closed_envelope"] for r in ratios] == [False, False, True, True, True]
    assert [r["joint_ratio_also_rounded_half_unit"]["compatible_with_closed_envelope"] for r in ratios] == [False, False, True, True, True]
    supplement_pdf = (HERE / "raw/ao6c00086_si_001.pdf").read_bytes()
    supplement_sha = hashlib.sha256(supplement_pdf).hexdigest()
    assert supplement_sha == "2161f703c72a5bcf5412fa2654425adf4f31d6be7efde87f88661a283303aa96"
    supplement_text = (HERE / "raw/supplement.txt").read_text()
    assert hashlib.sha256((HERE / "raw/supplement.txt").read_bytes()).hexdigest() == "e6ae88e4d25f1a2063c73587117d937ee9da388cfbb4d9b3855c358a2e5dcfd6"
    s7 = supplement_text.split("Table S7:", 1)[1].split("Table S8:", 1)[0]
    s8 = supplement_text.split("Table S8:", 1)[1].split("Literature", 1)[0]
    s7_rows = re.findall(r"^\s*(\d+)\s+([\d.]+)\s+([\d.]+)\s+(99)\s+(99)\s+(\d+)\s*$", s7, re.M)
    s8_rows = re.findall(r"^\s*([123])\s+([\d.]+)\s+(>\s*99)\s+(>\s*99)\s+(\d+)\s*$", s8, re.M)
    assert len(s7_rows) == 10 and len(s8_rows) == 3
    stats = {}
    for label, column in (("Te_rejection_percent", 1), ("permeate_flux_L_m2_h", 4)):
        values = [F(row[column]) for row in s8_rows]
        mean = statistics.mean(values)
        sample_variance = statistics.variance(values)
        stats[label] = {"values_exact": list(map(str, values)), "mean_exact": str(mean),
                        "sample_variance_exact": str(sample_variance),
                        "sample_sd": math.sqrt(sample_variance),
                        "population_sd": statistics.pstdev(values),
                        "standard_error_of_mean": math.sqrt(sample_variance / len(values))}
    assert stats["Te_rejection_percent"]["sample_variance_exact"] == "1/25"
    assert stats["permeate_flux_L_m2_h"]["sample_variance_exact"] == "43"
    assert statistics.variance([F(1), F(2), F(3)]) == 1
    result = {"status": "COMPLETE_RETROSPECTIVE_EXTRACTION_AND_CONDITIONAL_CHECK",
              "source_sha256": SOURCE_SHA256, "self_checks_passed": self_check(),
              "rows": observations, "source_tables": tables,
              "ratio_assumptions": ["Feed molar Te:V:W is 1:3:3 for every Table 3 arm.",
                  "Equation 1 uses element-specific feed concentrations; mass-to-mole conversion cancels within each element's rejection.",
                  "Each printed integer rejection is within +/-0.5 percentage point of its underlying value.",
                  "Closed envelopes conservatively include rounding ties; these are not measurement uncertainties.",
                  "Printed composition means molar Te:V:W with W normalized to exactly 3.",
                  "The secondary calculation also allows +/-0.5 unit on Te and V ratios, not on the normalization constant.",
                  "These conditional assumptions are not proof of the authors' rounding or sample-normalization procedures."],
              "table3_ratio_checks": ratios,
              "supplement": {"pdf_sha256": supplement_sha,
                  "text_sha256": hashlib.sha256((HERE / "raw/supplement.txt").read_bytes()).hexdigest(),
                  "table_s7_columns": ["pressure_bar", "flow_rate_mL_min", "Te_rejection_percent", "W_rejection_percent", "V_rejection_percent", "permeate_flux_L_m2_h"],
                  "table_s7_source_rows": s7_rows,
                  "table_s8_columns": ["run", "Te_rejection_percent", "W_rejection_percent", "V_rejection_percent", "permeate_flux_L_m2_h"],
                  "table_s8_source_rows": s8_rows, "table_s8_stats": stats,
                  "table_s8_reported_sd": {"Te_rejection_percent": "0.2", "permeate_flux_L_m2_h": "4"},
                  "table_s8_flux_sd_reproduced": False,
                  "table_s8_concentration_mM": None,
                  "statistical_assertions_passed": 3,
                  "statistics_scope": "Printed three-run values only; >99 censoring for W/V preserved, not treated as exact99; missing concentration not inferred."},
              "fit_performed": False,
              "held_out_validation": False, "new_candidate_roles": 0, "complement_admissions": 0}
    (HERE / "extracted-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "rows": len(observations),
                      "self_checks_passed": result["self_checks_passed"],
                      "conditional_incompatible_concentrations_mM": [1, 5],
                      "supplement_rows": len(s7_rows) + len(s8_rows),
                      "statistical_assertions_passed": 3,
                      "table_s8_flux_sample_sd": stats["permeate_flux_L_m2_h"]["sample_sd"]}))


if __name__ == "__main__":
    main()
