"""Acquire one primary Ou package; keep native bytes and failed responses."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
DOI = "10.1038/s41467-023-43305-z"
ROUTES = [
    ("ou-main.pdf", "https://electrochemistry.berkeley.edu/sites/default/files/s41467-023-43305-z_2.pdf"),
    ("ou-si.pdf", "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-023-43305-z/MediaObjects/41467_2023_43305_MOESM1_ESM.pdf"),
    ("ou-figshare.json", "https://api.figshare.com/v2/articles/24197487"),
]


def fetch(item):
    name, url = item
    target = ROOT / name
    if target.exists():
        raise FileExistsError(target)
    record = dict(name=name, url=url, attempted_utc=datetime.now(timezone.utc).isoformat())
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        try:
            response = urllib.request.urlopen(request, timeout=45)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            record.update(status=response.code, resolved_url=response.url,
                          content_type=response.headers.get("Content-Type"))
            body = response.read()
        target.write_bytes(body)
        record.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                      md5=hashlib.md5(body).hexdigest())
    except Exception as error:
        record["error"] = repr(error)
    return record


def main():
    receipt_path = ROOT / "receipt.json"
    if receipt_path.exists():
        raise FileExistsError("Preserve the existing receipt; use a new attempt directory")
    records, checks, run_error = [], {}, None
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            records = list(pool.map(fetch, ROUTES))
        metadata_record = next(r for r in records if r["name"] == "ou-figshare.json")
        if metadata_record.get("status") == 200 and "error" not in metadata_record:
            metadata = json.loads((ROOT / "ou-figshare.json").read_text())
            checks["exact_resource_doi"] = metadata["resource_doi"] == DOI
            if not checks["exact_resource_doi"]:
                raise ValueError("Registry is not the intended primary source")
            candidates = [f for f in metadata["files"] if f["name"] == "Raw Tabulated Data from Figures.xlsx"]
            checks["one_exact_workbook"] = len(candidates) == 1
            if len(candidates) == 1:
                item = candidates[0]
                record = fetch(("ou-tabulated.xlsx", item["download_url"]))
                record.update(expected_size=item["size"], expected_md5=item["computed_md5"])
                checks["workbook_size"] = record.get("bytes") == item["size"]
                checks["workbook_md5"] = record.get("md5") == item["computed_md5"]
                records.append(record)
        for record in records:
            if record["name"].endswith(".pdf"):
                checks[record["name"] + "_pdf_signature"] = (
                    record.get("status") == 200 and "error" not in record
                    and (ROOT / record["name"]).read_bytes().startswith(b"%PDF"))
        assert len(checks) == 6 and all(checks.values()), "Acquisition incomplete"
    except Exception as error:
        run_error = repr(error)
        raise
    finally:
        result = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(), resource_doi=DOI,
                      requests=records, checks=checks, execution_error=run_error,
                      scientific_validation=False)
        receipt_path.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(dict(requests=[{k: r[k] for k in ("name", "status", "bytes", "error") if k in r} for r in records], checks=checks), indent=2))


if __name__ == "__main__":
    main()
