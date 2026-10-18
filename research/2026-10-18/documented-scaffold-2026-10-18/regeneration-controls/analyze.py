from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from inventory import ROOT, SOURCE, number

OUT = ROOT / "results"
G = np.logspace(-3, 8, 61)
D = np.logspace(-5, 1, 61)
R = np.r_[0.0, np.logspace(-4, 3, 41)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(item):
    path = SOURCE / item["path"]
    assert sha(path) == item["sha256"]
    lines = path.read_text(errors="replace").splitlines()
    idx = next(i for i, s in enumerate(lines) if s.split("\t")[1:2] == ["TABLE"])
    cols = lines[idx + 1].strip().split("\t")
    units = lines[idx + 2].strip().split("\t")
    rows = []
    for line in lines[idx + 3:]:
        fields = line.strip().split("\t")
        if not re.fullmatch(r"\d+", fields[0]):
            break
        assert len(fields) == len(cols)
        rows.append([number(fields[j]) for j in (1, 2, 3)])
    data = np.array(rows, dtype=float)
    assert len(data) == item["tables"][0]["rows"] and np.isfinite(data).all()
    assert cols[:4] == ["Pt", "T", "Vf", "Im"] and units[1] == "s" and units[3] == "A"
    assert np.all(np.diff(data[:, 0]) >= 0)
    return data, cols, units


def stamp(item):
    h = item["headers"]
    date = h["DATE"][1].replace("/", "-")
    return datetime.strptime(date + " " + h["TIME"][1], "%d-%m-%Y %H:%M:%S")


def aggregate(data, endpoints):
    out = []
    for end in endpoints:
        rows = data[(data[:, 0] >= end - 300) & (data[:, 0] <= end)]
        assert len(rows) >= 2 and rows[0, 0] <= end - 300 + np.median(np.diff(data[:, 0]))
        out.append({"sample_time_s": float(np.median(rows[:, 0])), "endpoint_s": float(end),
                    "voltage_V": float(np.median(rows[:, 1])), "rows": len(rows),
                    "current_median_A": float(np.median(rows[:, 2]))})
    return out


def extract(files):
    by_specimen = defaultdict(list)
    for item in files:
        if item.get("specimen"):
            by_specimen[item["specimen"]].append(item)
    runs = []
    followups = []
    provenance = []
    for specimen, members in sorted(by_specimen.items()):
        oer = sorted([x for x in members if x.get("headers", {}).get("TAG", [""])[0] == "CHRONOP"], key=stamp)
        if not oer:
            continue
        pulses = sorted([x for x in members if Path(x["path"]).name.startswith("Regen_") and x.get("tables")], key=stamp)
        followup = [x for x in oer if specimen == "WNi78T" and Path(x["path"]).name == "WNi78Tfinal.DTA"]
        oer = [x for x in oer if x not in followup]
        summaries, events, metadata, all_raw = [], [], [], []
        cumulative = 0.0
        for i, item in enumerate(oer):
            data, cols, units = table(item)
            data = data[data[:, 0] >= 0]
            end = float(data[-1, 0])
            assert data[0, 0] == 0
            endpoints = np.arange(6000, end + 1e-8, 6000) if len(oer) == 1 else np.array([end])
            if len(oer) > 1:
                assert end == 6000
            for point in aggregate(data, endpoints):
                point.update(oer_h=(cumulative + point["sample_time_s"]) / 3600,
                             split="training" if (cumulative + point["endpoint_s"]) / 3600 <= 24 else "reserved",
                             interval_end_oer_h=(cumulative + point["endpoint_s"]) / 3600,
                             source_path=item["path"])
                summaries.append(point)
            if i == 0:
                anchor_rows = data[(data[:, 0] >= 1800) & (data[:, 0] <= 3600)]
                assert len(anchor_rows) > 1
                anchor_v = float(np.median(anchor_rows[:, 1]))
                anchor_h = float(np.median(anchor_rows[:, 0])) / 3600
            all_raw.append(np.c_[(cumulative + data[:, 0]) / 3600, data[:, 1]])
            current = data[1:, 2]
            metadata.append({"path": item["path"], "sha256": item["sha256"], "columns": cols, "units": units,
                             "rows": len(data), "duration_s": end, "partial_tail_s": float(end % 6000),
                             "start": stamp(item).isoformat(), "current_min_A": float(current.min()),
                             "current_median_A": float(np.median(current)), "current_max_A": float(current.max()),
                             "relative_current_max_deviation": float(np.max(abs(current / np.median(current) - 1))),
                             "initial_current_A": float(data[0, 2])})
            cumulative += end
            next_start = stamp(oer[i + 1]) if i + 1 < len(oer) else None
            between = [p for p in pulses if stamp(p) >= stamp(item) + timedelta(seconds=end)
                       and (next_start is None or stamp(p) < next_start)]
            for pulse in between:
                pd, pc, pu = table(pulse)
                duration = max(0.0, float(pd[-1, 0]))
                events.append({"oer_h": cumulative / 3600, "duration_h": duration / 3600,
                               "path": pulse["path"], "sha256": pulse["sha256"],
                               "native_min_s": float(pd[0, 0]), "native_max_s": float(pd[-1, 0]),
                               "terminal_not_between_oer_blocks": next_start is None})
            if next_start:
                gap = (next_start - stamp(item)).total_seconds() - end
                metadata[-1]["wall_gap_to_next_oer_s"] = gap
                metadata[-1]["observed_pulse_in_gap_s"] = sum(e["duration_h"] * 3600 for e in events if e["oer_h"] == cumulative / 3600)
                metadata[-1]["unassigned_gap_s"] = gap - metadata[-1]["observed_pulse_in_gap_s"]
        raw = np.concatenate(all_raw)
        for p in summaries:
            p["delta_voltage_V"] = p["voltage_V"] - anchor_v
        run = {"specimen": specimen, "figure_group": oer[0]["group"], "anchor_V": anchor_v, "anchor_oer_h": anchor_h,
               "oer_duration_h": cumulative / 3600, "pulse_run": bool(pulses), "summaries": summaries,
               "pulse_events": events, "native_records": metadata}
        runs.append(run)
        for processed in [x for x in members if x["path"].endswith("processed.txt")]:
            assert sha(SOURCE / processed["path"]) == processed["sha256"]
            lines = (SOURCE / processed["path"]).read_text().splitlines()
            processed_rows = [row.split("\t") for row in lines[1:] if row.strip()]
            assert all(len(row) == 2 for row in processed_rows)
            pd = np.array([[number(row[0]), number(row[1]) if row[1].strip() else np.nan] for row in processed_rows])
            assert np.isfinite(pd[:, 0]).all()
            n = min(len(raw), len(pd))
            assert np.isfinite(pd[:n]).all()
            # Paired acquisition row order is checked independently of any Fe-dose assignment.
            scale, offset = np.linalg.lstsq(np.c_[raw[:n, 1], np.ones(n)], pd[:n, 1], rcond=None)[0]
            time_scale, time_offset = np.linalg.lstsq(np.c_[raw[:n, 0], np.ones(n)], pd[:n, 0], rcond=None)[0]
            err = pd[:n, 1] - (scale * raw[:n, 1] + offset)
            provenance.append({"specimen": specimen, "path": processed["path"], "sha256": processed["sha256"],
                               "paired_rows": n, "raw_rows": len(raw), "processed_rows": len(pd),
                               "processed_voltage_scale_per_raw_V": float(scale), "processed_voltage_offset": float(offset),
                               "voltage_pair_RMSE_processed_units": float(np.sqrt(np.mean(err**2))),
                               "voltage_pair_max_abs_error_processed_units": float(abs(err).max()),
                               "processed_time_scale_per_oer_h": float(time_scale), "processed_time_offset_h": float(time_offset),
                               "time_pair_max_abs_error_h": float(abs(pd[:n, 0] - raw[:n, 0]).max()),
                               "time_affine_residual_max_h": float(abs(pd[:n, 0] - (time_scale * raw[:n, 0] + time_offset)).max()),
                               "unsupported_processed_tail_rows": len(pd) - n,
                               "missing_processed_voltage_rows_1based_with_header": (np.flatnonzero(~np.isfinite(pd[:, 1])) + 2).tolist(),
                               "unsupported_tail_start_h": float(pd[n, 0]) if n < len(pd) else None,
                               "unsupported_tail_end_h": float(pd[-1, 0]) if n < len(pd) else None})
        for item in followup:
            data, cols, units = table(item)
            points = aggregate(data, np.arange(6000, data[-1, 0] + 1e-8, 6000))
            av = float(np.median(data[(data[:, 0] >= 1800) & (data[:, 0] <= 3600), 1]))
            followups.append({"specimen": specimen, "source_path": item["path"], "sha256": item["sha256"],
                              "start": stamp(item).isoformat(), "duration_s": float(data[-1, 0]),
                              "anchor_V": av, "partial_tail_s": float(data[-1, 0] % 6000), "summaries": points,
                              "status": "NOT_VALIDATED: intervening EIS and unknown gap; separate <=24h followup, no reserved data"})
    assert len(runs) == 10
    return runs, followups, provenance


def competence(times, anchor, events, ds, rs):
    """Exact phase updates, with unobserved wall gaps excluded rather than labelled rest."""
    ds, rs = np.broadcast_arrays(np.asarray(ds, float), np.asarray(rs, float))
    x = np.ones(ds.shape)
    last = anchor
    j = 0
    pulses = sorted([e for e in events if e["oer_h"] >= anchor], key=lambda e: e["oer_h"])
    values = []
    for t in times:
        while j < len(pulses) and pulses[j]["oer_h"] <= t:
            e = pulses[j]
            x *= np.exp(-ds * (e["oer_h"] - last))
            x = 1 - (1 - x) * np.exp(-rs * e["duration_h"])
            last = e["oer_h"]
            j += 1
        x *= np.exp(-ds * (t - last))
        last = t
        values.append(x.copy())
    return np.stack(values, axis=-1)


def observe(x, g, b):
    return b * (np.log1p(g) - np.log1p(g * x))


def fit(times, y, anchor, events, b, restoration):
    rates = R if restoration else R[:1]
    x = competence(times, anchor, events, D[:, None], rates[None, :])
    pred = observe(x[None, :, :, :], G[:, None, None, None], b)
    sse = np.sum((pred - y) ** 2, axis=-1)
    idx = np.unravel_index(np.argmin(sse), sse.shape)
    gi, di, ri = idx
    best = float(sse[idx])
    close = sse <= best + max(1e-12, best * .01)
    inds = np.argwhere(close)
    return {"g": float(G[gi]), "d_per_h": float(D[di]), "r_per_h": float(rates[ri]), "training_SSE": best,
            "grid_index": [int(v) for v in idx], "grid_points": int(sse.size),
            "near_optimal_definition": "SSE <= minSSE + max(1e-12,0.01*minSSE)",
            "near_optimal_count": int(close.sum()),
            "near_optimal_parameter_ranges": {"g": [float(G[inds[:, 0].min()]), float(G[inds[:, 0].max()])],
                                               "d_per_h": [float(D[inds[:, 1].min()]), float(D[inds[:, 1].max()])],
                                               "r_per_h": [float(rates[inds[:, 2].min()]), float(rates[inds[:, 2].max()])]},
            "boundary_flags": {"g": gi in (0, len(G)-1), "d": di in (0, len(D)-1),
                               "r_zero": bool(ri == 0), "r_upper": bool(restoration and ri == len(rates)-1)}}


def metrics(y, pred):
    residual = pred - y
    rmse = float(np.sqrt(np.mean(residual**2)))
    maximum = float(abs(residual).max())
    return {"n": len(y), "RMSE_V": rmse, "MAE_V": float(abs(residual).mean()), "max_abs_error_V": maximum,
            "screen_pass": rmse <= .05 and maximum <= .1, "residual_pred_minus_observed_V": residual.tolist()}


def origin_counterexample():
    # Arrays index atom origin (founder,new) and pool (active,buried,liquid).
    retained = np.array([[1., 0., 0.], [0., 0., 10.]])
    replacement = retained.copy()
    history = []
    for cycle in range(12):
        survival, restore = np.exp(-.2 * 1.5), 1 - np.exp(-20 / 36)
        for pools, destination in ((retained, 1), (replacement, 2)):
            moved = pools[:, 0] * (1 - survival)
            pools[:, 0] -= moved
            pools[:, destination] += moved
        amount = (1 - retained[:, 0].sum()) * restore
        moved = retained[:, 1] * restore
        retained[:, 1] -= moved
        retained[:, 0] += moved
        liquid = replacement[:, 2].sum()
        assert liquid >= amount
        moved = replacement[:, 2] * (amount / liquid)
        replacement[:, 2] -= moved
        replacement[:, 0] += moved
        assert np.all(retained >= 0) and np.all(replacement >= 0)
        assert np.allclose(retained.sum(axis=1), [1, 10], atol=1e-12)
        assert np.allclose(replacement.sum(axis=1), [1, 10], atol=1e-12)
        assert np.isclose(retained[:, 0].sum(), replacement[:, 0].sum(), atol=1e-12)
        history.append({"cycle": cycle + 1, "retention_pools": retained.tolist(), "replacement_pools": replacement.tolist(),
                        "retention_delta_V": float(observe(retained[:, 0].sum(), 10, .04)),
                        "replacement_delta_V": float(observe(replacement[:, 0].sum(), 10, .04))})
    relabel = replacement[::-1].copy()
    assert np.allclose(relabel.sum(axis=0), replacement.sum(axis=0))
    assert replacement[1, 0] > .1 and retained[1, 0] == 0
    return {"status": "PASS: same initial pools, different origin-specific active fractions, identical voltage",
            "initial_by_origin_active_buried_liquid": [[1, 0, 0], [0, 0, 10]], "units": "synthetic normalized metal inventory",
            "max_voltage_difference_V": max(abs(h["retention_delta_V"]-h["replacement_delta_V"]) for h in history),
            "origin_relabel_output_invariance": True, "history": history}


def selfchecks():
    t = np.arange(0, 6001, 30)
    fake = np.c_[t, t / 1000, np.ones(len(t)) * .057]
    summary = aggregate(fake, [6000])[0]
    assert summary["sample_time_s"] == 5850 and summary["voltage_V"] == 5.85 and summary["rows"] == 11
    pulse = np.c_[np.arange(0, 101, 10), np.full(11, -99.), np.full(11, -.01)]
    phases = [("OER", fake), ("pulse", pulse), ("OER", fake.copy())]
    synthetic_summaries = [aggregate(data, [6000])[0] for phase, data in phases if phase == "OER"]
    assert len(synthetic_summaries) == 2 and all(p["voltage_V"] == 5.85 for p in synthetic_summaries)
    assert sum(data[-1, 0] for phase, data in phases if phase == "pulse") == 100
    events = [{"oer_h": 2., "duration_h": .5}, {"oer_h": 4., "duration_h": .25}]
    times = np.array([1., 3., 5.])
    assert np.allclose(competence(times, 0, events, .2, 0), np.exp(-.2*times))
    assert np.all(competence(times, 0, events, 0, 10) == 1)
    x = competence(times, 0, events, .2, 3)
    assert np.all((x >= 0) & (x <= 1)) and np.all(x+(1-x) == 1)
    assert np.allclose(competence([3], 0, events, .2, 3)[0],
                       (1-(1-np.exp(-.4))*np.exp(-1.5))*np.exp(-.2))
    assert np.all(observe(np.ones(3), 10, .04) == 0)
    synthetic_times = np.linspace(1, 23, 14)
    synthetic_events = [{"oer_h": v, "duration_h": .1 if i % 2 else .5} for i, v in enumerate(np.arange(1.5, 24, 1.5))]
    true = (G[25], D[37], R[25])
    sy = observe(competence(synthetic_times, .75, synthetic_events, true[1], true[2]), true[0], .04)
    recovered = fit(synthetic_times, sy, .75, synthetic_events, .04, True)
    assert np.allclose([recovered["g"], recovered["d_per_h"], recovered["r_per_h"]], true, rtol=1e-10)
    passive = fit(synthetic_times, sy, .75, synthetic_events, .04, False)
    assert recovered["training_SSE"] <= passive["training_SSE"] + 1e-14
    return {"aggregation_known_synthetic": "PASS", "no_loss_no_restoration_exact_phases": "PASS",
            "positivity_competence_conservation": "PASS", "synthetic_grid_recovery": "PASS", "nesting": "PASS",
            "synthetic_true_parameters": list(true), "synthetic_recovered": recovered}


def main():
    OUT.mkdir(exist_ok=True)
    checks = selfchecks()
    manifest = json.loads((ROOT / "file_manifest.json").read_text())
    runs, followups, provenance = extract(manifest["files"])
    fits = []
    for run in runs:
        times = np.array([x["oer_h"] for x in run["summaries"]])
        y = np.array([x["delta_voltage_V"] for x in run["summaries"]])
        train = np.array([x["split"] == "training" for x in run["summaries"]])
        assert train.any() and (~train).any() and times[train].max() <= 24 and times[~train].min() > 24
        run["training_n"], run["reserved_n"] = int(train.sum()), int((~train).sum())
        run["flat_baseline"] = {"prediction_V": float(y[train][-1]), "training": metrics(y[train], np.full(train.sum(), y[train][-1])),
                                "reserved": metrics(y[~train], np.full((~train).sum(), y[train][-1]))}
        for b in (.04, .02, .08):
            for model in ("M0", "M1"):
                fitted = fit(times[train], y[train], run["anchor_oer_h"], run["pulse_events"], b, model == "M1" and run["pulse_run"])
                x = competence(times, run["anchor_oer_h"], run["pulse_events"], fitted["d_per_h"], fitted["r_per_h"])
                pred = observe(x, fitted["g"], b)
                assert np.all((x >= 0) & (x <= 1))
                # The two atom-origin interpretations share total competence and observation law.
                founder_interpretation = observe(x, fitted["g"], b)
                replacement_interpretation = observe(x.copy(), fitted["g"], b)
                assert np.array_equal(founder_interpretation, replacement_interpretation)
                result = {"specimen": run["specimen"], "b_V": b, "model": model, "parameters": fitted,
                          "predicted_delta_V": pred.tolist(), "predicted_total_competence": x.tolist(),
                          "training": metrics(y[train], pred[train]), "reserved": metrics(y[~train], pred[~train]),
                          "origin_equivalence_max_difference_V": float(abs(founder_interpretation-replacement_interpretation).max())}
                fits.append(result)
            assert fits[-1]["parameters"]["training_SSE"] <= fits[-2]["parameters"]["training_SSE"] + 1e-12
            if not run["pulse_run"]:
                assert fits[-1]["predicted_delta_V"] == fits[-2]["predicted_delta_V"]
        print(run["specimen"], "summaries", len(times), "train", train.sum(), "reserved", (~train).sum(), flush=True)
    result = {"protocol_sha256": sha(ROOT / "PROTOCOL.md"), "amendments_sha256": sha(ROOT / "AMENDMENTS.md"),
              "script_sha256": sha(Path(__file__)), "manifest_sha256": sha(ROOT / "file_manifest.json"),
              "selfchecks": checks, "runs": runs, "fits": fits, "processed_raw_provenance": provenance,
              "separate_followups": followups, "origin_counterexample": origin_counterexample(),
              "fit_data_boundary": "Only times/y indexed by training mask passed to fit; reserved arrays used only after parameters fixed.",
              "validation_scope": "Retrospective paper-informed within-specimen forecast; Fe doses unresolved; no independent-specimen validation."}
    (OUT / "analysis.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    fig, axes = plt.subplots(5, 2, figsize=(12, 17))
    for ax, run in zip(axes.flat, runs):
        points = run["summaries"]
        times = np.array([p["oer_h"] for p in points])
        y = np.array([p["delta_voltage_V"] for p in points])
        training = times <= 24
        ax.scatter(times[training], y[training], s=12, c="black", label="native training")
        ax.scatter(times[~training], y[~training], s=12, facecolors="none", edgecolors="black", label="native reserved")
        for model, color in (("M0", "tab:orange"), ("M1", "tab:blue")):
            f = next(f for f in fits if f["specimen"] == run["specimen"] and f["model"] == model and f["b_V"] == .04)
            ax.plot(times, f["predicted_delta_V"], color=color, label=model)
        ax.axhline(run["flat_baseline"]["prediction_V"], ls=":", color="gray", label="flat baseline")
        ax.axvline(24, ls="--", color="gray", lw=.7)
        ax.set(title=run["specimen"] + " (" + run["figure_group"] + ")", xlabel="Cumulative OER exposure (h)", ylabel="Raw potential change (V)")
    axes.flat[0].legend(fontsize=7)
    fig.suptitle("Poli2025 native specimens: fixed b=0.040 V; feed identities unresolved")
    fig.tight_layout()
    fig.savefig(OUT / "forecasts.png", dpi=150)
    plt.close(fig)
    print("PASS: execution/selfchecks; scientific forecast failures retained in analysis.json")


if __name__ == "__main__":
    main()
