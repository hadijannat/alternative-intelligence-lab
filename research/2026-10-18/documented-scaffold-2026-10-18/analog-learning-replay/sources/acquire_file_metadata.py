"""Follow the version URL from the acquired, exact-identity Dryad metadata."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "origin-function-followup/sources"))
import acquire as recorder


if __name__ == "__main__":
    metadata = json.loads((ROOT / "attempt1/dryad-dataset.json").read_text())
    assert metadata["identifier"] == "doi:10.5061/dryad.8w9ghx3vx"
    assert any(w.get("identifier") == "https://doi.org/10.1073/pnas.2319718121"
               for w in metadata["relatedWorks"])
    version = metadata["_links"]["stash:version"]["href"]
    assert version.startswith("/api/v2/versions/") and version.removeprefix("/api/v2/versions/").isdigit()
    attempt = ROOT / "attempt2"
    attempt.mkdir(exist_ok=False)
    recorder.ROOT = attempt
    record = recorder.fetch(("dryad-files.json", urljoin("https://datadryad.org", version + "/files")))
    (attempt / "receipt.json").write_text(json.dumps(dict(
        retrieved_utc=datetime.now(timezone.utc).isoformat(), requests=[record],
        scientific_validation=False), indent=2) + "\n")
    print(json.dumps(record, indent=2))
