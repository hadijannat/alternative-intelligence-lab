"""Verify publication bytes and declared scope, without executing research models."""
import hashlib
import json
from pathlib import Path, PurePosixPath

from export_followup import COORDINATES, LABS


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
    assert COORDINATES <= {r['path'] for r in included}
    recursive = base / 'recursive-compound-2026-10-15'
    inputs = json.loads((recursive / 'parent-inputs/metadata.json').read_text())['candidates']
    assert {c['id'] for c in inputs} == {'P0_A', 'P0_B', 'PT57_A', 'PT57_B'}
    for candidate_input in inputs:
        assert candidate_input['physical_admission'] is False
        assert candidate_input['checks']['computational_input_admitted'] is True
        xyz = recursive / 'parent-inputs' / (candidate_input['id'] + '.xyz')
        assert hashlib.sha256(xyz.read_bytes()).hexdigest() == candidate_input['xyz_sha256']
    qualification = recursive / 'identity/next-step/method-qualification'
    failed = json.loads((qualification / 'derivative-result.json').read_text())
    corrected = json.loads((qualification / 'grid-response-result.json').read_text())
    assert failed['pass_all'] is False and corrected['original_failure_preserved'] is True
    assert failed['threshold_Eh_per_bohr'] == corrected['threshold_Eh_per_bohr']
    preflight = json.loads((recursive / 'parent-pilot/run-v1/preflight.json').read_text())
    assert preflight['screening_estimate_bytes'] > preflight['screening_limit_bytes']
    assert preflight['physical_admission'] is False
    blocked_run = recursive / 'parent-pilot-blocked/run-v1'
    terminal = json.loads((blocked_run / 'supervisor.json').read_text())
    assert terminal['termination_reason'] == 'WALL_LIMIT' and terminal['returncode'] == -15
    assert not (blocked_run / 'SCF-result.json').exists()
    assert not (blocked_run / 'iterations.jsonl').exists()
    implementation = json.loads((recursive / 'cpcm-blocked/result.json').read_text())
    assert implementation['status'] == 'PASS_IMPLEMENTATION_EQUIVALENCE_ONLY'
    assert implementation['physical_admission'] is False
    parent_audit = json.loads((recursive / 'published-parent/analysis.json').read_text())
    assert parent_audit['physical_admission'] is False
    assert parent_audit['held_out_validation'] is False and parent_audit['SCFs_launched'] == 0
    linkage = json.loads((recursive / 'boundary/nd-linker-proposition.json').read_text())
    assert linkage['candidate_role'] == 19 and linkage['admitted_to_assembly'] is False
    assert linkage['proposed_formula_observed'] is False
    assert not (recursive / 'published-parent/item.html').exists()
    topology = recursive / 'proton-topology'
    assert (topology / 'result.json').read_bytes() == (topology / 'result-v1.json').read_bytes()
    geometry = json.loads((topology / 'result.json').read_text())
    assert geometry['status'] == 'GEOMETRY_AUDIT_ONLY'
    assert geometry['physical_admission'] is False and geometry['SCFs_launched'] == 0
    connectivity = json.loads((topology / 'guibonds-result.json').read_text())
    assert connectivity['status'] == 'AUTHORED_CONNECTIVITY_AUDIT_ONLY'
    assert connectivity['O_count_by_declared_H_count'] == {'0': 100, '1': 24, '2': 4}
    for campaign in ('rij-qualification', 'rij-qualification-v2'):
        result = json.loads((recursive / campaign / 'run-v1/result.json').read_text())
        assert result['status'] == 'FAIL_NUMERICAL_SCREEN' and result['pins_unchanged'] is True
        assert result['physical_admission'] is False and result['parent_SCF_run'] is False
        assert result['experimental_validation'] is False and len(result['cases']) == 4
    failures = []
    for path in sorted((recursive / 'rij-qualification-v2/run-v1').glob('*/result.json')):
        case = json.loads(path.read_text())
        failures.extend((case['case'], check['name']) for check in case['checks'] if not check['pass'])
    assert failures == [('heldout-Mo2O7', 'direct_Fock_residual'),
                        ('neutral-water', 'direct_Fock_residual')]
    jkfit = recursive / 'rij-jkfit-qualification'
    pending = json.loads((jkfit / 'evidence/preparation-pending.json').read_text())
    assert pending['status'] == 'PREPARED_DRIVER_PENDING_NEW_PRIMARY_INPUT'
    assert pending['SCFs_launched'] == 0 and len(pending['missing_primary_files']) == 3
    assert not (jkfit / 'run-v1').exists()
    return dict(status='PASS_FOLLOWUP_PUBLICATION_ONLY', laboratories=len(LABS),
                verified_files=len(included), published_bytes=manifest['published_bytes'], scientific_reruns=0)


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1])))
