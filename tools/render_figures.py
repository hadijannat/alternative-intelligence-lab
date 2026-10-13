#!/usr/bin/env python3

import csv
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data/mo36-encounter-illustrative.csv"
ASSETS = ROOT / "assets"
TITLE = "Salt screening in an assumed Mo36 encounter model"
DESCRIPTION = (
    "Illustrative saved model values, not measurements. Added NaCl 0, 0.03, "
    "0.08, and 0.18 M gives electrical encounter log-weight L of "
    "6.290, 3.812, 2.181, 0.994 for the point representation and "
    "6.744, 4.478, 2.957, 1.757 for the shell representation. "
    "ASSUMED Fe +50 mV / Si 0 mV, z = -8, gap 0.5 nm. "
    "Zero means equal electrical encounter weights. Representation sensitivity "
    "is not a confidence interval. This is not a survival or preservation result. "
    "Unknown surface potentials can reverse the preference. See the companion CSV."
)


def render_encounter():
    with CSV.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    x = [float(row["added_nacl_M"]) for row in rows]
    point = [float(row["L_point"]) for row in rows]
    shell = [float(row["L_shell"]) for row in rows]
    assert x == [0.0, 0.03, 0.08, 0.18]
    assert point == [6.290, 3.812, 2.181, 0.994]
    assert shell == [6.744, 4.478, 2.957, 1.757]

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "svg.fonttype": "none", "svg.hashsalt": "ail-encounter-v1"})
    fig, ax = plt.subplots(figsize=(10, 7), facecolor="#ffffff")
    fig.subplots_adjust(left=0.115, right=0.96, top=0.77, bottom=0.30)
    fig.text(0.06, 0.945, TITLE, fontsize=19, weight="bold", color="#10283b")
    fig.text(0.06, 0.885, "ASSUMED  Fe +50 mV / Si 0 mV  ·  z = −8  ·  gap 0.5 nm",
             fontsize=13, color="#10283b")
    fig.text(0.06, 0.835, "Saved illustrative model values · no empirical calibration",
             fontsize=11, color="#53636d")
    ax.axhline(0, color="#526575", linewidth=1.2, linestyle="--")
    ax.plot(x, point, color="#007d80", marker="o", markersize=7, linewidth=2,
            label="Point representation")
    ax.plot(x, shell, color="#9b6600", marker="s", markersize=7, linewidth=2,
            label="Shell representation")
    ax.set(xlabel="Added NaCl (mol/L)", ylabel="Electrical encounter log-weight, L",
           xlim=(-0.008, 0.188), ylim=(-0.45, 7.45), xticks=x, yticks=range(0, 8))
    ax.set_xticklabels(["0.00", "0.03", "0.08", "0.18"])
    ax.grid(axis="y", color="#e4e9ec", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#9aa9b2")
    ax.legend(loc="upper right", frameon=False, fontsize=11)
    fig.text(0.115, 0.205, "L = ln(c_Fe / c_Si) from the electrical contribution only; L = 0 means equal weights.",
             fontsize=10.5, color="#10283b")
    fig.text(0.115, 0.155, "Limits: infinite dilution and assigned fields; omitted chemical and non-electrical effects.\n"
             "Point–shell differences show representation sensitivity, not confidence intervals.\n"
             "Unknown surface potentials can reverse the preference. No survival or preservation result.",
             fontsize=10.2, linespacing=1.55, color="#445763", va="top")
    fig.text(0.115, 0.025, "Source: saved encounter report, 2026-10-13 · companion CSV retains rounded report values.",
             fontsize=9, color="#53636d")
    save_figure(fig, "mo36-encounter-illustrative", TITLE, DESCRIPTION)
    print(f"Rendered encounter SVG/PNG from {CSV}; four source rows verified.")


def save_figure(fig, stem, title, description):
    ASSETS.mkdir(parents=True, exist_ok=True)
    svg = ASSETS / f"{stem}.svg"
    fig.savefig(svg, metadata={"Date": None, "Title": title, "Description": description})
    fig.savefig(ASSETS / f"{stem}.png", dpi=180,
                metadata={"Title": title, "Description": description})
    plt.close(fig)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(svg)
    root = tree.getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "chart-title chart-desc")
    for index, (name, identifier, value) in enumerate([
        ("title", "chart-title", title), ("desc", "chart-desc", description)
    ]):
        element = ET.Element(f"{{http://www.w3.org/2000/svg}}{name}", {"id": identifier})
        element.text = value
        root.insert(index, element)
    tree.write(svg, encoding="utf-8", xml_declaration=True)


def render_cco():
    with (ROOT / "data/cco-summary.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    values = {(row["model"], row["split"]): float(row["correctness_percent"]) for row in rows}
    models = ["CCO 128", "Independent cells 128", "Centralized recurrent", "Recurrent GNN"]
    shifts = ["Larger size", "Concentrated allocation", "Longer path"]
    assert len(rows) == len(values) == 10
    assert [values[model, "ID"] for model in models] == [49.67, 50.59, 50.00, 100.00]
    assert [values["CCO 128", shift] for shift in shifts] == [50.52, 50.69, 50.26]
    assert [values["Recurrent GNN", shift] for shift in shifts] == [98.96, 100.00, 51.39]
    title = "CCO pilot: the registered hypothesis was unsupported"
    description = (
        "Saved pilot v1 results, 2026-10-09. Campaign: 24 runs across eight architectures, "
        "three seeds each. Selected model means shown, without uncertainty bars. "
        "In-distribution correctness: CCO 128 49.67%, independent cells 128 50.59%, "
        "centralized recurrent 50.00%, recurrent GNN 100.00%. "
        "Out-of-distribution larger size, concentrated allocation, longer path: "
        "CCO 128 50.52%, 50.69%, 50.26%; GNN 98.96%, 100.00%, 51.39%. "
        "Chance is 50%. CCO stays near chance; GNN fails on longer paths. "
        "This bounded negative result does not generalize to all communicating neural systems."
    )
    fig, axes = plt.subplots(1, 2, figsize=(13, 7.6), facecolor="white")
    fig.subplots_adjust(left=0.16, right=0.96, top=0.72, bottom=0.30, wspace=0.70)
    fig.text(0.035, 0.94, title, fontsize=20, weight="bold", color="#10283b")
    fig.text(0.035, 0.877, "Saved pilot v1 · 24 runs / 8 architectures / 3 seeds each · selected means shown",
             fontsize=12.5, color="#53636d")
    for ax in axes:
        ax.set_xlim(0, 112)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("Correctness (%)")
        ax.axvline(50, color="#526575", linestyle="--", linewidth=1.2, zorder=3)
        ax.grid(axis="x", color="#e4e9ec", linewidth=0.7)
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color("#9aa9b2")
        ax.tick_params(axis="y", length=0)
    left, right = axes
    left.set_title("A  In-distribution test", loc="left", fontsize=14, pad=20)
    bars = left.barh(range(4), [values[model, "ID"] for model in models], height=0.54,
                     color=["#007d80", "#8496a1", "#8496a1", "#9b6600"])
    left.set_yticks(range(4), ["CCO 128", "Independent\ncells 128", "Centralized\nrecurrent", "Recurrent GNN"])
    left.invert_yaxis()
    left.bar_label(bars, fmt="%.2f", padding=4, fontsize=10)
    right.set_title("B  Out-of-distribution tests", loc="left", fontsize=14, pad=20)
    for model, offset, color in [("CCO 128", -0.17, "#007d80"), ("Recurrent GNN", 0.17, "#9b6600")]:
        bars = right.barh([index + offset for index in range(3)],
                          [values[model, shift] for shift in shifts], height=0.28,
                          color=color, label=model)
        right.bar_label(bars, fmt="%.2f", padding=4, fontsize=10)
    right.set_yticks(range(3), ["Larger\nsize", "Concentrated\nallocation", "Longer\npath"])
    right.invert_yaxis()
    right.legend(loc="lower center", bbox_to_anchor=(0.5, 1.14), ncol=2, frameon=False, fontsize=10)
    fig.text(0.16, 0.20, "Dashed line: 50% chance. Means across three seeds; descriptive intervals remain in the report.",
             fontsize=11, color="#10283b")
    fig.text(0.16, 0.145, "CCO remained near chance. The GNN solved the ID task but failed on the longer-path shift.\n"
             "Bounded negative result: this architecture, task family and training allowance; compute was not matched.",
             fontsize=11, linespacing=1.7, color="#445763", va="top")
    fig.text(0.16, 0.035, "Source: cco/REPORT.md · pilot v1, 2026-10-09 · values transcribed into data/cco-summary.csv",
             fontsize=10, color="#53636d")
    save_figure(fig, "cco-summary", title, description)
    print("Rendered CCO SVG/PNG from data/cco-summary.csv; ten source values verified.")


if __name__ == "__main__":
    render_encounter()
    render_cco()
