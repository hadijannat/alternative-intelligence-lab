from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
F = 96485.33212
CURRENT_FACTOR = 4 * F * 1e-6
GAMMA = np.linspace(-np.log(10), np.log(10), 1001)
GAMMA[500] = 0


def fit(n, j, changing=False):
    dn = n[1:4] - n[0]
    dj = j[1:4] - j[0]
    gamma = GAMMA if changing else np.array([0.0])
    z = CURRENT_FACTOR * np.exp(gamma[:, None] * np.arange(1, 4)[None, :] / 3) * dn
    denom = np.sum(z*z, axis=1)
    k = np.maximum(0, np.divide(np.sum(z*dj, axis=1), denom,
                              out=np.zeros(len(gamma)), where=denom > 0))
    sse = np.sum((z*k[:, None]-dj)**2, axis=1)
    best = int(np.argmin(sse))
    close = sse <= sse[best] + max(1e-12, .01*sse[best])
    return {"k_apparent_per_s": float(k[best]), "gamma": float(gamma[best]),
            "training_SSE_mA2_cm4": float(sse[best]), "training_count": 3,
            "gamma_boundary": bool(changing and best in (0, len(gamma)-1)),
            "zero_competence": bool(k[best] == 0), "zero_density_leverage": bool(np.all(denom == 0)),
            "near_optimal_gamma_range": [float(gamma[close].min()), float(gamma[close].max())],
            "near_optimal_definition": "SSE <= minSSE + max(1e-12,0.01*minSSE)"}


def predict(n, j1, p):
    return j1 + CURRENT_FACTOR * p["k_apparent_per_s"] * np.exp(p["gamma"]*np.arange(len(n))/3) * (n-n[0])


def metrics(observed, prediction):
    residual = prediction - observed
    rmse = float(np.sqrt(np.mean(residual**2)))
    scale = float(np.sqrt(np.mean(observed**2)))
    normalized = rmse / max(scale, 1e-30)
    fractional = abs(residual) / np.maximum(abs(observed), .1)
    return {"RMSE_mA_cm2": rmse, "normalized_RMSE": normalized,
            "max_fractional_error": float(fractional.max()),
            "nominal_operational_screen_pass": bool(normalized <= .1 and fractional.max() <= .2),
            "residuals_pred_minus_observed_mA_cm2": residual.tolist()}


def origin_witness():
    total = np.array([1., 1.1, 1.4, 1.9, 2.5, 2.9, 3.])
    founder_a = total.copy()
    new_a = np.zeros(7)
    founder_b = np.ones(7)
    new_b = total - 1
    j_a = 2 + CURRENT_FACTOR*3*(founder_a+new_a)
    j_b = 2 + CURRENT_FACTOR*3*(founder_b+new_b)
    assert np.array_equal(j_a, j_b)
    initial = {"founder_total": 3., "founder_accessible": 1., "fresh_liquid_total": 2.}
    for founders, new in ((founder_a, new_a), (founder_b, new_b)):
        assert np.allclose(founders+(3-founders), 3)
        assert np.allclose(new+(2-new), 2)
        assert np.all(founders >= 0) and np.all(new >= 0)
    return {"kind": "Synthetic observation nonuniqueness; not fitted to source",
            "units": "nmol/cm2 in synthetic finite pools", "same_initial_pools": initial,
            "total_accessible_Fe": total.tolist(), "founder_only_accessible": founder_a.tolist(),
            "replacement_founder_accessible": founder_b.tolist(), "replacement_new_accessible": new_b.tolist(),
            "max_charge_or_count_difference": 0., "max_current_difference_mA_cm2": float(abs(j_a-j_b).max()),
            "measured_initial_founder_inventory_upper_bound": None}


def self_check():
    assert abs(CURRENT_FACTOR - .38594132848) < 1e-12
    n = np.array([.1, .13, .2, .3, .5, .7, .9])
    p = {"k_apparent_per_s": 3., "gamma": float(GAMMA[600])}
    j = predict(n, 2., p)
    recovered = fit(n, j, True)
    assert abs(recovered["k_apparent_per_s"] - 3) < 1e-12 and recovered["gamma"] == p["gamma"]
    flat = fit(n, np.ones(7), True)
    assert flat["zero_competence"]
    none = fit(np.ones(7), np.arange(7.), True)
    assert none["zero_density_leverage"]
    changed = j.copy()
    changed[4:] = [100, 200, 300]
    assert fit(n, changed, True) == recovered
    m0 = fit(n, j)
    assert recovered["training_SSE_mA2_cm4"] <= m0["training_SSE_mA2_cm4"] + 1e-12
    nchanged = n.copy()
    nchanged[4:] *= 100
    assert fit(nchanged, j, True) == recovered
    witness = origin_witness()
    return {"units_charge_and_molar_density": "PASS", "synthetic_parameter_recovery": "PASS",
            "zero_competence_and_no_leverage": "PASS", "reserved_values_excluded": "PASS",
            "M0_nested_in_M1": "PASS", "origin_counterexample": witness}


def corner_sensitivity(points):
    bounds = [p["n_interval_nmol_cm2"] for p in points] + [p["j_interval_mA_cm2"] for p in points]
    summary = {m: {"pass_corners": 0, "nRMSE_min": float("inf"), "nRMSE_max": 0.,
                   "prediction_min_mA_cm2": [float("inf")]*3, "prediction_max_mA_cm2": [-float("inf")]*3}
               for m in ("M0", "M1", "B1", "B4")}
    for corner in itertools.product((0, 1), repeat=14):
        values = np.array([bounds[i][v] for i, v in enumerate(corner)])
        n, j = values[:7], values[7:]
        for model in summary:
            if model in ("M0", "M1"):
                pred = predict(n, j[0], fit(n, j, model == "M1"))[4:]
            else:
                pred = np.full(3, j[0] if model == "B1" else j[3])
            score = metrics(j[4:], pred)
            s = summary[model]
            s["pass_corners"] += int(score["nominal_operational_screen_pass"])
            s["nRMSE_min"] = min(s["nRMSE_min"], score["normalized_RMSE"])
            s["nRMSE_max"] = max(s["nRMSE_max"], score["normalized_RMSE"])
            s["prediction_min_mA_cm2"] = np.minimum(s["prediction_min_mA_cm2"], pred).tolist()
            s["prediction_max_mA_cm2"] = np.maximum(s["prediction_max_mA_cm2"], pred).tolist()
    return {"scope": "All 16384 independent interval-box corners; not an interior bound, probability, CI or independent replicates. Curve/axis correlations are unmodeled.",
            "corners": 16384, "models": summary}


def main():
    checks = self_check()
    source = ROOT / "data/figS8_points.json"
    data = json.loads(source.read_text())
    points = data["points"]
    assert [p["cycle"] for p in points] == list(range(1, 8))
    n = np.array([p["n_nmol_cm2"] for p in points])
    j = np.array([p["j_mA_cm2"] for p in points])
    assert np.isfinite(n).all() and np.isfinite(j).all()
    for p in points:
        assert p["n_interval_nmol_cm2"][0] <= p["n_nmol_cm2"] <= p["n_interval_nmol_cm2"][1]
        assert p["j_interval_mA_cm2"][0] <= p["j_mA_cm2"] <= p["j_interval_mA_cm2"][1]
    fits = {}
    for model in ("M0", "M1", "B1", "B4"):
        p = fit(n, j, model == "M1") if model in ("M0", "M1") else None
        pred = predict(n, j[0], p) if p else np.full(7, j[0] if model == "B1" else j[3])
        fits[model] = {"parameters": p, "predictions_mA_cm2": pred.tolist(),
                       "training": metrics(j[1:4], pred[1:4]), "reserved": metrics(j[4:], pred[4:])}
    assert fits["M1"]["parameters"]["training_SSE_mA2_cm4"] <= fits["M0"]["parameters"]["training_SSE_mA2_cm4"] + 1e-12
    sensitivity = corner_sensitivity(points)
    paths = [ROOT / "PROTOCOL.md", Path(__file__), source, ROOT / "sources/cs2c03898_si_001.pdf"]
    result = {"scope": "Retrospective raster-derived conditional current screening; measured reserved density supplied; no independent functional-origin validation",
              "hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              "self_checks": checks, "points": points, "fit_cycles": [2, 3, 4], "baseline_cycle": 1,
              "reserved_cycles": [5, 6, 7], "current_factor_mA_per_nmol_per_s": CURRENT_FACTOR,
              "models": fits, "digitization_corner_sensitivity": sensitivity,
              "TOF_used_as_response": False, "independent_redox_charge_reintegration": False,
              "origin_function_identified": False, "verified_integrated_complements_added": 0}
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "models.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    cycles = np.arange(1, 8)
    for ax, key, values, ylabel in ((axes[0], "n_interval_nmol_cm2", n, "Reported Fe density (nmol/cm2)"),
                                  (axes[1], "j_interval_mA_cm2", j, "Current density (mA/cm2)")):
        intervals = np.array([p[key] for p in points])
        ax.errorbar(cycles, values, yerr=np.c_[values-intervals[:, 0], intervals[:, 1]-values].T,
                    fmt="ko", capsize=3, label="Raster midpoint and extraction range")
        ax.axvline(4.5, color="gray", linestyle=":")
        ax.set(xlabel="Cycle", ylabel=ylabel)
    for model, value in fits.items():
        axes[1].plot(cycles, value["predictions_mA_cm2"], label=model)
    axes[0].legend(fontsize=7)
    axes[1].legend(fontsize=7)
    fig.suptitle("Figure-derived site/current test; ranges are not measurement confidence intervals")
    fig.tight_layout()
    fig.savefig(out / "models.png", dpi=150)
    plt.close(fig)
    print(json.dumps({m: v["reserved"] for m, v in fits.items()}, indent=2))
    print("PASS: numerical checks; source/extraction/model limitations retained")


if __name__ == "__main__":
    main()
