"""Save a public PDF URL actually observed after legitimate publisher browsing."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from collect_sources import recorder

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    receipt = ROOT / "browser-main-receipt.json"
    if receipt.exists():
        raise FileExistsError(receipt)
    recorder.ROOT = ROOT
    record = recorder.fetch(("nishioka-browser-main.pdf", sys.argv[1]))
    result = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(), requests=[record],
                  stable_publisher_url="https://pubs.rsc.org/ta/article-pdf/14/36/23803/12747865/d6ta02355j.pdf",
                  provenance="URL observed in normal Chrome after public publisher PDF navigation; no challenge solved or access restriction bypassed",
                  scientific_validation=False)
    receipt.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("name", "status", "bytes", "error") if k in record}))
    assert record.get("status") == 200 and "error" not in record, "Attempt failed; receipt retained"
