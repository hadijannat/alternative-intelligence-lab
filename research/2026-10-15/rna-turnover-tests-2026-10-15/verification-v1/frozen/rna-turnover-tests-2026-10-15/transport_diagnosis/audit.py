"""Read-only source/replay audit; no fitting or benchmark-based model selection."""
import csv
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import importlib.util
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys

import numpy as np
import openpyxl

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
PRIOR = WORKSPACE / "rna-reaction-tests-2026-10-15"
SOURCE = WORKSPACE / "measured-coupling-2026-10-15/rna_sources"
INPUTS = [PRIOR / name for name in (
    "model.py", "run.py", "results-v1/transport.json",
    "results-v1/transport_predictions.csv", "results-v1/transport_trajectories.json",
    "results-v1/transport_refinement.json", "results-v1/full_fits.json")]
INPUTS += [SOURCE / name for name in (
    "observations.csv", "conditions.json", "raw/salibi_data.xlsx",
    "raw/salibi.txt", "raw/salibi_si.txt", "raw/salibi_si.pdf")]
INPUTS += [WORKSPACE / "rna-mechanism-2026-10-15/sources/salibi/conditions.json"]


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def hashes():
    return {str(p.relative_to(WORKSPACE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS}


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def stats(rows):
    errors = np.array([r["error_pp"] for r in rows])
    return dict(n=len(rows), bias_pp=float(errors.mean()),
                rmse_pp=float(np.sqrt(np.mean(errors**2))),
                max_absolute_error_pp=float(np.max(np.abs(errors))))


def main():
    expected = {"python": "3.12.3", "numpy": "2.4.1", "scipy": "1.16.1",
                "matplotlib": "3.10.8", "openpyxl": "3.1.3"}
    runtime = {k: platform.python_version() if k == "python" else version(k) for k in expected}
    assert runtime == expected, runtime
    before = hashes()
    receipt = HERE / "input_hashes.json"
    if receipt.exists():
        assert json.loads(receipt.read_text()) == before, "An audited input changed"
    else:
        save("input_hashes.json", before)
    spec = importlib.util.spec_from_file_location("audited_transport_model", PRIOR / "model.py")
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)
    with (SOURCE / "observations.csv").open() as stream:
        source = [r for r in csv.DictReader(stream) if r["dataset"] in ("Figure_2", "Figure_3")]
    wb = openpyxl.load_workbook(SOURCE / "raw/salibi_data.xlsx", data_only=True)
    for row in source:
        cell = wb[row["source_sheet"]][row["source_cell"]]
        assert float(cell.value) == float(row["value_percent"])
        assert float(wb[row["source_sheet"]].cell(cell.row, 2).value) == float(row["x"])
        assert (cell.column - 3) // 3 == int(float(row["seed_uM"]))
        assert (cell.column - 3) % 3 + 1 == int(row["replicate"])
    assert len(source) == 108
    with (PRIOR / "results-v1/transport_predictions.csv").open() as stream:
        predictions = list(csv.DictReader(stream))
    for row in predictions:
        for field in ("seed_uM", "x", "value_percent", "predicted_percent", "error_pp"):
            row[field] = float(row[field])
        assert abs(row["predicted_percent"] - row["value_percent"] - row["error_pp"]) < 1e-12
        matching = [s for s in source if (s["source_sheet"], s["source_cell"]) ==
                    (row["source_sheet"], row["source_cell"])]
        assert len(matching) == 1 and float(matching[0]["value_percent"]) == row["value_percent"]
    parameters = json.loads((PRIOR / "results-v1/transport.json").read_text())
    full = json.loads((PRIOR / "results-v1/full_fits.json").read_text())["independent_inactivation"]["parameters"]
    saved = json.loads((PRIOR / "results-v1/transport_trajectories.json").read_text())
    replay_error, trajectory_error, balance_error = 0., 0., 0.
    loss_counterexamples, differential_retention = [], []
    inheritance = []
    for transport, record in parameters.items():
        p = model.Parameters(**record["parameters"])
        for name, value in full.items():
            if name not in ("transport", "mixing"):
                assert record["parameters"][name] == value
        training = [r for r in predictions if r["transport"] == transport and r["x"] > 0
                    and r["stage"] == "transport_calibration"]
        benchmark = [r for r in predictions if r["transport"] == transport and r["x"] > 0
                     and r["stage"] == "historical_benchmark"]
        assert len(training) == 18 and len(benchmark) == 72
        assert {r["row_id"] for r in training} == set(record["mixing_fit"]["training_row_ids"])
        assert not {r["row_id"] for r in training} & {r["row_id"] for r in benchmark}
        assert all(r["dataset"] == "Figure_2" and r["seed_uM"] in (0, 1) for r in training)
        assert abs(stats(benchmark)["rmse_pp"] - record["benchmark"]["rmse_pp"]) < 1e-12
        trajectories = {s: model.serial(p, s) for s in (0, 1, 2)}
        cycles = {(s, n): model.single_cycle(p, s, n) for s in (0, 1, 2) for n in range(4)}
        for row in (r for r in predictions if r["transport"] == transport):
            s, n = int(row["seed_uM"]), int(row["x"])
            value = trajectories[s][n]["yield_percent"] if row["dataset"] == "Figure_3" else cycles[s, n]
            replay_error = max(replay_error, abs(value - row["predicted_percent"]))
        for s, trajectory in trajectories.items():
            assert abs(trajectory[1]["yield_percent"] - cycles[s, 3]) < 1e-9
            assert len(trajectory) == 8
            no_regeneration = model.serial(p, s, regeneration=False)
            for g, row in enumerate(trajectory):
                old = saved[transport][str(s)][g]
                for field, value in row.items():
                    trajectory_error = max(trajectory_error, float(np.max(np.abs(np.asarray(value) - np.asarray(old[field])))))
                balance_error = max(balance_error, row["moiety_balance_max_error_uM"])
                f = s / 3 if g == 0 else s/3 * .55**g * .5**(g-1) * np.exp(-60*p.kd*g)
                assert abs(no_regeneration[g]["F1_uM"] - f) < 1e-8
                assert abs(row["founder_F1_model_uM"] - f) < 1e-12
                assert row["cohorts"] == (3+2*max(0, g-1) if transport == "fractional" else 3+2*max(0, g-1)+3*g)
            end = trajectory[-1]
            inheritance.append(dict(transport=transport, seed_uM=s,
                observed_g7_percent=float(np.mean([r["value_percent"] for r in predictions if
                    r["transport"] == transport and r["dataset"] == "Figure_3" and r["seed_uM"] == s and r["x"] == 7])),
                predicted_g7_percent=end["yield_percent"], active_F1_g7_uM=end["F1_uM"],
                founder_F1_g7_uM=end["founder_F1_model_uM"],
                no_regeneration_g7_percent=no_regeneration[-1]["yield_percent"],
                cohorts_g7=end["cohorts"]))
        x, w = model.initial(2, p)
        np.testing.assert_allclose(w, np.ones(3)/3)
        np.testing.assert_allclose(w@x, [10/3, 2.5/3, 5, 2/3, 0, 0, 0, 0])
        np.testing.assert_allclose(.25*model.fresh(p).sum(axis=0), [2.5, .625, 3.75, 0, 0, 0, 0, 0])
        after, weights, lost = model.exchange(x, w, p, 3)
        np.testing.assert_allclose(weights@after, .55*(w@x), atol=1e-12)
        np.testing.assert_allclose(weights@after+lost, w@x, atol=1e-12)
        # Equal population RNA inventories need not imply equal local concentrations.
        homogeneous = np.array([[10/3, 2.5/3, 5, 2/3, 0, 0, 0, 0]])
        thinned = .55*homogeneous
        localized = np.vstack([homogeneous, np.zeros((1, 8))])
        np.testing.assert_allclose(thinned[0], np.array([.55, .45])@localized)
        y_thin = model.reporter(model.react(thinned, 60, p), [1])
        y_local = model.reporter(model.react(localized, 60, p), [.55, .45])
        assert abs(y_thin-y_local) > .1
        loss_counterexamples.append(dict(transport=transport,
            definition="Synthetic equal-inventory maps, not fitted to either figure",
            concentration_thinning_percent=y_thin, fraction_content_loss_percent=y_local,
            difference_pp=y_local-y_thin))
        synthetic = np.ones((1, 8))
        differential, weights, _ = model.exchange(synthetic, [1], replace(p, retention_f=.8), 3)
        expected_retention = [.55, .55, .55, .8, .55, .8, .55, .55]
        np.testing.assert_allclose(weights@differential, expected_retention, atol=1e-12)
        differential_retention.append(dict(transport=transport,
            test_parameters={"retention_f": .8, "retention_fragments": .55},
            observed_species_retention=dict(zip(model.NAMES, expected_retention)),
            baseline_affected=False))
    assert replay_error < 1e-7 and trajectory_error < 1e-7 and balance_error < 1e-7
    grouped = []
    for transport, dataset, seed, x in sorted({(r["transport"], r["dataset"], r["seed_uM"], r["x"]) for r in predictions}):
        rows = [r for r in predictions if (r["transport"], r["dataset"], r["seed_uM"], r["x"]) ==
                (transport, dataset, seed, x)]
        obs = np.array([r["value_percent"] for r in rows])
        assert len(rows) == 3 and len({r["predicted_percent"] for r in rows}) == 1
        grouped.append(dict(transport=transport, dataset=dataset, seed_uM=seed, x=x,
            stage=rows[0]["stage"], observed_mean_percent=float(obs.mean()), observed_sd_percent=float(obs.std(ddof=1)),
            predicted_percent=rows[0]["predicted_percent"], error_mean_pp=float(rows[0]["predicted_percent"]-obs.mean()),
            **stats(rows)))
    summaries = []
    for transport, dataset, seed in sorted({(r["transport"], r["dataset"], r["seed_uM"]) for r in predictions}):
        rows = [r for r in predictions if (r["transport"], r["dataset"], r["seed_uM"]) == (transport, dataset, seed) and r["x"] > 0]
        summaries.append(dict(transport=transport, dataset=dataset, seed_uM=seed, **stats(rows)))
    replicate_differences = []
    for seed in (0, 1, 2):
        a = next(r for r in grouped if (r["transport"], r["dataset"], r["seed_uM"], r["x"]) == ("fractional", "Figure_2", seed, 3))
        b = next(r for r in grouped if (r["transport"], r["dataset"], r["seed_uM"], r["x"]) == ("fractional", "Figure_3", seed, 1))
        replicate_differences.append(dict(seed_uM=seed, figure2_ft3_mean=a["observed_mean_percent"],
            figure3_g1_mean=b["observed_mean_percent"], difference_pp=b["observed_mean_percent"]-a["observed_mean_percent"],
            combined_sd_percent=float(np.hypot(a["observed_sd_percent"], b["observed_sd_percent"]))))
    kd = parameters["fractional"]["parameters"]["kd"]
    clock = dict(FT_freeze_minutes=5, FT_thaw_minutes=5, FT_per_generation=3,
        elapsed_minutes_per_generation=90, model_42C_reaction_minutes_per_generation=60,
        active_fraction_after_60min=float(np.exp(-60*kd)), active_half_life_model_minutes=float(np.log(2)/kd),
        founder_active_ratio_per_post_g1_generation=float(.5*.55*np.exp(-60*kd)),
        unjustified_same_kd_extra_30min_multiplier=float(np.exp(-30*kd)),
        per_FT_retention_model=float(.55**(1/3)),
        incorrect_55percent_each_FT_three_cycle_retention=float(.55**3))
    save("diagnosis.json", dict(classification="Retrospective fixed-parameter audit; no fitting", runtime=runtime,
        source_observations_checked=108, predictions_checked=len(predictions),
        maximum_prediction_replay_difference_pp=replay_error,
        maximum_trajectory_replay_difference=trajectory_error, maximum_moiety_error_uM=balance_error,
        dynamic_residuals_by_seed=summaries, g7_state=inheritance,
        nominally_identical_protocol_experiment_differences=replicate_differences,
        clock_and_retention=clock, equal_inventory_loss_counterexample=loss_counterexamples,
        differential_retention_code_test=differential_retention,
        supplied_A_moiety_no_reaction_steady_uM=float(.55*3.125/(1-.55*.5)),
        fresh_reporter_feed_uM=.625, g1_total_reporter_uM=.55*2.5/3,
        steady_total_reporter_uM=float(.55*.625/(1-.55*.5)),
        baseline_implementation_error_found=False,
        latent_differential_retention_issue="Cy5F1 classified as fragment while unlabelled F1 classified as full length; equal-retention saved baseline unaffected",
        unmeasured_closures=["per-species retention", "loss location versus concentration dilution", "vesicle volume weighting", "all-or-nothing versus fractional exchange", "membrane effects on chemical rates", "active versus reporter product equivalence", "bound-complex survival and activity", "temperature-dependent chemical and inactivation rates during FT"],
        inputs_unchanged=hashes()==before))
    write_csv("residuals_by_condition.csv", grouped)
    write_csv("dynamic_residuals_by_seed.csv", summaries)
    write_csv("g7_state.csv", inheritance)
    assert hashes() == before, "An audited input changed"
    save("verification.json", dict(utc=datetime.now(timezone.utc).isoformat(), pass_all_assertions=True,
        runtime=runtime, input_count=len(before), inputs_unchanged=True,
        output_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir())
                       if p.is_file() and p.name != "verification.json"}))
    print(json.dumps(dict(pass_all_assertions=True, observations=108, predictions=len(predictions),
                         replay_max_pp=replay_error, preserved_inputs=len(before)), indent=2))


if __name__ == "__main__":
    main()
