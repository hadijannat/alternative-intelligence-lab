"""Check the bounded novelty audit's arithmetic and retained source integrity."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    cases = [
        ("Mo36 parent", {"MoVI": 36, "OII": 112}, -8),
        ("Mo34WV(V) hypothesis", {"MoVI": 34, "WVI": 1, "VV": 1, "OII": 112}, -9),
        ("Mo34WV(IV) hypothesis", {"MoVI": 34, "WVI": 1, "VIV": 1, "OII": 112}, -10),
        ("Mo35W hypothesis", {"MoVI": 35, "WVI": 1, "OII": 112}, -8),
        ("Mo35V hypothesis", {"MoVI": 35, "VV": 1, "OII": 112}, -9),
        ("P mixed Keggin search probe", {"PV": 1, "MoVI": 6, "WVI": 5, "VV": 1, "OII": 40}, -4),
        ("Si mixed Keggin search probe", {"SiIV": 1, "MoVI": 6, "WVI": 5, "VV": 1, "OII": 40}, -5),
        ("known hydroxylated Mo36", {"MoVI": 36, "OII": 110, "OH": 6}, -10),
    ]
    oxidation = {"MoVI": 6, "WVI": 6, "VV": 5, "VIV": 4,
                 "PV": 5, "SiIV": 4, "OII": -2, "OH": -1}
    charges = []
    for name, composition, expected in cases:
        actual = sum(oxidation[key] * count for key, count in composition.items())
        assert actual == expected, (name, actual, expected)
        assert all(key in oxidation for key in composition)
        charges.append({"name": name, "charge": actual})
    acquired = json.loads((ROOT / "acquisition.json").read_text())
    retained = []
    for item in acquired:
        if "sha256" in item:
            data = (ROOT / "raw" / item["name"]).read_bytes()
            assert len(data) == item["bytes"]
            assert hashlib.sha256(data).hexdigest() == item["sha256"]
            retained.append(item["name"])
    log = json.loads((ROOT / "search_log.json").read_text())
    assert log["date"] == "2026-10-15"
    assert log["exact_candidate_novelty"] == "UNRESOLVED"
    assert log["compound_discovery_claim"] is False
    assert len({x["query"] for x in log["queries"]}) == len(log["queries"])
    source_ids = [x["id"] for x in json.loads((ROOT / "sources.json").read_text())]
    assert len(set(source_ids)) == len(source_ids)
    result = {"status": "PASS", "charge_checks": charges, "retained_files": retained,
              "queries": len(log["queries"]), "primary_sources": len(source_ids),
              "meaning": "formal arithmetic and artifact integrity only; no molecular or novelty validation"}
    (ROOT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
