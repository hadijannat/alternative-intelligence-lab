"""Verify publication bytes and declared scope, without executing research models."""
import hashlib
import json
from pathlib import Path, PurePosixPath

from export_followup import LABS


def verify(root):
    base = root / 'research' / '2026-10-15'
    manifest = json.loads((base / 'manifest.json').read_text())
    assert manifest['scientific_validation'] is False
    assert manifest['labs'] == list(LABS)
    included = [r for r in manifest['files'] if r['status'] == 'included']
    assert len(included) == manifest['included_files']
    assert len({r['path'] for r in included}) == len(included)
    assert len({r['published_sha256'] for r in included}) == manifest['unique_published_blobs']
    assert sum(r['published_size'] for r in included) == manifest['published_bytes']
    for record in included:
        name = PurePosixPath(record['path'])
        assert not name.is_absolute() and '..' not in name.parts and name.parts[0] in LABS
        path = base / name
        assert not path.is_symlink() and path.stat().st_size == record['published_size'], name
        with path.open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == record['published_sha256'], name
    candidate = json.loads((base / 'noncarbon-discovery-2026-10-15/candidate.json').read_text())
    assert candidate['status'] == 'UNVERIFIED_COMPOSITION_HYPOTHESIS'
    assert candidate['life_or_intelligence'] == 'NOT_DEMONSTRATED'
    assert candidate['structural_geometry'] is None
    agents = json.loads((base / 'noncarbon-discovery-2026-10-15/verification/agents.json').read_text())
    assert agents['actual_participating_subagents'] == 24 and not agents['thousand_agents_executed']
    return dict(status='PASS_FOLLOWUP_PUBLICATION_ONLY', laboratories=len(LABS),
                verified_files=len(included), published_bytes=manifest['published_bytes'], scientific_reruns=0)


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1])))
