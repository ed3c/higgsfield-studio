import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_animatic as ba  # noqa: E402

HAS_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


@unittest.skipUnless(HAS_FFMPEG, "需要 ffmpeg")
class BuildAnimaticTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)
        shots = [
            {"shot_id": "S01", "act": 1, "start_s": 0, "duration_s": 1.5},
            {"shot_id": "S02", "act": 1, "start_s": 1.5, "duration_s": 2.0},
            {"shot_id": "S03", "act": 2, "start_s": 3.5, "duration_s": 2.5},
        ]
        (self.project / "shots.json").write_text(json.dumps(shots), encoding="utf-8")
        stills = self.project / "stills"
        stills.mkdir()
        for name, color in (("s01.png", "red"), ("s02.png", "green"), ("s03a.png", "blue"), ("s03b.png", "yellow")):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c={color}:s=360x640:d=1",
                            "-frames:v", "1", str(stills / name)], check=True)
        with (self.project / "selects.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["shot_id", "keyframe", "endframe"])
            writer.writerow(["S01", "stills/s01.png", ""])
            writer.writerow(["S02", "stills/s02.png", ""])
            writer.writerow(["S03", "stills/s03a.png", "stills/s03b.png"])
        self.out = self.project / "renders" / "animatic.mp4"

    def tearDown(self):
        self.tmp.cleanup()

    def test_renders_full_length_with_video_and_audio(self):
        result = ba.build(self.project, self.out, size=(270, 480), fps=12)
        self.assertEqual(result["placeholders"], 0)
        info = probe(self.out)
        kinds = {s["codec_type"]: s for s in info["streams"]}
        self.assertEqual((kinds["video"]["width"], kinds["video"]["height"]), (270, 480))
        self.assertIn("audio", kinds)
        self.assertAlmostEqual(float(info["format"]["duration"]), 6.0, delta=0.2)

    def test_endframe_crossfade_reaches_end_color(self):
        ba.build(self.project, self.out, size=(270, 480), fps=12, audio="silent")
        frame = self.project / "last.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.2", "-i", str(self.out),
                        "-vf", "crop=20:20:125:230,scale=1:1", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        str(frame)], check=True)
        r, g, b = frame.read_bytes()[:3]
        self.assertGreater(r, 180)  # yellow end frame, not the blue key frame
        self.assertGreater(g, 180)
        self.assertLess(b, 90)

    def test_missing_still_is_refused_without_placeholder(self):
        (self.project / "stills" / "s02.png").unlink()
        with self.assertRaisesRegex(ba.AnimaticError, "S02"):
            ba.build(self.project, self.out, size=(270, 480), fps=12)

    def test_placeholder_fills_missing_still(self):
        (self.project / "stills" / "s02.png").unlink()
        result = ba.build(self.project, self.out, size=(270, 480), fps=12, placeholder=True)
        self.assertEqual(result["placeholders"], 1)
        self.assertTrue(self.out.exists())


if __name__ == "__main__":
    unittest.main()
