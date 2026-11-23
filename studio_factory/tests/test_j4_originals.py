"""HOF-07: byte-exact J4 text/code originals must match the private archive inventory."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/'projects'/'j4-async-succession'/'archive'/'originals_2026-11-23'


class J4OriginalsTests(unittest.TestCase):
    def test_every_original_matches_manifest_digest(self):
        man=json.loads((ROOT/'ORIGINALS_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(len(man['files']),77)
        self.assertEqual(sum(1 for f in man['files'] if f['git_slot']),32)
        on_disk={str(p.relative_to(ROOT/'files')) for p in (ROOT/'files').rglob('*') if p.is_file()}
        self.assertEqual(on_disk,{f['source_relative'] for f in man['files']})
        for f in man['files']:
            raw=(ROOT/'files'/f['source_relative']).read_bytes()
            self.assertEqual(len(raw),f['size_bytes'],f['source_relative'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),f['sha256'],f['source_relative'])

    def test_no_media_or_archives(self):
        bad={'.mp4','.mov','.jpeg','.jpg','.png','.zip','.wav','.mp3'}
        self.assertFalse([p for p in (ROOT/'files').rglob('*') if p.suffix.lower() in bad])

    def test_parsed_slots_still_present_unchanged(self):
        slot=ROOT.parent/'v2_6'/'j4_qc_matrix.csv'
        self.assertIn('PARSED TEXT FOR SHEET',slot.read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
