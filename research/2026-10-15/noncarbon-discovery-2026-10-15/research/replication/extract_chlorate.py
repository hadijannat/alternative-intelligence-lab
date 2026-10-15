"""Extract source Table S1 without replacing inconsistent printed summaries."""
import csv
import hashlib
import json
from pathlib import Path
import statistics
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "raw/sonication-2021-mmc1.docx"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == "d9d7e44ad46285817b343d59928164ec09fafe96d9f13c92a6af7de067ef7477"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
with zipfile.ZipFile(SOURCE) as archive:
    document = ET.fromstring(archive.read("word/document.xml"))
tables = document.findall(".//w:tbl", NS)
assert len(tables) == 1
rows, printed = [], {}
condition = None
for row in tables[0].findall("w:tr", NS):
    cells = ["".join(cell.itertext()).strip() for cell in row.findall("w:tc", NS)]
    if len(cells) == 1:
        condition = cells[0]
        printed[condition] = {}
    elif cells[0] in ("RH", "LH"):
        assert condition is not None and len(cells) == 3
        mass, similarity = map(float, cells[1:])
        assert mass > 0 and 0 <= similarity <= 100
        rows.append(dict(condition=condition, trial=sum(r["condition"] == condition for r in rows) + 1,
                         seed_handedness=cells[0], total_crystal_mass_g=mass, seed_similarity_percent=similarity))
    elif cells[0] in ("Average", "Standard Deviation"):
        printed[condition][cells[0]] = list(map(float, cells[1:]))
    else:
        assert cells == ["Seed Crystal handedness", "Total Crystal mass (g)", "Percentage Seed Similarity (%)"]
assert len(rows) == 13
assert [sum(r["condition"] == c for r in rows) for c in printed] == [4, 5, 4]
summary = []
for condition, published in printed.items():
    selected = [r for r in rows if r["condition"] == condition]
    for i, field in enumerate(("total_crystal_mass_g", "seed_similarity_percent")):
        values = [r[field] for r in selected]
        for label, calculate in (("Average", statistics.mean), ("Standard Deviation", statistics.stdev)):
            observed = calculate(values)
            original = published[label][i]
            summary.append(dict(condition=condition, n=len(values), field=field, statistic=label,
                                printed=original, recomputed=observed, difference=observed - original,
                                agrees_with_rounding=abs(observed - original) <= 0.015))
assert sum(not r["agrees_with_rounding"] for r in summary) == 4
with (ROOT / "chlorate_trials.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
(ROOT / "chlorate_summary_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({"trials": len(rows), "conditions": len(printed), "summary_cells": len(summary),
                  "discrepant_summary_cells": sum(not r["agrees_with_rounding"] for r in summary)}))
