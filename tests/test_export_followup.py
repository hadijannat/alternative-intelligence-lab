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

    def test_historical_model_retained(self):
        self.assertIsNone(exclusion(Path('rna-turnover-tests-2026-10-15/results-v1/frozen/model.py')))

    def test_scientific_evidence_retained(self):
        self.assertIsNone(exclusion(Path('measured-coupling-2026-10-15/droplet_model/.omo/evidence/run-v1/frozen/model.py')))

    def test_normalized_inheritance_retained(self):
        self.assertIsNone(exclusion(Path('rna-mechanism-2026-10-15/sources/inheritance/normalized/ameta_droplet_umis.csv')))

    def test_retention_verification_retained(self):
        self.assertIsNone(exclusion(Path('rna-mechanism-2026-10-15/sources/retention/.omo/evidence/verification.json')))

    def test_signed_query_removed_without_touching_stable_query(self):
        text = '"https://example.org/file?Expires=1&Signature=private&Key-Pair-Id=key" https://example.org/?id=2'
        cleaned, count = strip_signed_urls(text)
        self.assertEqual(cleaned, '"https://example.org/file" https://example.org/?id=2')
        self.assertEqual(count, 1)

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
