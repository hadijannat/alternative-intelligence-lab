#!/usr/bin/env python3
"""Package existing research artifacts; never execute scientific code."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tarfile
import tempfile
import zlib

sys.set_int_max_str_digits(0)
GROUPS = set('alternative-biochemistry-2026-10-06 cco claude-run discovery-loop metal-oxide noncarbon simulation virtual-lab data results figures src tests docs references'.split())
BLOCKED = set('.git .venv venv env site-packages node_modules __pycache__ publication tools session sessions skills .claude .agents supplementary cache .pytest_cache .ruff_cache .hypothesis .remember'.split())
TEXT = set('.md .py .csv .json .jsonl .yaml .yml .toml .ini .cfg .html .css .js .mjs .svg .bib .tex .sh .txt .tsv .r .jl .c .h .cpp'.split())
BINARY = set('.npz .npy .pt .sqlite .sqlite3 .db .png .jpg .jpeg .webp .gif .gz'.split())
PROTECTED = '41467_2024_55701_MOESM4_ESM'
SECRET_NAME = re.compile(r'(^|[_.-])(credentials?|keyring|secrets?|tokens?|cookies?)([_.-]|$)', re.I)
HOST = re.compile(r'/(?:Users|home)/[^/\s\"\x27<>]+')
KEY = re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b')
ASSIGNMENT = re.compile(r'(?i)([\"\x27]?(?:api_key|access_token|refresh_token|password|client_secret)[\"\x27]?\s*[:=]\s*)[\"\x27]([^\"\x27\r\n]{8,})[\"\x27]')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(st):
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def decision(rel, is_dir=False):
    parts = rel.parts
    name = rel.name.lower()
    if PROTECTED.lower() in name:
        return 'protected source payload: no stat or content access'
    if any(p.lower() in BLOCKED for p in parts):
        return 'dependency, acquired-source, cache, session, tooling, or publication subtree'
    if name.startswith('.env') or SECRET_NAME.search(name):
        return 'potential credential material'
    if parts[0] == '.omo':
        if len(parts) > 1 and parts[1] not in {'evidence', 'artifacts'}:
            return 'orchestration metadata'
        if not is_dir and rel.suffix.lower() not in {'.md', '.py', '.csv', '.sqlite', '.json'}:
            return 'evidence format outside scientific allowlist'
    elif parts[0] not in GROUPS and not (len(parts) == 1 and not is_dir and (name in {'readme.md', 'report.md', 'dashboard.html', 'workplan.md', 'requirements.txt', 'pyproject.toml'} or name.startswith('references'))):
        return 'outside research publication scope'
    if is_dir:
        return None
    suffix = rel.suffix.lower()
    if set(parts).intersection({'sources', 'source'}) and suffix not in {'.md', '.py'} and not (suffix in {'.json', '.csv'} and any(label in name for label in ('analysis', 'summary', 'metadata', 'provenance', 'license', 'audit', 'result'))):
        return 'acquired source payload; authored reports/code and named derived metadata remain eligible'
    if suffix not in TEXT | BINARY:
        return 'unapproved format, acquired document, or raw payload'
    if suffix == '.txt' and name != 'requirements.txt' and not set(parts).intersection({'models', 'experiments', 'results'}):
        return 'text log or raw web body outside own model/experiment/results scope'
    if any(x in name for x in ('stdout', 'stderr', 'transcript', 'web-response', 'web_response', 'raw_response', 'raw-web', 'raw_web')):
        return 'tool log or raw web body'
    return None


def inventory(source):
    records = []

    def walk(directory):
        for path in sorted(directory.iterdir(), key=lambda p: p.name):
            rel = path.relative_to(source)
            # Check protected names before even lstat; never follow links.
            reason = 'protected source payload: no stat or content access' if PROTECTED.lower() in path.name.lower() else None
            if not reason and any(p.lower() in BLOCKED for p in rel.parts):
                reason = 'dependency, acquired-source, cache, session, tooling, or publication subtree'
            if not reason and (path.name.lower().startswith('.env') or SECRET_NAME.search(path.name)):
                reason = 'potential credential material'
            if reason:
                records.append({'path': rel.as_posix(), 'status': 'excluded', 'reason': reason, 'scope': 'entry/subtree; contents not enumerated'})
                continue
            st = path.lstat()
            if stat.S_ISLNK(st.st_mode):
                reason = 'symbolic link: target never opened'
            elif stat.S_ISDIR(st.st_mode):
                reason = decision(rel, True)
                if reason:
                    records.append({'path': rel.as_posix(), 'status': 'excluded', 'reason': reason, 'scope': 'subtree; contents not enumerated'})
                else:
                    walk(path)
                continue
            elif not stat.S_ISREG(st.st_mode):
                reason = 'nonregular filesystem entry'
            elif st.st_nlink != 1:
                reason = 'multiply linked file: potential protected-payload alias'
            else:
                reason = decision(rel)
            record = {'path': rel.as_posix(), 'status': 'excluded' if reason else 'candidate', 'reason': reason or 'own research source, protocol, report, figure, or numerical artifact', 'source_size': st.st_size}
            if not reason:
                record['_fingerprint'] = fingerprint(st)
            records.append(record)
    walk(source)
    return records


def sanitize(text, source):
    operations = []
    for pattern, replacement, label in ((re.escape(str(source)), 'PROJECT_ROOT', 'project path'), (HOST, '/USER_HOME', 'host home path'), (KEY, '[REDACTED_CREDENTIAL]', 'credential pattern'), (ASSIGNMENT, r'\1"[REDACTED_CREDENTIAL]"', 'credential assignment')):
        text, count = re.subn(pattern, replacement, text)
        if count:
            operations.append({'transformation': label, 'count': count})
    return text, operations


def native_receipt(value):
    if isinstance(value, list):
        return any(native_receipt(item) for item in value)
    if not isinstance(value, dict):
        return False
    native = value.get('native')
    if isinstance(native, dict) and 'output' in native and any(key in native for key in ('chunk_id', 'session_id', 'wall_time_seconds', 'exit_code', 'tool_name', 'call_id')):
        return True
    return (isinstance(value.get('tool_calls'), list) or isinstance(value.get('tool_result'), dict) or (isinstance(value.get('content'), list) and any(key in value for key in ('isError', 'structuredContent'))) or ('output' in value and any(isinstance(value.get(key), str) for key in ('tool', 'tool_name', 'call_id'))))


def prepare(source, record):
    path = source / record['path']
    suffix = path.suffix.lower()
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        if fingerprint(os.fstat(stream.fileno())) != record['_fingerprint']:
            raise RuntimeError('Source changed before read: ' + record['path'])
        if suffix == '.gz':
            record['source_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
            stream.seek(0)
            published = tempfile.TemporaryFile()
            totals = {}
            try:
                with gzip.GzipFile(fileobj=stream, mode='rb') as unzipped:
                    with io.TextIOWrapper(unzipped, encoding='utf-8', newline='') as lines:
                        with gzip.GzipFile(filename='', fileobj=published, mode='wb', mtime=0, compresslevel=1) as zipped:
                            for line in lines:
                                transformed, operations = sanitize(line, source)
                                for operation in operations:
                                    label = operation['transformation']
                                    totals[label] = totals.get(label, 0) + operation['count']
                                zipped.write(transformed.encode('utf-8'))
            except (UnicodeDecodeError, gzip.BadGzipFile, EOFError, zlib.error):
                published.close()
                record.update(status='excluded', reason='gzip trace could not be safely decoded as UTF-8')
                return None
            if fingerprint(os.fstat(stream.fileno())) != record['_fingerprint']:
                published.close()
                raise RuntimeError('Source changed during read: ' + record['path'])
            size = published.tell()
            published.seek(0)
            checksum = hashlib.file_digest(published, 'sha256').hexdigest()
            transformations = [{'transformation': label, 'count': count} for label, count in sorted(totals.items())]
            transformations.append({'transformation': 'deterministic gzip recompression level 1', 'count': 1})
            record.update(status='included', published_size=size, published_sha256=checksum, transformations=transformations)
            published.seek(0)
            return published
        if suffix in BINARY and suffix != '.gz':
            published = tempfile.TemporaryFile()
            checksum = hashlib.sha256()
            while chunk := stream.read(1024 * 1024):
                checksum.update(chunk)
                published.write(chunk)
            if fingerprint(os.fstat(stream.fileno())) != record['_fingerprint']:
                published.close()
                raise RuntimeError('Source changed during read: ' + record['path'])
            record.update(status='included', source_sha256=checksum.hexdigest(), published_size=published.tell(), published_sha256=checksum.hexdigest(), transformations=[])
            published.seek(0)
            return published
        raw = stream.read()
        if fingerprint(os.fstat(stream.fileno())) != record['_fingerprint']:
            raise RuntimeError('Source changed during read: ' + record['path'])
    record['source_sha256'] = digest(raw)
    transformations = []
    if suffix in TEXT:
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            record.update(status='excluded', reason='allowlisted text/trace could not be safely decoded')
            return None
        if suffix == '.json':
            try:
                value = json.loads(text)
            except (ValueError, RecursionError):
                record.update(status='excluded', reason='invalid or excessively nested JSON')
                return None
            if native_receipt(value):
                record.update(status='excluded', reason='native tool receipt; scientific outputs must be independently exported')
                return None
        if suffix == '.jsonl':
            try:
                if any(native_receipt(json.loads(line)) for line in text.splitlines() if line.strip()):
                    record.update(status='excluded', reason='JSONL includes native tool receipts')
                    return None
            except (ValueError, RecursionError):
                record.update(status='excluded', reason='invalid or excessively nested JSONL')
                return None
        text, transformations = sanitize(text, source)
        data = text.encode('utf-8')
    else:
        data = raw
    record.update(status='included', published_size=len(data), published_sha256=digest(data), transformations=transformations)
    return io.BytesIO(data)


def build(source, output, limit, dry_run=False):
    records = inventory(source)
    if dry_run:
        print(json.dumps({'mode': 'inventory-only; content decisions and hashes deferred', 'candidate_bytes': sum(r.get('source_size', 0) for r in records if r['status'] == 'candidate'), 'records': [{k: v for k, v in r.items() if not k.startswith('_')} for r in records]}, indent=2))
        return
    if output.exists():
        raise ValueError('Output must not already exist; choose a fresh directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.archive-build-', dir=output.parent) as temp:
        staging = Path(temp)
        archives = []
        members = []
        tar = zipped = destination = None
        used = 0

        def close_shard():
            nonlocal tar, zipped, destination
            if tar is None:
                return
            tar.close()
            zipped.close()
            destination.close()
            artifact = staging / archives[-1]['name']
            if artifact.stat().st_size > limit:
                raise RuntimeError('Compressed shard exceeds size limit')
            with tarfile.open(artifact, 'r:gz') as check:
                actual = check.getmembers()
                if len(actual) != len(members):
                    raise RuntimeError('Archive member count mismatch')
                for item, expected in zip(actual, members):
                    with check.extractfile(item) as recovered:
                        recovered_sha256 = hashlib.file_digest(recovered, 'sha256').hexdigest()
                    if item.name != expected['name'] or recovered_sha256 != expected['sha256']:
                        raise RuntimeError('Archive member verification failed')
            with artifact.open('rb') as archive_bytes:
                checksum = hashlib.file_digest(archive_bytes, 'sha256').hexdigest()
            archives[-1].update(size=artifact.stat().st_size, sha256=checksum, verified_member_count=len(members))
            tar = None

        for record in records:
            if record['status'] != 'candidate':
                continue
            data = prepare(source, record)
            if data is None:
                continue
            record['chunks'] = []
            capacity = limit - 2 * 1024 * 1024
            for offset in range(0, max(1, record['published_size']), capacity):
                chunk = data.read(capacity)
                cost = ((len(chunk) + 511) // 512 + 4) * 512
                if tar is None or used + cost > capacity:
                    close_shard()
                    name = f'research-{len(archives) + 1:04d}.tar.gz'
                    archives.append({'name': name})
                    destination = (staging / name).open('wb')
                    zipped = gzip.GzipFile(filename='', mode='wb', fileobj=destination, mtime=0, compresslevel=1)
                    tar = tarfile.open(fileobj=zipped, mode='w', format=tarfile.PAX_FORMAT)
                    members = []
                    used = 0
                name = record['path'] if record['published_size'] <= capacity else record['path'] + f'.archive-part-{offset // capacity:04d}'
                info = tarfile.TarInfo(name)
                info.size = len(chunk)
                info.mode = 0o644
                tar.addfile(info, io.BytesIO(chunk))
                member = {'name': name, 'sha256': digest(chunk), 'size': len(chunk), 'offset': offset, 'archive': archives[-1]['name']}
                members.append(member)
                record['chunks'].append(member)
                used += cost
            data.close()
        close_shard()
        for record in records:
            if '_fingerprint' in record:
                if fingerprint((source / record['path']).lstat()) != record.pop('_fingerprint'):
                    raise RuntimeError('Source changed during archive build: ' + record['path'])
        summaries = {}
        for record in records:
            group = record['path'].split('/')[0]
            summary = summaries.setdefault(group, {'included_files': 0, 'excluded_entries': 0, 'published_bytes': 0})
            summary['included_files' if record['status'] == 'included' else 'excluded_entries'] += 1
            summary['published_bytes'] += record.get('published_size', 0)
        with (staging / 'result-report-index.csv').open('w', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(['path', 'group', 'kind', 'published_size', 'published_sha256', 'archives'])
            for r in records:
                if r['status'] == 'included':
                    writer.writerow([r['path'], r['path'].split('/')[0], Path(r['path']).suffix, r['published_size'], r['published_sha256'], ';'.join(dict.fromkeys(c['archive'] for c in r['chunks']))])
        manifest = {'schema_version': 1, 'source_root': 'PROJECT_ROOT', 'archive_limit_bytes': limit, 'gzip_compression_level': 1, 'verification': 'Each recovered tar member SHA256 matched the published chunk bytes; no scientific results were revalidated.', 'groups': summaries, 'archives': archives, 'files': records}
        (staging / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
        staging.rename(output)
    print(json.dumps({'output': str(output), 'archives': len(archives), 'included_files': sum(r['status'] == 'included' for r in records)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--max-shard-mib', type=int, default=512)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.max_shard_mib < 4:
        parser.error('--max-shard-mib must be at least 4')
    build(args.source.resolve(), args.output.absolute(), args.max_shard_mib * 1024 * 1024, args.dry_run)


if __name__ == '__main__':
    main()
