"""Verify retained sources and the proposed closed-bath algebra; no model fitting."""
from pathlib import Path
import hashlib
import json
import math
from xml.etree import ElementTree
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent


def main():
    ledger = json.loads((HERE / "sources.json").read_text())
    checked = {}
    for group in ("source_input_sha256", "acquired_sha256"):
        for name, expected in ledger[group].items():
            digest = hashlib.sha256((WORKSPACE / name).read_bytes()).hexdigest()
            assert digest == expected, name
            checked[name] = digest
    article = (WORKSPACE / "measured-coupling-2026-10-15/rna_sources/raw/salibi.txt").read_text()
    supplement = (WORKSPACE / "measured-coupling-2026-10-15/rna_sources/raw/salibi_si.txt").read_text()
    assert "No exogenous full-length ribozyme was added in later generations." in article
    assert "Samples were subsequently washed twice" in article
    assert "Collected samples" in supplement and "were washed with outer phase buffer" in supplement
    assert "half the volume was sampled and the other half was transferred" in supplement
    litschel = (HERE / "raw/litschel2018.txt").read_text()
    assert "even for large molecules up to 40 kDa" in litschel
    tsuji = (HERE / "raw/tsuji2026_vor.txt").read_text()
    assert "Qβ replicase provided as substrates" in tsuji
    assert "provided as Supplementary Data" in tsuji
    assert len(ledger["new_models_recommended_not_implemented_here"]) == 3
    assert ledger["fixed_sensitivity"]["primary"] == ["reactive", "carried"]
    inventory = json.loads((HERE / "dataset_inventory.json").read_text())
    namespace = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(WORKSPACE / inventory["workbook"]) as workbook:
        strings = ["".join(item.itertext()) for item in ElementTree.fromstring(workbook.read("xl/sharedStrings.xml"))]
        for sheet in inventory["sheets"]:
            cells = {}
            for cell in ElementTree.fromstring(workbook.read(sheet["xml_member"])).findall(".//s:c", namespace):
                value = cell.find("s:v", namespace)
                if value is not None:
                    cells[cell.attrib["r"]] = strings[int(value.text)] if cell.attrib.get("t") == "s" else value.text
            row_number = lambda address: int("".join(filter(str.isdigit, address)))
            assert len({row_number(address) for address in cells}) - 1 == sheet["nonempty_data_rows"]
            assert {address: value for address, value in cells.items() if row_number(address) == 1} == sheet["headers"]
            for address, expected in sheet.get("selected_cells", {}).items():
                assert cells[address] == expected, (sheet["sheet"], address)
    cases = []
    for nu in (0.82, 1.0, 2.0, 5.0, 20.0, 100.0):
        kappa = -nu / (3 * (nu + 1)) * math.log((0.55 * (nu + 1) - 1) / nu)
        retention = (1 + nu * math.exp(-3 * kappa * (1 + 1 / nu))) / (1 + nu)
        assert kappa > 0 and abs(retention - 0.55) < 1e-12
        # At equilibrium, conserved tracer occupies both aqueous volumes.
        assert 1 / (1 + nu) < retention
        cases.append({"nu": nu, "kappa": kappa, "retention_after_three": retention})
    patch_cases = []
    weights, inside, exterior = (0.2, 0.3, 0.5), (0.0, 2.0, 7.5), (1.5, 0.0, 3.0)
    mean_exterior = sum(w * e for w, e in zip(weights, exterior))
    for nu in (1.0, 2.0, 20.0):
        for diffusion in (0.0, 0.3, 7.0):
            kappa = 0.7
            flux = sum(w * (kappa * (e - c) + nu * ((kappa / nu) * (c - e) + diffusion * (mean_exterior - e))) for w, c, e in zip(weights, inside, exterior))
            assert abs(flux) < 1e-12
            before = nu * mean_exterior
            homogenized = sum(w * nu * mean_exterior for w in weights)
            assert abs(before - homogenized) < 1e-12
            after_transfer = sum(w * nu * mean_exterior / 2 for w in weights)
            assert abs(after_transfer - before / 2) < 1e-12
            patch_cases.append({"nu": nu, "D": diffusion, "total_inventory_flux": flux})
    receipt = {
        "status": "PASS",
        "source_hashes_checked": checked,
        "closed_bath_algebra_cases": cases,
        "effective_patch_conservation_cases": patch_cases,
        "dataset_sheets_checked": len(inventory["sheets"]),
        "dataset_data_rows_checked": sum(sheet["nonempty_data_rows"] for sheet in inventory["sheets"]),
        "dataset_inventory_sha256": hashlib.sha256((HERE / "dataset_inventory.json").read_bytes()).hexdigest(),
        "not_checked": ["Experimental validity of bath assumptions", "Unavailable raw Peter microscopy data", "Measured transport fit"],
        "verification_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_ledger_sha256": hashlib.sha256((HERE / "sources.json").read_bytes()).hexdigest(),
    }
    (HERE / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "source_hash_count": len(checked), "bath_algebra_cases": len(cases), "patch_conservation_cases": len(patch_cases), "dataset_sheets": len(inventory["sheets"])}))


if __name__ == "__main__":
    main()
