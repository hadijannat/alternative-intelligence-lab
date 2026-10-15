"""Check formal charges and the acquired reference data; no material prediction."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
formulas = [
    ("[MoVI36O112(H2O)16]8-", {"MoVI": 36, "O": 112}, -8, "known parent"),
    ("[MoVI35WVIO112(H2O)16]8-", {"MoVI": 35, "WVI": 1, "O": 112}, -8, "hypothetical control"),
    ("[MoVI35VVO112(H2O)16]9-", {"MoVI": 35, "VV": 1, "O": 112}, -9, "hypothetical control"),
    ("[MoVI34WVIVVO112(H2O)16]9-", {"MoVI": 34, "WVI": 1, "VV": 1, "O": 112}, -9, "hypothetical target"),
    ("[MoVI34WVIVIVO112(H2O)16]10-", {"MoVI": 34, "WVI": 1, "VIV": 1, "O": 112}, -10, "hypothetical reduced target"),
    ("[PVMo11O40]4-", {"PV": 1, "VV": 1, "MoVI": 11, "O": 40}, -4, "known comparator"),
    ("[PVW11O40]4-", {"PV": 1, "VV": 1, "WVI": 11, "O": 40}, -4, "known comparator"),
    ("[P2W18O62]6-", {"PV": 2, "WVI": 18, "O": 62}, -6, "known comparator"),
]
valence = {"MoVI": 6, "WVI": 6, "VV": 5, "VIV": 4, "PV": 5, "O": -2}
checks = []
for formula, atoms, expected, status in formulas:
    charge = sum(valence[atom] * count for atom, count in atoms.items())
    assert charge == expected, (formula, charge, expected)
    checks.append({"formula": formula, "oxidation_state_counts": atoms, "formal_charge": charge, "evidence_status": status})

data = ROOT / "raw/mo36_seed_timeseries.csv"
digest = hashlib.sha256(data.read_bytes()).hexdigest()
assert digest == "b9cfcb759f2140d61a7b21a984f3c5c761958d7d93ac9c815289596fae4520a7"
with data.open() as handle:
    rows = list(csv.DictReader(handle))
counts = Counter(row["Exp"] for row in rows)
assert len(rows) == 480 and len(counts) == 6 and set(counts.values()) == {80}
for condition in counts:
    times = [float(row["Time"]) for row in rows if row["Exp"] == condition]
    assert all(b > a for a, b in zip(times, times[1:]))
result = {"status": "PASS bounded accounting checks only", "formula_checks": checks,
          "data_sha256": digest, "measured_rows": len(rows), "condition_counts": dict(counts),
          "excluded_prediction_columns": ["c.pred", "c.pred.u", "c.pred.l"],
          "limits": ["No existence, geometry or stability prediction follows from charge balance.",
                     "Hydration, protonation and oxidation-state assignments are conditional.",
                     "Raw CSV units and independent replicate identities remain unresolved."]}
(ROOT / "checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "formula_checks": len(checks), "measured_rows": len(rows)}))
