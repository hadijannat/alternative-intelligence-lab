"""Extract article pages from the public combined PDF without retaining the large PDF."""
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import urllib.request
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
URL = "https://ars.els-cdn.com/content/image/1-s2.0-S2451929425004073-mmc2.pdf?download=true"


def main():
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    assert data.startswith(b"%PDF-")
    pdf = PdfReader(io.BytesIO(data))
    text = "\n\n".join(f"=== COMBINED PDF PAGE {i+1} ===\n" + page.extract_text()
                          for i, page in enumerate(pdf.pages[:14])).replace("\x00", "")
    (ROOT / "article.txt").write_text(text)
    metadata = {"url": URL, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                "source_bytes": len(data), "source_sha256": hashlib.sha256(data).hexdigest(),
                "source_pdf_pages": len(pdf.pages), "license": "CC BY 4.0",
                "retained": "Text of first 14 PDF pages (article plus graphical abstract); source PDF not retained to keep local data below 30MB",
                "text_sha256": hashlib.sha256(text.encode()).hexdigest()}
    (ROOT / "article_manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Extracted 14 of {len(pdf.pages)} pages; source {len(data)} bytes not retained")


if __name__ == "__main__":
    main()
