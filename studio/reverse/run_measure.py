"""Stage 1 runner: parse pre-computed ffmpeg outputs, write measured JSON into the private pack dir."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from studio.reverse import film_baseline as fb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True, type=Path)
    ap.add_argument("--srt", required=True, type=Path)
    ap.add_argument("--duration", required=True, type=float)
    a = ap.parse_args()
    w = a.pack / "work"
    t, s = fb.parse_scene_scores(w / "scene_scores.txt")
    blacks = fb.parse_black(w / "passA.log")
    cuts, dropped = fb.detect_cuts(t, s, blacks)
    segs = fb.build_segments(cuts, blacks, a.duration)
    fr = fb.load_frames(w / "frames_2fps_160x90.rgb")
    fm = fb.frame_metrics(fr)
    cues = fb.parse_srt(a.srt)
    sil = fb.parse_silence(w / "passC.log")
    audio = fb.audio_measures(w / "audio_16k_mono.s16", a.duration, cues, sil)
    lt, lv = fb.parse_ebur128_m(w / "ebur128_M.txt")
    segs = fb.attach(segs, fm, fr, audio, lt, lv, cues)
    grad = fb.gradual_candidates(fr, segs)
    rhythm = fb.rhythm_and_sync(segs, cues, audio, a.duration)
    score_at = {round(c["t"], 3): c["score"] for c in cuts}
    for sg in segs:
        sg["in_cut_score"] = score_at.get(sg["start"])
    (a.pack / "shots").mkdir(exist_ok=True)
    (a.pack / "audio").mkdir(exist_ok=True)
    (a.pack / "transcript").mkdir(exist_ok=True)
    json.dump({"schema": "studio.reverse.segments.v1", "params": fb.PARAMS, "n_frames_2fps": len(fr.arr),
               "hard_cuts": cuts, "dropped_cut_candidates": dropped, "black_segments_ffmpeg": blacks,
               "segments": segs, "gradual_candidates": grad, "rhythm": rhythm},
              open(a.pack / "shots/segments.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"schema": "studio.reverse.audio_structure.v1", **audio,
               "integrated_loudness_ffmpeg": open(w / "passC.log").read().split("Summary:")[-1].strip()},
              open(a.pack / "audio/audio_structure.json", "w"), indent=1)
    align = []
    for c in cues:
        ov = [sg["id"] for sg in segs if fb._overlap(sg["start"], sg["end"], c["start"], c["end"]) > 0]
        align.append({"cue": c["index"], "start": c["start"], "end": c["end"], "segments": ov,
                      "spans_cut": len(ov) > 1, "n_chars": len(c["text"])})
    json.dump({"schema": "studio.reverse.cue_alignment.v1", "srt": str(a.srt.name), "cues": align},
              open(a.pack / "transcript/cue_segment_alignment.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rhythm, indent=1))
    print("segments", len(segs), "gradual", len(grad), "dropped", len(dropped))


if __name__ == "__main__":
    main()
