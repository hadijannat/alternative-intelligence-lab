import csv
import hashlib
import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
TOL = 1e-12


def feasible_bounds(edge, plane, incoming, k_edge, k_plane, background=0.2):
    values = (edge, plane, incoming, k_edge, k_plane, background)
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise ValueError("Pools, coefficients and background must be finite and nonnegative")
    if incoming > edge + plane:
        raise ValueError("Incoming Fe exceeds total Fe")
    lo = max(0, incoming - plane)
    hi = min(edge, incoming)
    endpoints = [k_edge * x + k_plane * (incoming - x) for x in (lo, hi)]
    return lo, hi, min(endpoints), max(endpoints)


def allocation(edge, plane, incoming, k_edge, k_plane, background, new_edge):
    lo, hi, _, _ = feasible_bounds(edge, plane, incoming, k_edge, k_plane, background)
    if not math.isfinite(new_edge) or new_edge < lo or new_edge > hi:
        raise ValueError("New edge Fe is outside the feasible interval")
    pools = (edge - new_edge, new_edge, plane - incoming + new_edge, incoming - new_edge)
    old_current = k_edge * pools[0] + k_plane * pools[2]
    new_current = k_edge * pools[1] + k_plane * pools[3]
    return dict(zip(("founder_edge", "new_edge", "founder_plane", "new_plane",
                     "founder_current", "new_current", "total_current"),
                    map(float, (*pools, old_current, new_current,
                                background + old_current + new_current))))


def evaluate_case(case_id, values):
    edge, plane, incoming, ke, kp, bg = values
    lo, hi, lower, upper = feasible_bounds(*values)
    rows = []
    residuals = {key: 0.0 for key in ("nonnegativity", "edge_closure", "plane_closure",
                  "incoming_closure", "founder_closure", "total_closure", "current_closure",
                  "bounds_containment", "lower_attained", "upper_attained")}
    for i in range(21):
        row = allocation(*values, lo + (hi - lo) * Fraction(i, 20))
        fe, ne, fp, np_ = [row[k] for k in ("founder_edge", "new_edge", "founder_plane", "new_plane")]
        errors = {
            "nonnegativity": max(0, -min(fe, ne, fp, np_)),
            "edge_closure": abs(fe + ne - float(edge)),
            "plane_closure": abs(fp + np_ - float(plane)),
            "incoming_closure": abs(ne + np_ - float(incoming)),
            "founder_closure": abs(fe + fp - float(edge + plane - incoming)),
            "total_closure": abs(fe + ne + fp + np_ - float(edge + plane)),
            "current_closure": abs(row["total_current"] - float(bg + ke * edge + kp * plane)),
            "bounds_containment": max(0, float(lower) - row["new_current"], row["new_current"] - float(upper)),
        }
        for key, value in errors.items():
            residuals[key] = max(residuals[key], value)
        rows.append({"case_id": case_id, "allocation_index": i, **row})
    residuals["lower_attained"] = abs(min(r["new_current"] for r in rows) - float(lower))
    residuals["upper_attained"] = abs(max(r["new_current"] for r in rows) - float(upper))
    return {
        "case_id": case_id,
        "inputs": dict(zip(("edge", "plane", "incoming", "k_edge", "k_plane", "background"), map(float, values))),
        "new_edge_interval": [float(lo), float(hi)],
        "new_current_bounds": [float(lower), float(upper)],
        "identified_under_assumptions": abs(float(upper - lower)) <= TOL,
        "maximum_residuals": residuals,
        "checks": {key: value <= TOL for key, value in residuals.items()},
        "all_pass": all(value <= TOL for value in residuals.values()),
    }, rows


def main():
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    f = Fraction
    main_values = (f("0.7"), f("0.3"), f("0.4"), 10, 1, f("0.2"))
    controls = {
        "equal_competence": (*main_values[:3], 1, 1, main_values[5]),
        "no_incoming": (f("0.7"), f("0.3"), 0, 10, 1, f("0.2")),
        "all_incoming": (f("0.7"), f("0.3"), 1, 10, 1, f("0.2")),
        "empty_edge": (0, 1, f("0.4"), 10, 1, f("0.2")),
        "empty_plane": (1, 0, f("0.4"), 10, 1, f("0.2")),
        "zero_inventories": (0, 0, 0, 10, 1, f("0.2")),
        "edge_activity_zero": (*main_values[:3], 0, 1, main_values[5]),
        "plane_activity_zero": (*main_values[:3], 10, 0, main_values[5]),
    }
    main_case, main_rows = evaluate_case("main", main_values)
    control_cases = [evaluate_case(name, values)[0] for name, values in controls.items()]
    cases, rows = [], []
    for i, (edge, plane, fraction, ke, kp) in enumerate(product(
            map(f, ("0", "0.2", "0.7", "1")),
            map(f, ("0", "0.2", "0.7", "1")),
            map(f, ("0", "0.25", "0.5", "0.75", "1")), (0, 1, 10), (0, 1, 10))):
        case, allocations = evaluate_case(i, (edge, plane, fraction * (edge + plane), ke, kp, f("0.2")))
        cases.append(case)
        rows.extend(allocations)
    matrix = np.array([[1, 1, 0, 0], [0, 0, 1, 1], [0, 1, 0, 1], [10, 10, 1, 1]], dtype=float)
    direction = np.array([1, -1, -1, 1], dtype=float)
    augmented = np.vstack((matrix, [0, 1, 0, 0]))
    algebra = {
        "columns": ["founder_edge", "new_edge", "founder_plane", "new_plane"],
        "rows": ["edge_total", "plane_total", "incoming_total", "current_minus_background"],
        "matrix": matrix.tolist(), "rank": int(np.linalg.matrix_rank(matrix)),
        "null_direction": direction.tolist(), "null_residual": (matrix @ direction).tolist(),
        "incoming_current_change_per_unit_direction": -9,
        "augmented_row": [0, 1, 0, 0], "augmented_rank": int(np.linalg.matrix_rank(augmented)),
        "scope": "Regional Fe ancestry identifies algebraic pools only under fixed known competence and background.",
    }
    checks = {
        "main_bounds_1_3_to_4": np.allclose(main_case["new_current_bounds"], [1.3, 4.0], atol=TOL, rtol=0),
        "main_current_7_5": all(abs(r["total_current"] - 7.5) <= TOL for r in main_rows),
        "rank_3_null_direction": algebra["rank"] == 3 and np.max(np.abs(matrix @ direction)) <= TOL,
        "augmented_rank_4": algebra["augmented_rank"] == 4,
        "positive_controls_identified": all(c["identified_under_assumptions"] for c in control_cases[:6]),
        "zero_one_site_activity_does_not_identify": all(not c["identified_under_assumptions"] for c in control_cases[6:]),
        "grid_720_cases_15120_allocations": len(cases) == 720 and len(rows) == 15120,
        "all_grid_and_control_checks": all(c["all_pass"] for c in [main_case, *control_cases, *cases]),
    }
    paths = ["PROTOCOL.md", "AMENDMENTS.md", "SOURCE_AUDIT.md", "sources/ja5c00438_si_001.pdf", "analyze.py"]
    result = {
        "classification": "source-informed analytical/synthetic identifiability test",
        "protocol_interpretation": "AMENDMENTS.md corrects prior fitted-model failures to prior synthetic-model failures; mathematics and frozen cases unchanged.",
        "empirical_held_out_validation": {"status": "INSUFFICIENT_DATA", "training_points": 0,
            "held_out_points": 0, "reason": "No qualified matched specimen-level site/Fe-ancestry/function dataset acquired."},
        "input_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() if (ROOT / p).is_file() else None for p in paths},
        "tolerance": TOL, "main_case": main_case,
        "same_observation_worlds": [main_rows[0], main_rows[-1]],
        "controls": control_cases, "linear_algebra": algebra,
        "grid_cases": cases, "checks": {k: bool(v) for k, v in checks.items()},
        "all_numerical_checks_pass": bool(all(checks.values())),
        "limitations": ["No measured rate, kinetic fit or experimental validation.",
            "Positive conditional lower bounds do not establish observed incoming-material function.",
            "No active repair, inheritance, life or integrated complement established.",
            "Remote-Fe five-hour ordering and numerical convergence failures remain unchanged."],
    }
    (out / "analysis.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    with (out / "grid_allocations.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {"cases": len(cases), "allocations": len(rows), "checks": result["checks"],
               "all_numerical_checks_pass": result["all_numerical_checks_pass"],
               "empirical_status": "INSUFFICIENT_DATA"}
    print(json.dumps(summary, indent=2))
    (out / "run-output.json").write_text(json.dumps(summary, indent=2) + "\n")
    return 0 if result["all_numerical_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
