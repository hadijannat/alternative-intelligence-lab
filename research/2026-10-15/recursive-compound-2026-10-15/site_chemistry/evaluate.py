"""Fixed-parent-geometry bond-valence mismatch; no energetics or target admission."""
import csv
import hashlib
import importlib.util
import json
import math
import re
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
IDENTITY = BASE.parent / 'identity'
EVIDENCE = BASE / '.omo/evidence'
CUTOFFS = (2.5, 2.6, 2.7)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name, rows):
    with (BASE / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    text = (BASE / 'sources/gagne2015.txt').read_text()
    table = text.split('Table 4 (continued)', 1)[1]
    params = {}
    for element, oxidation in [('Mo', 6), ('W', 6), ('V', 5)]:
        match = re.search(rf'\b{element}{oxidation}\+\s+(\d+)\s+(\d\.\d+)\s+(\d\.\d+)\s+(\d\.\d+)', table)
        assert match, f'Missing primary Table 4 row: {element}'
        n, r0, b, rmsd = match.groups()
        params[element] = dict(oxidation=oxidation, R0_A=float(r0), B_A=float(b), coordination_polyhedra=int(n), source_RMSD_vu=float(rmsd), table=4)
    assert params['Mo']['R0_A'] == 1.903 and params['W']['B_A'] == .339 and params['V']['coordination_polyhedra'] == 714
    (BASE / 'parameters.json').write_text(json.dumps(params, indent=2)+'\n')
    mapping = json.loads((IDENTITY / 'site_mapping.json').read_text())
    spec = importlib.util.spec_from_file_location('parent_extract', IDENTITY / 'extract.py')
    extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extractor)
    regenerated, _ = extractor.extract(2.6)
    assert regenerated == mapping, 'Original CIF extraction does not reproduce mapping'
    xyz = (IDENTITY / 'parent_heavy.xyz').read_text().splitlines()
    assert int(xyz[0]) == len(mapping) == 164
    for site, line in zip(mapping, xyz[2:], strict=True):
        fields = line.split()
        assert fields[0] == site['element']
        assert max(abs(a-float(b)) for a,b in zip(site['cartesian_A'], fields[1:])) < 5.1e-10
    metals = [s for s in mapping if s['element'] == 'Mo']
    oxygens = [s for s in mapping if s['element'] == 'O']
    assert len(metals) == 36 and len(oxygens) == 128
    rows, contacts, summary = [], [], []
    max_arithmetic_error = 0.
    for cutoff in CUTOFFS:
        reconstructed, extraction = extractor.extract(cutoff)
        assert [(s['label'], s['symmetry_index']) for s in reconstructed] == [(s['label'], s['symmetry_index']) for s in mapping]
        cutoff_rows = []
        for mo in metals:
            site_id = f"{mo['label']}@{mo['symmetry_index']}"
            lengths = [(o, math.dist(mo['cartesian_A'], o['cartesian_A'])) for o in oxygens]
            bonded = [(o,d) for o,d in lengths if d <= cutoff]
            # Independent extractor connectivity and vectorized arithmetic cross-check.
            assert len(bonded) == sum(site_id in o['Mo_neighbors'] for o in reconstructed)
            result = dict(cutoff_A=cutoff, site=site_id, xyz_index=mo['xyz_index'], crystallographic_label=mo['label'], coordination=len(bonded), shortest_A=min(d for _,d in bonded), longest_A=max(d for _,d in bonded), nearest_excluded_A=min(d for _,d in lengths if d>cutoff))
            for element, p in params.items():
                value = math.fsum(math.exp((p['R0_A']-d)/p['B_A']) for _,d in bonded)
                vec = np.linalg.norm(np.array([o['cartesian_A'] for o,_ in bonded])-np.array(mo['cartesian_A']), axis=1)
                independent = float(np.exp((p['R0_A']-vec)/p['B_A']).sum())
                max_arithmetic_error = max(max_arithmetic_error, abs(value-independent))
                assert abs(value-independent) < 1e-12
                result[f'{element}_BVS_vu'] = value
                result[f'{element}_signed_mismatch_vu'] = value-p['oxidation']
                result[f'{element}_absolute_mismatch_vu'] = abs(value-p['oxidation'])
            cutoff_rows.append(result)
            if cutoff == 2.7:
                for ox,d in sorted(lengths, key=lambda x:x[1]):
                    if d <= 3.5:
                        contacts.append(dict(metal=site_id, oxygen=f"{ox['label']}@{ox['symmetry_index']}", distance_A=d, included_2_5=d<=2.5, included_2_6=d<=2.6, included_2_7=d<=2.7))
        # 1e-8 grouping avoids ranking symmetry-equivalent sites by roundoff.
        for element in params:
            scores = sorted(set(round(r[f'{element}_absolute_mismatch_vu'],8) for r in cutoff_rows))
            for row in cutoff_rows:
                row[f'{element}_dense_rank'] = scores.index(round(row[f'{element}_absolute_mismatch_vu'],8))+1
        parent = [r['Mo_signed_mismatch_vu'] for r in cutoff_rows]
        summary.append(dict(cutoff_A=cutoff, parent_BVS_min=min(r['Mo_BVS_vu'] for r in cutoff_rows), parent_BVS_max=max(r['Mo_BVS_vu'] for r in cutoff_rows), parent_RMSD_vu=math.sqrt(math.fsum(v*v for v in parent)/36), coordination_numbers=sorted(set(r['coordination'] for r in cutoff_rows)), W_best=[r['site'] for r in cutoff_rows if r['W_dense_rank']==1], V_best=[r['site'] for r in cutoff_rows if r['V_dense_rank']==1]))
        rows.extend(cutoff_rows)
    write_csv('site_scores.csv', rows)
    write_csv('contacts_through_3_5A.csv', contacts)
    write_csv('cutoff_summary.csv', summary)
    for label in set(r['crystallographic_label'] for r in rows):
        for cutoff in CUTOFFS:
            symmetry = [r for r in rows if r['crystallographic_label']==label and r['cutoff_A']==cutoff]
            for element in params:
                assert max(r[f'{element}_BVS_vu'] for r in symmetry)-min(r[f'{element}_BVS_vu'] for r in symmetry) < 1e-10
    inputs = [IDENTITY/'site_mapping.json', IDENTITY/'parent_heavy.xyz', IDENTITY/'extract.py', ROOT/'noncarbon-discovery-2026-10-15/research/structure/raw/cod2107026.cif', ROOT/'noncarbon-discovery-2026-10-15/research/structure/check.py', BASE/'sources/gagne2015.pdf', BASE/'sources/gagne2015.txt', Path(__file__)]
    evidence = dict(status='PASS_BOUNDED_FIXED_GEOMETRY_ARITHMETIC', target_admitted=False, source_publications=1, source_parameter_rows=3, expanded_metal_sites=36, crystallographic_metal_sites=18, score_rows=len(rows), cutoffs_A=CUTOFFS, independent_arithmetic_max_error=max_arithmetic_error, checks=['CIF-to-mapping exact equality', 'XYZ-to-mapping within rounding', 'all cutoff extractions preserve 164-site component', 'connectivity counts match independent Cartesian distances', 'scalar math.fsum vs NumPy vectorized BVS within 1e-12', 'symmetry equivalent sums within 1e-10'], input_sha256={str(p.relative_to(ROOT)):sha(p) for p in inputs}, results=summary)
    (EVIDENCE/'validation.json').write_text(json.dumps(evidence, indent=2)+'\n')
    print(json.dumps(evidence, indent=2))

if __name__ == '__main__':
    main()
