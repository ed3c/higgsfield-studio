"""Repository-level proof that the entire final J4 text corpus remains recoverable."""
import json
import tempfile
import unittest
from pathlib import Path
from studio_factory.core import Factory
from studio_factory.seed_archive import seed

ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/"projects"/"j4-async-succession"

class J4ArchiveTests(unittest.TestCase):
    def test_version_corpus_fully_parseable(self):
        shots=json.loads((PROJECT/"archive"/"v2_6"/"j4_shots.json").read_text(encoding="utf-8"))
        self.assertEqual(len(shots["shots"]),25)
        self.assertEqual(shots["duration_ms"],90000)
        self.assertEqual(shots["shots"][17]["id"],"S18")
        self.assertEqual(shots["shots"][17]["start_ms"],63700)
        count=len([p for p in (PROJECT/"archive"/"v2_6").iterdir() if p.is_file()])
        versions=sorted((PROJECT/"archive").glob("v*/conversation_text_archive.json"))
        self.assertEqual(len(versions),14)
        for path in versions:
            blob=json.loads(path.read_text(encoding="utf-8"))
            for f in blob["files"]:
                self.assertIsInstance(f["content"],str)
                self.assertTrue(f["content"])
                if f["filename"].endswith(".json"):
                    json.loads(f["content"])
                count+=1
        self.assertEqual(count,132)

    def test_seed_creates_project_local_catalog_without_text_loss(self):
        with tempfile.TemporaryDirectory() as d:
            f=Factory(Path(d)/"factory.sqlite3")
            try:
                self.assertEqual(seed(f,PROJECT)["created"],132)
                self.assertEqual(seed(f,PROJECT)["unchanged"],132)
                export=f.export_manifest("j4-async-succession")
                self.assertEqual(len(export["artifacts"]),132)
                self.assertEqual(len(export["gates"]),0)
            finally:
                f.close()
