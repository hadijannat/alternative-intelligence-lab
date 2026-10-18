from pathlib import Path
import hashlib
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import openpyxl

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sources/41467_2025_60728_MOESM5_ESM.xlsx"
KGRID = np.r_[0.0, np.logspace(-4, 1, 1001)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def extract(ws, col, start):
    last = max((r for r in range(start, ws.max_row + 1)
                if ws.cell(r, col).value is not None or ws.cell(r, col + 1).value is not None), default=start - 1)
    rows = []
    for r in range(start, last + 1):
        x, y = ws.cell(r, col), ws.cell(r, col + 1)
        rows.append({"row": r, "x_cell": x.coordinate, "y_cell": y.coordinate,
                     "x": x.value, "y": y.value, "valid": finite(x.value) and finite(y.value)})
    return {"sheet": ws.title, "headers": [[ws.cell(r, c).value for c in (col, col + 1)]
            for r in range(1, start)], "rows": rows,
            "invalid_rows": [v["row"] for v in rows if not v["valid"]]}


def values(block):
    rows = [r for r in block["rows"] if r["valid"]]
    return np.array([r["x"] for r in rows], float), np.array([r["y"] for r in rows], float)


def window(block, lo, hi, final=False):
    rows = [r for r in block["rows"] if r["valid"] and r["x"] >= lo
            and (r["x"] <= hi if final else r["x"] < hi)]
    x, _ = values(block)
    if not rows:
        return {"window": [lo, hi], "n": 0, "full_edge_support": False, "observed": None}
    y = np.array([r["y"] for r in rows])
    return {"window": [lo, hi], "n": len(rows), "rows": [r["row"] for r in rows],
            "full_edge_support": bool(x.min() <= lo and x.max() >= hi),
            "observed": {"min": float(y.min()), "max": float(y.max()),
                         "median": float(np.median(y)), "midpoint": float((y.min() + y.max()) / 2)},
            "sample_time_bounds": [min(r["x"] for r in rows), max(r["x"] for r in rows)]}


def ratio(after, before):
    if after is None or before is None or before["min"] <= 0:
        return None
    return {"nominal": after["median"] / before["median"],
            "midpoint_ratio": after["midpoint"] / before["midpoint"],
            "bounds": [min(a / b for a in (after["min"], after["max"])
                           for b in (before["min"], before["max"])),
                       max(a / b for a in (after["min"], after["max"])
                           for b in (before["min"], before["max"]))]}


def crossings(block, target):
    found = []
    for left, right in zip(block["rows"], block["rows"][1:]):
        if not left["valid"] or not right["valid"]:
            continue
        x0, x1, y0, y1 = left["x"], right["x"], left["y"], right["y"]
        if not min(x0, x1) <= target <= max(x0, x1):
            continue
        currents = [y0, y1] if x0 == x1 == target else ([y0 + (target - x0) * (y1 - y0) / (x1 - x0)] if x0 != x1 else [])
        for current in currents:
            if not any(math.isclose(current, v["current"], rel_tol=0, abs_tol=1e-12) for v in found):
                found.append({"current": current, "segment_rows": [left["row"], right["row"]],
                              "cells": [left["x_cell"], left["y_cell"], right["x_cell"], right["y_cell"]]})
    currents = [v["current"] for v in found]
    return {"potential_V_RHE": target, "crossings": found,
            "summary": None if not currents else {"min": min(currents), "max": max(currents),
            "median": float(np.mean(currents)), "midpoint": (min(currents) + max(currents)) / 2,
            "nominal_definition": "arithmetic mean of all distinct crossing currents"}}


def metrics(observed, predicted):
    residual = predicted - observed
    rmse = float(np.sqrt(np.mean(residual ** 2)))
    nrmse = rmse / max(float(np.mean(np.abs(observed))), 1.0)
    maxfrac = float(np.max(np.abs(residual) / np.maximum(np.abs(observed), 1.0)))
    return {"rmse_pp": rmse, "normalized_rmse": nrmse, "maximum_fractional_error": maxfrac,
            "screen_pass": bool(nrmse <= 0.1 and maxfrac <= 0.2)}


def fit(n, y, n0, y0, kind):
    elapsed = n - n0
    e = np.exp(-KGRID[:, None] * elapsed)
    if kind == "loss":
        b = np.zeros(len(KGRID))
    else:
        z = 1 - e
        denominator = np.sum(z * z, axis=1)
        b = np.maximum(0, np.divide(np.sum(z * (y - y0 * e), axis=1), denominator,
                                    out=np.full(len(KGRID), y0, dtype=float), where=denominator > 0))
    pred = y0 * e + b[:, None] * (1 - e)
    sse = np.sum((pred - y) ** 2, axis=1)
    i = int(np.argmin(sse))
    near = sse <= sse[i] * 1.01 + 1e-12
    return {"k": float(KGRID[i]), "b": float(b[i]), "sse": float(sse[i]),
            "grid_index": i, "k_boundary": i in (0, len(KGRID) - 1),
            "b_boundary": bool(b[i] == 0),
            "near_optimal_k_range": [float(KGRID[near].min()), float(KGRID[near].max())]}


def candidate(block):
    n, y = values(block)
    if np.any(np.diff(n) < 0):
        raise ValueError("Candidate cycle order is not monotone; no silent sorting")
    positive = np.flatnonzero(y > 0)
    train, reserved = n <= 40, n > 40
    result = {"cycles": n.tolist(), "observed_percent": y.tolist(), "training_count": int(train.sum()),
              "reserved_count": int(reserved.sum()), "fits": {}, "status": "insufficient_data"}
    if not len(positive) or train.sum() < 3 or reserved.sum() < 2:
        return result
    n0, y0 = float(n[positive[0]]), float(y[positive[0]])
    result.update(status="tested", n0=n0, y0=y0)
    for kind in ("flat", "loss", "two_state"):
        if kind == "flat":
            parameters = {"last_training_value": float(y[train][-1])}
            pred = np.full(len(n), y[train][-1])
        else:
            parameters = fit(n[train], y[train], n0, y0, kind)
            e = np.exp(-parameters["k"] * (n - n0))
            pred = y0 * e + parameters["b"] * (1 - e)
        result["fits"][kind] = {"parameters": parameters, "prediction": pred.tolist(),
                                  "residual": (pred - y).tolist(), "training": metrics(y[train], pred[train]),
                                  "reserved": metrics(y[reserved], pred[reserved])}
    return result


def simulation(dt):
    parameters = [(ka, kc) for ka in (0, 0.1, 1, 10, 100) for kc in (0, 2)]
    ka = np.array([p[0] for p in parameters])
    kc = np.array([p[1] for p in parameters])
    state = np.zeros((10, 4)); state[:, 0] = 1
    states = [state.copy()]
    h = dt / 2
    for _ in range(round(5 / dt)):
        # Symmetric analytic substeps preserve nonnegativity and each Fe-unit balance.
        for reaction in (0, 1, 2, 3, 4, 4, 3, 2, 1, 0):
            if reaction < 4:
                source, sink, rate = ((0, 1, 1), (1, 0, 1), (1, 2, 0.05), (1, 3, kc))[reaction]
                amount = state[:, source] * (-np.expm1(-np.asarray(rate) * h))
                state[:, source] -= amount; state[:, sink] += amount
            else:
                a, d = state[:, 0], state[:, 1]
                smaller, difference = np.minimum(a, d), np.abs(a - d)
                e = np.exp(-difference * ka * h)
                denominator = difference + smaller * (-np.expm1(-difference * ka * h))
                remaining = np.divide(difference * smaller * e, denominator,
                                      out=smaller / (1 + ka * smaller * h), where=denominator > 0)
                amount = smaller - remaining
                state[:, 0] -= amount; state[:, 1] -= amount; state[:, 2] += 2 * amount
        states.append(state.copy())
    return parameters, np.array(states)


def selftests():
    w = openpyxl.Workbook(); ws = w.active
    for row in ((0, 0), (1, 2), (None, None), (1, 4), (0, 6)):
        ws.append(row)
    b = extract(ws, 1, 1)
    assert b["invalid_rows"] == [3]
    assert [v["current"] for v in crossings(b, 0.5)["crossings"]] == [1.0, 5.0]
    assert ratio({"min": 1, "max": 2, "median": 1.5, "midpoint": 1.5},
                 {"min": 0, "max": 2, "median": 1, "midpoint": 1}) is None
    n = np.array([0, 10, 20, 30, 50, 70.]); k = KGRID[501]
    y = 100 * np.exp(-k * n) + 40 * (1 - np.exp(-k * n)); tr = n <= 40
    fitted = fit(n[tr], y[tr], 0, 100, "two_state")
    assert fitted["k"] == k and abs(fitted["b"] - 40) < 1e-10
    changed = y.copy(); changed[~tr] = 1e9
    assert fit(n[tr], changed[tr], 0, 100, "two_state") == fitted
    constant = fit(n[tr], np.full(tr.sum(), 100.), 0, 100, "two_state")
    assert constant["k"] == 0 and constant["b"] == 100
    loss_y = 100 * np.exp(-k * n)
    assert fit(n[tr], loss_y[tr], 0, 100, "loss")["sse"] < 1e-20
    assert fit(n[tr], loss_y[tr], 0, 100, "two_state")["sse"] < 1e-20
    return {"parser_missing_gap": True, "multiple_branch_crossings": True, "nonpositive_ratio_denominator": True,
            "synthetic_grid_recovery": True, "reserved_response_exclusion": True, "zero_k_constant": True,
            "loss_nesting": True}


def main():
    for folder in (ROOT / "data", ROOT / "results"):
        folder.mkdir(exist_ok=True)
    checks = selftests()
    workbook = openpyxl.load_workbook(SOURCE, data_only=True)
    raw = {"CA": {}, "CV": {}, "candidate": {}}
    for name, col in (("SC", 42), ("AEM", 44), ("CEM", 46)):
        raw["CA"][name] = extract(workbook["Fig1"], col, 5)
    for name, col in (("SC", 1), ("CEM", 6), ("AEM", 11)):
        raw["CV"][name] = {"before": extract(workbook["FigS7"], col, 6),
                           "after": extract(workbook["FigS7"], col + 2, 6)}
    for name, col in (("LDH", 8), ("NiFeCl", 10), ("NiFeZnCl", 12)):
        raw["candidate"][name] = extract(workbook["Fig3"], col, 5)
    for block in raw["CA"].values():
        assert block["headers"][3][0] == "min" and "mA/cm" in block["headers"][3][1]
    for pair in raw["CV"].values():
        for block in pair.values():
            assert block["headers"][3] == ["V", "mA/cm2"]
    for block in raw["candidate"].values():
        assert block["headers"][2] == ["CV cycles", "activity retention (%)"]
    save(ROOT / "data/native_cells.json", raw)
    ca, cv = {}, {}
    for name, block in raw["CA"].items():
        anchor, end = window(block, 5, 10), window(block, 295, 300, final=True)
        x, _ = values(block)
        ca[name] = {"anchor": anchor, "endpoint_window": end,
                    "bins": [window(block, lo, lo + 5, final=lo == 295) for lo in range(0, 300, 5)],
                    "observed_window_retention": ratio(end["observed"], anchor["observed"]),
                    "strict_full_edge_retention": ratio(end["observed"], anchor["observed"])
                    if anchor["full_edge_support"] and end["full_edge_support"] else None,
                    "time_bounds": [float(x.min()), float(x.max())],
                    "out_of_order_pairs": int(np.sum(np.diff(x) < 0)),
                    "duplicate_time_count": len(x) - len(np.unique(x))}
    for target in (1.53, 1.55):
        cv[str(target)] = {}
        for name, pair in raw["CV"].items():
            before, after = crossings(pair["before"], target), crossings(pair["after"], target)
            cv[str(target)][name] = {"before": before, "after": after,
                                     "retention": ratio(after["summary"], before["summary"])}
    candidate_results = {name: candidate(block) for name, block in raw["candidate"].items()}
    params, coarse = simulation(0.001)
    _, fine = simulation(0.0005)
    conservation = float(max(np.max(np.abs(coarse.sum(axis=2) - 1)), np.max(np.abs(fine.sum(axis=2) - 1))))
    minimum = float(min(coarse.min(), fine.min()))
    convergence = np.max(np.abs(coarse - fine[::2]), axis=(0, 2))
    invariant_min = float(min(np.min(coarse[:, 0, 0] - coarse[:, 1, 0]), np.min(fine[:, 0, 0] - fine[:, 1, 0])))
    assert conservation < 1e-10 and minimum >= -1e-12 and invariant_min >= -1e-12
    checks.update(source_units=True, positive_pools=True, conserved_Fe_units=True,
                  ka_zero_sink_order=True, step_convergence_below_1e_minus_5=bool(np.max(convergence) < 1e-5))
    sim = {"assumptions": "synthetic normalized Fe pools; no experimentally fitted rates; A+D->2X coarse grained",
           "maximum_mass_error": conservation, "minimum_pool": minimum, "ka0_minimum_lower_sink_A_difference": invariant_min,
           "dt_h": 0.001, "fine_dt_h": 0.0005, "scenarios": []}
    for i, (ka, kc) in enumerate(params):
        sim["scenarios"].append({"ka": ka, "kc": kc, "end_A_D_X_C": coarse[-1, i].tolist(),
                                 "fine_end_A_D_X_C": fine[-1, i].tolist(),
                                 "max_step_halving_difference_all_times_pools": float(convergence[i])})
    sim["lower_sink_minus_higher_sink_A_5h"] = [
        {"ka": ka, "difference": float(coarse[-1, 2 * j, 0] - coarse[-1, 2 * j + 1, 0]),
         "reversal": bool(coarse[-1, 2 * j, 0] < coarse[-1, 2 * j + 1, 0])}
        for j, ka in enumerate((0, 0.1, 1, 10, 100))]
    sim["all_time_ordering"] = []
    for j, ka in enumerate((0, 0.1, 1, 10, 100)):
        difference = coarse[:, 2*j, 0] - coarse[:, 2*j+1, 0]
        fine_difference = fine[:, 2*j, 0] - fine[:, 2*j+1, 0]
        discrepancy = float(np.max(np.abs(difference - fine_difference[::2])))
        sim["all_time_ordering"].append({"ka": ka, "minimum_coarse_difference": float(difference.min()),
            "time_of_coarse_minimum_h": float(np.argmin(difference) * 0.001),
            "minimum_fine_difference": float(fine_difference.min()),
            "time_of_fine_minimum_h": float(np.argmin(fine_difference) * 0.0005),
            "maximum_step_difference_in_ordering": discrepancy,
            "negative_minima_exceed_observed_step_discrepancy": bool(max(difference.min(), fine_difference.min()) < -discrepancy)})
    np.savez_compressed(ROOT / "results/synthetic_trajectories.npz", dt=0.001, coarse=coarse, fine_dt=0.0005, fine=fine)
    result = {"hashes": {str(p.relative_to(ROOT)): digest(p) for p in (SOURCE, ROOT / "PROTOCOL.md", Path(__file__), ROOT / "data/native_cells.json")},
              "checks": checks, "CA": ca, "CV": cv, "candidate": candidate_results, "synthetic": sim}
    save(ROOT / "results/analysis.json", result)
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    for name, block in raw["CA"].items():
        anchor = ca[name]["anchor"]["observed"]["median"]
        bins = ca[name]["bins"]
        axes[0, 0].plot([np.mean(b["window"]) for b in bins if b["observed"]],
                        [b["observed"]["median"] / anchor for b in bins if b["observed"]], label=name)
    axes[0, 0].axvline(10, color="gray", linestyle=":")
    axes[0, 0].set(xlabel="CA time (min)", ylabel="Current / 5–10 min median", title="Native five-minute medians; AEM post-10 min reserved")
    for j, target in enumerate(("1.53", "1.55")):
        for i, name in enumerate(("SC", "CEM", "AEM")):
            r = cv[target][name]["retention"]
            if r:
                axes[0, 1].errorbar(i + 0.12 * (j - 0.5), r["nominal"],
                    yerr=[[r["nominal"] - r["bounds"][0]], [r["bounds"][1] - r["nominal"]]],
                    fmt="o", color=("tab:blue", "tab:orange")[j], label=target + " V" if i == 0 else None)
    axes[0, 1].set(xticks=range(3), xticklabels=["SC", "CEM", "AEM"], ylabel="Post / pre CV current",
                   title="Same-cell paired assay; bounds include all crossings")
    for name, block in raw["candidate"].items():
        x, y = values(block); axes[1, 0].plot(x, y, "o-", label=name)
    axes[1, 0].axvline(40, color="gray", linestyle=":")
    axes[1, 0].set(xlabel="CV cycles", ylabel="Reported activity retention (%)",
                   title="Candidate forecast NOT FIT: 2 training points < 3 required")
    for j, ka in enumerate((0, 0.1, 1, 10, 100)):
        axes[1, 1].plot(np.arange(len(coarse)) * 0.001, coarse[:, 2*j, 0] - coarse[:, 2*j+1, 0], label=f"ka={ka}")
    axes[1, 1].axhline(0, color="gray", linewidth=0.8)
    axes[1, 1].set(xlabel="Synthetic time (h)", ylabel="A(kc=0) − A(kc=2)", title="Synthetic aggregation test; no fitted chemical rates")
    for ax in axes.flat:
        ax.legend(fontsize=8); ax.grid(alpha=0.15)
    fig.savefig(ROOT / "results/observations.png", dpi=160)
    plt.close(fig)
    save(ROOT / "results/artifact_hashes.json", {str(p.relative_to(ROOT)): digest(p) for p in
         (ROOT / "data/native_cells.json", ROOT / "results/analysis.json",
          ROOT / "results/observations.png", ROOT / "results/synthetic_trajectories.npz")})
    print(json.dumps({"checks": checks, "candidate_status": {k: v["status"] for k, v in candidate_results.items()},
                       "CA_observed_window_retention": {k: v["observed_window_retention"] for k, v in ca.items()},
                       "CV_retention": {t: {k: v["retention"] for k, v in blocks.items()} for t, blocks in cv.items()},
                       "synthetic_reversal": sim["lower_sink_minus_higher_sink_A_5h"]}, indent=2))


if __name__ == "__main__":
    main()
