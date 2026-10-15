"""Audit prior predictions against workbook cells; no fitting or source mutation."""
import csv
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OLD = ROOT / "rna-mechanism-2026-10-15"
RESULTS = OLD / "model/results-v2"


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def metrics(rows):
    errors = [float(r["error_pp"]) for r in rows]
    scaled = [abs(float(r["error_pp"])) / float(r["sd_percent"])
              for r in rows if float(r["sd_percent"]) > 0]
    return {"n": len(errors), "rmse_pp": math.sqrt(sum(e*e for e in errors)/len(errors)),
            "bias_pp": sum(errors)/len(errors), "max_absolute_error_pp": max(map(abs, errors)),
            "n_nonzero_sd": len(scaled), "n_abs_error_above_2_reported_sd": sum(z > 2 for z in scaled),
            "maximum_abs_error_over_reported_sd": max(scaled, default=None)}


def main():
    import openpyxl
    inputs = [RESULTS / name for name in ("kinetic_predictions.csv", "cross_validation_predictions.csv",
              "full_fits.json", "cross_validation.json", "profiles.json", "summary.json")]
    inputs += [OLD / "model/model.py", OLD / "sources/salibi/observations.csv",
               OLD / "sources/salibi/conditions.json",
               ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi_data.xlsx"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    fitted = read_csv(inputs[0]); held = read_csv(inputs[1])
    assert len(fitted) == len(held) == 200
    fits = json.loads(inputs[2].read_text()); cv = json.loads(inputs[3].read_text())
    profiles = json.loads(inputs[4].read_text())
    selected = json.loads(inputs[5].read_text())["selected_chemistry"]
    source = {r["source_cell"]: r for r in read_csv(inputs[7]) if r["dataset"] in ("S13_F1", "S13_HyperA")}
    assert len(source) == 40 and selected == "saturation"
    book = openpyxl.load_workbook(inputs[-1], data_only=True, read_only=True)
    for cell, row in source.items():
        for field, coordinate in (("value",cell), ("sd",row["source_sd_cell"]), ("n",row["source_n_cell"])):
            assert float(row[field]) == float(book["S13"][coordinate].value), (cell, field)
    book.close()
    spec = importlib.util.spec_from_file_location("old_rna_diagnostic_model", inputs[6])
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)
    replay_max = 0.0
    all_groups = {}
    all_rows = []
    for label, rows in (("full_fit", fitted), ("held_dose", held)):
        grouped = defaultdict(list)
        for row in rows:
            origin = source[row["source_cell"]]
            assert float(row["value_percent"]) == float(origin["value"])
            assert float(row["sd_percent"]) == float(origin["sd"])
            assert float(row["x"]) == float(origin["x"])
            assert float(row["n"]) == float(origin["n"]) == 3
            assert row["dataset"] == origin["dataset"]
            dose = float(origin["group"].split("_")[1])
            assert (float(row["seed_uM"]), float(row["hyper_a_uM"])) == ((dose,0.) if row["dataset"] == "S13_F1" else (0.,dose))
            assert abs(float(row["error_pp"]) - (float(row["predicted_percent"])-float(row["value_percent"]))) < 1e-12
            grouped[(row["candidate"], row["dataset"], float(row["seed_uM"]), float(row["hyper_a_uM"]))].append(row)
            all_rows.append(dict(validation=label, **row,
                                 error_over_sd=None if float(row["sd_percent"]) == 0 else float(row["error_pp"])/float(row["sd_percent"])))
        for (candidate, dataset, seed, hyper), group in grouped.items():
            group.sort(key=lambda r: float(r["x"]))
            assert [float(r["x"]) for r in group] == [0,15,30,45,60]
            params = fits[candidate]["parameters"]
            if label == "held_dose":
                score = next(s for s in cv["scores"] if s["candidate"] == candidate)
                fold = next(f for f in score["folds"] if f["held_dose"] == [dataset,seed,hyper])
                params = fold["fit"]["parameters"]
            prediction = model.bulk_curve(model.Parameters(**params), seed=seed, hyper=hyper,
                                          times=[float(r["x"]) for r in group])
            replay_max = max(replay_max, *(abs(float(p)-float(r["predicted_percent"])) for p,r in zip(prediction,group)))
        all_groups[label] = {
            "candidate": {c: metrics([r for r in rows if r["candidate"] == c]) for c in fits},
            "selected_by_dose": {"|".join(map(str,key[1:])): metrics(group) for key,group in grouped.items() if key[0] == selected},
            "selected_by_dataset": {d: metrics([r for r in rows if r["candidate"] == selected and r["dataset"] == d]) for d in ("S13_F1", "S13_HyperA")},
            "selected_by_time": {str(t): metrics([r for r in rows if r["candidate"] == selected and float(r["x"]) == t]) for t in (0,15,30,45,60)},
            "selected_nonzero": metrics([r for r in rows if r["candidate"] == selected and float(r["x"]) > 0]),
        }
    assert replay_max < 1e-8
    selected_rows = [r for r in fitted if r["candidate"] == selected]
    f1 = [r for r in selected_rows if r["dataset"] == "S13_F1" and float(r["x"]) > 0]
    exposure_pairs = []
    for a,b in itertools.combinations(f1, 2):
        if float(a["seed_uM"])*float(a["x"]) != float(b["seed_uM"])*float(b["x"]):
            continue
        difference = float(b["value_percent"])-float(a["value_percent"])
        combined_sd = math.hypot(float(a["sd_percent"]), float(b["sd_percent"]))
        predicted_difference = float(b["predicted_percent"])-float(a["predicted_percent"])
        assert abs(predicted_difference) < 1e-5
        exposure_pairs.append({"first_cell":a["source_cell"], "second_cell":b["source_cell"],
            "exposure_uM_min":float(a["seed_uM"])*float(a["x"]),
            "first_seed_uM":float(a["seed_uM"]), "first_time_min":float(a["x"]),
            "second_seed_uM":float(b["seed_uM"]), "second_time_min":float(b["x"]),
            "observed_difference_pp":difference, "combined_reported_sd_pp":combined_sd,
            "difference_over_combined_sd":difference/combined_sd,
            "predicted_difference_pp":predicted_difference})
    shapes = []
    for dataset in ("S13_F1", "S13_HyperA"):
        doses = sorted(set(float(r["seed_uM"])+float(r["hyper_a_uM"]) for r in selected_rows if r["dataset"] == dataset))
        for dose in doses:
            rows = sorted([r for r in selected_rows if r["dataset"] == dataset and float(r["seed_uM"])+float(r["hyper_a_uM"]) == dose], key=lambda r:float(r["x"]))
            observed = [float(r["value_percent"]) for r in rows]
            predicted = [float(r["predicted_percent"]) for r in rows]
            obs_inc = [b-a for a,b in zip(observed,observed[1:])]
            pred_inc = [b-a for a,b in zip(predicted,predicted[1:])]
            shapes.append(dict(dataset=dataset,dose_uM=dose,observed=observed,predicted=predicted,
                observed_15min_increments_pp=obs_inc,predicted_15min_increments_pp=pred_inc,
                observed_second_differences_pp=[b-a for a,b in zip(obs_inc,obs_inc[1:])],
                predicted_second_differences_pp=[b-a for a,b in zip(pred_inc,pred_inc[1:])]))
    summary = dict(selected=selected,metrics=all_groups,matched_exposure=exposure_pairs,shapes=shapes,
        parameter_diagnostics={c:dict(parameters=f["parameters"], bounds_hit=f["bounds_hit"],
            jacobian_condition_number=max(f["jacobian_singular_values"])/min(f["jacobian_singular_values"])) for c,f in fits.items()},
        KB_profiles=[dict(KB_uM=p["fixed_KB_uM"],rmse_pp=p["fit"]["rmse_pp"]) for p in profiles],
        limitations=["S13 has summary means and SD (n=3), not individual replicates or cross-time covariance.",
            "SD-scaled diagnostics are descriptive, not p values or a calibrated chi-square test.",
            "All values were previously inspected; cross-validation is retrospective development evidence.",
            "Reporter ligation is not an independent measurement of active F1 formation."])
    (OUT / "summary.json").write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n")
    keys = list(dict.fromkeys(k for r in all_rows for k in r))
    with (OUT / "residuals.csv").open("w",newline="") as handle:
        writer=csv.DictWriter(handle, fieldnames=keys);writer.writeheader();writer.writerows(all_rows)
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == sha for p,sha in hashes.items())
    verification = dict(status="PASS",workbook_summary_values_checked=120,predictions_replayed=len(all_rows),
        diagnostic_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        replay_max_absolute_error_pp=replay_max, matched_exposure_pairs=len(exposure_pairs),
        source_hashes=hashes,source_hashes_unchanged=True,
        outputs={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ("summary.json","residuals.csv")})
    evidence=OUT/".omo/evidence";evidence.mkdir(parents=True,exist_ok=True)
    (evidence/"verification.json").write_text(json.dumps(verification,indent=2)+"\n")
    print(json.dumps({k:v for k,v in verification.items() if k not in ("source_hashes","outputs")}))


if __name__ == "__main__":
    main()
