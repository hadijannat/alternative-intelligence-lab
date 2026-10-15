"""Run the frozen maintenance assay and preserve every simulated step."""

import argparse
import csv
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
if __package__ in (None, ""):
    sys.path.insert(0, str(HERE.parent))
from maintenance.model import Params, initialise, step

FROZEN_FILES = ("__init__.py", "config.json", "PROTOCOL.md", "model.py", "test_model.py", "run_lab.py")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def freeze():
    target = HERE / "freeze.json"
    if target.exists():
        raise FileExistsError(f"Refusing to replace {target}")
    checks = subprocess.run([sys.executable, "-m", "unittest", "maintenance.test_model", "-v"], cwd=HERE.parent, text=True, capture_output=True)
    if checks.returncode:
        raise RuntimeError(checks.stdout + checks.stderr)
    record = {
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "files": {name: sha(HERE / name) for name in FROZEN_FILES},
        "test_command": f"{sys.executable} -m unittest maintenance.test_model -v",
        "test_exit_code": checks.returncode,
        "test_output": checks.stdout + checks.stderr,
        "official_runs_started": False,
    }
    write_json(target, record)
    print(f"Frozen {len(FROZEN_FILES)} files after passing unit tests: {target}")


def run_arm(config, seed, arm, feed_schedule, writer=None, dt=None):
    params = Params(**config["params"])
    if arm == "no_renewal":
        params = replace(params, renewal=False)
    if arm == "extra_leak":
        params = replace(params, decay_rate=params.decay_rate * config["extra_leak_multiplier"])
    state = initialise(**config["initial"])
    reservoir = config["reservoir"]
    dt = config["dt"] if dt is None else dt
    max_error = 0.0
    requested_work = 0.0
    fuel_start = state.fuel

    def row(index, influx=0, actual_work=0, renewed=0, converted=0):
        nonlocal max_error
        errors = {
            "material_residual": state.fuel + state.waste + state.structure - state.initial_material - state.fed_total,
            "energy_residual": state.energy + state.spent + state.dissipated - state.initial_energy - state.energy_generated,
            "reservoir_residual": reservoir + state.fed_total - config["reservoir"],
            "fuel_energy_residual": state.energy_generated - params.energy_yield * (fuel_start + state.fed_total - state.fuel),
        }
        max_error = max(max_error, *(abs(value) for value in errors.values()))
        record = {"seed": seed, "arm": arm, "step": index, "time": index * dt, **asdict(state), "reservoir": reservoir,
                  "influx": influx, "actual_work": actual_work, "renewed": renewed, "converted": converted, **errors}
        if writer is not None:
            writer.writerow(record)

    row(0)
    for index, offered in enumerate(feed_schedule, 1):
        influx = 0.0 if arm == "no_feed" else min(reservoir, offered)
        work = config["work_rate"] * dt
        result = step(state, influx, work, dt, params)
        state = result.state
        reservoir -= result.accepted_influx
        requested_work += work
        row(index, result.accepted_influx, result.actual_work, result.renewed, result.converted)
    return {"seed": seed, "arm": arm, "state": asdict(state), "reservoir": reservoir, "requested_work": requested_work,
            "work_fraction": state.spent / requested_work if requested_work else 1.0,
            "founder_fraction": state.founder_structure / state.structure if state.structure else 0.0,
            "maximum_absolute_ledger_error": max_error}


def evaluate(config, results):
    c = config["criteria"]
    paired = []
    for seed in config["seeds"]:
        arms = {row["arm"]: row for row in results if row["seed"] == seed}
        normal = arms["normal"]
        size = normal["state"]["structure"]
        checks = {
            "normal_retains_structure": size >= c["normal_structure_minimum"],
            "normal_renews_material": normal["state"]["new_structure"] >= c["normal_new_structure_minimum"],
            "founder_material_is_replaced": normal["founder_fraction"] <= c["normal_founder_fraction_maximum"],
            "normal_pays_work": normal["work_fraction"] >= c["normal_work_fraction_minimum"],
            "no_feed_dependency": arms["no_feed"]["state"]["structure"] <= c["negative_control_structure_ratio_maximum"] * size,
            "no_renewal_dependency": arms["no_renewal"]["state"]["structure"] <= c["negative_control_structure_ratio_maximum"] * size,
            "extra_leak_effect": arms["extra_leak"]["state"]["structure"] <= c["extra_leak_structure_ratio_maximum"] * size,
            "valid_ledgers": all(row["maximum_absolute_ledger_error"] <= c["ledger_tolerance"] for row in arms.values()),
        }
        paired.append({"seed": seed, "checks": checks, "pass": all(checks.values())})
    valid = len(results) == len(config["seeds"]) * len(config["arms"]) and all(row["checks"]["valid_ledgers"] for row in paired)
    decision = "INVALID_RUN" if not valid else "SUPPORTED_WITHIN_PHENOMENOLOGICAL_MODEL" if all(row["pass"] for row in paired) else "UNSUPPORTED_WITHIN_THIS_PROTOCOL"
    return {"decision": decision, "passed_seeds": sum(row["pass"] for row in paired), "total_seeds": len(paired), "paired": paired}


def run(output):
    frozen = json.loads((HERE / "freeze.json").read_text())
    for name, expected in frozen["files"].items():
        if sha(HERE / name) != expected:
            raise ValueError(f"Frozen source changed: {name}")
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite {output}")
    config = json.loads((HERE / "config.json").read_text())
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    results = []
    fieldnames = ["seed", "arm", "step", "time", *asdict(initialise()), "reservoir", "influx", "actual_work", "renewed", "converted",
                  "material_residual", "energy_residual", "reservoir_residual", "fuel_energy_residual"]
    with (output / "trajectories.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for seed in config["seeds"]:
            rng = random.Random(seed)
            feed = [config["feed_rate"] * config["dt"] * (1 + rng.uniform(-config["feed_noise_fraction"], config["feed_noise_fraction"])) for _ in range(config["steps"])]
            for arm in config["arms"]:
                results.append(run_arm(config, seed, arm, feed, writer))
    summary = evaluate(config, results)
    # shortcut: deterministic constant-feed refinement, extend to measured forcing after calibration.
    refinement = []
    for arm in config["arms"]:
        coarse = run_arm(config, None, arm, [config["feed_rate"] * config["dt"]] * config["steps"])
        fine = run_arm(config, None, arm, [config["feed_rate"] * config["dt"] / 2] * (config["steps"] * 2), dt=config["dt"] / 2)
        refinement.append({"arm": arm, "coarse_structure": coarse["state"]["structure"], "fine_structure": fine["state"]["structure"],
                           "relative_structure_difference": abs(coarse["state"]["structure"] - fine["state"]["structure"]) / max(1e-15, fine["state"]["structure"]),
                           "coarse_energy": coarse["state"]["energy"], "fine_energy": fine["state"]["energy"]})
    summary["maximum_absolute_ledger_error"] = max(row["maximum_absolute_ledger_error"] for row in results)
    summary["living_entity_created"] = False
    summary["molecular_implementation_demonstrated"] = False
    summary["intelligence_demonstrated"] = False
    write_json(output / "summary.json", summary)
    write_json(output / "endpoints.json", results)
    write_json(output / "dt_refinement.json", refinement)
    for name in ("config.json", "PROTOCOL.md", "freeze.json"):
        (output / name).write_bytes((HERE / name).read_bytes())
    table = []
    for arm in config["arms"]:
        rows = [row for row in results if row["arm"] == arm]
        values = [row["state"]["structure"] for row in rows]
        new = [row["state"]["new_structure"] for row in rows]
        paid = [row["work_fraction"] for row in rows]
        table.append(f"| {arm} | {min(values):.6f} to {max(values):.6f} | {min(new):.6f} to {max(new):.6f} | {min(paid):.6f} to {max(paid):.6f} |")
    report = f"""# Finite-inventory maintenance laboratory

Decision: **{summary['decision']}**. {summary['passed_seeds']}/{summary['total_seeds']} paired seeds met every frozen endpoint. This is a conditional mechanism result in an analyst-designed model.

| Arm | Final structure tokens | Surviving new structure | Fraction of requested work paid |
| --- | ---: | ---: | ---: |
{chr(10).join(table)}

All {len(results)} runs retain their initial state and 600 subsequent steps in trajectories.csv. The maximum absolute material, energy, reservoir or fuel-energy residual is {summary['maximum_absolute_ledger_error']:.3g}. Every accepted input is drawn from the finite 30-token external reservoir. Every work payment is capped by available work units. There is no recycling of waste or unrecorded replenishment.

The maximum final-structure relative change on deterministic constant-feed dt/2 refinement is {max(row['relative_structure_difference'] for row in refinement):.6g}. dt_refinement.json contains both endpoint values, including stored energy. This first-order sensitivity is separate from the frozen replicate decision and provides no physical calibration.

The API is `initialise(fuel, structure, energy) -> State`, `step(state, influx, work, dt, Params()) -> StepResult`, and `debit_work(state, work) -> (State, actual_work)`. Callers must debit accepted_influx from their own finite reservoir and gate task effects on actual_work. Dataclasses are immutable. `validate` rejects negative/nonfinite values and broken ledgers. Dividing an entity requires partitioning all inventories and accounting baselines; subtracting material without a recipient ledger is invalid.

The supplied renewal/catalytic rule and assumed material/work yields explain the effect by construction. This assay checks their consequences, accounting, dependence on supplied feed, and separation of founder material from new product. It establishes no chemical recipe, spontaneously originating catalyst, autonomous living entity, replication, intelligence, evolutionary novelty, or advantage over an optimized engineered maintenance controller. The finite source also rules out interpreting the endpoint as indefinite persistence. Initial structure and work are externally prepared. Preparation energy, molecular kinetics, transport and thermodynamic efficiency remain unmeasured.

Reproduce from the package root with `{sys.executable} maintenance/run_lab.py --output maintenance/replay-results` using a new output path. Frozen source hashes are checked before every run. The included unit-test record predates the official run. A rerun is computational repeatability, not independent experimental replication.
"""
    (output / "report.md").write_text(report)
    write_json(output / "manifest.json", {
        "created_utc": datetime.now(timezone.utc).isoformat(), "runtime_seconds": time.perf_counter() - started,
        "python": sys.version, "platform": platform.platform(), "source_sha256": frozen["files"],
        "freeze_sha256": sha(HERE / "freeze.json"), "trajectory_rows": len(results) * (config["steps"] + 1),
        "outputs_sha256": {path.name: sha(path) for path in sorted(output.iterdir()) if path.is_file()},
    })
    print(json.dumps({"output": str(output), "decision": summary["decision"], "passed_seeds": summary["passed_seeds"], "runs": len(results), "maximum_absolute_ledger_error": summary["maximum_absolute_ledger_error"]}))
    return 1 if summary["decision"] == "INVALID_RUN" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--freeze", action="store_true", help="run unit tests and freeze source hashes before official runs")
    group.add_argument("--output", type=Path, help="new result directory; existing paths are refused")
    args = parser.parse_args()
    try:
        if args.freeze:
            freeze()
            return 0
        return run(args.output.resolve())
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    sys.exit(main())
