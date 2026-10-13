#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description='Index generated, verified research archives for publication')
    parser.add_argument('--archive-dir', type=Path, required=True)
    args = parser.parse_args()
    source = args.archive_dir.resolve()
    root = Path(__file__).resolve().parents[1]
    manifest_path = source / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    base_url = 'https://github.com/hadijannat/alternative-intelligence-lab/releases/download/research-2026-10-13/'
    assets = []
    for record in manifest['archives']:
        asset = source / record['name']
        if asset.stat().st_size != record['size']:
            raise ValueError('Archive size differs: ' + record['name'])
        assets.append({**record, 'url': base_url + record['name']})
    catalogue = {
        'snapshot': '2026-10-13', 'scientific_validation': False,
        'scope': 'Existing authored scientific record, with declared exclusions and sanitization',
        'archives': assets,
        'included_files': sum(r['status'] == 'included' for r in manifest['files']),
        'excluded_entries': sum(r['status'] == 'excluded' for r in manifest['files']),
        'published_uncompressed_bytes': sum(r.get('published_size', 0) for r in manifest['files'] if r['status'] == 'included'),
        'compressed_archive_bytes': sum(r['size'] for r in assets),
        'groups': manifest['groups'],
        'archive_manifest_url': base_url + 'manifest.json',
        'archive_manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        'byte_verification': manifest['verification'],
    }
    (root / 'data/archive-catalogue.json').write_text(json.dumps(catalogue, indent=2) + '\n')
    shutil.copyfile(source / 'result-report-index.csv', root / 'data/research-index.csv')
    print(json.dumps({k: catalogue[k] for k in ('included_files', 'excluded_entries',
                                             'published_uncompressed_bytes', 'compressed_archive_bytes')}))


if __name__ == '__main__':
    main()
