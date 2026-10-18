import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent


def main():
    original = json.loads((ROOT / "results/hou-test.json").read_text())
    mapped = json.loads((ROOT / "results/hou-stage-mapping.json").read_text())
    fig, (left, right) = plt.subplots(1, 2, figsize=(13.5, 5.5))
    values = [value for cycle in mapped["cycles"]
              for value in (cycle["start_percent"], cycle["after_ten_hours_percent"])]
    for i in range(5):
        color = "#0b7591" if i % 2 == 0 else "#a14d18"
        left.plot([i, i + 1], values[i:i + 2], color=color, linewidth=2)
    left.scatter(range(6), values, color="#17324d", zorder=3)
    for i, value in enumerate(values):
        left.annotate(f"{value:g}", (i, value), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9)
    left.set_xticks(range(6), ["Start 1", "10 h 1", "Start 2", "10 h 2", "Start 3", "10 h 3"], rotation=25)
    left.set_ylim(60, 100)
    left.set_ylabel("Formate Faradaic efficiency (%)")
    left.set_title("Source-defined stages: recovery and renewed decline")
    left.plot([], [], color="#0b7591", label="10 h operation")
    left.plot([], [], color="#a14d18", label="Combined regeneration treatment")
    left.legend(loc="lower left", fontsize=8, frameon=False)
    traces = original["traces"]
    labels = [("10 h " if r["sheet"].endswith("16") else "Short ") + r["time_column"] for r in traces]
    colors = ["#17324d" if r["sheet"].endswith("16") else "#0b7591" for r in traces]
    right.bar(range(11), [r["retention"] for r in traces], color=colors)
    right.axhline(1, color="#a14d18", linestyle="--", linewidth=1.2, label="Persistent early-current reference")
    right.set_xticks(range(11), labels, rotation=50, ha="right", fontsize=8)
    right.set_ylim(0, 1.10)
    right.set_ylabel("Late / early recorded-current magnitude")
    right.set_title("All 11 traces retain lower late-window current")
    right.legend(loc="lower left", fontsize=8, frameon=False)
    for axis in (left, right):
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.15)
    fig.suptitle("Hou et al. 2022: retrospective native-data checks", fontsize=14, x=0.5)
    fig.text(0.02, 0.045, "FE stage interpretation corrected after execution. Current windows fixed at 10–20% and 90–100% of elapsed record time.", fontsize=8)
    fig.text(0.02, 0.015, "No error bars: uncertainty and independent specimen identities are unreported. Bundled intervention; no isolated repair mechanism or integrated-system claim.", fontsize=8)
    fig.tight_layout(rect=(0, 0.10, 1, 0.94))
    target = ROOT / "results/hou-comparisons-final.png"
    if target.exists():
        raise FileExistsError(target)
    fig.savefig(target, dpi=150)
    plt.close(fig)
    print(target)


if __name__ == "__main__":
    main()
