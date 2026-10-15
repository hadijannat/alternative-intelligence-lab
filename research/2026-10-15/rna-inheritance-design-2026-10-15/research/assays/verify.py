"""Check source-transcribed identities and retain reproducible assay design evidence."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt"
ledger = json.loads((HERE / "ledger.json").read_text())
seq = ledger["sequences"]
source = SOURCE.read_text().split("Supplementary Table 1.")[1].split("PDF PAGE 5")[0]
compact = "".join(source.split())
checks = []
for name, row in seq.items():
    assert len(row["sequence"]) == row["length_nt"], name
    assert set(row["sequence"]) <= set("ACGU"), name
    assert row["sequence"] in compact, name
    checks.append(f"{name}: length/alphabet/exact SI sequence")
assert seq["Hyper_A"]["sequence"] + seq["B"]["sequence"] == seq["F1"]["sequence"]
checks.append("52+14 nt precursor concatenation equals 66 nt F1")
differences = [(i + 1, a, b) for i, (a, b) in enumerate(zip(seq["Hyper_A"]["sequence"], seq["Cy5_A"]["sequence"])) if a != b]
assert differences == [(38, "G", "A")]
checks.append("Cy5-A differs from Hyper-A at G38A only")
ids = {source["id"] for source in ledger["sources"]}
assert len(ids) == len(ledger["sources"]) == 8
assert all(source["primary"] and source["url"].startswith("https://") and source["does_not_establish"] for source in ledger["sources"])
assert len(ledger["measurements"]) == 6
checks.append("eight primary source records and six bounded measurements")
volume_litres = 4 * math.pi * (5e-6) ** 3 / 3 * 1000
amount_fmol = volume_litres * 1e-6 * 1e15
assert abs(amount_fmol - 0.0005235987755982989) < 1e-12
checks.append("10 micron diameter at 1 micromolar contains 0.0005235988 fmol = 0.5235988 amol")
files = [SOURCE, HERE / "REPORT.md", HERE / "ledger.json", HERE / "verify.py"]
evidence = {"status": "PASS", "scenario": "exact SI identity and design ledger validation", "invocation": "python3 rna-inheritance-design-2026-10-15/research/assays/verify.py", "checks": checks, "check_count": len(checks), "amount_example_fmol": amount_fmol, "hashes": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}, "not_tested": "No wet assay, analytical sensitivity, label neutrality, native recovery or experimental inheritance was tested."}
out = HERE / ".omo/evidence/verification.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"status": evidence["status"], "checks": len(checks), "artifact": str(out)}))
