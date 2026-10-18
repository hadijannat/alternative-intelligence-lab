"""Verify acquisition receipts and schema inventory without reading outcomes."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent


def main():
    checks = {}
    receipts = [json.loads((ROOT / name).read_text()) for name in
                ("attempt1/receipt.json", "attempt2/receipt.json")]
    records = [(receipt, request) for receipt in receipts for request in receipt["requests"]]
    for index, (_, request) in enumerate(records):
        folder = ROOT / ("attempt1" if index < 10 else "attempt2")
        body = (folder / request["name"]).read_bytes()
        checks[f"request_{index + 1}_retained_bytes"] = (
            len(body) == request["bytes"] and hashlib.sha256(body).hexdigest() == request["sha256"])
    checks["seven_direct_403_bodies_preserved"] = sum(r.get("status") == 403 for _, r in records) == 7
    for suffix, doi, license_id in (("data", "10.5061/dryad.8w9ghx3vx", "cc0-1.0"),
                                    ("software", "10.5281/zenodo.12009234", "mit")):
        data = json.loads((ROOT / f"attempt1/datacite-{suffix}.json").read_text())["data"]["attributes"]
        checks[suffix + "_doi_license"] = data["doi"] == doi and any(
            r.get("rightsIdentifier") == license_id for r in data["rightsList"])
    metadata = json.loads((ROOT / "attempt1/dryad-dataset.json").read_text())
    checks["dataset_exact_article"] = (
        metadata["identifier"] == "doi:10.5061/dryad.8w9ghx3vx" and metadata["versionNumber"] == 4
        and any(w.get("identifier") == "https://doi.org/10.1073/pnas.2319718121" for w in metadata["relatedWorks"]))
    files = json.loads((ROOT / "attempt2/dryad-files.json").read_text())["_embedded"]["stash:files"]
    checks["both_dryad_assets_match_repository"] = len(files) == 2 and all(
        (ROOT / "browser-native" / item["path"]).stat().st_size == item["size"] and
        hashlib.sha256((ROOT / "browser-native" / item["path"]).read_bytes()).hexdigest() == item["digest"]
        for item in files)
    browser = json.loads((ROOT / "browser-receipt.json").read_text())
    acquired = [r for r in browser["requests"] if r["status"] == "verified_native_bytes"]
    checks["three_native_imports_match_receipt"] = len(acquired) == 3 and all(
        hashlib.sha256((ROOT / "browser-native" / r["name"]).read_bytes()).hexdigest() == r["sha256"]
        for r in acquired)
    checks["native_fig3_repository_md5"] = hashlib.md5((ROOT / "browser-native/PNASscriptFig3.m").read_bytes()).hexdigest() == "b1d791f1f80fabeb8699500e0592a261"
    inventory = json.loads((ROOT / "native-inventory.json").read_text())
    with zipfile.ZipFile(ROOT / "browser-native/data.zip") as archive:
        checks["archive_crcs_and_inventory"] = (archive.testzip() is None and len(archive.infolist()) == 404
            and len(inventory["archive_entries"]) == 404 and inventory["zip_crc_ok"] and not inventory["unsafe_entries"])
    matrices = inventory["matlab_files"]
    checks["all_201_matlab_files_read_at_storage_level"] = len(matrices) == 201 and not any("parse_error" in m for m in matrices)
    checks["200_opaque_Experiment2_objects_retained"] = sum(any(v["python_type"] == "MatlabOpaque" for v in m["variables"].values()) for m in matrices) == 200
    scope = next(m for m in matrices if m["name"] == "data/OscilloscopeData.mat")
    checks["oscilloscope_schema"] = scope["variables"]["T2"]["shape"] == [100, 3] and scope["variables"]["T2"]["dtype"] == "float64"
    protocol_hash = hashlib.sha256((ROOT.parent / "PROTOCOL.md").read_bytes()).hexdigest()
    checks["frozen_protocol_unchanged"] = protocol_hash == receipts[0]["protocol_sha256"] == inventory["protocol_sha256"]
    checks["no_numerical_outcome_replay"] = inventory["numerical_outcome_replay"] is False and inventory["independent_generalization_verified"] is False
    result = dict(checks=checks, passed=sum(checks.values()), total=len(checks), scientific_validation=False)
    (ROOT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    assert all(checks.values()), "Source acquisition/inventory check failed"


if __name__ == "__main__":
    main()
