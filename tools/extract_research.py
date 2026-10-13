#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tarfile
import tempfile

sys.set_int_max_str_digits(0)


def safe_path(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Invalid publication path')
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or path.as_posix() != name or ':' in path.parts[0]:
        raise ValueError('Unsafe publication path')
    return path


def open_regular(path):
    import stat
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    stream = os.fdopen(descriptor, 'rb')
    if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
        stream.close()
        raise ValueError('Expected regular publication file')
    return stream


def extract(archives, output, groups=()):
    if archives.is_symlink() or output.exists() or output.is_symlink():
        raise ValueError('Archive root must not be a symlink; output must be new')
    with open_regular(archives / 'manifest.json') as handle:
        manifest = json.load(handle)
    available = {record['path'].split('/')[0] for record in manifest['files'] if record['status'] == 'included'}
    if set(groups) - available:
        raise ValueError('Requested group is absent from included manifest files')
    selected = {}
    members = {}
    for record in manifest['files']:
        if record['status'] != 'included' or (groups and record['path'].split('/')[0] not in groups):
            continue
        name = safe_path(record['path']).as_posix()
        if name in selected:
            raise ValueError('Duplicate selected publication path')
        selected[name] = record
        offset = 0
        for chunk in sorted(record['chunks'], key=lambda item: item['offset']):
            archive_name = safe_path(chunk['archive'])
            member_name = safe_path(chunk['name']).as_posix()
            if len(archive_name.parts) != 1 or type(chunk['size']) is not int or chunk['size'] < 0 or type(chunk['offset']) is not int or chunk['offset'] != offset:
                raise ValueError('Invalid archive name or non-contiguous chunk metadata')
            key = (archive_name.as_posix(), member_name)
            if key in members:
                raise ValueError('Duplicate selected archive member')
            members[key] = (name, chunk)
            offset += chunk['size']
        if not record['chunks'] or offset != record['published_size']:
            raise ValueError('Published file size does not match chunk metadata')
    if not selected:
        raise ValueError('No included publication files selected')
    needed = {key[0] for key in members}
    archive_records = {}
    for archive in manifest['archives']:
        name = safe_path(archive['name']).as_posix()
        if name in archive_records:
            raise ValueError('Duplicate archive metadata')
        archive_records[name] = archive
    if needed - archive_records.keys():
        raise ValueError('Selected chunks reference an unknown archive')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.extract-research-', dir=output.parent) as temporary:
        staging = Path(temporary)
        seen = set()
        for archive_name in sorted(needed):
            with open_regular(archives / archive_name) as raw:
                if hashlib.file_digest(raw, 'sha256').hexdigest() != archive_records[archive_name]['sha256']:
                    raise ValueError('Archive SHA256 mismatch: ' + archive_name)
                raw.seek(0)
                with tarfile.open(fileobj=raw, mode='r|gz') as tar:
                    for member in tar:
                        safe_path(member.name)
                        if not member.isfile():
                            raise ValueError('Archive contains a symlink or nonregular member')
                        key = (archive_name, member.name)
                        if key not in members:
                            continue
                        if key in seen:
                            raise ValueError('Duplicate selected member in archive')
                        name, chunk = members[key]
                        if member.size != chunk['size']:
                            raise ValueError('Archive member size mismatch')
                        destination = staging / name
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        checksum = hashlib.sha256()
                        with destination.open('r+b' if destination.exists() else 'wb') as target:
                            target.seek(chunk['offset'])
                            with tar.extractfile(member) as source:
                                while data := source.read(1024 * 1024):
                                    checksum.update(data)
                                    target.write(data)
                        if checksum.hexdigest() != chunk['sha256']:
                            raise ValueError('Chunk SHA256 mismatch: ' + name)
                        seen.add(key)
        if seen != set(members):
            raise ValueError('Missing selected archive members')
        for name, record in selected.items():
            path = staging / name
            if path.stat().st_size != record['published_size']:
                raise ValueError('Reconstructed file size mismatch: ' + name)
            with path.open('rb') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != record['published_sha256']:
                    raise ValueError('Reconstructed file SHA256 mismatch: ' + name)
        staging.rename(output)
    print(json.dumps({'output': str(output), 'verified_files': len(selected), 'verified_chunks': len(seen), 'verified_archives': len(needed), 'scientific_execution': False}, indent=2))


def main():
    parser = argparse.ArgumentParser(description='Verify and reconstruct downloaded research publication files.')
    parser.add_argument('--archives', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--group', action='append', default=[])
    args = parser.parse_args()
    extract(args.archives.absolute(), args.output.absolute(), args.group)


if __name__ == '__main__':
    main()
