"""Verify one acquired primary PDF and preserve failed-route/source-unit evidence."""
import hashlib
import json
from pathlib import Path
import re

import fitz

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    failed = json.loads((ROOT / "receipt.json").read_text())["requests"]
    native = json.loads((ROOT / "browser-main-receipt.json").read_text())["requests"][0]
    checks = {}
    for record in failed + [native]:
        data = (ROOT / record["name"]).read_bytes()
        checks[record["name"] + "_unchanged"] = (
            len(data) == record["bytes"] and hashlib.sha256(data).hexdigest() == record["sha256"])
    checks["four_failed_routes_preserved"] = len(failed) == 4 and all(r["status"] == 403 for r in failed)
    data = (ROOT / native["name"]).read_bytes()
    checks["native_pdf_signature"] = native["status"] == 200 and data.startswith(b"%PDF")
    with fitz.open(stream=data, filetype="pdf") as document:
        texts = [page.get_text() for page in document]
        checks["eleven_pages"] = len(document) == 11
        checks["title"] = "Phosphate" in texts[0] and "stainless" in texts[0]
        checks["exact_doi"] = "10.1039/d6ta02355j" in " ".join(texts).lower()
        (ROOT / "nishioka-main.txt").write_text("\n".join(
            f"--- PDF PAGE {i + 1}; JOURNAL PAGE {23803 + i} ---\n" + text
            for i, text in enumerate(texts)))
        for page_number in (3, 6, 7, 8, 9, 10):
            document[page_number - 1].get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(
                ROOT / f"nishioka-page-{page_number}.png")
    unit_mentions = [dict(pdf_page=i + 1, journal_page=23803 + i, unit=m.group(1))
                     for i, text in enumerate(texts)
                     for m in re.finditer(r"0\.399\s*(m?C)", text)]
    unit_audit = dict(mentions=unit_mentions, literal_unit_ratio=1000,
                      disposition="Source inconsistency retained; no corrected capacity selected for analysis")
    checks["both_capacity_unit_readings_retained"] = {r["unit"] for r in unit_mentions} == {"C", "mC"}
    result = dict(checks=checks, all_pass=all(checks.values()), native_pdf= native["name"],
                  native_sha256=native["sha256"], capacity_unit_audit=unit_audit,
                  full_text_extracted=True, response_points_selected_for_analysis=0,
                  empirical_holdout_validation=False, scientific_validation=False,
                  missing_native=["Nishioka supplement", "Stevens main", "Cimino main"])
    (ROOT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(all_pass=result["all_pass"], checks=len(checks), native_sha256=native["sha256"],
                          unit_mentions=unit_mentions, failed=[k for k, v in checks.items() if not v]), indent=2))
    assert result["all_pass"], "Source verification failed; inspect retained artifact"
