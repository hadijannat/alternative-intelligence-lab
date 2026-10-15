"""Independent accounting, split/score checks and saved-parameter replay; no fitting."""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform

import numpy as np
import scipy

from model import MOIETIES, NAMES, Parameters, bulk_curves, initial_complexes, react, serial, single_cycle

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE_NAME = "measured-coupling-2026-10-15/rna_sources/observations.csv"
PARAMETERS = {
    "revised": ("kf", "kh", "kb"),
    "independent": ("kf", "kh", "kb", "ka", "krh"),
    "inactivation": ("kf", "kh", "kb", "kd"),
    "independent_inactivation": ("kf", "kh", "kb", "ka", "krh", "kd"),
    "trapping_free": ("kf", "kh", "kb", "kon", "koff"),
    "trapping_equilibrium": ("kf", "kh", "kb", "kon", "koff"),
}
BOUNDS = {"kf": [-4, 1], "kh": [-8, 0], "kb": [-2, 2], "ka": [-4, 1],
          "krh": [-8, 0], "kd": [-6, 0], "kon": [-6, 1], "koff": [-6, 1]}
START_NAMES = ("kf", "kh", "kb", "ka", "krh", "kd", "kon", "koff")
STARTS = [dict(zip(START_NAMES, row)) for row in (
    (-1, -5, 0, -1, -4, -2, -2, -2), (-.5, -3, 1, -.5, -2, -1, 0, -1),
    (-1.5, -6, -1, -1.5, -6, -3, -4, 0), (.2, -4, 1.8, -2, -3, -4, -1, -4),
    (-2, -2, -1.8, .5, -1, -.3, .7, .7), (.8, -7, .5, -.2, -7, -5, -5, -5))]
CLOCK_KEYS = {"elapsed_seconds", "utc_before_fit"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, label="value"):
    require(math.isfinite(float(actual)) and math.isfinite(float(expected)), f"{label}: nonfinite")
    require(abs(actual-expected) <= 1e-8 + 1e-8*abs(expected), f"{label}: {actual!r} != {expected!r}")


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
    successes = []
    for i, start in enumerate(detail["starts"]):
        require(start["start_id"] == i+1, "Start order")
        compare(start["log10_start"], [float(STARTS[i][n]) for n in free])
        require(start["nfev"] is None or 0 <= start["nfev"] <= 160, "Evaluation budget exceeded")
        if start["success"]:
            require(start["status"] in (1, 2, 3, 4) and start["sse"] >= 0, "Invalid successful optimizer termination")
            require(len(start["log10_parameters"]) == len(free), "Parameter dimension")
            require(all(BOUNDS[n][0]-1e-12 <= v <= BOUNDS[n][1]+1e-12 for n, v in zip(free, start["log10_parameters"])), "Parameter outside registered bounds")
            successes.append(start)
        require(isinstance(start["message"], str), "Missing optimizer receipt")
    require(detail["resolved"] == bool(successes), "Failed starts cannot resolve fit")
    if successes:
        best = min(successes, key=lambda s: s["sse"])
        close(detail["sse"], best["sse"], "Best successful SSE")
        values = dict(zip(free, 10**np.array(best["log10_parameters"])))
        values.update(fixed)
        p = Parameters(**values, equilibrated=candidate == "trapping_equilibrium")
        from dataclasses import asdict
        compare(detail["parameters"], asdict(p), "Selected start parameters")
        errors = np.array(prediction(p, training)) - [r["value_percent"] for r in training]
        close(detail["sse"], float(errors@errors), "Replayed training SSE")
        close(detail["rmse_pp"], float(np.sqrt(np.mean(errors**2))), "Replayed training RMSE")
        count = sum(abs(s["sse"]-best["sse"]) <= max(1e-4, 1e-4*best["sse"]) for s in successes)
        require(detail["successful_starts"] == len(successes) and detail["agreeing_successful_starts"] == count and detail["two_starts_agree"] == (count >= 2), "Multistart accounting")
        singular = detail["jacobian_singular_values"]
        require(len(singular) == len(free) and all(math.isfinite(x) and x >= 0 for x in singular), "Jacobian diagnostics")
    return bool(successes)


def verify(directory, replicate=None):
    directory = directory.resolve()
    manifest, freeze = read_json(directory/"manifest.json"), read_json(directory/"freeze.json")
    for name, expected in manifest.items():
        require(sha(directory/name) == expected, f"Manifest mismatch: {name}")
    for name, expected in freeze["files"].items():
        require(sha(directory/"frozen"/name) == expected, f"Snapshot mismatch: {name}")
        require(sha(WORKSPACE/name) == expected, f"Current input changed: {name}")
    prior = read_json(directory/"frozen"/ROOT.name/"diagnosis/.omo/evidence/verification.json")["source_hashes"]
    for name, expected in prior.items():
        require(sha(WORKSPACE/name) == expected, f"Previous laboratory input changed: {name}")
    compare(freeze["bounds"], BOUNDS)
    compare(freeze["starts"], STARTS)
    require(freeze["max_nfev"] == 160 and freeze["numpy"] == np.__version__ and
            freeze["scipy"] == scipy.__version__ and freeze["python"] == platform.python_version(), "Frozen execution configuration")
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
        name = f"{candidate}__late.json"
        detail = read_json(directory/"fits"/name)
        check_fit(detail, candidate, [r for r in bulk if r["x"] in (15, 30)])
        fits[candidate, "late"] = detail
        expected_files.add(name)
    expected_index = {c: {"|".join(str(doses.index(g)) for g in omitted) or "none":
        {"resolved": d["resolved"], "training_row_ids": d["training_row_ids"]}
        for (candidate, omitted), d in fits.items() if candidate == c and omitted != "late"} for c in PARAMETERS}
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
        require(stage in ("fixed_dose", "nested_inner", "nested_outer", "full_fit", "late_time"), "Unknown stage")
        omitted = tuple(sorted(g for g in (outer, inner) if g))
        detail = fits[candidate, "late" if stage == "late_time" else omitted]
        require(detail["resolved"], "Predictions from unresolved fit")
        if stage == "late_time":
            expected = [r for r in bulk if r["x"] in (45, 60)]
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
    late = read_json(directory/"late_time.json")
    require([r["candidate"] for r in late] == list(PARAMETERS), "All late challenges retained")
    for item in late:
        candidate, detail = item["candidate"], fits[item["candidate"], "late"]
        compare(item["training_row_ids"], [r["row_id"] for r in bulk if r["x"] in (15, 30)])
        compare(item["evaluation_row_ids"], [r["row_id"] for r in bulk if r["x"] in (45, 60)])
        check_evaluation(detail, item, [r for r in bulk if r["x"] in (45, 60)])
        if item["resolved"]:
            key = ("late_time", candidate, "", "")
            expected_buckets.add(key)
            check_score(item, buckets[key], "Late score")
        else:
            require(item["rmse_pp"] is None and not item["adequate"], "Unresolved late score")
    full = read_json(directory/"full_fits.json")
    numerical = read_json(directory/"numerical_checks.json")
    states = read_csv(directory/"bulk_state_inventories.csv")
    require(set(full) == set(PARAMETERS) == set(numerical), "All full fits and numerical checks retained")
    for item in validation["fixed_families"] + late:
        require(item["numerical_eligible"] == numerical[item["candidate"]]["pass"], "Numerical eligibility")
    require(nested["numerical_eligible"] == all(f["selected"] is not None and numerical[f["selected"]]["pass"] for f in nested["folds"]), "Nested numerical eligibility")
    for candidate in PARAMETERS:
        compare(full[candidate], fits[candidate, ()], "Full fit cache")
        saved_states = [r for r in states if r["candidate"] == candidate]
        if not full[candidate]["resolved"]:
            require(not saved_states and not numerical[candidate]["pass"], "Unresolved fullfit states")
            continue
        expected_buckets.add(("full_fit", candidate, "", ""))
        p = Parameters(**full[candidate]["parameters"])
        reps = [next(r for r in bulk if r["group_id"] == g) for g in doses]
        x = np.zeros((8, 8))
        x[:, 0], x[:, 1], x[:, 2], x[:, 3] = [r["hyper_a_uM"] for r in reps], 5, 7.5, [r["seed_uM"] for r in reps]
        x = initial_complexes(x, p)
        coarse = react(x, 60, p, times=[0, 15, 30, 45, 60])
        fine = react(x, 60, p, times=[0, 15, 30, 45, 60], rtol=1e-10)
        separate = np.concatenate([react(x[i:i+1], 60, p, times=[0, 15, 30, 45, 60]) for i in range(8)], axis=1)
        observer = lambda y: 100*y[:, :, 4]/(y[:, :, 1]+y[:, :, 4]+y[:, :, 7])
        delta = float(np.max(np.abs(observer(coarse)-observer(fine))))
        batch = float(np.max(np.abs(observer(coarse)-observer(separate))))
        balance = float(np.max(np.abs(coarse@MOIETIES.T-(x@MOIETIES.T)[None])))
        compare(numerical[candidate], {"maximum_tolerance_difference_pp": delta,
            "maximum_batch_difference_pp": batch, "maximum_moiety_error_uM": balance,
            "pass": delta < 1e-4 and batch < 1e-4 and balance < 1e-7}, "Numerical refinement")
        require(len(saved_states) == 40, "Full state inventory coverage")
        require(len({(s["group_id"], s["minutes"]) for s in saved_states}) == 40, "Duplicate state rows")
        for state in saved_states:
            gi, ti = doses.index(state["group_id"]), [0, 15, 30, 45, 60].index(float(state["minutes"]))
            for k, name in enumerate(NAMES):
                value = float(state[name+"_uM"])
                require(value >= 0, "Negative state inventory")
                close(value, float(coarse[ti, gi, k]), "State replay")
    require(set(buckets) == expected_buckets, "Missing or extra prediction batches")
    profiles = read_json(directory/"profiles.json")
    profile_keys = []
    if selected is not None and full[selected]["resolved"]:
        profile_keys = [(n, float(v)) for n in PARAMETERS[selected] if n not in ("kf", "kh") for v in np.linspace(*BOUNDS[n], 5)]
    compare([[p["parameter"], p["fixed_log10"]] for p in profiles], [[n, v] for n, v in profile_keys], "Profile grid")
    for entry in profiles:
        name, value = entry["parameter"], entry["fixed_log10"]
        filename = f"profile__{name}__{value:g}.json"
        compare(entry["fit"], read_json(directory/"fits"/filename), "Profile cache")
        check_fit(entry["fit"], selected, [r for r in bulk if r["x"] > 0], {name: float(10**value)})
        expected_files.add(filename)
    require({p.name for p in (directory/"fits").glob("*.json")} == expected_files, "Fit coverage")
    transport = read_json(directory/"transport.json")
    transport_rows = read_csv(directory/"transport_predictions.csv")
    trajectories = read_json(directory/"transport_trajectories.json")
    refinements = read_json(directory/"transport_refinement.json")
    require(set(transport) == {"fractional", "contact"}, "Both transport closures retained")
    require(all(r["transport"] in transport for r in transport_rows), "Unknown transport prediction")
    training = [r for r in rows if r["dataset"] == "Figure_2" and r["seed_uM"] in (0, 1) and r["x"] > 0]
    benchmark_ids = {r["row_id"] for r in rows if (r["dataset"] == "Figure_3" or (r["dataset"] == "Figure_2" and r["seed_uM"] == 2)) and r["x"] > 0}
    require(len(training) == 18 and len(benchmark_ids) == 72, "Transport source partitions")
    require(not set(r["row_id"] for r in training)&benchmark_ids, "Transport leakage")
    expected_refinement = []
    for mode, detail in transport.items():
        saved = [r for r in transport_rows if r["transport"] == mode]
        if not detail["resolved"]:
            require(not saved, "Predictions from unresolved transport")
            continue
        require(selected is not None and full[selected]["resolved"], "Transport without fixed chemistry")
        for key, value in full[selected]["parameters"].items():
            if key not in ("mixing", "transport"):
                compare(detail["parameters"][key], value, "Transport changed chemistry")
        p = Parameters(**detail["parameters"])
        require(p.transport == mode and p.retention_f == p.retention_fragments == .55, "Transport settings")
        compare(detail["mixing_fit"]["training_row_ids"], [r["row_id"] for r in training])
        require(detail["mixing_fit"]["n"] == 18, "Mixing training count")
        regenerated = {str(seed): serial(p, seed) for seed in (0, 1, 2)}
        compare(trajectories[mode], regenerated, "Transport state replay")
        cycles = {(s, n): single_cycle(p, s, n) for s in (0, 1, 2) for n in (0, 1, 2, 3)}
        expected = [r for r in rows if not r["dataset"].startswith("S13")]
        require([r["row_id"] for r in saved] == [r["row_id"] for r in expected], "Transport prediction coverage")
        for observed, original in zip(saved, expected):
            check_source_row(observed, original)
            value = regenerated[str(int(original["seed_uM"]))][int(original["x"])]["yield_percent"] if original["dataset"] == "Figure_3" else cycles[original["seed_uM"], original["x"]]
            close(float(observed["predicted_percent"]), value, "Transport reporter replay")
            close(float(observed["error_pp"]), value-original["value_percent"], "Transport residual")
            stage = "historical_benchmark" if original["dataset"] == "Figure_3" or original["seed_uM"] == 2 else "transport_calibration"
            require(observed["stage"] == stage, "Transport stage")
        calibration = [r for r in saved if r["row_id"] in {x["row_id"] for x in training}]
        sse = sum(float(r["error_pp"])**2 for r in calibration)
        close(detail["mixing_fit"]["sse"], sse, "Mixing objective")
        close(detail["mixing_fit"]["rmse_pp"], math.sqrt(sse/18), "Mixing RMSE")
        held = [r for r in saved if r["row_id"] in benchmark_ids]
        eligible = numerical[selected]["pass"] and all(r["pass"] for r in refinements if r["transport"] == mode)
        require(detail["numerical_eligible"] == eligible, "Transport numerical eligibility")
        check_score(detail["benchmark"], held, "Transport benchmark", True, eligible)
        check_score(detail["Figure2_seed2"], [r for r in held if r["dataset"] == "Figure_2"], "Figure2 benchmark", True, eligible)
        check_score(detail["Figure3"], [r for r in held if r["dataset"] == "Figure_3"], "Figure3 benchmark", True, eligible)
        for seed in (0, 1, 2):
            fine = serial(p, seed, rtol=1e-10)
            coarse = regenerated[str(seed)]
            delta = max(abs(a["yield_percent"]-b["yield_percent"]) for a, b in zip(fine, coarse))
            balance = max(r["moiety_balance_max_error_uM"] for r in coarse)
            expected_refinement.append({"transport": mode, "seed_uM": seed, "difference_pp": delta,
                "moiety_error_uM": balance, "pass": delta < 1e-4 and balance < 1e-7})
    compare(sorted(refinements, key=lambda r: (r["transport"], r["seed_uM"])),
            sorted(expected_refinement, key=lambda r: (r["transport"], r["seed_uM"])), "Transport refinement")
    summary = read_json(directory/"summary.json")
    require(summary["selected_chemistry"] == selected and summary["selected_full_fit_resolved"] == (selected is not None and full[selected]["resolved"]), "Summary selection")
    compare(summary["fixed_family_scores"], [{k: v for k, v in s.items() if k != "folds"} for s in validation["fixed_families"]])
    compare(summary["nested_selection"], {k: v for k, v in nested.items() if k != "folds"})
    compare(summary["late_time"], late)
    compare(summary["transport"], transport)
    require(summary["all_full_fit_numerical_checks_pass"] == all(n["pass"] for n in numerical.values()), "Summary numerical checks")
    require(summary["all_transport_refinement_pass"] == (bool(refinements) and all(r["pass"] for r in refinements)), "Summary transport checks")
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
        "profile_points_checked": len(profiles), "full_state_rows_replayed": len(states),
        "manifest_files_checked": len(manifest), "frozen_inputs_checked": len(freeze["files"]),
        "previous_laboratory_hashes_unchanged": len(prior),
        "verifier_sha256": sha(Path(__file__)), "verifier_tests_sha256": sha(ROOT/"test_verify_results.py"),
        "independent_refit_files_compared": compared_files, "absolute_tolerance": 1e-8, "relative_tolerance": 1e-8}


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
