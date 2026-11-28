"""Deterministic post-filter for Whisper ASR on mostly non-speech media.

Whisper is known to emit stock phrases over music/silence windows. This filter
drops a segment only when one of these pre-registered rules holds (fixed on
2026-11-27 before the YT3 alignment check ran):

  R1  duration >= 20 s AND no_speech_prob >= 0.6      (whole 30 s window over non-speech)
  R2  normalized text in KNOWN_HALLUCINATIONS AND no_speech_prob >= 0.6
  R3  no_speech_prob >= 0.85 AND avg_logprob <= -0.5

It also clamps cue ends to the media duration. The raw Whisper output is kept
unchanged next to the filtered SRT, and every dropped segment is logged.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

KNOWN_HALLUCINATIONS = {"ご視聴ありがとうございました", "おやすみなさい", "アーメン", "作詞・作曲・編曲 初音ミク"}


def fmt(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600_000); m, ms = divmod(ms, 60_000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def rule(seg: dict) -> str | None:
    d = seg["end"] - seg["start"]
    nsp, lp, txt = seg["no_speech_prob"], seg["avg_logprob"], seg["text"].strip()
    if d >= 20 and nsp >= 0.6:
        return "R1"
    if txt in KNOWN_HALLUCINATIONS and nsp >= 0.6:
        return "R2"
    if nsp >= 0.85 and lp <= -0.5:
        return "R3"
    return None


def run(whisper_json: Path, duration: float, out_srt: Path, out_log: Path) -> dict:
    segs = json.loads(whisper_json.read_text(encoding="utf-8"))["segments"]
    kept, dropped = [], []
    for s in segs:
        r = rule(s)
        (dropped if r else kept).append((r, s))
    lines = []
    n = 0
    for _, s in kept:
        st, en = s["start"], min(s["end"], duration)
        if en <= st or not s["text"].strip():
            dropped.append(("EMPTY_OR_OUT_OF_RANGE", s)); continue
        n += 1
        lines.append(f"{n}\n{fmt(st)} --> {fmt(en)}\n{s['text'].strip()}\n")
    out_srt.write_text("\n".join(lines), encoding="utf-8")
    log = {"rules": __doc__.split("\n\n")[1], "input_segments": len(segs), "kept": n, "dropped": len(dropped),
           "dropped_segments": [{"rule": r, "start": s["start"], "end": s["end"], "no_speech_prob": round(s["no_speech_prob"], 3),
                                 "avg_logprob": round(s["avg_logprob"], 3), "text": s["text"].strip()} for r, s in dropped]}
    out_log.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return log


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("whisper_json"); ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--out-srt", required=True); ap.add_argument("--out-log", required=True)
    a = ap.parse_args()
    lg = run(Path(a.whisper_json), a.duration, Path(a.out_srt), Path(a.out_log))
    print(json.dumps({k: lg[k] for k in ("input_segments", "kept", "dropped")}))
