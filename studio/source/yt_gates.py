"""Independent YT0–YT4 verifier for handoff §13 (HF-AGENTIC-FILM-2026-11-26).

Reads a per-source bundle directory produced by the acquisition step and
judges each gate from the bytes themselves (ffprobe/ffmpeg decode, SRT parse,
SHA-256 re-hash). It does not download anything and does not trust filenames,
exit codes or metadata alone.

Bundle layout (private, never in Git):
  rights.json            YT0 evidence (see REQUIRED_RIGHTS_FIELDS)
  <id>.mkv|.mp4|.webm    master with video+audio
  <id>.audio.wav         standalone PCM WAV extracted from the master
  <id>.<lang>.srt        original-language SRT (provenance in subtitles.json)
  subtitles.json         {"file","language","provenance": official|youtube_auto|asr, ...}
  <id>.info.json         downloader metadata
  media-probe.json       ffprobe output
  SHA256SUMS             sha256 of every artifact
  QA_REPORT.md

A gate whose prerequisite is not PASS is NOT_RUN (dependents pause only).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REQUIRED_RIGHTS_FIELDS = ("source_url", "video_id", "rights_holder", "permitted_operations",
                          "evidence", "confirmed_by", "confirmed_at")
NEEDED_OPS = {"download", "private_analysis"}
DURATION_TOL_S = 1.0       # master vs source metadata
WAV_TOL_S = 0.10           # WAV vs master audio stream (encoder delay/padding)
SRT_END_TOL_S = 2.0        # last cue end may exceed media by this much

_TS = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")


def _ts(s: str) -> float:
    h, m, sec, ms = map(int, _TS.fullmatch(s.strip()).groups())
    return h * 3600 + m * 60 + sec + ms / 1000


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def _probe(path: Path) -> dict[str, Any]:
    p = _run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:300])
    return json.loads(p.stdout)


def _decode_ok(path: Path, select: str) -> tuple[bool, str]:
    p = _run(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(path), "-map", select, "-f", "null", "-"])
    return p.returncode == 0 and not p.stderr.strip(), p.stderr.strip()[:300]


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def gate(state: str, **ev: Any) -> dict[str, Any]:
    return {"state": state, **ev}


def check_yt0(b: Path, video_id: str) -> dict[str, Any]:
    rp = b / "rights.json"
    if not rp.is_file():
        return gate("BLOCKED", reason="BLOCKED_SOURCE/RIGHTS: no rights.json (owner confirmation of source rights and permitted retrieval not recorded)")
    r = json.loads(rp.read_text(encoding="utf-8"))
    missing = [f for f in REQUIRED_RIGHTS_FIELDS if not r.get(f)]
    if missing:
        return gate("BLOCKED", reason=f"BLOCKED_SOURCE/RIGHTS: rights.json missing {missing}")
    if r.get("video_id") != video_id:
        return gate("FAIL", reason=f"rights.json is for {r.get('video_id')}, not {video_id}")
    ops = set(r.get("permitted_operations") or [])
    if not NEEDED_OPS <= ops:
        return gate("BLOCKED", reason=f"BLOCKED_SOURCE/RIGHTS: permitted_operations lacks {sorted(NEEDED_OPS - ops)}")
    return gate("PASS", rights_holder=r["rights_holder"], permitted_operations=sorted(ops),
                confirmed_by=r["confirmed_by"], confirmed_at=r["confirmed_at"])


def _find_master(b: Path, vid: str) -> Path | None:
    for ext in ("mkv", "mp4", "webm", "mov"):
        p = b / f"{vid}.{ext}"
        if p.is_file():
            return p
    return None


def check_yt1(b: Path, vid: str) -> dict[str, Any]:
    m = _find_master(b, vid)
    if not m or m.stat().st_size == 0:
        return gate("FAIL", reason="master missing or empty")
    pr = _probe(m)
    v = [s for s in pr["streams"] if s.get("codec_type") == "video"]
    a = [s for s in pr["streams"] if s.get("codec_type") == "audio"]
    if not v or not a:
        return gate("FAIL", reason=f"master needs video+audio, got v={len(v)} a={len(a)}")
    ok, err = _decode_ok(m, "0")
    if not ok:
        return gate("FAIL", reason=f"full decode error: {err}")
    dur = float(pr["format"]["duration"])
    info = b / f"{vid}.info.json"
    src_dur = ident = None
    if info.is_file():
        j = json.loads(info.read_text(encoding="utf-8"))
        src_dur, ident = j.get("duration"), j.get("id")
    if ident is not None and ident != vid:
        return gate("FAIL", reason=f"identity mismatch info.json id={ident}")
    if src_dur is None:
        return gate("FAIL", reason="no source duration (info.json) to check consistency")
    if abs(dur - float(src_dur)) > DURATION_TOL_S:
        return gate("FAIL", reason=f"duration {dur:.3f}s vs source {src_dur}s")
    return gate("PASS", file=m.name, duration_s=dur, source_duration_s=src_dur,
                video=f"{v[0].get('codec_name')} {v[0].get('width')}x{v[0].get('height')}",
                audio=f"{a[0].get('codec_name')} {a[0].get('sample_rate')}Hz ch={a[0].get('channels')}")


def check_yt2(b: Path, vid: str) -> dict[str, Any]:
    w = b / f"{vid}.audio.wav"
    m = _find_master(b, vid)
    if not w.is_file() or w.stat().st_size == 0:
        return gate("FAIL", reason="WAV missing or empty")
    pw = _probe(w)
    s = pw["streams"][0]
    if not str(s.get("codec_name", "")).startswith("pcm_"):
        return gate("FAIL", reason=f"not PCM: {s.get('codec_name')}")
    ok, err = _decode_ok(w, "0:a:0")
    if not ok:
        return gate("FAIL", reason=f"WAV decode error: {err}")
    ma = [x for x in _probe(m)["streams"] if x.get("codec_type") == "audio"][0]
    wd = float(pw["format"]["duration"])
    md = float(ma.get("duration") or _probe(m)["format"]["duration"])
    if int(s["sample_rate"]) != int(ma["sample_rate"]) or int(s["channels"]) != int(ma["channels"]):
        return gate("FAIL", reason=f"WAV {s['sample_rate']}Hz/{s['channels']}ch vs master {ma['sample_rate']}Hz/{ma['channels']}ch")
    if abs(wd - md) > WAV_TOL_S:
        return gate("FAIL", reason=f"WAV duration {wd:.3f}s vs master audio {md:.3f}s (> {WAV_TOL_S}s)")
    return gate("PASS", file=w.name, codec=s["codec_name"], sample_rate=int(s["sample_rate"]),
                channels=int(s["channels"]), duration_s=wd, master_audio_duration_s=md,
                delta_s=round(wd - md, 4))


def parse_srt(text: str) -> list[tuple[int, float, float, str]]:
    cues = []
    for block in re.split(r"\r?\n\r?\n+", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            raise ValueError(f"short cue block: {block[:60]!r}")
        n = int(lines[0].strip())
        a, _, z = lines[1].partition("-->")
        st, en = _ts(a), _ts(z)
        if en <= st:
            raise ValueError(f"cue {n} end<=start")
        cues.append((n, st, en, "\n".join(lines[2:])))
    return cues


def check_yt3(b: Path, vid: str, media_dur: float | None) -> dict[str, Any]:
    meta = b / "subtitles.json"
    if not meta.is_file():
        return gate("FAIL", reason="subtitles.json (language/provenance) missing")
    sm = json.loads(meta.read_text(encoding="utf-8"))
    if sm.get("provenance") not in ("official", "youtube_auto", "asr"):
        return gate("FAIL", reason=f"bad provenance {sm.get('provenance')!r}")
    if not sm.get("language") or not sm.get("is_original_language", False):
        return gate("FAIL", reason="original spoken language not declared/confirmed")
    f = b / sm["file"]
    try:
        raw = f.read_bytes()
        text = raw.decode("utf-8")
        cues = parse_srt(text.lstrip("\ufeff"))
    except Exception as exc:  # noqa: BLE001
        return gate("FAIL", reason=f"SRT unreadable: {exc}")
    if not cues:
        return gate("FAIL", reason="SRT empty")
    nums = [c[0] for c in cues]
    if nums != list(range(1, len(cues) + 1)):
        return gate("FAIL", reason="cue numbers not sequential from 1")
    starts = [c[1] for c in cues]
    if starts != sorted(starts):
        return gate("FAIL", reason="cue starts not chronological")
    if media_dur is not None and cues[-1][2] > media_dur + SRT_END_TOL_S:
        return gate("FAIL", reason=f"last cue ends {cues[-1][2]:.3f}s > media {media_dur:.3f}s + {SRT_END_TOL_S}s")
    align = sm.get("alignment_check")
    if not align or align.get("result") != "PASS":
        return gate("FAIL", reason="sampled subtitle/audio alignment check not recorded as PASS", cues=len(cues))
    return gate("PASS", file=f.name, cues=len(cues), language=sm["language"], provenance=sm["provenance"],
                last_end_s=cues[-1][2], alignment=align)


def check_yt4(b: Path, required: list[str]) -> dict[str, Any]:
    sums = b / "SHA256SUMS"
    if not sums.is_file():
        return gate("FAIL", reason="SHA256SUMS missing")
    listed = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, _, name = line.partition("  ")
            listed[name.strip().lstrip("./")] = h.strip()
    bad = [n for n, h in listed.items() if not (b / n).is_file() or _sha(b / n) != h]
    missing = [r for r in required if r not in listed]
    for need in ("QA_REPORT.md", "media-probe.json", "rights.json", "tool_versions.json"):
        if not (b / need).is_file():
            missing.append(need)
    if bad or missing:
        return gate("FAIL", reason=f"hash mismatch {bad} / missing {sorted(set(missing))}")
    return gate("PASS", hashed=len(listed))


def verify(bundle: Path, video_id: str) -> dict[str, Any]:
    g: dict[str, Any] = {}
    g["YT0"] = check_yt0(bundle, video_id)
    pause = lambda dep: gate("NOT_RUN", reason=f"depends on {dep} which is not PASS")  # noqa: E731
    g["YT1"] = check_yt1(bundle, video_id) if g["YT0"]["state"] == "PASS" else pause("YT0")
    ok1 = g["YT1"]["state"] == "PASS"
    g["YT2"] = check_yt2(bundle, video_id) if ok1 else pause("YT1")
    g["YT3"] = check_yt3(bundle, video_id, g["YT1"].get("duration_s")) if ok1 else pause("YT1")
    if all(g[k]["state"] == "PASS" for k in ("YT0", "YT1", "YT2", "YT3")):
        req = [g["YT1"]["file"], g["YT2"]["file"], g["YT3"]["file"]]
        g["YT4"] = check_yt4(bundle, req)
    else:
        g["YT4"] = pause("YT0-YT3")
    g["H01_acquisition_complete"] = all(g[k]["state"] == "PASS" for k in ("YT0", "YT1", "YT2", "YT3", "YT4"))
    return g


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Independent YT0–YT4 verifier (handoff §13)")
    ap.add_argument("bundle"); ap.add_argument("--video-id", required=True); ap.add_argument("--out")
    a = ap.parse_args(argv)
    res = verify(Path(a.bundle), a.video_id)
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(out + "\n", encoding="utf-8")
    print(out)
    return 0 if res["H01_acquisition_complete"] else 3


if __name__ == "__main__":
    sys.exit(main())
