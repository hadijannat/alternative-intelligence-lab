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
    verify_memory_followup(recursive, case_names)
    return dict(status='PASS_FOLLOWUP_PUBLICATION_ONLY', laboratories=len(LABS),
                verified_files=len(included), published_bytes=manifest['published_bytes'], scientific_reruns=0)


def verify_memory_followup(recursive, case_names):
    memory_qualification = recursive / 'cpcm-rij-memory-qualification'
    preparation = json.loads((memory_qualification / 'preparation.json').read_text())
    assert preparation['status'] == 'PREPARED_NOT_EXECUTED' and len(preparation['pins']) == 57
    assert len(preparation['cases']) == 5 and set(preparation['cases']) == case_names
    assert preparation['densities_per_case'] == 4 and preparation['SCFs_launched'] == 0
    run = memory_qualification / 'run-v1'
    assert json.loads((run / 'pins.json').read_text()) == preparation['pins']
    completed = json.loads((run / 'result.json').read_text())
    assert completed['status'] == 'PASS_RETROSPECTIVE_IMPLEMENTATION_EQUIVALENCE'
    assert completed['phase1_pass'] is True and completed['phase2_skipped'] is False
    assert completed['pins_unchanged'] is True and completed['maximum_new_SCFs'] == 1
    assert completed['parent_run'] is False and completed['physical_admission'] is False
    gate = json.loads((run / 'phase1-gate.json').read_text())
    assert gate['pass'] is True and gate['SCFs_launched'] == 0
    receipts = json.loads((run / 'operator-receipts.json').read_text())
    assert len(receipts) == 5 and {r['case'] for r in receipts} == case_names
    children = [('operators-' + r['case'], r['case'], 'operators', r) for r in receipts]
    children.append(('scf-new-external', 'new-external', 'scf', completed['phase2']))
    checks = []
    for folder, name, phase, receipt in children:
        supervisor = json.loads((run / folder / 'supervisor.json').read_text())
        assert {k: v for k, v in receipt.items() if k != 'case'} == supervisor
        assert supervisor['returncode'] == 0 and supervisor['termination_reason'] is None
        assert supervisor['monitor_error'] is None
        result = json.loads((run / folder / 'result.json').read_text())
        assert result['case'] == name and result['phase'] == phase
        assert result['status'] == ('PASS_OPERATORS' if phase == 'operators' else 'PASS_SCF')
        assert result['SCFs_launched'] == (0 if phase == 'operators' else 1)
        assert result['physical_admission'] is False and result['fresh_holdout'] is False
        assert result['checks'] and all(check['pass'] is True for check in result['checks'])
        checks.extend(result['checks'])
        if phase == 'scf':
            assert result['SCF']['converged'] is True and result['SCF']['cycles'] == 32
    assert len(checks) == 223
    reservoir = json.loads((recursive / 'energy/silicotungstate-20/assessment.json').read_text())
    assert reservoir['candidate_role'] == 20 and reservoir['status'] == 'UNRESOLVED_JOINT_FUNCTION'
    assert reservoir['standalone_component_evidence'] is True
    for claim in ('admitted_to_assembly', 'target_existence_verified',
                  'common_medium_joint_identity_verified', 'useful_target_energy_transfer_verified',
                  'functional_regeneration_verified'):
        assert reservoir[claim] is False
    assert reservoir['new_simulations'] == 0 and reservoir['new_physical_experiments'] == 0
    parent = recursive / 'parent-pilot-memory'
    preparation = json.loads((parent / 'preparation.json').read_text())
    assert preparation['status'] == 'PREPARED_PENDING_TERMINAL_QUALIFICATION_AND_INDEPENDENT_ROOT_REVIEW'
    assert len(preparation['pins']) == 66 and preparation['SCFs_launched'] == 0
    assert preparation['parent_molecule_built'] is False and preparation['parent_arrays_allocated'] is False
    run = parent / 'run-v1'
    terminal = json.loads((run / 'supervisor.json').read_text())
    assert json.loads((run / 'launch-result.json').read_text()) == terminal
    assert terminal['termination_reason'] == 'WALL_LIMIT' and terminal['returncode'] == -15
    assert terminal['monitor_error'] is None and terminal['wall_cap_seconds'] == 900
    assert terminal['wall_seconds'] >= terminal['wall_cap_seconds']
    assert terminal['rss_guard_bytes'] == 10 * 2**30
    assert terminal['sampled_max_rss_bytes'] < terminal['rss_guard_bytes']
    assert terminal['hard_OS_memory_limit'] is False
    stages = [json.loads(line)['stage'] for line in (run / 'stages.jsonl').read_text().splitlines()]
    assert stages[-1] == 'RI_metric_build_start' and 'SCF_start' not in stages
    for name in ('SCF-result.json', 'iterations.jsonl', 'storage.json'):
        assert not (run / name).exists()
    wv = recursive / 'wv-method-qualification'
    preparation = json.loads((wv / 'preparation.json').read_text())
    assert preparation['status'] == 'PREPARED_NOT_EXECUTED' and len(preparation['pins']) == 30
    assert len(preparation['cases']) == 2 and {c['case'] for c in preparation['cases']} == {'WO4', 'VO4'}
    assert preparation['SCFs_launched'] == 0 and preparation['operators_evaluated'] == 0
    run = wv / 'run-v1'
    assert json.loads((run / 'pins.json').read_text()) == preparation['pins']
    completed = json.loads((run / 'result.json').read_text())
    assert completed['status'] == 'PASS_NUMERICAL_SCREEN_ONLY'
    assert completed['pins_unchanged'] is True and completed['physical_admission'] is False
    assert completed['maximum_SCFs'] == completed['actual_SCFs_launched'] == 4
    assert completed['case_SCFs_launched'] == {'WO4': 2, 'VO4': 2}
    receipts = json.loads((run / 'receipts.json').read_text())
    assert len(receipts) == 2 and {r['case'] for r in receipts} == {'WO4', 'VO4'}
    checks, scfs = [], []
    for receipt in receipts:
        child = run / receipt['case']
        supervisor = json.loads((child / 'supervisor.json').read_text())
        assert {k: v for k, v in receipt.items() if k != 'case'} == supervisor
        assert supervisor['returncode'] == 0 and supervisor['termination_reason'] is None
        assert supervisor['monitor_error'] is None
        result = json.loads((child / 'result.json').read_text())
        assert result['case'] == receipt['case'] and result['status'] == 'PASS_NUMERICAL_SCREEN_ONLY'
        assert result['physical_admission'] is False and result['experimental_validation'] is False
        assert result['fresh_fixed_geometry_numerical_challenge'] is True
        assert result['SCFs_launched'] == 2 and len(result['checks']) == 20
        checks.extend(result['checks'])
        scfs.extend((result['direct_SCF'], result['RI_SCF']))
    assert len(checks) == 40 and all(check['pass'] is True for check in checks)
    assert len(scfs) == 4 and all(scf['converged'] is True for scf in scfs)
    diagnostic = (parent / 'THREAD_DIAGNOSTIC.md').read_text()
    probe = json.loads(diagnostic.split('```json\n', 1)[1].split('```', 1)[0])
    assert probe == {'before': 1, 'request_4_return': 0, 'after': 1,
                     'scientific_operators': 0, 'SCFs': 0}
    assert 'OpenMP is not available.' in diagnostic
    assert 'Full parent convergence, solution identity and target integration remain unverified.' in diagnostic
    renewal = recursive / 'renewal/fe-feed-21'
    assessment = json.loads((renewal / 'assessment.json').read_text())
    assert assessment['candidate_role'] == 21
    assert assessment['status'] == 'COMPONENT_SUPPORTED_TARGET_RENEWAL_UNRESOLVED'
    assert assessment['source_data_reanalyzed'] is True
    for claim in ('admitted_to_assembly', 'experimental_holdout', 'target_existence_verified',
                  'target_renewal_verified', 'functional_inheritance_verified',
                  'matched_Co_assisted_EQCM_comparison_available', 'fig2d_feed_unit_conflict_resolved'):
        assert assessment[claim] is False
    assert assessment['new_physical_experiments'] == assessment['new_fitted_models'] == 0
    for unknown in ('solid_fixed_molecular_formula', 'founder_replacement_fraction',
                    'fig2e_current_density_mA_cm2'):
        assert assessment[unknown] is None
    analysis = json.loads((renewal / 'analysis.json').read_text())
    inventory = json.loads((renewal / 'source-data-inventory.json').read_text())
    assert analysis['status'] == 'SOURCE_DATA_RECOVERED_MATCHED_EQCM_COMPARATOR_UNAVAILABLE'
    assert analysis['target_renewal_demonstrated'] is False
    assert analysis['source'] == inventory['source']
    assert analysis['source']['doi'] == '10.1038/s41467-021-26281-0'
    assert len(inventory['workbooks']) == 5
    sheets = {sheet['name']: sheet for book in inventory['workbooks'] for sheet in book['sheets']}
    conflict = analysis['source_label_conflict']
    assert conflict['workbook_label_verbatim'] == 'with 50 mM Fe(II)'
    assert sheets['Figure 2d']['text_cells_in_first_three_rows']['C1'] == conflict['workbook_label_verbatim']
    assert conflict['article_nominal_feed_uM'] == 50
    assert 'Unresolved mM versus microM discrepancy retained' in conflict['disposition']
    comparator = analysis['matched_Co_assisted_vs_unassisted_EQCM']
    assert comparator['common_potential_comparisons'] is None and comparator['Co_assisted_rate_data'] is None
    assert analysis['fig2e']['current_density_mA_cm-2'] is None
    assert analysis['fig2e']['deposition_rate'] is None
    assert len(analysis['fig1c']['observations']) == 12
    for observation in analysis['fig1c']['observations']:
        assert observation['mean'] is None
        assert observation['uncertainty'] is None and observation['replicate_count'] is None
    responses = analysis['fig2e']['descriptive_potential_response']['responses']
    assert len(responses) == 3 and {r['ion'] for r in responses} == {'Ni(II)', 'Co(II)', 'Fe(II)'}
    for response in responses:
        assert response['uncertainty'] is None and response['replicate_count'] is None
    assert 'Retrospective descriptive source audit; no physical experiment or held-out test.' in analysis['limitations']


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1])))
