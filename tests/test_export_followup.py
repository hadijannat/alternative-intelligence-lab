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
from verify_followup import verify_memory_followup, verify_openmp_renewal


class PublicationSelection(unittest.TestCase):
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
        for folder in ('copI-source', 'mo-blue-route'):
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
                       'parent-openmp-qualification', 'parent-openmp-qualification-v2'):
            self.assertTrue((source / folder).is_dir(), folder)
            for path in (source / folder).rglob('*'):
                if path.is_file() and path.suffix in ('.json', '.py', '.md'):
                    target = self.recursive / path.relative_to(source)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())

    def test_failure_and_unrun_repair_are_preserved(self):
        verify_openmp_renewal(self.recursive, self.case_names)

    def test_admission_and_result_mutations_are_rejected(self):
        mutations = (
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
             ('checks', 0, 'pass'), False))
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

    def test_prepared_or_launched_v2_is_rejected(self):
        for name in ('preparation.json', 'run-v1', 'pins.json'):
            with self.subTest(name=name):
                path = self.recursive / 'parent-openmp-qualification-v2' / name
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
