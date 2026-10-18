"""Reuse the reviewed native-body receipt helper for one bounded acquisition."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "origin-function-followup/sources"))
import acquire as recorder

ROUTES = [
    ("datacite-data.json", "https://api.datacite.org/dois/10.5061/dryad.8w9ghx3vx"),
    ("datacite-software.json", "https://api.datacite.org/dois/10.5281/zenodo.12009234"),
    ("dryad-dataset.json", "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.8w9ghx3vx"),
    ("zenodo-record.json", "https://zenodo.org/api/records/12009234"),
    ("PNASscriptFig2.m", "https://zenodo.org/records/12009234/files/PNASscriptFig2.m?download=1"),
    ("PNASscriptFig3.m", "https://zenodo.org/records/12009234/files/PNASscriptFig3.m?download=1"),
    ("PNASscriptFig4.m", "https://zenodo.org/records/12009234/files/PNASscriptFig4.m?download=1"),
    ("PNASscriptFig5.m", "https://zenodo.org/records/12009234/files/PNASscriptFig5.m?download=1"),
    ("PNASscriptFig6.m", "https://zenodo.org/records/12009234/files/PNASscriptFig6.m?download=1"),
    ("helper_scripts.zip", "https://zenodo.org/records/12009234/files/helper_scripts.zip?download=1"),
]


def main():
    attempt = ROOT / "attempt1"
    attempt.mkdir(exist_ok=False)
    recorder.ROOT = attempt
    records = []
    try:
        with ThreadPoolExecutor(max_workers=4) as pool:
            records = list(pool.map(recorder.fetch, ROUTES))
    finally:
        result = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),
                      protocol_sha256=hashlib.sha256((ROOT.parent / "PROTOCOL.md").read_bytes()).hexdigest(),
                      helper_sha256=hashlib.sha256(Path(recorder.__file__).read_bytes()).hexdigest(),
                      requests=records, scientific_validation=False)
        (attempt / "receipt.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps([{k: r[k] for k in ("name", "status", "bytes", "error") if k in r}
                          for r in records], indent=2))
    assert len(records) == len(ROUTES), "Attempt receipt incomplete"


if __name__ == "__main__":
    main()
