import csv
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROTOCOL_SHA = "2cd0ed6c85574a924d6159323c2129e60f5c23985195c38bdd4ef747d11acab3"
F = D(96485)


def source_volume_ml(charge_c):
    if charge_c < 0:
        raise ValueError("Charge must be nonnegative")
    return charge_c / (2 * F) * 24000


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    assert hashlib.sha256((BASE/"PROTOCOL.md").read_bytes()).hexdigest() == PROTOCOL_SHA
    inventory = D("0.025") * D("0.5")
    q = D(47)
    capacity = 2 * F * inventory
    gas_ml = source_volume_ml(q)
    measured, uncertainty = D("6.0"), D("0.2")
    assert source_volume_ml(D(0)) == 0
    try:
        source_volume_ml(D(-1))
    except ValueError:
        pass
    else:
        raise AssertionError("Negative charge accepted")
    rows = []
    max_charge_residual = D(0)
    for phase in ("photocharge", "electrical_release"):
        for i in range(101):
            progress = D(i)/100
            q_in = q*progress if phase == "photocharge" else q
            q_out = D(0) if phase == "photocharge" else q*progress
            red = (q_in-q_out)/(2*F)
            ox = inventory-red
            h2 = q_out/(2*F)
            o2_equivalent = q_in/(4*F)
            residual = abs(2*F*red-q_in+q_out)
            max_charge_residual = max(max_charge_residual, residual)
            assert red >= 0 and ox >= 0 and abs(red+ox-inventory) < D("1e-25")
            assert abs(red+h2-2*o2_equivalent) < D("1e-25")
            rows.append(dict(phase=phase, charge_coordinate_fraction=str(progress),
                             charge_in_C=str(q_in), charge_out_C=str(q_out),
                             Ox_mol=str(ox), Red_mol=str(red),
                             ideal_H2_equivalent_mol=str(h2),
                             ideal_O2_equivalent_mol=str(o2_equivalent)))
    assert max_charge_residual < D("1e-20")
    assert rows[-1]["Red_mol"] == "0"
    scenario_q, assumed_i, optical_power, assumed_v = D(100), D("0.001"), D("0.1"), D("1.5")
    scenario_time = scenario_q/assumed_i
    solar_j = optical_power*scenario_time
    electrical_j = assumed_v*scenario_q
    hhv_j = scenario_q/(2*F)*286000
    source_sha = {name: hashlib.sha256((BASE/"sources"/name).read_bytes()).hexdigest()
                  for name in ("bloor2016.pdf", "bloor2016-si.pdf")}
    result = dict(
        status="SOURCE_CONSISTENCY_AND_IDEAL_CHARGE_COORDINATE_CHECKS_COMPLETE",
        protocol_sha256=PROTOCOL_SHA, primary_sha256=source_sha,
        analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        evidence_class="Already-inspected primary endpoints; no fitted kinetics or fresh held-out experiment",
        source_cycle=dict(nominal_inventory_mol=str(inventory), capacity_C=str(capacity),
                          reported_charge_C=str(q), reported_recovered_C=str(q),
                          capacity_fraction_accessed=str(q/capacity),
                          charge_predicted_H2_mL=str(gas_ml), measured_H2_mL=str(measured),
                          burette_uncertainty_mL=str(uncertainty),
                          prediction_within_reported_interval=bool(measured-uncertainty <= gas_ml <= measured+uncertainty),
                          central_measured_over_predicted=str(measured/gas_ml),
                          ratio_uncertainty_from_burette_only=str(uncertainty/gas_ml),
                          observed_same_cycle_O2_mol=None,
                          actual_complete_cycle_energy_J=None,
                          new_active_material_mol=None,
                          inherited_function=None),
        ideal_trajectory=dict(rows=len(rows), coordinate="fraction of stated charge endpoint, not elapsed time",
                              max_charge_residual_C=str(max_charge_residual),
                              assumption="Two-state competent inventory, all charge follows specified PCET; O2 equivalents are formal predictions, not measured gas for this cycle"),
        energy_estimate=dict(classification="SI-7 assumed scenario, not measured 47C cycle",
                             illustrative_charge_C=str(scenario_q), assumed_current_A=str(assumed_i),
                             implied_time_s=str(scenario_time), incident_optical_J=str(solar_j),
                             assumed_cell_discharge_V=str(assumed_v), electrical_release_J=str(electrical_j),
                             H2_HHV_J=str(hhv_j), HHV_over_total_input=str(hhv_j/(solar_j+electrical_j)),
                             excluded="Lamp wall-plug conversion, pumps, compressors, degassing and other balance of plant"),
        retained_negatives=[
            "Only 1.9485% of nominal inventory capacity is exercised; no depletion validation",
            "O2 assay used Pt mesh, unlike carbonfelt photocharge; its84+/-6% cannot be inserted as charge loss in this cycle",
            "Zero photocharging bias does not remove required electrical input in H2 release",
            "+0.75V versus Ag/AgCl is not a measured full-cell voltage integral",
            "No identified active-material replacement or inherited useful state",
            "Methanesulfonicacid, carbonfelt and Nafion are source dependencies; organic-free integrated organization is unproved",
            "No transfer of source properties to Mo34WV"
        ])
    out=BASE/"results"
    out.mkdir(exist_ok=True)
    (out/"analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    with (out/"charge_coordinate.csv").open("w",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"capacity_C":str(capacity), "capacity_fraction_accessed":str(q/capacity),
                      "predicted_H2_mL":str(gas_ml), "within_burette_interval":result["source_cycle"]["prediction_within_reported_interval"],
                      "scenario_HHV_efficiency":str(hhv_j/(solar_j+electrical_j)),
                      "max_charge_residual_C":str(max_charge_residual)},indent=2))


if __name__ == "__main__":
    main()
