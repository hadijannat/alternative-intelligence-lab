"""Check source retention and proposed bookkeeping; performs no parameter fitting."""
from datetime import datetime, timezone
import hashlib
import json
from math import isclose, sqrt
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def main():
    ledger = json.loads((HERE / "sources.json").read_text())
    for name, expected in ledger["retained_input_hashes"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    si = (ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt").read_text()
    for needle in ("denatured at 85 °C for 5 minutes", "5 µM Cy5-A", "900 mM sucrose"):
        assert needle in si, needle
    xml = ET.parse(ROOT / "measured-coupling-2026-10-15/rna_sources/raw/salibi.xml").getroot()
    assert ledger["sources"][0]["title"] == "".join(xml.find(".//article-title").itertext())
    for source in ledger["sources"]:
        assert len(source.get("exact_excerpt", "").split()) <= 25

    # RNA moieties are wildtype-A, reporter-A, and B, including ligated B.
    inventories = {
        "A": (1, 0, 0), "R": (0, 1, 0), "B": (0, 0, 1),
        "F": (1, 0, 1), "D": (1, 0, 1), "P": (0, 1, 1),
        "QFF": (2, 0, 2), "QFD": (2, 0, 2), "QDD": (2, 0, 2),
        "QFP": (1, 1, 2), "QDP": (1, 1, 2), "QPP": (0, 2, 2),
    }
    competent = {"F": 1, "QFF": 2, "QFD": 1, "QFP": 1}
    ligated_reporter = {"P": 1, "QFP": 1, "QDP": 1, "QPP": 2}
    events = [
        ("F active ligation", {"F": -1, "A": -1, "B": -1, "QFF": 1}, 1, 0),
        ("F reporter ligation", {"F": -1, "R": -1, "B": -1, "QFP": 1}, 0, 1),
        ("precursor active net", {"A": -1, "B": -1, "F": 1}, 1, 0),
        ("precursor reporter net", {"R": -1, "B": -1, "P": 1}, 0, 1),
        ("no-regeneration F route", {"F": -1, "A": -1, "B": -1, "QFD": 1}, 0, 0),
        ("free loss", {"F": -1, "D": 1}, -1, 0),
        ("FF loss", {"QFF": -1, "QFD": 1}, -1, 0),
        ("FD loss", {"QFD": -1, "QDD": 1}, -1, 0),
        ("FP loss", {"QFP": -1, "QDP": 1}, -1, 0),
    ]
    pairs = [("F", "F"), ("F", "D"), ("D", "D"), ("F", "P"), ("D", "P"), ("P", "P")]
    for left, right in pairs:
        change = {"Q" + left + right: 1}
        for name in (left, right):
            change[name] = change.get(name, 0) - 1
        events.append((left + right + " association", change, 0, 0))
        events.append((left + right + " release", {key: -v for key, v in change.items()}, 0, 0))
    for name, change, expected_competence, expected_reporter in events:
        assert all(sum(n * inventories[s][i] for s, n in change.items()) == 0 for i in range(3)), name
        assert sum(n * competent.get(s, 0) for s, n in change.items()) == expected_competence, name
        assert sum(n * ligated_reporter.get(s, 0) for s, n in change.items()) == expected_reporter, name

    for seed in (0, 0.1, 1, 10, 100):
        for kstar in (1e-8, 0.01, 1, 100):
            free = 2 * seed / (1 + sqrt(1 + 4 * seed / kstar))
            complex_ff = 0.5 * free * free / kstar
            assert isclose(free + 2 * complex_ff, seed, abs_tol=1e-12, rel_tol=1e-12)
            assert free >= 0 and complex_ff >= 0
    f, d, p = 0.3, 0.8, 1.2
    association = 0.5 * (f*f + d*d + p*p) + f*d + f*p + d*p
    assert isclose(association, 0.5 * (f+d+p)**2)
    receipt = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "source_hashes_checked": len(ledger["retained_input_hashes"]),
        "stoichiometric_channels_checked": len(events),
        "inventories_checked": ["wildtype-A", "reporter-A", "B"],
        "competence_and_PAGE_changes_checked": True,
        "initial_equilibrium_cases_checked": 20,
        "shared_pair_association_convention_checked": True,
        "no_fit_performed": True,
        "limit": "Bookkeeping and retained-source checks only; chemistry and inferred inventories are not experimentally verified",
    }
    (HERE / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
