"""Frozen transport calibration, retrospective held-out tests, and retained failures."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import shutil
import time

import numpy as np
from scipy.optimize import least_squares

from model import single_cycle, serial

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE = WORKSPACE / "measured-coupling-2026-10-15/rna_sources"
PRIOR = WORKSPACE / "rna-turnover-tests-2026-10-15"
PARAMETERS = {"legacy": ("mixing",), "bath": ("nu",), "patch": ("nu", "diffusion")}
BOUNDS = {"mixing": (0., 1.), "nu": (0., float(np.log10(30))), "diffusion": (-3., 1.)}
STARTS = ({"mixing": .05, "nu": .05, "diffusion": .95},
          {"mixing": .2, "nu": .2, "diffusion": .8},
          {"mixing": .4, "nu": .4, "diffusion": .6},
          {"mixing": .6, "nu": .6, "diffusion": .4},
          {"mixing": .8, "nu": .8, "diffusion": .2},
          {"mixing": .95, "nu": .95, "diffusion": .05})
MAX_NFEV = 120
FAILURES = (ArithmeticError, RuntimeError, ValueError, np.linalg.LinAlgError)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def write_csv(path, rows):
    with path.open("w", newline="") as stream:
        if not rows:
            stream.write("status\nunresolved_no_rows\n")
            return
        keys = list(dict.fromkeys(key for row in rows for key in row))
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def load():
    with (SOURCE / "observations.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    for i, row in enumerate(rows):
        row["row_id"] = f"observation_{i:03d}"
        for key in ("seed_uM", "hyper_a_uM", "x", "value_percent"):
            row[key] = float(row[key])
    if len(rows) != 148:
        raise ValueError("Expected the frozen 148 source observations")
    return rows


def split(rows):
    train = [r for r in rows if r["dataset"] == "Figure_2" and r["seed_uM"] in (0, 1) and r["x"] > 0]
    held = [r for r in rows if r["x"] > 0 and (r["dataset"] == "Figure_3" or
            (r["dataset"] == "Figure_2" and r["seed_uM"] == 2))]
    ids = {r["row_id"] for r in train + held}
    if len(train) != 18 or len(held) != 72 or len(ids) != 90:
        raise ValueError("Invalid frozen 18/72 disjoint split")
    conditions = {(r["seed_uM"], r["x"]) for r in train}
    if conditions != {(s, n) for s in (0, 1) for n in (1, 2, 3)}:
        raise ValueError("Calibration conditions differ from the frozen protocol")
    if sum(r["dataset"] == "Figure_2" for r in held) != 9:
        raise ValueError("Expected nine held-out Figure 2 observations")
    return train, held


def decode(family, values, fixed=None):
    fixed = fixed or {}
    free = [name for name in PARAMETERS[family] if name not in fixed]
    return {**{name: float(value if name == "mixing" else 10**value)
               for name, value in zip(free, values)}, **fixed}


def calibration_predictions(family, parameters, rows, rtol=1e-8):
    values = {(seed, cycles): single_cycle(seed, family, parameters, int(cycles), rtol=rtol)["yield_percent"]
              for seed, cycles in sorted({(r["seed_uM"], r["x"]) for r in rows})}
    output = np.array([values[r["seed_uM"], r["x"]] for r in rows])
    if np.any(~np.isfinite(output)):
        raise ArithmeticError("Nonfinite calibration prediction")
    return output


def fit(family, rows, path, fixed=None):
    fixed = fixed or {}
    free = [name for name in PARAMETERS[family] if name not in fixed]
    details = {"family": family, "resolved": False, "complete": False,
               "training_row_ids": [r["row_id"] for r in rows], "fixed_parameters": fixed,
               "free_parameters": free, "starts": [], "max_nfev": MAX_NFEV}
    save(path, details)
    targets = np.array([r["value_percent"] for r in rows])
    residual_calls = 0

    def residual(values):
        nonlocal residual_calls
        residual_calls += 1
        return calibration_predictions(family, decode(family, values, fixed), rows) - targets

    if not free:
        try:
            errors = residual([])
            details.update(resolved=True, parameters=fixed, sse=float(errors @ errors),
                           rmse_pp=float(np.sqrt(np.mean(errors**2))), qualified=True,
                           direct_objective=True)
        except FAILURES as error:
            details["error"] = f"{type(error).__name__}: {error}"
        details.update(complete=True, residual_evaluations=residual_calls)
        save(path, details)
        return details
    low, high = np.array([BOUNDS[name] for name in free]).T
    successful = []
    for start_id, fractions in enumerate(STARTS, 1):
        start = low + (high-low)*np.array([fractions[name] for name in free])
        begun, calls_before = time.monotonic(), residual_calls
        entry = {"start_id": start_id, "optimizer_start": start.tolist()}
        try:
            result = least_squares(residual, start, bounds=(low, high), max_nfev=MAX_NFEV,
                                   jac="3-point", diff_step=1e-3, xtol=1e-8, ftol=1e-8, gtol=1e-8)
            finite = bool(np.all(np.isfinite(result.fun)) and np.all(np.isfinite(result.x)))
            entry.update(success=bool(result.success and finite), status=int(result.status),
                         nfev=int(result.nfev), njev=int(result.njev or 0),
                         sse=float(result.fun @ result.fun) if finite else None,
                         message=str(result.message), active_bounds=result.active_mask.tolist(),
                         optimizer_parameters=result.x.tolist() if finite else None)
            if entry["success"]:
                successful.append(result)
        except FAILURES as error:
            entry.update(success=False, status=None, nfev=None, njev=None, sse=None,
                         message=f"{type(error).__name__}: {error}", active_bounds=None)
        entry.update(elapsed_seconds=time.monotonic()-begun,
                     residual_evaluations=residual_calls-calls_before)
        details["starts"].append(entry)
        save(path, details)
    details.update(complete=True, residual_evaluations=residual_calls, qualified=False)
    if successful:
        best = min(successful, key=lambda result: float(result.fun @ result.fun))
        sse = float(best.fun @ best.fun)
        agreements = sum(abs(float(result.fun @ result.fun)-sse) <= max(1e-4, 1e-4*sse)
                         for result in successful)
        details.update(resolved=True, parameters=decode(family, best.x, fixed), sse=sse,
                       rmse_pp=float(np.sqrt(sse/len(rows))), active_bounds=best.active_mask.tolist(),
                       successful_starts=len(successful), agreeing_successful_starts=agreements,
                       qualified=agreements >= 2,
                       jacobian_singular_values=np.linalg.svd(best.jac, compute_uv=False).tolist())
    save(path, details)
    return details


def metrics(rows, qualified=True):
    if not rows:
        return {"resolved": False, "n": 0, "adequate": False}
    errors = np.array([r["error_pp"] for r in rows])
    if np.any(~np.isfinite(errors)):
        raise ValueError("Nonfinite errors cannot produce a score")
    groups = {(r["dataset"], r["seed_uM"], r["x"]) for r in rows}
    mean_errors = [np.mean([r["error_pp"] for r in rows
                           if (r["dataset"], r["seed_uM"], r["x"]) == group]) for group in groups]
    rmse, maximum = float(np.sqrt(np.mean(errors**2))), float(max(abs(e) for e in mean_errors))
    screen = rmse <= 2 and maximum <= 4
    return {"resolved": True, "n": len(rows), "n_conditions": len(groups), "rmse_pp": rmse,
            "max_absolute_condition_mean_error_pp": maximum,
            "max_absolute_replicate_error_pp": float(np.max(np.abs(errors))),
            "bias_pp": float(errors.mean()), "threshold_screen_pass": screen,
            "numerical_eligible": bool(qualified), "adequate": bool(screen and qualified)}


def scenarios():
    yield "legacy", True, True
    for family in ("bath", "patch"):
        for reactive in (True, False):
            for carried in (True, False):
                yield family, reactive, carried


def scenario_name(family, reactive, carried):
    return family if family == "legacy" else f"{family}|reactive-{int(reactive)}|carried-{int(carried)}"


def predict_scenario(family, parameters, rows, reactive, carried, rtol=1e-8):
    options = {"exterior_reactive": reactive, "exterior_carried": carried, "rtol": rtol}
    trajectories, stages, values = [], [], {}
    for seed in (0, 1, 2):
        trajectory, stage = serial(seed, family, parameters, return_stages=True, **options)
        trajectories.extend({"seed_uM": seed, **r} for r in trajectory)
        stages.extend({"seed_uM": seed, **r} for r in stage)
        for generation, result in enumerate(trajectory):
            values["Figure_3", seed, generation] = result["yield_percent"]
        for cycles in (1, 2, 3):
            values["Figure_2", seed, cycles] = single_cycle(seed, family, parameters, cycles, **options)["yield_percent"]
    pred = []
    for row in rows:
        value = float(values[row["dataset"], row["seed_uM"], row["x"]])
        if not np.isfinite(value):
            raise ArithmeticError("Nonfinite transport prediction")
        stage = "calibration" if row["dataset"] == "Figure_2" and row["seed_uM"] in (0, 1) else "held_out"
        pred.append({**row, "stage": stage, "predicted_percent": value, "error_pp": value-row["value_percent"]})
    return pred, trajectories, stages


def contrasts(trajectories):
    output = []
    for generation in range(8):
        by_seed = {r["seed_uM"]: r for r in trajectories if r["generation"] == generation}
        for seed in (1, 2):
            base, seeded = by_seed[0], by_seed[seed]
            output.append({"generation": generation, "contrast": f"{seed}-0",
                           **{key: float(value-base[key]) for key, value in seeded.items()
                              if key not in ("generation", "seed_uM") and isinstance(value, (float, int))
                              and isinstance(base.get(key), (float, int))}})
    return output


def prior_inventory():
    files = [p for directory in ("results-v1", "verification-v1")
             for p in sorted((PRIOR/directory).rglob("*")) if p.is_file()]
    files += [PRIOR/name for name in ("model.py", "run.py", "PROTOCOL.md", "REPORT.md") if (PRIOR/name).exists()]
    files += [SOURCE/name for name in ("observations.csv", "conditions.json", "raw/salibi_data.xlsx")]
    return {str(p.relative_to(WORKSPACE)): digest(p) for p in files}


def freeze(output):
    names = ("PROTOCOL.md", "WORKPLAN.md", "model.py", "test_model.py", "run.py", "test_validation.py",
             "plot.py", "requirements.txt")
    files = [ROOT/name for name in names]
    files += [p for folder in ("research", "diagnosis", "independent") for p in sorted((ROOT/folder).rglob("*"))
              if p.is_file() and p.suffix in (".py", ".json", ".md", ".csv") and "__pycache__" not in p.parts]
    files += [SOURCE/name for name in ("observations.csv", "conditions.json", "raw/salibi_data.xlsx")]
    files += [PRIOR/"results-v1/fits/baseline__omit-none.json"]
    hashes = {}
    for source in files:
        relative = source.relative_to(WORKSPACE)
        target = output/"frozen"/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[str(relative)] = digest(target)
    runtime = {"python": platform.python_version(), **{name: version(name) for name in
               ("numpy", "scipy", "matplotlib", "openpyxl")}}
    save(output/"freeze.json", {"utc_before_fit": datetime.now(timezone.utc).isoformat(),
                               "files": hashes, "runtime": runtime, "starts": STARTS, "bounds": BOUNDS,
                               "max_nfev": MAX_NFEV, "classification": "retrospective previously inspected data"})
    save(output/"prior_integrity_before.json", prior_inventory())


def profiles(train, output):
    records = []
    for family, name in (("bath", "nu"), ("patch", "nu"), ("patch", "diffusion")):
        for index, value in enumerate(np.logspace(*BOUNDS[name], 9)):
            detail = fit(family, train, output/"fits"/f"profile__{family}__{name}__{index}.json", {name: float(value)})
            records.append({"family": family, "parameter": name, "fixed_value": float(value), "fit": detail})
            save(output/"profiles.json", records)
            print("PROFILE", family, name, index, "resolved", detail["resolved"], flush=True)
    return records


def run(output):
    expected = {"python": "3.12.3", "numpy": "2.4.1", "scipy": "1.16.1", "matplotlib": "3.10.8", "openpyxl": "3.1.3"}
    actual = {"python": platform.python_version(), **{name: version(name) for name in expected if name != "python"}}
    if actual != expected:
        raise RuntimeError(f"Pinned runtime required: expected {expected}, found {actual}")
    output.mkdir(parents=True, exist_ok=False)
    (output/"fits").mkdir()
    freeze(output)
    begun = time.monotonic()
    rows = load()
    train, held = split(rows)
    used = train + held
    save(output/"splits.json", {"training_row_ids": [r["row_id"] for r in train],
                               "evaluation_row_ids": [r["row_id"] for r in held],
                               "excluded_row_ids": [r["row_id"] for r in rows if r not in used],
                               "classification": "retrospective; all observations previously inspected"})
    fits = {}
    for family in PARAMETERS:
        fits[family] = fit(family, train, output/"fits"/f"{family}.json")
        save(output/"fits.json", fits)
        print("FIT", family, "resolved", fits[family]["resolved"], flush=True)
    profile_records = profiles(train, output)
    results, predictions, refined_predictions, trajectories, stages, seed_contrasts = {}, [], [], [], [], []
    refined_trajectories, refined_stages = [], []
    for family, reactive, carried in scenarios():
        name = scenario_name(family, reactive, carried)
        detail = {"family": family, "exterior_reactive": reactive, "exterior_carried": carried,
                  "resolved": False, "fit_qualified": fits[family].get("qualified", False)}
        try:
            if not fits[family]["resolved"]:
                raise ArithmeticError("Calibration fit unresolved")
            parameters = fits[family]["parameters"]
            pred, trajectory, stage = predict_scenario(family, parameters, used, reactive, carried)
            predictions.extend({"scenario": name, **r} for r in pred)
            trajectories.extend({"scenario": name, **r} for r in trajectory)
            stages.extend({"scenario": name, **r} for r in stage)
            seed_contrasts.extend({"scenario": name, **r} for r in contrasts(trajectory))
            detail.update(parameters=parameters, prediction_resolved=True)
            fine, fine_trajectory, fine_stages = predict_scenario(family, parameters, used, reactive, carried, rtol=1e-10)
            delta = max(abs(a["predicted_percent"]-b["predicted_percent"]) for a, b in zip(pred, fine))
            balance = max(r["moiety_balance_max_error_uM"] for r in stage + fine_stages)
            numeric = delta <= 1e-4 and balance <= 1e-6
            eligible = detail["fit_qualified"] and numeric
            test = [r for r in pred if r["stage"] == "held_out"]
            detail.update(resolved=True, parameters=parameters, numerical_eligible=eligible,
                          refinement={"pass": numeric, "max_prediction_difference_pp": delta,
                                      "max_moiety_error_uM": balance},
                          calibration=metrics([r for r in pred if r["stage"] == "calibration"], eligible),
                          held_out=metrics(test, eligible),
                          held_out_seed2=metrics([r for r in test if r["dataset"] == "Figure_2"], eligible),
                          held_out_serial=metrics([r for r in test if r["dataset"] == "Figure_3"], eligible))
            refined_predictions.extend({"scenario": name, **r} for r in fine)
            refined_trajectories.extend({"scenario": name, **r} for r in fine_trajectory)
            refined_stages.extend({"scenario": name, **r} for r in fine_stages)
        except FAILURES as error:
            detail["error"] = f"{type(error).__name__}: {error}"
        results[name] = detail
        save(output/"scenarios.json", results)
        for filename, records in (("predictions.csv", predictions), ("refined_predictions.csv", refined_predictions),
                                  ("trajectories.csv", trajectories), ("stages.csv", stages), ("seed_contrasts.csv", seed_contrasts)):
            write_csv(output/filename, records)
        write_csv(output/"refined_trajectories.csv", refined_trajectories)
        write_csv(output/"refined_stages.csv", refined_stages)
        print("SCENARIO", name, "resolved", detail["resolved"], flush=True)
    after = prior_inventory()
    save(output/"prior_integrity_after.json", after)
    unchanged = after == json.loads((output/"prior_integrity_before.json").read_text())
    summary = {"classification": "retrospective held-out validation; no model selection", "fits": fits,
               "scenarios": results, "all_profiles_resolved": all(r["fit"]["resolved"] for r in profile_records),
               "all_profiles_qualified": all(r["fit"].get("qualified", False) for r in profile_records),
               "prior_files_unchanged": unchanged, "elapsed_seconds": time.monotonic()-begun,
               "scientific_limit": "Fixed bulk chemistry is inadequate; PAGE does not identify active catalyst or transport parameters."}
    save(output/"summary.json", summary)
    from plot import plot
    plot(output)
    save(output/"manifest.json", {str(p.relative_to(output)): digest(p) for p in sorted(output.rglob("*"))
                                 if p.is_file() and p.name != "manifest.json"})
    if not unchanged:
        raise RuntimeError("Prior evidence changed during execution")
    print(json.dumps({"finished": str(output), "scenarios_resolved": sum(r["resolved"] for r in results.values()),
                      "prior_files_unchanged": unchanged, "elapsed_seconds": summary["elapsed_seconds"]}, indent=2))


def development(output):
    output.mkdir(parents=True, exist_ok=False)
    timing = {}
    for family, truth in (("legacy", {"mixing": .37}), ("bath", {"nu": 4.}),
                          ("patch", {"nu": 4., "diffusion": .3})):
        rows = [{"row_id": f"synthetic_{s}_{n}_{rep}", "seed_uM": s, "x": n,
                 "value_percent": single_cycle(s, family, truth, n)["yield_percent"]}
                for s in (0, 1) for n in (1, 2, 3) for rep in (1, 2, 3)]
        begun = time.monotonic()
        detail = fit(family, rows, output/f"{family}.json")
        timing[family] = {"seconds": time.monotonic()-begun, "truth": truth,
                          "resolved": detail["resolved"], "qualified": detail.get("qualified", False),
                          "fitted_parameters": detail.get("parameters"), "rmse_pp": detail.get("rmse_pp"),
                          "synthetic_predictions_recovered": detail["resolved"] and detail["rmse_pp"] < 1e-3}
        save(output/"timing.json", {"classification": "synthetic implementation check only", "fits": timing})
        print(family, timing[family], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args()
    development(args.output) if args.development else run(args.output)
