#!/usr/bin/env python3
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import tarfile
import tempfile

from build_archive import HOST, KEY, TEXT

sys.set_int_max_str_digits(0)


def checksum(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_name(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Unsafe archive path')
    return name


def path_exclusion(name):
    path = PurePosixPath(name)
    parts = tuple(part.lower() for part in path.parts)
    if parts[:2] == ('.omo', 'artifacts') and path.name.lower() == 'web-return.json':
        return 'curation: raw web acquisition return'
    if path.name.lower().startswith(('provider-', 'provider_')) and path.name.lower().endswith(('-capture.json', '_capture.json')):
        return 'curation: provider tool capture; standalone scientific results remain eligible'
    if any(part in {'.legacy-scipy', 'vendor'} for part in parts):
        return 'curation: bundled third-party dependency subtree'
    if any(part.lower() in {'source-extract', 'source_extract', 'source-extracts'} for part in path.parts):
        return 'curation: acquired source extraction subtree'
    if path.suffix.lower() == '.txt' and path.name.lower() not in {'requirements.txt', 'settings.txt', 'own-reason-notes.txt', 'own_reason_notes.txt'}:
        return 'curation: unverified text acquisition/log; retain explicit own settings/reason notes only'
    return None


def tool_envelope(value, name=''):
    path = PurePosixPath(name)
    basename = path.name.lower()
    acquisition = tuple(part.lower() for part in path.parts[:1]) == ('.omo',) and len(path.parts) > 1 and path.parts[1].lower() in {'artifacts', 'evidence'} and any(token in basename for token in ('capture', 'provider', 'primary', 'book', 'source-return', 'source_return', 'search-return', 'search_return')) and not any(token in basename for token in ('protocol', 'selection', 'qualified_parameters', 'qualified-parameters', 'bookkeeping', 'analytical'))
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(child for child in item if isinstance(child, (dict, list)))
        elif isinstance(item, dict):
            if acquisition and set(item).intersection({'args', 'arguments', 'registered_args', 'request', 'invocation'}) and set(item).intersection({'actual', 'actual_return', 'provider_return', 'result', 'return', 'actual_visible_return'}):
                return True
            if acquisition and isinstance(item.get('initial_queries'), str) and isinstance(item.get('actual_primary_navigation'), str):
                return True
            if isinstance(item.get('args'), dict) and isinstance(item.get('actual'), str):
                return True
            output = item.get('output')
            if isinstance(output, str):
                if any(isinstance(item.get(key), (int, float)) and not isinstance(item.get(key), bool) for key in ('exit_code', 'wall_time_seconds', 'session_id')):
                    return True
                if any(isinstance(item.get(key), str) for key in ('tool_name', 'call_id')):
                    return True
            if isinstance(item.get('tool_calls'), list) and any(isinstance(call, dict) and ('function' in call or 'tool_name' in call) for call in item['tool_calls']):
                return True
            if isinstance(item.get('content'), list) and isinstance(item.get('isError'), bool):
                return True
            stack.extend(child for child in item.values() if isinstance(child, (dict, list)))
    return False


def scan_text(stream):
    for line in stream:
        if HOST.search(line) or KEY.search(line):
            raise ValueError('Retained text contains an unredacted host path or credential pattern')


def inspect_file(path, name, validation):
    suffix = PurePosixPath(name).suffix.lower()
    if suffix == '.json':
        with path.open(encoding='utf-8') as handle:
            value = json.load(handle)
        if tool_envelope(value, name):
            return 'curation: structured tool execution envelope (including nested receipts)'
        validation['retained_json_files'] += 1
        stack = [value]
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                if any(isinstance(child, (int, float)) and not isinstance(child, bool) for child in item):
                    validation['json_arrays_containing_numbers'] += 1
                stack.extend(child for child in item if isinstance(child, (dict, list)))
            elif isinstance(item, dict):
                stack.extend(child for child in item.values() if isinstance(child, (dict, list)))
    elif suffix == '.jsonl':
        with path.open(encoding='utf-8') as handle:
            for line in handle:
                if line.strip() and tool_envelope(json.loads(line), name):
                    return 'curation: JSONL tool execution envelope'
        validation['retained_jsonl_files'] += 1
    if suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8', newline='') as handle:
            scan_text(handle)
        validation['retained_gzip_traces_scanned'] += 1
    elif suffix in TEXT:
        with path.open(encoding='utf-8', newline='') as handle:
            scan_text(handle)
        validation['retained_text_files_scanned'] += 1
    return None


def curate(source, output):
    if output.exists():
        raise ValueError('Fresh output directory required')
    manifest_path = source / 'manifest.json'
    original_manifest_hash = checksum(manifest_path)
    manifest = json.loads(manifest_path.read_text())
    records = manifest['files']
    archive_records = {safe_name(a['name']): a for a in manifest['archives']}
    members = {}
    candidates = {}
    reasons = {}
    validation = dict(retained_json_files=0, retained_jsonl_files=0, json_arrays_containing_numbers=0, retained_gzip_traces_scanned=0, retained_text_files_scanned=0, verified_input_members=0, verified_output_members=0)
    for index, record in enumerate(records):
        if record['status'] != 'included':
            continue
        name = safe_name(record['path'])
        reason = path_exclusion(name)
        if reason:
            reasons[index] = reason
        if PurePosixPath(name).suffix.lower() in TEXT | {'.gz'} and not reason:
            candidates[index] = name
        offset = 0
        for chunk in record['chunks']:
            key = (safe_name(chunk['archive']), safe_name(chunk['name']))
            if key in members or chunk['offset'] != offset:
                raise ValueError('Duplicate member or non-contiguous chunk offsets')
            members[key] = (index, chunk)
            offset += chunk['size']
        if offset != record['published_size']:
            raise ValueError('Published size does not match chunks')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.curate-', dir=output.parent) as temporary:
        staging = Path(temporary)
        payloads = staging / '_inspection'
        payloads.mkdir()
        seen = set()
        whole_hashes = {i: hashlib.sha256() for i, r in enumerate(records) if r['status'] == 'included'}
        whole_offsets = {i: 0 for i in whole_hashes}
        for name, archive in archive_records.items():
            archive_path = source / name
            if checksum(archive_path) != archive['sha256']:
                raise ValueError('Input archive checksum mismatch: ' + name)
            with tarfile.open(archive_path, 'r|gz') as tar:
                for member in tar:
                    key = (name, member.name)
                    if not member.isfile() or key not in members or key in seen:
                        raise ValueError('Unexpected input archive member')
                    seen.add(key)
                    index, chunk = members[key]
                    if member.size != chunk['size'] or chunk['offset'] != whole_offsets[index]:
                        raise ValueError('Input member size/order mismatch')
                    piece_hash = hashlib.sha256()
                    with tar.extractfile(member) as stream:
                        handle = (payloads / str(index)).open('ab') if index in candidates else None
                        try:
                            while data := stream.read(1024 * 1024):
                                piece_hash.update(data)
                                whole_hashes[index].update(data)
                                if handle:
                                    handle.write(data)
                        finally:
                            if handle:
                                handle.close()
                    if piece_hash.hexdigest() != chunk['sha256']:
                        raise ValueError('Input member checksum mismatch')
                    whole_offsets[index] += member.size
                    validation['verified_input_members'] += 1
        if seen != set(members):
            raise ValueError('Missing input members')
        for index, whole_hash in whole_hashes.items():
            if whole_hash.hexdigest() != records[index]['published_sha256']:
                raise ValueError('Whole published file checksum mismatch')
        for index, name in candidates.items():
            reason = inspect_file(payloads / str(index), name, validation)
            if reason:
                reasons[index] = reason
        shutil.rmtree(payloads)
        affected = {chunk['archive'] for i in reasons for chunk in records[i]['chunks']}
        retained_keys = {key for key, (index, _) in members.items() if index not in reasons}
        final_archives = []
        for name, archive in archive_records.items():
            expected = {key for key in retained_keys if key[0] == name}
            if not expected:
                continue
            destination = staging / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if name not in affected:
                shutil.copyfile(source / name, destination)
                if checksum(destination) != archive['sha256']:
                    raise ValueError('Untouched archive copy mismatch')
            else:
                with tarfile.open(source / name, 'r|gz') as original:
                    with destination.open('wb') as raw:
                        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0, compresslevel=1) as zipped:
                            with tarfile.open(fileobj=zipped, mode='w|', format=tarfile.PAX_FORMAT) as rewritten:
                                for member in original:
                                    if (name, member.name) in expected:
                                        rewritten.addfile(member, original.extractfile(member))
                verified = set()
                with tarfile.open(destination, 'r|gz') as tar:
                    for member in tar:
                        key = (name, member.name)
                        if key not in expected or key in verified:
                            raise ValueError('Unexpected rewritten member')
                        with tar.extractfile(member) as stream:
                            value = hashlib.file_digest(stream, 'sha256').hexdigest()
                        if value != members[key][1]['sha256']:
                            raise ValueError('Rewritten member checksum mismatch')
                        verified.add(key)
                if verified != expected:
                    raise ValueError('Missing rewritten member')
            validation['verified_output_members'] += len(expected)
            size = destination.stat().st_size
            if size > manifest['archive_limit_bytes']:
                raise ValueError('Curated archive exceeds size limit')
            final_archives.append({'name': name, 'sha256': checksum(destination), 'size': size, 'verified_member_count': len(expected), 'curation': 'rewritten' if name in affected else 'unchanged copy'})
        for index, reason in reasons.items():
            record = records[index]
            record['prior_publication'] = {key: record.pop(key) for key in ('published_size', 'published_sha256', 'chunks')}
            record.update(status='excluded', reason=reason)
        groups = {}
        with (staging / 'result-report-index.csv').open('w', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(['path', 'group', 'kind', 'published_size', 'published_sha256', 'archives'])
            for record in records:
                group = record['path'].split('/')[0]
                summary = groups.setdefault(group, {'included_files': 0, 'excluded_entries': 0, 'published_bytes': 0})
                included = record['status'] == 'included'
                summary['included_files' if included else 'excluded_entries'] += 1
                if included:
                    summary['published_bytes'] += record['published_size']
                    writer.writerow([record['path'], group, PurePosixPath(record['path']).suffix, record['published_size'], record['published_sha256'], ';'.join(dict.fromkeys(c['archive'] for c in record['chunks']))])
        manifest.update(archives=final_archives, groups=groups, curation={'input_manifest_sha256': original_manifest_hash, 'excluded_files': len(reasons), 'rewritten_shards': sum(a['curation'] == 'rewritten' for a in final_archives), 'validation': validation, 'scientific_validation': 'Not performed; retained published file bytes and SHA256 preserved.'})
        if checksum(manifest_path) != original_manifest_hash:
            raise ValueError('Input manifest changed during curation')
        (staging / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
        staging.rename(output)
    print(json.dumps({'output': str(output), 'excluded_files': len(reasons), 'archives': len(final_archives), 'validation': validation}, indent=2))


def main():
    parser = argparse.ArgumentParser(description='Curate generated research archives without opening scientific sources.')
    parser.add_argument('--source', type=Path, required=True, help='Existing generated release directory')
    parser.add_argument('--output', type=Path, required=True, help='Fresh curated release directory')
    args = parser.parse_args()
    curate(args.source.resolve(), args.output.absolute())


if __name__ == '__main__':
    main()
