import ast
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
OLD = ROOT / 'noncarbon-discovery-2026-10-15/research/structure'
# Reuse pure parser functions without executing the prior audit's output writes.
tree = ast.parse((OLD / 'check.py').read_text())
helpers = ast.Module(body=[n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)) or isinstance(n, ast.FunctionDef) and n.name in {'number', 'loop', 'scalar', 'transformed'}], type_ignores=[])
namespace = {}
exec(compile(helpers, str(OLD / 'check.py'), 'exec'), namespace)
number, loop, scalar, transformed = [namespace[name] for name in ('number', 'loop', 'scalar', 'transformed')]


def extract(cutoff):
    cif = (OLD / 'raw/cod2107026.cif').read_text()
    rows = loop(cif, '_atom_site_label')
    ops = [r['_symmetry_equiv_pos_as_xyz'] for r in loop(cif, '_symmetry_equiv_pos_as_xyz')]
    a, b, c = [number(scalar(cif, f'_cell_length_{v}')) for v in 'abc']
    beta = np.deg2rad(number(scalar(cif, '_cell_angle_beta')))
    assert number(scalar(cif, '_cell_angle_alpha')) == number(scalar(cif, '_cell_angle_gamma')) == 90
    cell = np.array([[a, 0, 0], [0, b, 0], [c*np.cos(beta), 0, c*np.sin(beta)]])
    sites = []
    for row in rows:
        element = row['_atom_site_type_symbol'].split('-')[0].split('+')[0]
        if element not in ('Mo', 'O'):
            continue
        point = tuple(number(row[f'_atom_site_fract_{axis}']) for axis in 'xyz')
        seen = set()
        for op_index, op in enumerate(ops):
            pos = transformed(point, op)
            if pos in seen:
                continue
            seen.add(pos)
            sites.append(dict(label=row['_atom_site_label'], element=element, symmetry_index=op_index,
                              symmetry_expression=op, fractional_wrapped=list(pos), occupancy=number(row['_atom_site_occupancy'])))
    graph = [[] for _ in sites]
    images = np.array(list(itertools.product((-1, 0, 1), repeat=3)))
    for i, mo in enumerate(sites):
        if mo['element'] != 'Mo':
            continue
        for j, ox in enumerate(sites):
            if ox['element'] != 'O':
                continue
            distances = np.linalg.norm((np.array(ox['fractional_wrapped']) + images - mo['fractional_wrapped']) @ cell, axis=1)
            matches = np.flatnonzero(distances <= cutoff)
            assert len(matches) <= 1, 'ambiguous periodic bond image'
            if len(matches):
                shift = images[matches[0]]
                graph[i].append((j, shift))
                graph[j].append((i, -shift))
    seed = next(i for i, s in enumerate(sites) if s['label'] == 'Mo1' and s['symmetry_index'] == 0)
    offsets = {seed: np.zeros(3, dtype=int)}
    queue = deque([seed])
    while queue:
        i = queue.popleft()
        for j, shift in graph[i]:
            expected = offsets[i] + shift
            if j in offsets:
                assert np.array_equal(offsets[j], expected), 'component spans a periodic network'
            else:
                offsets[j] = expected
                queue.append(j)
    selected = sorted(offsets, key=lambda i: (sites[i]['element'] != 'Mo', int(sites[i]['label'].lstrip('MoO')), sites[i]['symmetry_index']))
    mapping = []
    for n, i in enumerate(selected, 1):
        s = dict(sites[i], xyz_index=n, cell_translation=offsets[i].tolist())
        s['cartesian_A'] = ((np.array(s['fractional_wrapped']) + offsets[i]) @ cell).tolist()
        s['Mo_neighbors'] = [sites[j]['label'] + '@' + str(sites[j]['symmetry_index']) for j, _ in graph[i] if sites[j]['element'] == 'Mo']
        mapping.append(s)
    positions = np.array([s['cartesian_A'] for s in mapping])
    distances = np.linalg.norm(positions[:, None] - positions[None, :], axis=2)
    np.fill_diagonal(distances, np.inf)
    return mapping, dict(cutoff_A=cutoff, counts=dict(Counter(s['element'] for s in mapping)),
                        connected=True, periodic_cycle_consistent=True,
                        partial_occupancy_selected=[s['label'] for s in mapping if s['occupancy'] != 1],
                        minimum_pair_distance_A=float(distances.min()),
                        Mo_coordination_histogram=dict(Counter(len(graph[i]) for i in selected if sites[i]['element'] == 'Mo')),
                        source_partial_occupancy_rows=[r['_atom_site_label'] for r in rows if number(r['_atom_site_occupancy']) != 1])


if __name__ == '__main__':
    mapping, result = extract(2.6)
    sensitivity = [extract(c)[1] for c in (2.5, 2.7)]
    evidence = dict(source=str((OLD/'raw/cod2107026.cif').relative_to(ROOT)),
                    sha256=hashlib.sha256((OLD/'raw/cod2107026.cif').read_bytes()).hexdigest(),
                    parser_sha256=hashlib.sha256((OLD/'check.py').read_bytes()).hexdigest(),
                    result=result, cutoff_sensitivity=sensitivity)
    (BASE/'.omo/evidence/extraction.json').write_text(json.dumps(evidence, indent=2)+'\n')
    (BASE/'site_mapping.json').write_text(json.dumps(mapping, indent=2)+'\n')
    admitted = (result['counts'] == {'Mo': 36, 'O': 128} and not result['partial_occupancy_selected'] and result['minimum_pair_distance_A'] > 1.5)
    admission = dict(parent_heavy_atom_admitted=admitted, complete_hydrated_molecule_admitted=False,
                     target_admitted=False, life_intelligence_verified=False,
                     status='PARENT_HEAVY_ATOM_ONLY' if admitted else 'EXTRACTION_REJECTED',
                     H_coordinates='ABSENT', oxide_aqua_site_assignment='UNRESOLVED',
                     solution_protonation='UNRESOLVED', target_substitution_sites=None)
    (BASE/'identity_admission.json').write_text(json.dumps(admission, indent=2)+'\n')
    if admitted:
        lines = ['164', 'COD2107026 parent heavy atoms only; H absent; no charge/bond-order inference']
        lines.extend(s['element']+' '+ ' '.join(f'{v:.9f}' for v in s['cartesian_A']) for s in mapping)
        (BASE/'parent_heavy.xyz').write_text('\n'.join(lines)+'\n')
    print(json.dumps(evidence, indent=2))
    assert admitted, 'Parent heavy-atom admission failed; inspect preserved evidence'
