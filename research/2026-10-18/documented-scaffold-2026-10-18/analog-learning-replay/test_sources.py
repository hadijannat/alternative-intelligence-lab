"""Offline checks for source-file integrity and safe archive inventory."""
import hashlib
import importlib.util
import io
import contextlib
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from inventory import checked_members

SPEC = importlib.util.spec_from_file_location("browser_import", Path(__file__).parent / "sources/import_browser_files.py")
browser_import = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(browser_import)


class SourceBoundaries(unittest.TestCase):
    def test_hash_mismatch_is_not_imported(self):
        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "source", Path(folder) / "target"
            source.write_bytes(b"wrong body")
            with self.assertRaises(ValueError):
                browser_import.verified_copy(source, target, "sha256", "0" * 64)
            self.assertFalse(target.exists())

    def test_valid_copy_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "source", Path(folder) / "target"
            source.write_bytes(b"verified body")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            browser_import.verified_copy(source, target, "sha256", digest, 13)
            with self.assertRaises(FileExistsError):
                browser_import.verified_copy(source, target, "sha256", digest, 13)
            self.assertEqual(target.read_bytes(), b"verified body")

    def test_archive_rejects_parent_path_and_symlink(self):
        for name, mode in (("../escape", 0), ("link", stat.S_IFLNK << 16)):
            with self.subTest(name=name):
                stream = io.BytesIO()
                with zipfile.ZipFile(stream, "w") as archive:
                    item = zipfile.ZipInfo(name)
                    item.external_attr = mode
                    archive.writestr(item, b"data")
                stream.seek(0)
                with zipfile.ZipFile(stream) as archive, self.assertRaises(ValueError):
                    checked_members(archive)

    def test_metadata_path_is_rejected_with_error_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "attempt2").mkdir()
            files = [{"path": "../outside"}, {"path": "README.md"}]
            (root / "attempt2/dryad-files.json").write_text(json.dumps({"_embedded": {"stash:files": files}}))
            with patch.object(browser_import, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    browser_import.main()
            receipt = json.loads((root / "browser-receipt.json").read_text())
            self.assertIsNotNone(receipt["execution_error"])
            self.assertEqual(receipt["requests"][0]["status"], "import_error")
            self.assertEqual(list((root / "browser-native").iterdir()), [])

    def test_later_hash_failure_preserves_prior_import_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "attempt2").mkdir()
            downloads = root / "downloads"
            downloads.mkdir()
            (downloads / "data.zip").write_bytes(b"first")
            (downloads / "README.md").write_bytes(b"wrong second")
            files = [{"path": "data.zip", "size": 5, "digest": hashlib.sha256(b"first").hexdigest()},
                     {"path": "README.md", "size": 12, "digest": "0" * 64}]
            (root / "attempt2/dryad-files.json").write_text(json.dumps({"_embedded": {"stash:files": files}}))
            with patch.object(browser_import, "ROOT", root), patch.object(browser_import, "DOWNLOADS", downloads), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    browser_import.main()
            receipt = json.loads((root / "browser-receipt.json").read_text())
            self.assertEqual(receipt["requests"][0]["status"], "verified_native_bytes")
            self.assertEqual(receipt["requests"][1]["status"], "import_error")
            self.assertEqual(receipt["requests"][1]["name"], "README.md")
            self.assertFalse((root / "browser-native/README.md").exists())


if __name__ == "__main__":
    unittest.main()
