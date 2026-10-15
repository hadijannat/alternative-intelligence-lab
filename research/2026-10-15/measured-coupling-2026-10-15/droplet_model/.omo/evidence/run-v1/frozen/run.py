"""Offline measured C3 coupling audit. Existing output directories are refused."""
import argparse
import csv
import hashlib
import itertools
import json
import platform
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import least_squares, minimize_scalar

from model import Q, VOLUME, initial, integrate, passages, total_product

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "droplet_sources"


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def write_csv(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def fit(time, observed, capacity=Q, baseline=False):
    def residual(p):
        return total_product(time, p[0], 0 if baseline else p[1], capacity) - observed
    starts = ([.001], [.1], [1]) if baseline else itertools.product((.001, .03, .3), (.1, 2, 10))
    fits = [least_squares(residual, x, bounds=([1e-6], [20]) if baseline else
                          ([1e-6, 0], [20, 100]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
            for x in starts]
    best = min(fits, key=lambda f: sum(f.fun**2))
    if not best.success:
        raise RuntimeError(best.message)
    return {"k0_per_min": float(best.x[0]), "kcat_per_mM_min": 0.0 if baseline else float(best.x[1]),
            "capacity_mM": capacity, "train_SSE_mM2": float(sum(best.fun**2))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    frozen = output / "frozen"
    frozen.mkdir()
    source_csv = SOURCE / "tables/observations.csv"
    paths = [HERE / f for f in ("PROTOCOL.md", "model.py", "run.py", "test_model.py")]
    paths += [source_csv, SOURCE / "conditions.json"]
    manifest = []
    for path in paths:
        copied = frozen / path.name
        shutil.copy2(path, copied)
        manifest.append({"source": str(path.relative_to(HERE.parent)),
                         "snapshot": str(copied.relative_to(output)),
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    write_json(output / "manifest.json", {"files": manifest, "versions": {
        "python": platform.python_version(), "numpy": np.__version__,
        "scipy": scipy.__version__, "matplotlib": matplotlib.__version__}})
    observations = [r for r in csv.DictReader(source_csv.open()) if r["condition_id"] == "single_Cys_PSS"]
    chemical = [r for r in observations if r["measurement"] == "concentration" and r["analyte"] == "C3"]
    turbidity = [r for r in observations if r["measurement"] == "turbidity"]
    if len(chemical) != 16 or len(turbidity) != 126:
        raise ValueError("Unexpected source counts: inspect provenance before changing the frozen protocol")
    time = np.array([float(r["time_value"]) for r in chemical])
    measured = np.array([float(r["value"]) for r in chemical])
    train = time <= 2
    holdout = time >= 4
    fitted = fit(time[train], measured[train])
    baseline = fit(time[train], measured[train], baseline=True)
    residual_rows = []
    for name, result in (("product_dependent", fitted), ("no_autocatalysis", baseline)):
        prediction = total_product(time, result["k0_per_min"], result["kcat_per_mM_min"])
        result["train_RMSE_mM"] = float(np.sqrt(np.mean((prediction[train]-measured[train])**2)))
        result["holdout_RMSE_mM"] = float(np.sqrt(np.mean((prediction[holdout]-measured[holdout])**2)))
        result["holdout_engineering_tolerance_pass"] = result["holdout_RMSE_mM"] <= .084
        for source, t, y, p in zip(chemical, time, measured, prediction):
            residual_rows.append({"model": name, "time_min": t, "measured_mM": y,
                                  "predicted_mM": p, "residual_mM": p-y,
                                  "split": "train" if t <= 2 else "holdout",
                                  "source_file": source["source_file"], "source_row": source["source_row"]})
    profile = []
    for kcat in np.linspace(0, 20, 101):
        optimum = minimize_scalar(lambda logk: float(sum((total_product(time[train], np.exp(logk), kcat)-measured[train])**2)),
                                  bounds=(np.log(1e-6), np.log(20)), method="bounded",
                                  options={"xatol": 1e-11})
        profile.append({"kcat_per_mM_min": float(kcat), "k0_per_min": float(np.exp(optimum.x)),
                        "train_SSE_mM2": float(optimum.fun),
                        "within_descriptive_envelope": bool(optimum.fun <= fitted["train_SSE_mM2"]+.0025)})
    capacity = [fit(time[train], measured[train], q) for q in (.80, .88)]
    for row in capacity:
        p = total_product(time[holdout], row["k0_per_min"], row["kcat_per_mM_min"], row["capacity_mM"])
        row["holdout_RMSE_mM"] = float(np.sqrt(np.mean((p-measured[holdout])**2)))
    windows = []
    for well in sorted({r["replicate_id"] for r in turbidity}):
        series = sorted((float(r["time_value"]), float(r["value"])) for r in turbidity if r["replicate_id"] == well)
        threshold = max(v for _, v in series) * .1
        crossing = next(i for i, (_, v) in enumerate(series) if v < threshold)
        windows.append({"well": well, "OD_threshold": threshold,
                        "last_above_min": series[max(0,crossing-1)][0], "first_below_min": series[crossing][0]})
    k0, kcat = fitted["k0_per_min"], fitted["kcat_per_mM_min"]
    witness = []
    for t in (0.0, .5, 1., 2., 4., 8., 16.):
        inside = integrate(initial(), t, k0, kcat, 1)
        outside = integrate(initial(), t, k0, kcat, 0)
        witness.append({"time_min": t, "inside_witness_total_mM": float(sum(inside[2:])/VOLUME),
                        "outside_witness_total_mM": float(sum(outside[2:])/VOLUME),
                        "inside_witness_dense_mM_bulk_equivalent": float(inside[4]/VOLUME),
                        "outside_witness_dense_mM_bulk_equivalent": float(outside[4]/VOLUME)})
    sweep, examples = [], {}
    max_balance = 0.0
    for localization, q, escape, active in itertools.product((0, .5, 1), (0, .5, 1), (0, 1), (0, .5, 1)):
        for control in ("regeneration", "baseline_only", "no_regeneration"):
            rows, balance = passages(k0, kcat, localization, q, escape, active, control)
            max_balance = max(max_balance, max(map(abs, balance.values())))
            sweep.append({"localization": localization, "retained_dense_fraction": q, "escape_per_min": escape,
                          "active_fraction": active, "control": control,
                          **{k: v for k, v in rows[-1].items() if k not in
                             ("state_nmol", "discarded_cumulative_nmol", "feed_cumulative_nmol")},
                          "max_balance_error_nmol": max(map(abs,balance.values()))})
    example_specs = {
        "retentive_selected": dict(localization=1,q=.5,escape=0,active=1),
        "unretained_selected": dict(localization=0,q=.5,escape=0,active=1),
        "bulk_transfer": dict(localization=1,q=.5,escape=0,active=1,mode="bulk"),
        "pooled_transfer": dict(localization=1,q=.5,escape=0,active=1,mode="pooled"),
        "founder_free": dict(localization=1,q=.5,escape=0,active=1,seed=0),
        "founder_only": dict(localization=1,q=.5,escape=0,active=1,control="no_regeneration"),
    }
    for name, params in example_specs.items():
        rows, balance = passages(k0,kcat,**params)
        examples[name] = {"parameters": params, "passages": rows, "balance_error": balance}
    refined, _ = passages(k0,kcat,1,.5,1,1,rtol=1e-11)
    ordinary, _ = passages(k0,kcat,1,.5,1,1)
    refinement_error = float(np.max(np.abs(np.array(refined[-1]["state_nmol"])-ordinary[-1]["state_nmol"])))
    if max_balance > 1e-6 or refinement_error > 1e-6:
        raise ArithmeticError("Chemical accounting or numerical refinement failed")
    summary = {"data": {"train_observations": int(sum(train)), "holdout_observations": int(sum(holdout)),
                         "OD_observations": len(turbidity), "paired_assays": False},
               "product_dependent_fit": fitted, "no_autocatalysis_fit": baseline,
               "capacity_sensitivity": capacity, "OD_operational_windows": windows,
               "observation_witness_max_total_difference_mM": max(abs(r["inside_witness_total_mM"]-r["outside_witness_total_mM"]) for r in witness),
               "sweep_counts": {c: {"total": sum(r["control"]==c for r in sweep),
                                    "conditional_function_pass": sum(r["control"]==c and r["conditional_function_pass"] for r in sweep)}
                                for c in ("regeneration","baseline_only","no_regeneration")},
               "max_balance_error_nmol": max_balance, "refinement_error_nmol": refinement_error,
               "conclusion": "Bulk formation and observed turbidity do not identify active C3 retention or inherited catalytic function; transfer outcomes are assumption-dependent, not measured inheritance.",
               "examples": examples}
    write_json(output / "results.json", summary)
    write_csv(output / "fit_residuals.csv", residual_rows)
    write_csv(output / "rate_profile.csv", profile)
    write_csv(output / "observation_witnesses.csv", witness)
    write_csv(output / "conditional_transfer_sweep.csv", sweep)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    grid = np.linspace(0,16,300)
    axes[0,0].scatter(time[train],measured[train],label="Fit observations")
    axes[0,0].scatter(time[holdout],measured[holdout],label="Temporal holdout",marker="x")
    for name,p in (("Product-dependent",fitted),("No-autocatalysis",baseline)):
        axes[0,0].plot(grid,total_product(grid,p["k0_per_min"],p["kcat_per_mM_min"]),label=name)
    axes[0,0].set(xlabel="Time (min)",ylabel="Bulk C3 (mM)",title="Measured formation; fixed early-time fit")
    axes[0,0].legend(fontsize=8)
    for well in sorted({r["replicate_id"] for r in turbidity}):
        series=sorted((float(r["time_value"]),float(r["value"])) for r in turbidity if r["replicate_id"]==well)
        axes[0,1].plot(*zip(*series),label=well)
    axes[0,1].axvline(2,color="grey",linestyle=":",label="Hypothetical passage time")
    axes[0,1].set(xlabel="Time (min)",ylabel="OD650",title="Separate aliquots: no phase-volume inference")
    axes[0,1].legend(fontsize=8)
    for key,label in (("inside_witness_dense_mM_bulk_equivalent","All inside"),("outside_witness_dense_mM_bulk_equivalent","All outside")):
        axes[1,0].plot([r["time_min"] for r in witness],[r[key] for r in witness],label=label)
    axes[1,0].set(xlabel="Time (min)",ylabel="Dense C3 / total sample volume (mM)",title="Same bulk predictions, opposite retention")
    axes[1,0].legend(fontsize=8)
    for name in ("retentive_selected","unretained_selected","founder_only","founder_free"):
        rows=examples[name]["passages"]
        axes[1,1].plot([r["passage"] for r in rows],[r["retained_active_new_mM"] for r in rows],label=name)
    axes[1,1].set(xlabel="Hypothetical passage",ylabel="Retained active new C3 (mM)",title="Conditional transfer; no observed daughter lineages")
    axes[1,1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(output / "coupling.png",dpi=160)
    plt.close(fig)
    envelope=[r["kcat_per_mM_min"] for r in profile if r["within_descriptive_envelope"]]
    report=f'''# Measured droplet coupling result

The matched nominal Cys/PSS assays support a bulk C3 formation timecourse and a
separate turbidity lifetime. They do not measure active C3 retention, division,
daughter-specific activity or functional variant transmission.

Early-time product-dependent fit: k0={k0:.6g} /min, kcat={kcat:.6g} /mM/min;
training RMSE={fitted['train_RMSE_mM']:.6g} mM, temporal holdout RMSE={fitted['holdout_RMSE_mM']:.6g} mM.
No-autocatalysis baseline holdout RMSE={baseline['holdout_RMSE_mM']:.6g} mM.
The frozen 0.084 mM engineering tolerance gives product-dependent holdout pass:
{fitted['holdout_engineering_tolerance_pass']}. This is not an experimental confidence test.
The descriptive kcat profile envelope is {min(envelope) if envelope else None} to
{max(envelope) if envelope else None} /mM/min on the tested grid; it is not a confidence interval.
Late nonmonotonic concentrations and unresolved intermediate formation remain model limitations.
A product-dependent fit does not uniquely establish molecular autocatalysis.

OD 10%-peak crossing brackets: {windows}. Both measured wells exceed this
operational threshold at the assumed two-minute passage time. This establishes
assay-level temporal overlap only; OD is not retained catalyst or compartment mass.

Inside-only and outside-only witnesses have maximum bulk-prediction difference
{summary['observation_witness_max_total_difference_mM']:.3g} mM. This degeneracy is
conditional on pooled substrate and phase-independent activity, not a claim that
real phase-specific chemistry must be identical. No active C3 transport parameter
was inferred from CuII partition or tracer FRAP.

The {len(sweep)} conditional transfer cases are hypothetical 25 uL selective
collection and refill, with external scaffold support. Counts: {summary['sweep_counts']}.
Neither these counts nor the operational function threshold constitute measured
success probabilities or vertical inheritance. Random half-volume and pooled
controls can preserve bulk catalytic function without tracked mother-daughter
identity. The no-regeneration control forms no new C3; founder-free baseline
chemistry can start production, so recovery is not evidence of inherited information.
New C3 here is a chemical label, not a demonstrated descendant genotype.

Maximum chemical balance error={max_balance:.3g} nmol; tolerance-refinement
difference={refinement_error:.3g} nmol. Units, assumptions and source exclusions
are frozen in PROTOCOL.md. Raw row provenance is in fit_residuals.csv; complete
chemical histories and feed/discard ledgers are in results.json. The closed
batch consumes limited substrate; serial replenishment is externally imposed.

Needed measurements: active C3 inside/outside versus time in this exact recipe;
phase-specific catalytic rates; separately labeled founder and newly made C3;
tracked compartment division and daughter catalytic activity; variant identity
and selective transmission controls. Without them, simultaneous regeneration,
retention and inherited function remain unidentifiable. No living or intelligent
entity has been created or demonstrated.
'''
    (output / "REPORT.md").write_text(report)
    print(json.dumps({"output":str(output),"fit_holdout_RMSE_mM":fitted["holdout_RMSE_mM"],
                      "cases":len(sweep),"max_balance_error_nmol":max_balance}))


if __name__ == "__main__":
    main()
