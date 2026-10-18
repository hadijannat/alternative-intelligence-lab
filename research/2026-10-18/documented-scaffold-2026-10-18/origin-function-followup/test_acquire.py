"""Offline failure checks: attempted primary access must leave a receipt."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("ou_acquire", Path(__file__).parent / "sources/acquire.py")
acquire = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acquire)


class ReceiptFailures(unittest.TestCase):
    def test_bad_metadata_preserves_all_initial_attempts(self):
        for body in ("invalid JSON", json.dumps({"resource_doi": "wrong DOI"})):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)

                def fake_fetch(item):
                    name, url = item
                    (root / name).write_text(body if name.endswith(".json") else "%PDF")
                    return dict(name=name, url=url, status=200)

                with patch.object(acquire, "ROOT", root), patch.object(acquire, "fetch", fake_fetch):
                    with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
                        acquire.main()
                saved = json.loads((root / "receipt.json").read_text())
                self.assertEqual(len(saved["requests"]), 3)
                self.assertIsNotNone(saved["execution_error"])

    def test_interrupted_body_keeps_response_status_and_error(self):
        class Interrupted(io.BytesIO):
            code, url, headers = 200, "https://example.test/final", {"Content-Type": "application/pdf"}

            def read(self):
                raise OSError("interrupted body")

        with tempfile.TemporaryDirectory() as folder, patch.object(acquire, "ROOT", Path(folder)):
            with patch.object(acquire.urllib.request, "urlopen", return_value=Interrupted()):
                saved = acquire.fetch(("test.pdf", "https://example.test/test"))
            self.assertEqual(saved["status"], 200)
            self.assertIn("interrupted body", saved["error"])
            self.assertFalse((Path(folder) / "test.pdf").exists())


if __name__ == "__main__":
    unittest.main()
