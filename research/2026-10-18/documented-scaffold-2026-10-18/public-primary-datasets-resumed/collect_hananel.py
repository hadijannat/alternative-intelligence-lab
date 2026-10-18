from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sources/hananel2025"
ROUTES = [
    ("main.xml", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12046555/fullTextXML"),
    ("deposit.json", "https://api.figshare.com/v2/articles/28823413"),
    ("si.pdf", "https://ndownloader.figshare.com/files/53780128"),
]


def main():
    SOURCE.mkdir(exist_ok=True)
    receipt_path = SOURCE / "receipt.json"
    if receipt_path.exists():
        raise FileExistsError(receipt_path)
    helper_path = ROOT.parent / "origin-function-followup/sources/acquire.py"
    spec = importlib.util.spec_from_file_location("reviewed_acquisition", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    helper.ROOT = SOURCE
    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(helper.fetch, ROUTES))
    checks = {r["name"] + "_http200": r.get("status") == 200 and "error" not in r for r in records}
    checks["si_size"] = (SOURCE / "si.pdf").stat().st_size == 760874 if (SOURCE / "si.pdf").exists() else False
    checks["si_md5"] = hashlib.md5((SOURCE / "si.pdf").read_bytes()).hexdigest() == "3aa8545778bb6b3466aa8b81d817cf02" if (SOURCE / "si.pdf").exists() else False
    checks["si_signature"] = (SOURCE / "si.pdf").read_bytes().startswith(b"%PDF") if (SOURCE / "si.pdf").exists() else False
    error = None
    try:
        metadata = json.loads((SOURCE / "deposit.json").read_text())
        checks["deposit_doi"] = metadata.get("doi") == "10.1021/jacs.4c16883.s001"
        checks["main_doi"] = b"10.1021/jacs.4c16883" in (SOURCE / "main.xml").read_bytes()
    except Exception as exc:
        error = repr(exc)
    result = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),
                  resource_doi="10.1021/jacs.4c16883", requests=records,
                  checks=checks, metadata_error=error, numerical_test_executed=False,
                  scientific_validation=False)
    receipt_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"requests": [{k: r[k] for k in ("name", "status", "bytes", "sha256", "error") if k in r} for r in records],
                      "checks": checks, "metadata_error": error}, indent=2))
    assert all(checks.values()) and error is None


if __name__ == "__main__":
    main()
