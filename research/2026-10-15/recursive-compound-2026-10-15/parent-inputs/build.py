"""Frozen hypothetical H construction; no energy evaluation or relaxation."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / 'identity'
SITES = json.loads((SOURCE / 'site_mapping.json').read_text())
HEAVY = np.array([s['cartesian_A'] for s in SITES])
KEYS = [s['label'] + '@' + str(s['symmetry_index']) for s in SITES]
WATER = [i for i, s in enumerate(SITES) if s['element'] == 'O' and int(s['label'][1:]) >= 57]
MOS = [i for i, s in enumerate(SITES) if s['element'] == 'Mo']
FORMULA = {'P0': 'Mo36O112(H2O)16', 'PT57': 'Mo36O111(OH)2(H2O)15'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def expected(arm):
    counts = {KEYS[i]: 2 for i in WATER}
    if arm == 'PT57':
        counts['O57@0'] = 1
        counts['O4@0'] = 1
    return counts

def construct(arm, start):
    hs, frames = [], []
    for i in WATER:
        vectors = HEAVY[MOS] - HEAVY[i]
        distances = np.linalg.norm(vectors, axis=1)
        neighbors = distances <= 2.6
        axis = -(vectors[neighbors] / distances[neighbors, None]).sum(axis=0)
        norm = np.linalg.norm(axis)
        if norm < 1e-8:
            raise ValueError(f'degenerate bisector at {KEYS[i]}')
        axis /= norm
        basis = np.eye(3)[np.argmin(np.abs(axis))]
        tangent = basis - np.dot(basis, axis) * axis
        tangent /= np.linalg.norm(tangent)
        if start == 'B':
            tangent = np.cross(axis, tangent)
        frames.append({'owner': KEYS[i], 'Mo_neighbors': [KEYS[MOS[j]] for j in np.flatnonzero(neighbors)], 'bisector': axis.tolist(), 'tangent': tangent.tolist(), 'azimuth_degrees': 0 if start == 'A' else 90})
        for number, sign in ((1, 1), (2, -1)):
            theta = np.deg2rad(104.5 / 2)
            position = HEAVY[i] + 0.98 * (np.cos(theta) * axis + sign * np.sin(theta) * tangent)
            owner = KEYS[i]
            if arm == 'PT57' and owner == 'O57@0' and number == 2:
                owner = 'O4@0'
                acceptor = HEAVY[KEYS.index(owner)]
                direction = HEAVY[i] - acceptor
                position = acceptor + 0.98 * direction / np.linalg.norm(direction)
            hs.append({'id': f'{KEYS[i]}:H{number}', 'element': 'H', 'xyz_index': 165 + len(hs), 'original_owner': KEYS[i], 'owner': owner, 'source': 'MODEL_BUILT_PROVISIONAL_AQUA_ASSIGNMENT', 'cartesian_A': position.tolist()})
    return {'id': f'{arm}_{start}', 'arm': arm, 'start': start, 'status': 'HYPOTHETICAL', 'water_assignment': 'PROVISIONAL O57-O64 both symmetry copies; not measured H', 'formula': FORMULA[arm], 'composition': {'Mo': 36, 'O': 128, 'H': 32}, 'charge': -8, 'charge_basis': 'nominal Mo(VI)/oxide(-2)/hydroxide(-1)/water(0)', 'physical_admission': False, 'heavy_atoms': copy.deepcopy(SITES), 'hydrogens': hs, 'frames': frames}

def check(candidate):
    failures, clashes = [], []
    arm, hs = candidate['arm'], candidate['hydrogens']
    if any(h.get('owner') not in KEYS or h.get('original_owner') not in KEYS for h in hs):
        return {'computational_input_admitted': False, 'physical_admission': False, 'verdict': 'REJECT_COMPUTATIONAL_INPUT', 'failures': ['missing_or_invalid_ownership'], 'clashes': []}
    heavy = candidate['heavy_atoms']
    if Counter(a.get('element') for a in heavy + hs) != {'Mo': 36, 'O': 128, 'H': 32}:
        failures.append('actual_element_counts')
    if [a.get('xyz_index') for a in heavy + hs] != list(range(1,197)):
        failures.append('atom_index_sequence')
    if heavy != SITES:
        failures.append('heavy_mapping_or_coordinates')
    if len(hs) != 32 or len({h['id'] for h in hs}) != 32:
        failures.append('H_count_or_identity')
    if Counter(h['owner'] for h in hs) != expected(arm):
        failures.append('proton_ownership')
    for h in hs:
        origin = h['id'].split(':')[0]
        owner = 'O4@0' if arm == 'PT57' and h['id'] == 'O57@0:H2' else origin
        if h['original_owner'] != origin or h['owner'] != owner:
            failures.append('proton_identity_origin_or_ownership')
    if candidate['composition'] != {'Mo': 36, 'O': 128, 'H': 32} or candidate['charge'] != -8 or candidate['formula'] != FORMULA[arm]:
        failures.append('composition_charge_formula')
    positions = np.array([h['cartesian_A'] for h in hs])
    if not np.isfinite(positions).all():
        return {'computational_input_admitted': False, 'physical_admission': False, 'verdict': 'REJECT_COMPUTATIONAL_INPUT', 'failures': sorted(set(failures + ['finite_coordinates'])), 'clashes': []}
    own_lengths, angles = [], []
    minima = {'H-H': float('inf'), 'H-otherO': float('inf'), 'H-Mo': float('inf')}
    for j, h in enumerate(hs):
        owner_index = KEYS.index(h['owner'])
        length = float(np.linalg.norm(positions[j] - HEAVY[owner_index]))
        own_lengths.append({'id': h['id'], 'length_A': length})
        if abs(length - 0.98) > 1e-8:
            failures.append('own_OH_length')
        for k in range(j):
            d = float(np.linalg.norm(positions[j] - positions[k]))
            minima['H-H'] = min(minima['H-H'], d)
            if d < 0.70:
                clashes.append({'kind': 'H-H', 'a': h['id'], 'b': hs[k]['id'], 'distance_A': d, 'threshold_A': 0.70})
        for k, site in enumerate(SITES):
            if k == owner_index:
                continue
            d = float(np.linalg.norm(positions[j] - HEAVY[k]))
            cutoff = 1.50 if site['element'] == 'Mo' else 1.20
            kind = 'H-Mo' if site['element'] == 'Mo' else 'H-otherO'
            minima[kind] = min(minima[kind], d)
            if d < cutoff:
                clashes.append({'kind': 'H-Mo' if site['element'] == 'Mo' else 'H-otherO', 'a': h['id'], 'b': KEYS[k], 'distance_A': d, 'threshold_A': cutoff})
    for owner, count in expected(arm).items():
        owned = [np.array(h['cartesian_A']) - HEAVY[KEYS.index(owner)] for h in hs if h['owner'] == owner]
        if count == 2 and len(owned) == 2:
            cosine = np.dot(*owned) / (np.linalg.norm(owned[0]) * np.linalg.norm(owned[1]))
            angle = float(np.rad2deg(np.arccos(np.clip(cosine, -1, 1))))
            angles.append({'owner': owner, 'angle_degrees': angle})
            if abs(angle - 104.5) > 1e-6:
                failures.append('HOH_angle')
    if clashes:
        failures.append('gross_clash')
    return {'computational_input_admitted': not failures, 'physical_admission': False, 'verdict': 'PASS_COMPUTATIONAL_INPUT_ONLY' if not failures else 'REJECT_COMPUTATIONAL_INPUT', 'failures': sorted(set(failures)), 'clashes': clashes, 'OH_lengths': own_lengths, 'HOH_angles': angles, 'minimum_distances_A': minima}

def xyz(candidate):
    rows = ['196', f"HYPOTHETICAL {candidate['id']} charge=-8; MODEL-BUILT H; PROVISIONAL aqua; not physical admission"]
    for atom in candidate['heavy_atoms'] + candidate['hydrogens']:
        rows.append(atom['element'] + ' ' + ' '.join(repr(float(x)) for x in atom['cartesian_A']))
    return '\n'.join(rows) + '\n'

def main():
    sources = {str(p.relative_to(BASE.parent)): digest(p) for p in (SOURCE/'site_mapping.json', SOURCE/'next-step/hypotheses.json', SOURCE/'parent_heavy.xyz', SOURCE/'identity_admission.json')}
    protocol_hash = digest(BASE/'PROTOCOL.md')
    candidates = [construct(a, s) for a in FORMULA for s in ('A', 'B')]
    checks = {c['id']: check(c) for c in candidates}
    for c in candidates:
        text = xyz(c)
        parsed = text.splitlines()[2:166]
        assert np.array_equal(np.array([r.split()[1:] for r in parsed], float), HEAVY)
        (BASE/f"{c['id']}.xyz").write_text(text)
        c['checks'] = checks[c['id']]
        c['xyz_sha256'] = digest(BASE/f"{c['id']}.xyz")
    distinct = {}
    for arm in FORMULA:
        a, b = [c for c in candidates if c['arm'] == arm]
        distances = {}
        for owner, count in expected(arm).items():
            pa, pb = [np.array([h['cartesian_A'] for h in c['hydrogens'] if h['owner'] == owner]) for c in (a,b)]
            d = np.linalg.norm(pa[:,None] - pb[None,:], axis=2)
            distances[owner] = float(max(d.min(axis=0).max(), d.min(axis=1).max()))
        assert max(distances.values()) > .1
        assert all(d > .1 for owner,d in distances.items() if expected(arm)[owner] == 2)
        distinct[arm] = distances
    controls = {}
    def control(name, mutation, required_failure=None, clash_kind=None):
        c = copy.deepcopy(candidates[0]); mutation(c); result = check(c)
        assert not result['computational_input_admitted']
        if required_failure: assert required_failure in result['failures']
        if clash_kind: assert any(x['kind'] == clash_kind for x in result['clashes'])
        controls[name] = result
    control('wrong_element', lambda c:c['hydrogens'][0].__setitem__('element','O'), 'actual_element_counts')
    control('wrong_index', lambda c:c['hydrogens'][0].__setitem__('xyz_index',1), 'atom_index_sequence')
    control('missing_ownership', lambda c:c['hydrogens'][0].pop('owner'), 'missing_or_invalid_ownership')
    control('nonfinite_H', lambda c:c['hydrogens'][0]['cartesian_A'].__setitem__(0,float('nan')), 'finite_coordinates')
    control('missing_H', lambda c:c['hydrogens'].pop(), 'H_count_or_identity')
    control('heavy_coordinate', lambda c:c['heavy_atoms'][0]['cartesian_A'].__setitem__(0,0), 'heavy_mapping_or_coordinates')
    control('wrong_ownership', lambda c:c['hydrogens'][0].__setitem__('owner','O4@0'), 'proton_ownership')
    control('H_overlap', lambda c:c['hydrogens'][0].__setitem__('cartesian_A', c['hydrogens'][1]['cartesian_A']), clash_kind='H-H')
    control('other_O_overlap', lambda c:c['hydrogens'][0].__setitem__('cartesian_A',HEAVY[KEYS.index('O4@0')].tolist()), clash_kind='H-otherO')
    control('Mo_overlap', lambda c:c['hydrogens'][0].__setitem__('cartesian_A',HEAVY[0].tolist()), clash_kind='H-Mo')
    assert sources == {p: digest(BASE.parent/p) for p in sources}
    metadata = {'schema_version': 1, 'status':'HYPOTHETICAL_MODEL_BUILT_H_ONLY', 'protocol_sha256':protocol_hash, 'build_sha256':digest(Path(__file__)), 'source_sha256':sources, 'candidates':candidates}
    (BASE/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (BASE/'checks.json').write_text(json.dumps({'candidates':checks,'unordered_H_Hausdorff_by_owner_A':distinct,'negative_controls':controls,'source_hashes_unchanged':True,'xyz_heavy_roundtrip_exact':True},indent=2)+'\n')
    print(json.dumps({k:{'verdict':v['verdict'],'clash_count':len(v['clashes'])} for k,v in checks.items()},indent=2))

if __name__ == '__main__':
    main()
