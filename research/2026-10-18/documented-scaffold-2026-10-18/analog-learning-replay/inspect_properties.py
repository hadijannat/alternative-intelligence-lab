"""Inspect named MCOS properties and metadata, without response calculations."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import tempfile
import warnings
import zipfile

import numpy as np
from matio import load_from_mat

from inventory import checked_members

ROOT = Path(__file__).resolve().parent
XOR = "data/experiment_XOR3S2T_0920_ETA=64_VIT=40_[2S2T2G]_23-09-20-15-31-46.mat"
COUNTS = ("MES", "TRA", "TST", "SOR", "TAR", "DEL")
SCALES = ("NODEMULT", "GATEMULT")
ARRAYS = ("TRAIN", "TEST", "TLOC", "SLOC", "TestFreeState", "TestClampedState",
          "HorizontalCapacitors", "VerticalCapacitors", "LearnTimes")


def describe(properties):
    return {name: dict(type=type(value).__name__, shape=list(value.shape), dtype=str(value.dtype))
            if isinstance(value, np.ndarray) else dict(type=type(value).__name__)
            for name, value in properties.items()}


def inspect(member, body):
    record = dict(member=member, sha256=hashlib.sha256(body).hexdigest())
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "native.mat"
        path.write_bytes(body)
        with warnings.catch_warnings(record=True) as observed:
            warnings.simplefilter("always")
            try:
                obj = load_from_mat(path, variable_names=["experiment"], raw_data=True)["experiment"]
                record["class"] = obj.classname
                properties = obj.properties
                record["properties"] = describe(properties)
                missing = sorted(set(COUNTS + SCALES + ARRAYS) - properties.keys())
                record["missing"] = missing
                if not missing:
                    if not all(np.isfinite(properties[k].item()) and properties[k].item() >= 0
                               and properties[k].item() == np.floor(properties[k].item()) for k in COUNTS):
                        raise ValueError("Count metadata must be finite nonnegative integers")
                    counts = {k: int(properties[k].item()) for k in COUNTS}
                    scales = {k: float(properties[k].item()) for k in SCALES}
                    record["count_metadata"] = counts
                    record["scale_metadata_volts"] = scales
                    m, a, t, s, o = (counts[k] for k in ("MES", "TRA", "TST", "SOR", "TAR"))
                    expected = {"TRAIN": (s + o, a), "TEST": (s + o, t), "TLOC": (o, 2),
                                "SLOC": (s, 2), "TestFreeState": (4, 4, m, t),
                                "TestClampedState": (4, 4, m, t), "LearnTimes": (1, m),
                                "HorizontalCapacitors": (4, 4, m), "VerticalCapacitors": (4, 4, m)}
                    record["shape_checks"] = {k: properties[k].shape == v for k, v in expected.items()}
                    record["scale_checks"] = {k: bool(np.isfinite(v) and v > 0) for k, v in scales.items()}
                    record["location_checks"] = {k: bool(np.all(np.isfinite(properties[k]))
                        and np.all(properties[k] == np.floor(properties[k]))
                        and np.all((properties[k] >= 0) & (properties[k] < 4))) for k in ("TLOC", "SLOC")}
            except Exception as error:
                record["error"] = repr(error)
            record["warnings"] = [str(w.message) for w in observed]
    record["qualified_schema"] = (record.get("class") == "Experiment2"
        and not record.get("error") and not record["warnings"] and not record.get("missing", ["unknown"])
        and all(record.get("shape_checks", {"unknown": False}).values())
        and all(record.get("scale_checks", {"unknown": False}).values())
        and all(record.get("location_checks", {"unknown": False}).values()))
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    output = ROOT / "results" / ("property-schema-all.json" if args.all else "property-schema-xor.json")
    if output.exists():
        raise FileExistsError(output)
    if args.all:
        prior = json.loads((ROOT / "results/property-schema-xor.json").read_text())
        assert prior["records"][0]["qualified_schema"], "Named XOR schema must qualify first"
    runtime = json.loads((ROOT / "reader-runtime.json").read_text())
    assert importlib.metadata.version("mat-io") == "1.0.1"
    assert runtime["upstream_tests"]["passed"] == 12 and runtime["upstream_tests"]["failed"] == 0
    native = ROOT / "sources/browser-native/data.zip"
    assert hashlib.sha256(native.read_bytes()).hexdigest() == "f6a972d8ab2aaa6ae91529a38d5e0dff54d6c4888984834633161226c1a6a57c"
    with zipfile.ZipFile(native) as archive:
        members = checked_members(archive)
        names = [i.filename for i in members if i.filename.startswith("data/experiment") and i.filename.endswith(".mat")] if args.all else [XOR]
        records = [inspect(name, archive.read(name)) for name in names]
    result = dict(records=records, reader_version="1.0.1", numerical_response_replay=False,
                  response_points_selected_for_analysis=0, empirical_holdout_validation=False)
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(objects=len(records), qualified=sum(r["qualified_schema"] for r in records),
                          failures=[dict(member=r["member"], missing=r.get("missing"), error=r.get("error"),
                                         warnings=r["warnings"], shape_checks=r.get("shape_checks"))
                                    for r in records if not r["qualified_schema"]],
                          output=str(output)), indent=2))


if __name__ == "__main__":
    main()
