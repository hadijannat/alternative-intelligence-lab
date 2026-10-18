from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sources"
DOI = "10.1038/s41467-022-35416-w"
PREFIX = ("https://media.springernature.com/original/springer-static/esm/"
          "art%3A10.1038%2Fs41467-022-35416-w/MediaObjects/")
ROUTES = [
    ("hou-si.pdf", PREFIX + "41467_2022_35416_MOESM1_ESM.pdf"),
    ("hou-source.xlsx", PREFIX + "41467_2022_35416_MOESM7_ESM.xlsx"),
]


def main():
    SOURCE.mkdir(exist_ok=True)
    receipt_path = SOURCE / "receipt.json"
    if receipt_path.exists():
        raise FileExistsError("Preserve the existing receipt; use a new attempt")
    helper_path = ROOT.parent / "origin-function-followup/sources/acquire.py"
    spec = importlib.util.spec_from_file_location("reviewed_acquisition", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    helper.ROOT = SOURCE
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(helper.fetch, ROUTES))
    workspace = ROOT.parents[1]
    original = workspace / ".omo/evidence/public-repair-datasets-2026-10-18/hou2022.html"
    target = SOURCE / "hou-main.html"
    if target.exists():
        raise FileExistsError(target)
    data = original.read_bytes()
    target.write_bytes(data)
    records.append(dict(name=target.name,
                        url="https://www.nature.com/articles/s41467-022-35416-w",
                        acquisition="preserved specialist publisher-response bytes; local import",
                        original_local_path=str(original.relative_to(workspace)),
                        bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    result = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(), resource_doi=DOI,
                  source_title="A self-healing electrocatalytic system via electrohydrodynamics induced evolution in liquid metal",
                  observed_publisher_license="CC BY 4.0",
                  source_helper_sha256=hashlib.sha256(helper_path.read_bytes()).hexdigest(),
                  requests=records, numerical_responses_selected=False,
                  scientific_validation=False)
    receipt_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"receipt": str(receipt_path), "requests": [
        {k: r[k] for k in ("name", "status", "bytes", "sha256", "error") if k in r}
        for r in records]}, indent=2))


if __name__ == "__main__":
    main()
