"""Download primary sources with content validation and a reproducible receipt."""
from pathlib import Path
import hashlib
import json
import requests
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "elife_metadata.json": "https://api.elifesciences.org/articles/83543",
    "edmond_metadata.json": "https://edmond.mpg.de/api/datasets/:persistentId/?persistentId=doi%3A10.17617%2F3.G6KSU2",
    "levay_exchange.zip": "https://cdn.elifesciences.org/articles/83543/elife-83543-fig3-figsupp2-data1-v2.zip",
    "ghosh_phase_concentrations.xlsx": "https://edmond.mpg.de/api/access/datafile/315224",
    "ghosh_dilute_concentrations.txt": "https://edmond.mpg.de/api/access/datafile/315264",
    "ghosh_rates.txt": "https://edmond.mpg.de/api/access/datafile/315232",
    "ghosh_whole_solution_rates.txt": "https://edmond.mpg.de/api/access/datafile/315165",
    "ghosh_partition_coefficients.xlsx": "https://edmond.mpg.de/api/access/datafile/315202",
    "ghosh_supernatant_fit.xlsx": "https://edmond.mpg.de/api/access/datafile/315001",
    "ghosh_si.pdf": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-63656-z/MediaObjects/41467_2025_63656_MOESM1_ESM.pdf",
    "levay2023.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10275638/fullTextXML",
    "coacervates2025.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12489098/fullTextXML",
    "dasgupta2023.html": "https://chemistry-europe.onlinelibrary.wiley.com/doi/full/10.1002/chem.202301376",
    "dasgupta2023_si.pdf": "https://chemistry-europe.onlinelibrary.wiley.com/doi/suppl/10.1002/chem.202301376/supinfo/chem202301376-sup-0001-misc_information.pdf",
    "peter2023.html": "https://onlinelibrary.wiley.com/doi/full/10.1002/anie.202218507",
}

def main():
    (ROOT / "raw").mkdir(parents=True, exist_ok=True)
    receipts = []
    for name, url in SOURCES.items():
        target = ROOT / "raw" / name
        receipt = {"file": str(target.relative_to(ROOT)), "url": url, "client_date": "2026-10-15"}
        if target.exists():
            content = target.read_bytes()
            receipt["status"] = "retained"
        else:
            try:
                response = requests.get(url, timeout=60)
                content = response.content
                valid = response.ok and (content.startswith(b"%PDF") if name.endswith(".pdf") else content.startswith(b"PK") if name.endswith((".zip", ".xlsx")) else b"<article" in content if name.endswith(".xml") else content.startswith(b"{") if name.endswith(".json") else b"<html" not in content.lower() if name.endswith(".txt") else b"RNA" in content and b"captcha" not in content.lower())
                receipt.update(http_status=response.status_code, final_url=response.url)
                if not valid:
                    receipt.update(status="rejected", bytes=len(content), response_prefix=content[:100].decode(errors="replace"))
                    receipts.append(receipt)
                    continue
                target.write_bytes(content)
                receipt["status"] = "downloaded"
            except requests.RequestException as error:
                receipt.update(status="failed", error=str(error))
                receipts.append(receipt)
                continue
        receipt.update(bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        receipts.append(receipt)
        if name.endswith(".xml"):
            tree = ET.fromstring(content)
            paragraphs = ["".join(e.itertext()) for e in tree.iter() if e.tag in {"title", "p", "caption"}]
            target.with_suffix(".txt").write_text("\n\n".join(paragraphs))
    (ROOT / "retrieval_receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps(receipts, indent=2))

if __name__ == "__main__":
    main()
