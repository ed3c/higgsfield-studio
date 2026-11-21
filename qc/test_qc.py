import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import creative_score  # noqa: E402
import mech_check  # noqa: E402

HAS_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


class CreativeScoreTest(unittest.TestCase):
    def test_all_eights_pass(self):
        scores = {k: 8 for k in creative_score.CRITERIA}
        self.assertTrue(creative_score.evaluate(scores)["pass"])

    def test_high_average_with_one_six_fails(self):
        scores = {k: 10 for k in creative_score.CRITERIA}
        scores["sound"] = 6
        result = creative_score.evaluate(scores)
        self.assertGreaterEqual(result["average"], 8)
        self.assertFalse(result["pass"])

    def test_all_sevens_fail_on_average(self):
        result = creative_score.evaluate({k: 7 for k in creative_score.CRITERIA})
        self.assertFalse(result["pass"])

    def test_missing_item_fails(self):
        self.assertFalse(creative_score.evaluate({"directing": 9})["pass"])


@unittest.skipUnless(HAS_FFMPEG, "需要 ffmpeg")
class MechCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.good = root / "good.mp4"
        ffmpeg("-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30:duration=2",
               "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=2",
               "-af", "volume=-12dB", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-shortest", str(cls.good))
        # Bad: wrong size, a 0.6 s black hole in the middle, full-scale clipped audio.
        cls.bad = root / "bad.mp4"
        ffmpeg("-f", "lavfi", "-i", "testsrc2=size=640x480:rate=30:duration=1",
               "-f", "lavfi", "-i", "color=black:size=640x480:rate=30:duration=0.6",
               "-f", "lavfi", "-i", "testsrc2=size=640x480:rate=30:duration=1",
               "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=2.6",
               "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v];[3:a]volume=30dB[a]",
               "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast",
               "-pix_fmt", "yuv420p", "-c:a", "aac", str(cls.bad))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_good_clip_passes_tiktok(self):
        report = mech_check.check(self.good, "tiktok")
        self.assertTrue(report["pass"], report["failed"])
        self.assertIn("safe_area_note", report)

    def test_bad_clip_fails_with_reasons(self):
        report = mech_check.check(self.bad, "tiktok")
        self.assertFalse(report["pass"])
        for name in ("resolution", "aspect", "black_frames", "audio_clipping"):
            self.assertIn(name, report["failed"])

    def test_contest_profile_rejects_short_film(self):
        report = mech_check.check(self.good, "higgsfield-contest")
        self.assertIn("duration", report["failed"])


if __name__ == "__main__":
    unittest.main()
