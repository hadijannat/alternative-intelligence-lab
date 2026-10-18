import csv
import hashlib
import json
from pathlib import Path

import fitz
from bs4 import BeautifulSoup


def verify() -> dict:
    directory = Path(__file__).resolve().parent
    soup = BeautifulSoup((directory / "zheng2014-main.html").read_bytes(), "html.parser")
    assert "Mechanism of seeding in hydrothermal synthesis" in soup.get_text()
    tables = [table for table in soup.find_all("table") if not table.find("table")]
    cells = [
        [[cell.get_text("", strip=True) for cell in row.find_all(["td", "th"])]
         for row in tables[index].find_all("tr")]
        for index in (1, 4)
    ]
    exact = json.loads((directory / "tables-exact.json").read_text())
    assert cells == [exact["table1"], exact["table2"]]
    with (directory / "seed-product-table.csv").open(newline="") as stream:
        joined = list(csv.reader(stream))[1:]
    seeds, products = cells[0][3:13], cells[1][2:12]
    assert len(joined) == len(seeds) == len(products) == 10
    for row, seed, product in zip(joined, seeds, products, strict=True):
        expected = [seed[0], product[0], seed[4], seed[5], seed[6], seed[7],
                    seed[9], seed[10], *product[2:]]
        normalized = [value.replace("∞", "inf").replace("—", "NA").replace("−", "-")
                      for value in expected]
        assert row == normalized, (row, normalized)
        assert seed[0] == product[1]
    with fitz.open(directory / "zheng2014-main.pdf") as document:
        assert len(document) == 11
        assert "Table 1" in document[2].get_text()
        assert "Table 2" in document[3].get_text()
    receipt = json.loads((directory / "receipt.json").read_text())
    for artifact in receipt["artifacts"]:
        content = (directory / artifact["path"]).read_bytes()
        assert content and len(content) == artifact["bytes"]
        assert hashlib.sha256(content).hexdigest() == artifact["sha256"]
    return {"status": "PASS", "scenario": "primary package and ten-row table join",
            "checks": {"pdf_pages": 11, "joined_rows": 10,
                       "html_tables_equal_archived_extraction": True,
                       "csv_cells_match_primary_tables": True,
                       "receipt_hashes_match": True},
            "limits": "No model fit, chemical validation, independent replicates or serial-transfer assay."}


if __name__ == "__main__":
    result = verify()
    output = Path(__file__).resolve().parent / ".omo/evidence/verification.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
