"""Acquire primary mechanistic references without importing their rates into Salibi."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
SOURCES={"robertson2014":"PMC3943892", "ferretti2013":"PMC3579227"}


def main():
    receipts=[]
    for name, pmcid in SOURCES.items():
        url=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
        path=ROOT/(name+".xml")
        record=dict(url=url,file=path.name,retrieved_utc=datetime.now(timezone.utc).isoformat())
        try:
            if path.exists():
                content=path.read_bytes()
            else:
                with urlopen(Request(url,headers={"User-Agent":"research-data-audit/1.0"}),timeout=45) as response:
                    content=response.read()
                assert b"<article" in content[:1000]
                path.write_bytes(content)
            root=ET.fromstring(content)
            text="\n\n".join("".join(e.itertext()) for e in root.iter() if e.tag in {"title","p","caption","table-wrap"})
            (ROOT/(name+".txt")).write_text(text)
            record.update(status="retained primary XML",bytes=len(content),sha256=hashlib.sha256(content).hexdigest())
        except Exception as error:
            record.update(status="failed",error=str(error))
        receipts.append(record)
    (ROOT/"mechanism_retrieval.json").write_text(json.dumps(receipts,indent=2)+"\n")
    print(json.dumps(receipts,indent=2))


if __name__=="__main__":
    main()
