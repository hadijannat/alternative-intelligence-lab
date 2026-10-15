"""Retrieve primary-source artifacts; preserve failed access and file hashes."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
SOURCES = {
    "ameta.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10167250/fullTextXML",
    "salibi.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9984477/fullTextXML",
    "ameta_si.pdf": "https://static-content.springer.com/esm/art%3A10.1038%2Fs42004-023-00887-5/MediaObjects/42004_2023_887_MOESM1_ESM.pdf",
    "salibi_si.pdf": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-36940-z/MediaObjects/41467_2023_36940_MOESM1_ESM.pdf",
    "salibi_data.xlsx": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-36940-z/MediaObjects/41467_2023_36940_MOESM8_ESM.xlsx",
}

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    receipts = []
    for name, url in SOURCES.items():
        destination = RAW / name
        if destination.exists():
            content = destination.read_bytes()
            receipts.append({"file": str(destination.relative_to(ROOT)), "url": url,
                             "status": "existing retained", "bytes": len(content),
                             "sha256": hashlib.sha256(content).hexdigest()})
            continue
        started = datetime.now(timezone.utc).isoformat()
        try:
            response = requests.get(url, timeout=90)
        except requests.RequestException as error:
            receipts.append({"file": str(destination.relative_to(ROOT)), "url": url,
                             "retrieved_utc": started, "status": "request failed", "error": str(error)})
            continue
        receipt = {"file": str(destination.relative_to(ROOT)), "url": url,
                   "retrieved_utc": started, "http_status": response.status_code,
                   "final_url": response.url, "content_type": response.headers.get("Content-Type")}
        content = response.content
        expected = content.startswith(b"%PDF") if name.endswith(".pdf") else (
            content.startswith(b"PK") if name.endswith(".xlsx") else b"<article" in content[:1000])
        if response.ok and expected:
            destination.write_bytes(content)
            receipt.update(status="downloaded", bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        else:
            receipt.update(status="rejected response", snippet=response.text[:200])
        receipts.append(receipt)
    (ROOT / "retrieval_receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
    for name in ["ameta", "salibi"]:
        path = RAW / (name + ".xml")
        if path.exists():
            tree = ET.fromstring(path.read_bytes())
            text = "\n\n".join("".join(e.itertext()) for e in tree.iter() if e.tag in {"title", "p", "caption"})
            (RAW / (name + ".txt")).write_text(text)
    print(json.dumps(receipts, indent=2))

if __name__ == "__main__":
    main()
