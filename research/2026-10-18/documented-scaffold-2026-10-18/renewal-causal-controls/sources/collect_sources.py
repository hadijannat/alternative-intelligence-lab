"""Reuse the reviewed receipt writer for four bounded primary-source requests."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "origin-function-followup/sources"))
import acquire as recorder

ROUTES = [
    ("nishioka-main.pdf", "https://pubs.rsc.org/ta/article-pdf/14/36/23803/12747865/d6ta02355j.pdf"),
    ("nishioka-si.pdf", "https://pubs.rsc.org/ta/article-supplement/1241054/pdf/d6ta02355j1_suppl/"),
    ("stevens-main.pdf", "https://escholarship.org/content/qt08k5s56q/qt08k5s56q_noSplash_1e87bb45bd80b5ee61ae972d8887dfd6.pdf"),
    ("cimino-main.pdf", "https://iris.cnr.it/retrieve/1a173e96-30dd-4110-a69a-57265ae685e5/prod_488104-doc_202951.pdf"),
]


if __name__ == "__main__":
    receipt = ROOT / "receipt.json"
    if receipt.exists() or any((ROOT / name).exists() for name, _ in ROUTES):
        raise FileExistsError("Use a fresh attempt directory; existing native bytes/receipts are preserved")
    recorder.ROOT = ROOT
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(recorder.fetch, ROUTES))
    receipt.write_text(json.dumps(dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),
                                       requests=records, scientific_validation=False), indent=2) + "\n")
    print(json.dumps([{k: record[k] for k in ("name", "status", "bytes", "error") if k in record}
                      for record in records], indent=2))
    assert len(records) == len(ROUTES), "Attempt receipts incomplete"
