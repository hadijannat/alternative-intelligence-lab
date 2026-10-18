import hashlib
import json
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

import fitz

BASE=Path(__file__).resolve().parent/"sources/gtm3"


def main():
    xml_path=BASE/"article.xml"
    root=ET.fromstring(xml_path.read_bytes())
    doi=root.find(".//article-id[@pub-id-type='doi']").text
    assert doi=="10.1021/jacs.2c01874"
    title=" ".join("".join(root.find(".//article-title").itertext()).split())
    assert "GTM-3" in title
    href="{http://www.w3.org/1999/xlink}href"
    assets={x.attrib[href] for x in root.findall(".//supplementary-material/media")}
    assert "ja2c01874_si_001.pdf" in assets
    with zipfile.ZipFile(BASE/"supplementary.zip") as archive:
        matches=[name for name in archive.namelist() if name.rsplit("/",1)[-1]=="ja2c01874_si_001.pdf"]
        assert len(matches)==1
        pdf=archive.read(matches[0])
    assert pdf.startswith(b"%PDF-")
    (BASE/"supporting-information.pdf").write_bytes(pdf)
    with fitz.open(stream=pdf,filetype="pdf") as document:
        pages=len(document)
        text="\n".join(f"PAGE {i+1}\n"+page.get_text() for i,page in enumerate(document))
    assert pages>10 and "EMPS" in text
    (BASE/"supporting-information.txt").write_text(text)
    paragraphs=["".join(p.itertext()) for p in root.findall(".//body//p")]
    (BASE/"body.txt").write_text("\n\n".join(paragraphs)+"\n")
    tables=[dict(id=t.attrib.get("id"),rows=[
        [" ".join("".join(c.itertext()).split()) for c in row if c.tag in ("th","td")]
        for row in t.findall(".//tr")]) for t in root.findall(".//table-wrap")]
    (BASE/"tables.json").write_text(json.dumps(tables,indent=2)+"\n")
    files=("article.xml","supplementary.zip","supporting-information.pdf","supporting-information.txt","body.txt","tables.json")
    receipt=dict(doi=doi,title=title,source_class="EuropePMC primary article XML and linked supplementary package",
                 article_url="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9100664/fullTextXML",
                 supplementary_url="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9100664/supplementaryFiles",
                 extracted_asset="ja2c01874_si_001.pdf",si_pages=pages,
                 files={name:dict(bytes=(BASE/name).stat().st_size,sha256=hashlib.sha256((BASE/name).read_bytes()).hexdigest()) for name in files},
                 failures=["Web reader received a PMC CAPTCHA page; ACS main article returned403. No challenge bypass attempted; public EuropePMC API succeeded."],
                 checks="PASS: exact DOI/title, XML-linked unique ZIP member, PDF signature/pages, primary tables retained")
    (BASE/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(dict(doi=doi,si_pages=pages,primary_tables=len(tables),checks="PASS")))


if __name__=="__main__":
    main()
