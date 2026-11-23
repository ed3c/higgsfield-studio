"""HOF-05: review SQLite backup and restore without silent loss."""
import tempfile
import unittest
from pathlib import Path
from studio_factory.review_web import ReviewStore, backup_reviews, restore_reviews


class ReviewBackupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.db=self.root/'reviews.sqlite3'
        s=ReviewStore(self.db,'j4-async-succession')
        for i,d in enumerate(('PASS','FAIL','DEFER')):s.put(f'item{i}',d,'note','reviewer','')
        s.connection.close()

    def tearDown(self):self.tmp.cleanup()

    def test_backup_restore_roundtrip_keeps_previous(self):
        out=self.root/'bk'/'reviews.backup.sqlite3'
        r=backup_reviews(self.db,out)
        self.assertEqual((r['rows'],r['integrity'],r['project']),(3,'ok','j4-async-succession'))
        self.assertTrue(out.with_name(out.name+'.receipt.json').is_file())
        with self.assertRaises(ValueError):backup_reviews(self.db,out)
        s=ReviewStore(self.db,'j4-async-succession');s.put('item0','FAIL','changed','x','');s.connection.close()
        res=restore_reviews(out,self.db)
        self.assertEqual(res['rows'],3);self.assertIsNotNone(res['previous_kept_at'])
        self.assertTrue(Path(res['previous_kept_at']).is_file())
        s=ReviewStore(self.db,'j4-async-succession')
        self.assertEqual(s.get_all()['item0']['decision'],'PASS');s.connection.close()

    def test_tampered_backup_is_refused(self):
        out=self.root/'reviews.backup.sqlite3';backup_reviews(self.db,out)
        with out.open('ab') as f:f.write(b'tamper')
        with self.assertRaisesRegex(ValueError,'receipt'):restore_reviews(out,self.db)


if __name__=='__main__':unittest.main()
