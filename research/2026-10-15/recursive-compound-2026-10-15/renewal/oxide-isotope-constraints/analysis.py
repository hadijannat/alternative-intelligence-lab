import csv
import hashlib
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent
SI_SHA256 = "17f478c53e89545ccd211e828e1cad87856b4ea39d90fea62161811f19f5c5a0"
CSV_SHA256 = "e18d1342987db045916ab42fe7536dafb6f5d908c5a25b280f404769bc9f20c7"
SITES = "ABCDEFG"
FIELDS = ["row_id", "temperature_C", "pH", "concentration_mM", "log_base", "rate_unit"] + [
    f"{site}_{field}" for site in SITES for field in ("log_k", "uncertainty", "status")
]


def number(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Nonfinite measurement")
    return result


def load_rows(path):
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("Unexpected CSV schema")
        rows = list(reader)
    if len(rows) != 17:
        raise ValueError("Expected all 17 source rows")
    for index, row in enumerate(rows, 1):
        if set(row) != set(FIELDS) or None in row.values():
            raise ValueError("Malformed CSV row")
        if row["row_id"] != f"S3-{index:02d}":
            raise ValueError("Source row identity/order changed")
        if row["log_base"] != "10" or row["rate_unit"] != "s^-1":
            raise ValueError("Expected common log of rate in s^-1")
        temperature = number(row["temperature_C"])
        ph = number(row["pH"])
        if temperature not in (6.0, 35.5) or not 0 <= ph <= 14 or number(row["concentration_mM"]) <= 0:
            raise ValueError("Invalid experimental conditions")
        for site in SITES:
            k, uncertainty, status = (row[f"{site}_{field}"] for field in ("log_k", "uncertainty", "status"))
            fast = site == "D" and temperature == 35.5 and ph <= 7.5
            if fast != (status == "too_fast_no_numeric_bound"):
                raise ValueError("Acidic Site D censoring changed")
            if status == "reported":
                number(k)
                if number(uncertainty) < 0:
                    raise ValueError("Negative uncertainty")
            elif status in ("not_reported", "too_fast_no_numeric_bound"):
                if k != "" or uncertainty != "":
                    raise ValueError("Missing/censored entries must have blank numeric fields")
            else:
                raise ValueError("Unknown measurement status")
    return rows


def ratio(row, numerator, denominator):
    if any(row[f"{site}_status"] != "reported" for site in (numerator, denominator)):
        raise ValueError("A ratio requires two reported rates from the same row")
    delta = round(number(row[f"{numerator}_log_k"]) - number(row[f"{denominator}_log_k"]), 2)
    return {
        "row_id": row["row_id"], "temperature_C": number(row["temperature_C"]),
        "pH": number(row["pH"]), "concentration_mM": number(row["concentration_mM"]),
        "ratio": f"{numerator}/{denominator}", "reported_log_difference": delta,
        "conditional_point_ratio_if_base10": 10 ** delta,
        "denominator_endpoint": "molecular_transformation" if denominator == "A" else "oxygen_isotope_signal_exchange",
        "confidence_interval": None,
    }


def analyze(base=BASE):
    pdf = (base / "raw/ja905166c_si_001.pdf").read_bytes()
    if len(pdf) != 513814 or hashlib.sha256(pdf).hexdigest() != SI_SHA256:
        raise ValueError("Primary SI bytes changed")
    rows = load_rows(base / "rates.csv")
    csv_hash = hashlib.sha256((base / "rates.csv").read_bytes()).hexdigest()
    if csv_hash != CSV_SHA256:
        raise ValueError("Source transcription changed; re-audit against Table S-1-2")
    counts = {site: sum(row[f"{site}_status"] == "reported" for row in rows) for site in SITES}
    return {
        "status": "MEASUREMENT_CONSTRAINT_ONLY",
        "source": "10.1021/ja905166c.s001, Table S-1-2, PDF page S3",
        "source_sha256": SI_SHA256, "csv_sha256": csv_hash,
        "log_base": {"source_explicitly_defines_base": False, "arithmetic_assumption": 10, "primary_quantity": "difference of reported log rates", "fold_ratios": "conditional on conventional base-10 interpretation"},
        "row_count": len(rows), "site_cell_count": 7 * len(rows),
        "reported_rate_count": sum(counts.values()), "reported_rate_count_by_site": counts,
        "too_fast_without_numeric_bound_count": 3,
        "not_reported_count": 7 * len(rows) - sum(counts.values()) - 3,
        "site_endpoints": {site: "molecular_transformation" if site == "A" else "oxygen_isotope_signal_exchange" for site in SITES},
        "endpoint_caveat": "Acidic experiments also transform the molecule; other site signals do not independently prove intact-molecule exchange.",
        "F_over_A": [ratio(row, "F", "A") for row in rows if row["A_status"] == "reported"],
        "D_over_E": [ratio(row, "D", "E") for row in rows if row["row_id"] in ("S3-05", "S3-06")],
        "uncertainty": {
            "temperature_C": 0.2, "concentration_relative_percent": 1,
            "log_rate_uncertainty": "regression error or repeated-trial standard deviation, whichever is larger",
            "confidence_level": None, "propagated_ratio_intervals": None,
        },
        "inference_limits": {
            "new_target_observations": 0, "new_candidate_assessments": 0,
            "verified_target_complements_added": 0,
            "target_rate_transfer": False, "target_core_renewal_demonstrated": False,
            "newly_competent_activity_demonstrated": False, "life_demonstrated": False,
            "fit_performed": False, "holdout_validation_performed": False,
        },
    }


if __name__ == "__main__":
    result = analyze()
    (BASE / "analysis.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
