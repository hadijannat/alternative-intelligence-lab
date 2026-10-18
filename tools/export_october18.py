#!/usr/bin/env python3
"""Curate the October 18 authored research snapshot without running models."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import stat

import build_archive as archive
import curate_archive as curator
from export_followup import strip_signed_urls

LAB = 'documented-scaffold-2026-10-18'
REVIEWS = tuple(name + '.md' for name in (
    'documented-scaffold-code-review', 'photo-beta-review', 'functional-carrier-review',
    'cue-activation-review', 'han-isotope-review', 'regeneration-controls-review',
    'state-template-growth-review', 'fe-site-observation-review',
    'dissolution-observation-review', 'contact-chirality-review',
    'remote-fe-transport-review', 'current-branch-impasse',
    'full-goal-critical-path-2026-10-18', 'spatial-fe-function-review',
    'october18-publication-review'))
FAILURES = {
    'founder-repair-search/execution_failures.txt',
    'regeneration-controls/execution_failures.txt',
    'regeneration-controls/results/execution.txt',
    'state-template-growth/execution_failures.txt',
    'fe-site-observation/extraction_failures.txt',
    'remote-fe-transport/results/execution.log',
    'spatial-fe-function/results/test-output.txt',
}
SOURCE_METADATA = {
    'receipt.json', 'receipts.json', 'supplement-receipts.json', 'verification.json',
    'acquisition.json', 'companion-acquisition.json', 'acquisition-checks.json',
    'browser-main-receipt.json', 'browser-si-receipt.json', 'attachment-receipt.json',
    'download_receipt.json', 'pdf-receipt.json', 'data-receipt.json', 'si-receipt.json',
    'asset-validation.json', 'checksums.json', 'figure3-inventory.json',
    'fig3g-cell-layout.json', 'fig6-axis-calibration.json', 'si-math-structure.json',
    'hal-metadata.json', 'hal-companion-metadata.json', 'workbook-structure.json',
}


def exclusion(rel, directory=False):
    parts = tuple(part.lower() for part in rel.parts)
    if any(p in {'consultation', '__pycache__', '.git', '.codex', '.pytest_cache'} for p in parts):
        return 'private consultation, runtime cache, or orchestration subtree'
    if archive.PROTECTED.lower() in rel.name.lower():
        return 'protected payload; unopened'
    if archive.SECRET_NAME.search(rel.name) or rel.name.startswith('.env'):
        return 'potential credential material; unopened'
    if directory:
        return None
    if rel.as_posix() in FAILURES:
        return None
    if rel.name in {'native_cells.json', 'fig3-text-cells.json'}:
        return 'one-to-one native workbook cells; derived analyses and provenance retained'
    if 'sources' in parts or 'raw' in parts:
        if rel.suffix == '.js':
            return 'third-party publisher JavaScript runtime; acquisition receipt retains URL and hash'
        if rel.suffix in {'.md', '.py'} or rel.name in SOURCE_METADATA:
            return None
        return 'third-party source payload or registry response; authored receipts retain provenance'
    if rel.suffix == '.png' and 'results' not in parts:
        return 'native figure crop or annotated source image; numeric extraction retained'
    if rel.suffix not in {'.md', '.py', '.json', '.csv', '.png', '.npz'}:
        return 'unapproved payload format; scientific failure logs use an explicit allowlist'
    return None


def export(source, output):
    if output.exists():
        raise ValueError('Fresh destination required')
    if not (source / LAB).is_dir():
        raise ValueError('Missing source laboratory')
    records = []

    def publish(path, destination, reason=None):
        rel = path.relative_to(source)
        record = dict(path=destination, source_path=rel.as_posix(), status='excluded', reason=reason)
        records.append(record)
        st = path.lstat()
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
            record['reason'] = 'linked or nonregular entry; target not read'
            return
        record['source_size'] = st.st_size
        if reason:
            return
        if st.st_size >= 100 * 1024 * 1024:
            raise ValueError('GitHub file limit: ' + str(rel))
        # prepare binds its read to the original inode/size/timestamps and sanitizes text.
        prepared = dict(path=rel.as_posix(), _fingerprint=archive.fingerprint(st))
        stream = archive.prepare(source, prepared)
        record.update({k: v for k, v in prepared.items() if k not in {'path', '_fingerprint'}})
        if stream is None:
            return
        with stream:
            data = stream.read()
        if path.suffix == '.log':
            text, changes = archive.sanitize(data.decode('utf-8'), source)
            record['transformations'].extend(changes)
            data = text.encode()
        if path.suffix in archive.TEXT or path.suffix == '.log':
            text, count = strip_signed_urls(data.decode('utf-8'))
            if count:
                record['transformations'].append(dict(transformation='signed URL query removed; stable URL retained', count=count))
            if path.suffix == '.json' and curator.tool_envelope(json.loads(text), str(rel)):
                record.update(status='excluded', reason='structured tool execution envelope')
                return
            if rel.as_posix() == LAB + '/CONTINUATION_LEDGER.md':
                old = '../recursive-compound-2026-10-15/PROTOCOL.md'
                count = text.count(old)
                text = text.replace(old, '../GOAL_CONTRACT.md')
                if count:
                    record['transformations'].append(dict(transformation='portable original goal-contract link', count=count))
            if '\r\n' in text:
                record['transformations'].append(dict(transformation='LF line endings', count=text.count('\r\n')))
                text = text.replace('\r\n', '\n')
            if archive.HOST.search(text) or archive.KEY.search(text):
                raise ValueError('Unredacted text: ' + str(rel))
            data = text.encode('utf-8')
        if archive.fingerprint(path.lstat()) != prepared['_fingerprint']:
            raise ValueError('Source changed during export: ' + str(rel))
        if len(data) >= 100 * 1024 * 1024:
            raise ValueError('GitHub file limit: ' + str(rel))
        target = output / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        record.update(status='included', reason='authored research or provenance record',
                      published_size=len(data), published_sha256=hashlib.sha256(data).hexdigest())

    def walk(folder):
        for path in sorted(folder.iterdir()):
            rel = path.relative_to(source / LAB)
            if path.is_symlink():
                records.append(dict(path=LAB + '/' + str(rel), source_path=LAB + '/' + str(rel), status='excluded', reason='symbolic link; target not read'))
            elif path.is_dir():
                reason = exclusion(rel, True)
                if reason:
                    records.append(dict(path=LAB + '/' + str(rel), source_path=LAB + '/' + str(rel), status='excluded', reason=reason, scope='subtree; contents not enumerated'))
                else:
                    walk(path)
            else:
                publish(path, LAB + '/' + str(rel), exclusion(rel))

    walk(source / LAB)
    publish(source / 'recursive-compound-2026-10-15/PROTOCOL.md', 'GOAL_CONTRACT.md')
    for name in REVIEWS:
        path = source / '.omo/evidence' / name
        if path.exists():
            publish(path, 'reviews/' + name)
        else:
            records.append(dict(path='reviews/' + name, source_path='.omo/evidence/' + name,
                                status='missing', reason='requested review absent; no review invented'))
    readme = '''# October 18 research snapshot

This is a curated publication of saved research artifacts. Publication integrity is not scientific validation. No scientific model is rerun by the exporter or verifier. The full life/intelligence goal remains unachieved; no integrated complement is verified.

Start with [the continuation ledger](documented-scaffold-2026-10-18/CONTINUATION_LEDGER.md), [the next-session prompt](documented-scaffold-2026-10-18/NEXT_SESSION_PROMPT.md), and [the original goal contract](GOAL_CONTRACT.md). Reports, protocols, authored model code, derived results, failed checks, numerical plots, and authored reviews are retained.

The manifest maps each original project-relative path and SHA256 to its published path and SHA256, with sanitization and exclusions recorded. Frozen hashes embedded in scientific outputs identify original local bytes; sanitized publication hashes can differ. Do not rewrite frozen scientific hashes to claim byte-identical reproduction.

Third-party full texts, native figures, movies, workbooks, one-to-one cell dumps, and 481 raw regeneration files are excluded. Their source URLs, acquisition hashes and license observations remain in authored receipts/reports and the regeneration file manifest. Reacquire required raw inputs through those URLs and verify their original hashes before rerunning extraction or analysis. This checkout alone is not a complete raw-data reproduction environment. Source documents retain their original licenses; this repository does not relicense them. Private Claude consultation UI/transcripts and caches are excluded; authored assessments remain.

Path mapping: original `documented-scaffold-2026-10-18/` is the same-named directory here; original `.omo/evidence/<review>.md` is `reviews/<review>.md`; original `recursive-compound-2026-10-15/PROTOCOL.md` is `GOAL_CONTRACT.md`. Other original project-relative dependencies can refer to older published snapshots or unpublished local inputs. The spatial Fe iteration is an analytical/synthetic identifiability test with zero qualified empirical training or held-out observations. Its positive algebra checks do not validate active chemical repair.

The publication review included here is the precommit review history available at export. Its earlier snapshot counts and pending delta-review statements describe that review stage. It does not certify its own subsequently exported bytes or a remote commit; final publication verification and remote commit checks are separate evidence.

From the repository root, run `python3 tools/verify_october18.py` and `python3 -m unittest discover -s tests -p test_export_october18.py` to check this publication boundary. These checks do not validate chemical repair, inheritance, life, or intelligence.
'''
    (output / 'README.md').write_text(readme)
    included = [r for r in records if r['status'] == 'included']
    manifest = dict(date='2026-10-18', scientific_validation=False, source_root='PROJECT_ROOT',
                    included_files=len(included), published_bytes=sum(r['published_size'] for r in included),
                    excluded_entries=sum(r['status'] == 'excluded' for r in records),
                    missing_reviews=[r['path'] for r in records if r['status'] == 'missing'],
                    exclusions_by_reason=dict(Counter(r['reason'] for r in records if r['status'] == 'excluded')),
                    generated_files={'README.md': hashlib.sha256(readme.encode()).hexdigest()},
                    files=sorted(records, key=lambda r: r['path']))
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return {k: v for k, v in manifest.items() if k not in {'files', 'generated_files'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.source.resolve(), args.output.resolve()), indent=2))
