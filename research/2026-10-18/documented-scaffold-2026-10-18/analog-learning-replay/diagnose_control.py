"""Inventory control-flag encoding after a stopped replay; no response errors."""
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

import numpy as np
from matio import load_from_mat

ROOT = Path(__file__).resolve().parent


def main():
    output = ROOT / "results/control-schema.json"
    if output.exists():
        raise FileExistsError(output)
    native = ROOT / "sources/browser-native/data.zip"
    assert hashlib.sha256(native.read_bytes()).hexdigest() == "f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c"
    schema = json.loads((ROOT / "results/property-schema-all.json").read_text())["records"]
    rows = []
    with zipfile.ZipFile(native) as archive, tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "native.mat"
        for record in schema:
            if not record["qualified_schema"]:
                continue
            path.write_bytes(archive.read(record["member"]))
            p = load_from_mat(path, variable_names=["experiment"], raw_data=True)["experiment"].properties
            flags = np.asarray(p["DOTEST"]).ravel()
            values, counts = np.unique(flags, return_counts=True)
            rows.append(dict(member=record["member"],
                flag_counts={str(v): int(n) for v, n in zip(values, counts)},
                nonfinite_indices=np.flatnonzero(~np.isfinite(flags)).tolist(),
                nonbinary_finite_indices=np.flatnonzero(np.isfinite(flags) & ~np.isin(flags, (0, 1))).tolist()))
    result = dict(records=rows, numerical_response_replay=False,
                  reason="First replay stopped on unverified DOTEST encoding; no rule changed here")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(objects=len(rows), patterns=sorted({json.dumps(r["flag_counts"], sort_keys=True) for r in rows}),
                          nonfinite_patterns=sorted({tuple(r["nonfinite_indices"]) for r in rows}),
                          nonbinary_finite=sum(bool(r["nonbinary_finite_indices"]) for r in rows)), indent=2))


if __name__ == "__main__":
    main()
