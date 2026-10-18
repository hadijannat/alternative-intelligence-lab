import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    output = ROOT / "results/hou-stage-mapping.json"
    if output.exists():
        raise FileExistsError(output)
    original = ROOT / "results/hou-test.json"
    source = json.loads(original.read_text())
    if source["status"] != "ok" or len(source["efficiency"]) != 3:
        raise ValueError("Original complete FE calculation required")
    records = source["efficiency"]
    transitions = []
    for index in (0, 1):
        before = records[index]["healed_native"]
        after = records[index + 1]["original_native"]
        transitions.append(dict(transition=index + 1,
                                deactivated_row=(4, 7)[index], next_start_row=(6, 9)[index],
                                before_percent=before, after_percent=after,
                                next_start_deactivated_ratio=after / before,
                                difference_percentage_points=after - before))
    stages = [dict(cycle=i + 1, start_percent=r["original_native"],
                   after_ten_hours_percent=r["healed_native"],
                   within_cycle_fe_retention=r["healed_original_ratio"],
                   start_initial_start_ratio=r["original_native"] / records[0]["original_native"])
              for i, r in enumerate(records)]
    paths = ("results/hou-test.json", "STAGE_MAPPING_AMENDMENT.md",
             "sources/hou-fig5.png", "sources/figure5-acquisition.json", "reconcile_hou_stages.py")
    result = dict(status="posthoc_descriptive_stage_reconciliation",
                  original_frozen_fe_physical_pairing="incorrect_for_recovery; preserved",
                  original_result_unchanged=True, cycles=stages, displayed_recovery_arrows=transitions,
                  source_figure_units="FE of formate (%)", unobserved_third_recovery=None,
                  fitted_parameters=0, predictive_validation=False, full_integrated_requirements_closed=[],
                  provenance={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths})
    with output.open("x") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
