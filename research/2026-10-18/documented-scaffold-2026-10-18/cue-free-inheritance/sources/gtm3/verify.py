from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
import fitz

root = Path(__file__).resolve().parent
receipt = json.loads((root / "receipt.json").read_text())
checks = []
for record in receipt["records"]:
    data = (root / record["file"]).read_bytes()
    assert len(data) == record["bytes"], record["file"]
    assert hashlib.sha256(data).hexdigest() == record["sha256"], record["file"]
    checks.append({"scenario": "raw asset integrity", "artifact": record["file"], "pass": True})
for year, doi, pages in [(2024, "10.1021/acsami.4c14487", 14), (2025, "10.1021/jacs.5c12567", 15)]:
    article = ET.fromstring((root / f"{year}-article.xml").read_bytes())
    assert doi in [n.text for n in article.findall(".//article-id[@pub-id-type='doi']")]
    assert article.find(".//article-title") is not None
    assert len(fitz.open(root / f"{year}-supporting-information.pdf")) == pages
    checks.append({"scenario": "source identity and complete supplemental PDF", "year": year, "pages": pages, "pass": True})
failure = (root / "cattod-publisher-response.html").read_text()
assert "CPE00001" in failure and "CLOUDFLARE_ERROR_1000S_BOX" in failure
assert next(r for r in receipt["records"] if r["file"] == "cattod-publisher-response.html")["status"] == 403
checks.append({"scenario": "blocked source remains classified as failure", "pass": True})
main = fitz.open(root / "2025-main.pdf")
assert len(main) == 14
assert "Figure 1." in main[2].get_text()
assert "10.1021/jacs.5c12567" in main[2].get_text()
checks.append({"scenario": "2025 publisher PDF and Figure 1 location", "pass": True})
out = root / ".omo/evidence"
out.mkdir(parents=True, exist_ok=True)
(out / "verification.json").write_text(json.dumps({"invocation": "python3 sources/gtm3/verify.py", "checks": checks,
    "scientific_limit": "These checks verify provenance and acquisition, not functional inheritance or a chemical model."}, indent=2) + "\n")
print(f"PASS: {len(checks)} provenance checks; evidence={out / 'verification.json'}")
