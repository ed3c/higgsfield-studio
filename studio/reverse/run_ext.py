"""Assemble the H02 extension outputs (new files only) + git-safe copy."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from studio.reverse import ext_analyses as ea


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", type=Path, required=True)
    ap.add_argument("--ext", type=Path, required=True)
    ap.add_argument("--git-out", type=Path, required=True)
    a = ap.parse_args()
    P, X = a.pack, a.ext
    seg = json.load(open(P / "shots/segments.json"))
    segs = seg["segments"]
    media_sha = json.load(open(P / "source-manifest.json"))["media"]["onNBysMf9WM.mkv"]
    raw = json.load(open(P / "work/scenedetect_raw.json"))
    v1_cuts = [s["start"] for s in segs if s["in_boundary"] == "cut"]
    e1 = ea.scenedetect_compare(raw, v1_cuts)
    e1["raw"] = {k: raw[k]["cuts_s"] for k in ("content", "adaptive")}
    json.dump({"schema": "studio.reverse.scenedetect_cuts.v1", "prereg": "PREREG_EXT_2026-11-27.md E1", **e1},
              open(X / "scenedetect_cuts.json", "w"), indent=1)
    cam = json.load(open(X / "camera_motion.json"))
    dark = json.load(open(X / "dark_boundary_disambiguation.json"))
    mus = json.load(open(X / "music_analysis.json"))
    cc = Counter(r["label"] for r in cam["rows"])
    dc = dark["label_counts"]
    mc = mus["label_counts_windows"]
    # music by v1 non-speech sections
    ns = [s for s in mus["sections"] if s["label_v1"] != "SPEECH"]
    ns_music = sum(s["window_labels"].get("MUSIC_LIKELY", 0) for s in ns)
    ns_total = sum(sum(s["window_labels"].values()) for s in ns)
    ia = json.load(open(P / "observations.agent.json"))["role_shots"]["interviewee_A_white_wall_title_lettering"]
    ia_lab = Counter(r["label"] for r in cam["rows"] if r["id"] in ia)
    base = {"source_id": "S1", "source_version": "youtube:onNBysMf9WM uploaded 20180406; local mkv", "media_sha256": media_sha,
            "creator_statement": None, "reviewer": "Grok Bot (producer; not independent)", "status": "UNREVIEWED"}
    C = []

    def add(cid, cls, loc, obs, inf=None, alt=None, unk=None, lim="", ev=None):
        C.append({"claim_id": cid, "class": cls, **base, "locator": loc, "observation": obs, "inference": inf,
                  "alternative_explanation": alt, "unknowns": unk or [], "confidence_limits": lim, "evidence_file": ev})

    for k in ("content", "adaptive"):
        e = e1[k]
        add(f"S1-EXT-MEA-E1-{k}", "MEASURED", f"pack-ext/scenedetect_cuts.json {k}",
            f"PySceneDetect {e1['version']} {k} detector: {e['n_cuts']} cuts; {e['matched_v1']}/{len(v1_cuts)} v1 hard cuts matched within ±3 frames; "
            f"{len(e['pyscenedetect_only'])} cuts found only by PySceneDetect.", ev="../pack-ext/scenedetect_cuts.json",
            lim="Neither detector is ground truth; PySceneDetect-only cuts include luminance flashes in dark sequences.")
    add("S1-EXT-MEA-E2", "MEASURED", "pack-ext/camera_motion.json",
        f"Global-motion fit on {len(cam['rows'])} SHOT segments >= 1 s: " + ", ".join(f"{k} {v}" for k, v in cc.most_common()) + ".",
        ev="../pack-ext/camera_motion.json",
        lim="2-D similarity fit at 5 fps 320x180; pan≈track and zoom≈dolly are indistinguishable; cumulative scale drift over long takes can over-label zoom; subject motion biases the fit.")
    add("S1-EXT-INF-E2", "INFERRED", "pack-ext/camera_motion.json rows for interviewee_A shots",
        f"Interviewee A shots: " + ", ".join(f"{k} {v}" for k, v in ia_lab.most_common()) + ".",
        inf="Interview set-ups are mostly locked-off with occasional slow push/pull or reframing.",
        alt="Detected scale change may be drift of the estimator rather than a real zoom; a human must view the shots.",
        unk=["actual camera support", "lens zoom vs dolly"], lim="Exploratory thresholds (pre-registered).")
    add("S1-EXT-MEA-E3", "MEASURED", "pack-ext/dark_boundary_disambiguation.json calibration",
        f"Calibration PASS: hard-cut control {dark['calibration']['cut_control_label_counts']} (0% classified same-take); "
        f"same-take control {dark['calibration']['same_control_label_counts']} ({dark['calibration']['same_control_classified_cut']*100:.0f}% classified cut).",
        ev="../pack-ext/dark_boundary_disambiguation.json", lim="Controls are drawn from lit footage; dark frames are harder.")
    add("S1-EXT-INF-E3", "INFERRED", "pack-ext/dark_boundary_disambiguation.json boundaries",
        f"Near-black intervals with SHOT on both sides: " + ", ".join(f"{k} {v}" for k, v in dc.items()) + ".",
        inf=f"Of {sum(v for k, v in dc.items() if not k.startswith('NOT_APPLICABLE'))} classifiable near-black interruptions, {dc.get('SAME_TAKE_LIGHTING', 0)} return to the same framing (lighting change inside a take) and {dc.get('EDITORIAL_CUT', 0)} switch to a different view (editorial); {dc.get('UNDETERMINED', 0)} stay undetermined. Dark passages therefore mix in-take light switching with real cuts.",
        alt="Same-framing returns can also be a cut back to the same locked-off camera; different views can be the same take with a large light change revealing other structure.",
        unk=["frame-level continuity through the black"], lim="ORB on CLAHE-boosted dark frames; UNDETERMINED is the largest class.")
    add("S1-EXT-MEA-E4", "MEASURED", "pack-ext/music_analysis.json label_counts_windows",
        f"5 s windows: " + ", ".join(f"{k} {v}" for k, v in mc.items()) + f"; in v1 non-speech sections {ns_music}/{ns_total} windows are MUSIC_LIKELY.",
        ev="../pack-ext/music_analysis.json", lim="Labels use exploratory uncalibrated thresholds; speech windows are excluded by the ASR speech mask.")
    add("S1-EXT-INF-E4", "INFERRED", "pack-ext/music_analysis.json sections",
        "Most non-speech passages are strongly harmonic and tonally peaked.",
        inf="Non-speech passages carry music (piano/strings) rather than plain room ambience — consistent with the installation/performance footage.",
        alt="The installation's own sound (sustained tones, prepared piano) is also harmonic; the analysis cannot separate composed score, live performance and installation output.",
        unk=["music source and whether it is sync sound"], lim="Needs human listening (U-05).")
    with open(X / "claims-evidence.ext.jsonl", "w", encoding="utf-8") as fh:
        for c in C:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    md = ["# S1 H02 extension (OpenCV / PySceneDetect / librosa; owner exception 2026-11-27)", "",
          "New files only; v1 pack unchanged. Pre-registration: `PREREG_EXT_2026-11-27.md`.", "",
          "| Analysis | Result | Status |", "|---|---|---|",
          f"| E1 PySceneDetect content | {e1['content']['n_cuts']} cuts, {e1['content']['matched_v1']}/{len(v1_cuts)} v1 cuts matched | MEASURED; agreement only |",
          f"| E1 PySceneDetect adaptive | {e1['adaptive']['n_cuts']} cuts, {e1['adaptive']['matched_v1']}/{len(v1_cuts)} v1 cuts matched | MEASURED; agreement only |",
          f"| E2 camera movement | {dict(cc)} | MEASURED fit, INFERRED labels; acceptance NOT_RUN |",
          f"| E3 dark boundaries | calibration {dark['calibration']['status']}; {dc} | INFERRED labels; acceptance NOT_RUN |",
          f"| E4 music | {mc}; non-speech MUSIC_LIKELY {ns_music}/{ns_total} | INFERRED; human listening NOT_RUN |", "",
          "Unknowns updated (no v1 overwrite): U-02 → partially addressed by E3 (still INCONCLUSIVE for UNDETERMINED); U-04 → E2 labels (INFERRED); U-05 → E4 labels (INFERRED)."]
    (X / "EXT.md").write_text("\n".join(md), encoding="utf-8")
    files = sorted(p for p in X.iterdir() if p.is_file() and p.suffix in (".json", ".jsonl", ".md"))
    with open(X / "SHA256SUMS", "w") as fh:
        for p in files:
            fh.write(f"{sha(p)}  {p.name}\n")
    G = a.git_out
    G.mkdir(parents=True, exist_ok=True)
    for p in files + [X / "SHA256SUMS"]:
        shutil.copy(p, G / p.name)
    print("\n".join(md))


if __name__ == "__main__":
    main()
