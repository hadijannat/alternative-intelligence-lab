"""Retrospective scores and frozen transport contrasts; missing fits stay visible."""
import csv
import json

LABELS = {"baseline": "Baseline", "release": "Release",
          "reversible_free": "Reversible: free", "reversible_equilibrium": "Reversible: equilibrium"}


def plot(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    summary = json.loads((output/"summary.json").read_text())
    profiles = json.loads((output/"profiles.json").read_text())
    with (output/"predictions.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    selected = summary["selected_chemistry"]
    fig, axes = plt.subplots(3, 2, figsize=(14, 14), layout="constrained")
    for ax, dataset in zip(axes[0], ("S13_F1", "S13_HyperA")):
        subset = [r for r in rows if r.get("stage") == "fixed_dose" and r["candidate"] == selected and r["dataset"] == dataset]
        for group in sorted({r["group_id"] for r in subset}):
            curve = sorted([r for r in subset if r["group_id"] == group], key=lambda r: float(r["x"]))
            dose = curve[0]["seed_uM"] if dataset == "S13_F1" else curve[0]["hyper_a_uM"]
            color = ax.plot([float(r["x"]) for r in curve], [float(r["predicted_percent"]) for r in curve],
                            label=f"{float(dose):g} µM")[0].get_color()
            ax.errorbar([float(r["x"]) for r in curve], [float(r["value_percent"]) for r in curve],
                        yerr=[float(r["sd_percent"]) if r["sd_percent"] else 0 for r in curve],
                        color=color, fmt="o", markersize=3, capsize=2)
        if not subset:
            ax.text(.5, .5, "Unresolved", transform=ax.transAxes, ha="center")
        dose_name = "F1 dose" if dataset == "S13_F1" else "Hyper-A dose"
        ax.set(title=f"Held {dose_name}\n{LABELS.get(selected, 'Unresolved chemistry')}",
               xlabel="Minutes", ylabel="PAGE reporter yield (%)")
        if subset:
            ax.legend(fontsize=8)
    scores = summary["fixed_family_scores"]
    names = [r["candidate"] for r in scores]
    ax = axes[1, 0]
    for i, row in enumerate(scores):
        if row["resolved"]:
            ax.barh(i, row["rmse_pp"], color="#367da2")
        else:
            ax.text(.1, i, "unresolved", va="center")
    ax.set(yticks=range(len(names)), yticklabels=[LABELS[n] for n in names],
           xlabel="Held-dose RMSE (pp)", title="Fixed families: eight held doses")
    ax.axvline(2, color="black", linestyle=":", label="2 pp RMSE component")
    ax.legend(fontsize=8)
    ax = axes[1, 1]
    for offset, stage, label, color in ((-.18, "late_time", "Late time", "#af6551"),
                                       (.18, "joint_challenge", "High dose + late time", "#7d759a")):
        for i, row in enumerate(summary[stage]):
            if row["resolved"]:
                ax.barh(i+offset, row["rmse_pp"], height=.34, color=color, label=label if i == 0 else None)
            else:
                ax.text(.1, i+offset, "unresolved", va="center", fontsize=8)
    ax.set(yticks=range(len(names)), yticklabels=[LABELS[n] for n in names], xlabel="Held RMSE (pp)",
           title="Fixed challenges\n15/30-minute training → 45/60-minute test")
    ax.axvline(2, color="black", linestyle=":")
    ax.legend(fontsize=8)
    ax = axes[2, 0]
    nested = [r for r in rows if r.get("stage") == "nested_outer" and float(r["x"]) > 0]
    for dataset in ("S13_F1", "S13_HyperA"):
        subset = [r for r in nested if r["dataset"] == dataset]
        if subset:
            ax.scatter([float(r["value_percent"]) for r in subset], [float(r["predicted_percent"]) for r in subset],
                       label=dataset.replace("S13_", ""), s=20)
    ax.plot([0, 100], [0, 100], "k:")
    ax.set(title="Nested selection: outer predictions", xlabel="Measured reporter (%)", ylabel="Predicted reporter (%)")
    if nested:
        ax.legend(fontsize=8)
    ax = axes[2, 1]
    for parameter in ("kb", "krel", "kbind"):
        subset = [r for r in profiles if r["parameter"] == parameter]
        if subset:
            x = [r["fixed_log10"] for r in subset]
            y = [r["fit"].get("rmse_pp", np.nan) for r in subset]
            ax.plot(x, y, "o-", label=parameter)
            for row in subset:
                if not row["fit"]["resolved"]:
                    ax.text(row["fixed_log10"], .02, "failed", rotation=90, transform=ax.get_xaxis_transform(), fontsize=7)
    ax.set(title="Selected chemistry: nuisance-refitted profiles\nFive fixed values per introduced rate / saturation constant",
           xlabel="Fixed parameter log10 value", ylabel="Full-data RMSE (pp)")
    if profiles:
        ax.legend(fontsize=8)
    for ax in axes.flat:
        ax.grid(alpha=.2)
    fig.suptitle("Retrospective RNA turnover comparison\nPAGE yield alone does not identify competent F1; adequacy also requires maximum-error and numerical checks", fontsize=13)
    fig.savefig(output/"comparison.png", dpi=180)
    plt.close(fig)

    transport = list(summary["transport"].values())
    fig, ax = plt.subplots(figsize=(13, max(8, .43*len(transport))), layout="constrained")
    labels = []
    for i, result in enumerate(transport):
        reset = "; reset" if result["complex_reset"] else ""
        labels.append(f"{LABELS[result['candidate']]} | {result['mixing_mode']} | {result['loss_closure'].replace('_', ' ')}{reset}")
        if result["resolved"]:
            ax.barh(i, result["benchmark"]["rmse_pp"], color="#af6551" if result["complex_reset"] else "#367da2")
        else:
            ax.text(.1, i, "unresolved", va="center")
    ax.set(yticks=range(len(labels)), yticklabels=labels, xlabel="Historical benchmark RMSE (pp; 72 positive-time rows)",
           title="All frozen chemistries × transport closures\nOnly mixing is fitted; retention remains 55% per three FT cycles")
    ax.invert_yaxis()
    ax.axvline(2, color="black", linestyle=":", label="2 pp RMSE component")
    ax.legend(fontsize=8)
    ax.grid(axis="x", alpha=.2)
    fig.savefig(output/"transport_comparison.png", dpi=180)
    plt.close(fig)
