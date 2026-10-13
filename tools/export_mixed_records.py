#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import tarfile


def saved_record(archive_dir, manifest, source):
    record = next(r for r in manifest['files'] if r['path'] == source)
    if record['status'] != 'included' or len(record['chunks']) != 1:
        raise ValueError('Expected one intact source member')
    chunk = record['chunks'][0]
    archive = next(a for a in manifest['archives'] if a['name'] == chunk['archive'])
    path = archive_dir / archive['name']
    with path.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != archive['sha256']:
            raise ValueError('Input archive hash mismatch')
    with tarfile.open(path, 'r:gz') as tar:
        member = tar.getmember(chunk['name'])
        if not member.isfile():
            raise ValueError('Expected a regular source member')
        raw = tar.extractfile(member).read()
    if hashlib.sha256(raw).hexdigest() != record['published_sha256']:
        raise ValueError('Source member hash mismatch')
    return record, json.loads(raw)


def projection(source, record, selected):
    return {
        'source_path': source,
        'source_original_sha256': record['source_sha256'],
        'source_published_sha256': record['published_sha256'],
        'projection': 'Own findings retained; raw provider captures excluded',
        'scientific_calculation_performed': False,
        **selected,
    }


def main():
    parser = argparse.ArgumentParser(description='Preserve own findings from mixed acquisition records')
    parser.add_argument('--archive-dir', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((args.archive_dir / 'manifest.json').read_text())
    output = Path(__file__).resolve().parents[1] / 'data'
    source = '.omo/artifacts/Mg-charge-budget-next/constant-captures.json'
    record, value = saved_record(args.archive_dir, manifest, source)
    selected = {key: value[key] for key in ('experiment_id', 'registered_at_utc', 'read_extent', 'qualified_parameters')}
    if set(selected['qualified_parameters']) != {'e', 'NA', 'F'}:
        raise ValueError('Qualified constant fields changed')
    result = projection(source, record, selected)
    (output / 'qualified-source-constants.json').write_text(json.dumps(result, indent=2) + '\n')
    findings = []
    for source, omitted in (
        ('.omo/evidence/e878-primary-route-packet.json', 'records'),
        ('.omo/evidence/e910-mo248-primary.json', 'calls'),
    ):
        record, value = saved_record(args.archive_dir, manifest, source)
        selected = {key: item for key, item in value.items() if key != omitted}
        if not selected.get('decision') or not isinstance(value[omitted], list):
            raise ValueError('Expected mixed source-admission record')
        findings.append(projection(source, record, selected))
    (output / 'source-admission-findings.json').write_text(json.dumps(findings, indent=2) + '\n')
    print(json.dumps({'status': 'EXPORTED_SAVED_FIELDS_ONLY', 'mixed_records': 3, 'scientific_calculations': 0}))


if __name__ == '__main__':
    main()
