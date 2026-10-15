"""Check source accounting and condition-table boundaries, not chemical validity."""
import csv
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree

root = Path(__file__).resolve().parent
sources = json.loads((root / 'sources.json').read_text())
rows = list(csv.DictReader((root / 'conditions.csv').open()))
assert len(sources) == 6 and len(rows) == 10
assert len({r['id'] for r in rows}) == len(rows)
source_ids = {s['id'] for s in sources} | {'HYPOTHESIS'}
assert all(r['source_id'] in source_ids for r in rows)
verified_files = 0
for source in sources:
    for name, expected in source['file_hashes'].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
        verified_files += 1
for record in json.loads((root / 'raw/acquisition.json').read_text()):
    if 'file' in record:
        assert hashlib.sha256((root / 'raw' / record['file']).read_bytes()).hexdigest() == record['sha256']
    if record['status'] != 200:
        assert record['acquired_article'] is False
text = ''.join(ElementTree.parse(root / 'raw/spencer2024.xml').getroot().itertext())
assert 'D4SC00102H' in text
for value in ('0.5 M H2SO4', '501.0 mV', '531.7 mV', '621.5 mV', '−0.493', '0.644'):
    assert value in text, value
assert 34 * 6 + 6 + 5 - 112 * 2 == -9
assert 34 * 6 + 6 + 4 - 112 * 2 == -10
hypothesis = next(r for r in rows if r['id'] == 'mo34wv_target')
assert hypothesis['evidence_class'] == 'UNMEASURED'
assert all(hypothesis[key] == 'UNMEASURED' for key in ('medium', 'temperature', 'concentration_or_geometry', 'potential_reference', 'atmosphere'))
receipt = {'status': 'PASS_ACCOUNTING_ONLY', 'conditions': len(rows), 'primary_sources': len(sources), 'hashed_source_files_checked': verified_files, 'formal_charges': [-9, -10], 'potential_conversions_performed': 0, 'chemical_simulations_or_experiments_performed': 0, 'joint_compatibility': 'UNMEASURED', 'new_compound_existence': 'UNMEASURED'}
(root / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
