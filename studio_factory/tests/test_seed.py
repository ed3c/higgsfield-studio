import json
import tempfile
import unittest
from pathlib import Path
from studio_factory.core import Factory
from studio_factory.seed_archive import seed

class SeedTests(unittest.TestCase):
    def test_idempotent_versioned_import(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"film";(p/"archive"/"v2_6").mkdir(parents=True)
            (p/"archive"/"v2_6"/"j4_shots.json").write_text('{"shots":[]}',encoding="utf-8")
            (p/"archive"/"v2_7").mkdir()
            (p/"archive"/"v2_7"/"conversation_text_archive.json").write_text(json.dumps({
                "format":"J4_VERSION_TEXT_ARCHIVE","files":[
                   {"filename":"j4_sound_ir.json","content":'{"stems":[]}'}
                ]}))
            f=Factory(Path(d)/"db.sqlite3")
            try:
                self.assertEqual(seed(f,p)["created"],2)
                self.assertEqual(seed(f,p)["unchanged"],2)
                data=f.export_manifest("j4-async-succession")
                self.assertEqual(len(data["artifacts"]),2)
                self.assertEqual({a["domain"] for a in data["artifacts"]},{"shot","sound"})
            finally:f.close()
