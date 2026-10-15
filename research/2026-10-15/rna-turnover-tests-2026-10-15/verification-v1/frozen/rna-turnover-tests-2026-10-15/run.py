"""Frozen retrospective mechanism comparison; every failed fit remains in the record."""
import argparse
import csv
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import platform
import shutil
import time

import numpy as np
import scipy
from scipy.optimize import least_squares, minimize_scalar

from model import (MOIETIES, NAMES, Parameters, bulk_curves, initial_complexes,
                   competent_inventory, reporter_product, react, serial, single_cycle)

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE = WORKSPACE / "measured-coupling-2026-10-15/rna_sources"
PARAMETERS = {
    "baseline": ("kf", "kh", "kb", "ka", "krh", "kd"),
    "release": ("kf", "kh", "kb", "ka", "krh", "kd", "krel"),
    "reversible_free": ("kf", "kh", "kb", "ka", "krh", "kd", "krel", "kbind"),
    "reversible_equilibrium": ("kf", "kh", "kb", "ka", "krh", "kd", "krel", "kbind"),
}
BOUNDS = {"kf": (-4, 1), "kh": (-8, 0), "kb": (-2, 2), "ka": (-4, 1),
          "krh": (-8, 0), "kd": (-6, 0), "krel": (-4, 2), "kbind": (-6, 2)}
START_NAMES = ("kf", "kh", "kb", "ka", "krh", "kd", "krel", "kbind")
STARTS = [dict(zip(START_NAMES, row)) for row in (
    (-1, -5, 0, -1, -4, -2, -1, -2),
    (-.5, -3, 1, -.5, -2, -1, 0, 0),
    (-1.5, -6, -1, -1.5, -6, -3, -3, -4),
    (.2, -4, 1.8, -2, -3, -4, 1, 1),
    (-2, -2, -1.8, .5, -1, -.3, .5, -5),
    (.8, -7, .5, -.2, -7, -5, -2, .5),
)]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def write_csv(path, rows):
    with path.open("w", newline="") as stream:
        if not rows:
            stream.write("status\nunresolved_no_predictions\n")
            return
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load():
    with (SOURCE / "observations.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    for i, row in enumerate(rows):
        row["row_id"] = f"observation_{i:03d}"
        for key in ("seed_uM", "hyper_a_uM", "x", "value_percent"):
            row[key] = float(row[key])
        row["group_id"] = f"{row['dataset']}|{row['seed_uM']:g}|{row['hyper_a_uM']:g}"
    if len(rows) != 148:
        raise ValueError("Expected the frozen 148 source observations")
    bulk = [r for r in rows if r["dataset"].startswith("S13")]
    if len(bulk) != 40 or len(groups(bulk)) != 8:
        raise ValueError("Expected eight complete S13 dose trajectories")
    for group in groups(bulk):
        if sorted(r["x"] for r in bulk if r["group_id"] == group) != [0, 15, 30, 45, 60]:
            raise ValueError("Invalid S13 time grid")
    return rows


def groups(rows):
    return sorted({r["group_id"] for r in rows})


def predict(p, rows):
    ordered_groups = groups(rows)
    times = sorted({r["x"] for r in rows})
    representatives = [next(r for r in rows if r["group_id"] == g) for g in ordered_groups]
    values = bulk_curves(p, [r["seed_uM"] for r in representatives],
                         [r["hyper_a_uM"] for r in representatives], times)
    output = []
    for r in rows:
        value = float(values[ordered_groups.index(r["group_id"]), times.index(r["x"])])
        if not np.isfinite(value):
            raise ArithmeticError("Nonfinite model prediction")
        output.append({**r, "predicted_percent": value, "error_pp": value-r["value_percent"]})
    return output


def metrics(rows):
    positive = [r for r in rows if r["x"] > 0]
    if not positive:
        return {"resolved": False, "n_positive": 0, "rmse_pp": None,
                "maximum_absolute_error_pp": None, "historical_all_rows_rmse_pp": None,
                "adequate": False}
    errors = np.array([r["error_pp"] for r in positive])
    if np.any(~np.isfinite(errors)):
        raise ValueError("Nonfinite errors must remain unresolved")
    rmse, maximum = float(np.sqrt(np.mean(errors**2))), float(np.max(np.abs(errors)))
    return {"resolved": True, "n_positive": len(positive), "rmse_pp": rmse,
            "maximum_absolute_error_pp": maximum, "bias_pp": float(errors.mean()),
            "historical_all_rows_rmse_pp": float(np.sqrt(np.mean([r["error_pp"]**2 for r in rows]))),
            "adequate": rmse <= 2 and maximum <= 4}


def select_family(scores):
    valid = [s for s in scores if s["resolved"] and s.get("rmse_pp") is not None
             and np.isfinite(s["rmse_pp"])]
    if not valid:
        return None
    minimum = min(s["rmse_pp"] for s in valid)
    eligible = [s for s in valid if s["rmse_pp"] <= minimum + .25]
    return min(eligible, key=lambda s: (len(PARAMETERS[s["candidate"]]), s["candidate"]))["candidate"]


def split_record(rows, outer, inner=None):
    omitted = {outer} | ({inner} if inner is not None else set())
    train = [r for r in rows if r["group_id"] not in omitted and r["x"] > 0]
    held = [r for r in rows if r["group_id"] == (inner if inner is not None else outer)]
    record = {"outer_group": outer, "inner_group": inner,
              "training_groups": groups(train), "training_row_ids": [r["row_id"] for r in train],
              "evaluation_group": inner if inner is not None else outer,
              "evaluation_row_ids": [r["row_id"] for r in held],
              "outer_row_ids": [r["row_id"] for r in rows if r["group_id"] == outer]}
    assert_split(record)
    return record


def assert_split(record):
    train = set(record["training_row_ids"])
    assert not train.intersection(record["evaluation_row_ids"])
    assert not train.intersection(record["outer_row_ids"])
    assert record["outer_group"] not in record["training_groups"]
    if record["inner_group"] is not None:
        assert record["inner_group"] != record["outer_group"]
        assert record["inner_group"] not in record["training_groups"]
        assert not set(record["evaluation_row_ids"]).intersection(record["outer_row_ids"])


def decode(candidate, log_values, fixed=None):
    fixed = fixed or {}
    free = [name for name in PARAMETERS[candidate] if name not in fixed]
    values = dict(zip(free, 10.**np.asarray(log_values)))
    values.update(fixed)
    return Parameters(**values, turnover=candidate != "baseline",
                      equilibrated=candidate == "reversible_equilibrium")


def fit(candidate, rows, path, fixed=None):
    fixed = fixed or {}
    train = [r for r in rows if r["x"] > 0]
    if not train:
        raise ValueError("No informative observations")
    free = [name for name in PARAMETERS[candidate] if name not in fixed]
    low, high = np.array([BOUNDS[name] for name in free]).T
    details = {"candidate": candidate, "resolved": False, "complete": False,
               "training_groups": groups(train), "training_row_ids": [r["row_id"] for r in train],
               "fixed_parameters": fixed, "free_parameters": free, "starts": [],
               "max_nfev": 160, "n_observations": len(train)}
    save(path, details)

    residual_calls = 0

    def residual(log_values):
        nonlocal residual_calls
        residual_calls += 1
        return np.array([r["error_pp"] for r in predict(decode(candidate, log_values, fixed), train)])

    successful = []
    for start_id, table in enumerate(STARTS):
        start = np.clip([table[name] for name in free], low, high)
        begun = time.monotonic()
        calls_before = residual_calls
        entry = {"start_id": start_id+1, "log10_start": start.tolist()}
        try:
            result = least_squares(residual, start, bounds=(low, high), max_nfev=160,
                                   jac="3-point", diff_step=1e-3,
                                   xtol=1e-8, ftol=1e-8, gtol=1e-8)
            finite = bool(np.all(np.isfinite(result.fun)) and np.all(np.isfinite(result.x)))
            entry.update(success=bool(result.success and finite), status=int(result.status),
                         nfev=int(result.nfev), njev=int(result.njev or 0),
                         sse=float(result.fun@result.fun) if finite else None,
                         message=result.message, active_bounds=result.active_mask.tolist(),
                         log10_parameters=result.x.tolist() if finite else None)
            if entry["success"]:
                successful.append(result)
        except (RuntimeError, ArithmeticError, ValueError, np.linalg.LinAlgError) as error:
            entry.update(success=False, status=None, nfev=None, njev=None, sse=None,
                         message=f"{type(error).__name__}: {error}", active_bounds=None)
        entry["elapsed_seconds"] = time.monotonic()-begun
        entry["residual_evaluations"] = residual_calls-calls_before
        details["starts"].append(entry)
        save(path, details)
    details["complete"] = True
    details["residual_evaluations"] = residual_calls
    if successful:
        best = min(successful, key=lambda result: float(result.fun@result.fun))
        p = decode(candidate, best.x, fixed)
        sse = float(best.fun@best.fun)
        agreements = sum(abs(float(result.fun@result.fun)-sse) <= max(1e-4, 1e-4*sse)
                         for result in successful)
        details.update(resolved=True, parameters=asdict(p), sse=sse,
                       rmse_pp=float(np.sqrt(sse/len(train))), active_bounds=best.active_mask.tolist(),
                       jacobian_singular_values=np.linalg.svd(best.jac, compute_uv=False).tolist(),
                       successful_starts=len(successful), agreeing_successful_starts=agreements,
                       two_starts_agree=agreements >= 2)
    save(path, details)
    return details


def get_parameters(detail):
    return Parameters(**detail["parameters"]) if detail["resolved"] else None


def evaluate(detail, held):
    if not detail["resolved"]:
        return {"resolved": False, "error": "Training fit unresolved"}, []
    try:
        pred = predict(get_parameters(detail), held)
        return {"resolved": True, "metrics": metrics(pred)}, pred
    except (RuntimeError, ArithmeticError, ValueError) as error:
        return {"resolved": False, "error": f"Prediction failed: {type(error).__name__}: {error}"}, []


def aggregate(candidate, folds, predictions):
    if not all(f["resolved"] for f in folds):
        return {"candidate": candidate, "resolved": False, "rmse_pp": None, "adequate": False,
                "folds": folds, "resolved_fold_count": sum(f["resolved"] for f in folds)}
    return {"candidate": candidate, **metrics(predictions), "folds": folds,
            "resolved_fold_count": len(folds)}


def validation(rows, output):
    dose_groups = groups(rows)
    cache, all_predictions, fixed_scores, records = {}, [], [], []
    jobs = []
    for candidate in PARAMETERS:
        cache[candidate] = {}
        for count in (0, 1, 2):
            for omitted in itertools.combinations(dose_groups, count):
                suffix = "-".join(str(dose_groups.index(g)) for g in omitted) or "none"
                filename = f"{candidate}__omit-{suffix}.json"
                train = [r for r in rows if r["group_id"] not in omitted]
                jobs.append((candidate, omitted, train, output/"fits"/filename))
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = pool.map(fit, [j[0] for j in jobs], [j[2] for j in jobs], [j[3] for j in jobs])
        for (candidate, omitted, _, _), detail in zip(jobs, results):
            cache[candidate][omitted] = detail
            print("FIT", candidate, "omitted", omitted, "resolved", detail["resolved"], flush=True)
    save(output/"fit_index.json", {c: {"|".join(str(dose_groups.index(g)) for g in omitted) or "none":
                                     {"resolved": d["resolved"], "training_row_ids": d["training_row_ids"]}
                                     for omitted, d in entries.items()} for c, entries in cache.items()})
    for candidate in PARAMETERS:
        folds, family_predictions = [], []
        for outer in dose_groups:
            detail = cache[candidate][(outer,)]
            record = split_record(rows, outer)
            assert record["training_row_ids"] == detail["training_row_ids"]
            records.append({"stage": "fixed_dose", "candidate": candidate, **record})
            evaluation, pred = evaluate(detail, [r for r in rows if r["group_id"] == outer])
            fold = {"held_group": outer, **evaluation}
            if fold["resolved"]:
                family_predictions.extend(pred)
                fold["metrics"] = metrics(pred)
                all_predictions.extend({"stage": "fixed_dose", "candidate": candidate,
                                        "outer_group": outer, "inner_group": "", **r} for r in pred)
            folds.append(fold)
        fixed_scores.append(aggregate(candidate, folds, family_predictions))
    nested_folds, nested_predictions = [], []
    for outer in dose_groups:
        inner_scores = []
        for candidate in PARAMETERS:
            folds, family_predictions = [], []
            for inner in dose_groups:
                if inner == outer:
                    continue
                detail = cache[candidate][tuple(sorted((outer, inner)))]
                record = split_record(rows, outer, inner)
                assert record["training_row_ids"] == detail["training_row_ids"]
                records.append({"stage": "nested_inner", "candidate": candidate, **record})
                evaluation, pred = evaluate(detail, [r for r in rows if r["group_id"] == inner])
                fold = {"held_group": inner, **evaluation}
                if fold["resolved"]:
                    family_predictions.extend(pred)
                    fold["metrics"] = metrics(pred)
                    all_predictions.extend({"stage": "nested_inner", "candidate": candidate,
                                            "outer_group": outer, "inner_group": inner, **r} for r in pred)
                folds.append(fold)
            inner_scores.append(aggregate(candidate, folds, family_predictions))
        chosen = select_family(inner_scores)
        detail = cache[chosen][(outer,)] if chosen is not None else None
        fold = {"held_group": outer, "selected": chosen, "inner_scores": inner_scores,
                "resolved": detail is not None and detail["resolved"]}
        if fold["resolved"]:
            evaluation, pred = evaluate(detail, [r for r in rows if r["group_id"] == outer])
            fold.update(evaluation)
        if fold["resolved"]:
            nested_predictions.extend(pred)
            fold["metrics"] = metrics(pred)
            all_predictions.extend({"stage": "nested_outer", "candidate": chosen,
                                    "outer_group": outer, "inner_group": "", **r} for r in pred)
            record = split_record(rows, outer)
            assert record["training_row_ids"] == detail["training_row_ids"]
            records.append({"stage": "nested_outer", "candidate": chosen, **record})
        nested_folds.append(fold)
    selected = select_family(fixed_scores)
    nested = aggregate("nested_selection_procedure", nested_folds, nested_predictions)
    save(output/"validation.json", {"fixed_families": fixed_scores, "nested": nested,
                                    "final_development_choice": selected})
    save(output/"splits.json", records)
    return cache, all_predictions, fixed_scores, nested, selected


def numerical_check(p, rows):
    reps = [next(r for r in rows if r["group_id"] == g) for g in groups(rows)]
    x = np.zeros((len(reps), len(NAMES)))
    x[:, 0], x[:, 1], x[:, 2], x[:, 3] = [r["hyper_a_uM"] for r in reps], 5, 7.5, [r["seed_uM"] for r in reps]
    x = initial_complexes(x, p)
    times = [0, 15, 30, 45, 60]
    coarse = react(x, 60, p, times=times)
    fine = react(x, 60, p, times=times, rtol=1e-10)
    separate = np.concatenate([react(x[i:i+1], 60, p, times=times) for i in range(len(x))], axis=1)

    def observer(y):
        return 100*reporter_product(y)/(y@MOIETIES.T)[:, :, 1]

    delta = float(np.max(np.abs(observer(coarse)-observer(fine))))
    batch_delta = float(np.max(np.abs(observer(coarse)-observer(separate))))
    balance = float(np.max(np.abs(coarse@MOIETIES.T-(x@MOIETIES.T)[None])))
    states = [{"group_id": r["group_id"], "minutes": t,
               **{name+"_uM": float(value) for name, value in zip(NAMES, coarse[ti, gi])},
               "competent_total_model_uM": float(competent_inventory(coarse[ti, gi])),
               "PAGE_product_model_uM": float(reporter_product(coarse[ti, gi]))}
              for gi, r in enumerate(reps) for ti, t in enumerate(times)]
    return {"maximum_tolerance_difference_pp": delta, "maximum_batch_difference_pp": batch_delta,
            "maximum_moiety_error_uM": balance,
            "pass": delta < 1e-4 and batch_delta < 1e-4 and balance < 1e-7}, states


def transport_metrics(rows):
    result = metrics(rows)
    positive = [r for r in rows if r["x"] > 0]
    keys = {(r["dataset"], r["seed_uM"], r["x"]) for r in positive}
    mean_errors = [np.mean([r["error_pp"] for r in positive
                           if (r["dataset"], r["seed_uM"], r["x"]) == key]) for key in keys]
    maximum = float(np.max(np.abs(mean_errors)))
    result["maximum_absolute_group_mean_error_pp"] = maximum
    result["adequate"] = result["rmse_pp"] <= 2 and maximum <= 4
    return result


def scenario_metadata(candidate, p):
    return {"candidate": candidate, "mixing_mode": p.transport, "loss_closure": p.loss,
            "complex_reset": p.complex_reset,
            "scenario": f"{candidate}|{p.transport}|{p.loss}|reset-{int(p.complex_reset)}"}


def transport_scenarios(selected):
    for candidate in PARAMETERS:
        resets = (False, True) if candidate == selected and candidate != "baseline" else (False,)
        for reset, mode, loss in itertools.product(resets, ("fractional", "contact"),
                                                    ("uniform", "all_or_none")):
            yield candidate, mode, loss, reset


def transport_predictions(p, rows, candidate):
    metadata = scenario_metadata(candidate, p)
    trajectories = {str(s): [{**metadata, **r} for r in serial(p, s)] for s in (0, 1, 2)}
    cycles = {(s, n): single_cycle(p, s, n) for s in (0, 1, 2) for n in (0, 1, 2, 3)}
    predictions = []
    for row in rows:
        if row["dataset"].startswith("S13"):
            continue
        value = (trajectories[str(int(row["seed_uM"]))][int(row["x"])]["yield_percent"]
                 if row["dataset"] == "Figure_3" else cycles[(row["seed_uM"], row["x"])])
        stage = "historical_benchmark" if row["dataset"] == "Figure_3" or row["seed_uM"] == 2 else "transport_calibration"
        predictions.append({"stage": stage, **metadata, **row,
                            "predicted_percent": value, "error_pp": value-row["value_percent"]})
    return predictions, trajectories


def fit_transport(p, rows, path):
    training = [r for r in rows if r["dataset"] == "Figure_2" and r["seed_uM"] in (0, 1) and r["x"] > 0]
    assert len(training) == 18
    detail = {"resolved": False, "complete": False, "n": len(training),
              "training_row_ids": [r["row_id"] for r in training], "evaluations": [],
              "fitted_parameters": ["mixing"], "bounds": [0, 1],
              "frozen_chemistry_parameters": asdict(p)}
    save(path, detail)

    def objective(mixing):
        entry = {"mixing": float(mixing)}
        try:
            candidate = replace(p, mixing=float(mixing))
            values = {(s, n): single_cycle(candidate, s, n) for s in (0, 1) for n in (1, 2, 3)}
            sse = float(sum((values[(r["seed_uM"], r["x"])]-r["value_percent"])**2 for r in training))
            if not np.isfinite(sse):
                raise ArithmeticError("Nonfinite transport mixing SSE")
            entry.update(resolved=True, sse=sse)
            return sse
        except (RuntimeError, ArithmeticError, ValueError) as error:
            entry.update(resolved=False, error=f"{type(error).__name__}: {error}")
            raise
        finally:
            detail["evaluations"].append(entry)
            save(path, detail)

    try:
        result = minimize_scalar(objective, bounds=(0, 1), method="bounded", options={"xatol": 1e-7})
        detail.update(nfev=int(result.nfev), message=str(result.message), success=bool(result.success))
        if not result.success or not np.isfinite(result.fun):
            raise ArithmeticError("Transport mixing optimization unresolved")
        fitted = replace(p, mixing=float(result.x))
        detail.update(resolved=True, mixing=float(result.x), sse=float(result.fun),
                      rmse_pp=float(np.sqrt(result.fun/len(training))))
        return fitted, detail
    except (RuntimeError, ArithmeticError, ValueError) as error:
        detail.update(error=f"{type(error).__name__}: {error}")
        raise
    finally:
        detail["complete"] = True
        save(path, detail)


def challenge_split(rows, joint=False):
    train = [r for r in rows if r["x"] in (15, 30)
             and (not joint or (r["seed_uM"] <= .5 and r["hyper_a_uM"] <= 2))]
    held = [r for r in rows if r["x"] in (45, 60)
            and (not joint or r["seed_uM"] == 1 or r["hyper_a_uM"] == 2.5)]
    assert not {r["row_id"] for r in train}.intersection(r["row_id"] for r in held)
    assert (len(train), len(held)) == ((12, 4) if joint else (16, 16))
    if joint:
        assert not set(groups(train)).intersection(groups(held))
    return train, held


def challenges(bulk, output):
    jobs = [(candidate, joint, *challenge_split(bulk, joint))
            for candidate in PARAMETERS for joint in (False, True)]
    paths = [output/"fits"/f"{c}__{'joint' if joint else 'late'}.json" for c, joint, _, _ in jobs]
    records, predictions = {"late_time": [], "joint_challenge": []}, []
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = pool.map(fit, [j[0] for j in jobs], [j[2] for j in jobs], paths)
        for (candidate, joint, _, held), detail in zip(jobs, results):
            stage = "joint_challenge" if joint else "late_time"
            evaluation, pred = evaluate(detail, held)
            record = {"candidate": candidate, "resolved": evaluation["resolved"],
                      "training_row_ids": detail["training_row_ids"],
                      "evaluation_row_ids": [r["row_id"] for r in held]}
            if evaluation["resolved"]:
                record.update(metrics(pred))
                predictions.extend({"stage": stage, "candidate": candidate,
                                    "outer_group": "", "inner_group": "", **r} for r in pred)
            else:
                record.update(rmse_pp=None, adequate=False, error=evaluation["error"])
            records[stage].append(record)
            save(output/f"{stage}.json", records[stage])
            print(stage.upper(), candidate, "resolved", evaluation["resolved"], flush=True)
    return records, predictions


def freeze(output):
    files = [ROOT/name for name in ("PROTOCOL.md", "WORKPLAN.md", "model.py", "test_model.py",
                                   "run.py", "test_validation.py", "plot.py", "requirements.txt")]
    files += [SOURCE/name for name in ("observations.csv", "conditions.json", "raw/salibi_data.xlsx")]
    for directory in ("diagnosis", "transport_diagnosis", "research"):
        files += [p for p in sorted((ROOT/directory).rglob("*")) if p.is_file()
                  and p.suffix in (".py", ".json", ".md", ".csv") and "__pycache__" not in p.parts]
    files += [WORKSPACE/"rna-reaction-tests-2026-10-15/results-v1/full_fits.json"]
    hashes = {}
    for source in files:
        relative = source.relative_to(WORKSPACE)
        target = output/"frozen"/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[str(relative)] = digest(target)
    save(output/"freeze.json", {"utc_before_fit": datetime.now(timezone.utc).isoformat(),
                                "files": hashes, "python": platform.python_version(),
                                "numpy": np.__version__, "scipy": scipy.__version__,
                                "matplotlib": version("matplotlib"), "openpyxl": version("openpyxl"),
                                "max_nfev": 160, "starts": STARTS, "bounds": BOUNDS,
                                "classification": "retrospective previously inspected measured data"})


def run(output):
    expected = {"python": "3.12.3", "numpy": "2.4.1", "scipy": "1.16.1",
                "matplotlib": "3.10.8", "openpyxl": "3.1.3"}
    actual = {"python": platform.python_version(), **{name: version(name) for name in expected if name != "python"}}
    if actual != expected:
        raise RuntimeError(f"Pinned runtime required: expected {expected}, found {actual}")
    output.mkdir(parents=True, exist_ok=False)
    (output/"fits").mkdir()
    (output/"mixing_fits").mkdir()
    freeze(output)
    begun = time.monotonic()
    rows = load()
    bulk = [r for r in rows if r["dataset"].startswith("S13")]
    cache, predictions, scores, nested, selected = validation(bulk, output)
    fullfits, numerical, states = {}, {}, []
    for candidate in PARAMETERS:
        detail = cache[candidate][()]
        fullfits[candidate] = detail
        if detail["resolved"]:
            p = get_parameters(detail)
            evaluation, pred = evaluate(detail, bulk)
            if evaluation["resolved"]:
                predictions.extend({"stage": "full_fit", "candidate": candidate,
                                    "outer_group": "", "inner_group": "", **r} for r in pred)
            try:
                numerical[candidate], state = numerical_check(p, bulk)
                numerical[candidate]["full_fit_prediction_resolved"] = evaluation["resolved"]
                numerical[candidate]["pass"] &= evaluation["resolved"]
                states.extend({"candidate": candidate, **r} for r in state)
            except (RuntimeError, ArithmeticError, ValueError) as error:
                numerical[candidate] = {"pass": False, "error": str(error)}
        else:
            numerical[candidate] = {"pass": False, "error": "Full-data fit unresolved"}
    challenge_results, challenge_predictions = challenges(bulk, output)
    predictions.extend(challenge_predictions)
    for score in scores + challenge_results["late_time"] + challenge_results["joint_challenge"]:
        score["threshold_screen_pass"] = score["adequate"]
        score["numerical_eligible"] = numerical[score["candidate"]]["pass"]
        score["adequate"] = score["threshold_screen_pass"] and score["numerical_eligible"]
    nested["threshold_screen_pass"] = nested["adequate"]
    nested["numerical_eligible"] = all(f["selected"] is not None and numerical[f["selected"]]["pass"]
                                       for f in nested["folds"])
    nested["adequate"] = nested["threshold_screen_pass"] and nested["numerical_eligible"]
    save(output/"validation.json", {"fixed_families": scores, "nested": nested,
                                    "final_development_choice": selected})
    save(output/"full_fits.json", fullfits)
    save(output/"numerical_checks.json", numerical)
    for stage, records in challenge_results.items():
        save(output/f"{stage}.json", records)
    write_csv(output/"predictions.csv", predictions)
    write_csv(output/"bulk_state_inventories.csv", states)
    profiles, profile_states, transport, transport_rows, trajectories, refinement = [], [], {}, [], {}, []
    selected_p = get_parameters(fullfits[selected]) if selected is not None else None
    if selected_p is not None:
        profile_jobs = [(name, float(log_value)) for name in ("kb", "krel", "kbind")
                        if name in PARAMETERS[selected] for log_value in np.linspace(*BOUNDS[name], 5)]
        paths = [output/"fits"/f"profile__{name}__{log_value:g}.json" for name, log_value in profile_jobs]
        with ProcessPoolExecutor(max_workers=4) as pool:
            results = pool.map(fit, [selected]*len(profile_jobs), [bulk]*len(profile_jobs), paths,
                               [{name: float(10**log_value)} for name, log_value in profile_jobs])
            for (name, log_value), detail in zip(profile_jobs, results):
                record = {"parameter": name, "fixed_log10": log_value, "fit": detail}
                if detail["resolved"]:
                    try:
                        _, inventory = numerical_check(get_parameters(detail), bulk)
                        profile_states.extend({"parameter": name, "fixed_log10": log_value, **r} for r in inventory)
                    except (RuntimeError, ArithmeticError, ValueError) as error:
                        record["inventory_error"] = str(error)
                profiles.append(record)
                save(output/"profiles.json", profiles)
                write_csv(output/"profile_inventories.csv", profile_states)
                print("PROFILE", name, log_value, "resolved", detail["resolved"], flush=True)
    for candidate, mode, loss, reset in transport_scenarios(selected):
        chemistry = get_parameters(fullfits[candidate])
        template = replace(chemistry or Parameters(), transport=mode, loss=loss, complex_reset=reset)
        metadata = scenario_metadata(candidate, template)
        key = metadata["scenario"]
        path = output/"mixing_fits"/f"{candidate}__{mode}__{loss}__reset-{int(reset)}.json"
        if chemistry is None:
            transport[key] = {**metadata, "resolved": False, "error": "Full-data chemistry unresolved"}
            save(output/"transport.json", transport)
            continue
        try:
            p, mixing = fit_transport(template, rows, path)
            pred, trajectory = transport_predictions(p, rows, candidate)
            benchmark = [r for r in pred if r["stage"] == "historical_benchmark" and r["x"] > 0]
            assert len(benchmark) == 72
            assert not set(mixing["training_row_ids"]).intersection(r["row_id"] for r in benchmark)
            transport[key] = {**metadata, "resolved": True, "parameters": asdict(p), "mixing_fit": mixing,
                              "prediction_resolved": True, "refinement_resolved": False,
                              "benchmark": transport_metrics(benchmark),
                              "Figure2_seed2": transport_metrics([r for r in benchmark if r["dataset"] == "Figure_2"]),
                              "Figure3": transport_metrics([r for r in benchmark if r["dataset"] == "Figure_3"])}
            transport_rows.extend(pred)
            trajectories[key] = trajectory
            for seed in (0, 1, 2):
                fine = serial(p, seed, rtol=1e-10)
                delta = max(abs(a["yield_percent"]-b["yield_percent"]) for a, b in zip(fine, trajectory[str(seed)]))
                balance = max(r["moiety_balance_max_error_uM"] for r in trajectory[str(seed)])
                refinement.append({**metadata, "seed_uM": seed, "difference_pp": delta,
                                   "moiety_error_uM": balance, "pass": delta < 1e-4 and balance < 1e-7})
            transport[key]["refinement_resolved"] = True
        except (RuntimeError, ArithmeticError, ValueError) as error:
            transport[key] = {**transport.get(key, metadata), "resolved": False, "error": f"{type(error).__name__}: {error}",
                              "mixing_fit": json.loads(path.read_text()) if path.exists() else None}
        save(output/"transport.json", transport)
        save(output/"transport_trajectories.json", trajectories)
        save(output/"transport_refinement.json", refinement)
        write_csv(output/"transport_predictions.csv", transport_rows)
        print("TRANSPORT", key, "resolved", transport[key]["resolved"], flush=True)
    for key, detail in transport.items():
        if detail["resolved"]:
            checks = [r for r in refinement if r["scenario"] == key]
            eligible = numerical[detail["candidate"]]["pass"] and len(checks) == 3 and all(r["pass"] for r in checks)
            detail["numerical_eligible"] = eligible
            for name in ("benchmark", "Figure2_seed2", "Figure3"):
                detail[name]["threshold_screen_pass"] = detail[name]["adequate"]
                detail[name]["adequate"] = detail[name]["threshold_screen_pass"] and eligible
    save(output/"profiles.json", profiles)
    write_csv(output/"profile_inventories.csv", profile_states)
    save(output/"transport.json", transport)
    save(output/"transport_trajectories.json", trajectories)
    save(output/"transport_refinement.json", refinement)
    write_csv(output/"transport_predictions.csv", transport_rows)
    summary = {"classification": "retrospective; all measured data previously inspected",
               "selected_chemistry": selected, "selected_full_fit_resolved": selected_p is not None,
               "fixed_family_scores": [{k: v for k, v in s.items() if k != "folds"} for s in scores],
               "nested_selection": {k: v for k, v in nested.items() if k != "folds"},
               **challenge_results, "transport": transport,
               "all_full_fit_numerical_checks_pass": all(n["pass"] for n in numerical.values()),
               "all_transport_refinement_pass": bool(refinement) and all(d["resolved"] for d in transport.values())
                                                and all(r["pass"] for r in refinement),
               "elapsed_seconds": time.monotonic()-begun,
               "scientific_limit": "PAGE reporter data do not identify active F1 or a unique mechanism; transport closures remain hypotheses."}
    save(output/"summary.json", summary)
    from plot import plot
    plot(output)
    save(output/"manifest.json", {str(p.relative_to(output)): digest(p) for p in sorted(output.rglob("*"))
                                 if p.is_file() and p.name != "manifest.json"})
    print(json.dumps(summary, indent=2))


def replay(directory):
    manifest = json.loads((directory/"manifest.json").read_text())
    assert all(digest(directory/name) == value for name, value in manifest.items()), "Manifest mismatch"
    frozen = json.loads((directory/"freeze.json").read_text())["files"]
    assert all(digest(directory/"frozen"/name) == value for name, value in frozen.items()), "Snapshot mismatch"
    assert all(digest(WORKSPACE/name) == value for name, value in frozen.items()), "Current frozen-input mismatch"
    rows = load()
    by_id = {r["row_id"]: r for r in rows}
    maximum_sse_difference, replayed_fits = 0., 0
    for path in sorted((directory/"fits").glob("*.json")):
        detail = json.loads(path.read_text())
        assert detail["complete"] and len(detail["starts"]) == 6
        if detail["resolved"]:
            pred = predict(get_parameters(detail), [by_id[i] for i in detail["training_row_ids"]])
            sse = sum(r["error_pp"]**2 for r in pred)
            delta = abs(sse-detail["sse"])
            assert delta <= 1e-8 + abs(detail["sse"])*1e-8, path
            maximum_sse_difference = max(maximum_sse_difference, delta)
            replayed_fits += 1
    records = json.loads((directory/"splits.json").read_text())
    for record in records:
        assert_split(record)
    with (directory/"predictions.csv").open() as stream:
        saved = list(csv.DictReader(stream))
    dose_groups = groups([r for r in rows if r["dataset"].startswith("S13")])
    batches = {}
    for row in saved:
        if "predicted_percent" not in row:
            continue
        if row["stage"] in ("late_time", "joint_challenge"):
            suffix = "late" if row["stage"] == "late_time" else "joint"
            filename = f"{row['candidate']}__{suffix}.json"
        else:
            omitted = sorted([g for g in (row["outer_group"], row["inner_group"]) if g])
            suffix = "-".join(str(dose_groups.index(g)) for g in omitted) or "none"
            filename = f"{row['candidate']}__omit-{suffix}.json"
        batches.setdefault((filename, row["stage"], row["outer_group"], row["inner_group"]), []).append(row)
    maximum_prediction_difference, replayed_predictions = 0., 0
    for (filename, _, _, _), saved_rows in batches.items():
        p = get_parameters(json.loads((directory/"fits"/filename).read_text()))
        original = [by_id[r["row_id"]] for r in saved_rows]
        regenerated = predict(p, original)
        delta = max(abs(float(a["predicted_percent"])-b["predicted_percent"]) for a, b in zip(saved_rows, regenerated))
        assert all(abs(float(a["predicted_percent"])-b["predicted_percent"]) <=
                   1e-8 + 1e-8*abs(b["predicted_percent"]) for a, b in zip(saved_rows, regenerated)), filename
        maximum_prediction_difference = max(maximum_prediction_difference, delta)
        replayed_predictions += len(saved_rows)
    transport = json.loads((directory/"transport.json").read_text())
    with (directory/"transport_predictions.csv").open() as stream:
        saved_transport = list(csv.DictReader(stream))
    for scenario, detail in transport.items():
        saved_mode = [r for r in saved_transport if r.get("scenario") == scenario]
        if saved_mode:
            assert "parameters" in detail, scenario
            pred, _ = transport_predictions(Parameters(**detail["parameters"]), rows, detail["candidate"])
            assert len(pred) == len(saved_mode)
            delta = max(abs(a["predicted_percent"]-float(b["predicted_percent"])) for a, b in zip(pred, saved_mode))
            assert delta < 1e-8
            maximum_prediction_difference = max(maximum_prediction_difference, delta)
            replayed_predictions += len(pred)
    print(json.dumps({"status": "PASS", "replayed_resolved_fits": replayed_fits,
                      "replayed_predictions": replayed_predictions, "split_records_checked": len(records),
                      "maximum_sse_difference": maximum_sse_difference,
                      "maximum_prediction_difference_pp": maximum_prediction_difference,
                      "manifest_and_frozen_sources_match": True}, indent=2))


def development(output):
    output.mkdir(parents=True, exist_ok=False)
    synthetic = []
    truth = Parameters(kf=.1, kh=.001, kb=1, ka=.08, krh=.002, kd=.001,
                       turnover=True, krel=.1, kbind=.02)
    for i, (seed, hyper) in enumerate(((.1, 0), (.25, 0), (.5, 0), (1, 0), (0, 1), (0, 1.5), (0, 2), (0, 2.5))):
        values = bulk_curves(truth, [seed], [hyper])[0]
        for t, value in zip((0, 15, 30, 45, 60), values):
            synthetic.append({"group_id": f"synthetic_{i}", "row_id": f"synthetic_{i}_{t}",
                              "seed_uM": seed, "hyper_a_uM": hyper, "x": t, "value_percent": float(value)})
    timing = {}
    for candidate in ("baseline", "reversible_free"):
        begun = time.monotonic()
        detail = fit(candidate, synthetic, output/f"{candidate}.json")
        timing[candidate] = {"seconds": time.monotonic()-begun, "resolved": detail["resolved"],
                             "successful_starts": detail.get("successful_starts", 0),
                             "synthetic_rmse_pp": detail.get("rmse_pp"),
                             "known_mechanism_curve_recovered":
                             (detail["resolved"] and detail["rmse_pp"] < 1e-3)
                             if candidate == "reversible_free" else None}
    save(output/"timing.json", {"classification": "synthetic implementation timing only", "fits": timing})
    print(json.dumps(timing, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path)
    action.add_argument("--replay", type=Path)
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args()
    if args.development and args.replay:
        parser.error("--development requires --output")
    if args.replay:
        replay(args.replay)
    elif args.development:
        development(args.output)
    else:
        run(args.output)
