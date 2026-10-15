"""Replay retained RNA failures and audit residuals; no parameter optimization."""
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import openpyxl
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OLD = ROOT / "rna-reaction-tests-2026-10-15"
RESULTS = OLD / "results-v1"
SOURCE = ROOT / "measured-coupling-2026-10-15/rna_sources"
SELECTED = "independent_inactivation"
FAMILIES = ("revised", "independent", SELECTED)
sys.dont_write_bytecode = True


def read_csv(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(name, rows):
    with (OUT / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(rows):
    error = np.array([float(r["error_pp"]) for r in rows])
    assert len(error) > 0 and np.all(np.isfinite(error))
    return dict(n=len(error), rmse_pp=float(np.sqrt(np.mean(error**2))),
                bias_pp=float(error.mean()), maximum_absolute_error_pp=float(np.max(abs(error))),
                sse_pp2=float(error @ error))


def independent_replay(parameters, groups):
    """Independent six-state DOP853 implementation for non-trapping families."""
    p = parameters
    initial = np.array([[h, 5., 7.5, f, 0., 0.] for f, h in groups])

    def rhs(_, flattened):
        a, r, b, f, _, _ = flattened.reshape(-1, 6).T
        s = b / (p["kb"] + b)
        va = (p["kf"] if p["ka"] is None else p["ka"]) * f*a*s + p["kh"]*a*a*s*s
        vr = p["kf"]*f*r*s + p["krh"]*a*r*s*s
        loss = p["kd"]*f
        return np.column_stack((-va, -vr, -va-vr, va-loss, vr, loss)).ravel()

    result = solve_ivp(rhs, (0., 60.), initial.ravel(), method="DOP853",
                       t_eval=[0, 15, 30, 45, 60], rtol=1e-11, atol=1e-13)
    assert result.success
    states = result.y.T.reshape(5, len(groups), 6).transpose(1, 0, 2)
    moieties = np.array([[1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 1, 1]])
    assert np.max(abs(states @ moieties.T - (initial @ moieties.T)[:, None, :])) < 1e-8
    assert states.min() >= -1e-9
    return 100 * states[:, :, 4] / (states[:, :, 1] + states[:, :, 4]), states


def main():
    inputs = [SOURCE / "observations.csv", SOURCE / "raw/salibi_data.xlsx",
              ROOT / "rna-mechanism-2026-10-15/sources/salibi/observations.csv",
              OLD / "model.py", OLD / "run.py", OLD / "PROTOCOL.md"]
    inputs += [RESULTS / name for name in ("predictions.csv", "full_fits.json", "validation.json",
              "transport_predictions.csv", "transport.json", "bulk_state_inventories.csv", "freeze.json")]
    inputs += sorted((RESULTS / "fits").glob("*.json"))
    before = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    freeze = json.loads((RESULTS / "freeze.json").read_text())["files"]
    checked_frozen = 0
    for relative, expected in freeze.items():
        if relative in before:
            assert before[relative] == expected, relative
            checked_frozen += 1

    source = read_csv(SOURCE / "observations.csv")
    assert len(source) == 148
    origins = {(r["source_sheet"], r["source_cell"]): r for r in source}
    workbook = openpyxl.load_workbook(SOURCE / "raw/salibi_data.xlsx", data_only=True, read_only=True)
    checked_cells = 0
    for row in source:
        assert float(row["value_percent"]) == float(workbook[row["source_sheet"]][row["source_cell"]].value)
        checked_cells += 1
    previous_export = read_csv(inputs[2])
    for row in previous_export:
        if row["dataset"] not in ("S13_F1", "S13_HyperA"):
            continue
        retained = origins[row["source_sheet"], row["source_cell"]]
        assert float(retained["sd_percent"]) == float(row["sd"])
        assert float(retained["n"]) == float(row["n"]) == 3
        for field, address in (("sd", "source_sd_cell"), ("n", "source_n_cell")):
            assert float(row[field]) == float(workbook[row["source_sheet"]][row[address]].value)
            checked_cells += 1
    workbook.close()
    assert checked_cells == 228

    predictions = read_csv(RESULTS / "predictions.csv")
    transport = read_csv(RESULTS / "transport_predictions.csv")
    for row in predictions + transport:
        origin = origins[row["source_sheet"], row["source_cell"]]
        for key in ("value_percent", "seed_uM", "hyper_a_uM", "x"):
            assert float(row[key]) == float(origin[key])
        assert abs(float(row["predicted_percent"]) - float(row["value_percent"]) - float(row["error_pp"])) < 1e-12
    groups = sorted({r["group_id"] for r in predictions})
    doses = [(float(g.split("|")[1]), float(g.split("|")[2])) for g in groups]
    fullfits = json.loads((RESULTS / "full_fits.json").read_text())
    residuals = [r for r in predictions if r["candidate"] in FAMILIES
                 and r["stage"] in ("full_fit", "fixed_dose", "late_time")]
    replay_max = 0.
    replay_count = 0
    inventory_max = 0.
    replay_worst = None
    state_rows = []
    for candidate in FAMILIES:
        for stage in ("full_fit", "fixed_dose", "late_time"):
            for index, group in enumerate(groups):
                if stage == "full_fit":
                    fit = fullfits[candidate]
                else:
                    suffix = "late" if stage == "late_time" else f"omit-{index}"
                    fit = json.loads((RESULTS / "fits" / f"{candidate}__{suffix}.json").read_text())
                assert fit["resolved"]
                predicted, state = independent_replay(fit["parameters"], [doses[index]])
                records = [r for r in residuals if r["candidate"] == candidate and r["stage"] == stage and r["group_id"] == group]
                for row in records:
                    time_index = int(float(row["x"]) / 15)
                    delta = abs(predicted[0, time_index] - float(row["predicted_percent"]))
                    if delta > replay_max:
                        replay_max = float(delta)
                        replay_worst = dict(candidate=candidate, stage=stage, group=group, minutes=float(row["x"]))
                    replay_count += 1
                for ti, minutes in enumerate((0, 15, 30, 45, 60)):
                    state_rows.append(dict(candidate=candidate, stage=stage, group_id=group, minutes=minutes,
                        predicted_percent=float(predicted[0, ti]),
                        **{n + "_uM": float(state[0, ti, j]) for j, n in enumerate(("HyperA", "Cy5A", "B", "F1", "Cy5F1", "inactive_F1"))}))
                if stage == "full_fit":
                    inventory = [r for r in read_csv(RESULTS / "bulk_state_inventories.csv")
                                 if r["candidate"] == candidate and r["group_id"] == group]
                    names = ("HyperA", "Cy5A", "B", "F1", "Cy5F1", "inactive_F1")
                    for row in inventory:
                        ti = int(row["minutes"]) // 15
                        inventory_max = max(inventory_max, max(abs(float(row[n + "_uM"]) - state[0, ti, j]) for j, n in enumerate(names)))
    assert replay_count == len(residuals) == 288
    assert replay_max < 1e-4 and inventory_max < 1e-5
    write_csv("residuals.csv", residuals)
    write_csv("replayed_inventories.csv", state_rows)

    summaries = {}
    for candidate in FAMILIES:
        summaries[candidate] = {}
        for stage in ("full_fit", "fixed_dose", "late_time"):
            rows = [r for r in residuals if r["candidate"] == candidate and r["stage"] == stage and float(r["x"]) > 0]
            summaries[candidate][stage] = dict(overall=metrics(rows),
                by_group={g: metrics([r for r in rows if r["group_id"] == g]) for g in groups},
                by_time={str(t): metrics([r for r in rows if float(r["x"]) == t]) for t in sorted({float(r["x"]) for r in rows})},
                by_branch={d: metrics([r for r in rows if r["dataset"] == d]) for d in ("S13_F1", "S13_HyperA")})
            if stage == "fixed_dose":
                summaries[candidate][stage]["dose_position"] = {
                    name: metrics([r for r in rows if r["group_id"] in [groups[i] for i in indices]])
                    for name, indices in (("endpoint_extrapolation", (0, 3, 4, 7)), ("interior_interpolation", (1, 2, 5, 6)))}

    parameter_rows = []
    for suffix in ["omit-none", *[f"omit-{i}" for i in range(8)], "late"]:
        fit = json.loads((RESULTS / "fits" / f"{SELECTED}__{suffix}.json").read_text())
        row = dict(fit=suffix, omitted_group=groups[int(suffix[5:])] if suffix.startswith("omit-") and suffix != "omit-none" else "",
                   training_rmse_pp=fit["rmse_pp"], successful_starts=fit["successful_starts"],
                   agreeing_starts=fit["agreeing_successful_starts"],
                   **{key: fit["parameters"][key] for key in fit["free_parameters"]},
                   activity_half_life_min=math.log(2) / fit["parameters"]["kd"],
                   active_bounds="|".join(str(x) for x in fit["active_bounds"]))
        parameter_rows.append(row)
    write_csv("parameter_changes.csv", parameter_rows)
    all_fits = [(p, json.loads(p.read_text())) for p in sorted((RESULTS / "fits").glob("*.json"))]
    optimization = dict(fits=len(all_fits), starts=sum(len(f["starts"]) for _, f in all_fits),
        unresolved=[p.name for p, f in all_fits if not f["resolved"]],
        no_two_start_agreement=[p.name for p, f in all_fits if not f["two_starts_agree"]],
        capped=[dict(fit=p.name, start_id=s["start_id"], sse=s["sse"])
                for p, f in all_fits for s in f["starts"] if s["status"] == 0])

    spec = importlib.util.spec_from_file_location("retained_rna_audit_model", OLD / "model.py")
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)
    transport_parameters = json.loads((RESULTS / "transport.json").read_text())
    transport_max = 0.
    transport_groups = []
    transport_summary = {}
    for mode, detail in transport_parameters.items():
        p = model.Parameters(**detail["parameters"])
        cached = {}
        for seed in (0., 1., 2.):
            cached["Figure_3", seed] = {float(r["generation"]): r["yield_percent"] for r in model.serial(p, seed)}
            cached["Figure_2", seed] = {float(n): model.single_cycle(p, seed, n) for n in range(4)}
        rows = [r for r in transport if r["transport"] == mode]
        for row in rows:
            prediction = cached[row["dataset"], float(row["seed_uM"])][float(row["x"])]
            transport_max = max(transport_max, abs(prediction - float(row["predicted_percent"])))
        for dataset, seed, time in sorted({(r["dataset"], float(r["seed_uM"]), float(r["x"])) for r in rows if float(r["x"]) > 0}):
            rr = [r for r in rows if (r["dataset"], float(r["seed_uM"]), float(r["x"])) == (dataset, seed, time)]
            transport_groups.append(dict(transport=mode, dataset=dataset, seed_uM=seed, x=time,
                stage=rr[0]["stage"], observed_mean_percent=float(np.mean([float(r["value_percent"]) for r in rr])),
                predicted_percent=float(rr[0]["predicted_percent"]), **metrics(rr)))
        benchmark = [r for r in rows if r["stage"] == "historical_benchmark" and float(r["x"]) > 0]
        transport_summary[mode] = dict(overall=metrics(benchmark),
            by_branch={f"{dataset}|{seed:g}": metrics([r for r in benchmark if r["dataset"] == dataset and float(r["seed_uM"]) == seed])
                       for dataset, seed in sorted({(r["dataset"], float(r["seed_uM"])) for r in benchmark})})
    assert transport_max < 1e-8
    write_csv("transport_group_residuals.csv", transport_groups)

    inventory_rows = [r for r in read_csv(RESULTS / "bulk_state_inventories.csv") if r["candidate"] in FAMILIES and r["minutes"] == "60"]
    write_csv("endpoint_inventories.csv", inventory_rows)
    assert all(digest(ROOT / relative) == sha for relative, sha in before.items())
    save("summary.json", dict(metrics=summaries, optimization=optimization, transport=transport_summary,
        selected_parameter_changes=parameter_rows,
        evidence_class="Retrospective diagnosis of existing inspected observations; no fit or new experimental validation"))
    receipt = dict(status="PASS", workbook_values_checked=checked_cells, frozen_files_checked=checked_frozen,
        bulk_predictions_independently_replayed=replay_count, bulk_replay_solver="DOP853 rtol=1e-11 atol=1e-13",
        maximum_independent_bulk_replay_difference_pp=replay_max, maximum_inventory_difference_uM=inventory_max,
        worst_bulk_replay_location=replay_worst,
        transport_predictions_replayed=len(transport), transport_replay="retained model with saved parameters; independent score aggregation",
        maximum_transport_replay_difference_pp=transport_max,
        residual_arithmetic_rows_checked=len(predictions) + len(transport), all_input_hashes_unchanged=True,
        input_hashes=before, audit_script_sha256=digest(Path(__file__)))
    save("verification.json", receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k != "input_hashes"}, indent=2))


if __name__ == "__main__":
    main()
