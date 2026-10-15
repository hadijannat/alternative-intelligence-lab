"""Verify retained sources and replay both chemistry models in fresh processes."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks():
    checks = []
    droplet = ROOT / "droplet_sources"
    manifest = json.loads((droplet / "manifest.json").read_text())
    for item in [*manifest["files"], manifest["supplement"]]:
        checks.append({"file": str((droplet / item["path"]).relative_to(ROOT)),
                       "matched": sha(droplet / item["path"]) == item["sha256"]})
    article = json.loads((droplet / "article_manifest.json").read_text())
    checks.append({"file": "droplet_sources/article.txt",
                   "matched": sha(droplet / "article.txt") == article["text_sha256"]})
    rna = ROOT / "rna_sources"
    for item in json.loads((rna / "retrieval_receipts.json").read_text()):
        if "sha256" in item:
            checks.append({"file": str((rna / item["file"]).relative_to(ROOT)),
                           "matched": sha(rna / item["file"]) == item["sha256"]})
    with (droplet / "tables/observations.csv").open() as handle:
        droplet_rows = sum(1 for _ in csv.DictReader(handle))
    with (rna / "observations.csv").open() as handle:
        rna_rows = sum(1 for _ in csv.DictReader(handle))
    expected = sum(json.loads((droplet / "tables/counts.json").read_text()).values())
    checks.append({"file": "droplet_sources/tables/observations.csv",
                   "rows": droplet_rows, "matched": droplet_rows == expected})
    extraction = json.loads((rna / "extraction.json").read_text())
    checks.append({"file": "rna_sources/observations.csv",
                   "rows": rna_rows, "matched": rna_rows == extraction["rows"]})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f"Output already exists: {output}")
    output.mkdir(parents=True)
    start = time.monotonic()
    receipt = {"status": "running", "python": sys.version, "platform": platform.platform(),
               "commands": [], "source_checks": [], "replay_comparisons": [],
               "physical_replication": False}
    inputs = [ROOT / "run_suite.py", ROOT / "requirements.txt"]
    for name in ("droplet_model", "rna_model", "droplet_sources", "rna_sources"):
        inputs.extend(p for p in (ROOT / name).iterdir()
                      if p.is_file() and p.suffix in (".py", ".json", ".csv", ".md"))
    inputs.append(ROOT / "droplet_sources/tables/observations.csv")
    before = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    with zipfile.ZipFile(output / "code-and-ledger-snapshot.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for p in inputs:
            archive.write(p, str(p.relative_to(ROOT)))

    def execute(label, argv, cwd):
        proc = subprocess.run([sys.executable, *argv], cwd=cwd, text=True,
                              capture_output=True, timeout=600)
        log = proc.stdout + proc.stderr
        (output / (label + ".log")).write_text(log)
        receipt["commands"].append({"label": label, "argv": argv,
                                    "cwd": str(cwd.relative_to(ROOT)), "exit_code": proc.returncode})
        if proc.returncode:
            raise RuntimeError(f"{label} failed: see {label}.log")
        return log

    try:
        import numpy, scipy, matplotlib, openpyxl
        receipt["packages"] = {m.__name__: m.__version__ for m in (numpy, scipy, matplotlib, openpyxl)}
        receipt["source_checks"] = source_checks()
        if not all(row["matched"] for row in receipt["source_checks"]):
            raise AssertionError("Retained-source integrity or extraction count mismatch")
        tests = 0
        for name in ("droplet_model", "rna_model"):
            log = execute(name + "-tests", ["-m", "unittest", "discover", "-p", "test*.py", "-v"], ROOT / name)
            counts = re.findall(r"Ran (\d+) tests? in", log)
            if len(counts) != 1 or int(counts[0]) == 0:
                raise AssertionError(f"Could not establish nonzero test count for {name}")
            tests += int(counts[0])
            execute(name + "-replay", ["run.py", "--output", str(output / name)], ROOT / name)
        receipt["tests_passed"] = tests
        # All retained numerical CSV/JSON files are compared; provenance/timing/plots are separate.
        excluded = {"freeze.json", "manifest.json", "runtime.json", "provenance.json"}
        for name in ("droplet_model", "rna_model"):
            original = ROOT / name / "results-v1"
            replay = output / name
            files = [p for p in original.iterdir() if p.suffix in (".csv", ".json") and p.name not in excluded]
            if not files:
                raise AssertionError(f"No numerical results found for {name}")
            for p in sorted(files):
                target = replay / p.name
                if p.suffix == ".json":
                    left, right = json.loads(p.read_text()), json.loads(target.read_text())
                    if isinstance(left, dict) and isinstance(right, dict):
                        left.pop("elapsed_seconds", None)
                        right.pop("elapsed_seconds", None)
                    matched = left == right
                    method = "JSON equality, excluding top-level elapsed_seconds only"
                else:
                    matched, method = sha(p) == sha(target), "SHA256 byte equality"
                receipt["replay_comparisons"].append({"file": str(p.relative_to(ROOT)),
                                                        "matched": matched, "method": method})
        if not all(row["matched"] for row in receipt["replay_comparisons"]):
            raise AssertionError("Numerical replay mismatch")
        if before != {str(p.relative_to(ROOT)): sha(p) for p in inputs}:
            raise AssertionError("Inputs changed during verification")
        if source_checks() != receipt["source_checks"]:
            raise AssertionError("Retained sources changed during verification")
        receipt.update(status="passed", input_sha256=before, elapsed_seconds=time.monotonic()-start)
        print(json.dumps({"status": "passed", "tests": tests,
                          "source_checks": len(receipt["source_checks"]),
                          "replay_comparisons": len(receipt["replay_comparisons"])}))
    except Exception as exc:
        receipt.update(status="failed", error=str(exc), elapsed_seconds=time.monotonic()-start)
        raise
    finally:
        (output / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
