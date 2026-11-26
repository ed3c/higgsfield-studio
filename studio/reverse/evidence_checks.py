"""Pre-registered automated checks O1–O6 for a Reverse Evidence Pack.

Spec: docs/handoff/agentic-film-production/runs/2026-11-27-h02-s1/ORACLE_PREREG_S1_H02.md
(committed before this file ran). Independent-algorithm checks only: never marks V2 PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

FPS = 30000 / 1001
REQUIRED_CLAIM_FIELDS = ["claim_id", "source_id", "source_version", "media_sha256", "locator", "observation",
                         "inference", "alternative_explanation", "unknowns", "confidence_limits",
                         "creator_statement", "reviewer", "status", "class"]
CLASSES = {"SOURCE_EVIDENCE", "MEASURED", "INFERRED", "UNVERIFIED_CLAIM", "UNKNOWN"}
FORBIDDEN_FACT = re.compile(r"\b(focal length|\d+\s?mm lens|lens is|seed|prompt was|camera path|model parameter)", re.I)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def window_diffs(mkv: Path, t: float, half=0.25):
    ss = max(0.0, t - half)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(mkv), "-t", f"{2 * half:.3f}",
           "-an", "-vf", "scale=64:36,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 36, 64).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
    centre = int(round((t - ss) * FPS))  # frame index of the expected cut (first frame of new shot)
    return d, centre


def judge(d, centre):
    # diff index k compares frame k and k+1; cut between centre-1 and centre -> k = centre-1
    k0 = centre - 1
    near = [k for k in range(k0 - 2, k0 + 3) if 0 <= k < len(d)]
    far = [k for k in range(len(d)) if k not in near]
    if not near or not far:
        return None
    d_cut = float(d[near].max())
    d_base = float(np.median(d[far]))
    ok = d_cut >= 8.0 and d_cut >= 3 * max(d_base, 0.5)
    return {"d_cut": round(d_cut, 3), "d_base": round(d_base, 3), "confirmed": bool(ok)}


def o3(mkv: Path, segs, duration, seed=20261127, workers=4):
    cuts = [s["start"] for s in segs["segments"] if s["in_boundary"] == "cut"]
    bounds = sorted({s["start"] for s in segs["segments"]} | {s["end"] for s in segs["segments"]})
    rng = np.random.default_rng(seed)
    neg = []
    tries = 0
    while len(neg) < len(cuts) and tries < 100000:
        tries += 1
        t = float(rng.uniform(2, duration - 2))
        if min(abs(b - t) for b in bounds) >= 2.0:
            neg.append(round(t, 3))

    def run(t):
        d, c = window_diffs(mkv, t)
        r = judge(d, c)
        return {"t": t, **(r or {"confirmed": None, "error": "window too short"})}

    with ThreadPoolExecutor(workers) as ex:
        pos = list(ex.map(run, cuts))
        negr = list(ex.map(run, neg))
    pf = np.mean([r["confirmed"] is True for r in pos]) if pos else None
    nf = np.mean([r["confirmed"] is True for r in negr]) if negr else None
    return {"positives": pos, "negatives": negr, "confirmed_fraction": round(float(pf), 4),
            "negative_false_confirm_fraction": round(float(nf), 4),
            "O3": "PASS" if pf is not None and pf >= 0.90 else "FAIL",
            "O3n": "PASS" if nf is not None and nf <= 0.10 else "FAIL",
            "n_negative_tries": tries}


def o2(segs, duration):
    s = segs["segments"]
    ok = s[0]["start"] == 0 and abs(s[-1]["end"] - duration) <= 1 / FPS
    ok &= all(a["end"] == b["start"] for a, b in zip(s, s[1:]))
    ok &= all(x["start"] < x["end"] for x in s)
    return {"O2": "PASS" if ok else "FAIL", "n_segments": len(s), "last_end": s[-1]["end"], "duration": duration}


def o5(claims_path: Path, pack: Path):
    errs = []
    n = 0
    for line in open(claims_path, encoding="utf-8"):
        if not line.strip():
            continue
        n += 1
        c = json.loads(line)
        cid = c.get("claim_id", f"line{n}")
        for f in REQUIRED_CLAIM_FIELDS:
            if f not in c:
                errs.append(f"{cid}: missing {f}")
        if c.get("class") not in CLASSES:
            errs.append(f"{cid}: bad class {c.get('class')}")
        if c.get("class") == "MEASURED":
            ev = c.get("evidence_file")
            if not ev or not (pack / ev).exists():
                errs.append(f"{cid}: MEASURED evidence_file missing {ev}")
        if c.get("class") == "INFERRED":
            if not c.get("alternative_explanation") or not c.get("unknowns"):
                errs.append(f"{cid}: INFERRED without alternative/unknowns")
        if c.get("class") in ("MEASURED", "SOURCE_EVIDENCE") and FORBIDDEN_FACT.search(
                f'{c.get("observation", "")} {c.get("inference", "")}'):
            errs.append(f"{cid}: forbidden factual claim (lens/seed/prompt/camera path)")
    return {"O5": "PASS" if not errs and n else "FAIL", "n_claims": n, "errors": errs[:50]}


def o6(git_files, srt_cues):
    errs = []
    media_ext = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mkv", ".wav", ".opus", ".m4a", ".rgb", ".s16"}
    texts = [c for c in srt_cues if len(c) >= 8]
    for f in git_files:
        p = Path(f)
        if p.suffix.lower() in media_ext:
            errs.append(f"media file in git set: {f}")
            continue
        body = p.read_text(encoding="utf-8", errors="replace")
        if body.startswith("\xff\xd8") or "data:image" in body:
            errs.append(f"embedded image bytes: {f}")
        for t in texts:
            if t in body:
                errs.append(f"verbatim cue text in {f}: {t[:12]}…")
                break
    return {"O6": "PASS" if not errs else "FAIL", "n_files": len(git_files), "errors": errs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", type=Path, required=True)
    ap.add_argument("--mkv", type=Path, required=True)
    ap.add_argument("--wav", type=Path, required=True)
    ap.add_argument("--srt", type=Path, required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--expect", nargs=3, required=True, metavar=("MKV_SHA", "WAV_SHA", "SRT_SHA"))
    ap.add_argument("--git-files", nargs="*", default=[])
    ap.add_argument("--only", nargs="*", default=["O1", "O2", "O3", "O4", "O5", "O6"])
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    from studio.reverse.film_baseline import parse_srt
    segs = json.load(open(a.pack / "shots/segments.json"))
    res = {"prereg": "docs/handoff/agentic-film-production/runs/2026-11-27-h02-s1/ORACLE_PREREG_S1_H02.md",
           "kind": "automated independent-algorithm checks; NOT a human Oracle; never marks V2"}
    if "O1" in a.only:
        got = [sha256(a.mkv), sha256(a.wav), sha256(a.srt)]
        res["O1"] = {"status": "PASS" if got == a.expect else "FAIL", "got": got, "expected": a.expect}
    if "O2" in a.only:
        res["O2"] = o2(segs, a.duration)
    if "O4" in a.only:
        pr = json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(a.wav)],
                                       capture_output=True, check=True).stdout)
        wd = float(pr["format"]["duration"])
        cues = parse_srt(a.srt)
        inside = all(0 <= c["start"] < c["end"] <= a.duration for c in cues)
        res["O4"] = {"status": "PASS" if abs(wd - a.duration) <= 0.10 and inside else "FAIL",
                     "wav_duration": wd, "mkv_duration": a.duration, "cues_inside": inside, "n_cues": len(cues)}
    if "O5" in a.only:
        res["O5"] = o5(a.pack / "claims-evidence.jsonl", a.pack)
    if "O6" in a.only:
        res["O6"] = o6(a.git_files, [c["text"] for c in parse_srt(a.srt)])
    if "O3" in a.only:
        res["O3"] = o3(a.mkv, segs, a.duration)
    a.out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({k: (v.get("status") or v.get("O2") or v.get("O5") or v.get("O6") or
                          (v.get("O3"), v.get("O3n"), v.get("confirmed_fraction"), v.get("negative_false_confirm_fraction")))
                      if isinstance(v, dict) else v for k, v in res.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
