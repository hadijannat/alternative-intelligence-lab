import hashlib
import json
from pathlib import Path

B=Path(__file__).resolve().parent
r=json.loads((B/'feasibility.json').read_text())
h=json.loads((B/'hypotheses.json').read_text())
assert r['geometry_sha256']==hashlib.sha256((B.parent/'site_mapping.json').read_bytes()).hexdigest()
for row in r['models']:
    n=row['composition']
    assert sum(n.values())==196
    z={'Mo':42,'W':74,'V':23,'O':8,'H':1}
    core={'Mo':28,'W':60,'V':0,'O':0,'H':0}
    assert row['all_electron_count']==sum(z[e]*v for e,v in n.items())-row['charge']
    assert row['explicit_electrons']==row['all_electron_count']-sum(core[e]*v for e,v in n.items())
    a=row['spherical_AOs'];p=a*(a+1)//2
    assert row['storage_GiB']['eightfold_packed_four_center_ERI']==8*(p*(p+1)//2)/2**30
    assert not row['geometry_generated'] and not row['scf_run']
assert not h['coordinates_admitted'] and not h['hydrogens_generated']
for p in h['parent_alternatives']:
    assert 36*6-128*2+p['H']==p['charge']
    assert 36*42+128*8+p['H']-p['charge']-36*28==1568
for rec in json.loads((B/'acquisition.json').read_text()):
    if 'path' in rec:
        data=Path(rec['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==rec['sha256']
        assert not data.startswith(b'%PDF')
assert len(r['nearest_framework_O_candidates'])==16
assert abs(r['nearest_framework_O_candidates'][0]['distance_A']-2.575820285876855)<1e-12
old=json.loads((B.parent/'identity_admission.json').read_text())
assert old['parent_heavy_atom_admitted'] and not old['target_admitted']
assert not old['complete_hydrated_molecule_admitted']
print('PASS: count/storage arithmetic, four hypothesis charge/electron balances, source-response hashes, no PDF falsely admitted, 16 geometry-derived nearest pairs, parent-only admission preserved. Primary assignment remains unavailable; no full-cluster energy or geometry generated.')
