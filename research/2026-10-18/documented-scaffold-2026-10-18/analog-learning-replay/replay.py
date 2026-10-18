"""Retrospective native free-state replay under REPLAY_PROTOCOL.md."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import tempfile
import warnings
import zipfile

import numpy as np

from inventory import checked_members

ROOT = Path(__file__).resolve().parent
ARCHIVE_SHA256 = "f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c"
TOL = 1e-12


def logical(values, differential):
    if differential and values.shape[0] % 2:
        raise ValueError("Differential targets must form consecutive pairs")
    return values[1::2] - values[::2] if differential else values


def errors(prediction, target):
    per_output = np.mean((prediction - target) ** 2, axis=1)
    return dict(mse_volts2=float(np.mean(per_output)), per_output_mse_volts2=per_output.tolist())


def overlap(train, test, train_targets, test_targets, differential):
    """Audit full native source boundaries; retain every duplicate/matching index."""
    def audit(tolerance):
        def same(a, b):
            return bool(np.all(a == b) if tolerance == 0 else np.max(np.abs(a - b)) <= tolerance)

        def pair(i, j, left, right):
            return dict(left=i, right=j, native_target_conflict=not same(left[:, i], right[:, j]),
                        logical_target_conflict=not same(logical(left, differential)[:, i],
                                                        logical(right, differential)[:, j]))

        result = dict(test_to_train=[dict(test=j, matches=[
            pair(i, j, train_targets, test_targets) for i in range(train.shape[1])
            if same(train[:, i], test[:, j])]) for j in range(test.shape[1])],
            train_duplicates=[pair(i, j, train_targets, train_targets)
                for i in range(train.shape[1]) for j in range(i + 1, train.shape[1])
                if same(train[:, i], train[:, j])],
            test_duplicates=[pair(i, j, test_targets, test_targets)
                for i in range(test.shape[1]) for j in range(i + 1, test.shape[1])
                if same(test[:, i], test[:, j])])
        result["test_inputs_with_training_match"] = sum(bool(row["matches"]) for row in result["test_to_train"])
        result["test_inputs_without_training_match"] = test.shape[1] - result["test_inputs_with_training_match"]
        return result

    return dict(exact=audit(0), max_coordinate_tolerance_1e_12=audit(TOL))


def baselines(train_inputs, test_inputs, train_labels, test_labels):
    constant = np.repeat(np.mean(train_labels, axis=1, keepdims=True), test_inputs.shape[1], axis=1)
    features = np.flatnonzero(np.ptp(train_inputs, axis=1) > 1e-10)
    design = np.column_stack((np.ones(train_inputs.shape[1]), train_inputs[features].T))
    weights, _, rank, _ = np.linalg.lstsq(design, train_labels.T, rcond=None)
    evaluation = np.column_stack((np.ones(test_inputs.shape[1]), test_inputs[features].T))
    affine = (evaluation @ weights).T
    return dict(training_mean=dict(fitted_mean_volts=constant[:, 0].tolist(), **errors(constant, test_labels)),
                affine=dict(**errors(affine, test_labels),
                            source_coordinate_indices=features.tolist(), rank=int(rank),
                            feature_count=int(design.shape[1]), weights=weights.tolist(), rcond=None))


def analyze(properties):
    """Pure array analysis; no decoding, file access, or training on TEST labels."""
    p = properties
    counts = {}
    for key in ("MES", "TRA", "TST", "SOR", "TAR", "DEL"):
        value = np.asarray(p[key]).item()
        if not np.isfinite(value) or value != int(value) or value < (0 if key == "DEL" else 1):
            raise ValueError("Invalid count metadata: " + key)
        counts[key] = int(value)
    if counts["DEL"] not in (0, 1):
        raise ValueError("DEL must be zero or one")
    m, a, t, s, o, differential = (counts[k] for k in ("MES", "TRA", "TST", "SOR", "TAR", "DEL"))
    shape = dict(TRAIN=(s + o, a), TEST=(s + o, t), TLOC=(o, 2), SLOC=(s, 2),
                 TestFreeState=(4, 4, m, t), TestMeasurements=(o, t, m),
                 TestMSE=(1, m), LearnTimes=(1, m), DOTEST=(1, m),
                 HorizontalCapacitors=(4, 4, m), VerticalCapacitors=(4, 4, m))
    for key, expected in shape.items():
        if np.asarray(p[key]).shape != expected:
            raise ValueError("Unexpected shape for " + key)
    for key in ("TRAIN", "TEST", "SLOC", "TLOC"):
        if not np.all(np.isfinite(p[key])):
            raise ValueError("Nonfinite task/control array: " + key)
    for key in ("SLOC", "TLOC"):
        if not np.all((p[key] >= 0) & (p[key] < 4) & (p[key] == np.floor(p[key]))):
            raise ValueError("Invalid zero-based grid location: " + key)
    test_steps = np.asarray(p["DOTEST"], dtype=float).reshape(m)
    if (not np.all(np.isfinite(test_steps)) or not np.all(test_steps > 0)
            or not np.all(test_steps == np.floor(test_steps)) or not np.all(np.diff(test_steps) > 0)):
        raise ValueError("DOTEST must be finite positive integral strictly increasing test-step indices")
    scale, gate_scale = (float(np.asarray(p[k]).item()) for k in ("NODEMULT", "GATEMULT"))
    if not all(np.isfinite(v) and v > 0 for v in (scale, gate_scale)):
        raise ValueError("Invalid voltage scale")
    free = np.asarray(p["TestFreeState"], dtype=float)
    target_locs, source_locs = (np.asarray(p[k], dtype=int) for k in ("TLOC", "SLOC"))
    targets = free[target_locs[:, 0], target_locs[:, 1]].transpose(0, 2, 1)
    sources = free[source_locs[:, 0], source_locs[:, 1]].transpose(0, 2, 1)
    train, test = np.asarray(p["TRAIN"]), np.asarray(p["TEST"])
    labels = logical(test[s:], differential) * scale
    train_labels = logical(train[s:], differential) * scale
    intervals = np.asarray(p["LearnTimes"], dtype=float).reshape(m)
    time = np.cumsum(intervals) / 1e6
    time_ok = bool(np.all(np.isfinite(intervals)) and np.all(intervals >= 0)
                   and np.all(np.isfinite(time)) and np.all(np.diff(time) >= 0))
    rows, complete, mismatches = [], [], []
    for i in range(m):
        reasons = []
        mapping_difference = None
        if not np.all(np.isfinite(free[:, :, i, :])):
            reasons.append("nonfinite_free_state")
        if np.all(free[:, :, i, :] == 0) and np.any(test[:s] != 0):
            reasons.append("entire_zero_initialized_placeholder_with_nonzero_sources")
        if not reasons:
            complete.append(i)
            stored = np.asarray(p["TestMeasurements"])[:, :, i]
            mapping_difference = float(np.max(np.abs(targets[:, :, i] - stored)))
            if not np.allclose(targets[:, :, i], stored, atol=TOL, rtol=TOL):
                mismatches.append(i)
        rows.append(dict(index=i, scheduled_training_step=int(test_steps[i]),
                         learning_interval_microseconds=float(intervals[i]),
                         learning_seconds=float(time[i]), complete=not reasons, validity_reasons=reasons,
                         mapping_max_abs_normalized=mapping_difference,
                         stored_TestMSE_normalized=float(p["TestMSE"][0, i]),
                         stored_TestMSE_volts2=float(p["TestMSE"][0, i] * scale ** 2)))
    result = dict(count_metadata=counts, node_scale_volts=scale, gate_scale_volts=gate_scale,
                  snapshots=rows, structurally_complete_indices=complete,
                  native_first_snapshot_complete=0 in complete,
                  native_final_snapshot_complete=(m - 1) in complete,
                  time_valid=time_ok, mapping_mismatch_indices=mismatches,
                  mapping_atol_normalized=TOL, mapping_rtol=TOL,
                  status="failed_time" if not time_ok else "failed_mapping" if mismatches else
                         "failed_no_complete_snapshot" if not complete else "replayed")
    if result["status"] != "replayed":
        return result
    result["task_overlap"] = overlap(train[:s], test[:s], train[s:], test[s:], differential)
    result["baselines"] = baselines(train[:s] * scale, test[:s] * scale, train_labels, labels)
    first, last = complete[0], complete[-1]
    for i in complete:
        prediction = logical(targets[:, :, i], differential) * scale
        source_error = (sources[:, :, i] - test[:s]) * scale
        rows[i].update(**errors(prediction, labels),
                       source_program_mismatch_rms_volts=float(np.sqrt(np.mean(source_error ** 2))),
                       source_program_mismatch_max_abs_volts=float(np.max(np.abs(source_error))))
        rows[i]["recomputed_minus_stored_mse_volts2"] = rows[i]["mse_volts2"] - rows[i]["stored_TestMSE_volts2"]
    result["baselines"]["frozen_earliest_observed"] = dict(
        observation_index=first, observation_learning_seconds=float(time[first]),
        **errors(logical(targets[:, :, first], differential) * scale, labels))
    result["endpoints"] = dict(earliest_available_measured_snapshot=first,
        final_complete_snapshot=last, earliest_learning_seconds=float(time[first]),
        final_learning_seconds=float(time[last]), first_mse_volts2=rows[first]["mse_volts2"],
        final_mse_volts2=rows[last]["mse_volts2"],
        first_minus_final_mse_volts2=rows[first]["mse_volts2"] - rows[last]["mse_volts2"])
    result["endpoint_comparisons"] = {label: {key: dict(
        baseline_minus_observed_mse_volts2=value["mse_volts2"] - rows[index]["mse_volts2"],
        observed_over_baseline_mse=None if value["mse_volts2"] == 0 else rows[index]["mse_volts2"] / value["mse_volts2"])
        for key, value in result["baselines"].items()} for label, index in (("earliest", first), ("final", last))}
    drift = (sources[:, :, last] - sources[:, :, first]) * scale
    result["source_first_to_final_drift"] = dict(rms_volts=float(np.sqrt(np.mean(drift ** 2))),
                                                max_abs_volts=float(np.max(np.abs(drift))))
    caps = np.concatenate([np.asarray(p[k], dtype=float).reshape(16, m)
                           for k in ("HorizontalCapacitors", "VerticalCapacitors")]) * gate_scale
    cap_ok = bool(np.all(np.isfinite(caps[:, [first, last]])))
    result["capacitor_first_to_final"] = dict(count=32, endpoints_finite=cap_ok,
        nonfinite_endpoint_values=int(np.count_nonzero(~np.isfinite(caps[:, [first, last]]))),
        rms_change_volts=float(np.sqrt(np.mean((caps[:, last] - caps[:, first]) ** 2))) if cap_ok else None)
    return result


def json_safe(value):
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    return None if isinstance(value, float) and not np.isfinite(value) else value


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_path(name):
    if (Path(name).name != name or "\\" in name or not name.endswith(".json")
            or len(name) <= len(".json")):
        raise ValueError("Output name must be a JSON basename within results")
    output = ROOT / "results" / name
    if output.exists():
        raise FileExistsError(output)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-name", default="replay.json", help="Fresh JSON basename within results")
    output = result_path(parser.parse_args(argv).output_name)
    runtime = json.loads((ROOT / "reader-runtime.json").read_text())
    if (importlib.metadata.version("mat-io") != "1.0.1"
            or runtime["upstream_tests"].get("passed") != 12 or runtime["upstream_tests"].get("failed") != 0):
        raise ValueError("Qualified reader/runtime tests required")
    native = ROOT / "sources/browser-native/data.zip"
    if sha256(native) != ARCHIVE_SHA256:
        raise ValueError("Native archive SHA256 mismatch")
    schema = json.loads((ROOT / "results/property-schema-all.json").read_text())["records"]
    qualified = {r["member"]: r for r in schema if r["qualified_schema"]}
    schema_by_name = {r["member"]: r for r in schema}
    if len(qualified) != 191 or len(schema_by_name) != 200 or len(schema) != 200:
        raise ValueError("Frozen all-object schema inventory mismatch")
    from matio import load_from_mat

    records = []
    with zipfile.ZipFile(native) as archive:
        members = checked_members(archive)
        names = [item.filename for item in members]
        experiments = {name for name in names if name.startswith("data/experiment") and name.endswith(".mat")}
        if len(names) != len(set(names)) or experiments != schema_by_name.keys():
            raise ValueError("Duplicate ZIP name or changed native experiment inventory")
        for item in members:
            body = archive.read(item)
            digest = hashlib.sha256(body).hexdigest()
            record = dict(member=item.filename, bytes=len(body), sha256=digest)
            records.append(record)
            if item.filename not in qualified:
                record.update(status="excluded", reason="schema_missing_properties:" + ",".join(
                    schema_by_name[item.filename].get("missing", [])) if item.filename in schema_by_name else
                    "directory" if item.is_dir() else "oscilloscope_trace_outside_task_replay" if
                    item.filename == "data/OscilloscopeData.mat" else "archive_metadata_outside_task_replay")
                continue
            if digest != qualified[item.filename]["sha256"]:
                raise ValueError("Native MAT/schema hash mismatch: " + item.filename)
            with tempfile.TemporaryDirectory() as directory, warnings.catch_warnings(record=True) as observed:
                warnings.simplefilter("always")
                try:
                    path = Path(directory) / "native.mat"
                    path.write_bytes(body)
                    obj = load_from_mat(path, variable_names=["experiment"], raw_data=True)["experiment"]
                    if obj.classname != "Experiment2":
                        raise ValueError("Unexpected named object class")
                    if observed:
                        raise ValueError("Reader warning; numerical interpretation stopped")
                    record.update(analyze(obj.properties))
                except Exception as error:
                    record.update(status="failed", error=repr(error))
                record["warnings"] = [str(w.message) for w in observed]
    groups = {}
    for record in records:
        if record["member"].startswith("data/") and record["member"].endswith(".mat"):
            groups.setdefault(record["sha256"], []).append(record["member"])
    result = dict(observed_utc=datetime.now(timezone.utc).isoformat(), archive_sha256=ARCHIVE_SHA256,
        zip_crc_ok=True, duplicate_mat_hashes={k: v for k, v in groups.items() if len(v) > 1},
        provenance_sha256={name: sha256(ROOT / name) for name in ("REPLAY_PROTOCOL.md", "REPLAY_CLARIFICATIONS.md",
            "REPLAY_SCHEDULE_AMENDMENT.md", "DECODING_PROTOCOL.md", "DECODING_AMENDMENT.md", "replay.py", "test_replay.py",
            "reader-runtime.json", "results/property-schema-all.json", "sources/browser-native/README.md",
            "sources/browser-native/PNASscriptFig3.m")},
        runtime=dict(executable=sys.executable, python=platform.python_version(),
            packages={name: importlib.metadata.version(name) for name in ("mat-io", "numpy", "scipy")}),
        records=records, retrospective_observational_replay=True, new_physical_experiment=False,
        causal_update_ablation_verified=False, independent_environment_generalization_verified=False,
        integrated_goal_verified=False)
    with output.open("x") as handle:
        json.dump(json_safe(result), handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps(dict(output=str(output), qualified=len(qualified),
        statuses={status: sum(r["status"] == status for r in records)
                  for status in sorted({r["status"] for r in records})}), indent=2))


if __name__ == "__main__":
    main()
