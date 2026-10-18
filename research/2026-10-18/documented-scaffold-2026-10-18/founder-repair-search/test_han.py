import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import openpyxl

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "sources/repair/han2025/41467_2025_60201_MOESM3_ESM.xlsx"
SOURCE_SHA = "6807bd68789619eaa116329b9b73b14ed3d1e779696590dca665c77f12183206"
AMOUNT = np.array([0.05845, 0.91754, 0.02119, 0.00282])
MASS = np.array([53.939608, 55.934936, 56.935392, 57.933274])
WEIGHT = AMOUNT*MASS/np.sum(AMOUNT*MASS)
TOLERANCE = 0.25


def advance(solid, liquid, uptake, loss, hours):
    solid, liquid, uptake, loss = np.broadcast_arrays(solid, liquid, uptake, loss)
    rate = uptake+loss
    equilibrium = np.divide(uptake*(solid+liquid), rate,
                            out=np.zeros_like(rate, dtype=float), where=rate > 0)
    new_solid = equilibrium+(solid-equilibrium)*np.exp(-rate*hours)
    return new_solid, solid+liquid-new_solid


def fit_controls(initial, bath, observed):
    bounds = np.log([[1e-5, 1e-5], [10.0, 1000.0]])
    current = np.array([0.5, 0.03])[:, None]

    def grid(lower, upper, size):
        first = np.linspace(lower[0], upper[0], size)
        second = np.linspace(lower[1], upper[1], size)
        a, b = np.meshgrid(first, second, indexing="ij")
        uptake = np.exp(a.ravel())[:, None, None]
        loss = np.exp(b.ravel())[:, None, None]*current
        predicted, _ = advance(initial, bath, uptake, loss, 20.0)
        errors = np.sum((predicted-observed)**2, axis=(1, 2))
        return first, second, errors

    first, second, errors = grid(bounds[0], bounds[1], 121)
    best_error = np.inf
    for candidate in np.argsort(errors)[:64]:
        i, j = np.unravel_index(candidate, (121, 121))
        lower = np.array([first[max(0, i-1)], second[max(0, j-1)]])
        upper = np.array([first[min(120, i+1)], second[min(120, j+1)]])
        for _ in range(4):
            a, b, local = grid(lower, upper, 61)
            index = int(np.argmin(local))
            x, y = np.unravel_index(index, (61, 61))
            if local[index] < best_error:
                best_error = float(local[index])
                parameters = np.exp([a[x], b[y]])
            lower = np.array([a[max(0, x-1)], b[max(0, y-1)]])
            upper = np.array([a[min(60, x+1)], b[min(60, y+1)]])
    return parameters, bool(np.any(np.abs(np.log(parameters)-bounds) < 1e-4))


def pulse_prediction(initial, bath, uptake, loss_per_current, clock):
    solid, liquid = initial.copy(), bath.copy()
    total_elapsed, oer_hours = 0.0, 0.0
    while (oer_hours if clock == "oer" else total_elapsed) < 20.0-1e-10:
        remaining = 20.0-(oer_hours if clock == "oer" else total_elapsed)
        duration = min(1.0, remaining)
        solid, liquid = advance(solid, liquid, uptake, loss_per_current*0.5, duration)
        total_elapsed += duration
        oer_hours += duration
        rest = 0.05 if clock == "oer" else min(0.05, max(0.0, 20.0-total_elapsed))
        solid, liquid = advance(solid, liquid, uptake, 0.0, rest)
        total_elapsed += rest
    return solid, liquid, total_elapsed, oer_hours


def self_check():
    solid, liquid = np.array([2.0, 0.3]), np.array([0.9, 5.0])
    for uptake, loss in ((0, 0), (0, 0.5), (0.4, 0), (0.3, 0.7)):
        s, l = advance(solid, liquid, uptake, loss, 20)
        assert np.all(s >= -1e-12) and np.all(l >= -1e-12)
        assert np.max(np.abs(s+l-solid-liquid)) < 1e-12
        a, b = advance(solid, liquid, uptake, loss, 7)
        a, b = advance(a, b, uptake, loss, 13)
        assert np.max(np.abs(a-s)) < 1e-12
    assert np.allclose(advance(solid, liquid, 0, 0, 20)[0], solid)
    assert np.allclose(advance(solid, liquid, 0, 0.2, 20)[0], solid*np.exp(-4))
    eq = (solid+liquid)*0.3
    assert np.allclose(advance(eq, solid+liquid-eq, 0.3, 0.7, 20)[0], eq)
    synthetic, _ = advance(solid, liquid, 0.1, np.array([0.5, 0.03])[:, None]*2, 20)
    fitted, _ = fit_controls(solid, liquid, synthetic)
    assert np.allclose(fitted, [0.1, 2], rtol=1e-5)
    for clock, expected in (("oer", 21), ("elapsed", 20)):
        s, l, elapsed, active = pulse_prediction(solid, liquid, 0.1, 2, clock)
        assert abs(elapsed-expected) < 1e-10 and active <= 20+1e-10
        assert np.max(np.abs(s+l-solid-liquid)) < 1e-12


def main():
    self_check()
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("Source workbook changed")
    workbook = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)
    sheet = workbook["Fig3"]
    block = list(sheet.iter_rows(min_row=25, max_row=30, min_col=8, max_col=11, values_only=True))
    workbook.close()
    assert block[0][0] == "3g" and block[1][1:] == ("56Fe", "57Fe", "56Fe+57Fe")
    assert [row[0] for row in block[2:]] == ["EA high J", "w/o EA High j", "w/o EA low j", "EA high j"]
    values = np.array([row[1:] for row in block[2:]], dtype=float)
    initial, controls, reserved = values[0, :2], values[1:3, :2], values[3, :2]
    names = ["initial", "high_no_EA", "low_no_EA", "high_EA_reserved"]
    source_rows = [{"condition": name, "source_row": 27+i,
                    "Fe56_ug_cm2": float(v[0]), "Fe57_ug_cm2": float(v[1]),
                    "reported_two_isotope_sum": float(v[2]),
                    "individual_sum_minus_reported": float(v[0]+v[1]-v[2])}
                   for i, (name, v) in enumerate(zip(names, values))]
    scenarios = []
    for volume_ml in (50, 100):
        background_mass = 20*volume_ml/1000
        added_label = 100*volume_ml/1000
        bath = background_mass*WEIGHT[1:3]+np.array([0, added_label])
        assert reserved[1] > TOLERANCE
        minimum_ratio = min(initial[0]/initial[1], (initial[0]+bath[0])/(initial[1]+bath[1]))
        tolerance_box_ratio = (reserved[0]+TOLERANCE)/(reserved[1]-TOLERANCE)
        parameters, boundary = fit_controls(initial, bath, controls)
        uptake, loss = parameters
        predicted, liquid = advance(initial, bath, uptake, np.array([0.5, 0.03])[:, None]*loss, 20)
        control_residuals = predicted-controls
        scaling = []
        for factor in (0.5, 1, 2, 4, 8):
            scaled_control = advance(initial, bath, uptake*factor,
                                     np.array([0.5, 0.03])[:, None]*loss*factor, 20)[0]
            scaled_reserved = pulse_prediction(initial, bath, uptake*factor, loss*factor, "oer")[0]
            scaling.append({"rate_multiplier": factor,
                            "control_sse_ug2_cm4": float(np.sum((scaled_control-controls)**2)),
                            "reserved_prediction_ug_cm2": scaled_reserved.tolist(),
                            "class": "Post-hoc timescale sensitivity; not selected against reserved data"})
        cone = []
        for name, observed in zip(names[1:], values[1:, :2]):
            alpha, beta = np.linalg.solve(np.column_stack((initial, initial+bath)), observed)
            cone.append({"condition": name, "alpha": float(alpha), "beta": float(beta),
                         "exact_point_inside_physical_cone": bool(alpha >= 0 and beta >= 0 and alpha+beta <= 1),
                         "class": "Post-hoc algebraic diagnostic of mean endpoints, not an uncertainty test"})
        tests = []
        for clock in ("oer", "elapsed"):
            estimate, remaining, elapsed, oer = pulse_prediction(initial, bath, uptake, loss, clock)
            residual = estimate-reserved
            tests.append({"clock": clock, "predicted_ug_cm2": estimate.tolist(),
                          "residual_ug_cm2": residual.tolist(),
                          "rmse_ug_cm2": float(np.sqrt(np.mean(residual**2))),
                          "screen_pass": bool(np.max(np.abs(residual)) <= TOLERANCE),
                          "remaining_bath_ug_cm2": remaining.tolist(),
                          "elapsed_hours": elapsed, "oer_hours": oer,
                          "prescribed_OER_charge_C_cm2": 0.5*oer*3600,
                          "reductive_pulse_charge_C_cm2": None})
        scenarios.append({"accessible_volume_ml": volume_ml, "initial_bath_ug_cm2": bath.tolist(),
                          "deterministic_screen_compatibility": {
                              "minimum_model_Fe56_Fe57_mass_ratio": float(minimum_ratio),
                              "maximum_ratio_in_reserved_tolerance_box": float(tolerance_box_ratio),
                              "possible_to_meet_both_isotope_tolerances": bool(minimum_ratio <= tolerance_box_ratio),
                              "class": "Post-hoc analytic necessary condition; applies to any common nonnegative rate history within the same closed reservoir"},
                          "untracked_other_background_Fe_ug": float(background_mass*(WEIGHT[0]+WEIGHT[3])),
                          "uptake_per_h": float(uptake), "loss_per_h_per_A_cm2": float(loss),
                          "parameter_boundary": boundary, "control_predictions_ug_cm2": predicted.tolist(),
                          "control_residuals_ug_cm2": control_residuals.tolist(),
                          "control_rmse_ug_cm2": float(np.sqrt(np.mean(control_residuals**2))),
                          "control_screen_pass": bool(np.max(np.abs(control_residuals)) <= TOLERANCE),
                          "absolute_rates_identified": False,
                          "timescale_sensitivity": scaling,
                          "exact_endpoint_cone_diagnostic": cone,
                          "reserved_tests": tests})
    excess = [{"condition": name, "endpoint_minus_initial_Fe57_ug_cm2": float(v[1]-initial[1]),
               "positive_excess_ug_cm2": float(max(0, v[1]-initial[1])),
               "positive_excess_fraction_of_measured_isotope_sum": float(max(0, v[1]-initial[1])/sum(v[:2]))}
              for name, v in zip(names[1:], values[1:])]
    result = {"source_doi": "10.1038/s41467-025-60201-w", "material": "Ni felt Bekaert2Ni18-025",
              "source_sha256": SOURCE_SHA, "units": "micrograms per geometric cm2",
              "protocol_sha256": hashlib.sha256((BASE / "PROTOCOL.md").read_bytes()).hexdigest(),
              "deviations_sha256": hashlib.sha256((BASE / "DEVIATIONS.md").read_bytes()).hexdigest(),
              "validation_class": "Retrospective reserved condition; exact outcomes exposed before implementation; EA excluded from fitting",
              "source_rows": source_rows, "replicate_level_values": None, "numeric_SEM": None,
              "screen_tolerance_ug_cm2": TOLERANCE, "isotope_mass_fractions_background": WEIGHT.tolist(),
              "conditional_excess_label": excess, "finite_bath_models": scenarios,
              "retained_only_baseline_control_rmse": float(np.sqrt(np.mean((initial-controls)**2))),
              "retained_only_baseline_reserved_rmse": float(np.sqrt(np.mean((initial-reserved)**2))),
              "initial_measured_Fe57_Fe56_mass_ratio": float(initial[1]/initial[0]),
              "nominal_natural_Fe57_Fe56_mass_ratio": float(WEIGHT[2]/WEIGHT[1]),
              "functional_contribution_of_new_Fe": None, "functional_inheritance_demonstrated": False,
              "verified_integrated_complements_added": 0,
              "self_check": "PASS: tracked-isotope conservation, positivity, semigroup, zero-rate limits, equilibrium, synthetic fit and pulse clocks"}
    out = BASE / "results"
    out.mkdir(exist_ok=True)
    (out / "han_test.json").write_text(json.dumps(result, indent=2)+"\n")
    figure, axes = plt.subplots(1, 2, figsize=(9, 3.7))
    for i, label in enumerate(("56Fe", "57Fe")):
        axes[i].bar(np.arange(4), values[:, i], color=["gray", "tab:red", "tab:green", "tab:blue"])
        for scenario, marker in zip(scenarios, ("x", "+")):
            estimate = scenario["reserved_tests"][0]["predicted_ug_cm2"][i]
            axes[i].scatter([3], [estimate], marker=marker, s=100, color="black",
                            label=f"Passive-rest null, {scenario['accessible_volume_ml']}mL")
        axes[i].set(xticks=np.arange(4), xticklabels=["Initial", "High noEA", "Low noEA", "High EA"],
                    ylabel=f"{label} (micrograms/cm²)")
        axes[i].legend(fontsize=8)
    figure.suptitle("Han2025 Ni felt: reported means and reserved-condition predictions")
    figure.tight_layout()
    figure.savefig(out / "han_test.png", dpi=160)
    print(json.dumps({"self_check": result["self_check"], "conditional_excess_label": excess,
                      "scenarios": [{"volume_ml": s["accessible_volume_ml"],
                                     "control_rmse": s["control_rmse_ug_cm2"],
                                     "reserved": s["reserved_tests"]} for s in scenarios]}))


if __name__ == "__main__":
    main()
