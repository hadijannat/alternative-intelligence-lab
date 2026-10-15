"""Check exact source cells and provenance; no fitting or source writes."""
import csv
import hashlib
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def main():
    manifest = json.loads((ROOT / "sources.json").read_text())
    for name, expected in manifest["retained_input_sha256"].items():
        assert hashlib.sha256((REPO / name).read_bytes()).hexdigest() == expected, name
    book = openpyxl.load_workbook(REPO / manifest["workbook"], data_only=True)
    rows = list(csv.DictReader((ROOT / "s18_zero_ft_challenge.csv").open()))
    assert len(rows) == 6
    assert len({(r["source_sheet"], r["source_cell"]) for r in rows}) == 6
    for row in rows:
        assert float(row["value_percent"]) == book[row["source_sheet"]][row["source_cell"]].value
        assert int(row["ft_cycles"]) == 0 and int(row["time_min_42C"]) == 60
    means = {str(seed): sum(float(r["value_percent"]) for r in rows if int(r["seed_uM"]) == seed) / 3 for seed in (0, 1)}
    assert abs(means["0"] - 62.806) < 1e-12
    assert abs(means["1"] - 68.424) < 1e-12
    result = {"status": "PASS", "checked_input_hashes": len(manifest["retained_input_sha256"]), "exact_cells": len(rows), "mean_percent": means, "seed1_minus_seed0_pp": means["1"] - means["0"], "measured_fits_performed": 0}
    (ROOT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
