"""Finite-resource, explicitly supplied compositional copying model."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import numpy as np

ARMS = ("faithful", "exchanged", "neutral", "no_synthesis")
HERE = Path(__file__).resolve().parent


def _counts(counts: np.ndarray) -> np.ndarray:
    a = np.asarray(counts)
    if a.shape != (2,) or a.dtype.kind not in "iu" or np.any(a < 0):
        raise ValueError("counts must be a nonnegative integer array of shape (2,)")
    if sum(map(int, a)) > np.iinfo(np.int64).max:
        raise ValueError("counts exceed int64 range")
    return a.astype(np.int64, copy=True)


def _probability(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.number)):
        raise ValueError(f"{name} must be a number")
    if not np.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must lie in [0, 1]")


def partition_counts(counts: np.ndarray, rng: np.random.Generator):
    """Return two real daughters; each species count is exactly conserved."""
    a = _counts(counts)
    first = rng.binomial(a, 0.5)
    return first, a - first


def mutate_counts(counts: np.ndarray, probability: float, rng: np.random.Generator):
    """Switch the types of existing molecules without adding or losing material."""
    a = _counts(counts)
    _probability(probability, "probability")
    switched = rng.binomial(a, probability)
    return a - switched + switched[::-1]


def validate_config(c):
    expected = {"version", "seeds", "compartments", "passages", "founder_purge_passage",
                "founder_counts", "mutation_probabilities", "resource_budgets",
                "degradation_probability", "birth_success_probability",
                "production_slots_per_catalyst", "assay_substrate_per_type", "assay_rate",
                "assay_cross_activity", "final_passages", "criteria"}
    if set(c) != expected or c["version"] != "heredity-v1":
        raise ValueError("config schema/version")
    for k in ("compartments", "passages", "founder_purge_passage", "production_slots_per_catalyst",
              "assay_substrate_per_type", "final_passages"):
        if type(c[k]) is not int or c[k] < 1:
            raise ValueError(f"{k} must be a positive integer")
    if c["compartments"] % 2 or c["compartments"] < 4:
        raise ValueError("compartments must be even and at least four")
    if not c["founder_purge_passage"] < c["passages"]:
        raise ValueError("purge must precede final passage")
    if c["final_passages"] > c["passages"] - c["founder_purge_passage"]:
        raise ValueError("final window must follow purge")
    founder = _counts(np.asarray(c["founder_counts"]))
    if founder.sum() == 0 or founder[0] <= founder[1]:
        raise ValueError("founder counts must encode an A-rich starting population")
    for k in ("seeds", "resource_budgets"):
        if not isinstance(c[k], list) or not c[k] or any(type(x) is not int or x < 0 for x in c[k]):
            raise ValueError(f"invalid {k}")
        if len(set(c[k])) != len(c[k]):
            raise ValueError(f"duplicate {k}")
    if not c["mutation_probabilities"] or len(set(c["mutation_probabilities"])) != len(c["mutation_probabilities"]):
        raise ValueError("invalid mutation grid")
    for p in c["mutation_probabilities"]:
        _probability(p, "mutation")
    for k in ("degradation_probability", "birth_success_probability", "assay_cross_activity"):
        _probability(c[k], k)
    if isinstance(c["assay_rate"], bool) or not np.isfinite(c["assay_rate"]) or c["assay_rate"] <= 0:
        raise ValueError("invalid assay rate")
    criteria = c["criteria"]
    if set(criteria) != {"parent_child_correlation", "functional_contrast", "contrast_advantage", "minimum_median_new_events"}:
        raise ValueError("criteria schema")
    for key, value in criteria.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value) or value < 0:
            raise ValueError(f"invalid criterion {key}")


def retain_types(state, totals, rng):
    """Condition a fair molecular sample on chosen retained F/N counts."""
    a = rng.hypergeometric(state[:, :, 0], state[:, :, 1], totals)
    return np.stack((a, totals - a), axis=2)


def purge_founders(state):
    result = state.copy()
    removed = result[:, 0].sum(axis=1)
    result[:, 0] = 0
    return result, removed


def exchange(state, rng):
    """Pool and redistribute actual molecules; preserve each recipient's F/N count."""
    result = np.zeros_like(state)
    for age in range(2):
        pool = state[:, age].sum(axis=0)
        for i, count in enumerate(state[:, age].sum(axis=1)):
            a = int(rng.hypergeometric(pool[0], pool[1], count))
            result[i, age] = (a, count - a)
            pool -= result[i, age]
        if np.any(pool):
            raise AssertionError("exchange lost molecules")
    if not np.array_equal(result.sum(axis=2), state.sum(axis=2)):
        raise AssertionError("exchange changed recipient counts")
    return result


def assay(state, c, rng):
    substrate = c["assay_substrate_per_type"]
    rows = []
    for weights in ((1.0, c["assay_cross_activity"]), (c["assay_cross_activity"], 1.0)):
        hazard = (state * np.asarray(weights)).sum(axis=2) * c["assay_rate"] / substrate
        summed = hazard.sum(axis=1)
        events = rng.binomial(substrate, -np.expm1(-summed))
        new_share = np.divide(hazard[:, 1], summed, out=np.zeros_like(summed), where=summed > 0)
        new_events = rng.binomial(events, new_share)
        rows.append((events, new_events))
    x, y = rows[0][0], rows[1][0]
    total = x + y
    preference = np.divide(x - y, total, out=np.zeros(len(state), dtype=float), where=total > 0)
    return dict(x=x, y=y, new_events=rows[0][1]+rows[1][1], fuel=total, preference=preference)


def simulate_arm(c, seed, budget, mutation, arm):
    if arm not in ARMS:
        raise ValueError("unknown arm")
    validate_config(c)
    n = c["compartments"]
    state = np.zeros((n, 2, 2), dtype=np.int64)
    state[:n//2, 0] = c["founder_counts"]
    state[n//2:, 0] = c["founder_counts"][::-1]
    # Shared demographics match active-arm counts; chemistry/assays use distinct streams.
    dem = np.random.default_rng(np.random.SeedSequence([seed, budget, 1000]))
    typ = np.random.default_rng(np.random.SeedSequence([seed, budget, 2000, ARMS.index(arm)]))
    obs = np.random.default_rng(np.random.SeedSequence([seed, budget, 3000, ARMS.index(arm)]))
    records, count_history, preferences, new_events = [], [], [], []
    for passage in range(1, c["passages"] + 1):
        before = state.sum(axis=(1, 2))
        age_before = state.sum(axis=2)
        survivors = dem.binomial(age_before, 1 - c["degradation_probability"])
        state = retain_types(state, survivors, typ)
        degraded = age_before.sum(axis=1) - survivors.sum(axis=1)
        totals = state.sum(axis=(1, 2))
        slots = np.minimum(budget, c["production_slots_per_catalyst"] * totals)
        births = dem.binomial(slots, c["birth_success_probability"])
        if arm == "no_synthesis":
            births[:] = 0
        a_share = np.divide(state[:, :, 0].sum(axis=1), totals,
                            out=np.zeros(n, dtype=float), where=totals > 0)
        probability = np.full(n, 0.5) if arm == "neutral" else mutation + (1 - 2*mutation)*a_share
        a_births = typ.binomial(births, probability)
        state[:, 1, 0] += a_births
        state[:, 1, 1] += births - a_births
        before_partition = state.sum(axis=2)
        retained = dem.binomial(before_partition, 0.5)
        state = retain_types(state, retained, typ)
        discarded = (before_partition - retained).sum(axis=1)
        if arm == "exchanged":
            state = exchange(state, typ)
        purge = np.zeros(n, dtype=int)
        if passage == c["founder_purge_passage"]:
            state, purge = purge_founders(state)
        after = state.sum(axis=(1, 2))
        residual = before + births - degraded - discarded - purge - after
        if np.any(residual) or np.any(births > budget) or np.any(state < 0):
            raise AssertionError("finite material/resource balance")
        if passage >= c["founder_purge_passage"] and np.any(state[:, 0]):
            raise AssertionError("founder survived purge")
        measured = assay(state, c, obs)
        if np.any(measured["fuel"] > 2*c["assay_substrate_per_type"]):
            raise AssertionError("assay fuel overuse")
        count_history.append(state.sum(axis=2).tolist())
        preferences.append(measured["preference"])
        new_events.append(measured["new_events"])
        for i in range(n):
            records.append(dict(seed=seed, budget=budget, mutation=mutation, arm=arm,
                passage=passage, compartment=i, founder_group="A" if i < n//2 else "B",
                founder_A=int(state[i, 0, 0]), founder_B=int(state[i, 0, 1]),
                new_A=int(state[i, 1, 0]), new_B=int(state[i, 1, 1]),
                material_before=int(before[i]), births=int(births[i]), degraded=int(degraded[i]),
                other_daughter=int(discarded[i]), founder_purged=int(purge[i]),
                synthesis_feed_supplied=budget, synthesis_fuel_supplied=budget,
                synthesis_feed_used=int(births[i]), synthesis_fuel_used=int(births[i]),
                synthesis_unused_each=budget-int(births[i]),
                assay_X_supplied=c["assay_substrate_per_type"], assay_Y_supplied=c["assay_substrate_per_type"],
                assay_fuel_supplied=2*c["assay_substrate_per_type"],
                X_events=int(measured["x"][i]), Y_events=int(measured["y"][i]),
                new_material_events=int(measured["new_events"][i]),
                founder_events=int(measured["fuel"][i]-measured["new_events"][i]),
                assay_fuel_used=int(measured["fuel"][i]), preference=float(measured["preference"][i]),
                balance_residual=int(residual[i])))
    pref = np.asarray(preferences)
    window = c["final_passages"]
    parent, child = pref[-window-1:-1].ravel(), pref[-window:].ravel()
    correlation = float(np.corrcoef(parent, child)[0, 1]) if parent.std() and child.std() else 0.0
    contrast = float((pref[-window:, :n//2].mean() - pref[-window:, n//2:].mean()) / 2)
    summary = dict(parent_child_correlation=correlation, functional_contrast=contrast,
                   median_new_events=float(np.median(np.asarray(new_events)[-window:])),
                   final_extinct_compartments=int(np.count_nonzero(state.sum(axis=(1, 2)) == 0)),
                   post_purge_founder_events=sum(r["founder_events"] for r in records if r["passage"] >= c["founder_purge_passage"]))
    return records, summary, count_history


def wilson(successes, n):
    z = 1.959963984540054
    p = successes/n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [max(0.0, center-half), min(1.0, center+half)]


def pins():
    return {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
            for name in ("config.json", "PROTOCOL.md", "lab.py", "test_lab.py")}


def json_write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def run(c, output):
    validate_config(c)
    start = time.monotonic()
    frozen = pins()
    output.mkdir(parents=True, exist_ok=False)
    json_write(output/"freeze.json", dict(pins=frozen, config=c, python=platform.python_version(), numpy=np.__version__))
    seed_rows, conditions, writer, raw_count = [], [], None, 0
    try:
        with (output/"raw.csv").open("w", newline="") as stream:
            for mutation in c["mutation_probabilities"]:
                for budget in c["resource_budgets"]:
                    condition_rows = []
                    for seed in c["seeds"]:
                        summaries, reference = {}, None
                        for arm in ARMS:
                            records, summary, counts = simulate_arm(c, seed, budget, mutation, arm)
                            if writer is None:
                                writer = csv.DictWriter(stream, fieldnames=list(records[0]))
                                writer.writeheader()
                            writer.writerows(records)
                            raw_count += len(records)
                            if arm == "faithful":
                                reference = counts
                            elif arm != "no_synthesis" and counts != reference:
                                raise AssertionError("active controls did not match exact F/N counts")
                            if arm == "no_synthesis" and any(r["new_A"]+r["new_B"]+r["founder_A"]+r["founder_B"]+r["X_events"]+r["Y_events"] for r in records if r["passage"] >= c["founder_purge_passage"]):
                                raise AssertionError("no-synthesis retained post-purge activity")
                            summaries[arm] = summary
                        f, ex, neu = (summaries[x] for x in ARMS[:3])
                        criterion = c["criteria"]
                        exchange_advantage = f["functional_contrast"] - ex["functional_contrast"]
                        neutral_advantage = f["functional_contrast"] - neu["functional_contrast"]
                        gates = dict(correlation=f["parent_child_correlation"] > criterion["parent_child_correlation"],
                                     contrast=f["functional_contrast"] > criterion["functional_contrast"],
                                     exchange_advantage=exchange_advantage > criterion["contrast_advantage"],
                                     neutral_advantage=neutral_advantage > criterion["contrast_advantage"],
                                     new_activity=f["median_new_events"] >= criterion["minimum_median_new_events"])
                        row = dict(seed=seed, mutation=mutation, budget=budget, arms=summaries,
                                   exchange_advantage=exchange_advantage, neutral_advantage=neutral_advantage,
                                   gates=gates, passed=all(gates.values()))
                        seed_rows.append(row)
                        condition_rows.append(row)
                    successes = sum(r["passed"] for r in condition_rows)
                    conditions.append(dict(mutation=mutation, budget=budget, successes=successes,
                        total=len(condition_rows), every_replicate_pass=successes == len(condition_rows),
                        pass_fraction=successes/len(condition_rows), wilson_95=wilson(successes, len(condition_rows)),
                        exchange_advantage_range=[min(r["exchange_advantage"] for r in condition_rows), max(r["exchange_advantage"] for r in condition_rows)],
                        neutral_advantage_range=[min(r["neutral_advantage"] for r in condition_rows), max(r["neutral_advantage"] for r in condition_rows)]))
        if pins() != frozen:
            raise RuntimeError("frozen files changed during execution")
        result = dict(version=c["version"], status="complete", conditions=conditions, seeds=seed_rows,
                      raw_rows=raw_count, elapsed_seconds=time.monotonic()-start,
                      exact_active_counts_matched=True, all_material_balances_zero=True,
                      no_synthesis_post_purge_activity_zero=True,
                      conclusion="Conditional supplied-network result; physical heredity, life and intelligence unassessed.",
                      frozen_pins_verified_after_run=True)
        json_write(output/"results.json", result)
        report(output, result)
        return result
    except Exception as exc:
        json_write(output/"failure.json", dict(status="failed", error=str(exc), raw_rows=raw_count,
                   completed_seeds=seed_rows, elapsed_seconds=time.monotonic()-start))
        raise


def report(output, result):
    lines = ["# Compositional transmission: official v1 results", "",
             "The result concerns an investigator-supplied copying/assay network. No physical chemistry was calibrated or executed.", "",
             "| Copying error | Resource budget | Seed passes | Every replicate | Wilson 95% interval |",
             "|---:|---:|---:|:---:|:---:|"]
    for r in result["conditions"]:
        lo, hi = r["wilson_95"]
        lines.append(f'| {r["mutation"]:.2f} | {r["budget"]} | {r["successes"]}/{r["total"]} | {r["every_replicate_pass"]} | {lo:.3f} to {hi:.3f} |')
    lines.extend(["", f'All {result["raw_rows"]:,} compartment/passage records are retained in `raw.csv`; per-seed metrics, individual gates and paired differences are in `results.json`. Runtime: {result["elapsed_seconds"]:.2f} seconds.', "",
        "All active controls matched F/N counts exactly in every compartment/passage. Every material balance was zero; synthesis cost and finite reporter fuel constraints passed. Founder activity was absent after the ideal purge. The no-synthesis arm had zero catalysts and activity after purge.", "",
        "The strict all-seeds criterion is evaluated independently in each frozen grid cell; a failure is preserved. Wilson intervals describe seed-level variability, not physical replication. There is no test-set optimization, evolutionary selection or evidence of autonomous life/intelligence.", "",
        "Limits: copying, catalytic specificity and selective founder purge are supplied rules. Synthesis and assay fuels are bookkeeping resources, with no thermodynamic calibration. New-material activity is an exact simulator attribution, not experimentally measured material-specific activity. The exchange control is whole-population pooling with exact recipient counts. Physical feasibility and a mechanism that discovers copying remain untested.", ""])
    (output/"REPORT.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output directory; existing paths are refused.")
    args = parser.parse_args()
    config = json.loads((HERE/"config.json").read_text())
    result = run(config, args.output)
    print(json.dumps(dict(status=result["status"], raw_rows=result["raw_rows"], elapsed_seconds=result["elapsed_seconds"],
                          every_replicate_cells=sum(r["every_replicate_pass"] for r in result["conditions"]))))


if __name__ == "__main__":
    main()
