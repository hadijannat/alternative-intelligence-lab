"""Fixed-parameter interventions; no fits or changes to previous laboratories."""
import csv
from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PREVIOUS = ROOT / "rna-turnover-tests-2026-10-15"
spec = importlib.util.spec_from_file_location("old_turnover", PREVIOUS / "model.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
CASES = {
    "reference": {},
    "zero_competence_loss": {"kd": 0.},
    "perfect_material_retention": {"retention_f": 1., "retention_fragments": 1.},
    "zero_competence_and_material_loss": {"kd": 0., "retention_f": 1., "retention_fragments": 1.},
    "no_transfer_no_feed": {},
    "no_background": {"kh": 0., "krh": 0.},
    "no_unseeded_active_initiation": {"kh": 0.},
    "no_direct_background_reporter": {"krh": 0.},
    "no_regeneration": {},
    "empty_volume_feed": {},
    "complete_mixing": {"mixing": 1.},
    "stop_mixing_after_g1": {},
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def simulate(p, seed, case, rtol):
    p = replace(p, **CASES[case])
    x, w = m.initial(seed, p)
    source, removed = w @ x, np.zeros(len(m.NAMES))
    founder = seed / 3
    rows = []

    def record(g, stage):
        inventory = w @ x
        competent = float(m.competent_inventory(inventory))
        moieties = m.MOIETIES @ np.stack((source, removed, inventory)).T
        balance = float(np.max(np.abs(moieties[:, 0]-moieties[:, 1]-moieties[:, 2])))
        assert balance < 1e-7, (case, seed, g, stage, balance)
        assert competent >= founder - 1e-7
        rows.append({"generation": g, "stage": stage, "seed_uM": seed,
                     "yield_percent": m.reporter(x, w),
                     **{name+"_uM": float(v) for name, v in zip(m.NAMES, inventory)},
                     "competent_uM": competent, "competent_founder_uM": founder,
                     "newly_generated_competent_uM": max(0., competent-founder),
                     "reporter_product_uM": float(m.reporter_product(inventory)),
                     "local_free_F_variance": float(w @ (x[:, 3]-inventory[3])**2),
                     "local_A_B_covariance": float(w @ ((x[:, 0]-inventory[0])*(x[:, 2]-inventory[2]))),
                     "moiety_balance_max_error_uM": balance,
                     **{f"{kind}_moiety_{i}_uM": float(moieties[i, j])
                        for j, kind in enumerate(("source", "removed", "retained")) for i in range(3)}})

    record(0, "initial")
    for g in range(1, 8):
        if g > 1 and case != "no_transfer_no_feed":
            removed += .5*(w @ x)
            w *= .5
            founder *= .5
            fresh = m.fresh(p) if case != "empty_volume_feed" else np.zeros((2, len(m.NAMES)))
            source += .25*fresh.sum(axis=0)
            x, w = np.vstack((x, fresh)), np.r_[w, .25, .25]
        record(g, "after_feed")
        exchange_p = replace(p, mixing=0.) if case == "stop_mixing_after_g1" and g > 1 else p
        x, w, lost = m.exchange(x, w, exchange_p, 3)
        removed += lost
        founder *= p.retention_f
        record(g, "after_exchange")
        x = m.react(x, 60, p, regeneration=case != "no_regeneration", rtol=rtol)
        founder *= np.exp(-60*p.kd)
        record(g, "after_reaction")
    return rows


def main():
    inputs = [PREVIOUS / "model.py", PREVIOUS / "results-v1/transport.json",
              PREVIOUS / "results-v1/transport_predictions.csv", PREVIOUS / "results-v1/full_fits.json",
              ROOT / "measured-coupling-2026-10-15/rna_sources/observations.csv",
              ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi.txt",
              ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt",
              ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi_data.xlsx",
              HERE / "PROTOCOL.md", Path(__file__)]
    hashes = {str(path.relative_to(ROOT)): digest(path) for path in inputs}
    (HERE / "input_hashes.json").write_text(json.dumps(hashes, indent=2)+"\n")
    transport = json.loads((PREVIOUS / "results-v1/transport.json").read_text())
    rows, tighter_rows, summaries = [], [], []
    maximum_reference_error, maximum_refinement_pp, maximum_refinement_uM = 0., 0., 0.
    for family in ("baseline", "release"):
        p = m.Parameters(**transport[f"{family}|fractional|uniform|reset-0"]["parameters"])
        for case in CASES:
            runs = {}
            for seed in (0., 1., 2.):
                run = simulate(p, seed, case, 1e-8)
                tight = simulate(p, seed, case, 1e-10)
                runs[seed] = run
                for a, b in zip(run, tight):
                    maximum_refinement_pp = max(maximum_refinement_pp, abs(a["yield_percent"]-b["yield_percent"]))
                    for key in a:
                        if key.endswith("_uM"):
                            maximum_refinement_uM = max(maximum_refinement_uM, abs(a[key]-b[key]))
                    rows.append({"family": family, "intervention": case, **a})
                    tighter_rows.append({"family": family, "intervention": case, **b})
                if case == "reference":
                    old = m.serial(p, seed)
                    new = [r for r in run if r["stage"] in ("initial", "after_reaction")]
                    maximum_reference_error = max(maximum_reference_error, max(abs(a["yield_percent"]-b["yield_percent"]) for a,b in zip(old,new)))
                if case == "no_background" and seed == 0:
                    assert all(r["competent_uM"] == 0 and r["yield_percent"] == 0 for r in run)
                if case == "no_regeneration":
                    assert max(abs(r["competent_uM"]-r["competent_founder_uM"]) for r in run) < 1e-7
            for i, low in enumerate(runs[0.]):
                mid, high = runs[1.][i], runs[2.][i]
                summaries.append({"family": family, "intervention": case, "generation": low["generation"], "stage": low["stage"],
                                  **{f"seed_{j}_yield_percent": runs[float(j)][i]["yield_percent"] for j in range(3)},
                                  "seed2_minus_seed0_pp": high["yield_percent"]-low["yield_percent"],
                                  "seed1_minus_seed0_pp": mid["yield_percent"]-low["yield_percent"],
                                  "seed2_minus_seed0_competent_uM": high["competent_uM"]-low["competent_uM"],
                                  "seed2_founder_uM": high["competent_founder_uM"]})
        print(f"Finished {family}", flush=True)
    assert maximum_reference_error < 1e-7
    assert maximum_refinement_pp < 1e-4
    assert maximum_refinement_uM < 1e-7
    assert all(digest(ROOT / path) == value for path,value in hashes.items())
    write_csv(HERE / "stage_states.csv", rows)
    write_csv(HERE / "refined_stage_states.csv", tighter_rows)
    write_csv(HERE / "seed_contrasts.csv", summaries)
    operators = {}
    for family in ("baseline", "release"):
        p = m.Parameters(**transport[f"{family}|fractional|uniform|reset-0"]["parameters"])
        operators[family] = {
            "parameters": p.__dict__,
            "passive_competent_founder_multiplier_per_later_generation": .5*p.retention_f*np.exp(-60*p.kd),
            "passive_material_founder_multiplier_per_later_generation": .5*p.retention_f,
            "mixing_concentration_deviation_multiplier_per_three_FT": (1-p.mixing)**3,
            "mixing_variance_multiplier_per_three_FT": (1-p.mixing)**6,
            "mixing_and_uniform_retention_variance_multiplier_per_three_FT": p.retention_f**2*(1-p.mixing)**6,
            "founder_material_G7_seed2_uM": 2/3*p.retention_f**7*.5**6,
            "founder_competent_G7_seed2_uM": 2/3*p.retention_f**7*.5**6*np.exp(-420*p.kd),
        }
    (HERE / "operators.json").write_text(json.dumps(operators, indent=2)+"\n")
    verification = {"status": "PASS", "families": 2, "interventions_per_family": len(CASES),
                    "seeds": [0,1,2], "stage_rows": len(rows), "contrast_rows": len(summaries),
                    "runtime": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__},
                    "max_reference_yield_error_pp": maximum_reference_error,
                    "max_refinement_yield_error_pp": maximum_refinement_pp,
                    "max_refinement_inventory_error_uM": maximum_refinement_uM,
                    "max_moiety_balance_error_uM": max(r["moiety_balance_max_error_uM"] for r in rows),
                    "inputs_unchanged": True, "parameter_fits": 0,
                    "limitations": ["Counterfactual explanatory audit, not held-out model validation", "Reuse of prior chemistry implementation, not an independent solver"]}
    (HERE / "verification.json").write_text(json.dumps(verification, indent=2)+"\n")
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
