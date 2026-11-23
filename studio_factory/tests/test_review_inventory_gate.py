"""G-14: an empty or missing asset root must never report inventory PASS."""
import json
import tempfile
import unittest
from pathlib import Path
from studio_factory.review_web import Catalog


class InventoryGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.repo=self.root/'repo';(self.repo/'projects'/'film').mkdir(parents=True)
        (self.root/'assets').mkdir()

    def tearDown(self):self.tmp.cleanup()

    def catalog(self,config=None):
        if config is not None:
            (self.repo/'projects'/'film'/'PROJECT.json').write_text(json.dumps(config))
        c=Catalog(self.root/'assets',self.repo,self.root/'r.sqlite3',project='film')
        self.addCleanup(c.store.connection.close)
        return c

    def test_missing_manifest_with_declared_count_is_blocked(self):
        c=self.catalog({'project_id':'film','expected_asset_files':267})
        self.assertFalse(c.manifest_present)
        self.assertEqual(c.expected,267)
        r=c.run_test('inventory')
        self.assertEqual(r['state'],'BLOCKED')
        self.assertEqual((r['checked'],r['expected']),(0,267))
        self.assertEqual(c.public()['expected_files'],267)

    def test_empty_root_without_declaration_is_not_pass(self):
        r=self.catalog().run_test('inventory')
        self.assertEqual(r['state'],'BLOCKED')
        self.assertEqual(r['expected'],0)

    def test_partial_manifest_against_declared_count_fails(self):
        files=self.root/'assets'/'files';files.mkdir();(files/'a.txt').write_bytes(b'a')
        import hashlib
        inv={'files_count':1,'files':[{'source_relative':'a.txt','size_bytes':1,'sha256':hashlib.sha256(b'a').hexdigest()}]}
        (self.root/'assets'/'MANIFEST').mkdir();(self.root/'assets'/'MANIFEST'/'inventory.json').write_text(json.dumps(inv))
        r=self.catalog({'project_id':'film','expected_asset_files':2}).run_test('inventory')
        self.assertEqual(r['state'],'FAIL')
        self.assertIn('verified 1 of expected 2',r['failures'])


if __name__=='__main__':unittest.main()
