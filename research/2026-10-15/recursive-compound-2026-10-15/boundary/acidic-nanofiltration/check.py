import hashlib
import json
from decimal import Decimal
from pathlib import Path

base = Path(__file__).resolve().parent
data = json.loads((base / 'evidence.json').read_text())
for source in data['sources']:
    raw = (base / source['path']).read_bytes()
    assert len(raw) == source['bytes'] and raw.startswith(b'%PDF-')
    assert hashlib.sha256(raw).hexdigest() == source['sha256']
conditions = data['corrosion_protocol']['ordered_conditions']
assert [row['pH'] for row in conditions] == [2, 13, 1]
assert sum(row['weeks'] for row in conditions) == 12
rows = data['printed_cutoff_annotations']
assert [r['elapsed_weeks'] for r in rows] == list(range(0, 13, 2))
assert [r['MWCO_as_printed'] for r in rows] == [200, 220, 290, 220, 230, 290, 260]
assert all(r['uncertainty'] is None for r in rows)
assert data['PEG_assay']['pressure_bar'] == 10
assert data['corrosion_protocol']['pressure_bar'] == [5, 7]
assert data['decision']['admission'] is False
assert data['decision']['cross_paper_integration_claim'] is False
assert data['decision']['heldout_validation'] is False
initial = Decimal(data['permeability']['initial'])
final = Decimal(data['permeability']['final_after_sequence'])
assert initial > 0 and final > 0
result = {
    'status': 'PASS_SOURCE_RECORD_AND_ARITHMETIC_ONLY',
    'source_hashes_checked': 2,
    'cutoff_annotations_checked': len(rows),
    'permeability_change_L_h_m2_bar': str(final - initial),
    'relative_change_percent': str((final - initial) / initial * 100),
    'statistical_improvement_demonstrated': False,
    'target_transport_inferred': False,
    'verified_integrated_complements_added': 0,
    'evidence_sha256': hashlib.sha256((base / 'evidence.json').read_bytes()).hexdigest(),
}
with (base / 'validation.json').open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps(result))
