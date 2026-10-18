from pathlib import Path
import hashlib
import json
import urllib.request
import urllib.error
import datetime
import fitz

ROOT = Path(__file__).resolve().parent
records = []
for article_id in [12662087, 12662108, 12662111]:
    url = f"https://api.figshare.com/v2/articles/{article_id}"
    with urllib.request.urlopen(url, timeout=60) as response:
        metadata_bytes = response.read()
    metadata = json.loads(metadata_bytes)
    (ROOT / f"figshare-{article_id}.json").write_bytes(metadata_bytes)
    assert metadata["doi"].startswith("10.1021/acs.cgd.0c00693.s")
    for file in metadata["files"]:
        failures = []
        for query in ["?download=1", "?download=2", "?download=3"]:
            download_url = file["download_url"] + query
            try:
                with urllib.request.urlopen(download_url, timeout=60) as response:
                    content = response.read()
                break
            except urllib.error.HTTPError as error:
                failures.append({"url": download_url, "http_status": error.code})
        else:
            raise RuntimeError(failures)
        assert len(content) == file["size"], (file["name"], len(content))
        assert hashlib.md5(content).hexdigest() == file["computed_md5"]
        path = ROOT / file["name"]
        path.write_bytes(content)
        record = {"article_id": article_id, "doi": metadata["doi"],
                  "metadata_url": url, "url": download_url, "file": path.name,
                  "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                  "md5_matches_deposit": True, "failed_download_attempts": failures}
        if path.suffix == ".pdf":
            doc = fitz.open(stream=content, filetype="pdf")
            record["pages"] = len(doc)
            (ROOT / "supporting-information.txt").write_text(
                "\n".join(f"\n--- PDF PAGE {i + 1} ---\n" + p.get_text()
                          for i, p in enumerate(doc)))
        records.append(record)

url = "https://pubs.acs.org/doi/10.1021/acs.cgd.0c00693"
try:
    with urllib.request.urlopen(url, timeout=60) as response:
        content = response.read()
        status = response.status
except urllib.error.HTTPError as error:
    content, status = error.read(), error.code
(ROOT / "publisher-main-response.html").write_bytes(content)
records.append({"url": url, "status": status, "file": "publisher-main-response.html",
                "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                "main_text_verified": False})
(ROOT / "receipt.json").write_text(json.dumps({
    "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "records": records}, indent=2) + "\n")
print(json.dumps(records, indent=2))
