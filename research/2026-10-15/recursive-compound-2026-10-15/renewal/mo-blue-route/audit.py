import hashlib
import json
from decimal import Decimal
from pathlib import Path

BASE = Path(__file__).resolve().parent
PDF = BASE / "raw/ja3c09344_si_001.pdf"
SHA256 = "693c8723f09a0d9c4bb96131c60172f575c21c986047556637cbcdd2e53d64fa"


def implied_molar_mass(mass_g, acid_mL, acid_M, stated_H_Mo):
    values = [Decimal(str(x)) for x in (mass_g, acid_mL, acid_M, stated_H_Mo)]
    if not all(x.is_finite() and x > 0 for x in values):
        raise ValueError("Positive finite recipe quantities required")
    mass, volume, concentration, ratio = values
    return ratio * mass / (2 * volume / 1000 * concentration)


def main():
    data = PDF.read_bytes()
    if len(data) != 8385595 or hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError("Acquired supplement differs from pinned primary source")
    pairs = [("3.90", "1.25"), ("4.68", "1.5"), ("6.25", "2"),
             ("10.90", "3.5"), ("12.50", "4")]
    rows = [{"H2SO4_volume_mL": float(volume), "stated_nominal_H_per_Mo": float(ratio),
             "implied_Na2MoO4_formula_unit_mass_g_mol": float(implied_molar_mass(15, volume, 1, ratio))}
            for volume, ratio in pairs]
    result = {
        "status": "SOURCE_METHOD_CONSTRAINTS_ONLY",
        "source_doi": "10.1021/jacs.3c09344.s001", "source_sha256": SHA256,
        "source_scope": "Acquired supporting information only; main article not acquired",
        "nominal_control_recipe": {"page": 8, "solution_volume_mL": 15,
            "printed_Na2MoO4_g_mL": 1, "printed_H2SO4_M": 1,
            "H_equivalents_per_H2SO4_assumed_for_nominal_ratio": 2, "rows": rows,
            "recipe_consistency_resolved": False,
            "interpretation": "Printed quantities imply about 2400 g/mol per Mo-containing formula unit. Ordinary anhydrous sodium molybdate or its dihydrate do not reconcile this; no source typo or hydration state is silently corrected."},
        "raman_normalization": {"page": 9, "each_species_own_maximum_percent": 100,
            "cross_species_response_calibration_supplied": False,
            "absolute_species_mass_balance_identified": False,
            "sampling_side": "UNRESOLVED: page8 says anolyte connection and cathode electrolytes"},
        "ESI_sampling": {"page": 9, "sample_to_acetonitrile_volume_ratio": [1, 39],
            "maximum_reported_standing_before_dilution_minutes": 30,
            "total_scan_completion_delay_minutes": None,
            "Mo36_route_sample_times_seconds": [0, 280, 2000, 4000, 6000],
            "unperturbed_operando_solution_identity_established": False},
        "source_apparatus": {"pages": [5, 7, 8], "carbon_paper_electrodes": True,
            "Nafion_115_membrane": True, "IrO2_oxygen_evolution_catalyst": True,
            "externally_supplied_flow_mL_min": 112, "applied_current_density_mA_cm2": 2.5,
            "geometric_electrode_area_cm2": 4},
        "target_renewal_verified": False, "functional_inheritance_verified": False,
        "new_candidate_role": False, "experimental_holdout": False,
        "new_fitted_models": 0, "new_physical_experiments": 0,
        "limits": ["No raw spectral time series acquired.",
                   "Species-specific normalized Raman areas cannot be summed as concentrations.",
                   "Precursor deassembly and formation of different clusters do not establish original target repair."]}
    (BASE / "analysis.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "recipe_rows": len(rows),
                      "implied_mass_range_g_mol": [min(r["implied_Na2MoO4_formula_unit_mass_g_mol"] for r in rows),
                                                   max(r["implied_Na2MoO4_formula_unit_mass_g_mol"] for r in rows)],
                      "target_admitted": False}))


if __name__ == "__main__":
    main()
