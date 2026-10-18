"""Check the new native helper attachment without running deposited code."""
import hashlib
import json
from pathlib import Path
import zipfile

from import_browser_files import SOFTWARE

ROOT = Path(__file__).resolve().parent


def main():
    receipt = json.loads((ROOT / "attachment-receipt.json").read_text())
    native = ROOT / "helper-native"
    body = (native / "helper_scripts.zip").read_bytes()
    checks = dict(
        successful_immutable_attachment_receipt=receipt["execution_error"] is None,
        native_size=len(body) == receipt["native_zip"]["bytes"] == 50569,
        repository_md5=hashlib.md5(body).hexdigest() == SOFTWARE["helper_scripts.zip"] == receipt["native_zip"]["expected_digest"],
        native_sha256=hashlib.sha256(body).hexdigest() == receipt["native_zip"]["sha256"],
        no_deposited_code_execution=receipt["third_party_code_executed"] is False,
        no_numerical_response_replay=receipt["numerical_response_replay"] is False)
    with zipfile.ZipFile(native / "helper_scripts.zip") as archive:
        checks["zip_crc_and_entry_count"] = archive.testzip() is None and len(archive.infolist()) == 14
        checks["six_extracted_sources_match_archive"] = len(receipt["extracted_files"]) == 6 and all(
            (native / item["name"]).read_bytes() == archive.read(item["archive_path"])
            and hashlib.sha256((native / item["name"]).read_bytes()).hexdigest() == item["sha256"]
            for item in receipt["extracted_files"])
    software = json.loads((ROOT / "attempt1/datacite-software.json").read_text())["data"]["attributes"]
    checks["repository_software_license_mit"] = any(r.get("rightsIdentifier") == "mit" for r in software["rightsList"])
    result = dict(checks=checks, passed=sum(checks.values()), total=len(checks), scientific_validation=False)
    (ROOT / "attachment-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    assert all(checks.values()), "Native helper attachment check failed"


if __name__ == "__main__":
    main()
