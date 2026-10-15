"""Acquire pinned author data; never execute the downloaded notebooks."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
COMMIT = "5e39536facd68c2a133454b6a31390d53f19ad30"
BASE = "https://raw.githubusercontent.com/hsoria/Primitive-Genotype-Phenotype-coupling/"
TREE_URL = f"https://api.github.com/repos/hsoria/Primitive-Genotype-Phenotype-coupling/git/trees/{COMMIT}?recursive=1"


def acquire(item):
    path = item["path"]
    url = BASE + COMMIT + "/" + urllib.parse.quote(path)
    destination = ROOT / "author" / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
        resolved = response.url
    assert len(data) == item["size"], path
    destination.write_bytes(data)
    return {"path": str(destination.relative_to(ROOT)), "source_path": path,
            "url": url, "resolved_url": resolved, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "retrieved_utc": datetime.now(timezone.utc).isoformat(),
            "license": "MIT repository root; no separate data license identified"}


def main():
    with urllib.request.urlopen(TREE_URL, timeout=60) as response:
        tree = json.load(response)
    assert not tree.get("truncated"), "Tree truncated"
    selected = [item for item in tree["tree"] if item["type"] == "blob"
                and (Path(item["path"]).suffix in {".csv", ".xlsx", ".ipynb", ".py"}
                     or item["path"] in {"LICENSE", "README.md"})]
    assert sum(item["size"] for item in selected) < 10_000_000
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(acquire, selected))
    manifest = {"doi": "10.1016/j.chempr.2025.102816", "commit": COMMIT,
                "tree_url": TREE_URL, "files": rows,
                "excluded": "TIFF images >20MB each; .DS_Store, pyc and extensionless duplicate"}
    si_url = "https://ars.els-cdn.com/content/image/1-s2.0-S2451929425004073-mmc1.pdf?download=true"
    with urllib.request.urlopen(urllib.request.Request(si_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as response:
        data = response.read()
    assert data.startswith(b"%PDF-"), "SI is not PDF"
    (ROOT / "supplement.pdf").write_bytes(data)
    manifest["supplement"] = {"url": si_url, "path": "supplement.pdf", "bytes": len(data),
                              "sha256": hashlib.sha256(data).hexdigest(),
                              "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                              "license": "CC BY 4.0 article license"}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Acquired {len(rows)} files; {sum(row['bytes'] for row in rows)} bytes")


if __name__ == "__main__":
    main()
