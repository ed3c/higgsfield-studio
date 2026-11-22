import json
import tempfile
import unittest
from pathlib import Path
from studio_factory.archive import unpack, ArchiveError

class ArchiveTests(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"archive.json"
            path.write_text(json.dumps({"format":"J4_VERSION_TEXT_ARCHIVE",
                "files":[{"filename":"shot.json","content":'{"hello":"世界"}\n'}]}),encoding="utf-8")
            dst=Path(d)/"out"
            self.assertEqual(unpack(path,dst),1)
            self.assertEqual((dst/"shot.json").read_text(), '{"hello":"世界"}\n')
            with self.assertRaises(ArchiveError):
                unpack(path,dst)
    def test_path_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"bad.json"
            path.write_text(json.dumps({"format":"J4_VERSION_TEXT_ARCHIVE",
                "files":[{"filename":"../outside","content":"x"}]}))
            with self.assertRaises(ArchiveError):
                unpack(path,Path(d)/"out")
