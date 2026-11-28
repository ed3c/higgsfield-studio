"""Sampled subtitle/audio alignment check for YT3 (handoff §13).

Pre-registered rule (fixed before looking at the S1 transcript):
- Sample K cues (deterministic seed) among cues whose text has >= MIN_CHARS
  non-space characters.
- For each cue, cut the audio window [start-PAD, end+PAD], transcribe it with a
  *different* Whisper checkpoint than the one that produced the SRT, and score
  character similarity (difflib ratio on normalized text) against the cue.
- Negative control: the same cue text against the window shifted by SHIFT_S.
- PASS if >= PASS_MIN of K aligned scores >= THRESH and mean(aligned) >
  mean(shifted) + MARGIN. Otherwise FAIL. This is an automated check, not a
  human listening review.
"""
from __future__ import annotations

import argparse
import difflib
import json
import random
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

from .yt_gates import parse_srt

K, MIN_CHARS, PAD, SHIFT_S, THRESH, PASS_MIN, MARGIN, SEED = 8, 6, 0.3, 15.0, 0.5, 6, 0.2, 20261127


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[\s\W_]+", "", s)


def cut(wav: Path, start: float, end: float, out: Path) -> None:
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{max(0, start):.3f}", "-to", f"{end:.3f}",
                    "-i", str(wav), "-ac", "1", "-ar", "16000", str(out)], check=True)


def run(srt: Path, wav: Path, model_name: str, language: str, duration: float) -> dict:
    import whisper  # admitted openai-whisper (MIT); imported lazily
    cues = parse_srt(srt.read_text(encoding="utf-8").lstrip("\ufeff"))
    pool = [c for c in cues if len(norm(c[3])) >= MIN_CHARS]
    rng = random.Random(SEED)
    sample = sorted(rng.sample(pool, min(K, len(pool))), key=lambda c: c[1])
    model = whisper.load_model(model_name, device="cpu")
    rows = []
    with tempfile.TemporaryDirectory() as d:
        for n, st, en, text in sample:
            out = {}
            for label, off in (("aligned", 0.0), ("shifted", SHIFT_S if en + SHIFT_S < duration else -SHIFT_S)):
                p = Path(d) / f"{n}_{label}.wav"
                cut(wav, st - PAD + off, en + PAD + off, p)
                hyp = model.transcribe(str(p), language=language, fp16=False, temperature=0,
                                       condition_on_previous_text=False)["text"]
                out[label] = {"hyp": hyp, "ratio": round(difflib.SequenceMatcher(None, norm(text), norm(hyp)).ratio(), 3)}
            rows.append({"cue": n, "start": st, "end": end_fmt(en), "text": text, **out})
    al = [r["aligned"]["ratio"] for r in rows]
    sh = [r["shifted"]["ratio"] for r in rows]
    passed = sum(a >= THRESH for a in al)
    ok = len(rows) == K and passed >= PASS_MIN and (sum(al) / len(al)) > (sum(sh) / len(sh)) + MARGIN
    return {"result": "PASS" if ok else "FAIL", "method": "sampled re-transcription with a different Whisper checkpoint + shifted-window negative control",
            "checker_model": model_name, "rule": {"K": K, "min_chars": MIN_CHARS, "pad_s": PAD, "shift_s": SHIFT_S,
            "thresh": THRESH, "pass_min": PASS_MIN, "margin": MARGIN, "seed": SEED},
            "aligned_pass": passed, "mean_aligned": round(sum(al) / len(al), 3) if al else None,
            "mean_shifted": round(sum(sh) / len(sh), 3) if sh else None, "samples": rows,
            "note": "automated check; not a human listening review"}


def end_fmt(x: float) -> float:
    return round(x, 3)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("srt"); ap.add_argument("wav"); ap.add_argument("--model", default="small")
    ap.add_argument("--language", default="ja"); ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    res = run(Path(a.srt), Path(a.wav), a.model, a.language, a.duration)
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("result", "aligned_pass", "mean_aligned", "mean_shifted")}))
    return 0 if res["result"] == "PASS" else 4


if __name__ == "__main__":
    raise SystemExit(main())
