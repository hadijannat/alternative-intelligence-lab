import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

BASE = Path(__file__).resolve().parent
SOURCES = [
    ("theses-catalog.html", "https://theses.fr/2017SACLV078"),
    ("theses-catalog-json.response", "https://theses.fr/2017SACLV078.json"),
    ("hal-author-metadata.json", "https://api.archives-ouvertes.fr/search/?q=authLastName_t%3AMoussawi&wt=json&fl=title_s,doiId_s,uri_s,fileMain_s,authFullName_s,producedDateY_i&rows=100"),
    ("crossref-author-metadata.json", "https://api.crossref.org/works?query.author=Moussawi&query=polyoxometalate&filter=from-pub-date%3A2014-01-01,until-pub-date%3A2020-12-31&rows=100"),
]

def acquire(item):
    filename, url = item
    record = {"filename": filename, "requested_url": url,
              "accessed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
            record.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get("Content-Type"),
                          bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                          pdf_magic=data.startswith(b"%PDF-"))
        (BASE / "raw" / filename).write_bytes(data)
    except Exception as exc:
        record["error"] = str(exc)
    return record

if __name__ == "__main__":
    (BASE / "raw").mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(acquire, SOURCES))
    (BASE / "acquisition.json").write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(records, indent=2))
