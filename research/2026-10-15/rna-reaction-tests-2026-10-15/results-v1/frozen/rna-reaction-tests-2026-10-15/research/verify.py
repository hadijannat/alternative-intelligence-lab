"""Recheck sources and proposed reaction bookkeeping, without fitting data."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ledger = json.loads((HERE / "sources.json").read_text())
checks = []
for relative, expected in ledger["sources"][0]["local_files"].items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
    checks.append("primary source hash: " + relative)
si = (ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt").read_text()
compact = "".join(si.split("Supplementary Table 1.")[1].split("PDF PAGE 5")[0].split())
a, r, b = (ledger["sequences"][key] for key in ("A", "R", "B"))
assert (len(a), len(r), len(b)) == (52, 52, 14)
assert all(sequence in compact for sequence in (a, r, b, a + b))
assert [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, r)) if x != y] == [(38, "G", "A")]
checks.append("exact primary SI sequences and reporter G38A")
model = (ROOT / "rna-mechanism-2026-10-15/model/model.py").read_text()
assert "p.kf*f*a*occupancy" in model and "p.kf*f*r*occupancy" in model
assert "p.kh*a*a*occupancy**2" in model and "p.hroute*p.kh*a*r*occupancy**2" in model
checks.append("revised model shares F efficiencies; optional hroute=1 ties precursor efficiencies")
rows = list(csv.DictReader((ROOT / "rna-mechanism-2026-10-15/sources/salibi/observations.csv").open()))
counts = Counter(row["source_sheet"] for row in rows)
assert len(rows) == 529 and counts["S12"] == 126 and counts["S15"] == 18 and counts["S18"] == 48
checks.append("existing source export inventory; no claimed new acquisition")
# Species: A,R,B,F,P,I. Columns: active ligation, reporter ligation, functional loss.
reactions = [(-1, 0, -1, 1, 0, 0), (0, -1, -1, 0, 1, 0), (0, 0, 0, -1, 0, 1)]
moieties = [(1, 0, 0, 1, 0, 1), (0, 1, 0, 0, 1, 0), (0, 0, 1, 1, 1, 1)]
assert all(sum(x * y for x, y in zip(m, reaction)) == 0 for m in moieties for reaction in reactions)
checks.append("all three moieties conserved by proposed net reactions")
# Extend species with CA,CR; forward trapping takes one of each free strand.
complex_reactions = [(-1, 0, -1, 0, 0, 0, 1, 0), (0, -1, -1, 0, 0, 0, 0, 1)]
complex_moieties = [(1, 0, 0, 1, 0, 1, 1, 0), (0, 1, 0, 0, 1, 0, 0, 1), (0, 0, 1, 1, 1, 1, 1, 1)]
assert all(sum(x * y for x, y in zip(m, reaction)) == 0 for m in complex_moieties for reaction in complex_reactions)
assert "prepared on ice" in si and "started by the addition of MgCl2" in si
checks.append("complex stoichiometry and Mg-triggered assay start; initial occupancy remains unknown")
assert len({item["id"] for item in ledger["sources"]}) == 4
assert all(item["primary"] and item["does_not_establish"] and item["data_admission"] for item in ledger["sources"])
assert ledger["new_compatible_numerical_holdout_acquired"] is False
checks.append("bounded primary-source admission ledger")
out = HERE / ".omo/evidence/verification.json"
out.parent.mkdir(parents=True, exist_ok=True)
result = {
    "status": "PASS_SOURCE_AND_DESIGN_CHECKS_ONLY", "checks": checks, "check_count": len(checks),
    "scenario": "retained source identities, rate equalities, data inventory and stoichiometric conservation",
    "invocation": "python3 rna-reaction-tests-2026-10-15/research/verify.py",
    "source_sheet_counts": dict(counts),
    "artifact_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE / "REPORT.md", HERE / "sources.json", HERE / "verify.py")},
    "not_tested": "No new kinetic fit, physical mechanism, external dataset compatibility experiment, or wet assay."
}
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": len(checks), "artifact": str(out)}))
