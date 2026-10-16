"""Verify publication bytes and declared scope, without executing research models."""
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath

from export_followup import COORDINATES, LABS, exclusion


def verify(root):
    base = root / 'research' / '2026-10-15'
    manifest = json.loads((base / 'manifest.json').read_text())
    assert manifest['scientific_validation'] is False
    assert manifest['labs'] == list(LABS)
    included = [r for r in manifest['files'] if r['status'] == 'included']
    matrix_path = 'recursive-compound-2026-10-15/parent-metric-solve-diagnostic-v2/run-v1/original_metric.npy'
    matrix_record, = [r for r in manifest['files'] if r['path'] == matrix_path]
    assert matrix_record['status'] == 'excluded' and matrix_record['source_size'] == 3077044480
    assert matrix_record['reason'] == exclusion(Path(matrix_path))
    verify_parent_pilot_source_bindings(included)
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
    verify_stage_artifact_bindings(recursive, included)
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
    verify_openmp_renewal(recursive, case_names)
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


def verify_openmp_renewal(recursive, case_names):
    renewal = json.loads((recursive / 'renewal/copI-source/assessment.json').read_text())
    assert renewal['candidate_role'] == 22
    assert renewal['status'] == 'COMPONENT_RECYCLING_SUPPORTED_TARGET_RENEWAL_UNRESOLVED'
    for key in ('admitted_to_assembly', 'target_identity_verified', 'target_renewal_verified',
                'functional_inheritance_verified', 'experimental_holdout',
                'newly_competent_activity_positive_lower_bound_identified'):
        assert renewal[key] is False
    for key in ('fixed_molecular_formula', 'retained_founder_organization_fraction',
                'newly_competent_activity_upper_bound'):
        assert renewal[key] is None
    assert renewal['newly_competent_activity_trivial_lower_bound'] == 0
    assert renewal['new_physical_experiments'] == renewal['new_fitted_models'] == 0
    blue = json.loads((recursive / 'renewal/mo-blue-route/analysis.json').read_text())
    assert blue['status'] == 'SOURCE_METHOD_CONSTRAINTS_ONLY'
    for key in ('target_renewal_verified', 'functional_inheritance_verified',
                'new_candidate_role', 'experimental_holdout'):
        assert blue[key] is False
    assert blue['new_fitted_models'] == blue['new_physical_experiments'] == 0
    assert blue['nominal_control_recipe']['recipe_consistency_resolved'] is False
    raman = blue['raman_normalization']
    assert raman['each_species_own_maximum_percent'] == 100
    assert raman['cross_species_response_calibration_supplied'] is False
    assert raman['absolute_species_mass_balance_identified'] is False
    assert raman['sampling_side'].startswith('UNRESOLVED:')
    esi = blue['ESI_sampling']
    assert esi['sample_to_acetonitrile_volume_ratio'] == [1, 39]
    assert esi['total_scan_completion_delay_minutes'] is None
    assert esi['unperturbed_operando_solution_identity_established'] is False
    run = recursive / 'parent-openmp-qualification/run-v1'
    result = json.loads((run / 'result.json').read_text())
    assert result['status'] == 'FAIL' and result['phase1_pass'] is False
    assert result['phase2'] is None and result['phase2_skipped'] is True
    assert result['pins_unchanged'] is True
    for key in ('parent_run', 'fresh_holdout', 'physical_admission'):
        assert result[key] is False
    assert json.loads((run / 'phase1-gate.json').read_text()) == {'pass': False, 'SCFs_launched': 0}
    receipts = json.loads((run / 'operator-receipts.json').read_text())
    expected = {(threads, name) for threads in (1, 4) for name in case_names | {'WO4', 'VO4'}}
    assert len(receipts) == 14 and {(r['threads'], r['case']) for r in receipts} == expected
    checks = []
    for receipt in receipts:
        child = run / ('threads-' + str(receipt['threads'])) / 'run-v1' / ('operators-' + receipt['case'])
        supervisor = json.loads((child / 'supervisor.json').read_text())
        assert {k: v for k, v in receipt.items() if k not in {'threads', 'case'}} == supervisor
        failed = receipt['case'] in {'WO4', 'VO4'}
        assert supervisor['returncode'] == (1 if failed else 0)
        assert supervisor['termination_reason'] is None and supervisor['monitor_error'] is None
        result = json.loads((child / 'result.json').read_text())
        assert result['case'] == receipt['case'] and result['threads'] == receipt['threads']
        assert result['phase'] == 'operators' and result['SCFs_launched'] == 0
        assert result['runtime_guard_pass'] is (not failed)
        assert result['status'] == ('ERROR' if failed else 'PASS_OPERATORS')
        assert result['physical_admission'] is False and result['fresh_holdout'] is False
        checks.extend(result['checks'])
    assert len(checks) == 520 and all(check['pass'] is True for check in checks)
    assert not list(run.rglob('scf-*')) and not list(run.rglob('SCF-result.json'))
    qualified = recursive / 'parent-openmp-qualification-v2'
    for name in ('run.py', 'test_run.py', 'PROTOCOL.md'):
        assert (qualified / name).is_file() and (qualified / name).stat().st_size > 0
    run = qualified / 'run-v1'
    result = json.loads((run / 'result.json').read_text())
    assert result['status'] == 'PASS_RETROSPECTIVE_RUNTIME_EQUIVALENCE'
    assert result['phase1_pass'] is True and result['phase2_skipped'] is False
    assert result['pins_unchanged'] is True and result['maximum_SCFs'] == 1
    for key in ('parent_run', 'fresh_holdout', 'physical_admission'):
        assert result[key] is False
    assert json.loads((run / 'phase1-gate.json').read_text()) == {'pass': True, 'SCFs_launched': 0}
    assert json.loads((run / 'scf-claimed.json').read_text()) == {
        'maximum_SCFs': 1, 'case': 'new-external', 'threads': 4}
    receipts = json.loads((run / 'operator-receipts.json').read_text())
    assert len(receipts) == 14 and {(r['threads'], r['case']) for r in receipts} == expected
    checks = []
    for index, receipt in enumerate(receipts + [dict(result['phase2'], threads=4, case='new-external')]):
        scf = index == 14
        phase = 'scf' if scf else 'operators'
        child = run / ('threads-' + str(receipt['threads'])) / 'run-v1' / (phase + '-' + receipt['case'])
        supervisor = json.loads((child / 'supervisor.json').read_text())
        assert {k: v for k, v in receipt.items() if k not in {'threads', 'case'}} == supervisor
        assert supervisor['returncode'] == 0
        assert supervisor['termination_reason'] is None and supervisor['monitor_error'] is None
        item = json.loads((child / 'result.json').read_text())
        assert item['case'] == receipt['case'] and item['threads'] == receipt['threads']
        assert item['phase'] == phase and item['SCFs_launched'] == int(scf)
        assert item['runtime_guard_pass'] is True
        assert item['status'] == ('PASS_SCF' if scf else 'PASS_OPERATORS')
        assert item['physical_admission'] is False and item['fresh_holdout'] is False
        expected_checks = 46 if receipt['case'] == 'anion-eps1' else (42 if receipt['case'] in case_names else 23)
        assert len(item['checks']) == (9 if scf else expected_checks)
        if scf:
            assert item['SCF']['converged'] is True
        checks.extend(item['checks'])
    assert len(checks) == 529 and all(check['pass'] is True for check in checks)
    assert len([path for path in run.rglob('scf-*') if path.is_dir()]) == 1
    for campaign in ('parent-openmp-first-j', 'parent-openmp-first-j-v2'):
        base = recursive / campaign
        preparation = json.loads((base / 'preparation.json').read_text())
        assert preparation['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
        assert preparation['parent_molecule_built'] is False
        assert preparation['J_calls'] == preparation['SCFs_launched'] == 0
        assert preparation['density']['shape'] == [3068, 3068]
        assert preparation['density']['cycle'] == 0
        run = base / 'run-v1'
        launch = json.loads((run / 'launch-result.json').read_text())
        assert launch['receipt'] == json.loads((run / 'supervisor.json').read_text())
        assert launch['gate_unchanged'] is True and launch['gate_error'] is None
        assert launch['maximum_children'] == launch['maximum_J_calls'] == 1
        assert launch['maximum_SCFs'] == 0
        assert launch['physical_admission'] is False and launch['parent_SCF_readiness'] is False
        assert launch['receipt']['termination_reason'] is None and launch['receipt']['monitor_error'] is None
        if campaign == 'parent-openmp-first-j':
            assert launch['status'] == 'INCOMPLETE_OR_FAILED_FIRST_J'
            assert launch['receipt']['returncode'] == 1 and launch['worker_result'] == {}
            assert launch['J_sha256_observed'] is None
            failure = json.loads((run / 'failure.json').read_text())
            assert 'ValueError: PCM allocated during setup' in failure['exception']
            assert failure['SCFs_launched'] == 0 and failure['physical_admission'] is False
            assert not (run / 'result.json').exists() and not (run / 'J.npy').exists()
        else:
            assert launch['status'] == 'PASS_BOUNDED_FIRST_J_ONLY'
            assert launch['receipt']['returncode'] == 0
            assert launch['worker_result_error'] is None and launch['J_hash_error'] is None
            worker = json.loads((run / 'result.json').read_text())
            assert launch['worker_result'] == worker
            assert worker['status'] == 'PASS_BOUNDED_FIRST_J_ONLY'
            assert worker['J_calls'] == 1 and worker['SCFs_launched'] == 0
            assert worker['J_sha256'] == launch['J_sha256_observed']
            assert len(worker['J_sha256']) == 64
            assert worker['physical_admission'] is False and worker['parent_SCF_readiness'] is False
            assert worker['whole_SCF_performance_claim'] is False
            assert worker['checks'] == json.loads((run / 'checks.json').read_text())
            assert set(worker['checks']) == {'J_shape', 'J_finite', 'J_symmetric', 'one_J', 'one_factor',
                'no_ERI', 'no_3index', 'metric_cd', 'metric_shape', 'factor_immutable_Fortran', 'auxbasis', 'no_PCM'}
            assert all(value is True for value in worker['checks'].values())

    oxide = recursive / 'renewal/oxide-isotope-constraints'
    analysis = json.loads((oxide / 'analysis.json').read_text())
    assert analysis['status'] == 'MEASUREMENT_CONSTRAINT_ONLY'
    assert analysis['row_count'] == 17 and analysis['site_cell_count'] == 119
    assert analysis['reported_rate_count'] == 74
    assert analysis['too_fast_without_numeric_bound_count'] == 3
    assert analysis['not_reported_count'] == 42
    assert analysis['site_endpoints']['A'] == 'molecular_transformation'
    assert analysis['log_base']['source_explicitly_defines_base'] is False
    assert analysis['log_base']['arithmetic_assumption'] == 10
    for key in ('new_target_observations', 'new_candidate_assessments', 'verified_target_complements_added'):
        assert analysis['inference_limits'][key] == 0
    for key in ('target_rate_transfer', 'target_core_renewal_demonstrated', 'newly_competent_activity_demonstrated',
                'life_demonstrated', 'fit_performed', 'holdout_validation_performed'):
        assert analysis['inference_limits'][key] is False
    with (oxide / 'rates.csv').open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 17 and len({row['row_id'] for row in rows}) == 17
    statuses = [row[site + '_status'] for row in rows for site in 'ABCDEFG']
    assert {status: statuses.count(status) for status in set(statuses)} == {
        'reported': 74, 'too_fast_no_numeric_bound': 3, 'not_reported': 42}
    for row in rows:
        for site in 'ABCDEFG':
            if row[site + '_status'] != 'reported':
                assert row[site + '_log_k'] == row[site + '_uncertainty'] == ''
    manganese = json.loads((recursive / 'renewal/manganese-regeneration-constraints/constraints.json').read_text())
    assert manganese['status'] == 'RETROSPECTIVE_SOURCE_CONSTRAINTS_ONLY'
    for key in ('new_candidate_role', 'admitted_to_assembly', 'target_renewal_verified',
                'newly_competent_activity_positive_bound_identified', 'experimental_holdout',
                'raw_numerical_data_acquired'):
        assert manganese[key] is False
    assert manganese['new_fitted_models'] == manganese['new_physical_experiments'] == 0
    assert manganese['long_duration_protocol']['nominal_high_fraction_exact'] == '2/47'
    assert manganese['long_duration_protocol']['voltage_reference'] == 'two-electrode cell voltage'
    assert manganese['long_duration_protocol']['low_duration_minutes'] == 180
    assert manganese['long_duration_protocol']['high_duration_minutes'] == 8
    assert manganese['long_duration_protocol']['continuous_high_current_duration_identified'] is False
    assert manganese['QCM_protocol']['nominal_high_fraction_exact'] == '1/16'
    assert manganese['QCM_protocol']['low_duration_seconds'] == 300
    assert manganese['QCM_protocol']['high_duration_seconds'] == 20
    assert manganese['QCM_protocol']['slopes_transfer_to_long_protocol'] is False
    assert manganese['QCM_protocol']['long_duration_cycle_integrated_mass_balance'] is None
    control = manganese['phosphate_free_control']
    assert control['detection_limit'] is None
    assert control['reaction_rate_inferred_zero'] is False and control['catalytic_renewal_measured'] is False
    mixed = json.loads((recursive / 'identity/mixed-addenda-source-audit/evidence.json').read_text())
    assert mixed['exact_target_established'] is False and mixed['numerical_chemistry_jobs_run'] == 0
    findings = mixed['source_findings']
    assert len(findings) == 4 and all(finding['exact_target_supported'] is False for finding in findings)
    tungsten = next(finding for finding in findings if finding['id'] == 'moussawi_2017_mo36')
    for key in ('w_loading', 'refined_w_occupancy', 'derivative_cif', 'quantified_solution_stability'):
        assert tungsten[key] is None
    assert tungsten['full_thesis_acquired'] is False
    assert mixed['relationship_to_existing_bvs']['new_calculation'] is False
    assert mixed['relationship_to_existing_bvs']['exact_source_to_parent_site_map_established'] is False
    receiver = json.loads((recursive / 'renewal/receiver-function-audit/constraints.json').read_text())
    assert receiver['status'] == 'RETROSPECTIVE_RECEIVER_FUNCTION_CONSTRAINTS'
    assert receiver['candidate_role_count_added'] == receiver['verified_integrated_complements_added'] == 0
    positive = receiver['positive_control']
    assert positive['water_rinse'] is True and positive['oxygen_two_point_calibration'] is True
    assert positive['quantitative_rinse_carryover_bound'] is None
    for key in ('independent_atom_count', 'deposit_stable_during_assay', 'exclusive_surface_catalysis_proven'):
        assert positive[key] is False
    assert receiver['negative_control']['post_transfer_oxygen_nondetection_claim'] is False
    assert receiver['negative_control']['transient_heterogeneous_catalysis_excluded'] is False
    assert receiver['comparison_2011']['washed_deposit_product_quantification_verified'] is False
    accounting = receiver['conditional_activity_equivalent_accounting']
    assert accounting['measured_conversion_fractions'] is False
    assert accounting['exact_per_active_site_rates_inferred'] is False
    for key in ('target_identity_verified', 'target_renewal_verified', 'functional_inheritance_verified',
                'shared_target_medium_verified', 'graph_digitization', 'heldout_target_validation',
                'raw_measurement_arrays_acquired'):
        assert receiver['limits'][key] is False
    assert receiver['limits']['physical_experiments'] == receiver['limits']['fitted_models'] == 0
    verify_saved_j_followup(recursive)


def verify_saved_j_followup(recursive):
    run = recursive / 'parent-saved-j-qualification/run-v1'
    launch = json.loads((run / 'launch-result.json').read_text())
    terminal = json.loads((run / 'terminal-progress.json').read_text())
    assert launch['status'] == 'PASS_RETROSPECTIVE_SAVED_J_HANDOFF'
    assert launch['gate_unchanged'] is True and launch['SCF_skipped'] is False
    assert launch['maximum_children'] == 2 and launch['maximum_SCFs'] == 1
    assert launch['errors'] == terminal['errors'] == {}
    assert launch['receipts'] == terminal['receipts']
    assert launch['results'] == terminal['results']
    assert set(launch['results']) == set(launch['receipts']) == {'operators', 'scf'}
    for key in ('parent_run', 'fresh_holdout', 'physical_admission'):
        assert launch[key] is False
    for phase, count in (('operators', 21), ('scf', 79)):
        item = json.loads((run / phase / 'result.json').read_text())
        receipt = json.loads((run / phase / 'supervisor.json').read_text())
        assert item == launch['results'][phase] and receipt == launch['receipts'][phase]
        assert receipt['returncode'] == 0
        assert receipt['termination_reason'] is None and receipt['monitor_error'] is None
        assert item['case'] == 'new-external' and item['phase'] == phase
        assert item['status'] == ('PASS_OPERATORS' if phase == 'operators' else 'PASS_SCF')
        assert item['SCFs_launched'] == int(phase == 'scf')
        assert len(item['checks']) == count and all(check['pass'] is True for check in item['checks'])
        for key in ('parent_run', 'fresh_holdout', 'physical_admission'):
            assert item[key] is False
    assert json.loads((run / 'operator-receipt.json').read_text()) == launch['receipts']['operators']
    assert launch['results']['scf']['SCF']['converged'] is True
    assert launch['results']['scf']['SCF']['cycles'] == 32
    source = json.loads((recursive / 'identity/moussawi-occupancy-followup/evidence.json').read_text())
    assert source['outcome'] == 'NO_OCCUPANCY_OR_CIF_RECOVERED'
    assert source['parent_abstract_evidence_changed'] is False and source['nominal_target_verified'] is False
    assert source['chemistry_jobs_run'] == source['new_candidates_added'] == source['new_primary_structure_datasets'] == 0
    assert set(source['exact_missing_fields']) == {'w_loading', 'refined_site_occupancy', 'occupancy_uncertainty',
        'substituted_salt_formula', 'cif_identifier', 'counterion_assignment', 'protonation_assignment',
        'source_to_parent_topology_map', 'solution_persistence', 'vanadium_assignment'}
    assert all(value is None for value in source['exact_missing_fields'].values())
    assert source['catalogue']['full_thesis'] is False
    assert source['catalogue']['accessibility_flag_is_download_confirmation'] is False
    assert source['metadata_scope']['exhaustive_publication_coverage_claimed'] is False
    assert source['collaborator_thesis']['full_pdf_acquired'] is False
    assert source['collaborator_thesis']['ordinary_mo36_occupancy_supported'] is False
    pilot = recursive / 'parent-saved-j-pilot'
    status = json.loads((pilot / 'STATUS.json').read_text())
    assert status['status'] == 'FAIL_OR_INCOMPLETE'
    assert status['unit_tests_run'] == 22 and status['qualified_handoff_regression_tests'] == 15
    assert status['SCFs_launched'] == 1 and status['physical_admission'] is False
    assert status['execution_clearance'] is False and status['completed_cycles'] == 0
    assert status['native_converged'] is False and status['worker_result_status'] == 'RUNNING'
    assert status['historical_snapshot'] == 'history/f5c945a-incomplete'
    for key in ('implementation_complete', 'independent_implementation_review_complete', 'protocol_frozen',
                'prepared', 'gate_check_passed'):
        assert status[key] is True
    preparation = json.loads((pilot / 'preparation.json').read_text())
    approval = json.loads((pilot / 'independent-root-review.json').read_text())
    assert preparation['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
    assert preparation['parent_molecule_built'] is False and preparation['SCFs_launched'] == 0
    assert approval['status'] == 'APPROVED_ONE_PARENT_SAVED_J_PILOT'
    assert approval['independent_root_review'] is True and approval['physical_admission'] is False
    assert approval['preparation_sha256'] == 'c36e153c2cbf102764e8381685a4fda3691eed8a4701eeb2e6aca4f75602beed'
    assert approval['saved_J_qualification_artifacts'] == preparation['pins']['saved_J_qualification']
    for record in (preparation, approval):
        assert record['maximum_children'] == record['maximum_SCFs'] == 1
        assert record['wall_cap_seconds'] == 1800 and record['sampled_RSS_guard_bytes'] == 10 * 1024**3
    assert preparation['proof']['method']['max_cycle'] == approval['max_cycle'] == 20
    assert preparation['proof']['density_cycle'] == 0
    for name in ('run.py', 'test_run.py', 'PROTOCOL.md'):
        assert (pilot / name).is_file()
    run = pilot / 'run-v1'
    launch = json.loads((run / 'launch-result.json').read_text())
    worker = json.loads((run / 'result.json').read_text())
    receipt = json.loads((run / 'supervisor.json').read_text())
    assert launch['status'] == 'FAIL_OR_INCOMPLETE' and launch['required_evidence_present'] is False
    assert launch['receipt'] == receipt and launch['result'] == worker
    assert launch['gate_unchanged'] is True and launch['errors'] == {}
    assert receipt['returncode'] == -5
    assert receipt['termination_reason'] is None and receipt['monitor_error'] is None
    assert receipt['wall_seconds'] == 1346.6326383340638
    assert receipt['sampled_max_rss_bytes'] == 7584022528 and receipt['hard_OS_memory_limit'] is False
    assert worker['status'] == 'RUNNING' and worker['SCFs_launched'] == 1
    assert worker['initial_potential_complete'] is True
    for key in ('native_converged', 'final_validation_complete', 'physical_admission', 'fresh_holdout', 'geometry_optimization'):
        assert worker[key] is False
    for key in ('physical_admission', 'geometry_optimization', 'full_parent_oracle'):
        assert launch[key] is False
    assert 'latest_complete_cycle' not in worker and 'native_final_state' not in worker
    stages = [json.loads(line) for line in (run / 'stages.jsonl').read_text().splitlines()]
    assert stages[-1]['stage'] == 'native_metric_return' and stages[-1]['finite_J'] is True
    assert not any(row['stage'] in {'completed_cycle', 'kernel_return', 'native_post_kernel_entry',
        'native_post_kernel_return', 'final_validation_entry', 'final_validation_return'} for row in stages)
    for name in ('latest-complete-cycle.npz', 'native-final-state.npz', 'final-validated-state.npz'):
        assert not (run / name).exists()
    draft = pilot / 'history/f5c945a-incomplete'
    status = json.loads((draft / 'STATUS.json').read_text())
    assert status['status'] == 'DRAFT_INCOMPLETE_NOT_QUALIFIED'
    assert status['syntax_check'] == 'AST parse only; no import or execution'
    assert status['unit_tests_run'] == status['SCFs_launched'] == 0
    for key in ('implementation_complete', 'independent_implementation_review_complete', 'protocol_frozen',
                'prepared', 'physical_admission', 'execution_clearance'):
        assert status[key] is False
    assert (draft / 'run.py').is_file()
    for name in ('PROTOCOL.md', 'test_run.py', 'preparation.json', 'independent-root-review.json', 'run-v1'):
        assert not (draft / name).exists()
    vanadium = json.loads((recursive / 'identity/vanadium-incorporation-followup/evidence.json').read_text())
    assert vanadium['outcome'] == 'UNRESOLVED_VV_MO36_IDENTITY_WITH_PRECURSOR_DEPENDENCE_CONSTRAINT'
    for key in ('exact_target_changed', 'exact_target_verified', 'thermodynamic_exclusion_established'):
        assert vanadium[key] is False
    assert vanadium['scope']['structure_computations_run'] == vanadium['scope']['new_candidates_added'] == 0
    assert vanadium['scope']['targeted_search_count'] == vanadium['scope']['targeted_search_cap'] == 6
    assert vanadium['scope']['distinct_new_primary_route_count'] == vanadium['scope']['new_primary_route_cap'] == 4
    assert len(vanadium['missing_target_data']) == 14
    assert all(value is None for value in vanadium['missing_target_data'].values())
    matrix = vanadium['primary_constraint']['matrix']
    assert matrix['pH'] is None
    assert [entry['pH'] for entry in matrix['pH_conflicting_reports']] == [2.8, 4.2]
    assert matrix['mo_v_ratio'] == 4 and matrix['target_mo_v_ratio'] == 34
    for key in ('target_w_present_in_dataset', 'matched_sulfate_ammonium_inputs_demonstrated',
                'independently_measured_mo36_bound_valences'):
        assert matrix[key] is False
    assert vanadium['existing_evidence_reclassification']['formal_feed_v_oxidation_state'] == 4
    assert vanadium['existing_evidence_reclassification']['measured_vv_site'] is False
    assert vanadium['existing_evidence_reclassification']['preserve_original_raman_observation'] is True
    assert vanadium['next_test']['missing_51v_signal_alone_sufficient'] is False
    assert vanadium['next_test']['apply_4_to_1_data_as_34_to_1_target_calibration'] is False
    competing = json.loads((recursive / 'identity/competing-mov-speciation/evidence.json').read_text())
    assert competing['outcome'] == 'NUMERICAL_LEADS_RECOVERED_BUT_ZERO_PRIMARY_MOV_CALIBRATION_ROWS'
    assert competing['accepted_primary_mov_calibration_rows'] == []
    assert competing['scope']['scientific_simulations'] == competing['scope']['source_fits'] == competing['scope']['new_candidates'] == 0
    for key in ('changed', 'identity_established', 'thermodynamic_exclusion_established'):
        assert competing['target'][key] is False
    assert len(competing['reproduced_numeric_leads']) == 10
    for row in competing['reproduced_numeric_leads']:
        for key in ('original_source_acquired', 'calibration_eligible', 'original_row_conditions_verified'):
            assert row[key] is False
        assert row['uncertainty'] is None and row['original_component_denominator'] is None
    assert all(value is False for value in competing['application_boundary'].values())
    assert competing['denominator_audit']['automatic_conversion_to_vo4_basis'] is False
    assert competing['denominator_audit']['cross_system_w_mo_constant_comparison_admitted'] is False
    holdout = json.loads((recursive / 'identity/next-step/pcm-heldout-selection/selection.json').read_text())
    assert holdout['status'] == 'CANDIDATE_NUMERICAL_HOLDOUT_ACQUIRED_NOT_TESTED'
    assert holdout['formula'] == 'HMo2O7' and holdout['source_input_charge'] == -1
    assert holdout['scientific_operators_evaluated'] == holdout['SCFs_launched'] == 0
    assert holdout['planned_numerical_spin'] is None and holdout['numerical_qualification_pass'] is None
    for key in ('source_output_spin_verified', 'source_outputs_or_energies_inspected', 'successor_protocol_frozen',
                'chemical_validation', 'target_identity_verified', 'new_candidate_role', 'independent_source_family'):
        assert holdout[key] is False
    verify_crash_followup(recursive)


def verify_crash_followup(recursive):
    diagnostic = recursive / 'parent-saved-j-crash-diagnostic'
    crash = json.loads((diagnostic / 'crash-excerpt.json').read_text())
    assert crash['status'] == 'OBSERVED_CRASH_BOUNDARY_ROOT_CAUSE_UNRESOLVED'
    assert crash['root_cause_identified'] is False
    assert crash['scientific_operators_evaluated'] == crash['SCFs_launched'] == 0
    assert crash['pid'] == 94528 and crash['signal'] == 'SIGTRAP'
    assert crash['exception_type'] == 'EXC_BREAKPOINT' and crash['termination_code'] == 5
    fault = crash['threads'][crash['faulting_thread']]
    assert fault['faulting'] is True
    assert fault['frames'][0]['image_name'] == 'libsystem_malloc.dylib'
    allocation = json.loads((diagnostic / 'allocation-audit.json').read_text())
    assert allocation['status'] == 'PASS_SOURCE_ONLY_INTEGER_MODEL'
    assert allocation['guard']['unchanged'] is True
    assert allocation['guard']['before'] == allocation['guard']['after']
    assert 'exact compiled-source equivalence unproven' in allocation['evidence_boundary']
    observation = allocation['allocation_observation']
    assert observation['combined_bytes_per_thread_before_bookkeeping'] == 3200150672
    assert observation['OMP4_bytes_before_bookkeeping'] == 12800602688
    assert observation['four_GiB_is_conservative_allocated_virtual_bound'] is False
    assert observation['is_RSS_measurement_or_crash_cause'] is False
    assert allocation['negative_size_limit_control']['rejected'] is True
    assert allocation['writeback']['pass1']['shape'] == [19612, 1]
    assert allocation['writeback']['pass2']['shape'] == [3068, 3068]
    assert allocation['writeback']['pass2']['max_destination_index'] == 3068**2 - 1
    assert len(allocation['mock_scenarios']) == 3
    for scenario in allocation['mock_scenarios']:
        for result in scenario['passes']:
            assert all(order['flush_required'] is False for order in result['orders'])
    source = json.loads((recursive / 'identity/competing-mov-primary-followup/evidence.json').read_text())
    assert source['outcome'] == 'PRIMARY_SMALLER_MOV_FINGERPRINT_FOUND_ORIGINAL_1991_CONSTANTS_UNRESOLVED'
    assert source['scope']['scientific_fits'] == source['scope']['new_compounds_admitted'] == 0
    assert source['target']['changed'] is False and source['target']['identity_verified'] is False
    original = source['original_1991']
    assert original['original_full_text_acquired'] is False and original['reproduced_values_modified'] is False
    assert original['accepted_formation_constant_rows'] == []
    for key in ('verified_formation_reactions', 'verified_component_denominator', 'verified_uncertainties'):
        assert original[key] is None
    assert source['primary_assay']['ordinary_mo36'] is False
    assert source['conditions']['constant_pH_demonstrated'] is False
    assert source['conditions']['species_specific_response_validation'] is None
    fingerprint = source['assigned_fingerprint_rows']
    assert len(fingerprint) == 6
    assert [row['chemical_shift_ppm'] for row in fingerprint] == [-423, -494, -503, -513, -515, -523]
    for row in fingerprint:
        assert row['target_mo36_assignment'] is False and row['quantitative_abundance_calibration'] is False
    rows = source['reported_percentage_rows']
    assert len(rows) == 6
    assert [sum(row['reported_percent'].values()) for row in rows] == [105, 91, 106, 101, 101, 105]
    for row in rows:
        assert row['calibration_eligible'] is False and row['denominator'] is None and row['uncertainty'] is None
        assert row['zeros_are_reported_values_not_validated_detection_limits'] is True
    multiplicity = source['source_quality_flags'][0]
    assert multiplicity['as_printed'] == [2, 2, 2, 1, 2, 1]
    for row in source['reported_prose_observations']:
        assert row['detected_fraction_upper_bound'] is None and row['kinetic_rate_constant'] is None
        assert row['not_transferred_to_target'] is True
    verify_signed_boundary_followup(recursive)


def verify_signed_boundary_followup(recursive):
    diagnostic = recursive / 'parent-signed-j-diagnostic'
    preparation = json.loads((diagnostic / 'preparation.json').read_text())
    assert preparation['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
    assert preparation['SCFs_launched'] == preparation['operators_executed'] == 0
    assert preparation['molecule_built'] is False and preparation['physical_admission'] is False
    assert preparation['maximum_children'] == 1 and preparation['maximum_J_calls'] == 2
    assert preparation['wall_cap_seconds'] == 600 and preparation['sampled_RSS_guard_bytes'] == 10 * 1024**3
    assert preparation['density']['shape'] == [3068, 3068] and preparation['density']['cycle'] == 0
    for name in ('run.py', 'test_run.py', 'PROTOCOL.md'):
        assert (diagnostic / name).is_file()
    assert (diagnostic / 'independent-root-review.json').is_file()
    run = diagnostic / 'run-v1'
    launch = json.loads((run / 'launch-result.json').read_text())
    receipt = json.loads((run / 'supervisor.json').read_text())
    first = json.loads((run / 'first-checks.json').read_text())
    failure = json.loads((run / 'failure.json').read_text())
    assert launch['status'] == 'INCOMPLETE_OR_FAILED_SIGNED_J'
    assert launch['receipt'] == receipt and launch['worker_result'] == {}
    assert launch['gate_unchanged'] is True and launch['artifact_sha256'] == {}
    assert 'second-checks.json' in launch['errors']['artifacts']
    assert launch['maximum_children'] == 1 and launch['maximum_J_calls'] == 2 and launch['maximum_SCFs'] == 0
    assert launch['physical_admission'] is False and launch['parent_SCF_readiness'] is False
    assert receipt['returncode'] == 1
    assert receipt['termination_reason'] is None and receipt['monitor_error'] is None
    assert first['finite'] is True and first['symmetric'] is True and first['sign_pass'] is False
    assert first['max_sign_error'] == 5.282743131829193e-10
    assert preparation['absolute_tolerance'] == 1e-10 and preparation['relative_tolerance'] == 0
    assert first['max_sign_error'] > preparation['absolute_tolerance']
    assert failure['SCFs_launched'] == 0 and failure['physical_admission'] is False
    assert 'ValueError: First sign/finite/symmetry check failed' in failure['exception']
    for name in ('second-checks.json', 'selected-oracle.json', 'result.json', 'checks.json'):
        assert not (run / name).exists()
    assert (diagnostic / 'REPORT.md').is_file()
    membrane = json.loads((recursive / 'boundary/acidic-nanofiltration/evidence.json').read_text())
    assert membrane['new_candidate_roles'] == membrane['verified_integrated_complements_added'] == 0
    assert membrane['decision']['status'] == 'COMPONENT_SUPPORTED_ACIDIC_MEMBRANE_ARCHITECTURE_TARGET_FUNCTION_UNRESOLVED'
    for key in ('admission', 'cross_paper_integration_claim', 'heldout_validation'):
        assert membrane['decision'][key] is False
    for key in ('target_retention', 'target_seed_activity', 'precursor_and_proton_flux', 'boundary_renewal', 'functional_inheritance'):
        assert membrane['decision'][key] is None
    for key in ('chloride_medium_tested', 'POM_tested', 'target_tested'):
        assert membrane['membrane'][key] is False
    assert membrane['corrosion_protocol']['sequential_history_not_independent_pH_arms'] is True
    assert membrane['corrosion_protocol']['independent_membrane_replicate_count'] is None
    assert membrane['PEG_assay']['corrosion_pH_during_PEG_assay'] is None
    assert membrane['POM_comparator']['explicit_retention_denominator'] is None
    assert membrane['POM_comparator']['intact_species_resolved_recovery'] is None
    assert membrane['POM_comparator']['smaller_precursor_retention_measured'] is False
    for key in ('curve_digitizations', 'physical_experiments', 'target_transport_fits'):
        assert membrane['work_scope'][key] == 0
    assay_dir = recursive / 'identity/mov9-independent-assay-followup'
    assay = json.loads((assay_dir / 'evidence.json').read_text())
    assert assay['evidence_status'] == 'ACCESS_LIMITED_NO_QUANTITATIVE_SPECIATION_DATA_ACQUIRED'
    for key in ('admitted_quantitative_speciation_rows', 'admitted_calibration_rows',
                'admitted_active_retention_rows', 'admitted_independent_validation_rows'):
        assert assay[key] == []
    assert assay['source']['supporting_information_downloaded'] is False
    assert assay['source']['supporting_information_sha256'] is None
    assert assay['source']['full_methods_or_spectra_inspected'] is False
    assert all(value is None for value in assay['unavailable_measurements'].values())
    assert assay['source_family']['independent_experimental_data'] is None
    for key in ('independent_research_family', 'data_reuse_demonstrated', 'independent_measurement_check_possible'):
        assert assay['source_family'][key] is False
    assert assay['target_boundary']['new_candidate_count'] == 0
    for key in ('supports_ordinary_Krebs_Mo36_target_identity', 'supports_target_competing_species_quantitative_prediction',
                'target_admission_count_changed'):
        assert assay['target_boundary'][key] is False
    for row in assay['excluded_numerical_observations']:
        assert row['admissible_for_quantitative_speciation'] is False
        assert row['admissible_for_active_catalyst_retention'] is False
    acquisition = json.loads((assay_dir / 'acquisition.json').read_text())
    routes = {row['id']: row for row in acquisition['routes']}
    assert routes['R3']['outcome'] == 'FETCH_FAILED_403' and routes['R3']['http_status'] == 403
    assert routes['R3']['pdf_acquired'] is False and routes['R3']['pdf_sha256'] is None
    assert routes['R4']['outcome'] == 'FULLTEXT_LINK_REDIRECTED_TO_ABSTRACT'
    assert routes['R4']['http_status'] is None and routes['R4']['full_article_acquired'] is False
    candidate = recursive / 'boundary/pom-polyoxocation-23'
    decision = json.loads((candidate / 'DECISION.json').read_text())
    assessment = json.loads((candidate / 'assessment.json').read_text())
    assert decision['status'] == 'REVIEWED_SOURCE_CANDIDATE_ONLY_NOT_ADMITTED'
    assert decision['candidate_role_id'] == decision['aggregate_candidate_role_assessments'] == 23
    assert decision['aggregate_verified_integrated_complements'] == 0 and decision['verified_integrated_member'] is False
    for key in ('target_compatibility', 'intact_active_target_retention', 'functional_boundary_renewal'):
        assert decision[key] is None
    for key in ('physical_experiments', 'target_model_fits', 'heldout_target_validations'):
        assert decision[key] == 0
    assert decision['finite_growth_termination_preserved'] is True and decision['upper_concentration_failure_preserved'] is True
    assert assessment['candidate_role_id'] == 23 and assessment['verified_integrated_complement_admissions'] == 0
    assert assessment['decision']['integrated_complement_admitted'] is False
    assert assessment['joint_target_requirements']['target_mixture_tested'] is False
    for key in ('intact_target_identity', 'intact_target_activity', 'intact_target_recovery_fraction', 'recovery_denominator'):
        assert assessment['joint_target_requirements'][key] is None
    observations = {row['id']: row for row in assessment['observations']}
    assert observations['O3']['failure_threshold_mM_in_source'] == 30
    assert observations['O3']['maximum_tested_above_30_mM'] is None
    assert observations['O4']['remaining_seed_at_termination'] is True
    assert (recursive / 'boundary/active-retention-identifiability.md').is_file()
    verify_repeatability_followup(recursive)


def verify_repeatability_followup(recursive):
    repeatability = recursive / 'parent-j-repeatability'
    preparation = json.loads((repeatability / 'preparation.json').read_text())
    review = json.loads((repeatability / 'independent-root-review.json').read_text())
    assert preparation['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
    assert preparation['operators_executed'] == preparation['SCFs_launched'] == 0
    assert preparation['molecule_built'] is False and preparation['physical_admission'] is False
    assert preparation['sequence'] == [1, 1, -1]
    assert review['status'] == 'APPROVED_ONE_PARENT_J_REPEATABILITY_DIAGNOSTIC'
    assert review['independent_root_review'] is True and review['no_retry'] is True
    assert review['preparation_sha256'] == '5746a8e8fbecfb9084070dad998f3edb03d0135e19c5e6a07171d59379d52dde'
    assert review['parent_SCF_readiness'] is False and review['sign_and_call_order_confounded'] is True
    for record in (preparation, review):
        assert record['maximum_children'] == 1 and record['maximum_J_calls'] == 3
        assert record['wall_cap_seconds'] == 1000 and record['sampled_RSS_guard_bytes'] == 10 * 1024**3
        assert record['absolute_tolerance'] == 1e-10 and record['relative_tolerance'] == 0
        assert record['physical_admission'] is False
    history = repeatability / 'preparation-history'
    for prefix in ('pre-setup-order', 'pre-claim-guards'):
        snapshot = json.loads((history / (prefix + '.json')).read_text())
        assert snapshot['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
        assert snapshot['operators_executed'] == snapshot['SCFs_launched'] == 0
        for suffix in ('-PROTOCOL.md', '-run.py', '-test_run.py'):
            assert (history / (prefix + suffix)).is_file()
    run = repeatability / 'run-v1'
    launch = json.loads((run / 'launch-result.json').read_text())
    worker = json.loads((run / 'result.json').read_text())
    assert launch['status'] == worker['status'] == 'COMPLETED_WITH_NUMERICAL_NONPASS'
    assert launch['worker_result'] == worker and launch['errors'] == {}
    assert launch['gate_unchanged'] is True and worker['gate_unchanged'] is True
    assert launch['maximum_children'] == 1 and launch['maximum_J_calls'] == 3 and launch['maximum_SCFs'] == 0
    for record in (launch, worker):
        assert record['physical_admission'] is False and record['parent_SCF_readiness'] is False
    assert worker['J_calls'] == worker['metric_calls'] == 3 and worker['factor_count'] == 1
    assert worker['SCFs_launched'] == 0 and worker['invariants_passed'] is True
    assert worker['numerical_pass'] is False and worker['sign_and_call_order_confounded'] is True
    receipt = launch['receipt']
    assert receipt == json.loads((run / 'supervisor.json').read_text())
    assert receipt['returncode'] == 0 and receipt['termination_reason'] is None and receipt['monitor_error'] is None
    assert receipt['wall_seconds'] == 696.6868703749496 < receipt['wall_cap_seconds'] == 1000
    assert receipt['sampled_max_rss_bytes'] == 3655090176 < receipt['rss_guard_bytes'] == 10 * 1024**3
    assert receipt['hard_OS_memory_limit'] is False
    artifacts = launch['artifacts']
    assert artifacts['missing'] == [] and artifacts['errors'] == {}
    assert len(artifacts['sha256']) == 24
    assert worker['J_sha256'] == {name: artifacts['sha256'][name] for name in ('J1.npy', 'J2.npy', 'J3.npy')}
    calls = json.loads((run / 'call-records.json').read_text())
    assert [(record['call'], record['multiplier']) for record in calls] == [(1, 1), (2, 1), (3, -1)]
    stages = [json.loads(line) for line in (run / 'stages.jsonl').read_text().splitlines() if line.strip()]
    for record in calls:
        number = record['call']
        assert record['J_sha256'] == worker['J_sha256'][f'J{number}.npy']
        assert record['matrix_checks']['finite'] is True and record['matrix_checks']['symmetric'] is True
        call_stages = [stage for stage in stages if stage.get('call') == number]
        assert [stage['stage'] for stage in call_stages] == [
            'native_J_start', 'native_J_returned', 'returned_J_save_start', 'returned_J_saved_closed',
            'post_call_file_start', 'post_call_file_closed', 'full_arrays_released']
        assert call_stages[3]['sha256'] == record['J_sha256']
    comparisons = json.loads((run / 'comparisons.json').read_text())
    assert comparisons['missing'] == comparisons['errors'] == {}
    assert comparisons['external_reference_is_independent_algorithm'] is False
    assert comparisons['sign_and_call_order_confounded'] is True
    assert comparisons['categories'] == worker['categories'] == {
        'same_sign': 'NONPASS', 'sign_reversal': 'NONPASS', 'external_run': 'NONPASS'}
    expected = {
        'J2-J1': (4.844054046770907e-10, 284), 'J3+J1': (4.420286359163583e-10, 231),
        'J3+J2': (4.142748366575688e-10, 31), 'J1-Jold': (4.718572199635673e-10, 304),
        'J2-Jold': (9.484324436925817e-11, 0), 'J3+Jold': (3.2159164220502134e-10, 14)}
    assert set(comparisons['comparisons']) == set(expected)
    for name, (error, count) in expected.items():
        comparison = comparisons['comparisons'][name]
        assert comparison['absolute_tolerance'] == 1e-10 and comparison['relative_tolerance'] == 0
        assert comparison['max_absolute_error'] == error and comparison['entries_above_tolerance'] == count
        assert comparison['pass'] is (count == 0)
    charge = json.loads((recursive / 'boundary/pom-polyoxocation-23/charge-followup.json').read_text())
    assert charge['status'] == 'CHARGE_GAP_UNRESOLVED_SOURCE_METADATA_REVERIFIED'
    assert charge['candidate_role_id'] == 23
    for key in ('charge_gap_resolved', 'original_species_mechanism_verified', 'target_function_claim'):
        assert charge['decision'][key] is False
    for key in ('new_calibrated_speciation_rows', 'new_transport_or_retention_rows', 'new_candidate_role_count',
                'new_integrated_complement_admissions', 'scientific_fits', 'simulations', 'chemical_experiments'):
        assert charge['decision'][key] == 0
    for key in ('full_article_body_acquired', 'supporting_information_acquired', 'CIF_acquired'):
        assert charge['source'][key] is False
    arithmetic = charge['conditional_arithmetic']
    assert arithmetic['fixed_core_La_loss']['charge_difference'] == 2
    assert arithmetic['observed_six_electron_oxidation'] is False and arithmetic['observed_four_proton_loss'] is False
    assert arithmetic['accepted_conversion_reaction'] is None and arithmetic['rate_constants'] is None
    assert charge['relation_to_frozen_Points_assessment']['frozen_assessment_rewritten'] is False
    tubes = json.loads((recursive / 'boundary/tube-alternative-followup/evidence.json').read_text())
    assert tubes['status'] == 'ORGANIC_WALL_ROUTES_EXCLUDED_PHOSPHATE_LEAD_UNRESOLVED'
    for key in ('new_candidate_roles', 'verified_integrated_complements_added', 'physical_experiments', 'target_fits'):
        assert tubes[key] == 0
    assert len(tubes['primary_sources']) == 2
    for source in tubes['primary_sources']:
        assert source['carbon_free_active_wall_supported'] is False and source['active_target_retention'] is None
    lead = tubes['unresolved_lead']
    assert lead['methods_acquired'] is False and lead['cited_phosphate_transport_study_identified'] is False
    for key in ('wall_composition', 'pH', 'permeability', 'target_compatibility'):
        assert lead[key] is None
    phosphate = json.loads((recursive / 'boundary/phosphate-transport-lead/evidence.json').read_text())
    assert phosphate['status'] == 'CITED_TRANSPORT_SOURCE_IDENTIFIED_METHODS_UNRESOLVED'
    assert phosphate['new_candidate_roles'] == phosphate['verified_integrated_complements_added'] == 0
    assert phosphate['cited_transport_source']['methods_recovered'] is False
    for key in ('permeability_definition', 'numeric_permeability', 'uncertainty', 'pH'):
        assert phosphate['cited_transport_source'][key] is None
    for key in ('active_retention', 'acidic_compatibility', 'functional_renewal', 'growth_pH', 'phase_purity'):
        assert phosphate['target_evidence'][key] is None
    assert phosphate['target_evidence']['heldout_validation'] is False
    assert phosphate['target_evidence']['integrated_admission'] is False
    verify_stage_transport_followup(recursive)


def verify_stage_transport_followup(recursive):
    for folder, status in (
            ('parent-j-error-impact', 'PREPARED_SAVED_ARRAY_ANALYSIS_NOT_RUN'),
            ('parent-j-stage-localization', 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW')):
        base = recursive / folder
        preparation = json.loads((base / 'preparation.json').read_text())
        assert preparation['status'] == status
        assert preparation['operators_executed'] == preparation['SCFs_launched'] == 0
        for name in ('PROTOCOL.md', 'run.py', 'test_run.py'):
            assert (base / name).is_file()
        if folder == 'parent-j-error-impact':
            assert preparation['real_arrays_analyzed'] is False
        else:
            assert preparation['PCM_builds'] == 0 and preparation['molecule_built'] is False
            assert preparation['physical_admission'] is False
            assert preparation['maximum_children'] == 1 and preparation['maximum_J_calls'] == 3
            assert preparation['wall_cap_seconds'] == 1000 and preparation['sampled_RSS_guard_bytes'] == 10 * 1024**3
            assert preparation['J_absolute_tolerance'] == 1e-10 and preparation['J_relative_tolerance'] == 0
            assert preparation['sequence'] == ['ordinary_A_P0', 'ordinary_B_P0', 'controlled_C_fixed_rho_A']
    impact = recursive / 'parent-j-error-impact'
    review = json.loads((impact / 'independent-root-review.json').read_text())
    assert review['status'] == 'APPROVED_SAVED_ARRAY_ERROR_IMPACT'
    assert review['independent_root_review'] is True and review['scientific_admission'] is False
    assert review['original_threshold_unchanged'] is True
    assert review['preparation_sha256'] == '8525666d8c02c092d160425a63a5ce84d5d4b9537e2f9d6c36a3c13c8efffd68'
    gate = json.loads((impact / 'analysis-v1/analysis-gate.json').read_text())
    assert gate['preparation_sha256'] == review['preparation_sha256']
    assert gate['review_sha256'] == '2977066eecd1eb167e21d18c93f2feb6785477fb152811faf8daa316c2ce8e79'
    result = json.loads((impact / 'analysis-v1/result.json').read_text())
    assert result['status'] == 'COMPLETE_FIXED_DENSITY_SENSITIVITY_ONLY'
    assert result['operators_executed'] == result['SCFs_launched'] == 0
    for key in ('physical_admission', 'parent_SCF_readiness', 'tolerance_relaxed'):
        assert result[key] is False
    assert result['input_pins_unchanged'] is True and result['AO_element_localization'] is None
    assert result['original_nonpasses'] == 5 and result['original_passes'] == 1
    original = json.loads((recursive / 'parent-j-repeatability/run-v1/comparisons.json').read_text())
    assert result['original_categories_unchanged'] == original['categories']
    assert set(result['comparisons']) == set(original['comparisons'])
    for name, row in result['comparisons'].items():
        prior = original['comparisons'][name]
        assert row['original_comparison'] == prior
        assert row['original_threshold_pass_recomputed'] is prior['pass']
        assert row['entries_above_original_tolerance'] == prior['entries_above_tolerance']
        assert row['max_absolute_entry'] == prior['max_absolute_error'] and row['argmax'] == prior['argmax']
        assert row['absolute_tolerance_unchanged'] == 1e-10 and row['relative_tolerance_unchanged'] == 0
    verify_stage_localization(recursive)
    copper = recursive / 'boundary/copper-phosphate-transport'
    evidence = json.loads((copper / 'evidence.json').read_text())
    assert evidence['status'] == 'SOURCE_ASSESSMENT_PENDING_INDEPENDENT_REVIEW'
    assert evidence['proposed_candidate_role_id'] == 24 and evidence['aggregate_before_registration'] == 23
    assert evidence['verified_integrated_complement_admissions'] == 0
    assert evidence['proposition']['exact_phase_stoichiometry'] is None
    assert evidence['proposition']['pure_Cu3_PO4_2_identity_verified'] is False
    assert evidence['proposition']['target_mixture_tested'] is False
    constraints = evidence['constraints']
    slope = constraints['growth_regression_slope']
    assert slope['zero_intercept_established'] is False and slope['pointwise_ratio_equivalence_established'] is False
    for key in ('solute_permeability', 'hydraulic_permeance', 'membrane_rejection_of_intact_target',
                'active_target_recovery', 'functional_boundary_renewal', 'shared_target_medium'):
        assert constraints[key] is None
    formation = constraints['formation_tests']
    assert formation['pH_and_outcome'] == [
        {'pH': 12.64, 'outcome': 'tubes'}, {'pH': 9.08, 'outcome': 'short tubes'},
        {'pH': 4.19, 'outcome': 'no precipitation'}]
    for key in ('only_proton_activity_changed', 'preformed_wall_dissolution_tested', 'target_pH_1_7_tested'):
        assert formation[key] is False
    for key in ('physical_experiments', 'target_fits', 'heldout_target_validations', 'digitized_figure_points'):
        assert evidence['work_scope'][key] == 0
    for key in ('target_function_demonstrated', 'integrated_admission', 'universal_acidic_wall_failure_proven',
                'target_formula_changed'):
        assert evidence['decision_boundary'][key] is False
    for name in ('INDEPENDENT_REVIEW.md', 'REPORT.md', 'model-observable.md'):
        assert (copper / name).is_file()
    with (copper / 'linear-growth.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == constraints['table2_rows'] == 5
    assert evidence['source']['uncertainty_type'] is None
    assert all(row['uncertainty_definition'] == 'unreported' for row in rows)
    decision = json.loads((copper / 'DECISION.json').read_text())
    assert decision['status'] == 'REVIEWED_SOURCE_CANDIDATE_ONLY_NOT_ADMITTED'
    assert decision['candidate_role_id'] == decision['aggregate_candidate_role_assessments'] == 24
    assert decision['aggregate_verified_integrated_complements'] == 0
    for key in ('verified_integrated_member', 'preformed_wall_acid_survival_tested',
                'pure_Cu3_PO4_2_phase_verified', 'growth_regression_identifies_target_transport'):
        assert decision[key] is False
    for key in ('target_compatibility', 'intact_active_target_retention', 'functional_boundary_renewal'):
        assert decision[key] is None
    for key in ('physical_experiments', 'target_model_fits', 'heldout_target_validations'):
        assert decision[key] == 0
    assert decision['source_pH_4_19_formation_failure_preserved'] is True
    for name, key in (('evidence.json', 'assessment_sha256'), ('REPORT.md', 'report_sha256'),
                      ('acquisition.json', 'acquisition_sha256'), ('INDEPENDENT_REVIEW.md', 'independent_review_sha256'),
                      ('model-observable.md', 'model_sha256'), ('linear-growth.csv', 'table_sha256')):
        assert hashlib.sha256((copper / name).read_bytes()).hexdigest() == decision[key]
    verify_source_constraints(recursive)
    verify_metric_checkpoint(recursive)


def verify_metric_checkpoint(recursive):
    failed = recursive / 'parent-metric-solve-diagnostic/run-v1'
    launch = json.loads((failed / 'launch-result.json').read_text())
    receipt = json.loads((failed / 'supervisor.json').read_text())
    assert launch['completed'] is False and launch['physical_admission'] is False
    assert launch['receipt'] == receipt and receipt['returncode'] == 1
    assert receipt['termination_reason'] is receipt['monitor_error'] is None
    failure = json.loads((failed / 'failure.json').read_text())
    assert failure['physical_admission'] is False
    assert failure['exception'].rstrip().endswith('ValueError: Molecule state changed')
    for name in ('result.json', 'original_metric.npy', 'SCF-result.json'):
        assert not (failed / name).exists()
    prepared = recursive / 'parent-metric-solve-diagnostic-v2'
    preparation = json.loads((prepared / 'preparation.json').read_text())
    assert preparation['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
    assert preparation['J_calls'] == preparation['SCFs'] == preparation['PCM_builds'] == 0
    assert preparation['physical_admission'] is False
    approval = json.loads((prepared / 'independent-root-review.json').read_text())
    assert approval['status'] == 'APPROVED_ONE_PARENT_METRIC_SOLVE_DIAGNOSTIC'
    terminal = json.loads((prepared / 'run-v1/launch-result.json').read_text())
    supervisor = json.loads((prepared / 'run-v1/supervisor.json').read_text())
    assert terminal['completed'] is terminal['physical_admission'] is False
    assert terminal['receipt'] == supervisor and supervisor['returncode'] == -10
    assert supervisor['termination_reason'] is supervisor['monitor_error'] is None
    for name in ('result.json', 'matrix-factor.json', 'SCF-result.json', 'original_metric.npy'):
        assert not (prepared / 'run-v1' / name).exists()
    postmortem = json.loads((prepared / 'postmortem/result.json').read_text())
    assert postmortem['terminal_artifacts_verified'] == terminal['artifact_hashes']
    assert postmortem['terminal_artifacts_verified']['original_metric.npy'] == '00a6c22b1bbf0d90ae9d4905b4dd4fa9edc864bb27c2af9a93ca2ce1b40aa3af'
    metric = postmortem['saved_metric']
    assert metric['shape'] == [19612, 19612] and metric['file_bytes'] == 3077044480
    assert metric['all_finite'] is True and metric['symmetry_max'] == 0
    assert metric['positive_definiteness_established'] is False
    assert postmortem['exception']['signal'] == 'SIGBUS'
    assert postmortem['root_cause_established'] is postmortem['physical_admission'] is False
    assert postmortem['factorizations'] == postmortem['solves'] == postmortem['J_calls'] == postmortem['SCFs'] == 0
    verify_blas_checkpoint(recursive)
    for name, passed in (('qualification.json', True), ('qualification-failed-v1.json', False)):
        qualification = json.loads((prepared / name).read_text())
        assert qualification['passed'] is passed and qualification['tests_run'] == 9
        assert qualification['native_parent_integrals'] == qualification['J_calls'] == qualification['SCFs'] == 0
        for case in qualification['cases']:
            assert case['estimate']['certified_bound'] is False
            assert case['errors']['certified_error_bound'] is False
    probe = json.loads((prepared / 'metadata-probe.json').read_text())
    assert probe['exact_prior_match'] is probe['aux_exact_prior_match'] is True
    assert probe['native_integral_calls'] == probe['J_calls'] == 0 and probe['PCM_unbuilt'] is True
    assert probe['after_setup_state'] == probe['prior_state']
    assert probe['changed_env_slots'] == [
        {'index': 18, 'before': 0.0, 'after': 1260.0}, {'index': 19, 'before': 0.0, 'after': 144.0}]
    ordering = json.loads((prepared / 'ordering-probe.json').read_text())['permutations']
    assert len(ordering) == 6 and all(row['native_integrals'] == 0 for row in ordering)
    assert [row['order'] for row in ordering if row['parent_match'] or row['aux_match']] == [['O', 'Mo', 'H']]
    source = recursive / 'boundary/aqueous-pom-nanofiltration-followup'
    evidence = json.loads((source / 'evidence.json').read_text())
    results = json.loads((source / 'extracted-results.json').read_text())
    assert evidence['status'] == 'RETROSPECTIVE_SOURCE_COMPARATOR_NOT_ADMITTED'
    assert evidence['conditional_incompatible_table3_concentrations_mM'] == [1, 5]
    assert evidence['fitted_parameters'] == [] and evidence['negative_results_preserved'] is True
    for key in ('target_compound_tested', 'functional_inheritance_observed',
                'catalytic_competence_of_target_observed', 'held_out_validation',
                's8_flux_reported_standard_deviation_reproduced'):
        assert evidence[key] is False
    for record in (evidence, results):
        assert record['new_candidate_roles'] == record['complement_admissions'] == 0
        assert record['held_out_validation'] is False
        assert record['source_sha256'] == '7fb77831963fcd4e25a5f62f454cbc8412525628f0e3286fa12f4f984b20f955'
    assert results['fit_performed'] is False and results['self_checks_passed'] == 4
    assert len(results['rows']) == evidence['extracted_main_table_rows'] == 15
    assert all(row['retrospective'] is True and row['target_compound_tested'] is False for row in results['rows'])
    checks = results['table3_ratio_checks']
    assert [row['concentration_mM'] for row in checks] == [1, 5, 10, 25, 50]
    for key in ('joint_exact_reported_ratio', 'joint_ratio_also_rounded_half_unit'):
        assert [row[key]['compatible_with_closed_envelope'] for row in checks] == [False, False, True, True, True]
    supplement = results['supplement']
    assert len(supplement['table_s7_source_rows']) == 10 and len(supplement['table_s8_source_rows']) == 3
    assert evidence['extracted_supplementary_rows'] == 13 and supplement['statistical_assertions_passed'] == 3
    assert supplement['table_s8_concentration_mM'] is evidence['s8_feed_concentration'] is None
    assert supplement['table_s8_flux_sd_reproduced'] is False
    assert all(row[2:4] == ['> 99', '> 99'] for row in supplement['table_s8_source_rows'])
    assert supplement['table_s8_stats']['permeate_flux_L_m2_h']['sample_variance_exact'] == '43'
    assert supplement['table_s8_reported_sd']['permeate_flux_L_m2_h'] == '4'


def verify_stage_localization(recursive):
    base = recursive / 'parent-j-stage-localization'
    review = json.loads((base / 'independent-root-review.json').read_text())
    assert review['status'] == 'APPROVED_ONE_PARENT_J_STAGE_LOCALIZATION'
    assert review['independent_root_review'] is True and review['physical_admission'] is False
    assert review['preparation_sha256'] == '077b972b1ea43bbf0472a7dcda5e3bbe89f964a583ee6ea2f34282c32b806c73'
    run = base / 'run-v1'
    gate = json.loads((run / 'launch-gate.json').read_text())
    assert gate['preparation_sha256'] == review['preparation_sha256']
    assert gate['review_sha256'] == '1e4e34875a0a160a09569fe002426ee250e7b1a7a7a7b779d548d2ec961cb3f5'
    assert gate['qualification_artifacts'] == review['qualification_artifacts']
    launch = json.loads((run / 'launch-result.json').read_text())
    result = json.loads((run / 'result.json').read_text())
    assert launch['completed'] is True and launch['worker_result'] == result
    assert result['status'] == 'COMPLETED_BOUNDED_STAGE_LOCALIZATION'
    assert result['calls'] == 3 and result['SCFs_launched'] == result['PCM_builds'] == 0
    assert result['invariants_passed'] is True and result['controlled_output_is_ordinary_J_P0'] is False
    for record in (launch, result):
        assert record['gate_unchanged'] is True
        assert record['physical_admission'] is False and record['parent_SCF_readiness'] is False
    receipt = json.loads((run / 'supervisor.json').read_text())
    assert launch['receipt'] == receipt and receipt['returncode'] == 0
    assert receipt['termination_reason'] is None and receipt['monitor_error'] is None
    assert receipt['wall_seconds'] == 698.8856680409517 < receipt['wall_cap_seconds'] == 1000
    assert receipt['sampled_max_rss_bytes'] == 3643949056 < receipt['rss_guard_bytes'] == 10 * 1024**3
    assert receipt['hard_OS_memory_limit'] is False
    assert len(launch['artifact_hashes']) == 30 and len(result['output_hashes']) == 9
    for name, digest in result['output_hashes'].items():
        assert launch['artifact_hashes'][name + '.npy'] == digest
    for arm, output in (('A', 'J_A'), ('B', 'J_B'), ('C', 'J_fixed_rho_A')):
        call = json.loads((run / f'call-{arm}.json').read_text())
        assert call['arm'] == arm and call['output'] == output
        assert call['ordinary_J_P0'] is (arm != 'C')
        assert call['solve_capture']['ordinary_returned_unchanged'] is (arm != 'C')
        assert call['matrix_checks']['finite'] is True and call['matrix_checks']['symmetric'] is True
        assert call['hashes'] == {name: result['output_hashes'][name] for name in
                                 (output, f'b_{arm}', f'rho_ordinary_{arm}')}
    comparisons = json.loads((run / 'comparisons.json').read_text())
    assert comparisons == result['comparisons']
    assert comparisons['controlled_output_is_ordinary_J_P0'] is False
    assert comparisons['stage_causality_proven'] is False
    expected = {'J_B_minus_J_A': (1.1883116712851916e-10, 2),
                'J_fixed_rho_A_minus_J_A': (6.536993168992922e-13, 0)}
    assert set(comparisons['J_comparisons']) == set(expected)
    for name, (error, count) in expected.items():
        row = comparisons['J_comparisons'][name]
        assert row['max_absolute_error'] == error and row['entries_above_tolerance'] == count
        assert row['pass'] is (count == 0)
        assert row['absolute_tolerance'] == 1e-10 and row['relative_tolerance'] == 0
    assert len(comparisons['vector_comparisons']) == 4
    for row in comparisons['vector_comparisons'].values():
        assert row['acceptance_threshold'] is None and row['exact_equal'] is False
    sensitivity = json.loads((base / 'saved-vector-sensitivity.json').read_text())
    assert sensitivity['operators_executed'] == sensitivity['SCFs_launched'] == 0
    assert sensitivity['scope'] == 'Observed saved-vector sensitivity only; not a condition-number estimate or certified bound'
    assert sensitivity['input_sha256'] == {name + '.npy': digest for name, digest in
        result['output_hashes'].items() if not name.startswith('J_')}
    for name in ('SCF-result.json', 'iterations.jsonl'):
        assert not (run / name).exists()


def verify_source_constraints(recursive):
    for folder, status in (
            ('boundary/hollow-silicalite-followup', 'REVIEWED_B1_ARCHITECTURE_REFINEMENT_ONLY'),
            ('identity/beta-vmo7-discriminator', 'REVIEWED_COMPETING_SPECIES_CONSTRAINT_ONLY')):
        base = recursive / folder
        evidence = json.loads((base / 'evidence.json').read_text())
        review = json.loads((base / 'ROOT_REVIEW.json').read_text())
        assert evidence['status'] == 'SOURCE_DOSSIER_PENDING_ROOT_REVIEW'
        assert review['status'] == status and review['original_dossier_pending_status_is_historical'] is True
        assert review['primary_text_checked'] is True and review['source_limits_preserved'] is True
        for key in ('local_primary_pdf_acquired', 'raw_measurements_acquired', 'target_model_calibration',
                    'heldout_target_validation', 'physical_target_tested'):
            assert review[key] is False
        assert review['new_candidate_roles'] == review['verified_integrated_complement_admissions'] == 0
        assert evidence['new_complement_roles'] == evidence['verified_integrated_complements'] == 0
        for key in ('heldout_target_validation', 'target_identity_demonstrated',
                    'target_joint_function_demonstrated', 'registration_performed'):
            assert evidence[key] is False
        assert all(value is None for value in evidence['target_parameters'].values())
        assert evidence['source']['local_source_file'] is evidence['source']['local_source_sha256'] is None
        for name, digest in review['artifact_sha256'].items():
            assert hashlib.sha256((base / name).read_bytes()).hexdigest() == digest
        if 'silicalite' in folder:
            assert evidence['existing_role_refinement'] == 'B1'
            loss = evidence['observed_in_source_as_reported_by_researcher'][-1]
            assert loss['encapsulated_reported_percent'] == 11 and loss['exterior_impregnated_reported_percent'] == 89
            assert loss['intact_molecular_fraction_measured'] is False and loss['active_fraction_measured'] is False
        else:
            conflicts = evidence['unresolved_source_conflicts']
            assert conflicts['NaCl']['adopted_value'] is None
            assert conflicts['dissolved_solid_pH']['adopted_values'] is None
            measurement = evidence['observed_in_source_as_reported_by_researcher'][1]
            assert measurement['claimed_VV_percent_by_time'] == [95, 73]
            assert measurement['response_validation_recovered'] is False and measurement['uncertainty'] is None
            assert all(row['new_dataset'] is False for row in evidence['prior_duplicate_leads'])
            assert hashlib.sha256((base / 'elemental-counterexample.md').read_bytes()).hexdigest() == '0a9852d6c4efced9fbe21db2c8a9e461ab1dbc8cfc5e32e3dfbf257220ee8b4e'


def verify_blas_checkpoint(recursive):
    audit = recursive / 'parent-blas-control-audit'
    verification = json.loads((audit / 'verification.json').read_text())
    observed = json.loads((audit / 'observed.json').read_text())
    assert verification['status'] == 'PASS_TINY_CONTROL_PROBE_ONLY'
    assert verification['native_solves_verified'] == 5 and verification['failed_setup_attempts_preserved'] == 2
    assert observed['parallel'] == 2 and observed['requested_environment']['OPENBLAS_NUM_THREADS'] == '1'
    states = {row['label']: (row['blas'], row['pyscf']) for row in observed['states']}
    assert states['initial'] == states['restored_after_exception'] == (4, 4)
    assert states['pyscf_context_before_explicit_setter_before'] == (4, 1)
    assert states['explicit_blas_one_before'] == (1, 4)
    assert observed['completed'] is observed['bitwise_equal_answers'] is True
    assert len(observed['solves']) == 5
    for row in observed['solves']:
        assert row['pass'] is True and row['residual_max_abs'] == row['error_max_abs'] == 0
        assert row['answer'] == [1, -2, 3, -0.5]
    for folder, code in (('', 0), ('failed-v1', 1), ('failed-v2', 1)):
        assert json.loads((audit / folder / 'supervisor.json').read_text())['returncode'] == code
    replay = recursive / 'parent-saved-metric-solve'
    prep = json.loads((replay / 'preparation.json').read_text())
    assert prep['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
    assert prep['parent_metric_builds'] == prep['J_calls'] == prep['SCFs'] == prep['PCM_builds'] == 0
    assert prep['physical_admission'] is False
    approval = json.loads((replay / 'independent-root-review.json').read_text())
    assert approval['status'] == 'APPROVED_ONE_SAVED_METRIC_SOLVE_DIAGNOSTIC'
    assert approval['independent_root_review'] is True
    assert approval['preparation_sha256'] == '75aae4c3937ccfd774246a10be98661ad848df2edc349a0b54df17267361c99f'
    launch = json.loads((replay / 'run-v1/launch-result.json').read_text())
    result = json.loads((replay / 'run-v1/result.json').read_text())
    assert launch['completed'] is True and launch['receipt']['returncode'] == 0
    assert len(launch['artifact_hashes']) == 37 and launch['physical_admission'] is False
    assert launch['artifact_hashes']['rho_A1.npy'] == launch['artifact_hashes']['rho_A2.npy']
    assert result['status'] == 'COMPLETED_SAVED_METRIC_SOLVE_DIAGNOSTIC_ONLY'
    assert result['comparisons']['A2']['exact_equal'] is True
    assert result['comparisons']['A2']['max_absolute_difference'] == result['comparisons']['A2']['RMS_difference'] == 0
    for arm in ('B', 'C'):
        assert result['comparisons'][arm]['exact_equal'] is False
        assert result['comparisons'][arm]['max_absolute_difference'] > 0
    assert all(row['acceptance_threshold'] is None for row in result['comparisons'].values())
    assert result['condition']['certified_bound'] is False and result['condition']['info'] == 0
    assert result['condition']['one_norm_condition_estimate'] == 24972383299521.492
    assert result['condition']['reciprocal_one_norm_condition_estimate'] == 4.004423558640322e-14
    for key in ('factor_matches_prior', 'physical_admission', 'parent_SCF_readiness', 'prior_call_causality_established'):
        assert result[key] is False
    assert result['J_calls'] == result['SCFs'] == result['PCM_builds'] == 0
    assert result['prior_J_tolerance_unchanged'] == 1e-10
    assert result['thread_counts_are_configured_getters_not_measured_team_sizes'] is True
    explicit = recursive / 'parent-explicit-blas-j'
    pending = json.loads((explicit / 'preparation.json').read_text())
    mocks = json.loads((explicit / 'qualification.json').read_text())
    assert pending['status'] == 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'
    assert sum(len(group) for group in pending['pins'].values()) == 429
    assert pending['SCFs'] == pending['PCM_builds'] == pending['operators_executed'] == 0
    assert pending['physical_admission'] is pending['parent_SCF_readiness'] is False
    assert mocks['passed'] is mocks['mock_only'] is True
    assert mocks['tests_run'] == 6 and mocks['failures'] == mocks['errors'] == mocks['native_parent_calls'] == 0
    assert not (explicit / 'independent-root-review.json').exists() and not (explicit / 'run-v1').exists()
    qualification = json.loads((replay / 'qualification.json').read_text())
    assert qualification['passed'] is True and qualification['tests_run'] == 8
    assert qualification['parent_native_execution'] is False
    for folder in ('boundary/hollow-silicalite-followup/wetting-constraint', 'identity/concentration-speciation-followup'):
        review = json.loads((recursive / folder / 'ROOT_REVIEW.json').read_text())
        assert review['new_candidate_roles'] == review['verified_integrated_complement_admissions'] == 0
        assert review['heldout_target_validation'] is review['physical_target_tested'] is False
    evidence = json.loads((recursive / 'identity/concentration-speciation-followup/evidence.json').read_text())
    assert evidence['target_tested'] is evidence['heldout_target_validation'] is False
    assert evidence['fitted_target_parameters'] == [] and evidence['negative_results_preserved'] is True


def verify_stage_artifact_bindings(recursive, included):
    source_hashes = {record['path']: record['source_sha256'] for record in included}
    stage = 'parent-j-stage-localization/run-v1'
    launch = json.loads((recursive / stage / 'launch-result.json').read_text())
    omitted_logs = {'native.log', 'stdout.txt', 'stderr.txt'}
    assert all('recursive-compound-2026-10-15/' + stage + '/' + name not in source_hashes
               for name in omitted_logs)
    bindings = {stage + '/' + name: digest for name, digest in launch['artifact_hashes'].items()
                if name not in omitted_logs}
    metric = 'parent-metric-solve-diagnostic/run-v1'
    failure = json.loads((recursive / metric / 'launch-result.json').read_text())
    bindings.update({metric + '/' + name: digest for name, digest in failure['artifact_hashes'].items()
                     if name not in omitted_logs})
    metric_v2 = 'parent-metric-solve-diagnostic-v2/run-v1'
    terminal = json.loads((recursive / metric_v2 / 'launch-result.json').read_text())
    bindings.update({metric_v2 + '/' + name: digest for name, digest in terminal['artifact_hashes'].items()
                     if name not in omitted_logs | {'original_metric.npy'}})
    assert 'recursive-compound-2026-10-15/' + metric_v2 + '/original_metric.npy' not in source_hashes
    replay = 'parent-saved-metric-solve/run-v1'
    completed = json.loads((recursive / replay / 'launch-result.json').read_text())
    assert len(completed['artifact_hashes']) == 37
    assert all('recursive-compound-2026-10-15/' + replay + '/' + name not in source_hashes
               for name in omitted_logs)
    bindings.update({replay + '/' + name: digest for name, digest in completed['artifact_hashes'].items()
                     if name not in omitted_logs})
    for folder, receipt, key in (('parent-blas-control-audit', 'verification.json', 'sha256'),
                                 ('parent-saved-metric-solve', 'qualification.json', 'tiny_artifact_hashes')):
        hashes = json.loads((recursive / folder / receipt).read_text())[key]
        bindings.update({folder + '/' + name: digest for name, digest in hashes.items()
                         if name.split('/')[-1] not in omitted_logs and not name.startswith('sources/')})
    for folder in ('boundary/hollow-silicalite-followup', 'identity/beta-vmo7-discriminator',
                   'boundary/hollow-silicalite-followup/wetting-constraint', 'identity/concentration-speciation-followup'):
        review = json.loads((recursive / folder / 'ROOT_REVIEW.json').read_text())
        bindings.update({folder + '/' + name: digest for name, digest in review['artifact_sha256'].items()})
    copper = 'boundary/copper-phosphate-transport'
    decision = json.loads((recursive / copper / 'DECISION.json').read_text())
    for name, key in (('evidence.json', 'assessment_sha256'), ('REPORT.md', 'report_sha256'),
                      ('acquisition.json', 'acquisition_sha256'), ('INDEPENDENT_REVIEW.md', 'independent_review_sha256'),
                      ('model-observable.md', 'model_sha256'), ('linear-growth.csv', 'table_sha256')):
        bindings[copper + '/' + name] = decision[key]
    for name, digest in bindings.items():
        assert source_hashes['recursive-compound-2026-10-15/' + name] == digest


def verify_parent_pilot_source_bindings(included):
    # Published paths are sanitized; immutable launch pins refer to original source bytes.
    source_hashes = {record['path']: record['source_sha256'] for record in included}
    expected = {
        'preparation.json': 'c36e153c2cbf102764e8381685a4fda3691eed8a4701eeb2e6aca4f75602beed',
        'independent-root-review.json': '56453679ecac728c78363faccd6f7b2a3bec2ea80fdfa546b5299ff9be1223de',
        'history/f5c945a-incomplete/run.py': '0cc1e086687a9f50f1b334bb65cdac32aee9977fa72d31121e6b2311f514e7ce',
        'history/f5c945a-incomplete/STATUS.json': '0f513146f3fa0dc35b7020e96c831f4f95ad6bb7ccc6ae78de2f7043c45bf01e'}
    for name, digest in expected.items():
        assert source_hashes['recursive-compound-2026-10-15/parent-saved-j-pilot/' + name] == digest
    assert source_hashes['recursive-compound-2026-10-15/parent-j-repeatability/preparation.json'] == '5746a8e8fbecfb9084070dad998f3edb03d0135e19c5e6a07171d59379d52dde'
    for name, digest in {
            'J1.npy': '8bacd08c2f8e852b9dd164bd33aa6518d872dd87b65cce2ffeabab7d6f861bb6',
            'J2.npy': 'de18f44800b2fa29fe36b171fedfcefd3d01cf0f38fd55b937616744d890c831',
            'J3.npy': 'a152f67d3cea79974e826aac9fd39ff2b9f33712ce1577fd1759bd5f2d5101ee'}.items():
        assert source_hashes['recursive-compound-2026-10-15/parent-j-repeatability/run-v1/' + name] == digest
    for name, digest in {
            'parent-j-error-impact/preparation.json': '8525666d8c02c092d160425a63a5ce84d5d4b9537e2f9d6c36a3c13c8efffd68',
            'parent-j-error-impact/independent-root-review.json': '2977066eecd1eb167e21d18c93f2feb6785477fb152811faf8daa316c2ce8e79',
            'parent-j-error-impact/analysis-v1/result.json': '748b359617096b93f9b60aa1ad3be05b9d2aa57244d0cef26067d02929ecac5f',
            'parent-j-stage-localization/preparation.json': '077b972b1ea43bbf0472a7dcda5e3bbe89f964a583ee6ea2f34282c32b806c73',
            'parent-j-stage-localization/independent-root-review.json': '1e4e34875a0a160a09569fe002426ee250e7b1a7a7a7b779d548d2ec961cb3f5',
            'parent-j-stage-localization/run-v1/result.json': '290093ea73cfbc27da90321c9d47fdacd62ea0bc44aad508949906963250aeba',
            'parent-j-stage-localization/run-v1/launch-result.json': '6c7ce531a0f06fd8e2a4cf643be2f69a68b6a1cfc7356709016d8da3e16b7344',
            'boundary/copper-phosphate-transport/DECISION.json': '803b1979d22fb1d4fed3a8713fe5df046b7fa335fa2ecce60b2876d41257e8e5',
            'boundary/hollow-silicalite-followup/ROOT_REVIEW.json': 'c3f9baad1897b1994ca3df288e59a4bb5c4b2cba991d9a6332199aba65eb43f9',
            'identity/beta-vmo7-discriminator/ROOT_REVIEW.json': '08d497341e0c32dbc7f9aff64662a871d6d611c55f030fec81213aff4fb488ba'}.items():
        assert source_hashes['recursive-compound-2026-10-15/' + name] == digest
    for name, digest in {
            'parent-metric-solve-diagnostic/run.py': 'e4cb38e887346231bb159d99279c1bb4d951ca0e769ea6565d50408849489212',
            'parent-metric-solve-diagnostic-v2/independent-root-review.json': 'd86da87a208cc8b76e5fb71c7193921242dcfc984eb612f86122c264603e3b62',
            'parent-metric-solve-diagnostic-v2/run-v1/launch-result.json': '99a6d164abd220703824deb93662a7cc0415966be52a26b5536a54d79f0c8810',
            'parent-metric-solve-diagnostic-v2/postmortem/result.json': 'daa3a11b0fdeaa6cd226255d3ec05acd87ecc83ce42e9c5fe0330effe4d312c3',
            'parent-blas-control-audit/verification.json': '19867b0620af103a0508da6497b935ba1ecb0e4f533ef341866c18b87c4cc9cb',
            'parent-saved-metric-solve/run.py': '3d95774ea1b1e18ea155284b632dee58d07b31a0eb62e8c0dbac3ab6e4b61a8b',
            'parent-saved-metric-solve/preparation.json': '75aae4c3937ccfd774246a10be98661ad848df2edc349a0b54df17267361c99f',
            'parent-saved-metric-solve/qualification.json': '7bf4f765d428a445399aa71f637d87e7dde6231374d963e9e209a0be5340896a',
            'boundary/hollow-silicalite-followup/wetting-constraint/ROOT_REVIEW.json': 'ab7e331bab39501211b41b62da80dbaae36309c012287da49b4e275948c28f88',
            'identity/concentration-speciation-followup/ROOT_REVIEW.json': '353cc3ce4a006086b85ed47b93c191a2e54e69f1bc5cb2d77a0e722071133711',
            'parent-metric-solve-diagnostic/preparation.json': 'd39a9309180d2406eba32c91be45292eb8e789c68070de4062f900aaf3b6e7a4',
            'parent-metric-solve-diagnostic/independent-root-review.json': '284b9b707fbcb799efe2d0deb071205ae4cf8e6408ecd6def4c0dfd806d6b9a0',
            'parent-metric-solve-diagnostic/run-v1/launch-result.json': '6da6d27fb1752be0db3ed6e7ac8ee955d3184146758bc16157069f2779787c5f',
            'parent-metric-solve-diagnostic-v2/run.py': 'c838f96be1270691bf8a0022d28c9c3a239eb0785850b9d414ffd7df9ad87776',
            'parent-metric-solve-diagnostic-v2/preparation.json': '876d9901607cbe588636bacffafc8f66e8683df10dc3d27764853054a1c6076b',
            'parent-metric-solve-diagnostic-v2/qualification.json': 'fccd60bc3b721720a8121c893d914381f581b25222586d056d1148d66e1e54b3',
            'parent-metric-solve-diagnostic-v2/qualification-failed-v1.json': '95c6e8632e277641e0acb56c6a18734b4d0077570829ca0fc5a82f0a66999009',
            'parent-metric-solve-diagnostic-v2/metadata-probe.json': 'e1151d1bfb58969ba908337a463b033c31e0ed2cd94a85ce6919b384f813236d',
            'parent-metric-solve-diagnostic-v2/ordering-probe.json': '00509989dec1e7245edb34ac0e1ad614b6cb61b086d0a8379f6f26b81e324e92',
            'boundary/aqueous-pom-nanofiltration-followup/evidence.json': 'f0a078125641d6a395a8abc433f114e57ac78959407573c8954ccd28709914f4',
            'boundary/aqueous-pom-nanofiltration-followup/extracted-results.json': 'd87aff4510136de06830951259de5a322a6ffdc78da5c69ebe6ad36cc749aaf1',
            'boundary/aqueous-pom-nanofiltration-followup/main-table-results.json': 'f678db15da8fa2246e887a3fd755c99a2fadd9a0f5b3ac611dc84c7604f3d776',
            'boundary/aqueous-pom-nanofiltration-followup/extract_and_check.py': '15d72134896cb39ea0978ae57f97e237ce12ff51021e961bfc84c4212c3f071d'}.items():
        assert source_hashes['recursive-compound-2026-10-15/' + name] == digest

    for name, digest in {
            'parent-saved-metric-solve/independent-root-review.json': '03769aabaf813daa6cd66219c208e6525a32a86bfb0a99b069b0766d88489aed',
            'parent-saved-metric-solve/run-v1/launch-result.json': '1b12b619c3491182c6eb0e8dfb557905e1c73c2afda12c5c3e477ae20e88a730',
            'parent-saved-metric-solve/run-v1/result.json': '6f4f2b4e2755d9dbba32242dc8cef5420d77a94280a7e15c0b37254b205cb22a',
            'parent-explicit-blas-j/preparation.json': '13cf6df31ebf08fd49d873e96d77843dd1df4cbe8e4039488a0376bf0d90d51e',
            'parent-explicit-blas-j/qualification.json': '1e1a757e739a5605b925605285477173db475018035eeb3977a52b4fd22cd85a',
            'parent-explicit-blas-j/test_run.py': '9de6d3b5767dd37416bca777d2eb5037896bc36db21e4f25185b0d6b6ffefb4c',
            'parent-explicit-blas-j/run.py': 'b7f2ee113dab465dcf8528b6a80020f098ee17fa6f9b09efb4c81fef4e085beb',
            'identity/competing-mov-speciation/ACCESS_FOLLOWUP_2026-10-16.md': '871dc24fddfd0fa6a2e684fd3c299109915d1e8a62309311d2e1f075374aaa00',
    }.items():
        assert source_hashes['recursive-compound-2026-10-15/' + name] == digest


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1])))
