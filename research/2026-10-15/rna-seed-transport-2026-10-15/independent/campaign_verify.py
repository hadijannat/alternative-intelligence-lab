"""Audit a completed frozen campaign without fitting or changing its outputs."""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys

import numpy as np
import openpyxl

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
ROOT = LAB.parent
SPECIES = ("A", "R", "B", "F", "P", "D", "H")
MOIETIES = np.array([[1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 0, 1, 0, 0],
                     [0, 0, 1, 1, 1, 1, 0]], float)
PARAMETERS = {"legacy": ("mixing",), "bath": ("nu",), "patch": ("nu", "diffusion")}
BOUNDS = {"mixing": (0, 1), "nu": (0, math.log10(30)), "diffusion": (-3, 1)}
FRACTIONS = (.05, .2, .4, .6, .8, .95)
DIFFUSION_FRACTIONS = (.95, .8, .6, .4, .2, .05)
IGNORED_JSON_FIELDS = {"elapsed_seconds", "utc_before_fit"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def read_csv(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def scientific(value):
    if isinstance(value, dict):
        return {k: scientific(v) for k, v in value.items() if k not in IGNORED_JSON_FIELDS}
    if isinstance(value, list):
        return [scientific(v) for v in value]
    return value


def number_count(value):
    if isinstance(value, dict):
        return sum(number_count(v) for v in value.values())
    if isinstance(value, list):
        return sum(number_count(v) for v in value)
    return int(isinstance(value, (int, float)) and not isinstance(value, bool))


class Audit:
    def __init__(self):
        self.rows = []
        self.max_arithmetic_error = 0.0

    def check(self, name, passed, detail=""):
        self.rows.append({"check": name, "pass": bool(passed), "detail": detail})

    def close(self, name, value, expected, tolerance=1e-9):
        error = abs(float(value) - float(expected))
        self.max_arithmetic_error = max(self.max_arithmetic_error, error)
        self.check(name, math.isfinite(error) and error <= tolerance,
                   {"value": float(value), "expected": float(expected), "absolute_error": error,
                    "tolerance": tolerance})


def metrics(rows, eligible):
    errors = [float(row["error_pp"]) for row in rows]
    groups = {}
    for row in rows:
        key = row["dataset"], float(row["seed_uM"]), float(row["x"])
        groups.setdefault(key, []).append(float(row["error_pp"]))
    rmse = math.sqrt(math.fsum(e*e for e in errors)/len(errors))
    maximum = max(abs(math.fsum(e)/len(e)) for e in groups.values())
    screen = rmse <= 2 and maximum <= 4
    return {"resolved": True, "n": len(rows), "n_conditions": len(groups), "rmse_pp": rmse,
            "max_absolute_condition_mean_error_pp": maximum,
            "max_absolute_replicate_error_pp": max(abs(e) for e in errors),
            "bias_pp": math.fsum(errors)/len(errors), "threshold_screen_pass": screen,
            "numerical_eligible": eligible, "adequate": bool(screen and eligible)}


def vector(row, label):
    return np.array([float(row[f"{label}_{s}_uM"]) for s in SPECIES])


def audit_stages(rows, scenarios, audit, prefix):
    groups = {}
    for row in rows:
        groups.setdefault((row["scenario"], row["seed_uM"]), []).append(row)
    for (scenario, seed), records in groups.items():
        detail = scenarios[scenario]
        nu = detail["parameters"].get("nu", 0)
        previous = None
        for index, row in enumerate(records):
            label = f"{prefix}:{scenario}:seed{seed}:stage{index}"
            inside, outside, source, removed = (vector(row, k) for k in ("inside", "outside", "source", "removed"))
            denominator = inside[1]+inside[4]
            audit.close(label+":PAGE", row["yield_percent"], 100*inside[4]/denominator if denominator else 0)
            audit.close(label+":denominator", row["reporter_denominator_inside_uM"], denominator)
            audit.close(label+":exterior_volume", np.max(abs(outside-nu*vector(row, "outside_concentration"))), 0)
            balance = float(np.max(abs(MOIETIES @ (source-removed-inside-outside))))
            audit.close(label+":balance_record", row["moiety_balance_max_error_uM"], balance)
            audit.check(label+":conservation", balance <= 1e-6, balance)
            audit.check(label+":nonnegative", min(inside.min(), outside.min()) >= -1e-10)
            for place, quantities in (("inside", inside), ("outside", outside)):
                audit.check(label+":"+place+":founder_subset", quantities[6] <= quantities[3]+1e-8)
                for field, expected in (("competent", quantities[3]), ("founder", quantities[6]),
                                        ("newly_generated_competent", max(0, quantities[3]-quantities[6]))):
                    audit.close(label+":"+field+":"+place, row[f"{field}_{place}_uM"], expected)
            for name, values in (("source", source), ("removed", removed), ("retained", inside+outside)):
                for j, value in enumerate(MOIETIES @ values, 1):
                    audit.close(label+f":{name}_moiety{j}", row[f"{name}_moiety_{j}_uM"], value)
            if previous is None:
                expected = np.array([10/3, 2.5/3, 5, float(seed)/3, 0, 0, float(seed)/3])
                audit.close(label+":initial", np.max(abs(inside-expected)), 0)
            else:
                prior_inside, prior_outside = vector(previous, "inside"), vector(previous, "outside")
                stage = row["stage"]
                if stage == "feed":
                    fresh = np.array([2.5, .625, 3.75, 0, 0, 0, 0])
                    audit.close(label+":feed_inside", np.max(abs(inside-.5*prior_inside-fresh)), 0)
                    audit.close(label+":feed_outside", np.max(abs(outside-.5*prior_outside)), 0)
                    audit.close(label+":feed_source", np.max(abs(source-vector(previous,"source")-fresh)), 0)
                    audit.close(label+":feed_removed", np.max(abs(removed-vector(previous,"removed")-.5*(prior_inside+prior_outside))), 0)
                elif stage == "exchange":
                    if detail["family"] == "legacy":
                        audit.close(label+":legacy_retention", np.max(abs(inside-.55*prior_inside)), 0)
                        audit.close(label+":legacy_removal", np.max(abs(removed-vector(previous,"removed")-.45*prior_inside)), 0)
                    else:
                        audit.close(label+":exchange_inventory", np.max(abs(inside+outside-prior_inside-prior_outside)), 0)
                elif stage == "warm_start":
                    audit.close(label+":warm_inside", np.max(abs(inside-prior_inside)), 0)
                    audit.close(label+":warm_outside", np.max(abs(outside-prior_outside)), 0)
                elif stage == "measurement":
                    audit.close(label+":inside_production", row["new_reporter_inside_uM"], inside[4]-prior_inside[4])
                    audit.close(label+":outside_production", row["new_reporter_outside_uM"], outside[4]-prior_outside[4])
                    audit.close(label+":inside_chemical_balance", np.max(abs(MOIETIES@(inside-prior_inside))), 0, 1e-7)
                    audit.close(label+":outside_chemical_balance", np.max(abs(MOIETIES@(outside-prior_outside))), 0, 1e-7)
                    factor = math.exp(-0.012946670134460872*60)
                    audit.close(label+":inside_founder_decay", inside[6], prior_inside[6]*factor)
                    audit.close(label+":outside_founder_decay", outside[6], prior_outside[6]*(factor if detail["exterior_reactive"] else 1))
                elif stage == "discard":
                    audit.close(label+":discarded_exterior", np.max(abs(outside)), 0)
                    audit.close(label+":discarded_inside", np.max(abs(inside-prior_inside)), 0)
                    audit.close(label+":discard_removed", np.max(abs(removed-vector(previous,"removed")-prior_outside)), 0)
                    audit.close(label+":discard_ledger", np.max(abs(vector(row,"discarded")-vector(previous,"discarded")-prior_outside)), 0)
            previous = row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    main_dir, repeat_dir = LAB/"results-v1", LAB/"verification-v1"
    for folder in (main_dir, repeat_dir):
        if not (folder/"manifest.json").is_file():
            raise SystemExit(f"Campaign incomplete: missing {folder}/manifest.json; no audit output created")
    args.output.mkdir(parents=True, exist_ok=False)
    audit = Audit()
    comparison_rows = []
    manifests = [read_json(p/"manifest.json") for p in (main_dir, repeat_dir)]
    audit.check("main_refit_same_file_set", set(manifests[0]) == set(manifests[1]))
    for folder, manifest in zip((main_dir, repeat_dir), manifests):
        actual_files = {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file() and p.name != "manifest.json"}
        audit.check(folder.name+":manifest_completeness", actual_files == set(manifest))
        for name, digest in manifest.items():
            audit.check(folder.name+":manifest:"+name, sha(folder/name) == digest)
        freeze = read_json(folder/"freeze.json")
        audit.check(folder.name+":runtime", freeze["runtime"] == {"python":"3.12.3","numpy":"2.4.1","scipy":"1.16.1","matplotlib":"3.10.8","openpyxl":"3.1.3"})
        for name, digest in freeze["files"].items():
            audit.check(folder.name+":frozen:"+name, sha(folder/"frozen"/name) == digest)
            audit.check(folder.name+":live_frozen:"+name, sha(ROOT/name) == digest)
        before, after = (read_json(folder/f"prior_integrity_{suffix}.json") for suffix in ("before", "after"))
        audit.check(folder.name+":prior_before_after", before == after)
        for name, digest in before.items():
            audit.check(folder.name+":prior_live:"+name, sha(ROOT/name) == digest)
    scientific_files = scalar_count = plots_excluded = 0
    for name in sorted(set(manifests[0]) & set(manifests[1])):
        a, b = main_dir/name, repeat_dir/name
        if a.suffix.lower() in (".png", ".pdf"):
            method, equal = "plot_bytes_excluded", True
            plots_excluded += 1
        elif a.suffix == ".json":
            left, right = scientific(read_json(a)), scientific(read_json(b))
            method, equal = "json_scientific_exact", left == right
            scalar_count += number_count(left)
            scientific_files += 1
        else:
            method, equal = "bytes_exact", a.read_bytes() == b.read_bytes()
            scientific_files += 1
            if a.suffix == ".csv":
                for row in read_csv(a):
                    for value in row.values():
                        try:
                            float(value)
                            scalar_count += 1
                        except (TypeError, ValueError):
                            pass
        audit.check("main_refit:"+name, equal)
        comparison_rows.append({"path": name, "method": method, "equal": equal,
                                "main_sha256": sha(a), "refit_sha256": sha(b)})
    source = ROOT/"measured-coupling-2026-10-15/rna_sources"
    observations = read_csv(source/"observations.csv")
    for index, row in enumerate(observations):
        row["row_id"] = f"observation_{index:03d}"
    train = [r for r in observations if r["dataset"] == "Figure_2" and float(r["seed_uM"]) in (0,1) and float(r["x"]) > 0]
    held = [r for r in observations if float(r["x"]) > 0 and (r["dataset"] == "Figure_3" or (r["dataset"] == "Figure_2" and float(r["seed_uM"]) == 2))]
    train_ids, held_ids = [r["row_id"] for r in train], [r["row_id"] for r in held]
    split = read_json(main_dir/"splits.json")
    audit.check("split18_72", len(train)==18 and len(held)==72 and not set(train_ids)&set(held_ids))
    audit.check("split_training", split["training_row_ids"] == train_ids)
    audit.check("split_heldout", split["evaluation_row_ids"] == held_ids)
    audit.check("split_excluded", split["excluded_row_ids"] == [r["row_id"] for r in observations if r not in train+held])
    workbook = openpyxl.load_workbook(source/"raw/salibi_data.xlsx", read_only=True, data_only=True)
    for row in train+held:
        audit.close("workbook:"+row["row_id"], row["value_percent"], workbook[row["source_sheet"]][row["source_cell"]].value)
    workbook.close()
    spec = importlib.util.spec_from_file_location("seed_campaign_model", LAB/"model.py")
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)
    prediction_cache = {}

    def calibration(family, params):
        key = family, tuple(sorted(params.items()))
        if key not in prediction_cache:
            prediction_cache[key] = {(seed, cycles): model.single_cycle(seed, family, params, cycles)["yield_percent"]
                                     for seed in (0,1) for cycles in (1,2,3)}
        return prediction_cache[key]

    def objective(family, params):
        predictions = calibration(family, params)
        return math.fsum((predictions[float(r["seed_uM"]),int(float(r["x"]))]-float(r["value_percent"]))**2 for r in train)

    fits = read_json(main_dir/"fits.json")
    profiles = read_json(main_dir/"profiles.json")
    audit.check("three_main_fits", set(fits)==set(PARAMETERS))
    audit.check("27_profile_points", len(profiles)==27)
    fit_paths = sorted((main_dir/"fits").glob("*.json"))
    audit.check("30_fit_records", len(fit_paths)==30)
    total_starts = direct = successful = qualified = 0
    objective_rows = []
    for path in fit_paths:
        fit = read_json(path)
        name = path.stem
        family = fit["family"]
        fixed = fit["fixed_parameters"]
        free = [p for p in PARAMETERS[family] if p not in fixed]
        audit.check(name+":training_only", fit["training_row_ids"]==train_ids and not set(fit["training_row_ids"])&set(held_ids))
        audit.check(name+":free_names", fit["free_parameters"]==free)
        audit.check(name+":budget", fit["max_nfev"]==120)
        audit.check(name+":complete", fit["complete"])
        audit.check(name+":resolved", fit["resolved"])
        audit.check(name+":starts_retained", len(fit["starts"])==(6 if free else 0))
        total_starts += len(fit["starts"])
        direct += not free
        successful += sum(s["success"] for s in fit["starts"])
        qualified += fit.get("qualified", False)
        for start in fit["starts"]:
            start_id = start["start_id"]
            expected_start = [BOUNDS[p][0]+(BOUNDS[p][1]-BOUNDS[p][0])*(DIFFUSION_FRACTIONS if p=="diffusion" else FRACTIONS)[start_id-1] for p in free]
            audit.close(name+f":start{start_id}:initial", max(abs(a-b) for a,b in zip(start["optimizer_start"],expected_start)), 0, 1e-12)
            audit.check(name+f":start{start_id}:budget", start["nfev"] is None or start["nfev"]<=120)
            if start.get("optimizer_parameters") is not None:
                params = dict(fixed)
                for parameter, value in zip(free,start["optimizer_parameters"]):
                    audit.check(name+f":start{start_id}:bounds:{parameter}", BOUNDS[parameter][0]-1e-12<=value<=BOUNDS[parameter][1]+1e-12)
                    params[parameter] = value if parameter=="mixing" else 10**value
                actual_sse = objective(family,params)
                audit.close(name+f":start{start_id}:objective", start["sse"], actual_sse, 1e-8)
                objective_rows.append({"fit":name,"start":start_id,"stored_sse":start["sse"],"replayed_sse":actual_sse})
        actual_sse = objective(family,fit["parameters"])
        audit.close(name+":selected_objective", fit["sse"], actual_sse, 1e-8)
        audit.close(name+":RMSE", fit["rmse_pp"], math.sqrt(actual_sse/18), 1e-9)
        if free:
            successes = [s for s in fit["starts"] if s["success"]]
            best = min(s["sse"] for s in successes)
            agreements = sum(abs(s["sse"]-best)<=max(1e-4,1e-4*best) for s in successes)
            audit.close(name+":best_successful_objective", fit["sse"], best, 1e-12)
            audit.check(name+":successful_count", fit["successful_starts"]==len(successes))
            audit.check(name+":agreement_count", fit["agreeing_successful_starts"]==agreements)
            audit.check(name+":qualification", fit["qualified"]==(agreements>=2))
        else:
            audit.check(name+":direct_objective", fit["direct_objective"] and fit["residual_evaluations"]==1 and fit["qualified"])
    audit.check("126_starts", total_starts==126)
    audit.check("nine_direct_objectives", direct==9)
    for family in PARAMETERS:
        audit.check("main_fit_duplicate:"+family, fits[family]==read_json(main_dir/"fits"/f"{family}.json"))
    for family, parameter in (("bath","nu"),("patch","nu"),("patch","diffusion")):
        entries = [r for r in profiles if r["family"]==family and r["parameter"]==parameter]
        audit.check(f"profile_grid:{family}:{parameter}", len(entries)==9)
        for index,(row,value) in enumerate(zip(entries,np.logspace(*BOUNDS[parameter],9))):
            audit.close(f"profile_value:{family}:{parameter}:{index}", row["fixed_value"], value, 1e-12)
            audit.check(f"profile_fixed:{family}:{parameter}:{index}", row["fit"]["fixed_parameters"]=={parameter:row["fixed_value"]})
            audit.check(f"profile_duplicate:{family}:{parameter}:{index}", row["fit"]==read_json(main_dir/"fits"/f"profile__{family}__{parameter}__{index}.json"))

    scenarios = read_json(main_dir/"scenarios.json")
    predictions = read_csv(main_dir/"predictions.csv")
    refined = read_csv(main_dir/"refined_predictions.csv")
    trajectories = read_csv(main_dir/"trajectories.csv")
    stages = read_csv(main_dir/"stages.csv")
    refined_trajectories = read_csv(main_dir/"refined_trajectories.csv")
    refined_stages = read_csv(main_dir/"refined_stages.csv")
    contrasts = read_csv(main_dir/"seed_contrasts.csv")
    expected_scenarios = {"legacy"}|{f"{family}|reactive-{r}|carried-{c}" for family in ("bath","patch") for r in (0,1) for c in (0,1)}
    audit.check("nine_scenarios", set(scenarios)==expected_scenarios)
    audit.check("810_predictions", len(predictions)==810 and len(refined)==810)
    audit.check("216_trajectories", len(trajectories)==216 and len(refined_trajectories)==216)
    audit.check("840_stages", len(stages)==840 and len(refined_stages)==840)
    audit.check("144_contrasts", len(contrasts)==144)
    used = {r["row_id"]:r for r in train+held}
    replay_rows = []
    for name, detail in scenarios.items():
        family, params = detail["family"], detail["parameters"]
        audit.check(name+":fit_reuse", params==fits[family]["parameters"])
        audit.check(name+":fit_qualification", detail["fit_qualified"]==fits[family]["qualified"])
        for records,fine in ((predictions,False),(refined,True)):
            subset = [r for r in records if r["scenario"]==name]
            audit.check(name+f":rows_refined{fine}", [r["row_id"] for r in subset]==train_ids+held_ids)
            options = {"exterior_reactive":detail["exterior_reactive"],"exterior_carried":detail["exterior_carried"],"rtol":1e-10 if fine else 1e-8}
            values = {}
            for seed in (0,1,2):
                replay_trajectory,replay_stages = model.serial(seed,family,params,return_stages=True,**options)
                for kind,replayed,saved in (("trajectory",replay_trajectory,refined_trajectories if fine else trajectories),
                                           ("stages",replay_stages,refined_stages if fine else stages)):
                    selected = [r for r in saved if r["scenario"]==name and float(r["seed_uM"])==seed]
                    audit.check(name+f":{kind}:seed{seed}:fine{fine}:count", len(selected)==len(replayed))
                    for index,(stored, fresh) in enumerate(zip(selected,replayed)):
                        for key, value in fresh.items():
                            label = name+f":{kind}:seed{seed}:fine{fine}:{index}:{key}"
                            if isinstance(value,str):
                                audit.check(label,stored[key]==value)
                            else:
                                audit.close(label,stored[key],value,1e-12)
                for generation,row in enumerate(replay_trajectory):
                    values["Figure_3",seed,generation] = row["yield_percent"]
                for cycles in (1,2,3):
                    values["Figure_2",seed,cycles] = model.single_cycle(seed,family,params,cycles,**options)["yield_percent"]
            for row in subset:
                reference = used[row["row_id"]]
                for key, value in reference.items():
                    if key in ("seed_uM","hyper_a_uM","x","value_percent"):
                        audit.close(name+":source:"+row["row_id"]+":"+key,row[key],value,0)
                    else:
                        audit.check(name+":source:"+row["row_id"]+":"+key,row[key]==value)
                expected = values[row["dataset"],float(row["seed_uM"]),int(float(row["x"]))]
                audit.close(name+f":prediction:{row['row_id']}:fine{fine}",row["predicted_percent"],expected,1e-12)
                audit.close(name+f":residual:{row['row_id']}:fine{fine}",row["error_pp"],expected-float(reference["value_percent"]),1e-12)
                audit.check(name+f":partition:{row['row_id']}:fine{fine}",row["stage"]==("calibration" if row["row_id"] in train_ids else "held_out"))
                replay_rows.append({"scenario":name,"row_id":row["row_id"],"refined":fine,"stored":float(row["predicted_percent"]),"replayed":expected})
        normal = [r for r in predictions if r["scenario"]==name]
        fine = [r for r in refined if r["scenario"]==name]
        delta = max(abs(float(a["predicted_percent"])-float(b["predicted_percent"])) for a,b in zip(normal,fine))
        balance = max(float(r["moiety_balance_max_error_uM"]) for r in stages+refined_stages if r["scenario"]==name)
        numeric = delta<=1e-4 and balance<=1e-6
        eligible = fits[family]["qualified"] and numeric
        audit.close(name+":refinement_delta",detail["refinement"]["max_prediction_difference_pp"],delta)
        audit.close(name+":refinement_balance",detail["refinement"]["max_moiety_error_uM"],balance)
        audit.check(name+":refinement_pass",detail["refinement"]["pass"]==numeric)
        audit.check(name+":numerical_eligible",detail["numerical_eligible"]==eligible)
        subsets = {"calibration":[r for r in normal if r["stage"]=="calibration"],
                   "held_out":[r for r in normal if r["stage"]=="held_out"],
                   "held_out_seed2":[r for r in normal if r["stage"]=="held_out" and r["dataset"]=="Figure_2"],
                   "held_out_serial":[r for r in normal if r["dataset"]=="Figure_3"]}
        for subset, rows in subsets.items():
            for key, value in metrics(rows,eligible).items():
                if isinstance(value,bool):
                    audit.check(name+":"+subset+":"+key,detail[subset][key]==value)
                else:
                    audit.close(name+":"+subset+":"+key,detail[subset][key],value)
    audit_stages(stages,scenarios,audit,"ordinary")
    audit_stages(refined_stages,scenarios,audit,"refined")
    trajectory_index = {(r["scenario"],int(r["generation"]),int(r["seed_uM"])):r for r in trajectories}
    for row in contrasts:
        seed = int(row["contrast"].split("-")[0])
        base = trajectory_index[row["scenario"],int(row["generation"]),0]
        seeded = trajectory_index[row["scenario"],int(row["generation"]),seed]
        for key,value in row.items():
            if key not in ("scenario","generation","contrast"):
                audit.close("contrast:"+row["scenario"]+":"+row["generation"]+":"+row["contrast"]+":"+key,value,float(seeded[key])-float(base[key]),1e-12)
    summary = read_json(main_dir/"summary.json")
    audit.check("summary_scenarios",summary["scenarios"]==scenarios)
    audit.check("summary_fits",summary["fits"]==fits)
    audit.check("summary_profiles_resolved",summary["all_profiles_resolved"]==all(p["fit"]["resolved"] for p in profiles))
    audit.check("summary_profiles_qualified",summary["all_profiles_qualified"]==all(p["fit"]["qualified"] for p in profiles))
    independent = read_json(HERE/"results-v2/verification.json")
    audit.check("independent_transport_receipt",independent["status"]=="PASS" and independent["failed_checks"]==[] and independent["failed_serial_comparisons"]==0)
    audit.check("independent_model_hash",read_json(HERE/"results-v2/source_hashes.json")[str((LAB/"model.py").relative_to(ROOT))]==sha(LAB/"model.py"))
    failures = [r for r in audit.rows if not r["pass"]]
    result = {"status":"PASS" if not failures else "FAIL", "check_count":len(audit.rows),"failed_checks":failures,
              "main_fits":3,"profile_nuisance_fits":18,"direct_objectives":direct,
              "optimization_starts":total_starts,"successful_starts":successful,"qualified_fit_records":qualified,
              "source_workbook_cells":len(train+held),"training_rows":len(train),"heldout_rows":len(held),
              "scenarios":len(scenarios),"predictions":len(predictions),"refined_predictions":len(refined),
              "trajectory_rows":len(trajectories),"stage_rows":len(stages),"seed_contrasts":len(contrasts),
              "scientific_files_exactly_matched":scientific_files,"numeric_fields_in_exact_comparison":scalar_count,
              "plot_files_byte_comparison_excluded":plots_excluded,"prior_files_unchanged":len(read_json(main_dir/"prior_integrity_before.json")),
              "frozen_files_per_run":len(read_json(main_dir/"freeze.json")["files"]),
              "max_arithmetic_or_replay_discrepancy":audit.max_arithmetic_error,
              "all_nine_adequacy_failures_preserved":all(not d["held_out"]["adequate"] for d in scenarios.values()),
              "patch_diffusion_upper_boundary_retained":fits["patch"]["parameters"]["diffusion"],
              "scientific_limit":"Numerical and preservation audit only; physical transport and functional inheritance remain unvalidated."}
    save(args.output/"verification.json",result)
    save(args.output/"checks.json",audit.rows)
    save(args.output/"file_comparison.json",comparison_rows)
    save(args.output/"start_objective_replay.json",objective_rows)
    save(args.output/"prediction_replay.json",replay_rows)
    shutil.copyfile(__file__,args.output/"campaign_verify.py")
    save(args.output/"audit_source_hashes.json",{"campaign_verify.py":sha(Path(__file__)),"main_manifest.json":sha(main_dir/"manifest.json"),"refit_manifest.json":sha(repeat_dir/"manifest.json")})
    print(json.dumps(result,indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
