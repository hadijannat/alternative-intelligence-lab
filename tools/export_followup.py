#!/usr/bin/env python3
"""Publish the dated follow-up using the archive's existing curation rules."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import stat
from urllib.parse import parse_qsl

import build_archive as archive
import curate_archive as curator

archive.TEXT.add('.xyz')

LABS = tuple(name + '-2026-10-15' for name in (
    'alternative-entity-lab', 'measured-coupling', 'noncarbon-discovery',
    'rna-coupled-chemistry', 'rna-inheritance-design', 'rna-mechanism',
    'rna-reaction-tests', 'rna-seed-transport', 'rna-turnover-tests',
    'recursive-compound'))
COORDINATES = {'recursive-compound-2026-10-15/' + name for name in (
    'identity/parent_heavy.xyz', 'parent-inputs/P0_A.xyz', 'parent-inputs/P0_B.xyz',
    'parent-inputs/PT57_A.xyz', 'parent-inputs/PT57_B.xyz')}
DERIVED = {'observations.csv', 'conditions.json', 'normalised.csv', 'normalized.csv'}
RAW_METADATA = {'acquisition.json', 'download_log.json', 'manifest.json'}
AUTHORED_SOURCE_NAMES = {
    'condition_ledger.csv', 'manifest.json', 'verification.json',
    'ghosh_HH_phase_concentrations.csv', 'ghosh_pellet_cleavage.csv',
    'levay_exchange.csv', 'sources.json', 'retrieval_receipts.json',
    'v1_calibration_residuals.csv', 'mechanism_retrieval.json'}


def strip_signed_urls(text):
    count = 0

    def replace(match):
        nonlocal count
        address, separator, query = match.group().partition('?')
        if not separator:
            return match.group()
        keys = {key.lower() for key, _ in parse_qsl(query.split('#', 1)[0])}
        if keys & {'signature', 'key-pair-id', 'x-amz-signature', 'x-goog-signature', 'access_token', 'token'}:
            count += 1
            return address
        return match.group()

    return re.sub(r'https?://[^\s\"<>]+', replace, text), count


def exclusion(rel, directory=False):
    parts = tuple(part.lower() for part in rel.parts)
    name = rel.name.lower()
    if rel.suffix.lower() == '.xyz' and rel.as_posix() not in COORDINATES:
        return 'coordinate file outside the authored parent-input scope'
    if any(part in {'author', 'source-extract', 'source_extract', 'downloads',
                    'screenshots', '.codex'} for part in parts):
        return 'third-party acquisition or private orchestration subtree'
    if '.omo' in parts:
        index = parts.index('.omo')
        if len(parts) > index + 1 and parts[index + 1] not in {'evidence', 'artifacts'}:
            return 'private orchestration subtree'
    if name in {'selected_source_records.json', 'figshare-registry-live.py',
                'figshare-live.json', 'figshare-registry.py'}:
        return 'third-party source snapshot; provenance and derived outputs retained'
    if 'raw' in parts and not directory and name not in RAW_METADATA:
        return 'third-party raw payload; source URL/hash retained in ledgers'
    if not directory and name.startswith(('si13-page', 'page-')):
        return 'acquired publication screenshot'
    reason = archive.decision(rel, directory)
    own_source = ('sources' in parts and 'rna-mechanism-2026-10-15' in parts
                  and (rel.name in AUTHORED_SOURCE_NAMES or 'normalized' in parts))
    if reason and not directory and (name in DERIVED or own_source) and reason.startswith('acquired source payload;'):
        reason = None
    return reason or curator.path_exclusion(rel.as_posix())


def export(source, output):
    if output.exists():
        raise ValueError('Fresh destination required')
    archive.GROUPS.update(LABS)
    records = []
    for lab in LABS:
        if not (source / lab).is_dir():
            raise ValueError('Missing laboratory: ' + lab)
        pending = [source / lab]
        while pending:
            for path in sorted(pending.pop().iterdir()):
                rel = path.relative_to(source)
                if archive.PROTECTED.lower() in path.name.lower():
                    records.append(dict(path=str(rel), status='excluded', reason='protected source payload; unopened'))
                    continue
                st = path.lstat()
                directory = stat.S_ISDIR(st.st_mode)
                reason = exclusion(rel, directory)
                if stat.S_ISLNK(st.st_mode) or (not directory and st.st_nlink != 1):
                    reason = 'linked entry; target not read'
                if directory:
                    if not reason:
                        pending.append(path)
                    else:
                        records.append(dict(path=str(rel), status='excluded', reason=reason, scope='subtree'))
                    continue
                if not stat.S_ISREG(st.st_mode):
                    reason = reason or 'nonregular filesystem entry'
                record = dict(path=str(rel), status='excluded' if reason else 'candidate', reason=reason, source_size=st.st_size)
                records.append(record)
                if reason:
                    continue
                record['_fingerprint'] = archive.fingerprint(st)
                stream = archive.prepare(source, record)
                if stream is None:
                    record.pop('_fingerprint')
                    continue
                with stream:
                    data = stream.read()
                if path.suffix.lower() in archive.TEXT:
                    text = data.decode('utf-8')
                    text, signed_count = strip_signed_urls(text)
                    if signed_count:
                        record['transformations'].append(dict(transformation='signed URL query removed; stable URL retained', count=signed_count))
                        data = text.encode('utf-8')
                    if path.suffix.lower() == '.json' and curator.tool_envelope(json.loads(text), str(rel)):
                        record.update(status='excluded', reason='structured tool execution envelope')
                        record.pop('_fingerprint')
                        continue
                    if path.suffix.lower() == '.jsonl' and any(curator.tool_envelope(json.loads(line), str(rel)) for line in text.splitlines() if line.strip()):
                        record.update(status='excluded', reason='structured tool execution envelope')
                        record.pop('_fingerprint')
                        continue
                    if '\r\n' in text:
                        record['transformations'].append(dict(transformation='LF line endings for Git text attributes', count=text.count('\r\n')))
                        data = text.replace('\r\n', '\n').encode('utf-8')
                    if archive.HOST.search(data.decode('utf-8')) or archive.KEY.search(data.decode('utf-8')):
                        raise ValueError('Unredacted text: ' + str(rel))
                if len(data) >= 100 * 1024 * 1024:
                    raise ValueError('GitHub file limit: ' + str(rel))
                if archive.fingerprint(path.lstat()) != record.pop('_fingerprint'):
                    raise ValueError('Source changed during export: ' + str(rel))
                destination = output / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                record.update(published_size=len(data), published_sha256=hashlib.sha256(data).hexdigest())
    records.sort(key=lambda r: r['path'])
    included = [r for r in records if r['status'] == 'included']
    manifest = dict(date='2026-10-15', scientific_validation=False,
                    source_root='PROJECT_ROOT', labs=list(LABS),
                    included_files=len(included), published_bytes=sum(r['published_size'] for r in included),
                    unique_published_blobs=len({r['published_sha256'] for r in included}),
                    excluded_entries=sum(r['status'] == 'excluded' for r in records),
                    per_lab=dict(Counter(r['path'].split('/')[0] for r in included)), files=records)
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    export(args.source.resolve(), args.output.resolve())
