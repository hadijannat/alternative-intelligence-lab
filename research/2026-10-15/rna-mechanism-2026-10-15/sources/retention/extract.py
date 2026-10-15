"""Normalize source coordinates; reject ambiguous units rather than invent rates."""
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile
import openpyxl
import pymupdf

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"

def write_csv(name, rows):
    with (ROOT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    checks = []
    for receipt in json.loads((ROOT / "retrieval_receipts.json").read_text()):
        if "sha256" in receipt:
            path = ROOT / receipt["file"]
            assert path.stat().st_size > 0
            assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"]
            checks.append({"scenario": "retained primary source integrity", "artifact": receipt["file"], "pass": True})
    archive = zipfile.ZipFile(RAW / "levay_exchange.zip")
    member = "Figure 3 - supplement 2-3/Figure 3 - supplement 2-3 - source data 1.xlsx"
    sheet = openpyxl.load_workbook(io.BytesIO(archive.read(member)), data_only=True).active
    assert sheet["K1"].value == "PCCpop" and sheet["M1"].value == "PCCdroplet"
    exchange = []
    for row in range(2, 18):
        record = {"ribozyme_state": sheet[f"A{row}"].value, "peptide_ratio": sheet[f"B{row}"].value,
                  "time_h": float(sheet[f"C{row}"].value.split()[0]),
                  "PCC_population": sheet[f"K{row}"].value, "PCC_population_SEM": sheet[f"L{row}"].value,
                  "PCC_droplet": sheet[f"M{row}"].value, "PCC_droplet_SEM": sheet[f"N{row}"].value,
                  "source": "raw/levay_exchange.zip", "member": member,
                  "sheet": sheet.title, "coordinate": f"A{row}:N{row}",
                  "observer": "labelled substrate/concatemer mixing; not active catalyst retention"}
        assert -1 <= record["PCC_population"] <= 1 and -1 <= record["PCC_droplet"] <= 1
        exchange.append(record)
    assert len(exchange) == 16
    write_csv("levay_exchange.csv", exchange)
    checks.append({"scenario": "four condition groups each at four times, exact workbook cells", "count": len(exchange), "pass": True})

    kinetics = []
    peptide = None
    for line_number, line in enumerate((RAW / "ghosh_rates.txt").read_text().splitlines(), 1):
        fields = line.split("\t")
        if len(fields) < 6:
            continue
        if fields[1].strip().startswith("P-") and fields[2].strip().replace(".", "", 1).isdigit():
            peptide = fields[1].strip()
        if peptide is None:
            continue
        try:
            time, substrate, product, percent = map(float, fields[2:6])
        except ValueError:
            continue
        if time not in [2, 5, 10, 15, 20, 30, 45, 60, 120, 240, 360]:
            continue
        assert abs(100 * product / (substrate + product) - percent) < 1e-6
        assert 0 <= percent <= 100
        kinetics.append({"peptide": peptide, "time_min": time, "substrate_intensity": substrate,
                         "product_intensity": product, "cleavage_percent": percent,
                         "source": "raw/ghosh_rates.txt", "line": line_number,
                         "columns_1based": "3:6", "observer": "gel fraction in pellet containing dense and dilute phases; representative series"})
    assert len(kinetics) == 77 and len({r["peptide"] for r in kinetics}) == 7
    write_csv("ghosh_pellet_cleavage.csv", kinetics)
    checks.append({"scenario": "77 numerical gel fractions reconstructed from raw band intensities", "maximum_allowed_absolute_error_percent": 1e-6, "pass": True})

    sheet = openpyxl.load_workbook(RAW / "ghosh_phase_concentrations.xlsx", data_only=True).active
    assert sheet["H1"].value == "[hhRNA]_dil_uMce" and sheet["L1"].value == "[hhRNA]_cond_uMce"
    phases = []
    for row in range(2, 9):
        dilute, dense = sheet[f"H{row}"].value, sheet[f"L{row}"].value
        phases.append({"peptide": sheet[f"A{row}"].value,
                       "HH_dilute_uM_charge_equivalents": dilute, "HH_dilute_error_uMce": sheet[f"I{row}"].value,
                       "HH_condensed_uM_charge_equivalents": dense, "HH_condensed_error_uMce": sheet[f"M{row}"].value,
                       "derived_dense_dilute_ratio": dense / dilute,
                       "source": "raw/ghosh_phase_concentrations.xlsx", "sheet": sheet.title,
                       "coordinate": f"H{row}:M{row}",
                       "observer": "fluorescent HH partition/QPI composition; active fraction not directly measured"})
        assert dense > dilute > 0
    write_csv("ghosh_HH_phase_concentrations.csv", phases)
    checks.append({"scenario": "7 source phase compositions kept in charge-equivalent units", "pass": True})
    document = pymupdf.open(RAW / "ghosh_si.pdf")
    text = "\n\n".join(f"PDF PAGE {i + 1}\n" + page.get_text() for i, page in enumerate(document))
    (RAW / "ghosh_si.txt").write_text(text)
    assert "units of charge concentration" in text
    assert "does not provide an" in text and "absolute value" in text
    checks.append({"scenario": "SI explicitly defines charge units and limits inferred rates", "pass": True})
    result = {"status": "PASS", "invocation": "python3 rna-mechanism-2026-10-15/sources/retention/extract.py",
              "checks": checks, "normalized_rows": {"exchange": 16, "cleavage": 77, "phase_compositions": 7},
              "limits": ["No fitting", "No active fraction inferred from fluorescence", "No transfer of kinetic constants to R3C/POPC"]}
    evidence = ROOT / ".omo" / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
