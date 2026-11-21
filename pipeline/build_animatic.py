#!/usr/bin/env python3
"""Build an animatic MP4 from chosen keyframe stills and the shot IR durations.

Each shot is a slow centered push-in (Ken Burns) on its keyframe. A shot with an
end frame cross-fades from the keyframe to the end frame. The shot id, act and a
running timecode are burned in. Audio is silence or a quiet tone bed with a short
blip at every cut. Free: uses only ffmpeg on local stills.

    python3 pipeline/build_animatic.py projects/2026-11-proof-trailer
    python3 pipeline/build_animatic.py projects/2026-11-proof-trailer --placeholder --size 540x960
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

XFADE_S = 0.5
KEY_SHARE = 0.6


class AnimaticError(Exception):
    pass


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AnimaticError(f"ffmpeg 失敗：{' '.join(cmd[:6])}…\n{result.stderr[-1500:]}")


def find_font() -> str:
    for family in ("monospace", "sans"):
        result = subprocess.run(["fc-match", "-f", "%{file}", family], capture_output=True, text=True, check=False)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    raise AnimaticError("找不到字型（需要 fontconfig）")


def load_shots(project: Path) -> list[dict]:
    shots = json.loads((project / "shots.json").read_text(encoding="utf-8"))
    return sorted(shots, key=lambda shot: float(shot["start_s"]))


def load_selects(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["shot_id"]: row for row in csv.DictReader(handle)}


def make_placeholder(path: Path, label: str, size: tuple[int, int], font: str) -> None:
    w, h = size
    text = label.replace(":", r"\:")
    run(["ffmpeg", "-hide_banner", "-y", "-f", "lavfi", "-i", f"color=c=0x3a3f47:s={w}x{h}:d=1",
         "-vf", f"drawtext=fontfile={font}:text='{text}':fontcolor=white:fontsize={max(h // 16, 12)}:"
                f"x=(w-text_w)/2:y=(h-text_h)/2", "-frames:v", "1", str(path)])


def resolve_stills(project: Path, shots: list[dict], selects: dict[str, dict], placeholder: bool,
                   tmp: Path, size: tuple[int, int], font: str) -> dict[str, tuple[Path, Path | None]]:
    stills: dict[str, tuple[Path, Path | None]] = {}
    missing: list[str] = []
    for shot in shots:
        sid = shot["shot_id"]
        row = selects.get(sid, {})
        key_rel = row.get("keyframe") or shot.get("keyframe") or ""
        end_rel = row.get("endframe") or shot.get("endframe") or ""
        key = project / key_rel if key_rel else None
        end = project / end_rel if end_rel else None
        if key is None or not key.exists():
            if not placeholder:
                missing.append(f"{sid}: {key_rel or '（未指定）'}")
                continue
            key = tmp / f"{sid}_kf_placeholder.png"
            make_placeholder(key, f"{sid} KF", size, font)
        if end is not None and not end.exists():
            if placeholder:
                end_path = tmp / f"{sid}_ef_placeholder.png"
                make_placeholder(end_path, f"{sid} EF", size, font)
                end = end_path
            else:
                missing.append(f"{sid}: {end_rel}")
                continue
        stills[sid] = (key, end)
    if missing:
        raise AnimaticError("缺少靜幀（加 --placeholder 可用灰卡代替）：\n" + "\n".join(missing))
    return stills


def push_in(still: Path, out: Path, seconds: float, size: tuple[int, int], fps: int, zoom: float) -> None:
    w, h = size
    frames = max(int(round(seconds * fps)), 1)
    vf = (f"scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
          f"zoompan=z='1+{zoom - 1:.4f}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"d=1:s={w}x{h}:fps={fps},setsar=1,format=yuv420p")
    run(["ffmpeg", "-hide_banner", "-y", "-loop", "1", "-framerate", str(fps), "-t", f"{seconds:.3f}",
         "-i", str(still), "-vf", vf, "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "20", "-r", str(fps), str(out)])


def burn(src: Path, out: Path, shot: dict, start: float, size: tuple[int, int], fps: int, font: str) -> None:
    h = size[1]
    small = max(h // 40, 10)
    label = f"{shot['shot_id']}  ACT {shot['act']}  {start:05.1f}-{start + float(shot['duration_s']):05.1f}s"
    vf = (f"drawtext=fontfile={font}:text='{label}':fontcolor=white:fontsize={small}:box=1:boxcolor=black@0.55:"
          f"boxborderw={small // 3}:x={small}:y={small},"
          f"drawtext=fontfile={font}:text='TC %{{pts\\:hms\\:{start:.3f}}}':fontcolor=white:fontsize={small}:"
          f"box=1:boxcolor=black@0.55:boxborderw={small // 3}:x={small}:y=h-text_h-{small}")
    run(["ffmpeg", "-hide_banner", "-y", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps), str(out)])


def render_shot(shot: dict, key: Path, end: Path | None, start: float, tmp: Path,
                size: tuple[int, int], fps: int, zoom: float, font: str) -> Path:
    sid = shot["shot_id"]
    d = float(shot["duration_s"])
    raw = tmp / f"{sid}_raw.mp4"
    if end is None or d < 2 * XFADE_S + 0.5:
        push_in(key, raw, d, size, fps, zoom)
    else:
        a = round(d * KEY_SHARE + XFADE_S / 2, 3)
        b = round(d - a + XFADE_S, 3)
        ka, eb = tmp / f"{sid}_a.mp4", tmp / f"{sid}_b.mp4"
        push_in(key, ka, a, size, fps, zoom)
        push_in(end, eb, b, size, fps, zoom)
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(ka), "-i", str(eb), "-filter_complex",
             f"[0:v][1:v]xfade=transition=fade:duration={XFADE_S}:offset={a - XFADE_S:.3f},format=yuv420p",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(fps), str(raw)])
    final = tmp / f"{sid}.mp4"
    burn(raw, final, shot, start, size, fps, font)
    return final


def audio_input(kind: str, cuts: list[float], total: float) -> list[str]:
    if kind == "silent":
        return ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    blips = "+".join(f"between(t\\,{c:.3f}\\,{c + 0.08:.3f})" for c in cuts) or "0"
    expr = f"0.04*sin(2*PI*220*t)+0.25*sin(2*PI*880*t)*({blips})"
    return ["-f", "lavfi", "-t", f"{total:.3f}", "-i", f"aevalsrc=exprs='{expr}|{expr}':s=48000"]


def build(project: Path, out: Path, selects_path: Path | None = None, size: tuple[int, int] = (1080, 1920),
          fps: int = 24, zoom: float = 1.08, audio: str = "tone", placeholder: bool = False) -> dict:
    if not shutil.which("ffmpeg"):
        raise AnimaticError("需要 ffmpeg")
    font = find_font()
    shots = load_shots(project)
    if not shots:
        raise AnimaticError("shots.json 沒有鏡頭")
    selects = load_selects(selects_path or project / "selects.csv")
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        stills = resolve_stills(project, shots, selects, placeholder, tmp, size, font)
        parts, cuts, t = [], [], 0.0
        for shot in shots:
            key, end = stills[shot["shot_id"]]
            cuts.append(t)
            parts.append(render_shot(shot, key, end, t, tmp, size, fps, zoom, font))
            t += float(shot["duration_s"])
        listing = tmp / "list.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        video = tmp / "video.mp4"
        run(["ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(video)])
        out.parent.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-hide_banner", "-y", "-i", str(video), *audio_input(audio, cuts, t),
             "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
             "-t", f"{t:.3f}", "-movflags", "+faststart", str(out)])
    used = sum(1 for sid in stills if "placeholder" in stills[sid][0].name)
    return {"output": str(out), "shots": len(shots), "seconds": t, "placeholders": used}


def parse_size(raw: str) -> tuple[int, int]:
    w, h = raw.lower().split("x")
    if int(w) % 2 or int(h) % 2:
        raise argparse.ArgumentTypeError("寬高要是偶數")
    return int(w), int(h)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="用免費靜幀和 shots.json 的鏡長做 animatic")
    parser.add_argument("project", type=Path)
    parser.add_argument("--selects", type=Path, help="預設是專案的 selects.csv")
    parser.add_argument("--out", type=Path, help="預設是專案的 renders/animatic.mp4（不進 git）")
    parser.add_argument("--size", type=parse_size, default=(1080, 1920))
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--zoom", type=float, default=1.08, help="每鏡結束時的放大倍率")
    parser.add_argument("--audio", choices=["tone", "silent"], default="tone")
    parser.add_argument("--placeholder", action="store_true", help="缺圖時用灰卡代替")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    out = args.out or args.project / "renders" / "animatic.mp4"
    try:
        result = build(args.project, out, args.selects, args.size, args.fps, args.zoom, args.audio, args.placeholder)
    except (AnimaticError, OSError, KeyError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
