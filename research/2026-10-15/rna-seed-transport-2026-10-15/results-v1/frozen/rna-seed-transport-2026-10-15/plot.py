"""Plots include every frozen scenario, including unsuccessful predictions."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def plot(output):
    output = Path(output)
    results = json.loads((output/"scenarios.json").read_text())
    predictions = read(output/"predictions.csv")
    contrasts = read(output/"seed_contrasts.csv")
    colors = ("#0072B2", "#D55E00", "#009E73")
    fig, axes = plt.subplots(3, 3, figsize=(14, 11), sharex=True, sharey=True, constrained_layout=True)
    for ax, (scenario, detail) in zip(axes.flat, results.items()):
        ax.set_title(scenario.replace("|", "\n"), fontsize=9)
        if not detail["resolved"]:
            ax.text(.5, .5, "UNRESOLVED", ha="center", transform=ax.transAxes)
            continue
        for seed, color in enumerate(colors):
            rows = [r for r in predictions if r.get("scenario") == scenario and r["dataset"] == "Figure_3" and float(r["seed_uM"]) == seed]
            xs = sorted({float(r["x"]) for r in rows})
            means = [np.mean([float(r["value_percent"]) for r in rows if float(r["x"]) == x]) for x in xs]
            sd = [np.std([float(r["value_percent"]) for r in rows if float(r["x"]) == x], ddof=1) for x in xs]
            predicted = [next(float(r["predicted_percent"]) for r in rows if float(r["x"]) == x) for x in xs]
            ax.errorbar(xs, means, yerr=sd, color=color, fmt="o", ms=3, capsize=2)
            ax.plot(xs, predicted, color=color, label=f"Seed {seed} µM")
        ax.grid(alpha=.2)
        metric = detail["held_out_serial"]
        ax.text(.02, .97, f"RMSE {metric['rmse_pp']:.2f} pp; {'PASS' if metric['adequate'] else 'FAIL'}",
                transform=ax.transAxes, va="top", fontsize=8)
    for ax in axes[-1]:
        ax.set_xlabel("Serial generation")
    for ax in axes[:, 0]:
        ax.set_ylabel("Washed intracellular PAGE yield (%)")
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("Retrospective held-out serial tests: lines model; points mean ± replicate SD")
    for extension in ("png", "pdf"):
        fig.savefig(output/f"serial_validation.{extension}", dpi=170)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    first = next((name for name, detail in results.items() if detail["resolved"]), None)
    for ax, contrast in zip(axes, ("1-0", "2-0")):
        for scenario in results:
            rows = [r for r in contrasts if r.get("scenario") == scenario and r["contrast"] == contrast]
            if rows:
                ax.plot([int(r["generation"]) for r in rows], [float(r["yield_percent"]) for r in rows], label=scenario)
        if first is not None:
            source = [r for r in predictions if r.get("scenario") == first and r["dataset"] == "Figure_3"]
            xs = sorted({float(r["x"]) for r in source})
            observed = [np.mean([float(r["value_percent"]) for r in source if float(r["x"]) == x and float(r["seed_uM"]) == int(contrast[0])])
                        - np.mean([float(r["value_percent"]) for r in source if float(r["x"]) == x and float(r["seed_uM"]) == 0]) for x in xs]
            ax.plot(xs, observed, "ko--", label="Observed mean contrast")
        ax.axhline(0, color="gray", lw=.5)
        ax.set(xlabel="Serial generation", ylabel="Intracellular yield difference (pp)", title=f"Seed contrast {contrast} µM")
        ax.grid(alpha=.2)
    axes[1].legend(fontsize=7, loc="upper right")
    fig.suptitle("Seed dependence: every frozen transport scenario")
    for extension in ("png", "pdf"):
        fig.savefig(output/f"seed_contrasts.{extension}", dpi=170)
    plt.close(fig)

    profiles = json.loads((output/"profiles.json").read_text())
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), constrained_layout=True)
    for ax, (family, name) in zip(axes, (("bath", "nu"), ("patch", "nu"), ("patch", "diffusion"))):
        rows = [r for r in profiles if r["family"] == family and r["parameter"] == name]
        ax.plot([r["fixed_value"] for r in rows], [r["fit"].get("sse", np.nan) for r in rows], "o-")
        for row in rows:
            if not row["fit"]["resolved"]:
                ax.axvline(row["fixed_value"], color="red", alpha=.3)
        ax.set(xscale="log", xlabel=name, ylabel="Calibration SSE (pp²)", title=f"{family}: {name}")
        ax.grid(alpha=.2)
    fig.suptitle("Training-only profiles; no confidence intervals or held-out tuning")
    for extension in ("png", "pdf"):
        fig.savefig(output/f"training_profiles.{extension}", dpi=170)
    plt.close(fig)
