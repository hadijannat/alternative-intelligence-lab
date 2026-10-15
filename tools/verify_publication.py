#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from verify_followup import verify as verify_followup

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    snapshot = json.loads((ROOT / 'data/snapshot.json').read_text())
    require(snapshot['scientific_goal'] == 'UNMET', 'Scientific outcome changed')
    require(snapshot['chemical_goal_status'] == 'BLOCKED', 'Chemical status changed')
    require(set(snapshot['integrated_gates'].values()) == {'UNRESOLVED'}, 'Gate upgrade')
    require(snapshot['scientific_runs_during_publication'] == 0, 'Publication scope changed')
    constants = json.loads((ROOT / 'data/qualified-source-constants.json').read_text())
    require(constants['scientific_calculation_performed'] is False, 'Constant projection scope')
    require(set(constants['qualified_parameters']) == {'e', 'NA', 'F'}, 'Qualified constants missing')
    admission = json.loads((ROOT / 'data/source-admission-findings.json').read_text())
    require(len(admission) == 2 and all(x['decision'] and x['scientific_calculation_performed'] is False for x in admission),
            'Negative source-admission findings missing')
    require(all('records' not in x and 'calls' not in x for x in admission), 'Raw capture fields in projection')
    with (ROOT / 'data/candidates.csv').open(newline='') as stream:
        candidates = list(csv.DictReader(stream))
    require(len(candidates) == 329, 'Preparation count')
    require(len({x['candidate_id'] for x in candidates}) == 329, 'Duplicate preparation ID')
    require(len({x['family'] for x in candidates}) == 58, 'Architecture-group count')
    for row in candidates:
        require(isinstance(json.loads(row['gates']), dict), 'Candidate gate encoding')
    ledger = json.loads((ROOT / 'data/initial-evidence-ledger.json').read_text())
    require(len(ledger) == 34, 'Initial-ledger count')
    require(all(x['source'].startswith('https://') and x['limitations'] for x in ledger),
            'Claim provenance or limitations absent')
    mo = json.loads((ROOT / 'data/mo36-encounter-full.json').read_text())
    require(mo['main_count'] == len(mo['rows']) == 480, 'Mo36 case count')
    require(mo['status'] == 'PASS_NUMERICAL_CONTROLS_ONLY', 'Mo36 evidence class')
    require(all(math.isfinite(v) for row in mo['rows'] for v in row if isinstance(v, (int, float))),
            'Nonfinite Mo36 output')
    with (ROOT / 'data/mo36-encounter-illustrative.csv').open(newline='') as stream:
        for summary in csv.DictReader(stream):
            salt = float(summary['added_nacl_M'])
            for rep in ('point', 'shell'):
                rows = [r for r in mo['rows'] if r[:5] == [salt, 50, 0, 0.5, rep]]
                require(len(rows) == 1, 'Illustrative scenario missing')
                require(abs(rows[0][7] - float(summary['L_' + rep])) <= 0.00051,
                        'Figure values differ from saved full output')
    links = 0
    for path in [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('*.md'))]:
        text = path.read_text()
        targets = re.findall(r'(?<!!)\[[^\]\n]*\]\(([^)]+)\)', text)
        targets += re.findall(r'!\[[^\]\n]*\]\(([^)]+)\)', text)
        targets += re.findall(r'(?:src|href)="([^"]+)"', text)
        for target in targets:
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            require((path.parent / target).is_file(), 'Broken relative link: ' + target)
            links += 1
    for asset in ('hero.svg', 'mo36-encounter-illustrative.svg', 'cco-summary.svg'):
        root = ET.parse(ROOT / 'assets' / asset).getroot()
        require(root.get('viewBox') is not None, 'Unscalable SVG')
        require(root.find('{http://www.w3.org/2000/svg}title') is not None, 'SVG title missing')
        require(root.find('{http://www.w3.org/2000/svg}desc') is not None, 'SVG description missing')
    catalogue = json.loads((ROOT / 'data/archive-catalogue.json').read_text())
    require(catalogue['scientific_validation'] is False, 'Packaging/science conflation')
    require(catalogue['archives'] and catalogue['included_files'] > 0, 'Empty research archive')
    for asset in catalogue['archives']:
        require(re.fullmatch('[a-f0-9]{64}', asset['sha256']) is not None, 'Archive checksum')
        require(0 < asset['size'] <= 512 * 1024 * 1024, 'Archive size')
        require(asset['url'].startswith('https://github.com/hadijannat/alternative-intelligence-lab/releases/download/'),
                'Unexpected release asset destination')
    with (ROOT / 'data/research-index.csv').open(newline='') as stream:
        index = list(csv.DictReader(stream))
    require(len(index) == catalogue['included_files'], 'Archive index count')
    require(any(x['path'] == 'cco/REPORT.md' for x in index), 'CCO report absent')
    require(any(x['path'] == '.omo/evidence/e1092-research-report.md' for x in index),
            'Final checkpoint report absent')
    require(any(x['path'] == 'discovery-loop/candidate_registry.json' for x in index),
            'Full canonical registry absent')
    print(json.dumps({'status': 'PASS_PUBLICATION_ONLY', 'preparations': 329,
                      'groups': 58, 'main_cases': 480, 'local_links': links,
                      'archived_files': len(index), 'scientific_reruns': 0}))
    print(json.dumps(verify_followup(ROOT)))


if __name__ == '__main__':
    main()
