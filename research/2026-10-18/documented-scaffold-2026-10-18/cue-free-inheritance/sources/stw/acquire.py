import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import fitz
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
URLS = {
    "brand2017.pdf": "https://authors.library.caltech.edu/records/z7d4m-g6c56/files/PNAS-2017-Brand-5101-6.pdf?download=1",
    "brand2017_si.pdf": "https://authors.library.caltech.edu/records/z7d4m-g6c56/files/pnas.1704638114.sapp.pdf?download=1",
    "kang2021.pdf": "https://osti.gov/servlets/purl/1846400",
    "kang2021_si.pdf": "https://authors.library.caltech.edu/records/28da0-k5c41/files/cm0c04573_si_001.pdf?download=1",
    "sugar2024.html": "https://www.nature.com/articles/s41467-024-49659-2",
    "sugar2024_si.pdf": "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-49659-2/MediaObjects/41467_2024_49659_MOESM1_ESM.pdf",
}

if __name__ == "__main__":
    receipts = []
    for name, url in URLS.items():
        record = {"name": name, "url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat()}
        try:
            response = requests.get(url, timeout=20)
            record["http_status"] = response.status_code
            response.raise_for_status()
        except requests.RequestException as error:
            record["error"] = str(error)
            receipts.append(record)
            continue
        if name.endswith(".pdf"):
            assert response.content.startswith(b"%PDF"), name
        (ROOT / name).write_bytes(response.content)
        record.update(bytes=len(response.content), sha256=hashlib.sha256(response.content).hexdigest())
        if name.endswith(".pdf"):
            document = fitz.open(stream=response.content, filetype="pdf")
            text = "\n".join(f"\n--- PDF PAGE {i+1} ---\n{page.get_text()}" for i, page in enumerate(document))
            record["pages"] = len(document)
        else:
            text = BeautifulSoup(response.text, "html.parser").get_text("\n", strip=True)
        (ROOT / Path(name).with_suffix(".txt")).write_text(text)
        receipts.append(record)
    (ROOT / "receipt.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps(receipts, indent=2))
