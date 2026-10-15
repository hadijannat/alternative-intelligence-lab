"""Display unresolved results as missing, never as zero prediction error."""
import csv
import json


def plot(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    summary = json.loads((output/"summary.json").read_text())
    with (output/"predictions.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    selected = summary["selected_chemistry"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for ax, dataset in zip(axes[0, :2], ("S13_F1", "S13_HyperA")):
        subset = [r for r in rows if r.get("stage") == "fixed_dose" and r["candidate"] == selected and r["dataset"] == dataset]
        for group in sorted({r["group_id"] for r in subset}):
            curve = sorted([r for r in subset if r["group_id"] == group], key=lambda r: float(r["x"]))
            color = ax.plot([float(r["x"]) for r in curve], [float(r["predicted_percent"]) for r in curve],
                            label=group.replace("S13_", ""))[0].get_color()
            ax.errorbar([float(r["x"]) for r in curve], [float(r["value_percent"]) for r in curve],
                        yerr=[float(r["sd_percent"]) if r["sd_percent"] else 0 for r in curve],
                        color=color, fmt="o", markersize=3, capsize=2)
        if not subset:
            ax.text(.5, .5, "Unresolved", transform=ax.transAxes, ha="center")
        ax.set(title=f"{dataset}: held-dose predictions ({selected})", xlabel="Minutes", ylabel="Reporter yield (%)")
        if subset:
            ax.legend(fontsize=7)
    scores = summary["fixed_family_scores"]
    names = [r["candidate"] for r in scores]
    ax = axes[0, 2]
    for i, row in enumerate(scores):
        if row["resolved"]:
            ax.barh(i, row["rmse_pp"], color="#367da2")
        else:
            ax.text(.1, i, "unresolved", va="center")
    ax.set(yticks=range(len(names)), yticklabels=names, xlabel="Held-dose RMSE (pp)", title="All fixed families")
    ax.axvline(2, color="black", linestyle=":", label="2 pp criterion")
    ax.legend(fontsize=7)
    ax = axes[1, 0]
    for i, row in enumerate(summary["late_time"]):
        if row["resolved"]:
            ax.barh(i, row["rmse_pp"], color="#af6551")
        else:
            ax.text(.1, i, "unresolved", va="center")
    ax.set(yticks=range(len(names)), yticklabels=names, xlabel="45/60-minute RMSE (pp)", title="Late-time challenge, all families")
    ax.axvline(2, color="black", linestyle=":")
    ax = axes[1, 1]
    nested = [r for r in rows if r.get("stage") == "nested_outer" and float(r["x"]) > 0]
    for dataset in ("S13_F1", "S13_HyperA"):
        subset = [r for r in nested if r["dataset"] == dataset]
        ax.scatter([float(r["value_percent"]) for r in subset], [float(r["predicted_percent"]) for r in subset], label=dataset, s=18)
    ax.plot([0, 100], [0, 100], "k:")
    ax.set(title="Nested selection: outer predictions", xlabel="Measured reporter (%)", ylabel="Predicted reporter (%)")
    ax.legend(fontsize=7)
    ax = axes[1, 2]
    for i, (mode, result) in enumerate(summary["transport"].items()):
        if result["resolved"]:
            ax.barh(i, result["benchmark"]["rmse_pp"], color="#7d759a")
        else:
            ax.text(.1, i, "unresolved", va="center")
    ax.set(yticks=[0, 1], yticklabels=list(summary["transport"]), xlabel="Historical benchmark RMSE (pp)",
           title="Transport challenge: frozen chemistry")
    ax.axvline(2, color="black", linestyle=":")
    for ax in axes.flat:
        ax.grid(alpha=.2)
    fig.suptitle("Retrospective RNA mechanism comparison — reporter activity does not identify active F1")
    fig.tight_layout()
    fig.savefig(output/"comparison.png", dpi=180)
    plt.close(fig)
