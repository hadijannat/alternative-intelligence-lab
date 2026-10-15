#!/usr/bin/env python3
"""Independent source, selection, property and replay audit; imports no screen code."""
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
DB = LAB / 'database'


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def csv_rows(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))


def group(elements):
    if {'P', 'O'} <= elements:
        return 'phosphorus_oxygen'
    if {'Si', 'O'} <= elements:
        return 'silicon_oxygen'
    if 'S' in elements and 'O' not in elements:
        return 'sulfur_no_oxygen'
    if 'N' in elements and not elements & {'O', 'S'}:
        return 'nitrogen_no_oxygen_sulfur'
    return 'other_oxygen' if 'O' in elements else 'other'


def scalar(x):
    if isinstance(x, bool):
        return None
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def main():
    metadata = json.loads((HERE / 'figshare-live.json').read_text())
    official = next(f for f in metadata['files'] if f['id'] == 38521619)
    archive = DB / 'raw' / official['name']
    with zipfile.ZipFile(archive) as z:
        names = [n for n in z.namelist() if n.endswith('.json') and not n.startswith('__MACOSX/')]
        assert len(names) == 1
        source = json.loads(z.read(names[0]))
    checks = {
        'archive_md5_matches_independently_fetched_official_metadata': digest(archive, 'md5') == official['computed_md5'],
        'archive_size_matches_official': archive.stat().st_size == official['size'],
        'registry_matches_pinned_official_commit': digest(HERE / 'figshare-registry-live.py') == digest(DB / 'raw/figshare-pinned.py'),
        'official_license_cc_by_4': metadata['license']['name'] == 'CC BY 4.0',
    }
    source_by_id = {r['jid']: r for r in source}
    checks['all_source_ids_unique'] = len(source_by_id) == len(source)
    eligible, excluded = [], Counter()
    for row in source:
        elements = set(row['atoms']['elements'])
        if 'C' in elements:
            excluded['contains_carbon'] += 1
        elif len(elements) < 2:
            excluded['elemental_not_compound'] += 1
        else:
            eligible.append((hashlib.sha256(('noncarbon-screen-2026-10-15-v1|' + row['jid']).encode()).hexdigest(), row['jid'], group(elements)))
    eligible.sort()
    quotas = {'phosphorus_oxygen': 150, 'silicon_oxygen': 150, 'sulfur_no_oxygen': 200,
              'nitrogen_no_oxygen_sulfur': 100, 'other_oxygen': 300, 'other': 100}
    selected_ids = []
    for stratum, count in quotas.items():
        selected_ids.extend(jid for _, jid, g in [r for r in eligible if r[2] == stratum][:count])
    selected = csv_rows(DB / 'results-v1/selected_1000.csv')
    screened = csv_rows(DB / 'results-v1/screened_1000.csv')
    inventory = csv_rows(DB / 'results-v1/eligible_inventory.csv')
    retained_source = json.loads((DB / 'results-v1/selected_source_records.json').read_text())
    manifest = json.loads((DB / 'results-v1/selection_manifest.json').read_text())
    summary = json.loads((DB / 'results-v1/screen_summary.json').read_text())
    checks.update({
        'source_rows_75993': len(source) == 75993,
        'eligibility_count_and_exclusions': len(eligible) == 71739 and dict(excluded) == manifest['excluded'],
        'eligible_inventory_matches_source': [x[1] for x in eligible] == [r['jid'] for r in inventory],
        'selection_independently_reconstructed': set(selected_ids) == {r['jid'] for r in selected},
        'selected_and_screened_same_order': [r['jid'] for r in selected] == [r['jid'] for r in screened],
        'exactly_1000_unique_ids': len(screened) == len({r['jid'] for r in screened}) == 1000,
        'all_source_selected_rows_retained': retained_source == [source_by_id[r['jid']] for r in screened],
        'selected_and_protocol_hashes_match_manifest': digest(DB / 'results-v1/selected_1000.csv') == manifest['selection_sha256'] and digest(DB / 'PROTOCOL.md') == manifest['protocol_sha256'],
    })
    compositions, mismatches = set(), []
    fields = ['formation_energy_peratom', 'ehull', 'optb88vdw_bandgap', 'mbj_bandgap']
    counts = Counter()
    available = Counter()
    for row in screened:
        src = source_by_id[row['jid']]
        atoms = src['atoms']['elements']
        elements = set(atoms)
        assert 'C' not in elements and len(elements) >= 2
        atom_counts = Counter(atoms)
        divisor = math.gcd(*atom_counts.values())
        composition = '|'.join(f'{e}:{n // divisor}' for e, n in sorted(atom_counts.items()))
        compositions.add(composition)
        if composition != row['composition_key'] or src['formula'] != row['formula'] or '|'.join(sorted(elements)) != row['elements']:
            mismatches.append([row['jid'], 'identity'])
        for field in fields:
            if scalar(src.get(field)) != scalar(row[field]):
                mismatches.append([row['jid'], field])
            available[field] += scalar(row[field]) is not None
        formation = scalar(src.get('formation_energy_peratom'))
        hull = scalar(src.get('ehull'))
        fc = 'unknown' if formation is None else 'nonpositive_formation' if formation <= 0 else 'positive_formation'
        hc = 'unknown' if hull is None else 'negative_invalid' if hull < 0 else 'within_screen_threshold' if hull <= .1 else 'above_screen_threshold'
        if row['formation_class'] != fc or row['hull_class'] != hc:
            mismatches.append([row['jid'], 'classification'])
        counts[fc] += 1
        counts[hc] += 1
        counts['redox_element_present'] += bool(elements & set('V Cr Mn Fe Co Ni Cu Mo W'.split()))
        counts['ion_element_present'] += bool(elements & set('H Li Na K Rb Cs Ag Cu Mg Ca Zn'.split()))
    checks.update({
        'identity_4000_properties_and_threshold_classes_match_source': not mismatches,
        '923_distinct_reduced_compositions': len(compositions) == 923,
        'source_threshold_counts': counts['nonpositive_formation'] == 912 and counts['positive_formation'] == 88 and counts['within_screen_threshold'] == 680 and counts['above_screen_threshold'] == 320,
        'scalar_availability_matches_summary': dict(available) == summary['numeric_available'],
        'composition_flags_match_summary': counts['redox_element_present'] == summary['with_redox_relevant_elements'] and counts['ion_element_present'] == summary['with_candidate_ion_elements'],
        'life_and_novelty_not_fabricated': all(r['novelty_status'] == 'existing_database_structure' and all(r[k] == 'UNMEASURED' for k in ['autonomous_maintenance', 'replication', 'functional_inheritance', 'learning', 'intelligence']) for r in screened),
        'no_score_column': not any('score' in k for k in screened[0]),
    })
    replay_files = ['eligible_inventory.csv', 'selected_1000.csv', 'selection_manifest.json',
                    'screened_1000.csv', 'selected_source_records.json', 'screen_summary.json']
    replay = {name: {'main_sha256': digest(DB / 'results-v1' / name),
                     'replay_sha256': digest(DB / 'verification-v1' / name)} for name in replay_files}
    checks['all_six_fresh_process_replay_outputs_byte_identical'] = all(v['main_sha256'] == v['replay_sha256'] for v in replay.values())
    charges = {'Mo36_parent': 36 * 6 - 112 * 2,
               'Mo34_WVI_VV_hypothesis': 34 * 6 + 6 + 5 - 112 * 2,
               'Mo34_WVI_VIV_hypothesis': 34 * 6 + 6 + 4 - 112 * 2}
    checks['formal_charges_correct'] = charges == {'Mo36_parent': -8, 'Mo34_WVI_VV_hypothesis': -9, 'Mo34_WVI_VIV_hypothesis': -10}
    result = {'status': 'PASS_WITH_PROVENANCE_LIMITATION' if all(checks.values()) else 'FAIL',
              'checks': checks, 'source_rows': len(source), 'eligible': len(eligible),
              'excluded': dict(excluded), 'selected': len(screened), 'distinct_reduced_compositions': len(compositions),
              'counts': dict(counts), 'numeric_available': dict(available), 'mismatches': mismatches,
              'archive_sha256': digest(archive), 'official_file_metadata': official,
              'replay_file_hashes': replay, 'replay_exclusions': [], 'formal_charges': charges,
              'reviewed_screen_code_sha256': digest(DB / 'screen.py'),
              'provenance_limit': 'Protocol and selected IDs are hashed in the selection manifest, but no independent time-stamped pre-property code hash or immutable execution receipt is available. Property-blind selection is directly reproducible; chronology is not independently established.',
              'scope_limit': 'DFT crystal screen does not measure aqueous stability, molecular novelty, autonomy, inheritance or intelligence. Formal charge does not establish molecular structure or electron localization.'}
    (HERE / 'verification.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'checks_passed': sum(checks.values()), 'checks_total': len(checks), 'mismatches': mismatches, 'formal_charges': charges}, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
