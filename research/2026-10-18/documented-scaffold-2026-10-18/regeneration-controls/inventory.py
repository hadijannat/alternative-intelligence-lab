from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "founder-repair-search/sources/repair/poli2025"


def number(value):
    return float(value.replace(",", "."))


def gamry(blob):
    lines = blob.decode("utf-8", errors="replace").splitlines()
    tables = []
    headers = {}
    first_table = next((i for i, line in enumerate(lines) if line.split("\t")[1:2] == ["TABLE"]), len(lines))
    allowed = {"TAG", "TITLE", "DATE", "TIME", "PSTAT", "SEQUENCER", "AREA", "TSTEP1", "TSTEP2", "TPRESTEP", "SAMPLETIME", "FRAMEWORKVERSION"}
    for line in lines[:first_table]:
        fields = line.split("\t")
        if fields[0] in allowed:
            headers[fields[0]] = fields[1:]
    for i, line in enumerate(lines):
        if line.split("\t")[1:2] != ["TABLE"]:
            continue
        marker = line.split("\t")
        columns = lines[i + 1].strip().split("\t")
        units = lines[i + 2].strip().split("\t")
        time_index = next((j for j, name in enumerate(columns) if name in ("T", "Time", "Time/s")), None)
        times = []
        rows = 0
        malformed = 0
        for raw in lines[i + 3:]:
            fields = raw.strip().split("\t")
            if not fields or not re.fullmatch(r"\d+", fields[0]):
                break
            rows += 1
            if len(fields) != len(columns):
                malformed += 1
            if time_index is not None and time_index < len(fields):
                times.append(number(fields[time_index]))
        tables.append({"name": marker[0], "declared_rows": int(marker[2]) if len(marker) > 2 and marker[2] else None, "rows": rows,
                       "columns": columns, "units": units, "malformed_width_rows": malformed,
                       "time_min_s": min(times) if times else None, "time_max_s": max(times) if times else None,
                       "time_monotonic": all(b >= a for a, b in zip(times, times[1:])) if times else None})
    return headers, tables


def inspect(blob, suffix):
    if not blob:
        return {"native_format": "empty", "magic_hex": ""}
    result = {"magic_hex": blob[:16].hex()}
    if blob.startswith(b"EXPLAIN"):
        headers, tables = gamry(blob)
        result.update(native_format="Gamry plaintext", headers=headers, tables=tables)
    elif blob.startswith(b"CPYUA"):
        result["native_format"] = "Origin OPJU (CPYUA magic)"
    elif blob.startswith(b"PK"):
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            assert archive.testzip() is None
            names = archive.namelist()
            result["native_format"] = "XLSX" if "xl/workbook.xml" in names else "ZIP"
            result["zip_crc_ok"] = True
            if "xl/workbook.xml" in names:
                xml = ET.fromstring(archive.read("xl/workbook.xml"))
                result["sheets"] = [x.attrib["name"] for x in xml.iter() if x.tag.endswith("}sheet")]
                result["worksheet_structure"] = []
                for name in names:
                    if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name):
                        sheet = ET.fromstring(archive.read(name))
                        result["worksheet_structure"].append({"part": name,
                            "dimensions": [x.attrib["ref"] for x in sheet.iter() if x.tag.endswith("}dimension")],
                            "row_elements": sum(x.tag.endswith("}row") for x in sheet.iter())})
    else:
        result["native_format"] = "plaintext" if b"\x00" not in blob[:4096] else "unclassified binary"
        if suffix == ".txt" and blob.startswith(b"Hours"):
            lines = blob.decode("utf-8", errors="replace").splitlines()
            times = [number(x.split("\t")[0]) for x in lines[1:] if x.strip()]
            result.update(columns=lines[0].split("\t"), rows=len(times),
                          time_min_h=min(times), time_max_h=max(times),
                          time_monotonic=all(b >= a for a, b in zip(times, times[1:])))
    return result


def main():
    receipt = json.loads((SOURCE / "data-receipt.json").read_text())
    deposit = json.loads((SOURCE / "dataverse.json").read_text())["data"]["latestVersion"]["files"]
    metadata = {x["dataFile"]["id"]: x for x in deposit}
    files = []
    for item in sorted(receipt, key=lambda x: x["path"]):
        path = SOURCE / item["path"]
        blob = path.read_bytes()
        meta = metadata[item["id"]]["dataFile"]
        check = meta["checksum"]
        actual = hashlib.new(check["type"].lower().replace("-", ""), blob).hexdigest()
        sha256 = hashlib.sha256(blob).hexdigest()
        assert actual == check["value"] and sha256 == item["sha256"]
        assert len(blob) == meta["filesize"] == item["bytes"]
        parts = Path(item["path"]).parts
        files.append({"id": item["id"], "path": item["path"], "bytes": len(blob),
                      "sha256": sha256, "repository_checksum": check, "checksum_ok": True,
                      "deposit_mime": meta["contentType"], "group": parts[1] if len(parts) > 2 else None,
                      "specimen": parts[2] if len(parts) > 3 else None, **inspect(blob, path.suffix.lower())})
    assert len(files) == 481
    actual_paths = {str(x.relative_to(SOURCE)) for x in (SOURCE / "data").rglob("*") if x.is_file()}
    assert actual_paths == {x["path"] for x in files}
    hashes = defaultdict(list)
    for item in files:
        hashes[item["sha256"]].append(item["path"])
    summary = {"acquired_files": len(files), "deposit_files": len(deposit), "bytes": sum(x["bytes"] for x in files),
               "all_checksums_ok": True, "native_formats": dict(Counter(x["native_format"] for x in files)),
               "empty_paths": [x["path"] for x in files if not x["bytes"]],
               "duplicate_byte_groups": [v for v in hashes.values() if len(v) > 1],
               "row_count_mismatches": [{"path": x["path"], "table": t["name"], "declared": t["declared_rows"], "parsed": t["rows"]} for x in files for t in x.get("tables", []) if t["declared_rows"] is not None and t["declared_rows"] != t["rows"]],
               "tables_without_declared_count": [{"path": x["path"], "table": t["name"], "parsed": t["rows"]} for x in files for t in x.get("tables", []) if t["declared_rows"] is None],
               "selfchecks": "PASS: synthetic comma-decimal Gamry table, zero-byte, source hashes, repository hashes, exact acquired-path coverage"}
    (ROOT / "file_manifest.json").write_text(json.dumps({"summary": summary, "files": files}, indent=2) + "\n")
    with (ROOT / "file_manifest.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "path", "bytes", "sha256", "checksum_ok", "native_format", "group", "specimen"])
        writer.writeheader()
        writer.writerows({key: item[key] for key in writer.fieldnames} for item in files)
    print(json.dumps({key: value for key, value in summary.items() if key != "tables_without_declared_count"}, indent=2))


if __name__ == "__main__":
    fake = b"EXPLAIN\nTAG\tCHRONOA\nCURVE\tTABLE\t2\n\tPt\tT\tVf\n\t#\ts\tV\n\t0\t0,0\t123\n\t1\t2,5\t456\n"
    headers, tables = gamry(fake)
    assert headers["TAG"] == ["CHRONOA"]
    assert tables[0]["rows"] == 2 and tables[0]["time_max_s"] == 2.5
    assert "123" not in json.dumps(tables) and "456" not in json.dumps(tables)
    assert gamry(fake.replace(b"CURVE\tTABLE\t2", b"CURVE\tTABLE"))[1][0]["rows"] == 2
    assert inspect(b"", ".dta")["native_format"] == "empty"
    main()
