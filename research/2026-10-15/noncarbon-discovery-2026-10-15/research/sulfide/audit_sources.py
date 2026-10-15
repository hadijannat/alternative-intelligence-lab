"""Inventory downloaded primary data without treating figure rows as replicates."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
EXPECTED = {
    "nickel-mackinawite.csv": (8502, 68),
    "mos2-fig1f.csv": (43, 17),
    "mos2-fig2g.csv": (17, 23),
    "mos2-fig2i.csv": (130, 4),
    "mos2-fig3b-d.csv": (49, 31),
    "mos2-fig3f.csv": (4, 6),
}


def main():
    inventory = []
    for filename, expected in EXPECTED.items():
        path = RAW / filename
        rows = list(csv.reader(path.open(newline="")))
        dimensions = (len(rows), max(map(len, rows)))
        assert dimensions == expected, (filename, dimensions, expected)
        inventory.append({"file": filename, "bytes": path.stat().st_size,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "rows_including_headers": dimensions[0],
                          "maximum_columns": dimensions[1]})
    rows = list(csv.reader((RAW / "nickel-mackinawite.csv").open(newline="")))
    extracted = []
    for row in rows[1:]:
        for label, tcol, ycol in [("higher_loading", 18, 19), ("lower_loading", 20, 21)]:
            if row[tcol] and row[ycol]:
                extracted.append({"series": label, "time_h": float(row[tcol]),
                                  "aqueous_Ni_mmol_L": float(row[ycol])})
    assert len(extracted) == 20
    for label in ("higher_loading", "lower_loading"):
        series = [r for r in extracted if r["series"] == label]
        assert all(r["aqueous_Ni_mmol_L"] >= 0 for r in series)
        assert all(b["time_h"] > a["time_h"] for a, b in zip(series, series[1:]))
    with (ROOT / "nickel_uptake_fig4.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(extracted[0]))
        writer.writeheader()
        writer.writerows(extracted)
    result = {"status": "PASS", "scope": "byte inventory and source-table parsing only",
              "data_files": inventory, "kinetic_rows": len(extracted),
              "independent_replicates_verified": False,
              "fitting_or_predictive_validation_performed": False}
    (ROOT / "data_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
