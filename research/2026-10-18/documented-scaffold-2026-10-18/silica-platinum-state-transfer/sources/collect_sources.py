"""Acquire exact open primary XML/ZIP using the reviewed receipt writer."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "origin-function-followup/sources"))
import acquire as recorder

ROUTES = [
    ("article.xml", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11897212/fullTextXML"),
    ("supplementary.zip", "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11897212/supplementaryFiles"),
]

if __name__ == "__main__":
    receipt = ROOT / "receipt.json"
    if receipt.exists() or any((ROOT / name).exists() for name, _ in ROUTES):
        raise FileExistsError("Existing attempt preserved; use a fresh source layout")
    recorder.ROOT = ROOT
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(recorder.fetch, ROUTES))
    receipt.write_text(json.dumps(dict(retrieved_utc=datetime.now(timezone.utc).isoformat(), requests=records,
                                      scientific_validation=False), indent=2) + "\n")
    print(json.dumps([{k:r[k] for k in ("name", "status", "bytes", "error") if k in r} for r in records]))
    assert len(records) == 2 and all(r.get("status") == 200 and "error" not in r for r in records), "Access incomplete; receipts retained"
