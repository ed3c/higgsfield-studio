#!/usr/bin/env python3
"""Mechanical pass/fail checks on a video file with ffprobe/ffmpeg.

Black frames, audio clipping, resolution/aspect, codec, pixel format, fps,
sample rate, duration, plus a luma-flicker warning. Prints a JSON report.
Exit 0 when nothing fails, 1 when any check fails, 2 on usage errors.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROFILES = REPO / "delivery" / "profiles.json"
BLACK_MIN_S = 0.1
BLACK_PIXEL_TH = 0.10
EDGE_GRACE_S = 0.5
CLIP_DBFS = -0.1
FLICKER_DELTA = 40.0
MANUAL = ["字幕安全區", "人物身份漂移", "肢體異常", "權利與來源"]


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def probe(path: Path) -> dict:
    result = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)


def black_segments(path: Path) -> list[tuple[float, float]]:
    result = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf",
                  f"blackdetect=d={BLACK_MIN_S}:pix_th={BLACK_PIXEL_TH}", "-an", "-f", "null", "-"])
    segments = []
    for match in re.finditer(r"black_start:([\d.]+)\s+black_end:([\d.]+)", result.stderr):
        segments.append((float(match.group(1)), float(match.group(2))))
    return segments


def max_volume(path: Path) -> float | None:
    result = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"])
    match = re.search(r"max_volume:\s*(-?[\d.]+|-inf) dB", result.stderr)
    if not match:
        return None
    return float("-inf") if match.group(1) == "-inf" else float(match.group(1))


def flicker_frames(path: Path) -> int:
    result = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf",
                  "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"])
    values = [float(v) for v in re.findall(r"lavfi\.signalstats\.YAVG=([\d.]+)", result.stderr)]
    return sum(1 for a, b in zip(values, values[1:]) if abs(b - a) > FLICKER_DELTA)


def add(checks: list[dict], name: str, ok: bool, detail: str, level: str = "fail") -> None:
    checks.append({"check": name, "status": "pass" if ok else level, "detail": detail})


def check(path: Path, profile_name: str, profiles_path: Path = PROFILES) -> dict:
    profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    if profile_name not in profiles or profile_name.startswith("_"):
        raise KeyError(f"沒有 profile {profile_name}")
    profile = profiles[profile_name]
    info = probe(path)
    video = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    audio = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
    duration = float(info["format"].get("duration", 0))
    checks: list[dict] = []

    if video is None:
        add(checks, "video_stream", False, "沒有影像串流")
    else:
        width, height = int(video["width"]), int(video["height"])
        if profile.get("width"):
            add(checks, "resolution", (width, height) == (profile["width"], profile["height"]),
                f"{width}x{height}，要 {profile['width']}x{profile['height']}")
            want = Fraction(profile["width"], profile["height"])
            add(checks, "aspect", Fraction(width, height) == want, f"{Fraction(width, height)}，要 {want}")
        if profile.get("max_long_edge"):
            add(checks, "resolution", max(width, height) <= profile["max_long_edge"],
                f"長邊 {max(width, height)}，上限 {profile['max_long_edge']}")
        add(checks, "video_codec", video.get("codec_name") in profile["video_codecs"],
            f"{video.get('codec_name')}，可用 {profile['video_codecs']}")
        if profile.get("pix_fmt"):
            add(checks, "pix_fmt", video.get("pix_fmt") == profile["pix_fmt"],
                f"{video.get('pix_fmt')}，要 {profile['pix_fmt']}")
        fps = float(Fraction(video.get("avg_frame_rate", "0/1"))) if video.get("avg_frame_rate", "0/0") != "0/0" else 0.0
        low, high = profile["fps"]
        add(checks, "fps", low <= fps <= high, f"{fps:.3f}，範圍 {low}–{high}")
        segments = black_segments(path)
        inner = [(s, e) for s, e in segments if s > EDGE_GRACE_S and e < duration - EDGE_GRACE_S]
        add(checks, "black_frames", not inner,
            "無" if not inner else "；".join(f"{s:.2f}–{e:.2f}s" for s, e in inner))
        jumps = flicker_frames(path)
        add(checks, "flicker", jumps == 0, f"亮度跳動 {jumps} 次（剪接點會誤報）", level="warn")

    if audio is None:
        add(checks, "audio_stream", False, "沒有音訊串流")
    else:
        add(checks, "audio_codec", audio.get("codec_name") in profile["audio_codecs"],
            f"{audio.get('codec_name')}，可用 {profile['audio_codecs']}")
        rate = int(audio.get("sample_rate", 0))
        add(checks, "sample_rate", rate in profile["sample_rates"], f"{rate} Hz，可用 {profile['sample_rates']}")
        peak = max_volume(path)
        add(checks, "audio_clipping", peak is not None and peak < CLIP_DBFS,
            f"峰值 {peak} dBFS，上限 {CLIP_DBFS}")

    add(checks, "duration", profile["min_s"] <= duration <= profile["max_s"],
        f"{duration:.2f}s，範圍 {profile['min_s']}–{profile['max_s']}s")
    failed = [c["check"] for c in checks if c["status"] == "fail"]
    safe = profile.get("safe_area_px")
    return {
        "file": str(path), "profile": profile_name, "pass": not failed, "failed": failed,
        "checks": checks, "manual_checks": MANUAL,
        "safe_area_note": (f"字幕與標題放在上 {safe['top']}、下 {safe['bottom']}、左 {safe['left']}、右 {safe['right']} px 以內"
                           if safe else "依平台／比賽規則；比賽版浮水印與 packshot 必須完整"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="影片機械檢查")
    parser.add_argument("file", type=Path)
    parser.add_argument("--profile", required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        print("需要 ffmpeg 與 ffprobe", file=sys.stderr)
        return 2
    try:
        report = check(args.file, args.profile)
    except (KeyError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
