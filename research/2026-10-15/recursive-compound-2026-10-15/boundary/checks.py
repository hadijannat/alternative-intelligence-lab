import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    candidates = json.loads((HERE / "candidates.json").read_text())
    sources = json.loads((HERE / "sources.json").read_text())
    assert len(candidates) == 5
    assert [c["order"] for c in candidates] == list(range(1, 6))
    assert len({c["id"] for c in candidates}) == 5
    ids = {s["id"] for s in sources}
    for c in candidates:
        assert not c["verified_complement"]
        for field in ("actual_finding", "limits", "disposition", "next_alternative", "carbon_status"):
            assert c[field]
        assert set(c["sources"]) <= ids
    for s in sources:
        assert (HERE / s["artifact"]).stat().st_size > 0
    acquisition = json.loads((HERE / "raw/acquisition.json").read_text())
    for entry in acquisition:
        if "sha256" in entry:
            data = (HERE / "raw" / entry["file"]).read_bytes()
            assert len(data) == entry["bytes"]
            assert hashlib.sha256(data).hexdigest() == entry["sha256"]

    zr_kinetic_ceiling = 100 * 0.010 / 0.050
    assert zr_kinetic_ceiling == 20
    zr_points = []
    for concentration, capacity in [(50, 7), (700, 51)]:
        feed = concentration * 0.010
        retained = capacity * 0.050
        assert 0 <= retained <= feed
        zr_points.append({"feed_mg_per_L": concentration, "reported_q_mg_per_g": capacity,
                          "feed_mg": feed, "retained_mg": retained,
                          "removal_fraction_derived": retained / feed})
    goethite_inventory = [10 / 5, 100 / 5]
    assert goethite_inventory == [2, 20]

    species = {
        "MoO4": {"Mo": 1, "O": 4, "q": -2}, "H+": {"H": 1, "q": 1},
        "Mo36": {"Mo": 36, "O": 128, "H": 32, "q": -8},
        "H2O": {"H": 2, "O": 1}, "FeOOH": {"Fe": 1, "O": 2, "H": 1},
        "Fe3+": {"Fe": 1, "q": 3}, "FeS": {"Fe": 1, "S": 1},
        "Fe2+": {"Fe": 1, "q": 2}, "H2S": {"H": 2, "S": 1},
        "Si(OH)4": {"Si": 1, "O": 4, "H": 4}, "SiO2": {"Si": 1, "O": 2}}
    reactions = [
        {"36 MoO4 + 64 H+ -> Mo36 + 16 H2O": {"MoO4": -36, "H+": -64, "Mo36": 1, "H2O": 16}},
        {"FeOOH + 3 H+ -> Fe3+ + 2 H2O": {"FeOOH": -1, "H+": -3, "Fe3+": 1, "H2O": 2}},
        {"FeS + 2 H+ -> Fe2+ + H2S": {"FeS": -1, "H+": -2, "Fe2+": 1, "H2S": 1}},
        {"Si(OH)4 -> SiO2 + 2 H2O": {"Si(OH)4": -1, "SiO2": 1, "H2O": 2}}]
    residuals = []
    for reaction in reactions:
        name, coefficients = next(iter(reaction.items()))
        residual = {e: sum(n * species[s].get(e, 0) for s, n in coefficients.items())
                    for e in ("Mo", "H", "O", "Fe", "S", "Si", "q")}
        assert all(v == 0 for v in residual.values())
        residuals.append({"formal_reaction": name, "residuals": residual})

    normalized_Mo_inventory = 36
    compatible_cluster_counts = [0, 1]
    assert all(36 * n <= normalized_Mo_inventory for n in compatible_cluster_counts)

    prior_files = [
        "discovery-loop/experiments/mo36-interface-resume-2026-10-13/REPORT.md",
        "discovery-loop/experiments/mo36-interface-resume-2026-10-13/encounter/model.py",
        "discovery-loop/experiments/mo36-feiii-clogging-v1/protocol.json",
        "discovery-loop/experiments/mo36-feiii-clogging-v1/model.py",
        "noncarbon-discovery-2026-10-15/research/compartments/REPORT.md",
        "noncarbon-discovery-2026-10-15/research/critical/REPORT.md",
        "noncarbon-discovery-2026-10-15/research/redox_compatibility/REPORT.md"]
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in prior_files}
    report = {
        "status": "PASS_ACCOUNTING_ONLY", "physical_boundary_verified": False,
        "invocation": "python3 recursive-compound-2026-10-15/boundary/checks.py",
        "zirconia_100_mg_L_batch_inventory_ceiling_mg_g": zr_kinetic_ceiling,
        "zirconia_reported_points_with_derived_inventory": zr_points,
        "goethite_tested_feed_inventory_umol_Mo_per_g": goethite_inventory,
        "formal_reaction_checks": residuals,
        "elemental_retention_nonidentifiability": {"normalized_Mo_atoms": 36, "possible_intact_Mo36_counts": compatible_cluster_counts,
            "meaning": "Both zero intact clusters and one intact cluster satisfy the same total Mo inventory. This is an algebraic counterexample, not measured speciation."},
        "candidate_count": 5, "verified_complements": 0,
        "prior_artifacts_read_sha256": hashes,
        "not_run": ["wet chemistry", "old model reruns", "parameter fitting", "DFT", "permeability prediction"],
        "limit": "Inventory and formal charge/atom checks establish no direction, rate, stability, active fraction or life."}
    destination = HERE / ".omo/evidence/checks.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "artifact": str(destination), "verified_complements": 0}))


if __name__ == "__main__":
    main()
