"""Audit declared input sets independently of the failed output-consistency test."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import warnings
import zipfile

import numpy as np
from matio import load_from_mat

from inventory import checked_members
from replay import ARCHIVE_SHA256, overlap

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = ROOT / "results/input-overlap.json"
    if output.exists():
        raise FileExistsError(output)
    native = ROOT / "sources/browser-native/data.zip"
    assert digest(native) == ARCHIVE_SHA256
    schema = json.loads((ROOT / "results/property-schema-all.json").read_text())["records"]
    rows = []
    with zipfile.ZipFile(native) as archive, tempfile.TemporaryDirectory() as directory:
        checked_members(archive)
        path = Path(directory) / "native.mat"
        for item in schema:
            row = dict(member=item["member"], native_sha256=item["sha256"])
            rows.append(row)
            if not item["qualified_schema"]:
                row.update(status="schema_excluded", missing=item.get("missing", []))
                continue
            body = archive.read(item["member"])
            assert hashlib.sha256(body).hexdigest() == item["sha256"]
            path.write_bytes(body)
            with warnings.catch_warnings(record=True) as observed:
                warnings.simplefilter("always")
                p = load_from_mat(path, variable_names=["experiment"], raw_data=True)["experiment"].properties
                assert not observed, "Reader warning; input audit stopped"
            s, o, a, t, d = (int(p[k].item()) for k in ("SOR", "TAR", "TRA", "TST", "DEL"))
            train, test = p["TRAIN"], p["TEST"]
            assert train.shape == (s + o, a) and test.shape == (s + o, t)
            assert np.all(np.isfinite(train)) and np.all(np.isfinite(test)) and d in (0, 1)
            assert d == 0 or o % 2 == 0
            row.update(status="input_audited", training_examples=a, test_examples=t,
                       unique_training_inputs=int(np.unique(train[:s].T, axis=0).shape[0]),
                       unique_test_inputs=int(np.unique(test[:s].T, axis=0).shape[0]),
                       source_boundaries_same_order=bool(np.array_equal(train[:s], test[:s])),
                       overlap=overlap(train[:s], test[:s], train[s:], test[s:], d))
    audited = [r for r in rows if r["status"] == "input_audited"]
    result = dict(observed_utc=datetime.now(timezone.utc).isoformat(), archive_sha256=ARCHIVE_SHA256,
                  provenance_sha256={name: digest(ROOT / name) for name in (
                      "INPUT_OVERLAP_PROTOCOL.md", "REPLAY_PROTOCOL.md", "input_overlap.py", "replay.py",
                      "results/property-schema-all.json", "results/replay-schedule.json")},
                  records=rows, audited_runs=len(audited),
                  total_test_columns=sum(r["test_examples"] for r in audited),
                  exact_untrained_test_columns=sum(r["overlap"]["exact"]["test_inputs_without_training_match"] for r in audited),
                  tolerance_untrained_test_columns=sum(r["overlap"]["max_coordinate_tolerance_1e_12"]["test_inputs_without_training_match"] for r in audited),
                  physical_response_replay_validated=False, independent_environment_generalization_verified=False,
                  empirical_performance_holdout_validation=False, integrated_goal_verified=False)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("records", "provenance_sha256")}, indent=2))


if __name__ == "__main__":
    main()
