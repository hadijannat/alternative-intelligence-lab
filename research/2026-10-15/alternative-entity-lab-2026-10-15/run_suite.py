"""Test and replay all four laboratories from retained inputs, without network access."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New directory for replay, logs and verification.json")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f"output already exists: {output}")
    output.mkdir(parents=True)
    commands = []

    def execute(label, argv, cwd=ROOT):
        completed = subprocess.run([sys.executable,*argv],cwd=cwd,capture_output=True,text=True,timeout=120)
        (output/f"{label}.log").write_text(completed.stdout+completed.stderr)
        commands.append({"label":label,"argv":[sys.executable,*argv],"cwd":str(cwd),"exit_code":completed.returncode})
        if completed.returncode:
            raise RuntimeError(f"{label} failed; read {output / (label+'.log')}")

    inputs = [ROOT/"run_suite.py"]
    for directory in ("maintenance","heredity","integrated","research"):
        inputs.extend(p for p in (ROOT/directory).iterdir() if p.is_file() and p.suffix in (".py",".json") and p.name != "results.json")
    before = {str(p.relative_to(ROOT)):sha(p) for p in inputs}
    try:
        execute("maintenance-tests",["-m","unittest","maintenance.test_model","-v"])
        execute("heredity-tests",["-m","unittest","test_lab","-v"],ROOT/"heredity")
        execute("integrated-tests",["-m","pytest","integrated/test_lab.py","-q"])
        execute("research-tests",["-m","unittest","test_analysis","-v"],ROOT/"research")
        execute("maintenance-replay",["maintenance/run_lab.py","--output",str(output/"maintenance")])
        execute("heredity-replay",["heredity/lab.py","--output",str(output/"heredity")])
        execute("integrated-replay",["integrated/lab.py","--output",str(output/"integrated")])
        shutil.copytree(ROOT/"research",output/"research",ignore=shutil.ignore_patterns("__pycache__",".pytest_cache"))
        execute("research-replay",[str(output/"research/analyze_data.py")])
        pairs = [
            ("maintenance/results-v1/trajectories.csv","maintenance/trajectories.csv"),
            ("maintenance/results-v1/endpoints.json","maintenance/endpoints.json"),
            ("maintenance/results-v1/summary.json","maintenance/summary.json"),
            ("maintenance/results-v1/dt_refinement.json","maintenance/dt_refinement.json"),
            ("heredity/results-v1/raw.csv","heredity/raw.csv"),
            ("integrated/results-v1.2/trajectories.csv","integrated/trajectories.csv"),
            ("integrated/results-v1.2/summary.json","integrated/summary.json"),
            ("research/results.json","research/results.json"),
        ]
        checks = [{"source":a,"replay":b,"matched":sha(ROOT/a)==sha(output/b),"sha256":sha(ROOT/a)} for a,b in pairs]
        official = json.loads((ROOT/"heredity/results-v1/results.json").read_text())
        replay = json.loads((output/"heredity/results.json").read_text())
        official.pop("elapsed_seconds")
        replay.pop("elapsed_seconds")
        checks.append({"source":"heredity/results-v1/results.json","matched":official==replay,"comparison":"JSON excluding measured elapsed_seconds only"})
        checks.append({"source":"integrated/results-v1.1","matched":sha(ROOT/"integrated/results-v1.1/trajectories.csv")==sha(ROOT/"integrated/results-v1.2/trajectories.csv") and sha(ROOT/"integrated/results-v1.1/summary.json")==sha(ROOT/"integrated/results-v1.2/summary.json"),"comparison":"input-validation-only v1.2 must preserve v1.1 numerical outputs"})
        if not all(item["matched"] for item in checks):
            raise AssertionError(f"replay mismatch: {[c for c in checks if not c['matched']]}")
        if before != {str(p.relative_to(ROOT)):sha(p) for p in inputs}:
            raise AssertionError("source inputs changed during verification")
        receipt = {"status":"passed","tests":33,"commands":commands,"checks":checks,"input_sha256":before,"replay_is_independent_physical_replication":False}
        (output/"verification.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps({"status":"passed","tests":33,"replay_comparisons":len(checks),"receipt":str(output/"verification.json")},indent=2))
    except Exception as exc:
        (output/"failure.json").write_text(json.dumps({"status":"failed","error":str(exc),"commands":commands},indent=2)+"\n")
        raise


if __name__ == "__main__":
    main()
