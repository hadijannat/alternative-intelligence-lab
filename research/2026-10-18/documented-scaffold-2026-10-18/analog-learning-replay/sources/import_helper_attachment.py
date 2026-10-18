"""Import the native methods ZIP using the existing verified-copy boundary."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from inventory import checked_members
from import_browser_files import SOFTWARE, verified_copy

EXPECTED = {"Experiment2.m", "ExperimentGroup.m", "logic_truth_table3.m",
            "makeOrthonormalModes.m", "makePlotPrettyNow.m", "network_project_superclass2.m"}


def main():
    receipt = ROOT / "attachment-receipt.json"
    if receipt.exists():
        raise FileExistsError("Preserve the existing attachment receipt")
    result = dict(observed_utc=datetime.now(timezone.utc).isoformat(),
                  source_url="https://zenodo.org/records/12009234/files/helper_scripts.zip?download=1",
                  source_record="10.5281/zenodo.12009234", license="MIT",
                  route="One normal Chrome link downloadMedia attempt returned native file path",
                  previous_absence_checked=True, extracted_files=[], execution_error=None,
                  third_party_code_executed=False, numerical_response_replay=False)
    try:
        target = ROOT / "helper-native"
        target.mkdir(exist_ok=False)
        result["native_zip"] = verified_copy(Path("/USER_HOME/Downloads/helper_scripts.zip"),
                                             target / "helper_scripts.zip", "md5", SOFTWARE["helper_scripts.zip"])
        with zipfile.ZipFile(target / "helper_scripts.zip") as archive:
            members = checked_members(archive)
            result["zip_crc_ok"] = True
            result["archive_entries"] = len(members)
            selected = [m for m in members if m.filename.startswith("helper_scripts/") and m.filename.endswith(".m")]
            if len(selected) != 6 or {Path(m.filename).name for m in selected} != EXPECTED:
                raise ValueError("Native helper ZIP differs from the observed six-file methods inventory")
            for item in selected:
                body = archive.read(item)
                saved = target / Path(item.filename).name
                if saved.exists():
                    raise FileExistsError(saved)
                saved.write_bytes(body)
                result["extracted_files"].append(dict(name=saved.name, archive_path=item.filename,
                    bytes=len(body), sha256=hashlib.sha256(body).hexdigest()))
    except Exception as error:
        result["execution_error"] = repr(error)
        raise
    finally:
        receipt.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
