"""Derive stage contrasts and current-generation production from saved diagnostics."""
import csv
import hashlib
import json
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    paths = [HERE / "stage_states.csv", ROOT / "rna-turnover-tests-2026-10-15/results-v1/transport_trajectories.json",
             ROOT / "measured-coupling-2026-10-15/rna_sources/observations.csv", Path(__file__)]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    states = list(csv.DictReader(paths[0].open()))
    keyed = {(r["family"], r["intervention"], int(r["generation"]), r["stage"], float(r["seed_uM"])): r for r in states}
    production, gains = [], []
    for family, case in sorted({(r["family"], r["intervention"]) for r in states}):
        for g in range(1, 8):
            for seed in (0., 1., 2.):
                pre = keyed[family, case, g, "after_exchange", seed]
                post = keyed[family, case, g, "after_reaction", seed]
                produced = float(post["reporter_product_uM"])-float(pre["reporter_product_uM"])
                total = float(post["reporter_product_uM"])+float(post["R_uM"])
                assert produced > -1e-8
                production.append({"family": family, "intervention": case, "generation": g, "seed_uM": seed,
                                   "reporter_inventory_uM": total, "inherited_reporter_product_uM": float(pre["reporter_product_uM"]),
                                   "new_reporter_product_this_generation_uM": produced,
                                   "new_reporter_product_this_generation_pp": 100*produced/total if total else 0.,
                                   "final_reporter_yield_percent": float(post["yield_percent"])})
            contrasts = {stage: float(keyed[family, case, g, stage, 2.]["competent_uM"])-float(keyed[family, case, g, stage, 0.]["competent_uM"])
                         for stage in ("after_feed", "after_exchange", "after_reaction")}
            gains.append({"family": family, "intervention": case, "generation": g, **{k+"_contrast_uM": v for k,v in contrasts.items()},
                          "reaction_contrast_multiplier": contrasts["after_reaction"]/contrasts["after_exchange"] if contrasts["after_exchange"] else "undefined"})
    previous = json.loads(paths[1].read_text())
    old_rows = []
    for scenario, runs in previous.items():
        for g in range(8):
            old_rows.append({"scenario": scenario, "generation": g,
                             **{f"seed_{seed}_yield_percent": runs[str(seed)][g]["yield_percent"] for seed in range(3)},
                             "seed2_minus_seed0_pp": runs["2"][g]["yield_percent"]-runs["0"][g]["yield_percent"]})
    observations = list(csv.DictReader(paths[2].open()))
    measured = []
    for g in range(8):
        grouped = [[float(r["value_percent"]) for r in observations if r["dataset"] == "Figure_3" and float(r["seed_uM"]) == seed and float(r["x"]) == g] for seed in range(3)]
        assert all(len(values) == 3 for values in grouped)
        means = list(map(statistics.mean, grouped))
        measured.append({"generation": g, **{f"seed_{seed}_yield_mean_percent": value for seed,value in enumerate(means)},
                         **{f"seed_{seed}_yield_sd_pp": statistics.stdev(values) for seed,values in enumerate(grouped)},
                         "seed2_minus_seed0_pp": means[2]-means[0]})
    write_csv("generation_production.csv", production)
    write_csv("reaction_contrast_gains.csv", gains)
    write_csv("previous_seed_contrasts.csv", old_rows)
    write_csv("observed_seed_contrasts.csv", measured)
    (HERE / "summary_hashes.json").write_text(json.dumps(hashes, indent=2)+"\n")
    print(f"Saved {len(production)} production, {len(gains)} contrast gain, {len(old_rows)} previous trajectory and {len(measured)} measured rows")


if __name__ == "__main__":
    main()
