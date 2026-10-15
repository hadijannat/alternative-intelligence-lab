"""Independent accounting, split/score checks and saved-parameter replay; no fitting."""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from dataclasses import asdict, replace
from importlib.metadata import version
import platform

import numpy as np
import scipy

from model import MOIETIES, NAMES, Parameters, bulk_curves, initial_complexes, react, serial, single_cycle

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE_NAME = "measured-coupling-2026-10-15/rna_sources/observations.csv"
PARAMETERS = {
    "baseline": ("kf", "kh", "kb", "ka", "krh", "kd"),
    "release": ("kf", "kh", "kb", "ka", "krh", "kd", "krel"),
    "reversible_free": ("kf", "kh", "kb", "ka", "krh", "kd", "krel", "kbind"),
    "reversible_equilibrium": ("kf", "kh", "kb", "ka", "krh", "kd", "krel", "kbind"),
}
BOUNDS = {"kf": [-4, 1], "kh": [-8, 0], "kb": [-2, 2], "ka": [-4, 1],
          "krh": [-8, 0], "kd": [-6, 0], "krel": [-4, 2], "kbind": [-6, 2]}
START_NAMES = ("kf", "kh", "kb", "ka", "krh", "kd", "krel", "kbind")
STARTS = [dict(zip(START_NAMES, row)) for row in (
    (-1, -5, 0, -1, -4, -2, -1, -2), (-.5, -3, 1, -.5, -2, -1, 0, 0),
    (-1.5, -6, -1, -1.5, -6, -3, -3, -4), (.2, -4, 1.8, -2, -3, -4, 1, 1),
    (-2, -2, -1.8, .5, -1, -.3, .5, -5), (.8, -7, .5, -.2, -7, -5, -2, .5))]
EXPECTED_NAMES = ("A", "R", "B", "F", "P", "D", "QFF", "QFP", "QFD", "QDD", "QDP", "QPP")
EXPECTED_MOIETIES = np.array([[1, 0, 0, 1, 0, 1, 2, 1, 2, 2, 1, 0],
                             [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2],
                             [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]], float)
CLOCK_KEYS = {"elapsed_seconds", "utc_before_fit"}
DIFFERENCES = {}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, label="value"):
    require(math.isfinite(float(actual)) and math.isfinite(float(expected)), f"{label}: nonfinite")
    difference, tolerance = abs(actual-expected), 1e-8 + 1e-8*abs(expected)
    require(difference <= tolerance, f"{label}: {actual!r} != {expected!r}")
    scope = "fresh_refit" if label.startswith("Refit ") else "replay_and_independent_arithmetic"
    stats = DIFFERENCES.setdefault(scope, {"comparisons": 0, "maximum_absolute_difference": 0.,
        "maximum_fraction_of_tolerance": 0., "largest_absolute_difference_label": None})
    stats["comparisons"] += 1
    if difference > stats["maximum_absolute_difference"]:
        stats["maximum_absolute_difference"] = float(difference)
        stats["largest_absolute_difference_label"] = label
    stats["maximum_fraction_of_tolerance"] = max(stats["maximum_fraction_of_tolerance"], float(difference/tolerance))


def compare(actual, expected, label="root", ignore_clocks=False):
    """Booleans, integers, identifiers and structure match exactly; real values use protocol tolerance."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict), label)
        excluded = CLOCK_KEYS if ignore_clocks else set()
        require(set(actual)-excluded == set(expected)-excluded, f"{label}: key mismatch")
        for key in expected.keys()-excluded:
            compare(actual[key], expected[key], f"{label}.{key}", ignore_clocks)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), f"{label}: length/type mismatch")
        for i, (a, b) in enumerate(zip(actual, expected)):
            compare(a, b, f"{label}[{i}]", ignore_clocks)
    elif isinstance(expected, float):
        require(isinstance(actual, (int, float)) and not isinstance(actual, bool), label)
        close(actual, expected, label)
    else:
        require(type(actual) is type(expected) and actual == expected, f"{label}: {actual!r} != {expected!r}")


def read_json(path):
    return json.loads(path.read_text())


def read_csv(path):
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    return [] if rows == [{"status": "unresolved_no_predictions"}] else rows


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows(path):
    rows = read_csv(path)
    for i, row in enumerate(rows):
        row["row_id"] = f"observation_{i:03d}"
        for key in ("seed_uM", "hyper_a_uM", "x", "value_percent"):
            row[key] = float(row[key])
        row["group_id"] = f"{row['dataset']}|{row['seed_uM']:g}|{row['hyper_a_uM']:g}"
    return rows


def check_source_row(saved, original):
    for key, value in original.items():
        if isinstance(value, float):
            close(float(saved[key]), value, f"Source value {key}")
        else:
            require(saved[key] == value, f"Source field changed: {key}")


def score(rows, transport=False):
    errors = np.array([float(r["error_pp"]) for r in rows if float(r["x"]) > 0])
    require(len(errors) > 0 and np.all(np.isfinite(errors)), "Score needs finite positive-time observations")
    rmse, maximum = float(np.sqrt(np.mean(errors**2))), float(np.max(np.abs(errors)))
    result = {"resolved": True, "n_positive": len(errors), "rmse_pp": rmse,
              "maximum_absolute_error_pp": maximum, "bias_pp": float(errors.mean()),
              "historical_all_rows_rmse_pp": float(np.sqrt(np.mean([float(r["error_pp"])**2 for r in rows]))),
              "adequate": rmse <= 2 and maximum <= 4}
    if transport:
        buckets = {}
        for r in rows:
            if float(r["x"]) > 0:
                buckets.setdefault((r["dataset"], float(r["seed_uM"]), float(r["x"])), []).append(float(r["error_pp"]))
        maximum = float(max(abs(np.mean(values)) for values in buckets.values()))
        result.update(maximum_absolute_group_mean_error_pp=maximum, adequate=rmse <= 2 and maximum <= 4)
    return result


def check_score(saved, rows, label, transport=False, numerical_eligible=None):
    for key, value in score(rows, transport).items():
        if key == "adequate" and "threshold_screen_pass" in saved:
            compare(saved["threshold_screen_pass"], value, f"{label}.threshold_screen_pass")
            eligible = saved.get("numerical_eligible", True) if numerical_eligible is None else numerical_eligible
            value = value and eligible
        compare(saved[key], value, f"{label}.{key}")


def choose(scores):
    eligible = [s for s in scores if s["resolved"] and s["rmse_pp"] is not None]
    if not eligible:
        return None
    minimum = min(s["rmse_pp"] for s in eligible)
    return min((s["candidate"] for s in eligible if s["rmse_pp"] <= minimum+.25),
               key=lambda c: (len(PARAMETERS[c]), c))


def prediction(p, rows):
    doses = sorted({r["group_id"] for r in rows})
    times = sorted({r["x"] for r in rows})
    reps = [next(r for r in rows if r["group_id"] == g) for g in doses]
    values = bulk_curves(p, [r["seed_uM"] for r in reps], [r["hyper_a_uM"] for r in reps], times)
    return [float(values[doses.index(r["group_id"]), times.index(r["x"])]) for r in rows]


def check_evaluation(detail, evaluation, held):
    if not detail["resolved"]:
        require(not evaluation["resolved"], "Unresolved fit cannot resolve evaluation")
    elif not evaluation["resolved"]:
        require(isinstance(evaluation.get("error"), str), "Missing held prediction failure")
        try:
            prediction(Parameters(**detail["parameters"]), held)
        except (RuntimeError, ArithmeticError, ValueError):
            return
        raise AssertionError("Recorded held prediction failure did not reproduce")


def check_fit(detail, candidate, training, fixed=None):
    fixed = fixed or {}
    ids = [r["row_id"] for r in training]
    free = [n for n in PARAMETERS[candidate] if n not in fixed]
    require(all(r["x"] > 0 for r in training), "Zero time in training")
    compare(detail["candidate"], candidate)
    compare(detail["training_row_ids"], ids)
    compare(detail["training_groups"], sorted({r["group_id"] for r in training}))
    compare(detail["fixed_parameters"], fixed)
    compare(detail["free_parameters"], free)
    require(detail["complete"] and detail["max_nfev"] == 160 and detail["n_observations"] == len(ids), "Fit completeness/budget")
    require(len(detail["starts"]) == 6, "All six starts must be retained")
    require(detail["residual_evaluations"] == sum(s["residual_evaluations"] for s in detail["starts"]),
            "Residual evaluation accounting")
    successes = []
    for i, start in enumerate(detail["starts"]):
        require(start["start_id"] == i+1, "Start order")
        compare(start["log10_start"], [float(STARTS[i][n]) for n in free])
        require(type(start["start_id"]) is int and type(start["success"]) is bool, "Start receipt types")
        require(start["nfev"] is None or type(start["nfev"]) is int and 0 <= start["nfev"] <= 160, "Evaluation budget exceeded")
        require(start["njev"] is None or type(start["njev"]) is int and start["njev"] >= 0, "Jacobian evaluation receipt")
        require(type(start["residual_evaluations"]) is int and start["residual_evaluations"] >= (start["nfev"] or 0),
                "Residual evaluation receipt")
        require(math.isfinite(start["elapsed_seconds"]) and start["elapsed_seconds"] >= 0, "Elapsed receipt")
        if start["sse"] is not None:
            require(math.isfinite(start["sse"]) and start["sse"] >= 0, "Nonfinite objective")
            values = start["log10_parameters"]
            require(len(values) == len(free) and all(math.isfinite(v) and BOUNDS[n][0]-1e-12 <= v <= BOUNDS[n][1]+1e-12
                    for n, v in zip(free, values)), "Finite start parameter bounds")
            require(len(start["active_bounds"]) == len(free) and all(type(v) is int and v in (-1, 0, 1) for v in start["active_bounds"]),
                    "Active bound receipt")
            parameters = dict(zip(free, 10**np.array(values)))
            parameters.update(fixed)
            replay = Parameters(**parameters, turnover=candidate != "baseline", equilibrated=candidate == "reversible_equilibrium")
            residuals = np.array(prediction(replay, training))-[r["value_percent"] for r in training]
            close(start["sse"], float(residuals@residuals), "Every finite start objective")
        else:
            require(not start["success"], "Successful start without finite objective")
        if start["success"]:
            require(type(start["status"]) is int and start["status"] in (1, 2, 3, 4) and start["sse"] >= 0, "Invalid successful optimizer termination")
            require(len(start["log10_parameters"]) == len(free), "Parameter dimension")
            require(all(BOUNDS[n][0]-1e-12 <= v <= BOUNDS[n][1]+1e-12 for n, v in zip(free, start["log10_parameters"])), "Parameter outside registered bounds")
            successes.append(start)
        require(isinstance(start["message"], str), "Missing optimizer receipt")
    require(detail["resolved"] == bool(successes), "Failed starts cannot resolve fit")
    if successes:
        best = min(successes, key=lambda s: s["sse"])
        close(detail["sse"], best["sse"], "Best successful SSE")
        compare(detail["active_bounds"], best["active_bounds"], "Winning bound receipt")
        values = dict(zip(free, 10**np.array(best["log10_parameters"])))
        values.update(fixed)
        p = Parameters(**values, turnover=candidate != "baseline",
                       equilibrated=candidate == "reversible_equilibrium")
        compare(detail["parameters"], asdict(p), "Selected start parameters")
        errors = np.array(prediction(p, training)) - [r["value_percent"] for r in training]
        close(detail["sse"], float(errors@errors), "Replayed training SSE")
        close(detail["rmse_pp"], float(np.sqrt(np.mean(errors**2))), "Replayed training RMSE")
        count = sum(abs(s["sse"]-best["sse"]) <= max(1e-4, 1e-4*best["sse"]) for s in successes)
        require(detail["successful_starts"] == len(successes) and detail["agreeing_successful_starts"] == count and detail["two_starts_agree"] == (count >= 2), "Multistart accounting")
        singular = detail["jacobian_singular_values"]
        require(len(singular) == len(free) and all(math.isfinite(x) and x >= 0 for x in singular), "Jacobian diagnostics")
    return bool(successes)


def challenge_rows(bulk, kind):
    require(kind in ("late", "joint"), "Unknown challenge")
    high = {r["group_id"] for r in bulk if r["seed_uM"] == 1 or r["hyper_a_uM"] == 2.5}
    training = [r for r in bulk if r["x"] in (15, 30) and (kind == "late" or r["group_id"] not in high)]
    held = [r for r in bulk if r["x"] in (45, 60) and (kind == "late" or r["group_id"] in high)]
    require((len(training), len(held)) == ((16, 16) if kind == "late" else (12, 4)), "Challenge dimensions")
    require(not {r["row_id"] for r in training} & {r["row_id"] for r in held}, "Challenge row leakage")
    if kind == "joint":
        require(len(high) == 2 and not {r["group_id"] for r in training} & {r["group_id"] for r in held},
                "Joint high-dose leakage")
    return training, held


def inventories(x):
    """Registered observer and competence arithmetic, independent of model helpers."""
    x = np.asarray(x)
    return x[..., 3]+2*x[..., 6]+x[..., 7]+x[..., 8], x[..., 4]+x[..., 7]+x[..., 10]+2*x[..., 11]


def bulk_inventory(p, rows):
    doses = sorted({r["group_id"] for r in rows})
    reps = [next(r for r in rows if r["group_id"] == g) for g in doses]
    x = np.zeros((len(doses), 12))
    x[:, 0], x[:, 1], x[:, 2], x[:, 3] = [r["hyper_a_uM"] for r in reps], 5, 7.5, [r["seed_uM"] for r in reps]
    x = initial_complexes(x, p)
    times = [0, 15, 30, 45, 60]
    coarse = react(x, 60, p, times=times)
    fine = react(x, 60, p, times=times, rtol=1e-10)
    separate = np.concatenate([react(x[i:i+1], 60, p, times=times) for i in range(len(x))], axis=1)
    def observer(y):
        product = inventories(y)[1]
        return 100*product/(y[..., 1]+product)
    delta = float(np.max(np.abs(observer(coarse)-observer(fine))))
    batch = float(np.max(np.abs(observer(coarse)-observer(separate))))
    balance = float(np.max(np.abs(coarse@EXPECTED_MOIETIES.T-(x@EXPECTED_MOIETIES.T)[None])))
    states = []
    for gi, group in enumerate(doses):
        for ti, minutes in enumerate(times):
            y = coarse[ti, gi]
            competent, product = inventories(y)
            states.append({"group_id": group, "minutes": minutes,
                **{name+"_uM": float(v) for name, v in zip(EXPECTED_NAMES, y)},
                "competent_total_model_uM": float(competent), "PAGE_product_model_uM": float(product)})
    return {"maximum_tolerance_difference_pp": delta, "maximum_batch_difference_pp": batch,
            "maximum_moiety_error_uM": balance,
            "pass": delta < 1e-4 and batch < 1e-4 and balance < 1e-7}, states


def check_inventories(saved, expected):
    require(len(saved) == len(expected), "Inventory coverage")
    for a, b in zip(saved, expected):
        for name, value in b.items():
            if isinstance(value, (int, float)):
                close(float(a[name]), value, f"Inventory {name}")
                require(name == "fixed_log10" or float(a[name]) >= 0, "Negative inventory")
            else:
                require(a[name] == value, f"Inventory identity {name}")


def scenarios(selected):
    result = {}
    for candidate in PARAMETERS:
        for reset in ((False, True) if candidate == selected and candidate != "baseline" else (False,)):
            for mode, loss in itertools.product(("fractional", "contact"), ("uniform", "all_or_none")):
                key = f"{candidate}|{mode}|{loss}|reset-{int(reset)}"
                result[key] = {"candidate": candidate, "mixing_mode": mode, "loss_closure": loss,
                               "complex_reset": reset, "scenario": key}
    return result


def check_trajectory(rows, p, seed):
    require([r["generation"] for r in rows] == list(range(8)), "Serial generation coverage")
    for row in rows:
        x = np.array([row[n+"_uM"] for n in EXPECTED_NAMES])
        require(np.all(np.isfinite(x)) and np.all(x >= 0), "Serial states")
        competent, product = inventories(x)
        close(row["competent_total_model_uM"], competent, "Serial competent inventory")
        close(row["yield_percent"], 100*product/(x[1]+product) if x[1]+product else 0., "Serial PAGE observer")
        g = row["generation"]
        founder = seed/3 if g == 0 else seed/3*.55**g*.5**(g-1)*math.exp(-60*p.kd*g)
        close(row["founder_competent_model_uM"], founder, "Total competent founder expectation")
        close(row["newly_generated_competent_model_uM"], max(0, competent-founder), "New competent expectation")
        compare(row["retained_moiety_uM"], (EXPECTED_MOIETIES@x).tolist(), "Serial retained moieties")
        error = np.max(np.abs(np.array(row["source_moiety_uM"])-row["removed_moiety_uM"]-row["retained_moiety_uM"]))
        close(row["moiety_balance_max_error_uM"], float(error), "Serial balance arithmetic")


def check_mixing(detail, template, training):
    require(detail["complete"], "Incomplete mixing fit")
    compare(detail["training_row_ids"], [r["row_id"] for r in training], "Mixing training IDs")
    compare(detail["fitted_parameters"], ["mixing"], "Only mixing fitted")
    compare(detail["bounds"], [0, 1], "Mixing bounds")
    compare(detail["frozen_chemistry_parameters"], asdict(template), "Frozen transport chemistry")
    require(detail["n"] == 18, "Mixing training count")
    for entry in detail["evaluations"]:
        require(math.isfinite(entry["mixing"]) and 0 <= entry["mixing"] <= 1, "Mixing evaluation bounds")
        try:
            p = replace(template, mixing=entry["mixing"])
            values = {(seed, n): single_cycle(p, seed, n) for seed in (0, 1) for n in (1, 2, 3)}
            sse = sum((values[r["seed_uM"], r["x"]]-r["value_percent"])**2 for r in training)
            if not math.isfinite(sse):
                raise ArithmeticError("Nonfinite transport mixing SSE")
        except (RuntimeError, ArithmeticError, ValueError) as error:
            require(not entry["resolved"] and entry["error"] == f"{type(error).__name__}: {error}", "Mixing failure receipt")
        else:
            require(entry["resolved"], "Unreproduced mixing failure")
            close(entry["sse"], sse, "Mixing evaluation objective")
    if detail["resolved"]:
        require(detail["success"] and detail["nfev"] == len(detail["evaluations"]), "Mixing optimizer receipt")
        require(any(e["resolved"] and e["mixing"] == detail["mixing"] and e["sse"] == detail["sse"]
                    for e in detail["evaluations"]), "Missing winning mixing evaluation")
        close(detail["rmse_pp"], math.sqrt(detail["sse"]/18), "Mixing RMSE")
    else:
        require(isinstance(detail.get("error"), str), "Unresolved mixing receipt")


def check_transport(directory, rows, full, selected, numerical):
    transport = read_json(directory/"transport.json")
    predictions = read_csv(directory/"transport_predictions.csv")
    trajectories = read_json(directory/"transport_trajectories.json")
    refinements = read_json(directory/"transport_refinement.json")
    expected_scenarios = scenarios(selected)
    require(set(transport) == set(expected_scenarios), "Registered transport scenario coverage")
    require(all(r["scenario"] in transport for r in predictions+refinements), "Unknown transport scenario")
    training = [r for r in rows if r["dataset"] == "Figure_2" and r["seed_uM"] in (0, 1) and r["x"] > 0]
    train_ids = {r["row_id"] for r in training}
    held_ids = {r["row_id"] for r in rows if r["x"] > 0 and (r["dataset"] == "Figure_3" or
               (r["dataset"] == "Figure_2" and r["seed_uM"] == 2))}
    require(len(train_ids) == 18 and len(held_ids) == 72 and not train_ids & held_ids, "Transport partition")
    expected_files, trajectory_keys = set(), set()
    for key, metadata in expected_scenarios.items():
        detail = transport[key]
        for name, value in metadata.items():
            compare(detail[name], value, "Scenario metadata")
        saved = [r for r in predictions if r["scenario"] == key]
        checks = [r for r in refinements if r["scenario"] == key]
        candidate, mode, loss, reset = (metadata[n] for n in ("candidate", "mixing_mode", "loss_closure", "complex_reset"))
        if not full[candidate]["resolved"]:
            require(not detail["resolved"] and not saved and not checks and key not in trajectories,
                    "Transport from unresolved chemistry")
            require(detail["error"] == "Full-data chemistry unresolved", "Unresolved chemistry receipt")
            continue
        filename = f"{candidate}__{mode}__{loss}__reset-{int(reset)}.json"
        expected_files.add(filename)
        mixing = read_json(directory/"mixing_fits"/filename)
        template = replace(Parameters(**full[candidate]["parameters"]), transport=mode, loss=loss, complex_reset=reset)
        check_mixing(mixing, template, training)
        compare(detail["mixing_fit"], mixing, "Mixing cache")
        if not mixing["resolved"]:
            require(not detail["resolved"] and not saved and not checks and key not in trajectories, "Unresolved mixing outputs")
            require(isinstance(detail.get("error"), str), "Missing mixing failure")
            continue
        p = replace(template, mixing=mixing["mixing"])
        try:
            regenerated = {str(seed): [{**metadata, **r} for r in serial(p, seed)] for seed in (0, 1, 2)}
            cycles = {(seed, n): single_cycle(p, seed, n) for seed in (0, 1, 2) for n in (0, 1, 2, 3)}
        except (RuntimeError, ArithmeticError, ValueError) as error:
            require(not detail["resolved"] and not saved and not checks and key not in trajectories, "Failed transport prediction")
            require(detail["error"] == f"{type(error).__name__}: {error}", "Transport prediction failure receipt")
            continue
        compare(detail["parameters"], asdict(p), "Only mixing changed")
        require(detail["prediction_resolved"], "Resolved transport prediction flag")
        trajectory_keys.add(key)
        compare(trajectories[key], regenerated, "Transport state replay")
        for seed in (0, 1, 2):
            check_trajectory(regenerated[str(seed)], p, seed)
        expected_rows = [r for r in rows if not r["dataset"].startswith("S13")]
        require([r["row_id"] for r in saved] == [r["row_id"] for r in expected_rows], "Transport row coverage/order")
        for observed, original in zip(saved, expected_rows):
            check_source_row(observed, original)
            for name, value in metadata.items():
                require(observed[name] == str(value), f"Transport row metadata {name}")
            value = regenerated[str(int(original["seed_uM"]))][int(original["x"])]["yield_percent"] if original["dataset"] == "Figure_3" else cycles[original["seed_uM"], original["x"]]
            close(float(observed["predicted_percent"]), value, "Transport reporter replay")
            close(float(observed["error_pp"]), value-original["value_percent"], "Transport residual")
            stage = "historical_benchmark" if original["dataset"] == "Figure_3" or original["seed_uM"] == 2 else "transport_calibration"
            require(observed["stage"] == stage, "Transport stage")
        calibration_sse = sum(float(r["error_pp"])**2 for r in saved if r["row_id"] in train_ids)
        close(mixing["sse"], calibration_sse, "Transport calibration objective")
        expected_checks = []
        try:
            for seed in (0, 1, 2):
                fine = serial(p, seed, rtol=1e-10)
                coarse = regenerated[str(seed)]
                delta = max(abs(a["yield_percent"]-b["yield_percent"]) for a, b in zip(fine, coarse))
                balance = max(r["moiety_balance_max_error_uM"] for r in coarse)
                expected_checks.append({**metadata, "seed_uM": seed, "difference_pp": delta,
                    "moiety_error_uM": balance, "pass": delta < 1e-4 and balance < 1e-7})
        except (RuntimeError, ArithmeticError, ValueError) as error:
            require(not detail["resolved"] and not detail["refinement_resolved"], "Refinement failure status")
            require(detail["error"] == f"{type(error).__name__}: {error}", "Refinement failure receipt")
        else:
            require(detail["resolved"] and detail["refinement_resolved"], "Unreproduced refinement failure")
        compare(checks, expected_checks, "Serial refinement records")
        eligible = numerical[candidate]["pass"] and len(checks) == 3 and all(r["pass"] for r in checks)
        if detail["resolved"]:
            compare(detail["numerical_eligible"], eligible, "Transport numerical eligibility")
        held = [r for r in saved if r["row_id"] in held_ids]
        for name, subset in (("benchmark", held), ("Figure2_seed2", [r for r in held if r["dataset"] == "Figure_2"]),
                             ("Figure3", [r for r in held if r["dataset"] == "Figure_3"])):
            check_score(detail[name], subset, name, True, eligible)
    require(set(trajectories) == trajectory_keys, "Transport trajectory coverage")
    require({p.name for p in (directory/"mixing_fits").glob("*.json")} == expected_files, "Mixing fit coverage")
    return transport, predictions, refinements


def verify(directory, replicate=None):
    DIFFERENCES.clear()
    directory = directory.resolve()
    manifest, freeze = read_json(directory/"manifest.json"), read_json(directory/"freeze.json")
    require(bool(manifest), "Empty manifest")
    actual_files = {str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file() and p.name != "manifest.json"}
    require(set(manifest) == actual_files, "Manifest file coverage")
    required_inputs = {f"{ROOT.name}/{n}" for n in ("PROTOCOL.md", "WORKPLAN.md", "model.py", "run.py", "test_model.py", "test_validation.py", "plot.py", "requirements.txt")}
    required_inputs.update({SOURCE_NAME, "measured-coupling-2026-10-15/rna_sources/raw/salibi_data.xlsx",
                            "measured-coupling-2026-10-15/rna_sources/conditions.json"})
    require(required_inputs <= freeze["files"].keys(), "Missing frozen input")
    for name, expected in manifest.items():
        require(sha(directory/name) == expected, f"Manifest mismatch: {name}")
    for name, expected in freeze["files"].items():
        require(sha(directory/"frozen"/name) == expected, f"Snapshot mismatch: {name}")
        require(sha(WORKSPACE/name) == expected, f"Current input changed: {name}")
    prior = read_json(directory/"frozen"/ROOT.name/"diagnosis/verification.json")["input_hashes"]
    prior.update(read_json(directory/"frozen"/ROOT.name/"transport_diagnosis/input_hashes.json"))
    for name, expected in prior.items():
        require(sha(WORKSPACE/name) == expected, f"Previous laboratory input changed: {name}")
    compare(freeze["classification"], "retrospective previously inspected measured data", "Frozen evidence classification")
    compare(freeze["bounds"], BOUNDS)
    compare(freeze["starts"], STARTS)
    require(freeze["max_nfev"] == 160 and freeze["numpy"] == np.__version__ and
            freeze["scipy"] == scipy.__version__ and freeze["python"] == platform.python_version(), "Frozen execution configuration")
    compare(list(NAMES), list(EXPECTED_NAMES), "Chemical state identities")
    require(np.array_equal(MOIETIES, EXPECTED_MOIETIES), "Registered moiety matrix")
    for name, expected in {"python": "3.12.3", "numpy": "2.4.1", "scipy": "1.16.1",
                           "matplotlib": "3.10.8", "openpyxl": "3.1.3"}.items():
        require(freeze[name] == expected, f"Pinned {name}")
        require((platform.python_version() if name == "python" else version(name)) == expected, f"Live {name}")
    require(not any(Path(n).name in ("verify_results.py", "test_verify_results.py") for n in freeze["files"]),
            "Verifier must be separate from fit freeze")
    rows = source_rows(directory/"frozen"/SOURCE_NAME)
    require(len(rows) == 148, "Source row count")
    bulk = [r for r in rows if r["dataset"].startswith("S13")]
    by_id = {r["row_id"]: r for r in rows}
    doses = sorted({r["group_id"] for r in bulk})
    require(len(bulk) == 40 and len(doses) == 8, "Bulk dimensions")
    for dose in doses:
        require(sorted(r["x"] for r in bulk if r["group_id"] == dose) == [0, 15, 30, 45, 60], "Bulk grid")
    fits, expected_files = {}, set()
    for candidate in PARAMETERS:
        for count in (0, 1, 2):
            for omitted in itertools.combinations(doses, count):
                suffix = "-".join(str(doses.index(g)) for g in omitted) or "none"
                name = f"{candidate}__omit-{suffix}.json"
                detail = read_json(directory/"fits"/name)
                check_fit(detail, candidate, [r for r in bulk if r["group_id"] not in omitted and r["x"] > 0])
                fits[candidate, omitted] = detail
                expected_files.add(name)
        for kind in ("late", "joint"):
            name = f"{candidate}__{kind}.json"
            detail = read_json(directory/"fits"/name)
            training, _ = challenge_rows(bulk, kind)
            check_fit(detail, candidate, training)
            fits[candidate, kind] = detail
            expected_files.add(name)
    expected_index = {c: {"|".join(str(doses.index(g)) for g in omitted) or "none":
        {"resolved": d["resolved"], "training_row_ids": d["training_row_ids"]}
        for (candidate, omitted), d in fits.items() if candidate == c and isinstance(omitted, tuple)} for c in PARAMETERS}
    compare(read_json(directory/"fit_index.json"), expected_index, "Fit index")
    predictions = read_csv(directory/"predictions.csv")
    buckets = {}
    for row in predictions:
        require(row["row_id"] in by_id and row["candidate"] in PARAMETERS, "Unknown prediction identity")
        original = by_id[row["row_id"]]
        check_source_row(row, original)
        close(float(row["error_pp"]), float(row["predicted_percent"])-original["value_percent"], "Residual")
        key = tuple(row[k] for k in ("stage", "candidate", "outer_group", "inner_group"))
        buckets.setdefault(key, []).append(row)
    for (stage, candidate, outer, inner), saved in buckets.items():
        require(stage in ("fixed_dose", "nested_inner", "nested_outer", "full_fit", "late_time", "joint_challenge"), "Unknown stage")
        omitted = tuple(sorted(g for g in (outer, inner) if g))
        kind = {"late_time": "late", "joint_challenge": "joint"}.get(stage)
        detail = fits[candidate, kind or omitted]
        require(detail["resolved"], "Predictions from unresolved fit")
        if kind:
            _, expected = challenge_rows(bulk, kind)
        elif stage == "full_fit":
            expected = bulk
        else:
            expected = [r for r in bulk if r["group_id"] == (inner or outer)]
        require([r["row_id"] for r in saved] == [r["row_id"] for r in expected], "Prediction coverage/order")
        values = prediction(Parameters(**detail["parameters"]), expected)
        for row, value in zip(saved, values):
            close(float(row["predicted_percent"]), value, "Saved-parameter prediction replay")
    validation = read_json(directory/"validation.json")
    require([s["candidate"] for s in validation["fixed_families"]] == list(PARAMETERS), "Every fixed family retained")
    expected_splits, expected_buckets = [], set()

    def split(stage, candidate, outer, inner=""):
        training = [r for r in bulk if r["group_id"] not in (outer, inner) and r["x"] > 0]
        held = [r for r in bulk if r["group_id"] == (inner or outer)]
        expected_splits.append({"stage": stage, "candidate": candidate, "outer_group": outer,
            "inner_group": inner or None, "training_groups": sorted({r["group_id"] for r in training}),
            "training_row_ids": [r["row_id"] for r in training], "evaluation_group": inner or outer,
            "evaluation_row_ids": [r["row_id"] for r in held],
            "outer_row_ids": [r["row_id"] for r in bulk if r["group_id"] == outer]})

    def aggregate(saved, stage, candidate, outer=""):
        expected_held = [g for g in doses if g != outer] if stage == "nested_inner" else doses
        require([f["held_group"] for f in saved["folds"]] == expected_held, "Fold coverage/order")
        collected, resolved = [], 0
        for fold in saved["folds"]:
            held = fold["held_group"]
            o, i = (outer, held) if stage == "nested_inner" else (held, "")
            detail = fits[candidate, tuple(sorted(g for g in (o, i) if g))]
            check_evaluation(detail, fold, [r for r in bulk if r["group_id"] == held])
            split(stage, candidate, o, i)
            if fold["resolved"]:
                key = (stage, candidate, o, i)
                expected_buckets.add(key)
                check_score(fold["metrics"], buckets[key], "Fold score")
                collected.extend(buckets[key])
                resolved += 1
        require(saved["resolved_fold_count"] == resolved and saved["resolved"] == (resolved == len(expected_held)), "Aggregate failure propagation")
        if saved["resolved"]:
            check_score(saved, collected, "Pooled score")
        else:
            require(saved["rmse_pp"] is None and not saved["adequate"], "Partial folds cannot form adequate score")

    for item in validation["fixed_families"]:
        aggregate(item, "fixed_dose", item["candidate"])
    nested = validation["nested"]
    require([f["held_group"] for f in nested["folds"]] == doses, "Outer fold coverage")
    nested_rows, resolved = [], 0
    for fold in nested["folds"]:
        outer = fold["held_group"]
        require([s["candidate"] for s in fold["inner_scores"]] == list(PARAMETERS), "All inner candidates retained")
        for item in fold["inner_scores"]:
            aggregate(item, "nested_inner", item["candidate"], outer)
        chosen = choose(fold["inner_scores"])
        require(fold["selected"] == chosen, "Outer labels cannot choose family")
        if chosen is not None:
            check_evaluation(fits[chosen, (outer,)], fold, [r for r in bulk if r["group_id"] == outer])
        else:
            require(not fold["resolved"], "No eligible family cannot resolve outer fold")
        if fold["resolved"]:
            key = ("nested_outer", chosen, outer, "")
            expected_buckets.add(key)
            check_score(fold["metrics"], buckets[key], "Outer score")
            nested_rows.extend(buckets[key])
            split("nested_outer", chosen, outer)
            resolved += 1
    require(nested["resolved_fold_count"] == resolved and nested["resolved"] == (resolved == 8), "Nested completeness")
    if nested["resolved"]:
        check_score(nested, nested_rows, "Nested score")
    else:
        require(nested["rmse_pp"] is None and not nested["adequate"], "Unresolved nested procedure")
    actual_splits = read_json(directory/"splits.json")
    compare(sorted(actual_splits, key=lambda x: json.dumps(x, sort_keys=True)),
            sorted(expected_splits, key=lambda x: json.dumps(x, sort_keys=True)), "Recorded splits")
    selected = choose(validation["fixed_families"])
    require(validation["final_development_choice"] == selected, "Final simplicity selection")
    challenges = {}
    for stage, kind in (("late_time", "late"), ("joint_challenge", "joint")):
        challenges[stage] = read_json(directory/f"{stage}.json")
        require([r["candidate"] for r in challenges[stage]] == list(PARAMETERS), "All challenges retained")
        training, held = challenge_rows(bulk, kind)
        for item in challenges[stage]:
            candidate, detail = item["candidate"], fits[item["candidate"], kind]
            compare(item["training_row_ids"], [r["row_id"] for r in training])
            compare(item["evaluation_row_ids"], [r["row_id"] for r in held])
            check_evaluation(detail, item, held)
            if item["resolved"]:
                key = (stage, candidate, "", "")
                expected_buckets.add(key)
                check_score(item, buckets[key], f"{stage} score")
            else:
                require(item["rmse_pp"] is None and not item["adequate"], "Unresolved challenge score")
    full = read_json(directory/"full_fits.json")
    numerical = read_json(directory/"numerical_checks.json")
    states = read_csv(directory/"bulk_state_inventories.csv")
    require(all(r["candidate"] in PARAMETERS for r in states), "Unknown full inventory family")
    require(set(full) == set(PARAMETERS) == set(numerical), "All full fits and numerical checks retained")
    for item in validation["fixed_families"] + challenges["late_time"] + challenges["joint_challenge"]:
        require(item["numerical_eligible"] == numerical[item["candidate"]]["pass"], "Numerical eligibility")
    require(nested["numerical_eligible"] == all(f["selected"] is not None and numerical[f["selected"]]["pass"] for f in nested["folds"]), "Nested numerical eligibility")
    for candidate in PARAMETERS:
        compare(full[candidate], fits[candidate, ()], "Full fit cache")
        saved_states = [r for r in states if r["candidate"] == candidate]
        if not full[candidate]["resolved"]:
            require(not saved_states and not numerical[candidate]["pass"], "Unresolved fullfit states")
            continue
        p = Parameters(**full[candidate]["parameters"])
        try:
            checks, replayed_states = bulk_inventory(p, bulk)
        except (RuntimeError, ArithmeticError, ValueError) as error:
            require(not saved_states and not numerical[candidate]["pass"], "Failed numerical inventory")
            require(numerical[candidate]["error"] == str(error), "Numerical failure receipt")
        else:
            evaluation = {"resolved": numerical[candidate]["full_fit_prediction_resolved"]}
            if not evaluation["resolved"]:
                evaluation["error"] = "Full-fit prediction failed"
            check_evaluation(full[candidate], evaluation, bulk)
            checks["full_fit_prediction_resolved"] = evaluation["resolved"]
            checks["pass"] &= evaluation["resolved"]
            compare(numerical[candidate], checks, "Numerical refinement")
            check_inventories(saved_states, replayed_states)
        if ("full_fit", candidate, "", "") in buckets:
            expected_buckets.add(("full_fit", candidate, "", ""))
        else:
            try:
                prediction(p, bulk)
            except (RuntimeError, ArithmeticError, ValueError):
                pass
            else:
                raise AssertionError("Missing resolved full-fit predictions")
    require(set(buckets) == expected_buckets, "Missing or extra prediction batches")
    profiles = read_json(directory/"profiles.json")
    profile_keys = []
    if selected is not None and full[selected]["resolved"]:
        profile_keys = [(n, float(v)) for n in ("kb", "krel", "kbind") if n in PARAMETERS[selected] for v in np.linspace(*BOUNDS[n], 5)]
    compare([[p["parameter"], p["fixed_log10"]] for p in profiles], [[n, v] for n, v in profile_keys], "Profile grid")
    profile_states = read_csv(directory/"profile_inventories.csv")
    expected_profile_states = []
    for entry in profiles:
        name, value = entry["parameter"], entry["fixed_log10"]
        filename = f"profile__{name}__{value:g}.json"
        compare(entry["fit"], read_json(directory/"fits"/filename), "Profile cache")
        check_fit(entry["fit"], selected, [r for r in bulk if r["x"] > 0], {name: float(10**value)})
        expected_files.add(filename)
        if entry["fit"]["resolved"]:
            try:
                _, inventory = bulk_inventory(Parameters(**entry["fit"]["parameters"]), bulk)
            except (RuntimeError, ArithmeticError, ValueError) as error:
                require(entry.get("inventory_error") == str(error), "Profile inventory failure")
            else:
                require("inventory_error" not in entry, "Unreproduced profile inventory failure")
                expected_profile_states.extend({"parameter": name, "fixed_log10": value, **r} for r in inventory)
    check_inventories(profile_states, expected_profile_states)
    require({p.name for p in (directory/"fits").glob("*.json")} == expected_files, "Fit coverage")
    transport, transport_rows, refinements = check_transport(directory, rows, full, selected, numerical)
    summary = read_json(directory/"summary.json")
    compare(summary["classification"], "retrospective; all measured data previously inspected", "Evidence classification")
    compare(summary["scientific_limit"], "PAGE reporter data do not identify active F1 or a unique mechanism; transport closures remain hypotheses.", "Scientific limitation")
    require(summary["selected_chemistry"] == selected and summary["selected_full_fit_resolved"] == (selected is not None and full[selected]["resolved"]), "Summary selection")
    compare(summary["fixed_family_scores"], [{k: v for k, v in s.items() if k != "folds"} for s in validation["fixed_families"]])
    compare(summary["nested_selection"], {k: v for k, v in nested.items() if k != "folds"})
    for stage, entries in challenges.items():
        compare(summary[stage], entries)
    compare(summary["transport"], transport)
    require(summary["all_full_fit_numerical_checks_pass"] == all(n["pass"] for n in numerical.values()), "Summary numerical checks")
    require(summary["all_transport_refinement_pass"] == (bool(refinements) and all(d["resolved"] for d in transport.values()) and all(r["pass"] for r in refinements)), "Summary transport checks")
    if replicate:
        replicate = replicate.resolve()
        for name, expected in read_json(replicate/"manifest.json").items():
            require(sha(replicate/name) == expected, f"Refit manifest mismatch: {name}")
        for name, expected in read_json(replicate/"freeze.json")["files"].items():
            require(sha(replicate/"frozen"/name) == expected, f"Refit snapshot mismatch: {name}")
    compared_files = compare_refit(directory, replicate) if replicate else None
    return {"status": "PASS", "classification": "software and record verification, not mechanism adequacy",
        "fit_records_checked": len(expected_files), "starts_retained": 6*len(expected_files),
        "prediction_rows_replayed": len(predictions)+len(transport_rows), "split_records_checked": len(actual_splits),
        "profile_points_checked": len(profiles), "profile_state_rows_replayed": len(profile_states),
        "transport_scenarios_checked": len(transport), "full_state_rows_replayed": len(states),
        "manifest_files_checked": len(manifest), "frozen_inputs_checked": len(freeze["files"]),
        "previous_laboratory_hashes_unchanged": len(prior),
        "verifier_sha256": sha(Path(__file__)), "verifier_tests_sha256": sha(ROOT/"test_verify_results.py"),
        "independent_refit_files_compared": compared_files, "numeric_comparisons": DIFFERENCES,
        "absolute_tolerance": 1e-8, "relative_tolerance": 1e-8}


def compare_refit(first, second):
    """Compare every scientific JSON/CSV, including individual failed starts; exclude clocks and plot bytes."""
    compare(read_json(first/"freeze.json"), read_json(second/"freeze.json"), "Refit freeze", ignore_clocks=True)
    files = lambda directory: {str(p.relative_to(directory)) for p in directory.rglob("*")
        if p.is_file() and p.suffix in (".json", ".csv") and "frozen" not in p.relative_to(directory).parts
        and p.name not in ("manifest.json", "freeze.json")}
    names = files(first)
    require(names == files(second), "Refit scientific file coverage")
    for name in sorted(names):
        if name.endswith(".json"):
            compare(read_json(first/name), read_json(second/name), f"Refit {name}", ignore_clocks=True)
        else:
            left, right = read_csv(first/name), read_csv(second/name)
            require(len(left) == len(right), f"Refit CSV rows {name}")
            for a, b in zip(left, right):
                require(a.keys() == b.keys(), f"Refit CSV columns {name}")
                for key in a:
                    if key in {"row_id", "group_id", "stage", "candidate", "outer_group", "inner_group",
                               "scenario", "dataset", "mixing_mode", "loss_closure", "complex_reset"}:
                        require(a[key] == b[key], f"Refit CSV identity {name}.{key}")
                        continue
                    try:
                        av, bv = float(a[key]), float(b[key])
                    except ValueError:
                        require(a[key] == b[key], f"Refit CSV identity {name}.{key}")
                    else:
                        close(av, bv, f"Refit CSV numeric {name}.{key}")
    return len(names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--replicate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.result, args.replicate), indent=2, allow_nan=False))
