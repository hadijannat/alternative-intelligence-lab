"""Engineered compartment integration; all chemistry and work units are hypothetical."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, fields, replace
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from maintenance.model import Params, State, debit_work, initialise, step, validate
from heredity.lab import partition_counts


def load_config(path):
    config = json.loads(Path(path).read_text())
    for name in ("episodes", "phase_length", "adaptation_allowance"):
        if type(config[name]) is not int or config[name] < 1:
            raise ValueError(f"{name} must be a positive integer")
    if config["adaptation_allowance"] >= config["phase_length"]:
        raise ValueError("adaptation allowance must leave an evaluation window")
    if len(config["seeds"]) != len(set(config["seeds"])) or not config["seeds"]:
        raise ValueError("seeds must be nonempty and unique")
    for name, value in config.items():
        if isinstance(value, (int, float)) and (not math.isfinite(value) or value < 0):
            raise ValueError(f"invalid {name}")
    if not 0 <= config["copy_error"] <= 0.5 or not 0 < config["learning_fraction"] <= 1:
        raise ValueError("invalid copying/learning probability")
    if config["switch_cost"] <= 0 or config["initial_structure"] < 1:
        raise ValueError("switch cost and initial carrier count must be positive")
    if config["division_structure"] <= config["initial_structure"]:
        raise ValueError("division threshold must exceed initial structure")
    for case in config["scenarios"].values():
        if any(not math.isfinite(v) or v < 0 for v in case.values()):
            raise ValueError("invalid scenario")
    Params(**config["maintenance"])
    return config


def history(config, seed):
    rng = np.random.default_rng(seed)
    n = config["episodes"]
    return {
        "cue": rng.integers(0, 2, n),
        "mapping": (np.arange(n) // config["phase_length"] + int(rng.integers(2))) % 2,
        "retention_draw": rng.random(n),
        "fallback": rng.integers(0, 2, n),
        "coin": rng.integers(0, 2, n),
        "feed_jitter": rng.uniform(0.9, 1.0, n),
    }


def retrieve(cue, delay, decay, draw, fallback):
    return int(cue if draw < math.exp(-decay * delay) else fallback)


def decide(counts, recalled_cue, tie_coin):
    hypothesis = int(counts[1] > counts[0]) if counts[1] != counts[0] else int(tie_coin)
    return int(recalled_cue) ^ hypothesis


def update_labels(counts, target_type, fraction, state, unit_cost):
    desired = int(math.ceil(int(counts[1 - target_type]) * fraction))
    switched = min(desired, int((state.energy + 1e-12) / unit_cost))
    state, paid = debit_work(state, switched * unit_cost)
    if paid + 1e-10 < switched * unit_cost:
        raise ArithmeticError("unpaid label switching")
    updated = counts.copy()
    updated[1 - target_type] -= switched
    updated[target_type] += switched
    return updated, state, switched


def renew_labels(counts, final_structure, survival, copy_error, rng):
    total = int(counts.sum())
    fraction_one = float(counts[1] / total) if total else 0.5
    survivors = rng.binomial(counts, survival)
    target = int(math.floor(final_structure + 1e-10))
    if int(survivors.sum()) > target:
        n_one = int(rng.hypergeometric(int(survivors[1]), int(survivors[0]), target))
        survivors = np.array([target - n_one, n_one], dtype=np.int64)
    new_count = target - int(survivors.sum())
    p_one = copy_error + (1 - 2 * copy_error) * fraction_one
    new_one = int(rng.binomial(new_count, p_one))
    return survivors + np.array([new_count - new_one, new_one], dtype=np.int64)


def split_state(state, fraction):
    left = State(**{f.name: getattr(state, f.name) * fraction for f in fields(state)})
    right = State(**{f.name: getattr(state, f.name) * (1 - fraction) for f in fields(state)})
    validate(left)
    validate(right)
    return left, right


def run_case(config, seed, scenario, arm, env=None):
    env = history(config, seed) if env is None else env
    rng = np.random.default_rng(seed + 100000)
    pars = Params(**config["maintenance"])
    if arm == "no_renewal":
        pars = replace(pars, renewal=False)
    state = initialise(config["initial_fuel"], config["initial_structure"], config["initial_energy"])
    initial_mass = state.initial_material
    initial_energy = state.initial_energy
    n = int(state.structure)
    counts = np.array([n // 2, n - n // 2], dtype=np.int64)
    discarded = {f.name: 0.0 for f in fields(state)}
    stock = config["feed_stock"]
    transfers = 0
    rows = []
    dead = False
    sc = config["scenarios"][scenario]
    max_balance = 0.0
    for t in range(config["episodes"]):
        cue = int(env["cue"][t])
        target = cue ^ int(env["mapping"][t])
        correct = False
        action = -1
        recalled = -1
        harvested = 0.0
        switches = 0
        divided = False
        if not dead:
            result = step(state, 0, 0, 1.0, pars)
            state = result.state
            counts = renew_labels(counts, state.structure, math.exp(-pars.decay_rate), config["copy_error"], rng)
            dead = state.structure < config["minimum_structure"] or int(counts.sum()) == 0
        if not dead:
            if arm in ("reactive", "random", "oracle"):
                action = cue if arm == "reactive" else int(env["coin"][t]) if arm == "random" else target
            else:
                state, sensed = debit_work(state, config["sense_cost"])
                recalled = retrieve(cue, sc["delay"], config["memory_decay"], env["retention_draw"][t], env["fallback"][t])
                if sensed + 1e-10 < config["sense_cost"] or arm == "erase_cue":
                    recalled = int(env["fallback"][t])
                action = decide(counts, recalled, env["coin"][t])
            state, action_paid = debit_work(state, config["action_cost"])
            if action_paid + 1e-10 >= config["action_cost"]:
                correct = action == target
                offered = config["feed_high"] if correct else config["feed_low"]
                harvested = min(stock, offered * sc["feed_scale"] * float(env["feed_jitter"][t])) if arm != "no_feed" else 0.0
                stock -= harvested
                # Feed enters storage; conversion occurs only at the next maintenance step.
                state = replace(state, fuel=state.fuel + harvested, fed_total=state.fed_total + harvested)
                validate(state)
                if arm not in ("reactive", "random", "oracle", "no_update", "no_feed"):
                    inferred = recalled ^ (action if correct else 1 - action)
                    counts, state, switches = update_labels(counts, inferred, config["learning_fraction"], state, config["switch_cost"])
            else:
                action = -1
            if state.structure >= config["division_structure"] and state.energy >= config["division_cost"]:
                state, paid = debit_work(state, config["division_cost"])
                left, right = partition_counts(counts, rng)
                fraction = float(left.sum() / counts.sum())
                state, sister = split_state(state, fraction)
                counts = left
                for key, value in asdict(sister).items():
                    discarded[key] += value
                if arm == "offspring_shuffle":
                    # Each changed label costs work; no material is created by the intervention.
                    desired_one = int(rng.binomial(int(counts.sum()), 0.5))
                    diff = desired_one - int(counts[1])
                    if diff:
                        desired = abs(diff)
                        wrong_type = 0 if diff > 0 else 1
                        frac = desired / int(counts[wrong_type])
                        counts, state, extra = update_labels(counts, 1 - wrong_type, frac, state, config["switch_cost"])
                        switches += extra
                transfers += 1
                divided = True
                dead = state.structure < config["minimum_structure"] or int(counts.sum()) == 0
        total = {key: value + discarded[key] for key, value in asdict(state).items()}
        residuals = [
            total["fuel"] + total["waste"] + total["structure"] - initial_mass - (config["feed_stock"] - stock),
            total["energy"] + total["spent"] + total["dissipated"] - initial_energy - total["energy_generated"],
        ]
        max_balance = max(max_balance, *(abs(v) for v in residuals))
        if max_balance > config["criteria"]["balance_tolerance"]:
            raise ArithmeticError(f"global resource imbalance: {residuals}")
        rows.append({
            "seed":seed,"scenario":scenario,"arm":arm,"episode":t,"cue":cue,"mapping":int(env["mapping"][t]),
            "recalled":recalled,"action":action,"correct":int(correct),"alive":int(not dead),
            "evaluation":int(t % config["phase_length"] >= config["adaptation_allowance"]),
            "structure":state.structure,"fuel":state.fuel,"energy":state.energy,"waste":state.waste,
            "founder_structure":state.founder_structure,"new_structure":state.new_structure,
            "type0":int(counts[0]),"type1":int(counts[1]),"feed":harvested,"stock":stock,
            "switches":switches,"division":int(divided),"transfers":transfers,
            "global_material_residual":residuals[0],"global_energy_residual":residuals[1],
        })
    evaluation = [r for r in rows if r["evaluation"]]
    alive_evaluation = [r for r in evaluation if r["alive"]]
    final = rows[-1]
    summary = {"seed":seed,"scenario":scenario,"arm":arm,"survived":not dead,"transfers":transfers,
        "accuracy":float(np.mean([r["correct"] for r in evaluation])),
        "alive_accuracy":float(np.mean([r["correct"] for r in alive_evaluation])) if alive_evaluation else None,
        "alive_episodes":sum(r["alive"] for r in rows),"final_structure":state.structure,
        "founder_fraction":state.founder_structure/state.structure if state.structure else 0.0,
        "consumed_feed":config["feed_stock"]-stock,"work_spent_all_branches":state.spent+discarded["spent"],
        "dissipated_all_branches":state.dissipated+discarded["dissipated"],"max_balance_error":max_balance,
        "discarded_sisters":discarded,"final_state":asdict(state),"final_counts":counts.tolist()}
    return summary, rows


def evaluate(config, summaries):
    result = {}
    bootstrap = np.random.default_rng(2026101599)
    for scenario in config["scenarios"]:
        by_arm = {arm:[s for s in summaries if s["scenario"] == scenario and s["arm"] == arm] for arm in config["arms"]}
        margins = []
        c = config["criteria"]
        for i, adaptive in enumerate(by_arm["adaptive"]):
            reactive, random, erased = [by_arm[a][i] for a in ("reactive","random","erase_cue")]
            irrelevant = by_arm["irrelevant_erasure"][i]
            matched = all(adaptive[k] == irrelevant[k] for k in adaptive if k != "arm")
            margins.append({"seed":adaptive["seed"],"integration_pass":bool(adaptive["survived"] and adaptive["transfers"] >= c["minimum_transfers"] and adaptive["founder_fraction"] <= c["maximum_founder_fraction"] and adaptive["accuracy"] - max(reactive["accuracy"],random["accuracy"]) >= c["accuracy_advantage"]),
                "accuracy_advantage":adaptive["accuracy"] - max(reactive["accuracy"], random["accuracy"]),
                "erasure_effect":adaptive["accuracy"]-erased["accuracy"],"irrelevant_equal":matched,
                "offspring_shuffle_effect":adaptive["accuracy"]-by_arm["offspring_shuffle"][i]["accuracy"]})
        effects = np.array([m["accuracy_advantage"] for m in margins])
        means = bootstrap.choice(effects, size=(2000,len(effects)),replace=True).mean(axis=1)
        result[scenario] = {"all_seed_integration_pass":all(m["integration_pass"] for m in margins),
            "integration_seeds_passed":sum(m["integration_pass"] for m in margins),
            "all_seed_memory_pass":all(m["erasure_effect"] >= c["erasure_effect"] for m in margins),
            "irrelevant_control_pass":all(m["irrelevant_equal"] for m in margins),
            "mean_accuracy_advantage":float(effects.mean()),"paired_seed_bootstrap_95_interval":np.quantile(means,[.025,.975]).tolist(),
            "margins":margins,
            "arms":{arm:{"mean_accuracy":float(np.mean([s["accuracy"] for s in values])),"survived":sum(s["survived"] for s in values),"mean_transfers":float(np.mean([s["transfers"] for s in values])),"mean_feed":float(np.mean([s["consumed_feed"] for s in values]))} for arm,values in by_arm.items()}}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    args.output.mkdir(parents=True, exist_ok=False)
    frozen = args.output / "frozen"
    frozen.mkdir()
    sources = [Path(__file__),args.config,Path(__file__).with_name("PROTOCOL.md"),ROOT/"maintenance/model.py",ROOT/"heredity/lab.py"]
    pins = {}
    for source in sources:
        key = str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else source.name
        pins[key] = hashlib.sha256(source.read_bytes()).hexdigest()
        dest = frozen / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source,dest)
    receipt = {"started_utc":datetime.now(timezone.utc).isoformat(),"source_sha256":pins,"python":platform.python_version(),"numpy":np.__version__,"evidence_class":"supplied dimensionless integrated construction","physical_life_demonstrated":False,"general_intelligence_demonstrated":False}
    (args.output/"manifest.json").write_text(json.dumps(receipt,indent=2)+"\n")
    summaries = []
    with (args.output/"trajectories.csv").open("w",newline="") as f:
        writer = None
        for seed in config["seeds"]:
            env = history(config,seed)
            for scenario in config["scenarios"]:
                for arm in config["arms"]:
                    summary,rows = run_case(config,seed,scenario,arm,env)
                    if writer is None:
                        writer = csv.DictWriter(f,fieldnames=list(rows[0]))
                        writer.writeheader()
                    writer.writerows(rows)
                    summaries.append(summary)
    result = {"runs":len(summaries),"evaluation":evaluate(config,summaries),"per_run":summaries}
    (args.output/"summary.json").write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({"runs":len(summaries),"outcome":{k:{x:v[x] for x in ("all_seed_integration_pass","integration_seeds_passed","all_seed_memory_pass","irrelevant_control_pass")} for k,v in result["evaluation"].items()}},indent=2))


if __name__ == "__main__":
    main()
