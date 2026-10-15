"""Offline extraction checks, original-model diagnosis and full revised-model replay."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "measured-coupling-2026-10-15"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(left, right):
    if left.suffix == ".json":
        a, b = json.loads(left.read_text()), json.loads(right.read_text())
        if isinstance(a, dict) and isinstance(b, dict):
            a.pop("elapsed_seconds", None)
            b.pop("elapsed_seconds", None)
        return a == b
    return sha(left) == sha(right)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("Use an unused output directory")
    output.mkdir(parents=True)
    started = time.monotonic()
    receipt = {"status": "running", "commands": [], "comparisons": [], "physical_replication": False,
               "python": sys.version, "packages": {name: importlib.metadata.version(name) for name in
                                                    ("numpy", "scipy", "matplotlib", "openpyxl", "PyMuPDF")}}
    inputs = [ROOT / "run_suite.py", ROOT / "diagnose.py", ROOT / "requirements.txt"]
    inputs += sorted(p for p in (ROOT / "model").iterdir() if p.suffix == ".py" or p.name == "PROTOCOL.md")
    inputs += sorted(p for p in (ROOT / "sources").rglob("*") if p.is_file() and
                     "__pycache__" not in p.parts and ".omo" not in p.parts and p.suffix != ".png")
    baseline = sorted(p for p in BASE.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    before = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    baseline_before = {str(p.relative_to(BASE)): sha(p) for p in baseline}
    with zipfile.ZipFile(output / "code-and-ledger-snapshot.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for p in inputs:
            if p.suffix in (".py", ".md", ".json", ".csv", ".txt") and p.stat().st_size < 3_000_000:
                archive.write(p, str(p.relative_to(ROOT)))

    def execute(label, arguments, cwd=ROOT):
        proc = subprocess.run([sys.executable, *arguments], cwd=cwd, capture_output=True,
                              text=True, timeout=1200)
        log = proc.stdout + proc.stderr
        (output / (label + ".log")).write_text(log)
        receipt["commands"].append({"label": label, "arguments": arguments,
                                    "cwd": str(cwd.relative_to(ROOT)), "exit_code": proc.returncode})
        if proc.returncode:
            raise RuntimeError(f"{label} failed; see retained log")
        return log

    try:
        execute("salibi-data", ["sources/salibi/extract.py"])
        execute("retention-data", ["sources/retention/extract.py"])
        execute("inheritance-data", ["sources/inheritance/verify_extract.py"])
        salibi = json.loads((ROOT / "sources/salibi/verification.json").read_text())
        retention = json.loads((ROOT / "sources/retention/.omo/evidence/verification.json").read_text())
        inheritance = json.loads((ROOT / "sources/inheritance/verification.json").read_text())
        assert salibi["all_checks_pass"] and retention["status"] == "PASS" and inheritance["all_pass"]
        receipt["data_verification"] = {"salibi_export_cells": salibi["exact_new_cell_checks"],
                                         "salibi_prior_cells": salibi["prior_extraction_cell_checks"],
                                         "retention_scenarios": len(retention["checks"]),
                                         "inheritance_scenarios": len(inheritance["checks"])}
        execute("diagnosis", ["diagnose.py", "--output", str(output / "diagnosis")])
        for name in ("diagnosis.json", "bulk_residuals.csv"):
            receipt["comparisons"].append({"file": "diagnosis-v1/" + name,
                                            "matched": compare(ROOT / "diagnosis-v1" / name, output / "diagnosis" / name)})
        log = execute("model-tests", ["-m", "unittest", "discover", "-p", "test*.py", "-v"], ROOT / "model")
        counts = re.findall(r"Ran (\d+) tests? in", log)
        assert len(counts) == 1 and int(counts[0]) > 0
        receipt["model_tests_passed"] = int(counts[0])
        execute("full-model-refit", ["run.py", "--output", str(output / "model")], ROOT / "model")
        execute("saved-parameter-replay", ["run.py", "--replay", "results-v2"], ROOT / "model")
        original = ROOT / "model/results-v2"
        numerical = sorted(p for p in original.iterdir() if p.suffix in (".json", ".csv") and
                           p.name not in ("freeze.json", "manifest.json"))
        assert numerical
        for p in numerical:
            receipt["comparisons"].append({"file": str(p.relative_to(ROOT)),
                                            "matched": compare(p, output / "model" / p.name)})
        assert all(c["matched"] for c in receipt["comparisons"]), "Numerical replay mismatch"
        assert before == {str(p.relative_to(ROOT)): sha(p) for p in inputs}, "Inputs changed during verification"
        assert baseline_before == {str(p.relative_to(BASE)): sha(p) for p in baseline}, "Previous laboratory changed"
        receipt.update(status="passed", input_sha256=before, baseline_sha256=baseline_before,
                       elapsed_seconds=time.monotonic()-started)
        print(json.dumps({"status": "passed", "model_tests": receipt["model_tests_passed"],
                          "numerical_comparisons": len(receipt["comparisons"]),
                          "data_verification": receipt["data_verification"]}))
    except Exception as exc:
        receipt.update(status="failed", error=str(exc), elapsed_seconds=time.monotonic()-started)
        raise
    finally:
        (output / "verification.json").write_text(json.dumps(receipt, indent=2)+"\n")


if __name__ == "__main__":
    main()
