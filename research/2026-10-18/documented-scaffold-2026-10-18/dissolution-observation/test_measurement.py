from pathlib import Path
import hashlib
import json
import math
import traceback


BASE = Path(__file__).resolve().parent
RESULTS = BASE / "results"
INTERVALS_H = (1.0, 1.0, 1.0, 3.0)
WINDOW_S = 300.0
OPERATORS = ("unreplenished", "clean_replenishment", "complete_reset")
INPUTS = (
    "PROTOCOL.md",
    "test_measurement.py",
    "sources/cs-2026-01228g.pdf",
    "sources/cs-2026-01228g_si_001.docx",
)


def hashes():
    return {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
            for name in INPUTS}


def simulate(operator, flow_ul_s, volume_ml=50.0, source_units_h=1.0,
             initial_solid=10.0):
    if operator not in OPERATORS:
        raise ValueError("unknown sampling operator")
    if not all(math.isfinite(x) for x in
               (flow_ul_s, volume_ml, source_units_h, initial_solid)):
        raise ValueError("nonfinite input")
    if volume_ml <= 0 or min(flow_ul_s, source_units_h, initial_solid) < 0:
        raise ValueError("invalid volume, flow, source or initial pool")
    solid, liquid, exported = initial_solid, 0.0, 0.0
    volume, exported_volume, polarization_h, wall_h = volume_ml, 0.0, 0.0, 0.0
    records = []
    for interval_h in INTERVALS_H:
        released = min(solid, source_units_h * interval_h)
        solid -= released
        liquid += released
        polarization_h += interval_h
        wall_h += interval_h
        before, before_volume = liquid, volume
        nominal_withdrawal = flow_ul_s * WINDOW_S / 1000.0
        if operator == "unreplenished":
            if nominal_withdrawal >= volume:
                raise ValueError("unreplenished sampling would empty the liquid pool")
            collected = liquid * nominal_withdrawal / volume
            volume -= nominal_withdrawal
            removed_volume = nominal_withdrawal
        elif operator == "clean_replenishment":
            collected = liquid * -math.expm1(-nominal_withdrawal / volume)
            removed_volume = nominal_withdrawal
        else:
            # This comparison assumes full removal/refill, independent of q.
            collected = liquid
            removed_volume = volume
        liquid -= collected
        exported += collected
        exported_volume += removed_volume
        wall_h += WINDOW_S / 3600.0
        record = {
            "polarization_h": polarization_h,
            "sampling_start_wall_h": wall_h - WINDOW_S / 3600.0,
            "sampling_end_wall_h": wall_h,
            "released_this_interval_units": released,
            "solid_units": solid,
            "pre_liquid_units": before,
            "post_liquid_units": liquid,
            "pre_volume_ml": before_volume,
            "post_volume_ml": volume,
            "pre_concentration_units_ml": before / before_volume,
            "post_concentration_units_ml": liquid / volume,
            "exported_this_window_units": collected,
            "cumulative_exported_units": exported,
            "nominal_flow_volume_ml": nominal_withdrawal,
            "actual_exported_volume_this_window_ml": removed_volume,
            "cumulative_exported_volume_ml": exported_volume,
            "conservation_error_units": solid + liquid + exported - initial_solid,
        }
        assert min(solid, liquid, exported, volume) >= 0
        assert math.isclose(solid + liquid + exported, initial_solid,
                            abs_tol=1e-12, rel_tol=1e-12)
        records.append(record)
    return {"operator": operator, "flow_ul_s": flow_ul_s,
            "initial_volume_ml": volume_ml, "initial_solid_units": initial_solid,
            "source_units_h": source_units_h, "records": records}


def checks():
    for operator in OPERATORS:
        base = simulate(operator, 3.2)
        zero = simulate(operator, 3.2, source_units_h=0)
        assert all(r["post_liquid_units"] == r["cumulative_exported_units"] == 0
                   for r in zero["records"])
        exhausted = simulate(operator, 3.2, source_units_h=100)
        assert all(r["solid_units"] == 0 for r in exhausted["records"])
        scaled = simulate(operator, 3.2, source_units_h=7, initial_solid=70)
        for r, s in zip(base["records"], scaled["records"]):
            for field in ("solid_units", "pre_liquid_units", "post_liquid_units",
                          "cumulative_exported_units", "pre_concentration_units_ml",
                          "post_concentration_units_ml"):
                assert math.isclose(s[field], 7 * r[field], abs_tol=1e-12)
    for operator in OPERATORS[:2]:
        zero_flow = simulate(operator, 0)
        for r in zero_flow["records"]:
            assert r["cumulative_exported_units"] == 0
            assert r["post_volume_ml"] == 50
            assert r["post_liquid_units"] == r["polarization_h"]
        for q in (3.2, 3.5):
            for r in simulate(operator, q)["records"]:
                v, mass = r["pre_volume_ml"], r["pre_liquid_units"]
                fraction = q * WINDOW_S / 1000 / v
                expected = mass * (1 - fraction if operator == "unreplenished"
                                   else math.exp(-fraction))
                assert math.isclose(r["post_liquid_units"], expected, abs_tol=1e-12)
                if operator == "unreplenished":
                    assert math.isclose(r["pre_concentration_units_ml"],
                                        r["post_concentration_units_ml"], abs_tol=1e-12)
    reset = simulate("complete_reset", 0)
    assert all(r["post_liquid_units"] == 0 for r in reset["records"])
    assert reset["records"][-1]["cumulative_exported_units"] == 6
    assert reset["records"][-1]["cumulative_exported_volume_ml"] == 200
    assert math.isclose(reset["records"][-1]["sampling_end_wall_h"], 6 + 4 / 12)
    for q in (3.2, 3.5):
        r = simulate("clean_replenishment", q)["records"][0]
        assert r["post_liquid_units"] > 0.97 * r["pre_liquid_units"]
    try:
        simulate("unreplenished", 3.2, volume_ml=0.05)
    except ValueError:
        pass
    else:
        raise AssertionError("impossible unreplenished small-volume topology accepted")
    return {name: "PASS" for name in (
        "finite_nonnegative_conserved_pools", "finite_source_exhaustion",
        "zero_source", "zero_flow_physical_operators", "analytical_withdrawal",
        "linear_mass_scaling", "unreplenished_concentration_invariance",
        "reset_comparison_semantics", "polarization_vs_wall_time",
        "nominal_50ml_sampling_is_not_complete_reset",
        "invalid_unreplenished_small_volume_rejected")}


def main():
    RESULTS.mkdir(exist_ok=True)
    before = hashes()
    check_results = checks()
    scenarios = [simulate(operator, q) for q in (3.2, 3.5) for operator in OPERATORS]
    sensitivity = [simulate("clean_replenishment", q, volume_ml=0.05)
                   for q in (3.2, 3.5)]
    assert before == hashes(), "protocol, script or input changed during execution"
    check_results["input_hashes_unchanged"] = "PASS"
    result = {
        "evidence_class": "synthetic conditional measurement calculation",
        "chemistry_fitted": False, "held_out_validation": False,
        "active_repair_identified": False, "verified_complement_added": False,
        "input_sha256": before,
        "parameters": {"polarization_intervals_h": INTERVALS_H,
                       "sampling_window_s": WINDOW_S,
                       "ocp_source_units_h": 0,
                       "ocp_zero_source_is_unverified_assumption": True},
        "checks": check_results,
        "conditional_50ml_scenarios": scenarios,
        "hypothetical_50ul_fixed_volume_sensitivity": sensitivity,
        "limits": [
            "50 mL is documented total electrolyte, not verified well-mixed circulating volume.",
            "Clean replenishment and full reset are alternative assumptions.",
            "Full reset removes/refills 50 mL per window independently of nominal flow.",
            "50 microlitres is synthetic sensitivity, not the native volume.",
            "No redeposition, metal supply or repair is present; arbitrary source transfers from finite solid.",
            "Dissolved stock and exported mass differ; neither attributes catalytic function to new material.",
        ],
    }
    (RESULTS / "measurement.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": check_results, "scenarios": len(scenarios),
                      "sensitivity_scenarios": len(sensitivity),
                      "artifact": str(RESULTS / "measurement.json")}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        RESULTS.mkdir(exist_ok=True)
        with (RESULTS / "failures.log").open("a") as failure_log:
            traceback.print_exc(file=failure_log)
        raise
