from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
import urllib.error
import fitz

ROOT = Path(__file__).resolve().parent
records = []
for name, url in [
    ("figshare.json", "https://api.figshare.com/v2/articles/21509957"),
    ("cs2c03898_si_001.pdf", "https://ndownloader.figshare.com/files/38122559"),
    ("acs-landing.html", "https://pubs.acs.org/doi/10.1021/acscatal.2c03898"),
    ("author-institution.html", "https://www.sigs.tsinghua.edu.cn/gl_en/list.htm"),
]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as error:
        response = error
    payload = response.read()
    (ROOT / name).write_bytes(payload)
    records.append({"url": url, "resolved_url": response.url, "status": response.code,
                    "path": name, "bytes": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "md5": hashlib.md5(payload).hexdigest(),
                    "content_type": response.headers.get("Content-Type")})

metadata = json.loads((ROOT / "figshare.json").read_text())
pdf_record = records[1]
deposited = metadata["files"]
assert len(deposited) == 1
assert pdf_record["status"] == 200
assert pdf_record["md5"] == deposited[0]["computed_md5"]
assert pdf_record["bytes"] == deposited[0]["size"]
document = fitz.open(ROOT / "cs2c03898_si_001.pdf")
text = "\n".join(f"\n--- PDF page {i+1} ---\n{page.get_text()}" for i, page in enumerate(document))
(ROOT / "supporting-information.txt").write_text(text)
rendered = []
for i, page in enumerate(document):
    if any(label in page.get_text() for label in ["Figure S4.", "Figure S5.", "Figure S8.", "Figure S9."]):
        name = f"si-page-{i+1:02d}.png"
        page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(ROOT / name)
        rendered.append(name)
receipt = {"retrieved_utc": datetime.now(timezone.utc).isoformat(), "requests": records,
           "native_file_list": deposited, "pdf_pages": len(document), "rendered_pages": rendered,
           "metadata_license": metadata["license"], "doi": metadata["doi"],
           "resource_doi": metadata["resource_doi"], "byte_verification": "PASS"}
(ROOT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"byte_verification": "PASS", "pdf_pages": len(document), "rendered_pages": rendered,
                  "requests": [{k:r[k] for k in ["path", "status", "bytes"]} for r in records]}, indent=2))
