import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from studio.source.yt_gates import verify, parse_srt, _sha

VID = "TESTVID0001"
HAVE_FF = shutil.which("ffmpeg") and shutil.which("ffprobe")


def ff(*args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], check=True)


def make_bundle(d: Path, *, audio=True, srt=None, rights=True):
    """Synthetic positive control (lavfi test pattern + tone); NOT the S1 source."""
    master = d / f"{VID}.mkv"
    if audio:
        ff("-f", "lavfi", "-i", "testsrc2=size=320x240:rate=25:duration=6", "-f", "lavfi",
           "-i", "sine=frequency=440:sample_rate=48000:duration=6", "-c:v", "libx264", "-c:a", "aac", "-shortest", str(master))
    else:
        ff("-f", "lavfi", "-i", "testsrc2=size=320x240:rate=25:duration=6", "-c:v", "libx264", str(master))
    dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_format", "-of", "json", str(master)],
                                          capture_output=True, text=True).stdout)["format"]["duration"])
    (d / f"{VID}.info.json").write_text(json.dumps({"id": VID, "duration": round(dur)}))
    if audio:
        ff("-i", str(master), "-map", "0:a:0", "-c:a", "pcm_s24le", str(d / f"{VID}.audio.wav"))
    (d / f"{VID}.ja.srt").write_text(srt or "1\n00:00:00,500 --> 00:00:02,000\nテスト\n\n2\n00:00:02,500 --> 00:00:05,000\n二\n", encoding="utf-8")
    (d / "subtitles.json").write_text(json.dumps({"file": f"{VID}.ja.srt", "language": "ja", "is_original_language": True,
                                                   "provenance": "asr", "alignment_check": {"result": "PASS", "samples": 2}}))
    if rights:
        (d / "rights.json").write_text(json.dumps({"source_url": "synthetic", "video_id": VID, "rights_holder": "self (synthetic)",
                                                    "permitted_operations": ["download", "private_analysis"], "evidence": "generated locally",
                                                    "confirmed_by": "test", "confirmed_at": "2026-11-26"}))
    (d / "media-probe.json").write_text("{}"); (d / "QA_REPORT.md").write_text("qa"); (d / "tool_versions.json").write_text("{}")
    names = [p.name for p in sorted(d.iterdir()) if p.name != "SHA256SUMS"]
    (d / "SHA256SUMS").write_text("".join(f"{_sha(d / n)}  {n}\n" for n in names))


@unittest.skipUnless(HAVE_FF, "ffmpeg/ffprobe required")
class GateTests(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_no_rights_blocks_and_pauses_dependents(self):
        g = verify(self.d, VID)
        self.assertEqual(g["YT0"]["state"], "BLOCKED")
        self.assertTrue(all(g[k]["state"] == "NOT_RUN" for k in ("YT1", "YT2", "YT3", "YT4")))
        self.assertFalse(g["H01_acquisition_complete"])

    def test_positive_control_all_pass(self):
        make_bundle(self.d)
        g = verify(self.d, VID)
        self.assertEqual([g[k]["state"] for k in ("YT0", "YT1", "YT2", "YT3", "YT4")], ["PASS"] * 5, g)
        self.assertTrue(g["H01_acquisition_complete"])

    def test_video_only_master_fails_yt1(self):
        make_bundle(self.d, audio=False)
        g = verify(self.d, VID)
        self.assertEqual(g["YT1"]["state"], "FAIL")
        self.assertEqual(g["YT2"]["state"], "NOT_RUN")

    def test_out_of_order_srt_fails_yt3(self):
        make_bundle(self.d, srt="1\n00:00:03,000 --> 00:00:04,000\na\n\n2\n00:00:01,000 --> 00:00:02,000\nb\n")
        self.assertEqual(verify(self.d, VID)["YT3"]["state"], "FAIL")

    def test_tampered_hash_fails_yt4(self):
        make_bundle(self.d)
        with (self.d / "QA_REPORT.md").open("a") as fh:
            fh.write("changed")
        self.assertEqual(verify(self.d, VID)["YT4"]["state"], "FAIL")


class SrtTests(unittest.TestCase):
    def test_parse(self):
        c = parse_srt("1\n00:00:01,000 --> 00:00:02,500\nhi\n")
        self.assertEqual(c[0][:3], (1, 1.0, 2.5))

    def test_bad_end(self):
        with self.assertRaises(ValueError):
            parse_srt("1\n00:00:03,000 --> 00:00:02,000\nx\n")


if __name__ == "__main__":
    unittest.main()
