import hashlib
import json
from pathlib import Path

import fitz

root = Path(__file__).parent
records = json.loads((root / "receipt.json").read_text())
successes = []
failures = []
for record in records:
    if "error" in record:
        failures.append(record["name"])
        continue
    file = root / record["name"]
    data = file.read_bytes()
    assert len(data) == record["bytes"]
    assert hashlib.sha256(data).hexdigest() == record["sha256"]
    assert (root / file.with_suffix(".txt").name).stat().st_size > 100
    if file.suffix == ".pdf":
        assert data.startswith(b"%PDF")
        assert len(fitz.open(file)) == record["pages"]
    successes.append(file.name)
assert len(successes) == 5
assert failures == ["kang2021.pdf"]
assert (root / "sugar2024-si-page24.png").stat().st_size > 1000
assert (root / "brand2017-page5.png").stat().st_size > 1000
output = root / ".omo/evidence/verification.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({"verified_saved_sources": successes, "retained_access_failures": failures, "source_integrity": "PASS", "functional_inheritance": "UNRESOLVED", "validation_scope": "Source byte integrity and parseability; scientific claims manually checked against named pages"}, indent=2) + "\n")
print(output)
