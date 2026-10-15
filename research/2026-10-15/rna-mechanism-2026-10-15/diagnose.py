"""Reproduce the old RNA failure and decompose it without changing its model."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "measured-coupling-2026-10-15"
sys.path.insert(0, str(BASE / "rna_model"))
from model import Parameters, bulk_curve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use an unused output path")
    args.output.mkdir(parents=True)
    summary = json.loads((BASE / "rna_model/results-v1/summary.json").read_text())
    parameters = Parameters(**summary["parameters"])
    with (BASE / "rna_sources/observations.csv").open() as handle:
        rows = [r for r in csv.DictReader(handle) if r["dataset"].startswith("S13")]
    output = []
    groups = sorted({(r["dataset"], float(r["seed_uM"]), float(r["hyper_a_uM"])) for r in rows})
    for dataset, seed, hyper in groups:
        group = sorted((r for r in rows if (r["dataset"], float(r["seed_uM"]), float(r["hyper_a_uM"])) == (dataset, seed, hyper)),
                       key=lambda r: float(r["x"]))
        prediction = bulk_curve(parameters, seed, hyper, [float(r["x"]) for r in group])
        for r, value in zip(group, prediction):
            output.append({"dataset": dataset, "seed_uM": seed, "hyper_uM": hyper,
                           "time_min": float(r["x"]), "observed_percent": float(r["value_percent"]),
                           "predicted_percent": float(value), "residual_pp": float(value)-float(r["value_percent"]),
                           "source_sheet": r["source_sheet"], "source_cell": r["source_cell"]})
    assert len(output) == 40
    overall = float(np.sqrt(np.mean([r["residual_pp"]**2 for r in output])))
    assert abs(overall-summary["kinetic_fit"]["rmse_pp"]) < 1e-9
    per_group = []
    for dataset, seed, hyper in groups:
        values = [r for r in output if (r["dataset"], r["seed_uM"], r["hyper_uM"]) == (dataset, seed, hyper)]
        per_group.append({"dataset": dataset, "seed_uM": seed, "hyper_uM": hyper,
                          "rmse_pp": float(np.sqrt(np.mean([r["residual_pp"]**2 for r in values]))),
                          "bias_pp": float(np.mean([r["residual_pp"] for r in values])),
                          "observed_60min_percent": values[-1]["observed_percent"],
                          "predicted_60min_percent": values[-1]["predicted_percent"]})
    sources = [BASE / "rna_model/model.py", BASE / "rna_model/results-v1/summary.json",
               BASE / "rna_sources/observations.csv"]
    result = {"overall_rmse_pp": overall, "saved_baseline_reproduced": True,
              "by_condition": per_group,
              "rmse_by_route_pp": {name: float(np.sqrt(np.mean([r["residual_pp"]**2 for r in output if r["dataset"] == name])))
                                   for name in ("S13_F1", "S13_HyperA")},
              "B_initial_uM": 7.5,
              "B_remaining_at_observed_F1_1uM_60min_uM": 7.5-5*next(r["observed_percent"] for r in output if r["seed_uM"] == 1 and r["time_min"] == 60)/100,
              "notes": ["The B estimate uses F1-only chemistry with one B consumed per observed reporter product.",
                        "Both held-out transfer outcomes and these bulk observations are now development evidence.",
                        "Residuals diagnose inadequacy; they do not uniquely identify the omitted mechanism."],
              "baseline_sha256": {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    (args.output / "diagnosis.json").write_text(json.dumps(result, indent=2)+"\n")
    with (args.output / "bulk_residuals.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader(); writer.writerows(output)
    print(json.dumps({"baseline_reproduced": True, "overall_rmse_pp": overall,
                      "rmse_by_route_pp": result["rmse_by_route_pp"]}))


if __name__ == "__main__":
    main()
