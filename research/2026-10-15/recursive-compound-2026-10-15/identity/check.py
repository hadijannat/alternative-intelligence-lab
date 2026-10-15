import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np
from extract import BASE, OLD, extract

mapping = json.loads((BASE/'site_mapping.json').read_text())
evidence = json.loads((BASE/'.omo/evidence/extraction.json').read_text())
acquisition = next(r for r in json.loads((OLD/'acquisition.json').read_text()) if r.get('filename') == 'cod2107026.cif')
assert hashlib.sha256((OLD/'raw/cod2107026.cif').read_bytes()).hexdigest() == evidence['sha256'] == acquisition['sha256']
assert Counter(s['element'] for s in mapping) == {'Mo':36,'O':128}
assert all(s['occupancy']==1 for s in mapping)
assert len({(s['label'],s['symmetry_index'],tuple(s['cell_translation'])) for s in mapping})==164
assert Counter(s['label'] for s in mapping)=={**{f'Mo{i}':2 for i in range(1,19)},**{f'O{i}':2 for i in range(1,65)}}
xyz=(BASE/'parent_heavy.xyz').read_text().splitlines()
assert int(xyz[0])==164 and len(xyz)==166
for row,s in zip(xyz[2:],mapping):
    fields=row.split()
    assert fields[0]==s['element']
    assert np.max(np.abs(np.array(fields[1:],float)-s['cartesian_A']))<1e-8
positions=np.array([s['cartesian_A'] for s in mapping])
d=np.linalg.norm(positions[:,None]-positions[None,:],axis=2)
is_mo=np.array([s['element']=='Mo' for s in mapping])
adj=(d<=2.6)&(is_mo[:,None]!=is_mo[None,:])
visited={0}
while True:
    expanded=visited|set(np.flatnonzero(adj[list(visited)].any(axis=0)))
    if expanded==visited:break
    visited=expanded
assert len(visited)==164
assert Counter(adj[is_mo].sum(axis=1))=={6:32,7:4}
assert np.min(d+np.eye(164)*100)>1.5
for cutoff in (2.5,2.6,2.7):
    fresh,result=extract(cutoff)
    assert fresh==mapping
    assert result['counts']=={'Mo':36,'O':128}
small,rejected=extract(2.0)
assert rejected['counts']!={'Mo':36,'O':128}
water_candidates=[s for s in mapping if s['element']=='O' and int(s['label'][1:])>=57]
assert len(water_candidates)==16
out={'checks_pass':True,'checks':['source hash','164 counts','full occupancy','unique site map','two copies O1-O64/Mo1-Mo18','XYZ serialization','independent Cartesian connectivity','Mo coordination','no short pair','cutoff invariance'], 'negative_control':{'cutoff_A':2.0,'counts':rejected['counts'],'full_parent_rejected':True}, 'aqua_candidates_inferred_only':[s['label']+'@'+str(s['symmetry_index']) for s in water_candidates]}
(BASE/'.omo/evidence/checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
