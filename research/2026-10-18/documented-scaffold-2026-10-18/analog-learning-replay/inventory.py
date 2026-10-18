"""Inventory retained native bytes and top-level MATLAB schema, never outcomes."""
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import platform
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def checked_members(archive):
    members = archive.infolist()
    if sum(item.file_size for item in members) > 256 * 1024 * 1024:
        raise ValueError("Archive exceeds frozen expanded-size limit")
    for item in members:
        path = PurePosixPath(item.filename)
        if path.is_absolute() or ".." in path.parts or stat.S_ISLNK(item.external_attr >> 16):
            raise ValueError("Unsafe archive entry: " + item.filename)
    damaged = archive.testzip()
    if damaged is not None:
        raise ValueError("ZIP CRC failure: " + damaged)
    return members


def main():
    import numpy
    import scipy
    from scipy.io import loadmat

    target = ROOT / "sources/native-inventory.json"
    if target.exists():
        raise FileExistsError(target)
    native = ROOT / "sources/browser-native/data.zip"
    records = []
    with zipfile.ZipFile(native) as archive:
        members = checked_members(archive)
        for item in members:
            if not item.filename.startswith("data/") or not item.filename.endswith(".mat"):
                continue
            record = dict(name=item.filename, bytes=item.file_size)
            try:
                data = loadmat(io.BytesIO(archive.read(item)))
                record["variables"] = {}
                for name, value in data.items():
                    if name in ("__header__", "__version__", "__globals__"):
                        continue
                    desc = dict(python_type=type(value).__name__, shape=list(value.shape),
                                dtype=str(value.dtype), fields=list(value.dtype.names or ()))
                    if type(value).__name__ == "MatlabOpaque":
                        desc["type_system"] = str(value["_TypeSystem"][0])
                        desc["class"] = str(value["_Class"][0])
                        desc["property_decoding"] = "unresolved; no MCOS mapping inferred"
                    record["variables"][name] = desc
            except Exception as error:
                record["parse_error"] = repr(error)
            records.append(record)
    result = dict(observed_utc=datetime.now(timezone.utc).isoformat(),
                  protocol_sha256=hashlib.sha256((ROOT / "PROTOCOL.md").read_bytes()).hexdigest(),
                  archive_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
                  zip_crc_ok=True, unsafe_entries=False,
                  archive_entries=[dict(name=i.filename, bytes=i.file_size, directory=i.is_dir()) for i in members],
                  expanded_bytes=sum(i.file_size for i in members), matlab_files=records,
                  runtime=dict(executable=sys.executable, python=platform.python_version(),
                               numpy=numpy.__version__, scipy=scipy.__version__),
                  numerical_outcome_replay=False, independent_generalization_verified=False)
    target.write_text(json.dumps(result, indent=2) + "\n")
    opaque = sum(any(v["python_type"] == "MatlabOpaque" for v in r.get("variables", {}).values()) for r in records)
    print(json.dumps(dict(zip_entries=len(members), matlab_files=len(records), opaque_files=opaque,
                          parse_errors=sum("parse_error" in r for r in records),
                          transparent_files=[r for r in records if not any(v["python_type"] == "MatlabOpaque" for v in r.get("variables", {}).values())]), indent=2))


if __name__ == "__main__":
    main()
