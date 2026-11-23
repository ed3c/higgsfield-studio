"""Handoff: verify the ZIP SHA-256 BEFORE extraction; checksum readback of an asset root."""
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from studio_factory.review_web import safe_extract, verify_assets


class ArchivePrecheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        raw=b'original\n';self.zip=self.root/'a.zip'
        inv={'files_count':1,'files':[{'source_relative':'x.txt','size_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}]}
        with zipfile.ZipFile(self.zip,'w') as z:
            z.writestr('files/x.txt',raw);z.writestr('MANIFEST/inventory.json',json.dumps(inv))
        self.digest=hashlib.sha256(self.zip.read_bytes()).hexdigest()

    def tearDown(self):self.tmp.cleanup()

    def test_wrong_digest_extracts_nothing(self):
        dest=self.root/'out'
        with self.assertRaisesRegex(ValueError,'nothing extracted'):
            safe_extract(self.zip,dest,expect_sha256='0'*64)
        self.assertFalse(dest.exists())

    def test_correct_digest_and_readback(self):
        dest=self.root/'out'
        r=safe_extract(self.zip,dest,expect_sha256=self.digest)
        self.assertEqual((r['verified'],r['archive_sha256_checked']),(1,True))
        self.assertEqual(verify_assets(dest)['state'],'PASS')
        (dest/'files'/'x.txt').write_bytes(b'tampered')
        v=verify_assets(dest)
        self.assertEqual((v['state'],v['mismatch']),('FAIL',['x.txt']))

    def test_readback_without_manifest_is_blocked(self):
        self.assertEqual(verify_assets(self.root/'empty')['state'],'BLOCKED')


if __name__=='__main__':unittest.main()
