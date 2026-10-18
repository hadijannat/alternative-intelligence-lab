import csv
import hashlib
import itertools
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent


def pools(conversion, ratio):
    conversion, ratio = np.broadcast_arrays(np.asarray(conversion), np.asarray(ratio))
    if np.any((conversion < 0) | (conversion >= 1)) or np.any(ratio <= 0):
        raise ValueError("Require 0<=conversion<1 and positive rate ratio")
    low, high = np.zeros_like(conversion), np.ones_like(conversion)
    for _ in range(70):
        u = (low+high)/2
        below = u+u**ratio < 2*(1-conversion)
        low = np.where(below, u, low)
        high = np.where(below, high, u)
    u = (low+high)/2
    return 0.5*u**ratio, 0.5*u


def predict(conversion, ratio):
    fast, slow = pools(conversion, ratio)
    return (slow-fast)/(slow+fast)


def fit_ratio(x, y):
    lo, hi = 0.0, np.log(1000.0)
    for count in (501, 81, 81, 81):
        grid = np.linspace(lo, hi, count)
        predicted = predict(x[:, None], np.exp(grid)[None, :])
        errors = np.mean((predicted-y[:, None])**2, axis=0)
        i = int(np.argmin(errors))
        best = float(np.exp(grid[i]))
        lo, hi = grid[max(0, i-1)], grid[min(count-1, i+1)]
    return best


def turning_test(series):
    best = None
    for a, b, c in itertools.combinations(series, 3):
        if min(b[0]-a[0], c[0]-b[0]) <= 0.04:
            continue
        valley = min(a[1]-b[1], c[1]-b[1])
        peak = min(b[1]-a[1], b[1]-c[1])
        excursion = max(valley, peak)
        if best is None or excursion > best["excursion"]:
            best = {"triple": [list(a), list(b), list(c)], "excursion": float(excursion),
                    "margin_after_allowance": float(excursion-0.04),
                    "kind": "valley" if valley >= peak else "peak"}
    if best is None:
        raise ValueError("No separated marker triple")
    best["stationary_channel_null_rejected"] = best["margin_after_allowance"] > 0
    return best


def self_check():
    x = np.linspace(0, 0.999, 101)
    assert np.max(np.abs(predict(x, 1))) < 1e-12
    assert np.max(np.abs(predict(x, 4)+predict(x, 0.25))) < 1e-12
    fast, slow = pools(x, 4)
    assert np.max(np.abs(fast+slow-(1-x))) < 1e-12
    assert np.all(fast >= 0) and np.all(slow >= 0)
    consumed_fast, consumed_slow = 0.5-fast, 0.5-slow
    assert np.max(np.abs(fast+slow+consumed_fast+consumed_slow-1)) < 1e-12
    assert abs(fit_ratio(x[10:70], predict(x[10:70], 3.7))-3.7) < 1e-5
    assert not turning_test([(0.1, 0.1), (0.5, 0.2), (0.9, 0.3)])[
        "stationary_channel_null_rejected"]
    assert turning_test([(0.1, -0.3), (0.5, -0.6), (0.9, -0.5)])[
        "stationary_channel_null_rejected"]


def main():
    self_check()
    with (BASE / "data/markers.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    assert {row["catalyst"] for row in rows} == {"GTM-4(RS-OMBMEP)"}
    data = {(p, t): sorted((float(r["conversion_pct"])/100, float(r["ee_pct"])/100)
                          for r in rows if r["panel"] == p and r["treatment"] == t)
            for p in ("A", "B") for t in ("untreated", "preactivated")}
    x, y = np.array(data["B", "preactivated"]).T
    train = (x >= 0.10) & (x <= 0.60)
    held = (x > 0.60) & (x < 0.95)
    assert train.sum() == 6 and held.sum() == 2
    ratio = fit_ratio(x[train], y[train])
    prediction = predict(x[held], ratio)
    residual = prediction-y[held]
    offsets = []
    for dx, dy in itertools.product((-0.02, 0, 0.02), repeat=2):
        offset_ratio = fit_ratio(x[train]+dx, y[train]+dy)
        envelope = [predict(x[held]+hx, offset_ratio).tolist() for hx in (-0.02, 0.02)]
        offsets.append({"training_x_shift": dx, "training_y_shift": dy,
                        "rate_ratio": offset_ratio, "heldout_x_endpoint_predictions": envelope})
    turns = {t: turning_test(data["A", t]) for t in ("untreated", "preactivated")}
    result = {
        "catalyst": "GTM-4(RS-OMBMEP)",
        "source_doi": "10.1021/jacs.5c12567",
        "source_figure": "Figure1 panels A/B",
        "protocol_sha256": hashlib.sha256((BASE / "PROTOCOL.md").read_bytes()).hexdigest(),
        "data_sha256": hashlib.sha256((BASE / "data/markers.csv").read_bytes()).hexdigest(),
        "validation_class": "Retrospective withheld-point assessment, source outcomes previously seen",
        "model": "Initially racemic irreversible pseudo-first-order depletion; one dimensionless total-rate ratio",
        "apparent_rate_ratio": ratio, "absolute_rates_identified": False,
        "training_count": int(train.sum()), "heldout_count": int(held.sum()),
        "training_rmse": float(np.sqrt(np.mean((predict(x[train], ratio)-y[train])**2))),
        "heldout_rows": [{"conversion": float(a), "observed_ee": float(b),
                          "predicted_ee": float(c), "residual": float(d),
                          "observation_class": "Plateau near 100% ee; resolution-limited, not exact extinction"}
                         for a, b, c, d in zip(x[held], y[held], prediction, residual)],
        "heldout_rmse": float(np.sqrt(np.mean(residual**2))),
        "heldout_max_absolute_error": float(np.max(np.abs(residual))),
        "screening_pass": bool(np.sqrt(np.mean(residual**2)) <= 0.05 and np.max(np.abs(residual)) <= 0.10),
        "axis_offset_sensitivity": offsets,
        "sensitivity_scope": "Coherent +/-2pp axis shifts and heldout x endpoints; not all per-point errors or a confidence interval",
        "stationary_branch_invariant": turns,
        "scope_limits": ["Two heldout markers share one high-ee plateau; limited independent constraint",
                         "Raster ee slightly above 1 is retained as artwork, not physical excess or exact purity",
                         "Constant total-rate ratio does not identify stationary product branching",
                         "Passing depletion screening cannot validate a site-activation or transport mechanism",
                         "No new Ge-state/transport/inheritance rates estimated; no PMo12 coupling tested"],
        "self_check": "PASS: conservation, positivity, equal rates, label swap, synthetic recovery and turning cases",
    }
    out = BASE / "results"
    out.mkdir(exist_ok=True)
    (out / "activation.json").write_text(json.dumps(result, indent=2)+"\n")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.7))
    for treatment, color in (("untreated", "tab:red"), ("preactivated", "tab:blue")):
        xx, yy = np.array(data["A", treatment]).T
        axes[0].plot(xx*100, yy*100, "o-", color=color, label=treatment)
    axes[0].set(xlabel="Total conversion (%)", ylabel="Unlike-product ee (%)",
                title="Stationary-branch invariant")
    axes[0].legend()
    grid = np.linspace(0, 0.949, 200)
    axes[1].plot(grid*100, predict(grid, ratio)*100, color="black", label="Frozen depletion fit")
    axes[1].scatter(x[train]*100, y[train]*100, label="Fit", color="tab:blue")
    axes[1].scatter(x[held]*100, y[held]*100, label="Withheld plateau", marker="s", color="tab:orange")
    axes[1].set(xlabel="Total conversion (%)", ylabel="Remaining-substrate ee (%)",
                title="One apparent rate ratio")
    axes[1].legend()
    fig.suptitle("GTM-4(RS-OMBMEP): published raster digitization; retrospective screening")
    fig.tight_layout()
    fig.savefig(out / "activation.png", dpi=160)
    print(json.dumps({k: result[k] for k in ("self_check", "apparent_rate_ratio", "heldout_rmse", "screening_pass")}))
    print(json.dumps(turns))


if __name__ == "__main__":
    main()
