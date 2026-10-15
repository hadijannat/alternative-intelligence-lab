"""Acquire pinned public observations and summarize them without fitting a life model."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
COMMIT = "5e39536facd68c2a133454b6a31390d53f19ad30"
REPOSITORY = "https://github.com/hsoria/Primitive-Genotype-Phenotype-coupling"
BASE = f"https://raw.githubusercontent.com/hsoria/Primitive-Genotype-Phenotype-coupling/{COMMIT}/"
ZENODO = "https://zenodo.org/api/records/21453837"
CHEMICAL_FILES = {
    "Figure3B_Data.csv": "00_Figures Main Text/Figure3/Figure3B_Data.csv",
    "Figure3C_Lifetime.csv": "00_Figures Main Text/Figure3/Figure3C_Lifetime.csv",
    "Figure2G_Error_Rates.csv": "00_Figures Main Text/Figure2/Figure2G_Error_Rates.csv",
    "SOURCE_LICENSE.txt": "LICENSE",
}
SCHEMAS = {
    "Figure3B_Data.csv": {"Time": "minutes", "Azide_1": "categorical source label", "Azide_2": "categorical source label", "Type": "Click or Control", "value": "optical density at 650 nm, dimensionless"},
    "Figure3C_Lifetime.csv": {"Lt": "minutes", "Azide_1": "categorical source label", "Azide_2": "categorical source label", "Type": "Click or Control", "C": "condition label"},
    "Figure2G_Error_Rates.csv": {"Type": "source condition label", "Azide1": "source label", "Azide2": "source label", "variable": "ER: chemical wrong-azide consumption fraction", "value": "dimensionless fraction, not per-base copying error", "C": "condition label"},
    "fig2.zip": {"fig2a_overlay_plotted.csv": "time_s/time_rel_s: s; pulse_index: integer; pulse_label: dimensionless relative illumination level; corrected_current_A: A", "fig2c_avg_response_present1p0.csv": "time_past*_s: seconds; mean_past*_A/std_past*_A: A; n_past*: pulse count", "fig2d_avg_response_present0p5.csv": "same schema as fig2c", "fig2_parameters.txt": "author timing, preprocessing, and interpolation details"},
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def download():
    destination = ROOT / "data"
    destination.mkdir(exist_ok=True)
    manifest_path = ROOT / "datasets_manifest.json"
    if manifest_path.exists():
        raise FileExistsError("Acquisition already recorded; use retained data or a new version directory.")
    urls = [(name, BASE + urllib.parse.quote(path), "MIT", "10.1016/j.chempr.2025.102816") for name, path in CHEMICAL_FILES.items()]
    urls += [("zenodo_metadata.json", ZENODO, "CC-BY-4.0", "10.5281/zenodo.21453837"), ("fig2.zip", ZENODO + "/files/fig2.zip/content", "CC-BY-4.0", "10.5281/zenodo.21453837")]
    entries = []
    for name, url, license_name, doi in urls:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read(5_000_001)
            resolved_url = response.url
        if len(data) > 5_000_000:
            raise ValueError(f"Unexpected large file: {name}")
        if name == "fig2.zip" and hashlib.md5(data).hexdigest() != "a1c2bbb7c2a8b46fbc0c0b689f10f85e":
            raise ValueError("Zenodo file no longer matches published checksum")
        if name == "zenodo_metadata.json" and json.loads(data)["metadata"]["license"]["id"] != "cc-by-4.0":
            raise ValueError("Zenodo license changed")
        (destination / name).write_bytes(data)
        entries.append({"file": "data/" + name, "url": url, "resolved_url": resolved_url, "doi": doi, "license": license_name, "downloaded_utc": datetime.now(timezone.utc).isoformat(), "sha256": sha(data), "bytes": len(data), "columns_units": SCHEMAS.get(name, {}), "source_commit": COMMIT if name in CHEMICAL_FILES else None})
    manifest = {"schema_version": 1, "chemical_repository": REPOSITORY, "chemical_data_license_basis": "Repository root MIT license, retained verbatim; no separate data license seen", "datasets": entries, "roles": {"chemical": "Measured component-level lifetime/error/turbidity summaries; no fitting of integrated entity", "physical": "Measured, author-corrected photocurrent memory demonstration; preprint evidence; no claim of chemical compatibility"}, "limitations": ["The source chemical time-course lacks explicit replicate identifiers; series are separated only by time reset.", "Lifetime and error-rate groups are small, including n=2; descriptive values are not population estimates.", "Error rate is a chemical product selectivity measure, not a genome mutation probability.", "Photocurrent observations are one supplied device sequence with preprocessing; pulse count is not device replication.", "No numerical parameter is transferred between materials or used to calibrate the synthetic simulation."]}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def finite(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Nonfinite observation")
    return result


def summary(values):
    if not values:
        raise ValueError("Empty observations")
    return {"n": len(values), "mean": statistics.mean(values), "min": min(values), "max": max(values), "sample_sd": statistics.stdev(values) if len(values) > 1 else None}


def halfpeak_time(points):
    if not points or any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise ValueError("Strictly increasing time is required")
    peak = max(range(len(points)), key=lambda i: points[i][1])
    threshold = points[peak][1] / 2
    for (t0, y0), (t1, y1) in zip(points[peak:], points[peak + 1:]):
        if y0 >= threshold >= y1 and y1 < y0:
            return t0 + (threshold - y0) * (t1 - t0) / (y1 - y0)
    return None


def interpolate(points, time):
    if not points or any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise ValueError("Strictly increasing time is required")
    if time == points[-1][0]:
        return points[-1][1]
    for (t0, y0), (t1, y1) in zip(points, points[1:]):
        if t0 <= time <= t1:
            return y0 + (y1 - y0) * (time - t0) / (t1 - t0)
    raise ValueError("Interpolation would extrapolate")


def analyze():
    manifest = json.loads((ROOT / "datasets_manifest.json").read_text())
    for entry in manifest["datasets"]:
        data = (ROOT / entry["file"]).read_bytes()
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise ValueError(f"Integrity failure: {entry['file']}")
    def rows(name):
        with (ROOT / "data" / name).open(newline="") as stream:
            return list(csv.DictReader(stream))
    lifetime = {}
    for row in rows("Figure3C_Lifetime.csv"):
        lifetime.setdefault(row["C"], []).append(finite(row["Lt"]))
    error = {}
    for row in rows("Figure2G_Error_Rates.csv"):
        value = finite(row["value"])
        if not 0 <= value <= 1:
            raise ValueError("Error fraction outside [0,1]")
        error.setdefault(row["Type"], []).append(value)
    traces = {}
    chemical_rows = rows("Figure3B_Data.csv")
    for row in chemical_rows:
        key = (row["Azide_1"], row["Azide_2"], row["Type"])
        point = (finite(row["Time"]), finite(row["value"]))
        series = traces.setdefault(key, [[]])
        if series[-1] and point[0] <= series[-1][-1][0]:
            series.append([])
        series[-1].append(point)
    trace_results = []
    for key, series in traces.items():
        for index, points in enumerate(series):
            trace_results.append({"condition": list(key), "series_by_time_reset": index, "rows": len(points), "start_min": points[0][0], "end_min": points[-1][0], "peak_OD650": max(y for _, y in points), "absolute_time_to_half_peak_min": halfpeak_time(points), "auc_observed_OD_min": sum((b[0]-a[0])*(a[1]+b[1])/2 for a,b in zip(points, points[1:]))})
    memory = []
    with zipfile.ZipFile(ROOT / "data/fig2.zip") as archive:
        for filename in ["fig2/fig2c_avg_response_present1p0.csv", "fig2/fig2d_avg_response_present0p5.csv"]:
            records = list(csv.DictReader(io.StringIO(archive.read(filename).decode())))
            first = records[0]
            high = [(finite(row["time_past1p0_s"]), finite(row["mean_past1p0_A"])) for row in records if row["mean_past1p0_A"]]
            low = [(finite(row["time_past0p1_s"]), finite(row["mean_past0p1_A"])) for row in records if row["mean_past0p1_A"]]
            # shortcut: one descriptive 4 s contrast, use full traces for a memory-kernel model.
            terminal_time = min(4.0, high[-1][0], low[-1][0])
            initial = finite(first["mean_past1p0_A"]) - finite(first["mean_past0p1_A"])
            terminal = interpolate(high, terminal_time) - interpolate(low, terminal_time)
            counts = {}
            for label in ["0p1", "1p0"]:
                available = [(finite(row[f"time_past{label}_s"]), int(finite(row[f"n_past{label}"]))) for row in records if row[f"mean_past{label}_A"]]
                for left, right in zip(available, available[1:]):
                    if left[0] <= terminal_time <= right[0]:
                        counts[label] = min(left[1], right[1])
                        break
            memory.append({"file": filename, "rows": len(records), "past_high_minus_low_initial_A": initial, "past_high_minus_low_terminal_A": terminal, "terminal_to_initial_separation_ratio": terminal / initial, "terminal_common_time_s": terminal_time, "minimum_pulse_counts_at_comparison_brackets": counts, "initial_pulse_counts": {key: int(finite(first[key])) for key in first if key.startswith("n_")}})
        overlay = list(csv.DictReader(io.StringIO(archive.read("fig2/fig2a_overlay_plotted.csv").decode())))
        for row in overlay:
            for key in ["time_s", "time_rel_s", "pulse_index", "pulse_label", "corrected_current_A"]:
                finite(row[key])
    result = {"evidence_class": "descriptive reanalysis of downloaded measured component data", "integrated_model_calibration": False, "lifetime_min": {key: summary(value) for key,value in lifetime.items()}, "lifetime_mean_ratio_KR_Click_to_KR_Control": statistics.mean(lifetime["kArg-kArg-Click"])/statistics.mean(lifetime["kArg-kArg-Control"]), "chemical_selectivity_error_fraction": {key: summary(value) for key,value in error.items()}, "turbidity_traces": trace_results, "turbidity_rows_total": len(chemical_rows), "physical_memory": memory, "photocurrent_rows": len(overlay), "photocurrent_unique_pulses": len({int(row["pulse_index"]) for row in overlay}), "method": {"half_peak": "First linear-interpolated downward crossing of half the raw peak after the peak; absolute acquisition time, no baseline subtraction; not a decay constant or author-defined lifetime", "auc": "Trapezoidal integral over each trace's entire observed interval, with no extrapolation", "memory": "Difference between author-averaged high-past and low-past current groups at t=0 and t=4 s using linear interpolation on separate source grids; source missing tail cells are omitted, never filled with zero; 4 s avoids poorly sampled tails; this descriptive choice is not preregistered", "inference": "No p-values, no fitted parameters, no extrapolation, no mechanistic inference, no cross-material calibration"}}
    (ROOT / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if args.download:
        download()
    analyze()
