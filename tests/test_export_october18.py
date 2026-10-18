import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from export_october18 import FAILURES, LAB, exclusion, export
from verify_october18 import verify


class October18Publication(unittest.TestCase):
    def test_export_sanitizes_and_rejects_links_and_tool_envelopes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source'
            lab = source / LAB
            (lab / 'sources').mkdir(parents=True)
            (source / 'recursive-compound-2026-10-15').mkdir()
            (source / 'recursive-compound-2026-10-15/PROTOCOL.md').write_text('original contract')
            (lab / 'CONTINUATION_LEDGER.md').write_text('../recursive-compound-2026-10-15/PROTOCOL.md')
            raw = '/Users/example/private https://example.org/data?X-Amz-Signature=abc&token=def\r\n'
            (lab / 'REPORT.md').write_bytes(raw.encode())
            (lab / 'sources/receipt.json').write_text(json.dumps({'url': 'https://example.org/data?token=private'}))
            (lab / 'sources/verification.json').write_text(json.dumps({'output': 'private tool content', 'exit_code': 0}))
            (lab / 'alias.md').symlink_to(lab / 'REPORT.md')
            output = root / 'publication'
            export(source, output)
            manifest = json.loads((output / 'manifest.json').read_text())
            records = {r['path']: r for r in manifest['files']}
            report = records[LAB + '/REPORT.md']
            self.assertEqual(report['source_sha256'], hashlib.sha256(raw.encode()).hexdigest())
            self.assertNotEqual(report['source_sha256'], report['published_sha256'])
            self.assertEqual((output / LAB / 'REPORT.md').read_text(), '/USER_HOME/private https://example.org/data\n')
            self.assertEqual(records[LAB + '/alias.md']['status'], 'excluded')
            self.assertEqual(records[LAB + '/sources/verification.json']['status'], 'excluded')
            self.assertEqual((output / LAB / 'CONTINUATION_LEDGER.md').read_text(), '../GOAL_CONTRACT.md')
            with self.assertRaises(ValueError):
                export(source, output)

    def test_exclusions_and_preserved_failure_formats(self):
        for name in FAILURES:
            self.assertIsNone(exclusion(Path(name)))
        for name in ('sources/article.pdf', 'sources/article.xml', 'sources/article.txt',
                     'renewal-lead/sources/publisher-download.js',
                     'sources/crossref.json', 'data/native_cells.json',
                     'sources/repair/han2025/fig3-text-cells.json', 'data/figS8_native.png',
                     'consultation/reply.txt', 'results/unreviewed.log',
                     'spatial-fe-function/sources/ja5c00438_si_001.pdf', '__pycache__/model.pyc'):
            self.assertIsNotNone(exclusion(Path(name)), name)
        for name in ('sources/receipt.json', 'results/analysis.json', 'results/models.png'):
            self.assertIsNone(exclusion(Path(name)), name)
        self.assertIsNone(exclusion(Path('spatial-fe-function/REPORT.md')))
        self.assertIn('publisher JavaScript', exclusion(Path('renewal-lead/sources/publisher-download.js')))

    def test_complete_saved_snapshot_and_tampering(self):
        source = Path(__file__).resolve().parents[1] / 'research/2026-10-18'
        self.assertEqual(verify(source)['status'], 'PASS_OCTOBER18_PUBLICATION_ONLY')
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / 'snapshot'
            shutil.copytree(source, base)
            name = LAB + '/remote-fe-transport/negative_results.json'
            path = base / name
            value = json.loads(path.read_text())
            value['candidate_forecast_validated'] = True
            path.write_text(json.dumps(value))
            manifest_path = base / 'manifest.json'
            manifest = json.loads(manifest_path.read_text())
            record = next(r for r in manifest['files'] if r['path'] == name)
            manifest['published_bytes'] += path.stat().st_size - record['published_size']
            record['published_size'] = path.stat().st_size
            record['published_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(AssertionError):
                verify(base)

    def test_missing_failure_and_extra_payload_rejected(self):
        source = Path(__file__).resolve().parents[1] / 'research/2026-10-18'
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / 'snapshot'
            shutil.copytree(source, base)
            path = base / LAB / 'fe-site-observation/extraction_failures.txt'
            original = path.read_bytes()
            path.unlink()
            with self.assertRaises(AssertionError):
                verify(base)
            path.write_bytes(original)
            (base / 'unexpected.pdf').write_bytes(b'unlisted source payload')
            with self.assertRaises(AssertionError):
                verify(base)

    def test_result_promotion_rejected_after_coordinated_manifest_update(self):
        source = Path(__file__).resolve().parents[1] / 'research/2026-10-18'
        mutations = [
            (('checks', 'step_convergence_below_1e_minus_5'), True),
            (('candidate', 'LDH', 'status'), 'validated'),
            (('candidate', 'NiFeCl', 'fits'), {'fitted': True}),
            (('candidate', 'NiFeZnCl', 'training_count'), 3),
            (('CA', 'AEM', 'strict_full_edge_retention'), 0),
            (('CA', 'CEM', 'strict_full_edge_retention'), 0),
            (('synthetic', 'lower_sink_minus_higher_sink_A_5h', 4, 'reversal'), True),
            (('synthetic', 'lower_sink_minus_higher_sink_A_5h'), []),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / 'snapshot'
            shutil.copytree(source, base)
            name = LAB + '/remote-fe-transport/results/analysis.json'
            path, manifest_path = base / name, base / 'manifest.json'
            original, original_manifest = path.read_text(), manifest_path.read_text()
            for keys, replacement in mutations:
                with self.subTest(keys=keys):
                    value, manifest = json.loads(original), json.loads(original_manifest)
                    target = value
                    for key in keys[:-1]:
                        target = target[key]
                    target[keys[-1]] = replacement
                    path.write_text(json.dumps(value))
                    record = next(r for r in manifest['files'] if r['path'] == name)
                    manifest['published_bytes'] += path.stat().st_size - record['published_size']
                    record['published_size'] = path.stat().st_size
                    record['published_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
                    manifest_path.write_text(json.dumps(manifest))
                    with self.assertRaises(AssertionError):
                        verify(base)

    def test_spatial_empirical_promotion_rejected_with_updated_hash(self):
        source = Path(__file__).resolve().parents[1] / 'research/2026-10-18'
        mutations = [
            (('empirical_held_out_validation', 'status'), 'PASS'),
            (('empirical_held_out_validation', 'training_points'), 1),
            (('empirical_held_out_validation', 'held_out_points'), 1),
            (('main_case', 'identified_under_assumptions'), True),
            (('limitations',), []),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary) / 'snapshot'
            shutil.copytree(source, base)
            name = LAB + '/spatial-fe-function/results/analysis.json'
            path, manifest_path = base / name, base / 'manifest.json'
            original, original_manifest = path.read_text(), manifest_path.read_text()
            for keys, replacement in mutations:
                with self.subTest(keys=keys):
                    value, manifest = json.loads(original), json.loads(original_manifest)
                    target = value
                    for key in keys[:-1]:
                        target = target[key]
                    target[keys[-1]] = replacement
                    path.write_text(json.dumps(value))
                    record = next(r for r in manifest['files'] if r['path'] == name)
                    manifest['published_bytes'] += path.stat().st_size - record['published_size']
                    record['published_size'] = path.stat().st_size
                    record['published_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
                    manifest_path.write_text(json.dumps(manifest))
                    with self.assertRaises(AssertionError):
                        verify(base)


if __name__ == '__main__':
    unittest.main()
