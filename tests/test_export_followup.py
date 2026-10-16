import sys
import unittest
import contextlib
import hashlib
import io
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import build_archive as archive
from export_followup import LABS, exclusion, export, strip_signed_urls
from verify_followup import (verify_memory_followup, verify_openmp_renewal,
                             verify_parent_pilot_source_bindings, verify_stage_artifact_bindings)


class PublicationSelection(unittest.TestCase):
    def test_measurement_access_failure_payload_stays_excluded(self):
        base = Path('recursive-compound-2026-10-15/identity/measurement-integrity-followup')
        for name in ('raw/poster-response.body', 'raw/poster.headers'):
            self.assertTrue(exclusion(base / name))
        for name in ('REPORT.md', 'acquisition.json', 'ROOT_REVIEW.json', 'INDEPENDENT_REVIEW.md'):
            self.assertIsNone(exclusion(base / name))

    def test_blas_upstream_readme_is_acquired_source(self):
        base = Path('recursive-compound-2026-10-15/parent-blas-control-audit')
        self.assertTrue(exclusion(base / 'sources', directory=True))
        for name in ('README.md', 'blas_server_omp.c', 'cblas.h'):
            self.assertTrue(exclusion(base / 'sources' / name))
        for name in ('REPORT.md', 'verification.json', 'observed.json'):
            self.assertIsNone(exclusion(base / name))

    def test_oversize_metric_exception_is_exact_and_keeps_receipts(self):
        base = Path('recursive-compound-2026-10-15/parent-metric-solve-diagnostic-v2')
        self.assertIn('3077044480-byte', exclusion(base / 'run-v1/original_metric.npy'))
        for name in ('run-v1/launch-result.json', 'postmortem/result.json', 'run-v2/original_metric.npy', 'run-v1/other.npy'):
            self.assertIsNone(exclusion(base / name))

    @classmethod
    def setUpClass(cls):
        archive.GROUPS.update(LABS)

    def test_normalized_observations_remain(self):
        self.assertIsNone(exclusion(Path('rna-mechanism-2026-10-15/sources/salibi/observations.csv')))

    def test_downloaded_source_data_excluded(self):
        self.assertTrue(exclusion(Path('noncarbon-discovery-2026-10-15/database/raw/data.json')))

    def test_copied_database_rows_excluded(self):
        self.assertTrue(exclusion(Path('noncarbon-discovery-2026-10-15/database/results-v1/selected_source_records.json')))

    def test_acquired_author_code_excluded(self):
        self.assertTrue(exclusion(Path('measured-coupling-2026-10-15/droplet_sources/author/model.py')))

    def test_negative_audit_retained(self):
        self.assertIsNone(exclusion(Path('rna-seed-transport-2026-10-15/independent/campaign-v1/checks.json')))

    def test_openmp_dependencies_excluded_at_subtree_boundary(self):
        base = Path('recursive-compound-2026-10-15/parent-openmp')
        for name in ('env', 'env-aligned', 'env-future', 'pkgs', 'cache', 'tmp', 'bin'):
            with self.subTest(name=name):
                self.assertTrue(exclusion(base / name, directory=True))
                self.assertTrue(exclusion(base / name / 'metadata.json'))
        for name in ('conda-pyscf-metadata.json', 'micromamba.tar.bz2'):
            self.assertTrue(exclusion(base / name))
        for name in ('ALIGNED_REPORT.md', 'guard-aligned.py', 'probe-aligned.py',
                     'aligned-install-receipt.json', 'aligned-source-binary-pins.json',
                     'aligned-probe-result.json', 'bootstrap.json'):
            self.assertIsNone(exclusion(base / name))

    def test_renewal_sources_excluded_and_authored_constraints_retained(self):
        base = Path('recursive-compound-2026-10-15/renewal')
        for folder in ('copI-source', 'mo-blue-route', 'oxide-isotope-constraints',
                       'manganese-regeneration-constraints', 'receiver-function-audit'):
            for name in ('raw/ja900023k_si_001.pdf', 'raw/ja3c09344_si_001.pdf',
                         'raw/figshare-2869057.json', 'si-text.txt'):
                self.assertTrue(exclusion(base / folder / name))
            for name in ('REPORT.md', 'analysis.json', 'audit.py', 'SOURCES.json'):
                self.assertIsNone(exclusion(base / folder / name))

    def test_export_prunes_runtime_trees_and_keeps_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, output = Path(temporary) / 'source', Path(temporary) / 'published'
            for lab in LABS:
                (source / lab).mkdir(parents=True)
            base = Path('recursive-compound-2026-10-15')
            runtime = base / 'parent-openmp/env-aligned'
            (source / runtime).mkdir(parents=True)
            (source / runtime / 'metadata.json').write_text('{invalid dependency payload')
            failure = base / 'parent-openmp-qualification/run-v1/result.json'
            (source / failure).parent.mkdir(parents=True)
            (source / failure).write_text('{"status":"FAIL"}')
            with contextlib.redirect_stdout(io.StringIO()):
                export(source, output)
            self.assertFalse((output / runtime).exists())
            self.assertEqual(json.loads((output / failure).read_text()), {'status': 'FAIL'})
            records = json.loads((output / 'manifest.json').read_text())['files']
            record = next(r for r in records if r['path'] == str(runtime))
            self.assertEqual((record['status'], record['scope']), ('excluded', 'subtree'))

    def test_signed_boundary_export_keeps_authored_evidence_and_excludes_raw(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, output = Path(temporary) / 'source', Path(temporary) / 'published'
            for lab in LABS:
                (source / lab).mkdir(parents=True)
            base = Path('recursive-compound-2026-10-15')
            kept = (base / 'parent-signed-j-diagnostic/preparation.json',
                    base / 'parent-j-repeatability/run-v1/J1.npy',
                    base / 'parent-j-stage-localization/preparation.json',
                    base / 'parent-j-error-impact/preparation.json',
                    base / 'boundary/copper-phosphate-transport/evidence.json',
                    base / 'boundary/acidic-nanofiltration/evidence.json',
                    base / 'identity/mov9-independent-assay-followup/acquisition.json')
            excluded = (base / 'boundary/acidic-nanofiltration/raw/article.pdf',
                        base / 'parent-j-repeatability/run-v1/post-call-1.bin',
                        base / 'boundary/copper-phosphate-transport/raw/rauscher2018.pdf',
                        base / 'boundary/copper-phosphate-transport/raw/rauscher2018.txt',
                        base / 'boundary/copper-phosphate-transport/raw/page-2.png',
                        base / 'boundary/acidic-nanofiltration/raw/page.png',
                        base / 'identity/mov9-independent-assay-followup/raw/route03-si-tool-response.txt',
                        base / 'parent-openmp/env-aligned/lib/runtime.bin')
            for path in kept + excluded:
                (source / path).parent.mkdir(parents=True, exist_ok=True)
                (source / path).write_text('{}')
            with contextlib.redirect_stdout(io.StringIO()):
                export(source, output)
            for path in kept:
                self.assertEqual((output / path).read_text(), '{}')
            for path in excluded:
                self.assertFalse((output / path).exists())

    def test_historical_model_retained(self):
        self.assertIsNone(exclusion(Path('rna-turnover-tests-2026-10-15/results-v1/frozen/model.py')))

    def test_scientific_evidence_retained(self):
        self.assertIsNone(exclusion(Path('measured-coupling-2026-10-15/droplet_model/.omo/evidence/run-v1/frozen/model.py')))

    def test_normalized_inheritance_retained(self):
        self.assertIsNone(exclusion(Path('rna-mechanism-2026-10-15/sources/inheritance/normalized/ameta_droplet_umis.csv')))

    def test_retention_verification_retained(self):
        self.assertIsNone(exclusion(Path('rna-mechanism-2026-10-15/sources/retention/.omo/evidence/verification.json')))

    def test_parent_coordinates_retained_but_raw_coordinates_excluded(self):
        self.assertIsNone(exclusion(Path('recursive-compound-2026-10-15/parent-inputs/P0_A.xyz')))
        self.assertIsNone(exclusion(Path('recursive-compound-2026-10-15/identity/parent_heavy.xyz')))
        self.assertTrue(exclusion(Path('recursive-compound-2026-10-15/raw/source.xyz')))

    def test_published_parent_acquisitions_excluded_and_analysis_retained(self):
        base = Path('recursive-compound-2026-10-15/published-parent')
        for name in ('item.html', 'parent32.xyz', 'geometry.cml', 'output.cml',
                     'Mo36O128-32H.in', 'petrus2021-si.pdf', 'petrus2021-si.txt'):
            with self.subTest(name=name):
                self.assertTrue(exclusion(base / name))
        for name in ('analysis.py', 'analysis.json', 'provenance.json', 'comparison.md'):
            with self.subTest(name=name):
                self.assertIsNone(exclusion(base / name))

    def test_parent_failures_and_solution_assessments_retained(self):
        base = Path('recursive-compound-2026-10-15')
        for name in ('parent-pilot/run-v1/preflight.json',
                     'parent-pilot-blocked/run-v1/supervisor.json',
                     'parent-pilot-blocked/run-v1/stages.jsonl',
                     'solution-constraints/sources.json',
                     'boundary/nd-linker-proposition.json'):
            with self.subTest(name=name):
                self.assertIsNone(exclusion(base / name))
        self.assertTrue(exclusion(base / 'solution-constraints/raw/izarova2005-crossref.json'))

    def test_signed_query_removed_without_touching_stable_query(self):
        text = '"https://example.org/file?Expires=1&Signature=private&Key-Pair-Id=key" https://example.org/?id=2'
        cleaned, count = strip_signed_urls(text)
        self.assertEqual(cleaned, '"https://example.org/file" https://example.org/?id=2')
        self.assertEqual(count, 1)

    def test_jkfit_and_memory_evidence_retained_without_raw_acquisitions(self):
        base = Path('recursive-compound-2026-10-15')
        retained = (
            'rij-qualification/run-v1/result.json',
            'rij-qualification-v2/run-v1/neutral-water/result.json',
            'rij-jkfit-qualification/evidence/preparation-pending.json',
            'rij-jkfit-qualification/preparation.json',
            'rij-jkfit-qualification/SOURCE.md',
            'rij-jkfit-qualification/run-v1/new-external/result.json',
            'rij-jkfit-qualification/run-v1/new-external/arrays.npz',
            'cpcm-rij-memory/allocation.json',
            'cpcm-rij-memory/evidence/observations.json',
            'cpcm-rij-memory-qualification/preparation.json',
            'cpcm-rij-memory-qualification/run-v1/result.json',
            'cpcm-rij-memory-qualification/run-v1/scf-new-external/result.json',
            'energy/silicotungstate-20/assessment.json',
            'parent-pilot-memory/preparation.json',
            'parent-pilot-memory/run-v1/launch-result.json',
            'parent-pilot-memory/run-v1/stages.jsonl',
            'wv-method-qualification/preparation.json',
            'wv-method-qualification/run-v1/result.json',
            'wv-method-qualification/run-v1/WO4/result.json',
            'wv-method-qualification/run-v1/VO4/supervisor.json',
            'parent-pilot-memory/THREAD_DIAGNOSTIC.md',
            'renewal/fe-feed-21/assessment.json',
            'renewal/fe-feed-21/analysis.json',
            'renewal/fe-feed-21/source-data-inventory.json')
        for name in retained:
            with self.subTest(name=name):
                self.assertIsNone(exclusion(base / name))
        for name in ('new-case.json', 'new.xyz', 'new.in', 'new-output.cml'):
            with self.subTest(name=name):
                self.assertTrue(exclusion(base / 'rij-jkfit-qualification/raw' / name))
        self.assertTrue(exclusion(base / 'cpcm-rij-memory/evidence/chunk-mutation-control.txt'))

    def test_export_retains_embedded_provenance_and_original_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, output = Path(temporary) / 'source', Path(temporary) / 'published'
            for lab in LABS:
                (source / lab).mkdir(parents=True)
            base = Path('recursive-compound-2026-10-15')
            failure = base / 'rij-qualification-v2/run-v1/result.json'
            result = base / 'rij-jkfit-qualification/run-v1/new-external/result.json'
            raw = base / 'rij-jkfit-qualification/raw/new-case.json'
            provenance = {'item_url': 'https://example.org/source',
                          'validation_scope': 'computational geometry only'}
            payloads = {
                failure: {'status': 'FAIL_NUMERICAL_SCREEN', 'physical_admission': False},
                result: {'status': 'PASS_NUMERICAL_SCREEN_ONLY', 'physical_admission': False,
                         'new_external_source': provenance},
                raw: provenance}
            for rel, data in payloads.items():
                (source / rel).parent.mkdir(parents=True, exist_ok=True)
                (source / rel).write_text(json.dumps(data))
            with contextlib.redirect_stdout(io.StringIO()):
                export(source, output)
            for rel in (failure, result):
                self.assertEqual(json.loads((output / rel).read_text()), payloads[rel])
            self.assertFalse((output / raw).exists())
            self.assertEqual(json.loads((source / raw).read_text()), provenance)
            manifest = json.loads((output / 'manifest.json').read_text())
            records = {record['path']: record for record in manifest['files']}
            self.assertEqual(manifest['included_files'], 2)
            self.assertEqual(records[str(raw)]['status'], 'excluded')

    def test_url_pattern_in_source_code_is_not_parsed_as_address(self):
        text = 'https://[example-pattern]'
        self.assertEqual(strip_signed_urls(text), (text, 0))

    def test_export_preserves_source_and_tracks_sanitized_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, output = Path(temporary) / 'source', Path(temporary) / 'published'
            for lab in LABS:
                (source / lab).mkdir(parents=True)
            rel = Path(LABS[2]) / 'acquisition.json'
            raw = b'{"url":"https://example.org/file?Signature=private"}\r\n'
            (source / rel).write_bytes(raw)
            with contextlib.redirect_stdout(io.StringIO()):
                export(source, output)
            record = json.loads((output / 'manifest.json').read_text())['files'][0]
            self.assertEqual((source / rel).read_bytes(), raw)
            self.assertEqual((output / rel).read_bytes(), b'{"url":"https://example.org/file"}\n')
            self.assertEqual(record['source_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(record['published_sha256'], hashlib.sha256((output / rel).read_bytes()).hexdigest())
            with self.assertRaises(ValueError):
                export(source, output)

    def test_coordinates_are_sanitized_and_manifested_as_text(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, output = Path(temporary) / 'source', Path(temporary) / 'published'
            for lab in LABS:
                (source / lab).mkdir(parents=True)
            rel = Path('recursive-compound-2026-10-15/parent-inputs/P0_A.xyz')
            (source / rel).parent.mkdir()
            raw = '1\n/Users/example/model.xyz\nH 0 0 0\n'
            (source / rel).write_text(raw)
            with contextlib.redirect_stdout(io.StringIO()):
                export(source, output)
            self.assertEqual((source / rel).read_text(), raw)
            self.assertEqual((output / rel).read_text(), '1\n/USER_HOME/model.xyz\nH 0 0 0\n')
            manifest = json.loads((output / 'manifest.json').read_text())
            self.assertEqual(manifest['included_files'], 1)
            self.assertEqual(manifest['files'][0]['published_sha256'],
                             hashlib.sha256((output / rel).read_bytes()).hexdigest())


class OpenMPRenewalVerification(unittest.TestCase):
    case_names = {'anion-water', 'neutral-water', 'anion-eps1', 'heldout-Mo2O7', 'new-external'}

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.recursive = Path(temporary.name)
        source = (Path(__file__).resolve().parents[1] / 'research/2026-10-15'
                  / 'recursive-compound-2026-10-15')
        for folder in ('renewal/copI-source', 'renewal/mo-blue-route',
                       'renewal/oxide-isotope-constraints', 'renewal/manganese-regeneration-constraints',
                       'renewal/receiver-function-audit', 'identity/mixed-addenda-source-audit',
                       'parent-openmp-qualification', 'parent-openmp-qualification-v2',
                       'parent-openmp-first-j', 'parent-openmp-first-j-v2', 'parent-saved-j-qualification',
                       'parent-saved-j-pilot', 'identity/moussawi-occupancy-followup',
                       'identity/vanadium-incorporation-followup', 'identity/competing-mov-speciation',
                       'identity/next-step/pcm-heldout-selection', 'parent-saved-j-crash-diagnostic',
                       'identity/competing-mov-primary-followup', 'parent-signed-j-diagnostic',
                       'boundary/acidic-nanofiltration', 'identity/mov9-independent-assay-followup',
                       'boundary/pom-polyoxocation-23', 'boundary/tube-alternative-followup',
                       'boundary/phosphate-transport-lead', 'parent-j-repeatability',
                       'parent-j-error-impact', 'parent-j-stage-localization', 'boundary/copper-phosphate-transport',
                       'boundary/hollow-silicalite-followup', 'identity/beta-vmo7-discriminator',
                       'parent-metric-solve-diagnostic', 'parent-metric-solve-diagnostic-v2',
                       'boundary/aqueous-pom-nanofiltration-followup', 'parent-blas-control-audit',
                       'parent-saved-metric-solve', 'parent-explicit-blas-j', 'identity/concentration-speciation-followup',
                       'explicit-blas-accuracy-qualification', 'identity/measurement-integrity-followup'):
            self.assertTrue((source / folder).is_dir(), folder)
            for path in (source / folder).rglob('*'):
                if path.is_file() and path.suffix in ('.json', '.jsonl', '.py', '.md', '.csv'):
                    target = self.recursive / path.relative_to(source)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())
        design = Path('boundary/active-retention-identifiability.md')
        (self.recursive / design).write_bytes((source / design).read_bytes())

    def test_failures_qualified_runtime_and_first_j_scope_are_preserved(self):
        verify_openmp_renewal(self.recursive, self.case_names)

    def test_admission_and_result_mutations_are_rejected(self):
        mutations = (
            ('parent-metric-solve-diagnostic-v2/run-v1/launch-result.json', 'completed', True),
            ('parent-metric-solve-diagnostic-v2/postmortem/result.json', 'root_cause_established', True),
            ('parent-metric-solve-diagnostic-v2/postmortem/result.json', ('terminal_artifacts_verified', 'original_metric.npy'), '0' * 64),
            ('parent-metric-solve-diagnostic-v2/postmortem/result.json', ('saved_metric', 'positive_definiteness_established'), True),
            ('parent-blas-control-audit/observed.json', ('states', 0, 'blas'), 1),
            ('parent-blas-control-audit/verification.json', 'failed_setup_attempts_preserved', 0),
            ('parent-saved-metric-solve/qualification.json', 'parent_native_execution', True),
            ('parent-saved-metric-solve/run-v1/result.json', 'status', 'PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW'),
            ('parent-saved-metric-solve/run-v1/result.json', ('comparisons', 'A2', 'exact_equal'), False),
            ('parent-saved-metric-solve/run-v1/result.json', ('condition', 'certified_bound'), True),
            ('parent-saved-metric-solve/run-v1/result.json', 'factor_matches_prior', True),
            ('parent-saved-metric-solve/run-v1/result.json', 'physical_admission', True),
            ('parent-saved-metric-solve/run-v1/result.json', 'parent_SCF_readiness', True),
            ('parent-saved-metric-solve/run-v1/launch-result.json', 'completed', False),
            ('parent-saved-metric-solve/run-v1/launch-result.json', ('artifact_hashes', 'rho_A2.npy'), '0' * 64),
            ('parent-saved-metric-solve/run-v1/launch-result.json', 'artifact_hashes', {}),
            ('parent-explicit-blas-j/preparation.json', 'pins', {}),
            ('parent-explicit-blas-j/qualification.json', 'native_parent_calls', 1),
            ('parent-explicit-blas-j/qualification.json', 'tests_run', 7),
            ('parent-explicit-blas-j/preparation.json', 'physical_admission', True),
            ('parent-explicit-blas-j/run-v1/launch-result.json', 'completed', False),
            ('parent-explicit-blas-j/run-v1/launch-result.json', 'gate_unchanged', False),
            ('parent-explicit-blas-j/run-v1/result.json', 'J_calls', 3),
            ('parent-explicit-blas-j/run-v1/result.json', 'SCFs', 1),
            ('parent-explicit-blas-j/run-v1/result.json', 'held_out_validation', True),
            ('parent-explicit-blas-j/run-v1/result.json', 'physical_admission', True),
            ('parent-explicit-blas-j/run-v1/result.json', 'parent_SCF_readiness', True),
            ('parent-explicit-blas-j/run-v1/threads-before_J_A.json', 'blas', 4),
            ('parent-explicit-blas-j/run-v1/call-A.json', ('capture', 'ordinary_returned_unchanged'), False),
            ('parent-explicit-blas-j/run-v1/metric-before-factor.json', 'causal_comparison_established', True),
            ('explicit-blas-accuracy-qualification/PREREQUISITE_STATUS.json', 'qualification_launched', True),
            ('explicit-blas-accuracy-qualification/PREREQUISITE_STATUS.json', 'reserved_HMo2O7_operator_or_SCF_use', True),
            ('explicit-blas-accuracy-qualification/PREREQUISITE_STATUS.json', 'parent_repeat_pass', True),
            ('identity/measurement-integrity-followup/ROOT_REVIEW.json', 'verified_integrated_complement_admissions', 1),
            ('identity/measurement-integrity-followup/ROOT_REVIEW.json', 'rates_fitted', True),
            ('identity/measurement-integrity-followup/acquisition.json', 'quantitative_raw_dataset_acquired', True),
            ('identity/measurement-integrity-followup/acquisition.json', ('root_observations', 5, 'pdf_magic'), True),
            ('identity/concentration-speciation-followup/evidence.json', 'target_tested', True),
            ('boundary/hollow-silicalite-followup/wetting-constraint/ROOT_REVIEW.json', 'physical_target_tested', True),
            ('parent-metric-solve-diagnostic/run-v1/launch-result.json', 'completed', True),
            ('parent-metric-solve-diagnostic-v2/preparation.json', 'physical_admission', True),
            ('parent-metric-solve-diagnostic-v2/qualification.json', 'native_parent_integrals', 1),
            ('parent-metric-solve-diagnostic-v2/qualification-failed-v1.json', 'passed', True),
            ('parent-metric-solve-diagnostic-v2/metadata-probe.json', 'native_integral_calls', 1),
            ('parent-metric-solve-diagnostic-v2/ordering-probe.json', ('permutations', 0, 'parent_match'), True),
            ('boundary/aqueous-pom-nanofiltration-followup/evidence.json', 'complement_admissions', 1),
            ('boundary/aqueous-pom-nanofiltration-followup/evidence.json', 'held_out_validation', True),
            ('boundary/aqueous-pom-nanofiltration-followup/evidence.json', 'functional_inheritance_observed', True),
            ('boundary/aqueous-pom-nanofiltration-followup/evidence.json', 'fitted_parameters', [0.99]),
            ('boundary/aqueous-pom-nanofiltration-followup/extracted-results.json',
             ('table3_ratio_checks', 0, 'joint_exact_reported_ratio', 'compatible_with_closed_envelope'), True),
            ('boundary/aqueous-pom-nanofiltration-followup/extracted-results.json',
             ('supplement', 'table_s8_concentration_mM'), 5),
            ('boundary/aqueous-pom-nanofiltration-followup/extracted-results.json',
             ('supplement', 'table_s8_source_rows', 0, 2), '99'),
            ('boundary/aqueous-pom-nanofiltration-followup/extracted-results.json',
             ('supplement', 'table_s8_stats', 'permeate_flux_L_m2_h', 'sample_variance_exact'), '16'),
            ('renewal/copI-source/assessment.json', 'admitted_to_assembly', True),
            ('renewal/copI-source/assessment.json', 'retained_founder_organization_fraction', 0.98),
            ('renewal/mo-blue-route/analysis.json', 'experimental_holdout', True),
            ('renewal/mo-blue-route/analysis.json',
             ('raman_normalization', 'absolute_species_mass_balance_identified'), True),
            ('parent-openmp-qualification/run-v1/result.json', 'status', 'PASS'),
            ('parent-openmp-qualification/run-v1/phase1-gate.json', 'SCFs_launched', 1),
            ('parent-openmp-qualification/run-v1/threads-1/run-v1/operators-WO4/result.json',
             'runtime_guard_pass', True),
            ('parent-openmp-qualification/run-v1/threads-4/run-v1/operators-VO4/result.json',
             ('checks', 0, 'pass'), False),
            ('parent-openmp-qualification-v2/run-v1/result.json', 'phase2_skipped', True),
            ('parent-openmp-qualification-v2/run-v1/result.json', 'fresh_holdout', True),
            ('parent-openmp-qualification-v2/run-v1/threads-4/run-v1/operators-WO4/result.json',
             'runtime_guard_pass', False),
            ('parent-openmp-qualification-v2/run-v1/threads-4/run-v1/scf-new-external/result.json',
             ('checks', 0, 'pass'), False),
            ('parent-openmp-qualification-v2/run-v1/threads-4/run-v1/scf-new-external/result.json',
             ('SCF', 'converged'), False),
            ('parent-openmp-first-j/preparation.json', 'J_calls', 1),
            ('parent-openmp-first-j/run-v1/launch-result.json', 'status', 'PASS_BOUNDED_FIRST_J_ONLY'),
            ('parent-openmp-first-j-v2/run-v1/launch-result.json', 'gate_unchanged', False),
            ('parent-openmp-first-j-v2/run-v1/launch-result.json', 'parent_SCF_readiness', True),
            ('parent-openmp-first-j-v2/run-v1/launch-result.json', 'J_sha256_observed', '0' * 64),
            ('parent-saved-j-qualification/run-v1/launch-result.json', 'status', 'PASS_PARENT_SCF'),
            ('parent-saved-j-qualification/run-v1/launch-result.json', 'physical_admission', True),
            ('parent-saved-j-qualification/run-v1/launch-result.json', 'fresh_holdout', True),
            ('parent-saved-j-qualification/run-v1/operator-receipt.json', 'returncode', 1),
            ('identity/moussawi-occupancy-followup/evidence.json', 'nominal_target_verified', True),
            ('identity/moussawi-occupancy-followup/evidence.json', ('exact_missing_fields', 'refined_site_occupancy'), 1),
            ('parent-saved-j-pilot/STATUS.json', 'status', 'QUALIFIED'),
            ('parent-saved-j-pilot/STATUS.json', 'execution_clearance', True),
            ('parent-saved-j-pilot/STATUS.json', 'unit_tests_run', 1),
            ('parent-saved-j-pilot/STATUS.json', 'SCFs_launched', 0),
            ('parent-saved-j-pilot/STATUS.json', 'physical_admission', True),
            ('parent-saved-j-pilot/run-v1/launch-result.json', 'status', 'PASS'),
            ('parent-saved-j-pilot/run-v1/launch-result.json', 'required_evidence_present', True),
            ('parent-saved-j-pilot/run-v1/supervisor.json', 'returncode', 0),
            ('identity/competing-mov-speciation/evidence.json', 'accepted_primary_mov_calibration_rows', [{'value': 60.37}]),
            ('identity/competing-mov-speciation/evidence.json', ('reproduced_numeric_leads', 0, 'calibration_eligible'), True),
            ('identity/next-step/pcm-heldout-selection/selection.json', 'numerical_qualification_pass', True),
            ('identity/next-step/pcm-heldout-selection/selection.json', 'scientific_operators_evaluated', 1),
            ('parent-saved-j-crash-diagnostic/crash-excerpt.json', 'root_cause_identified', True),
            ('parent-saved-j-crash-diagnostic/crash-excerpt.json', 'scientific_operators_evaluated', 1),
            ('parent-saved-j-crash-diagnostic/crash-excerpt.json', 'SCFs_launched', 1),
            ('parent-signed-j-diagnostic/preparation.json', 'operators_executed', 2),
            ('parent-signed-j-diagnostic/preparation.json', 'SCFs_launched', 1),
            ('parent-signed-j-diagnostic/preparation.json', 'physical_admission', True),
            ('parent-signed-j-diagnostic/preparation.json', 'absolute_tolerance', 1e-9),
            ('parent-signed-j-diagnostic/run-v1/first-checks.json', 'sign_pass', True),
            ('parent-signed-j-diagnostic/run-v1/first-checks.json', 'max_sign_error', 0),
            ('parent-signed-j-diagnostic/run-v1/launch-result.json', 'status', 'PASS'),
            ('parent-signed-j-diagnostic/run-v1/launch-result.json', 'parent_SCF_readiness', True),
            ('boundary/pom-polyoxocation-23/DECISION.json', 'verified_integrated_member', True),
            ('boundary/pom-polyoxocation-23/DECISION.json', 'aggregate_verified_integrated_complements', 1),
            ('boundary/pom-polyoxocation-23/DECISION.json', 'heldout_target_validations', 1),
            ('boundary/pom-polyoxocation-23/assessment.json', ('joint_target_requirements', 'recovery_denominator'), 'feed amount'),
            ('parent-j-repeatability/preparation.json', 'sequence', [1, -1, 1]),
            ('parent-j-repeatability/preparation.json', 'absolute_tolerance', 1e-9),
            ('parent-j-repeatability/independent-root-review.json', 'sign_and_call_order_confounded', False),
            ('parent-j-repeatability/preparation-history/pre-setup-order.json', 'SCFs_launched', 1),
            ('parent-j-repeatability/run-v1/comparisons.json', ('comparisons', 'J2-J1', 'pass'), True),
            ('parent-j-repeatability/run-v1/comparisons.json', ('comparisons', 'J2-J1', 'absolute_tolerance'), 1e-9),
            ('parent-j-repeatability/run-v1/comparisons.json', 'external_reference_is_independent_algorithm', True),
            ('parent-j-repeatability/run-v1/launch-result.json', ('artifacts', 'sha256', 'J1.npy'), '0' * 64),
            ('boundary/pom-polyoxocation-23/charge-followup.json', ('decision', 'charge_gap_resolved'), True),
            ('boundary/pom-polyoxocation-23/charge-followup.json', ('conditional_arithmetic', 'observed_six_electron_oxidation'), True),
            ('boundary/tube-alternative-followup/evidence.json', ('primary_sources', 0, 'carbon_free_active_wall_supported'), True),
            ('boundary/tube-alternative-followup/evidence.json', ('unresolved_lead', 'permeability'), 0.1),
            ('boundary/phosphate-transport-lead/evidence.json', ('target_evidence', 'heldout_validation'), True),
            ('boundary/phosphate-transport-lead/evidence.json', ('cited_transport_source', 'numeric_permeability'), 0.1),
            ('parent-j-error-impact/preparation.json', 'real_arrays_analyzed', True),
            ('parent-j-stage-localization/preparation.json', 'operators_executed', 3),
            ('parent-j-stage-localization/preparation.json', 'J_absolute_tolerance', 1e-9),
            ('boundary/copper-phosphate-transport/evidence.json', ('constraints', 'solute_permeability'), 0.1),
            ('boundary/copper-phosphate-transport/evidence.json', ('constraints', 'growth_regression_slope', 'pointwise_ratio_equivalence_established'), True),
            ('boundary/copper-phosphate-transport/evidence.json', ('decision_boundary', 'integrated_admission'), True),
            ('boundary/copper-phosphate-transport/evidence.json', ('decision_boundary', 'universal_acidic_wall_failure_proven'), True),
            ('boundary/copper-phosphate-transport/evidence.json', ('work_scope', 'heldout_target_validations'), 1),
            ('boundary/copper-phosphate-transport/DECISION.json', 'aggregate_verified_integrated_complements', 1),
            ('boundary/copper-phosphate-transport/DECISION.json', 'growth_regression_identifies_target_transport', True),
            ('boundary/hollow-silicalite-followup/evidence.json', ('target_parameters', 'active_retention_fraction'), 0.89),
            ('boundary/hollow-silicalite-followup/ROOT_REVIEW.json', 'new_candidate_roles', 1),
            ('boundary/hollow-silicalite-followup/ROOT_REVIEW.json', 'heldout_target_validation', True),
            ('identity/beta-vmo7-discriminator/evidence.json', ('target_parameters', 'aqueous_target_fraction'), 0.95),
            ('identity/beta-vmo7-discriminator/evidence.json', ('unresolved_source_conflicts', 'NaCl', 'adopted_value'), 0.5),
            ('identity/beta-vmo7-discriminator/ROOT_REVIEW.json', 'physical_target_tested', True),
            ('parent-j-error-impact/analysis-v1/result.json', 'parent_SCF_readiness', True),
            ('parent-j-error-impact/analysis-v1/result.json', 'original_nonpasses', 0),
            ('parent-j-error-impact/analysis-v1/result.json', 'operators_executed', 1),
            ('parent-j-stage-localization/run-v1/call-C.json', 'ordinary_J_P0', True),
            ('parent-j-stage-localization/saved-vector-sensitivity.json', 'scope', 'Certified condition number'),
            ('boundary/acidic-nanofiltration/evidence.json', ('decision', 'heldout_validation'), True),
            ('boundary/acidic-nanofiltration/evidence.json', ('decision', 'admission'), True),
            ('boundary/acidic-nanofiltration/evidence.json',
             ('POM_comparator', 'explicit_retention_denominator'), 'feed concentration'),
            ('identity/mov9-independent-assay-followup/evidence.json', 'admitted_calibration_rows', [{'value': 8.1}]),
            ('identity/mov9-independent-assay-followup/evidence.json',
             ('source_family', 'independent_experimental_data'), True),
            ('identity/mov9-independent-assay-followup/acquisition.json', ('routes', 2, 'http_status'), 200),
            ('parent-saved-j-crash-diagnostic/allocation-audit.json',
             ('allocation_observation', 'is_RSS_measurement_or_crash_cause'), True),
            ('parent-saved-j-crash-diagnostic/allocation-audit.json',
             ('allocation_observation', 'four_GiB_is_conservative_allocated_virtual_bound'), True),
            ('parent-saved-j-crash-diagnostic/allocation-audit.json', ('guard', 'unchanged'), False),
            ('parent-saved-j-crash-diagnostic/allocation-audit.json',
             ('writeback', 'pass2', 'max_destination_index'), 3068**2),
            ('identity/competing-mov-primary-followup/evidence.json', ('scope', 'new_compounds_admitted'), 1),
            ('identity/competing-mov-primary-followup/evidence.json',
             ('original_1991', 'accepted_formation_constant_rows'), [{'value': 60.37}]),
            ('identity/competing-mov-primary-followup/evidence.json',
             ('reported_percentage_rows', 0, 'calibration_eligible'), True),
            ('identity/competing-mov-primary-followup/evidence.json',
             ('assigned_fingerprint_rows', 0, 'target_mo36_assignment'), True),
            ('parent-saved-j-pilot/preparation.json', 'wall_cap_seconds', 3600),
            ('parent-saved-j-pilot/preparation.json', 'maximum_SCFs', 2),
            ('parent-saved-j-pilot/preparation.json', ('proof', 'method', 'max_cycle'), 40),
            ('parent-saved-j-pilot/independent-root-review.json', 'preparation_sha256', '0' * 64),
            ('parent-saved-j-pilot/history/f5c945a-incomplete/STATUS.json', 'prepared', True),
            ('identity/vanadium-incorporation-followup/evidence.json', 'exact_target_verified', True),
            ('identity/vanadium-incorporation-followup/evidence.json',
             ('primary_constraint', 'matrix', 'pH_conflicting_reports'), []),
            ('identity/vanadium-incorporation-followup/evidence.json', ('primary_constraint', 'matrix', 'pH'), 2.8),
            ('identity/vanadium-incorporation-followup/evidence.json',
             ('existing_evidence_reclassification', 'measured_vv_site'), True),
            ('identity/mixed-addenda-source-audit/evidence.json', 'exact_target_established', True),
            ('identity/mixed-addenda-source-audit/evidence.json',
             ('source_findings', 0, 'refined_w_occupancy'), 1),
            ('renewal/receiver-function-audit/constraints.json',
             ('positive_control', 'quantitative_rinse_carryover_bound'), 0),
            ('renewal/receiver-function-audit/constraints.json',
             ('negative_control', 'post_transfer_oxygen_nondetection_claim'), True),
            ('renewal/receiver-function-audit/constraints.json',
             ('conditional_activity_equivalent_accounting', 'measured_conversion_fractions'), True),
            ('renewal/receiver-function-audit/constraints.json',
             ('limits', 'functional_inheritance_verified'), True),
            ('renewal/oxide-isotope-constraints/analysis.json', 'reported_rate_count', 119),
            ('renewal/oxide-isotope-constraints/analysis.json', ('site_endpoints', 'A'), 'oxygen_exchange'),
            ('renewal/oxide-isotope-constraints/analysis.json', ('inference_limits', 'life_demonstrated'), True),
            ('renewal/manganese-regeneration-constraints/constraints.json',
             ('QCM_protocol', 'slopes_transfer_to_long_protocol'), True),
            ('renewal/manganese-regeneration-constraints/constraints.json',
             ('phosphate_free_control', 'reaction_rate_inferred_zero'), True))
        for name, key, value in mutations:
            with self.subTest(name=name, key=key):
                path = self.recursive / name
                original = path.read_bytes()
                data = json.loads(original)
                keys = key if isinstance(key, tuple) else (key,)
                target = data
                for part in keys[:-1]:
                    target = target[part]
                target[keys[-1]] = value
                path.write_text(json.dumps(data))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
                path.write_bytes(original)

    def test_results_added_to_failed_parent_are_rejected(self):
        for name in ('result.json', 'J.npy'):
            with self.subTest(name=name):
                path = self.recursive / 'parent-openmp-first-j/run-v1' / name
                path.write_text('{}')
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
                path.unlink()

    def test_consistently_promoted_saved_j_result_is_rejected(self):
        run = self.recursive / 'parent-saved-j-qualification/run-v1'
        paths = [run / name for name in ('scf/result.json', 'launch-result.json', 'terminal-progress.json')]
        originals = [path.read_bytes() for path in paths]
        for key, value in (('parent_run', True), ('fresh_holdout', True), ('physical_admission', True),
                           ('checks', []), ('SCFs_launched', 2)):
            with self.subTest(key=key):
                worker, launch, terminal = [json.loads(data) for data in originals]
                worker[key] = value
                launch['results']['scf'] = terminal['results']['scf'] = worker
                for path, data in zip(paths, (worker, launch, terminal)):
                    path.write_text(json.dumps(data))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        for path, data in zip(paths, originals):
            path.write_bytes(data)

    def test_fabricated_parent_completion_or_rewritten_draft_is_rejected(self):
        for name in ('run-v1/latest-complete-cycle.npz', 'run-v1/native-final-state.npz', 'run-v1/final-validated-state.npz',
                     'history/f5c945a-incomplete/preparation.json',
                     'history/f5c945a-incomplete/run-v1'):
            with self.subTest(name=name):
                path = self.recursive / 'parent-saved-j-pilot' / name
                path.write_text('{}')
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
                path.unlink()

    def test_consistently_promoted_terminal_parent_is_rejected(self):
        run = self.recursive / 'parent-saved-j-pilot/run-v1'
        paths = [run / name for name in ('result.json', 'launch-result.json')]
        originals = [path.read_bytes() for path in paths]
        for key, value in (('native_converged', True), ('final_validation_complete', True),
                           ('physical_admission', True), ('fresh_holdout', True)):
            with self.subTest(key=key):
                worker, launch = [json.loads(data) for data in originals]
                worker[key] = value
                launch['result'] = worker
                for path, data in zip(paths, (worker, launch)):
                    path.write_text(json.dumps(data))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        for path, data in zip(paths, originals):
            path.write_bytes(data)
        stages_path = run / 'stages.jsonl'
        original_stages = stages_path.read_text()
        for stage in ('completed_cycle', 'native_post_kernel_entry', 'native_post_kernel_return',
                      'kernel_return', 'final_validation_entry', 'final_validation_return'):
            with self.subTest(stage=stage):
                stages_path.write_text(json.dumps({'stage': stage}) + '\n' + original_stages)
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        stages_path.write_text(original_stages)

    def test_original_source_pin_bindings_are_required(self):
        manifest = Path(__file__).resolve().parents[1] / 'research/2026-10-15/manifest.json'
        records = [record for record in json.loads(manifest.read_text())['files'] if record['status'] == 'included']
        verify_parent_pilot_source_bindings(records)
        for suffix in ('parent-saved-j-pilot/preparation.json', 'parent-saved-j-pilot/independent-root-review.json',
                       'history/f5c945a-incomplete/run.py', 'history/f5c945a-incomplete/STATUS.json',
                       'parent-j-repeatability/preparation.json', 'parent-j-repeatability/run-v1/J1.npy',
                       'parent-j-error-impact/preparation.json', 'parent-j-error-impact/analysis-v1/result.json',
                       'parent-j-stage-localization/preparation.json', 'parent-j-stage-localization/independent-root-review.json',
                       'parent-j-stage-localization/run-v1/result.json', 'parent-j-stage-localization/run-v1/launch-result.json',
                       'boundary/copper-phosphate-transport/DECISION.json',
                       'boundary/hollow-silicalite-followup/ROOT_REVIEW.json', 'identity/beta-vmo7-discriminator/ROOT_REVIEW.json',
                       'parent-metric-solve-diagnostic/run-v1/launch-result.json',
                       'parent-metric-solve-diagnostic-v2/run.py',
                       'parent-metric-solve-diagnostic-v2/preparation.json',
                       'parent-metric-solve-diagnostic-v2/qualification-failed-v1.json',
                       'boundary/aqueous-pom-nanofiltration-followup/evidence.json',
                       'boundary/aqueous-pom-nanofiltration-followup/extracted-results.json',
                       'parent-saved-metric-solve/run-v1/launch-result.json',
                       'parent-saved-metric-solve/run-v1/result.json',
                       'parent-explicit-blas-j/preparation.json',
                       'parent-explicit-blas-j/qualification.json',
                       'parent-explicit-blas-j/test_run.py',
                       'parent-explicit-blas-j/run-v1/result.json',
                       'parent-explicit-blas-j/run-v1/launch-result.json',
                       'explicit-blas-accuracy-qualification/PROTOCOL_DRAFT.md',
                       'explicit-blas-accuracy-qualification/PREREQUISITE_STATUS.json',
                       'identity/measurement-integrity-followup/ROOT_REVIEW.json',
                       'identity/competing-mov-speciation/ACCESS_FOLLOWUP_2026-10-16.md'):
            with self.subTest(suffix=suffix):
                record = next(record for record in records if record['path'].endswith(suffix))
                original = record['source_sha256']
                record['source_sha256'] = '0' * 64
                with self.assertRaises(AssertionError):
                    verify_parent_pilot_source_bindings(records)
                record['source_sha256'] = original

    def test_repeatability_completion_cannot_be_promoted_or_lose_closed_checkpoint(self):
        run = self.recursive / 'parent-j-repeatability/run-v1'
        worker_path, launch_path = run / 'result.json', run / 'launch-result.json'
        originals = [path.read_bytes() for path in (worker_path, launch_path)]
        for key, value in (('numerical_pass', True), ('parent_SCF_readiness', True),
                           ('physical_admission', True), ('SCFs_launched', 1),
                           ('sign_and_call_order_confounded', False)):
            with self.subTest(key=key):
                worker, launch = [json.loads(data) for data in originals]
                worker[key] = value
                launch['worker_result'] = worker
                for path, data in zip((worker_path, launch_path), (worker, launch)):
                    path.write_text(json.dumps(data))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        for path, data in zip((worker_path, launch_path), originals):
            path.write_bytes(data)
        stages_path = run / 'stages.jsonl'
        original_stages = stages_path.read_text()
        for name in ('returned_J_saved_closed', 'post_call_file_closed'):
            with self.subTest(stage=name):
                stages_path.write_text('\n'.join(line for line in original_stages.splitlines()
                                                if json.loads(line)['stage'] != name) + '\n')
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        stages_path.write_text(original_stages)

    def test_stage_completion_cannot_consistently_promote_worker_and_launcher(self):
        run = self.recursive / 'parent-j-stage-localization/run-v1'
        worker_path, launch_path = run / 'result.json', run / 'launch-result.json'
        worker_original, launch_original = worker_path.read_bytes(), launch_path.read_bytes()
        for key, value in (('SCFs_launched', 1), ('PCM_builds', 1), ('parent_SCF_readiness', True),
                           ('physical_admission', True), ('controlled_output_is_ordinary_J_P0', True)):
            with self.subTest(key=key):
                worker, launch = json.loads(worker_original), json.loads(launch_original)
                worker[key] = value
                launch['worker_result'] = worker
                worker_path.write_text(json.dumps(worker))
                launch_path.write_text(json.dumps(launch))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        worker_path.write_bytes(worker_original)
        launch_path.write_bytes(launch_original)

    def test_metric_checkpoint_cannot_acquire_unobserved_result_or_approval(self):
        for suffix in ('parent-metric-solve-diagnostic/run-v1/result.json',
                       'parent-metric-solve-diagnostic/run-v1/original_metric.npy',
                       'explicit-blas-accuracy-qualification/run.py',
                       'explicit-blas-accuracy-qualification/run-v1/result.json',
                       'parent-metric-solve-diagnostic-v2/run-v1/result.json'):
            with self.subTest(suffix=suffix):
                path = self.recursive / suffix
                parent_existed = path.parent.exists()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('{}')
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
                path.unlink()
                if not parent_existed:
                    path.parent.rmdir()

    def test_stage_control_cannot_erase_ordinary_failure_or_claim_causality(self):
        run = self.recursive / 'parent-j-stage-localization/run-v1'
        paths = [run / name for name in ('comparisons.json', 'result.json', 'launch-result.json')]
        originals = [path.read_bytes() for path in paths]
        for promote in ('ordinary_pass', 'stage_causality_proven', 'controlled_output_is_ordinary_J_P0'):
            with self.subTest(promote=promote):
                comparisons, worker, launch = map(json.loads, originals)
                if promote == 'ordinary_pass':
                    comparisons['J_comparisons']['J_B_minus_J_A']['pass'] = True
                else:
                    comparisons[promote] = True
                worker['comparisons'] = comparisons
                launch['worker_result'] = worker
                for path, record in zip(paths, (comparisons, worker, launch)):
                    path.write_text(json.dumps(record))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        for path, original in zip(paths, originals):
            path.write_bytes(original)

    def test_explicit_blas_consistent_negative_result_promotions_are_rejected(self):
        run = self.recursive / 'parent-explicit-blas-j/run-v1'
        paths = [run / name for name in ('comparisons.json', 'result.json')]
        originals = [path.read_bytes() for path in paths]
        for key, value in (('pass', True), ('max_absolute_error', 0),
                           ('entries_above_tolerance', 0), ('absolute_tolerance', 1e-9),
                           ('relative_tolerance', 1e-9)):
            with self.subTest(key=key):
                comparisons, result = map(json.loads, originals)
                comparisons['repeat'][key] = value
                result['comparisons'] = comparisons
                for path, record in zip(paths, (comparisons, result)):
                    path.write_text(json.dumps(record))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        for path, original in zip(paths, originals):
            path.write_bytes(original)

    def test_stage_and_source_artifacts_bind_original_manifest_bytes(self):
        manifest = Path(__file__).resolve().parents[1] / 'research/2026-10-15/manifest.json'
        records = [record for record in json.loads(manifest.read_text())['files'] if record['status'] == 'included']
        verify_stage_artifact_bindings(self.recursive, records)
        for name in ('native.log', 'stdout.txt', 'stderr.txt'):
            with self.subTest(excluded_log=name):
                records.append({'path': 'recursive-compound-2026-10-15/parent-saved-metric-solve/run-v1/' + name,
                                'source_sha256': '0' * 64})
                with self.assertRaises(AssertionError):
                    verify_stage_artifact_bindings(self.recursive, records)
                records.pop()
        for name in ('raw/poster-response.body', 'raw/poster.headers'):
            with self.subTest(excluded_payload=name):
                records.append({'path': 'recursive-compound-2026-10-15/identity/measurement-integrity-followup/' + name,
                                'source_sha256': '0' * 64})
                with self.assertRaises(AssertionError):
                    verify_stage_artifact_bindings(self.recursive, records)
                records.pop()
        for suffix in ('parent-j-stage-localization/run-v1/J_A.npy',
                       'parent-j-stage-localization/run-v1/supervisor.json',
                       'boundary/copper-phosphate-transport/evidence.json',
                       'boundary/hollow-silicalite-followup/evidence.json',
                       'identity/beta-vmo7-discriminator/elemental-counterexample.md',
                       'parent-metric-solve-diagnostic/run-v1/failure.json',
                       'parent-metric-solve-diagnostic-v2/run-v1/supervisor.json',
                       'parent-blas-control-audit/observed.json',
                       'parent-blas-control-audit/failed-v1/probe.py',
                       'parent-saved-metric-solve/qualification-thread/errors-A1.json',
                       'parent-saved-metric-solve/run-v1/rho_A1.npy',
                       'parent-saved-metric-solve/run-v1/result.json',
                       'parent-explicit-blas-j/run-v1/J_A.npy',
                       'parent-explicit-blas-j/run-v1/result.json',
                       'identity/measurement-integrity-followup/acquisition.json',
                       'identity/concentration-speciation-followup/evidence.json',
                       'boundary/hollow-silicalite-followup/wetting-constraint/validation.json'):
            with self.subTest(suffix=suffix):
                record = next(record for record in records if record['path'].endswith(suffix))
                original = record['source_sha256']
                record['source_sha256'] = '0' * 64
                with self.assertRaises(AssertionError):
                    verify_stage_artifact_bindings(self.recursive, records)
                record['source_sha256'] = original

    def test_formal_counterexample_limits_cannot_be_removed(self):
        base = self.recursive / 'identity/beta-vmo7-discriminator'
        counterexample = base / 'elemental-counterexample.md'
        counterexample.write_text('The metal ratio proves target retention.\n')
        review_path = base / 'ROOT_REVIEW.json'
        review = json.loads(review_path.read_text())
        review['artifact_sha256']['elemental-counterexample.md'] = hashlib.sha256(counterexample.read_bytes()).hexdigest()
        review_path.write_text(json.dumps(review))
        with self.assertRaises(AssertionError):
            verify_openmp_renewal(self.recursive, self.case_names)

    def test_consistently_promoted_first_j_worker_is_rejected(self):
        run = self.recursive / 'parent-openmp-first-j-v2/run-v1'
        worker_path, launch_path = run / 'result.json', run / 'launch-result.json'
        worker_original, launch_original = worker_path.read_bytes(), launch_path.read_bytes()
        for key, value in (('SCFs_launched', 1), ('whole_SCF_performance_claim', True),
                           ('physical_admission', True)):
            with self.subTest(key=key):
                worker, launch = json.loads(worker_original), json.loads(launch_original)
                worker[key] = value
                launch['worker_result'] = worker
                worker_path.write_text(json.dumps(worker))
                launch_path.write_text(json.dumps(launch))
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
        worker_path.write_bytes(worker_original)
        launch_path.write_bytes(launch_original)

    def test_unquantified_rate_replaced_with_zero_is_rejected(self):
        path = self.recursive / 'renewal/oxide-isotope-constraints/rates.csv'
        path.write_text(path.read_text().replace(',,,too_fast_no_numeric_bound', ',0,0,too_fast_no_numeric_bound', 1))
        with self.assertRaises(AssertionError):
            verify_openmp_renewal(self.recursive, self.case_names)

    def test_inconsistent_percentage_rows_cannot_be_normalized(self):
        path = self.recursive / 'identity/competing-mov-primary-followup/evidence.json'
        data = json.loads(path.read_text())
        row = data['reported_percentage_rows'][0]['reported_percent']
        total = sum(row.values())
        for key in row:
            row[key] *= 100 / total
        path.write_text(json.dumps(data))
        with self.assertRaises(AssertionError):
            verify_openmp_renewal(self.recursive, self.case_names)

    def test_signed_diagnostic_cannot_gain_unobserved_completion(self):
        for name in ('second-checks.json', 'selected-oracle.json', 'result.json', 'checks.json'):
            with self.subTest(name=name):
                path = self.recursive / 'parent-signed-j-diagnostic/run-v1' / name
                path.write_text('{}')
                with self.assertRaises(AssertionError):
                    verify_openmp_renewal(self.recursive, self.case_names)
                path.unlink()


class MemoryFollowupVerification(unittest.TestCase):
    case_names = {'anion-water', 'neutral-water', 'anion-eps1', 'heldout-Mo2O7', 'new-external'}

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.recursive = Path(temporary.name)
        source = (Path(__file__).resolve().parents[1] / 'research/2026-10-15'
                  / 'recursive-compound-2026-10-15')
        for folder in ('cpcm-rij-memory-qualification', 'energy/silicotungstate-20',
                       'parent-pilot-memory', 'wv-method-qualification', 'renewal/fe-feed-21'):
            self.assertTrue((source / folder).is_dir(), folder)
            for path in (source / folder).rglob('*'):
                if path.is_file() and (path.suffix in ('.json', '.jsonl')
                                       or path.name == 'THREAD_DIAGNOSTIC.md'):
                    target = self.recursive / path.relative_to(source)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())

    def test_saved_terminal_results_and_prepared_snapshots_pass(self):
        verify_memory_followup(self.recursive, self.case_names)

    def test_result_regressions_are_rejected(self):
        mutations = (
            ('cpcm-rij-memory-qualification/preparation.json', 'status', 'EXECUTED'),
            ('cpcm-rij-memory-qualification/run-v1/result.json', 'phase2_skipped', True),
            ('cpcm-rij-memory-qualification/run-v1/operators-anion-water/result.json',
             'checks', [{'pass': False}]),
            ('cpcm-rij-memory-qualification/run-v1/scf-new-external/result.json',
             'SCF', {'converged': False, 'cycles': 32}),
            ('energy/silicotungstate-20/assessment.json', 'admitted_to_assembly', True),
            ('energy/silicotungstate-20/assessment.json', 'useful_target_energy_transfer_verified', True),
            ('parent-pilot-memory/run-v1/supervisor.json', 'termination_reason', None),
            ('wv-method-qualification/preparation.json', 'SCFs_launched', 1),
            ('wv-method-qualification/run-v1/result.json', 'physical_admission', True),
            ('wv-method-qualification/run-v1/result.json', 'actual_SCFs_launched', 3),
            ('wv-method-qualification/run-v1/receipts.json', (1, 'case'), 'WO4'),
            ('wv-method-qualification/run-v1/WO4/result.json', ('checks', 0, 'pass'), False),
            ('wv-method-qualification/run-v1/VO4/result.json', ('direct_SCF', 'converged'), False),
            ('wv-method-qualification/run-v1/VO4/result.json', 'experimental_validation', True),
            ('wv-method-qualification/run-v1/WO4/supervisor.json', 'returncode', 1),
            ('renewal/fe-feed-21/assessment.json', 'admitted_to_assembly', True),
            ('renewal/fe-feed-21/assessment.json', 'experimental_holdout', True),
            ('renewal/fe-feed-21/assessment.json', 'founder_replacement_fraction', 0),
            ('renewal/fe-feed-21/assessment.json', 'fig2d_feed_unit_conflict_resolved', True),
            ('renewal/fe-feed-21/analysis.json', 'target_renewal_demonstrated', True),
            ('renewal/fe-feed-21/analysis.json', ('source_label_conflict', 'workbook_label_verbatim'),
             'with 50 uM Fe(II)'),
            ('renewal/fe-feed-21/analysis.json', ('fig2e', 'current_density_mA_cm-2'), 10),
            ('renewal/fe-feed-21/analysis.json',
             ('matched_Co_assisted_vs_unassisted_EQCM', 'Co_assisted_rate_data'), []),
            ('renewal/fe-feed-21/analysis.json', ('fig1c', 'observations', 0, 'uncertainty'), 0),
            ('renewal/fe-feed-21/source-data-inventory.json',
             ('workbooks', 1, 'sheets', 2, 'text_cells_in_first_three_rows', 'C1'), 'with 50 uM Fe(II)'))
        for name, key, value in mutations:
            with self.subTest(name=name, key=key):
                path = self.recursive / name
                original = path.read_bytes()
                changed = json.loads(original)
                keys = (key,) if isinstance(key, str) else key
                target = changed
                for field in keys[:-1]:
                    target = target[field]
                target[keys[-1]] = value
                path.write_text(json.dumps(changed))
                try:
                    with self.assertRaises(AssertionError):
                        verify_memory_followup(self.recursive, self.case_names)
                finally:
                    path.write_bytes(original)

    def test_unreported_parent_results_are_rejected(self):
        for name in ('parent-pilot-memory/run-v1/SCF-result.json',
                     'parent-pilot-memory/run-v1/iterations.jsonl',
                     'parent-pilot-memory/run-v1/storage.json'):
            with self.subTest(name=name):
                path = self.recursive / name
                path.touch()
                try:
                    with self.assertRaises(AssertionError):
                        verify_memory_followup(self.recursive, self.case_names)
                finally:
                    path.unlink()

    def test_runtime_probe_cannot_be_promoted_to_scientific_execution(self):
        path = self.recursive / 'parent-pilot-memory/THREAD_DIAGNOSTIC.md'
        original = path.read_text()
        self.assertIn('"SCFs": 0', original)
        path.write_text(original.replace('"SCFs": 0', '"SCFs": 1'))
        with self.assertRaises(AssertionError):
            verify_memory_followup(self.recursive, self.case_names)
