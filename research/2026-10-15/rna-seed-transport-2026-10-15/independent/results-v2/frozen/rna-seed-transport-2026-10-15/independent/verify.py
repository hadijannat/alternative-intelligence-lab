"""Independent DOP853 oracles for the frozen seed-transport comparison."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
LAB = HERE.parent
ROOT = LAB.parent
SPECIES = ("A", "R", "B", "F", "P", "D", "H")
MOIETIES = np.array([
    [1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0],
], dtype=float)
CHEMISTRY_PATH = ROOT / "rna-turnover-tests-2026-10-15/results-v1/full_fits.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def write_csv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def permeability(nu):
    return -math.log(0.55 - 0.45 / nu) / (3 * (1 + 1 / nu))


def transport_oracle(inside, exterior, weights, nu, duration, exchange=None):
    """Directly integrate coupled concentrations, without a spectral solution."""
    n = len(weights)
    inside = np.asarray(inside, dtype=float)
    exterior = np.asarray(exterior, dtype=float)
    kappa = permeability(nu)
    bath = exchange is None
    initial = np.concatenate((inside.ravel(), exterior.ravel()))

    def rhs(_time, state):
        local = state[:n * 7].reshape(n, 7)
        outside = state[n * 7:].reshape((-1, 7))
        incoming = kappa * (outside - local)
        if bath:
            outgoing = -(weights @ incoming)[None, :] / nu
        else:
            outgoing = -incoming / nu + exchange * (weights @ outside - outside)
        return np.concatenate((incoming.ravel(), outgoing.ravel()))

    if duration == 0:
        return inside.copy(), exterior.copy()
    solution = solve_ivp(rhs, (0, duration), initial, method="DOP853", rtol=1e-11,
                         atol=1e-13, max_step=0.1)
    if not solution.success:
        raise RuntimeError(solution.message)
    final = solution.y[:, -1]
    return final[:n * 7].reshape(n, 7), final[n * 7:].reshape(exterior.shape)


def reaction_oracle(states, parameters, duration=60):
    shape = states.shape

    def rhs(_time, values):
        y = values.reshape(shape)
        a, r, b, f, _p, _d, h = y.T
        occupancy = b / (parameters["kb"] + b)
        active = parameters["ka"] * f * a * occupancy
        reporter = parameters["kf"] * f * r * occupancy
        spontaneous = parameters["kh"] * a * a * occupancy * occupancy
        background_reporter = parameters["krh"] * a * r * occupancy * occupancy
        da = active + spontaneous
        dr = reporter + background_reporter
        decay = parameters["kd"] * f
        return np.column_stack((-da, -dr, -da - dr, da - decay,
                                dr, decay, -parameters["kd"] * h)).ravel()

    solution = solve_ivp(rhs, (0, duration), states.ravel(), method="DOP853",
                         rtol=1e-11, atol=1e-13, max_step=0.5)
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[:, -1].reshape(shape)


def initial_oracle(seed, patch):
    inside = np.zeros((3, 7))
    inside[0, [3, 6]] = seed
    inside[1, [0, 1]] = [10, 2.5]
    inside[2, 2] = 15
    weights = np.full(3, 1 / 3)
    exterior = np.zeros((3 if patch else 1, 7))
    return inside, exterior, weights


def feed_oracle(inside, exterior, weights, carry, patch):
    external_mean = weights @ exterior if patch else exterior[0]
    feed = np.zeros((2, 7))
    feed[0, [0, 1]] = [10, 2.5]
    feed[1, 2] = 15
    next_weights = np.concatenate((weights / 2, [0.25, 0.25]))
    next_inside = np.vstack((inside, feed))
    outside = external_mean / 2 if carry else np.zeros(7)
    next_exterior = np.tile(outside, (len(next_weights) if patch else 1, 1))
    return next_inside, next_exterior, next_weights


def warm_oracle(inside, exterior, weights, parameters, reactive, patch):
    external_mean = weights @ exterior if patch else exterior[0]
    next_inside = reaction_oracle(inside, parameters)
    outside = reaction_oracle(external_mean[None, :], parameters)[0] if reactive else external_mean
    return next_inside, np.tile(outside, (len(weights) if patch else 1, 1))


def page_oracle(inside, weights):
    mean = weights @ inside
    return 100 * mean[4] / (mean[1] + mean[4])


def inventory(inside, exterior, weights, nu):
    exterior_mean = exterior[0] if len(exterior) == 1 else weights @ exterior
    return weights @ inside + nu * exterior_mean


def load_model():
    spec = importlib.util.spec_from_file_location("seed_transport_production", LAB / "model.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def serial_oracle(seed, family, params, parameters, reactive, carry):
    patch = family == "patch"
    nu = params["nu"]
    inside, exterior, weights = initial_oracle(seed, patch)
    source = weights @ inside
    removed, transfer_removed, discarded = (np.zeros(7) for _ in range(3))
    stages = []
    worst_tag_excess = 0.0
    smallest_state = 0.0

    def record(generation, stage, production=(0, 0)):
        nonlocal worst_tag_excess, smallest_state
        mean = weights @ inside
        outside_concentration = weights @ exterior if patch else exterior[0]
        outside_amount = nu * outside_concentration
        row = {"generation": generation, "stage": stage, "cohorts": len(weights),
               "yield_percent": page_oracle(inside, weights),
               "reporter_denominator_inside_uM": mean[1] + mean[4],
               "competent_inside_uM": mean[3], "competent_outside_uM": outside_amount[3],
               "founder_inside_uM": mean[6], "founder_outside_uM": outside_amount[6],
               "newly_generated_competent_inside_uM": mean[3] - mean[6],
               "newly_generated_competent_outside_uM": outside_amount[3] - outside_amount[6],
               "new_reporter_inside_uM": production[0], "new_reporter_outside_uM": production[1]}
        values = (("inside", mean), ("outside", outside_amount),
                  ("outside_concentration", outside_concentration), ("source", source),
                  ("removed", removed), ("transfer_removed", transfer_removed),
                  ("discarded", discarded))
        for label, value in values:
            row.update({f"{label}_{name}_uM": float(number) for name, number in zip(SPECIES, value)})
        stages.append(row)
        worst_tag_excess = max(worst_tag_excess, float(np.max(inside[:, 6] - inside[:, 3])),
                              float(np.max(exterior[:, 6] - exterior[:, 3])))
        smallest_state = min(smallest_state, float(inside.min()), float(exterior.min()))

    record(0, "initial")
    for generation in range(1, 4):
        if generation > 1:
            lost = inventory(inside, exterior, weights, nu) / 2
            inside, exterior, weights = feed_oracle(inside, exterior, weights, True, patch)
            removed += lost
            transfer_removed += lost
            source += np.array([2.5, 0.625, 3.75, 0, 0, 0, 0])
            record(generation, "feed")
        inside, exterior = transport_oracle(inside, exterior, weights, nu, 3,
                                            params.get("diffusion"))
        record(generation, "exchange")
        if patch:
            exterior = np.tile(weights @ exterior, (len(weights), 1))
        record(generation, "warm_start")
        before = inventory(inside, exterior, weights, nu)
        before_inside = weights @ inside
        before_outside = before - before_inside
        inside, exterior = warm_oracle(inside, exterior, weights, parameters, reactive, patch)
        after_inside = weights @ inside
        after_outside = inventory(inside, exterior, weights, nu) - after_inside
        record(generation, "measurement", (after_inside[4] - before_inside[4],
                                             after_outside[4] - before_outside[4]))
        if not carry:
            lost = nu * (weights @ exterior if patch else exterior[0])
            discarded += lost
            removed += lost
            exterior = np.zeros_like(exterior)
            record(generation, "discard")
    return stages, worst_tag_excess, smallest_state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    files = [Path(__file__), HERE / "PROTOCOL.md", LAB / "model.py", CHEMISTRY_PATH]
    hashes = {str(path.relative_to(ROOT)): sha(path) for path in files}
    parameters = json.loads(CHEMISTRY_PATH.read_text())["baseline"]["parameters"]
    model = load_model()
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    inside = np.array([[8, 2, 0, 1, 0.1, 0.2, 0.7], [0, 0, 14, 0.1, 0.3, 0.05, 0.06],
                       [1, 0.1, 3, 0.9, 0.5, 0.3, 0.8], [0.2, 1.1, 9, 0.4, 0.8, 0.1, 0.2]])
    preloaded = np.array([[0.2, 0.7, 1, 0.8, 0.3, 0.2, 0.4], [0.4, 0.2, 2, 0.3, 0.1, 0.6, 0.1],
                          [0.1, 0.4, 4, 0.9, 0.2, 0.1, 0.6], [0.8, 0.6, 1, 0.2, 0.7, 0.3, 0.01]])
    inputs = {"weights": weights.tolist(), "inside": inside.tolist(), "preloaded": preloaded.tolist(),
              "nu": [1, 3, 30], "diffusion": [0.001, 0.1, 10], "cycles": [1, 3],
              "serial_parameters": {"bath": {"nu": 3}, "patch": {"nu": 3, "diffusion": 0.1}},
              "serial_seeds": [0, 1, 2], "serial_generations": 3,
              "chemistry": {name: parameters[name] for name in model.CHEMISTRY}}
    write_json(args.output / "inputs.json", inputs)
    checks, transport_rows, serial_rows = [], [], []

    def check(name, error, tolerance):
        checks.append({"check": name, "value": float(error), "tolerance": float(tolerance),
                       "pass": bool(np.isfinite(error) and abs(error) <= tolerance)})

    check("frozen_chemistry_constants", max(abs(model.CHEMISTRY[k] - parameters[k]) for k in model.CHEMISTRY), 0)
    for family in ("bath", "patch"):
        for nu in inputs["nu"]:
            check(f"{family}_permeability_{nu}", model.permeability(nu) - permeability(nu), 1e-14)
            for diffusion in (inputs["diffusion"] if family == "patch" else [None]):
                params = {"nu": nu}
                if diffusion is not None:
                    params["diffusion"] = diffusion
                for loading in ("empty", "preloaded"):
                    exterior = np.zeros_like(inside) if loading == "empty" else preloaded.copy()
                    if family == "bath":
                        exterior[:] = weights @ exterior
                    for cycles in inputs["cycles"]:
                        case = f"{family}_nu{nu}_D{diffusion}_{loading}_FT{cycles}"
                        oracle_exterior = exterior if family == "patch" else exterior[:1]
                        expected_x, expected_e = transport_oracle(inside, oracle_exterior, weights,
                                                                  nu, cycles, diffusion)
                        if family == "bath":
                            expected_e = np.tile(expected_e, (len(weights), 1))
                        actual_x, actual_e, removed = model.exchange(inside, exterior, weights, family, params, cycles)
                        check(case + "_concentration", max(np.max(abs(actual_x - expected_x)),
                                                           np.max(abs(actual_e - expected_e))), 1e-9)
                        check(case + "_conservation", np.max(abs(inventory(actual_x, actual_e, weights, nu)
                                                                - inventory(inside, exterior, weights, nu))), 1e-9)
                        check(case + "_removed", np.max(abs(removed)), 0)
                        for location, expected, actual in (("inside", expected_x, actual_x),
                                                          ("outside", expected_e, actual_e)):
                            for cohort in range(len(weights)):
                                for j, species in enumerate(SPECIES):
                                    transport_rows.append({"case": case, "location": location,
                                        "cohort": cohort, "species": species,
                                        "expected_uM": float(expected[cohort, j]),
                                        "actual_uM": float(actual[cohort, j]),
                                        "absolute_error_uM": float(abs(actual[cohort, j] - expected[cohort, j]))})

    for family, params in inputs["serial_parameters"].items():
        nu = params["nu"]
        outside = preloaded.copy()
        if family == "bath":
            outside[:] = weights @ outside
        x0, e0, _ = model.exchange(inside, outside, weights, family, params, 0)
        check(f"{family}_zero_duration", max(np.max(abs(x0-inside)), np.max(abs(e0-outside))), 0)
        x0, e0, _ = model.exchange(inside, outside, weights, family, params, 3, kappa_override=0)
        check(f"{family}_zero_membrane_permeability", np.max(abs(x0-inside)), 1e-12)
        direct_x, direct_e, _ = model.exchange(inside, outside, weights, family, params, 3)
        split_x, split_e = inside.copy(), outside.copy()
        for _ in range(3):
            split_x, split_e, _ = model.exchange(split_x, split_e, weights, family, params, 1)
        check(f"{family}_unwashed_FT_semigroup", max(np.max(abs(split_x-direct_x)), np.max(abs(split_e-direct_e))), 1e-10)
        tracer = np.tile(np.array([1, 0, 0, 0, 0, 0, 0]), (len(weights), 1))
        tracer_x, _, _ = model.exchange(tracer, np.zeros_like(tracer), weights, family, params, 3)
        check(f"{family}_retention_anchor", float(weights @ tracer_x[:, 0]) - 0.55, 1e-12)
        uptake_x, _, _ = model.exchange(np.zeros_like(tracer), tracer, weights, family, params, 1)
        check(f"{family}_reuptake", 0 if float(weights @ uptake_x[:, 0]) > 0 else 1, 0)
        old_x, old_e, old_w = inside.copy(), outside.copy(), weights.copy()
        observed = model.reporter(inside, weights)
        check(f"{family}_PAGE", observed - page_oracle(inside, weights), 1e-12)
        check(f"{family}_observer_purity", max(np.max(abs(inside-old_x)), np.max(abs(outside-old_e)),
                                               np.max(abs(weights-old_w))), 0)
        fed_x, fed_e, fed_w, removed, added = model.feed(inside, outside, weights, nu)
        ref_x, ref_e, ref_w = feed_oracle(inside, outside if family == "patch" else outside[:1],
                                         weights, True, family == "patch")
        if family == "bath":
            ref_e = np.tile(ref_e, (len(ref_w), 1))
        check(f"{family}_feed_states", max(np.max(abs(fed_x-ref_x)), np.max(abs(fed_e-ref_e)),
                                          np.max(abs(fed_w-ref_w))), 1e-12)
        check(f"{family}_feed_ledger", np.max(abs(inventory(fed_x, fed_e, fed_w, nu) + removed
                                                  - inventory(inside, outside, weights, nu) - added)), 1e-12)
        for reactive in (False, True):
            for carry in (False, True):
                for seed in inputs["serial_seeds"]:
                    case = f"{family}_reactive{reactive}_carry{carry}_seed{seed}"
                    expected, tag_excess, minimum_state = serial_oracle(seed, family, params, parameters, reactive, carry)
                    _rows, actual = model.serial(seed, family, params, generations=3,
                        exterior_reactive=reactive, exterior_carried=carry, return_stages=True)
                    check(case + "_stage_count", len(actual)-len(expected), 0)
                    check(case + "_founder_subset", tag_excess, 1e-10)
                    check(case + "_nonnegative", minimum_state, 1e-10)
                    for reference, result in zip(expected, actual):
                        identity = reference["generation"] == result["generation"] and reference["stage"] == result["stage"]
                        check(case + f"_g{reference['generation']}_{reference['stage']}_identity", int(not identity), 0)
                        for key, value in reference.items():
                            if key in ("generation", "stage"):
                                continue
                            error = abs(result[key] - value)
                            tolerance = 1e-4 if key == "yield_percent" else 1e-6
                            serial_rows.append({"case": case, "generation": reference["generation"],
                                "stage": reference["stage"], "quantity": key, "expected": float(value),
                                "actual": float(result[key]), "absolute_error": float(error),
                                "tolerance": tolerance, "pass": bool(error <= tolerance)})
                    check(case + "_production_moiety_balance", max(row["moiety_balance_max_error_uM"] for row in actual), 1e-8)

    isolated_x, isolated_e, _ = model.exchange(inside, preloaded, weights, "patch", {"nu": 3, "diffusion": 0}, 3)
    check("isolated_patch_each_inventory", np.max(abs(isolated_x + 3*isolated_e - inside - 3*preloaded)), 1e-10)
    common = np.tile(weights @ preloaded, (len(weights), 1))
    bath_x, bath_e, _ = model.exchange(inside, common, weights, "bath", {"nu": 3}, 3)
    limit_errors = []
    for diffusion in (100, 1000, 10000):
        patch_x, patch_e, _ = model.exchange(inside, common, weights, "patch", {"nu": 3, "diffusion": diffusion}, 3)
        limit_errors.append(float(max(np.max(abs(patch_x-bath_x)), np.max(abs(patch_e-bath_e)))))
    check("patch_to_bath_limit_decreasing", 0 if all(a > b for a, b in zip(limit_errors, limit_errors[1:])) else 1, 0)
    check("patch_to_bath_limit_terminal", limit_errors[-1], 0.005)
    reacted = model.react(inside)
    expected_reacted = reaction_oracle(inside, parameters)
    check("independent_warm_chemistry", np.max(abs(reacted-expected_reacted)), 1e-6)
    check("warm_chemical_moieties", np.max(abs((reacted-inside) @ MOIETIES.T)), 1e-8)
    check("founder_decay", np.max(abs(reacted[:, 6] - inside[:, 6]*math.exp(-parameters["kd"]*60))), 1e-13)
    check("founder_subset_after_warm", max(0, np.max(reacted[:, 6]-reacted[:, 3])), 1e-10)
    for path in files:
        check("unchanged_" + str(path.relative_to(ROOT)), 0 if hashes[str(path.relative_to(ROOT))] == sha(path) else 1, 0)
    write_csv(args.output / "transport_comparisons.csv", transport_rows)
    write_csv(args.output / "serial_comparisons.csv", serial_rows)
    write_json(args.output / "source_hashes.json", hashes)
    result = {"status": "PASS" if all(c["pass"] for c in checks) and all(r["pass"] for r in serial_rows) else "FAIL",
              "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "checks": checks, "transport_scalar_comparisons": len(transport_rows),
              "serial_scalar_comparisons": len(serial_rows), "serial_paths": 24,
              "max_transport_error_uM": max(r["absolute_error_uM"] for r in transport_rows),
              "max_serial_inventory_error_uM": max(r["absolute_error"] for r in serial_rows if r["quantity"] != "yield_percent"),
              "max_serial_PAGE_error_pp": max(r["absolute_error"] for r in serial_rows if r["quantity"] == "yield_percent"),
              "patch_to_bath_limit_errors_uM": limit_errors,
              "failed_serial_comparisons": sum(not r["pass"] for r in serial_rows),
              "failed_checks": [c["check"] for c in checks if not c["pass"]],
              "limits": "Synthetic numerical verification; no measured fitting or physical validation."}
    write_json(args.output / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k not in ("checks",)}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
