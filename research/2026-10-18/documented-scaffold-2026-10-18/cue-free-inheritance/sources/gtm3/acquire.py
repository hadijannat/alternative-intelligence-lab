from pathlib import Path
import hashlib
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import zipfile
import io
import fitz

ROOT = Path(__file__).resolve().parent
records = []

def fetch(name, url):
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        data, status = error.read(), error.code
    except (urllib.error.URLError, TimeoutError) as error:
        records.append({"file": name, "url": url, "error": str(error)})
        return None
    (ROOT / name).write_bytes(data)
    records.append({"file": name, "url": url, "status": status,
                    "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return data if status == 200 else None

fetch("cattod-publisher-response.html", "https://www.sciencedirect.com/science/article/pii/S0920586123004133")
for year, pmc, doi in [("2024", "PMC11472255", "10.1021/acsami.4c14487"),
                       ("2025", "PMC12550838", "10.1021/jacs.5c12567")]:
    base = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}"
    data = fetch(f"{year}-article.xml", base + "/fullTextXML")
    if data:
        tree = ET.fromstring(data)
        assert doi in " ".join(tree.itertext()), doi
        paragraphs = []
        for node in tree.findall(".//body//p") + tree.findall(".//body//table-wrap"):
            paragraphs.append(" ".join("".join(node.itertext()).split()))
        (ROOT / f"{year}-body.txt").write_text("\n\n".join(paragraphs))
    archive = fetch(f"{year}-supplementary.zip", base + "/supplementaryFiles")
    if archive:
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            members = [m for m in z.namelist() if m.endswith("_si_001.pdf")]
            assert len(members) == 1, members
            pdf = z.read(members[0])
            assert pdf.startswith(b"%PDF")
            (ROOT / f"{year}-supporting-information.pdf").write_bytes(pdf)
            doc = fitz.open(stream=pdf, filetype="pdf")
            (ROOT / f"{year}-supporting-information.txt").write_text("\n".join(
                f"PAGE {i+1}\n{page.get_text()}" for i, page in enumerate(doc)))
            records.append({"file": f"{year}-supporting-information.pdf",
                            "archive_member": members[0], "pages": len(doc),
                            "bytes": len(pdf), "sha256": hashlib.sha256(pdf).hexdigest()})
(ROOT / "receipt.json").write_text(json.dumps({"checked_date": "2026-10-18",
    "scope": "Three follow-up sources; original JACS 2022 package remains in sibling functional-carrier-search.",
    "web_reader_failures": ["ScienceDirect 403", "PMC browser CAPTCHA", "UCL PDF 429"],
    "records": records}, indent=2) + "\n")
print(json.dumps(records, indent=2))
