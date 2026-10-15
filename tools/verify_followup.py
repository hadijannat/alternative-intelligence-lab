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
    completed = json.loads((jkfit / 'run-v1/result.json').read_text())
    assert completed['status'] == 'PASS_NUMERICAL_SCREEN_ONLY'
    assert completed['pins_unchanged'] is True
    assert completed['physical_admission'] is False and completed['parent_SCF_run'] is False
    assert completed['experimental_validation'] is False
    case_names = {'anion-water', 'neutral-water', 'anion-eps1', 'heldout-Mo2O7', 'new-external'}
    assert len(completed['cases']) == 5 and {c['case'] for c in completed['cases']} == case_names
    checks, scfs = [], []
    for receipt in completed['cases']:
        assert receipt['returncode'] == 0 and receipt['termination_reason'] is None
        case = json.loads((jkfit / 'run-v1' / receipt['case'] / 'result.json').read_text())
        assert case['case'] == receipt['case'] and case['status'] == 'PASS_NUMERICAL_SCREEN_ONLY'
        assert case['physical_admission'] is False and case['experimental_validation'] is False
        checks.extend(case['checks'])
        scfs.append(case['RI_SCF'])
        if case['case'] == 'new-external':
            assert case['heldout_numerical_case'] is True
            scfs.append(case['direct_SCF'])
            provenance = case['new_external_source']
            assert provenance['formula'] == 'H2Mo2O7' and provenance['charge'] == 0
            assert provenance['acquired_before_campaign'] is True
            assert provenance['validation_scope'] == (
                'External fixed computational geometry for numerical qualification; '
                'no experimental species, target geometry or independent stationary-point proof')
            assert provenance['publication_doi'] == '10.1021/acs.jpca.1c03292'
            assert provenance['collection_doi'] == '10.19061/iochem-bd-1-201'
        else:
            assert case['heldout_numerical_case'] is False
            assert 'direct_SCF' not in case and 'reused_direct_reference' in case
    assert len(checks) == 101 and all(check['pass'] is True for check in checks)
    assert len(scfs) == 6 and all(scf['converged'] is True for scf in scfs)
    for name in ('new-case.json', 'new.xyz', 'new.in', 'new-output.cml'):
        assert not (jkfit / 'raw' / name).exists()
    memory = recursive / 'cpcm-rij-memory'
    observations = json.loads((memory / 'evidence/observations.json').read_text())
    assert observations['success'] is True and observations['tests_run'] == 8
    assert observations['SCFs_launched'] == 0 and observations['parent_arrays_allocated'] is False
    scenarios = {o['scenario']: o for o in observations['observations']}
    assert len(scenarios) == 6
    assert scenarios['injected destructive native factor failure']['regular_fallback_calls'] == 0
    assert scenarios['injected destructive native factor failure']['optimizer_published'] is False
    assert scenarios['He six-surface-point factor-only PCM']['factor_shape'] == [6, 6]
    assert scenarios['He sto3g native two-pass JKFIT operator']['reuse'] is True
    allocation = json.loads((memory / 'allocation.json').read_text())
    assert allocation['status'] == 'ARITHMETIC_ONLY_NO_PARENT_ALLOCATION'
    assert allocation['passes_arithmetic_screen'] is True
    assert allocation['certified_peak_RSS'] is False and allocation['parent_array_allocated'] is False
    assert sum(allocation['terms_bytes'].values()) == allocation['sum_bytes']
    assert allocation['sum_bytes'] < allocation['screen_limit_bytes']
    memory_qualification = recursive / 'cpcm-rij-memory-qualification'
    preparation = json.loads((memory_qualification / 'preparation.json').read_text())
    assert preparation['status'] == 'PREPARED_NOT_EXECUTED' and len(preparation['pins']) == 57
    assert len(preparation['cases']) == 5 and set(preparation['cases']) == case_names
    assert preparation['densities_per_case'] == 4 and preparation['SCFs_launched'] == 0
    assert not (memory_qualification / 'run-v1').exists()
    return dict(status='PASS_FOLLOWUP_PUBLICATION_ONLY', laboratories=len(LABS),
                verified_files=len(included), published_bytes=manifest['published_bytes'], scientific_reruns=0)


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1])))
