#!/usr/bin/env python3
"""Frozen descriptive screening of existing JARVIS structures; no life score."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import zipfile

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / 'raw/jdft_3d-12-12-2022.json.zip'
EXPECTED_MD5 = 'fb3e1eb80339a70ff313af1c644c1777'
SALT = 'noncarbon-screen-2026-10-15-v1|'
QUOTAS = {'phosphorus_oxygen': 150, 'silicon_oxygen': 150, 'sulfur_no_oxygen': 200,
          'nitrogen_no_oxygen_sulfur': 100, 'other_oxygen': 300, 'other': 100}
REDOX = set('V Cr Mn Fe Co Ni Cu Mo W'.split())
ION = set('H Li Na K Rb Cs Ag Cu Mg Ca Zn'.split())
SCALARS = ['formation_energy_peratom', 'ehull', 'optb88vdw_bandgap', 'mbj_bandgap']


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + '\n')


def write_csv(path, rows):
    with Path(path).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_rows():
    if digest(ARCHIVE, 'md5') != EXPECTED_MD5:
        raise ValueError('Archive MD5 differs from official frozen snapshot')
    with zipfile.ZipFile(ARCHIVE) as archive:
        members = [n for n in archive.namelist() if n.endswith('.json') and not n.startswith('__MACOSX/')]
        if len(members) != 1:
            raise ValueError('Expected exactly one JSON dataset')
        with archive.open(members[0]) as stream:
            rows = json.load(stream)
    if not isinstance(rows, list):
        raise ValueError('Dataset must contain a list of material records')
    return rows


def stratum(elements):
    e = set(elements)
    if {'P', 'O'} <= e:
        return 'phosphorus_oxygen'
    if {'Si', 'O'} <= e:
        return 'silicon_oxygen'
    if 'S' in e and 'O' not in e:
        return 'sulfur_no_oxygen'
    if 'N' in e and not e.intersection({'O', 'S'}):
        return 'nitrogen_no_oxygen_sulfur'
    if 'O' in e:
        return 'other_oxygen'
    return 'other'


def identity(row):
    jid = row.get('jid')
    if not isinstance(jid, str) or not re.fullmatch(r'JVASP-\d+', jid):
        return None, 'invalid_jid'
    atoms = row.get('atoms')
    elements = atoms.get('elements') if isinstance(atoms, dict) else None
    if not isinstance(elements, list) or not elements or any(
        not isinstance(e, str) or not re.fullmatch(r'[A-Z][a-z]?', e) for e in elements
    ):
        return None, 'invalid_elements'
    e = set(elements)
    if 'C' in e:
        return None, 'contains_carbon'
    if len(e) < 2:
        return None, 'elemental_not_compound'
    formula = row.get('formula')
    if not isinstance(formula, str) or not formula.strip():
        return None, 'missing_formula'
    counts = Counter(elements)
    gcd = math.gcd(*counts.values())
    composition = '|'.join(f'{el}:{counts[el] // gcd}' for el in sorted(counts))
    return {'jid': jid, 'formula': formula, 'elements': '|'.join(sorted(e)),
            'composition_key': composition, 'stratum': stratum(e),
            'selection_hash': hashlib.sha256((SALT + jid).encode()).hexdigest()}, None


def select_records(rows, quotas=QUOTAS):
    ids = [r.get('jid') for r in rows if isinstance(r.get('jid'), str)]
    duplicates = {jid for jid, n in Counter(ids).items() if n > 1}
    eligible, excluded = [], Counter()
    for row in rows:
        item, reason = identity(row)
        if reason:
            excluded[reason] += 1
        elif item['jid'] in duplicates:
            excluded['duplicate_jid'] += 1
        else:
            eligible.append(item)
    key = lambda r: (r['selection_hash'], r['jid'])
    eligible.sort(key=key)
    target = sum(quotas.values())
    if len(eligible) < target:
        raise ValueError(f'Only {len(eligible)} eligible records for {target} required')
    chosen = []
    for group, quota in quotas.items():
        chosen.extend([r for r in eligible if r['stratum'] == group][:quota])
    chosen_ids = {r['jid'] for r in chosen}
    chosen.extend([r for r in eligible if r['jid'] not in chosen_ids][:target - len(chosen)])
    chosen.sort(key=key)
    return eligible, chosen, dict(sorted(excluded.items()))


def finite(value):
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (ValueError, TypeError):
        return None


def formation_class(value):
    return 'unknown' if value is None else ('nonpositive_formation' if value <= 0 else 'positive_formation')


def hull_class(value):
    if value is None:
        return 'unknown'
    if value < 0:
        return 'negative_invalid'
    return 'within_screen_threshold' if value <= 0.1 else 'above_screen_threshold'


def select(out):
    rows = load_rows()
    eligible, chosen, excluded = select_records(rows)
    out.mkdir(parents=True, exist_ok=False)
    write_csv(out / 'eligible_inventory.csv', eligible)
    write_csv(out / 'selected_1000.csv', chosen)
    manifest = {'archive_sha256': digest(ARCHIVE), 'archive_md5': digest(ARCHIVE, 'md5'),
                'protocol_sha256': digest(HERE / 'PROTOCOL.md'),
                'selection_sha256': digest(out / 'selected_1000.csv'),
                'eligible_sha256': digest(out / 'eligible_inventory.csv'),
                'total_source_rows': len(rows), 'eligible_count': len(eligible), 'excluded': excluded,
                'eligible_by_stratum': dict(Counter(r['stratum'] for r in eligible)),
                'selected_by_stratum': dict(Counter(r['stratum'] for r in chosen)),
                'selected_count': len(chosen),
                'distinct_selected_compositions': len({r['composition_key'] for r in chosen}),
                'selection_uses_numeric_properties': False}
    write_json(out / 'selection_manifest.json', manifest)
    print(json.dumps(manifest, indent=2))


def screen(out):
    manifest = json.loads((out / 'selection_manifest.json').read_text())
    if digest(out / 'selected_1000.csv') != manifest['selection_sha256']:
        raise ValueError('Selected IDs changed after freeze')
    if digest(HERE / 'PROTOCOL.md') != manifest['protocol_sha256']:
        raise ValueError('Protocol changed after selection freeze')
    if (out / 'screened_1000.csv').exists():
        raise ValueError('Refusing to overwrite existing screen; replay into a new directory')
    with (out / 'selected_1000.csv').open() as stream:
        chosen = list(csv.DictReader(stream))
    source = {r['jid']: r for r in load_rows() if r.get('jid') in {x['jid'] for x in chosen}}
    screened, raw = [], []
    for item in chosen:
        row = source[item['jid']]
        raw.append(row)
        e = set(item['elements'].split('|'))
        values = {field: finite(row.get(field)) for field in SCALARS}
        screened.append({**item, **{field: '' if value is None else value for field, value in values.items()},
                         'formation_class': formation_class(values['formation_energy_peratom']),
                         'hull_class': hull_class(values['ehull']),
                         'redox_elements': '|'.join(sorted(e & REDOX)),
                         'candidate_ion_elements': '|'.join(sorted(e & ION)),
                         'icsd_source_field': str(row.get('icsd', '')),
                         'novelty_status': 'existing_database_structure',
                         'autonomous_maintenance': 'UNMEASURED', 'replication': 'UNMEASURED',
                         'functional_inheritance': 'UNMEASURED', 'learning': 'UNMEASURED',
                         'intelligence': 'UNMEASURED'})
    write_csv(out / 'screened_1000.csv', screened)
    write_json(out / 'selected_source_records.json', raw)
    summary = {'n': len(screened),
               'formation_class': dict(Counter(r['formation_class'] for r in screened)),
               'hull_class': dict(Counter(r['hull_class'] for r in screened)),
               'numeric_available': {f: sum(r[f] != '' for r in screened) for f in SCALARS},
               'with_redox_relevant_elements': sum(bool(r['redox_elements']) for r in screened),
               'with_candidate_ion_elements': sum(bool(r['candidate_ion_elements']) for r in screened),
               'life_related_evidence': 'UNMEASURED for all 1000; no validated living or intelligent material',
               'screened_sha256': digest(out / 'screened_1000.csv'),
               'per_stratum': {s: {'count': sum(r['stratum'] == s for r in screened),
                                  'formation': dict(Counter(r['formation_class'] for r in screened if r['stratum'] == s)),
                                  'hull': dict(Counter(r['hull_class'] for r in screened if r['stratum'] == s))} for s in QUOTAS}}
    write_json(out / 'screen_summary.json', summary)
    print(json.dumps(summary, indent=2))


def verify(out, reference):
    files = ['eligible_inventory.csv', 'selected_1000.csv', 'selection_manifest.json',
             'screened_1000.csv', 'selected_source_records.json', 'screen_summary.json']
    comparisons = {f: digest(out / f) == digest(reference / f) for f in files}
    with (out / 'screened_1000.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    checks = {'exactly_1000': len(rows) == 1000, 'unique_ids': len({r['jid'] for r in rows}) == 1000,
              'all_carbon_free': all('C' not in r['elements'].split('|') for r in rows),
              'all_compounds': all(len(r['elements'].split('|')) >= 2 for r in rows),
              'life_unmeasured': all(all(r[k] == 'UNMEASURED' for k in ['autonomous_maintenance', 'replication',
                                      'functional_inheritance', 'learning', 'intelligence']) for r in rows),
              'byte_identical_replay': all(comparisons.values())}
    result = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks, 'file_comparisons': comparisons}
    write_json(out / 'verification.json', result)
    print(json.dumps(result, indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['select', 'screen', 'verify'])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--reference', type=Path)
    args = parser.parse_args()
    if args.command == 'verify':
        if args.reference is None:
            parser.error('--reference is required for verify')
        verify(args.out, args.reference)
    else:
        {'select': select, 'screen': screen}[args.command](args.out)
