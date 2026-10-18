"""Preserve public extended methods with the reviewed network receipt writer."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "origin-function-followup/sources"))
import acquire as recorder

if __name__ == "__main__":
    receipt = ROOT / "companion-acquisition.json"
    if receipt.exists() or (ROOT / "extended-methods.html").exists():
        raise FileExistsError("Prior attempt preserved")
    recorder.ROOT = ROOT
    record = recorder.fetch(("extended-methods.html", "https://arxiv.org/html/2311.00537v2"))
    receipt.write_text(json.dumps(dict(requests=[record], scientific_validation=False), indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("status", "bytes", "error") if k in record}))
    assert record.get("status") == 200 and not record.get("error"), "Extended-method source unavailable; attempt retained"
