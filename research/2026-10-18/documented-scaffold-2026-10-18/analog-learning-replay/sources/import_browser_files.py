"""Import only hash-verified browser downloads; preserve missing assets as null."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOWNLOADS = Path("/USER_HOME/Downloads")
SOFTWARE = {
    "PNASscriptFig2.m": "89fe4de35abcce826cb12cbb19c2a047",
    "PNASscriptFig3.m": "b1d791f1f80fabeb8699500e0592a261",
    "PNASscriptFig4.m": "c5e6488eca4a02b3e0f50554541485a9",
    "PNASscriptFig5.m": "909aadb27ef5de232317efb98e60c99b",
    "PNASscriptFig6.m": "2198a2746b62c6eb5ce5fb2185c6c4c9",
    "helper_scripts.zip": "b9b06b71f3b709445f97d4386366fe76",
}


def verified_copy(source, target, algorithm, expected_digest, expected_size=None):
    if target.exists():
        raise FileExistsError(target)
    body = source.read_bytes()
    if expected_size is not None and len(body) != expected_size:
        raise ValueError("Browser file size disagrees with repository metadata")
    if hashlib.new(algorithm, body).hexdigest() != expected_digest:
        raise ValueError("Browser file digest disagrees with repository metadata")
    target.write_bytes(body)
    return dict(name=target.name, source_path=str(source), bytes=len(body),
                sha256=hashlib.sha256(body).hexdigest(), md5=hashlib.md5(body).hexdigest(),
                expected_digest=expected_digest, digest_algorithm=algorithm,
                expected_size=expected_size, status="verified_native_bytes")


def main():
    receipt = ROOT / "browser-receipt.json"
    if receipt.exists():
        raise FileExistsError("Preserve the existing browser receipt; use a fresh attempt directory")
    records, reused_primary, current_asset, execution_error = [], None, None, None
    try:
        native = ROOT / "browser-native"
        native.mkdir(exist_ok=False)
        files = json.loads((ROOT / "attempt2/dryad-files.json").read_text())["_embedded"]["stash:files"]
        if len(files) != 2 or {item["path"] for item in files} != {"data.zip", "README.md"}:
            raise ValueError("Dryad metadata must name exactly data.zip and README.md basenames")
        for item in files:
            current_asset = item["path"]
            source = DOWNLOADS / current_asset
            if source.exists():
                records.append(verified_copy(source, native / current_asset, "sha256", item["digest"], item["size"]))
            else:
                records.append(dict(name=current_asset, status="no_native_file_observed", source_path=None))
        for name, expected in SOFTWARE.items():
            current_asset = name
            source = DOWNLOADS / name
            if source.exists():
                records.append(verified_copy(source, native / name, "md5", expected))
            else:
                records.append(dict(name=name, status="no_native_file_observed", source_path=None))
        current_asset = "reused primary XML"
        primary = ROOT.parents[2] / "noncarbon-discovery-2026-10-15/research/information/raw/analog-2024.xml"
        original_hash = hashlib.sha256(primary.read_bytes()).hexdigest()
        if original_hash != "4e2a79e948d3604d2aaf5146d8be85fb927453d827086a630a8b7c5520f3d349":
            raise ValueError("Previously verified primary XML hash changed")
        reused_primary = dict(path=str(primary), sha256=original_hash, native_copy=False)
    except Exception as error:
        execution_error = repr(error)
        records.append(dict(name=current_asset, status="import_error", error=execution_error))
        raise
    finally:
        result = dict(observed_utc=datetime.now(timezone.utc).isoformat(),
                      software_digest_source="Normal browser Zenodo12009234 file table, 2026-10-18",
                      reused_primary=reused_primary, requests=records,
                      execution_error=execution_error, scientific_validation=False)
        receipt.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
