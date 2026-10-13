#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

sys.set_int_max_str_digits(0)


def main():
    parser = argparse.ArgumentParser(description='Export saved publication data without executing scientific models')
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    output = Path(__file__).resolve().parents[1] / 'data'
    output.mkdir(exist_ok=True)
    paths = [
        'discovery-loop/candidate_registry.json',
        '.omo/evidence/mo36-resume-encounter-native-2026-10-13.json',
        'alternative-biochemistry-2026-10-06/data/evidence_ledger.json',
        '.omo/evidence/e1092-research-report.md',
        'cco/REPORT.md',
    ]
    raw = {p: (source / p).read_bytes() for p in paths}
    registry = json.loads(raw[paths[0]])
    packet = json.loads(raw[paths[1]])
    result = json.loads(json.loads(packet['native']['output'])['stdout'])
    ledger = json.loads(raw[paths[2]])
    if not (registry['version'] == '2.44' and len(registry['candidates']) == 329
            and len({r['family'] for r in registry['candidates']}) == 58
            and result['main_count'] == 480 and len(result['rows']) == 480
            and len(ledger) == 34):
        raise ValueError('Saved snapshot differs from the declared publication')

    def sanitize(text):
        text = text.replace(str(source), 'PROJECT_ROOT')
        return re.sub(r'/Users/[^/\s\"\x27<>]+', '/USER_HOME', text)

    fields = ['candidate_id', 'family', 'track', 'structural_chemistry', 'medium',
              'environment', 'essential_carbon', 'information',
              'maintenance_growth_reproduction', 'cognition', 'A', 'B', 'C',
              'gates', 'evidence']
    with (output / 'candidates.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in registry['candidates']:
            writer.writerow({k: sanitize(json.dumps(row.get(k, ''), ensure_ascii=False))
                             if isinstance(row.get(k), (dict, list))
                             else sanitize(str(row.get(k, ''))) for k in fields})
    (output / 'mo36-encounter-full.json').write_text(
        sanitize(json.dumps(result, indent=2, ensure_ascii=False)) + '\n', encoding='utf-8')
    (output / 'initial-evidence-ledger.json').write_text(
        sanitize(json.dumps(ledger, indent=2, ensure_ascii=False)) + '\n', encoding='utf-8')
    snapshot = {
        'snapshot': '2026-10-13', 'registry_version': '2.44',
        'preparations': 329, 'architecture_groups': 58,
        'scientific_goal': 'UNMET', 'chemical_goal_status': 'BLOCKED',
        'integrated_gates': {'G' + str(i): 'UNRESOLVED' for i in range(7)},
        'scientific_runs_during_publication': 0,
        'source_sha256': {p: hashlib.sha256(v).hexdigest() for p, v in raw.items()},
        'core_exports': {
            'candidates.csv': 'Column projection; complete original registry in archive',
            'mo36-encounter-full.json': 'Parsed saved numerical stdout; no model execution',
            'initial-evidence-ledger.json': 'Earlier bounded 34-claim review',
        },
    }
    (output / 'snapshot.json').write_text(json.dumps(snapshot, indent=2) + '\n')
    print(json.dumps({'status': 'EXPORTED_SAVED_DATA_ONLY', 'candidates': 329,
                      'main_cases': 480, 'initial_claims': 34}))


if __name__ == '__main__':
    main()
