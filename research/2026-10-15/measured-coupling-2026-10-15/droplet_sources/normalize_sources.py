"""Make source-preserving tables, without fitting or running author notebooks."""
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT / "author"
OUT = ROOT / "tables"
FIELDS = ["source_file", "source_row", "condition_id", "measurement", "analyte",
          "time_value", "time_unit", "value", "value_unit", "replicate_id",
          "replicate_basis", "notes"]
ROWS = []


def read(name):
    paths = list(AUTHOR.rglob(name))
    assert len(paths) == 1, name
    path = paths[0]
    return str(path.relative_to(ROOT)), list(csv.DictReader(path.open()))


def emit(path, i, condition, measurement, analyte, time, time_unit, value, unit,
         replicate, note="", basis="ordinal within identical condition/time; longitudinal pairing unknown"):
    assert math.isfinite(float(value)), (path, i, value)
    ROWS.append(dict(zip(FIELDS, [path, i + 2, condition, measurement, analyte,
                                  time, time_unit, value, unit, replicate, basis, note])))


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for item in manifest["files"] + [manifest["supplement"]]:
        assert hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"]
    for name, condition in [("Figure1F_Click_droplets.csv", "single_Cys_PSS"),
                            ("Figure1F_Click_no_droplets.csv", "single_Cys_noPSS")]:
        path, rows = read(name)
        seen = Counter()
        for i, row in enumerate(rows):
            seen[row["time"]] += 1
            emit(path, i, condition, "concentration", "C3", row["time"], "min", row["T"], "mM",
                 seen[row["time"]], "NoPSS values duplicate FigureS1 With RG2 T; do not count twice.")
    for name, condition in [("Figure1C_Click.csv", "single_Cys_PSS"),
                            ("Figure1C_Control.csv", "single_Cys_PSS_no_click")]:
        path, rows = read(name)
        for i, row in enumerate(rows):
            if not row["variable"]:
                assert float(row["Time"]) <= 0 and float(row["value"]) == 0.09
                continue
            emit(path, i, condition, "turbidity", "OD650", row["Time"], "min",
                 row["value"], "OD650", row["variable"],
                 "Unlabeled time<=0 constant0.09 plotting baseline omitted. Matched nominal chemistry to Figure1F, not same aliquot/paired replicate.", "source well label")
    path, rows = read("FigureS1.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        key = row["Type"], row["time"]
        seen[key] += 1
        condition = "single_Cys_noPSS" if row["Type"] == "With RG2" else "Cys_click_only"
        for field, species in [("Az", "C-N3"), ("M", "C1_intermediate"), ("B", "C2_intermediate"), ("T", "C3")]:
            emit(path, i, condition, "concentration", species, row["time"], "min", row[field], "mM", seen[key],
                 "With RG2 T duplicates Figure1F no-droplet observations; measured species do not perfectly close mass balance.")
    path, rows = read("FigureS2.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        key = row["Seed_mM"], row["time"]
        seen[key] += 1
        emit(path, i, "Cys_seed_" + row["Seed_mM"], "concentration", "C3_total_including_seed",
             row["time"], "min", row["T"], "mM", seen[key],
             "FigureS2 confirms C3 seeding but does not explicitly restate PSS/EDC/peptide concentrations; not automatically same conditions as droplet trace.")
    path, rows = read("FigureS3.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        key = row["Condition"], row["time"]
        seen[key] += 1
        for field, species in [("F", "EDC"), ("Ac", "peptide_acid"), ("An", "peptide_anhydride"), ("W", "EDU_waste")]:
            note = "Ac derived as 16-An; W equals 50-F; do not treat all four as independent measured quantities. PSS is not stated in S3 caption."
            emit(path, i, "fuel_click_" + row["Condition"], "concentration", species,
                 row["time"], "min", row[field], "mM", seen[key], note)
    path, rows = read("FigureS4.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        condition = "single_" + row["Azide_1"] + ("_PSS" if row["Type"] == "pSS" else "_noPSS")
        key = condition, row["Time"]
        seen[key] += 1
        emit(path, i, condition, "azide_conversion", row["Azide_1"] + "-N3", row["Time"], "min",
             row["Conversion"], "percent", seen[key], "Azide consumption; not directly tris-triazole concentration.")
    path, rows = read("FiguresS5_S7_S10.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        condition = "competition_" + row["Azide_1"] + "_" + row["Azide_2"] + ("_PSS" if row["Type"] == "pSS" else "_noPSS")
        key = condition, row["Time"]
        seen[key] += 1
        for field, species in [("Yield1", row["Azide_1"]), ("Yield2", row["Azide_2"])]:
            emit(path, i, condition, "azide_conversion", species + "-N3", row["Time"], "min",
                 row[field], "percent", seen[key], "Competition changes composition; not interchangeable with single-azide experiments.")
    path, rows = read("Figure2F_Partitioning.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        seen[row["Compound"]] += 1
        emit(path, i, "partition_" + row["Compound"], "partition_coefficient", row["Compound"],
             "2", "min before 1-min centrifugation", row["Kp"], "dimensionless", seen[row["Compound"]],
             "No ascorbate; azide and Cu partition differ from active click conditions. Equilibrium enrichment does not identify leakage.")
    for name, mode in [("Figure3H_insitu.csv", "insitu"), ("Figure3H_exsitu.csv", "exsitu")]:
        path, rows = read(name)
        for i, row in enumerate(rows):
            emit(path, i, "FRAP_" + mode, "normalized_fluorescence", "NBD-R_labeled_fraction",
                 row["sec"], "s", row["I"], "relative_intensity", "one_published_trace",
                 "Internal 4um-spot recovery, not trans-boundary loss of active KR3.", "replicate not identified in source")
    for name in ["Figure3C_Lifetime.csv", "Figure4D_Lifetimes.csv", "Figure5D_Lifetimes.csv"]:
        path, rows = read(name)
        seen = Counter()
        for i, row in enumerate(rows):
            condition = ("lifetime_single_" + row["Azide_1"] + "_" + row["Type"] if name.startswith("Figure3") else
                         ("refuel_seeded_" if name.startswith("Figure5") else "refuel_EDConly_") + row["Refuel_time"])
            seen[condition] += 1
            emit(path, i, condition, "droplet_lifetime", "OD650_disappearance", "", "", row["Lt"], "min",
                 seen[condition], "Published derived lifetime; thresholds and population identity are not resolved.")
    for name in ["Figure4B_no_dissolved.csv", "Figure4C_dissolved.csv", "Figure5B_Plate_reader.csv", "Figure5C_Plate_reader.csv"]:
        path, rows = read(name)
        seen = Counter()
        for i, row in enumerate(rows):
            condition = ("refuel_seeded_" if name.startswith("Figure5") else "refuel_EDConly_") + row["Refuel_time"]
            key = condition, row["Cycle"], row["Time"]
            seen[key] += 1
            replicate = row.get("variable") or seen[key]
            emit(path, i, condition, "turbidity", "OD650", row["Time"], "min", row["value"], "OD650",
                 replicate, "Cycle=" + row["Cycle"] + "; use Refuel_time metadata: Figure5B file is 8min and Figure5C file is 50min (caption reversed).",
                 "well label" if row.get("variable") else "ordinal at matched time; longitudinal pairing unknown")
    path, rows = read("Figure5E_product_distribution.csv")
    seen = Counter()
    for i, row in enumerate(rows):
        condition = "refuel_seeded_" + ("8min" if row["Type"] == "Did not dissolved" else "50min")
        key = condition, row["variable"]
        seen[key] += 1
        emit(path, i, condition, "relative_product_distribution", row["variable"], "third_cycle_endpoint", "",
             row["value"], "percent_HPLC_relative_area", seen[key],
             "A=C; B=KR. Nonquantitative filtration; background KR3 subtracted; not absolute concentrations.")
    OUT.mkdir(exist_ok=True)
    with (OUT / "observations.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ROWS)
    counts = Counter(row["condition_id"] for row in ROWS)
    (OUT / "counts.json").write_text(json.dumps(dict(sorted(counts.items())), indent=2) + "\n")
    assert len([r for r in ROWS if r["source_file"].endswith("Figure1F_Click_droplets.csv")]) == 16
    assert counts["refuel_seeded_8min"] > 700
    assert counts["refuel_seeded_50min"] > 1800
    print(f"Validated all source hashes; wrote {len(ROWS)} source-preserving observations")


if __name__ == "__main__":
    main()
