"""Assemble the handoff §4 Reverse Evidence Pack from measured JSON + agent observations.

Inputs are produced by run_measure.py (MEASURED) and a separate observations file (INFERRED,
producer agent, not independent). Writes the 16 §4 artefacts into --pack. Large/private
artefacts (keyframes, SRT text, raw frames) stay in the private pack; --git-out receives only
small, frame-free, transcript-text-free files.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path

import numpy as np
import opentimelineio as otio

RATE = 30000 / 1001


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def snap(t, starts):
    return min(starts, key=lambda s: abs(s - t))


class Claims:
    def __init__(self, src_id, version, media_sha):
        self.rows = []
        self.base = {"source_id": src_id, "source_version": version, "media_sha256": media_sha,
                     "creator_statement": None}

    def add(self, cid, cls, locator, observation, inference=None, alternative=None, unknowns=None,
            limits="", evidence_file=None, reviewer="Grok Bot (producer; not independent)", status="UNREVIEWED"):
        self.rows.append({"claim_id": cid, "class": cls, **self.base, "locator": locator,
                          "observation": observation, "inference": inference,
                          "alternative_explanation": alternative, "unknowns": unknowns or [],
                          "confidence_limits": limits, "evidence_file": evidence_file,
                          "reviewer": reviewer, "status": status})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", type=Path, required=True)
    ap.add_argument("--staging", type=Path, required=True)
    ap.add_argument("--source-id", default="S1")
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--drive-folder", required=True)
    ap.add_argument("--handoff-pin", required=True)
    ap.add_argument("--checks", type=Path, required=True)
    ap.add_argument("--git-out", type=Path, required=True)
    ap.add_argument("--n-frames", type=int, required=True, help="decoded frame count (full-decode evidence)")
    a = ap.parse_args()
    P, S, vid = a.pack, a.staging, a.video_id

    seg = json.load(open(P / "shots/segments.json"))
    aud = json.load(open(P / "audio/audio_structure.json"))
    cal = json.load(open(P / "transcript/cue_segment_alignment.json"))
    obs = json.load(open(P / "observations.agent.json"))
    info = json.load(open(S / f"{vid}.info.json"))
    probe = json.load(open(S / "media-probe.json"))
    rights = json.load(open(S / "rights.json"))
    tools = json.load(open(S / "tool_versions.json"))
    pf = json.load(open(S / "asr_postfilter_log.json"))
    checks = json.load(open(a.checks))
    sums = dict(reversed(l.split()) for l in open(S / "SHA256SUMS") if l.strip())
    media_sha = sums[f"{vid}.mkv"]
    duration = float(probe["format"]["duration"])
    segs = seg["segments"]
    starts = [s["start"] for s in segs]
    by_id = {s["id"]: s for s in segs}

    # ---- sequences (agent observation) snapped to measured segment boundaries
    seqs = []
    for q in obs["sequences"]:
        q = dict(q)
        q["start_snapped"] = snap(q["start"], starts)
        seqs.append(q)
    for q, nxt in zip(seqs, seqs[1:] + [None]):
        q["end_snapped"] = nxt["start_snapped"] if nxt else duration
        members = [s for s in segs if q["start_snapped"] <= s["start"] < q["end_snapped"]]
        q["segments"] = [s["id"] for s in members]
        dur = q["end_snapped"] - q["start_snapped"]
        sp = sum(min(1, s["audio"]["speech_fraction"]) * s["duration"] for s in members)
        q["measured"] = {"duration": round(dur, 3), "n_segments": len(members),
                         "n_shot": sum(s["kind"] == "SHOT" for s in members),
                         "n_hard_cuts": sum(s["in_boundary"] == "cut" for s in members),
                         "speech_fraction": round(sp / dur, 3) if dur else None,
                         "luma_mean_timeweighted": round(sum(s["visual"]["luma_mean"] * s["duration"] for s in members) / dur, 2)}
        for s in members:
            s["sequence"] = q["id"]
    role_of = {}
    for role, ids in obs["role_shots"].items():
        for i in ids:
            role_of[i] = role

    # ---- reverse-ir.json (Soodles higgsfield-studio route table: source/observation/inference/unknown/controls/acceptance)
    ir_rows = []
    for s in segs:
        v = s["visual"]
        near_black = s["kind"] == "BLACK"
        reliability = "HIGH (hard cut, O3-confirmed)" if s["in_boundary"] == "cut" else (
            "LOW: luminance-threshold boundary (blackdetect); may be light switching inside one take, not an editorial cut"
            if s["in_boundary"] in ("black_start", "black_end") else "START")
        ir_rows.append({
            "id": s["id"], "kind": "NEAR_BLACK" if near_black else "SHOT", "sequence": s.get("sequence"),
            "tc_in": s["tc_in"], "tc_out": s["tc_out"], "start_s": s["start"], "end_s": s["end"],
            "frame_in": s["frame_in"], "frame_out_excl": s["frame_out_excl"], "duration_s": s["duration"],
            "boundary_in": s["in_boundary"], "boundary_reliability": reliability, "cut_score": s.get("in_cut_score"),
            "source": {"media_sha256": media_sha, "keyframe": f"keyframes/{s['id']}.jpg (private)"},
            "measured": {"visual": v, "audio": s["audio"]},
            "observed_inferred": {
                "role": role_of.get(s["id"]),
                "sequence_label": next((q["label"] for q in seqs if q["id"] == s.get("sequence")), None),
                "shot_scale": next((q["shot_scale_hint"] for q in seqs if q["id"] == s.get("sequence")), None),
                "class": "INFERRED", "observer": "Grok Bot (not independent)"},
            "unknown": ["lens / focal length", "camera body and settings", "camera path (still frame)",
                        "grade / post pipeline", "whether sound is sync or laid"],
            "studio_controls_checkable": ["shot duration", "cut position", "average luminance / saturation range",
                                          "speech-on-cut alignment", "long-take vs cut density"],
            "acceptance": {"boundary": "O3 automated" if s["in_boundary"] == "cut" else "NOT_RUN (human)",
                           "inference": "NOT_RUN (independent reviewer, V2)"},
        })
    ir = {"schema": "studio.reverse.ir.v1", "source_id": a.source_id, "video_id": vid, "media_sha256": media_sha,
          "route": "Soodles skills/reverse-route/routes/higgsfield-studio.md @939875f (scene/shot table fields) via "
                   "Studio-specific HF-Q01 adapter studio/reverse/ (route itself excludes FFmpeg-dependent tools)",
          "rate": "30000/1001", "duration_s": duration, "sequences": seqs, "segments": ir_rows,
          "rhythm": seg["rhythm"], "gradual_candidates": seg["gradual_candidates"]}
    json.dump(ir, open(P / "reverse-ir.json", "w"), ensure_ascii=False, indent=1)

    # ---- timeline.otio
    tl = otio.schema.Timeline(name=f"{a.source_id} {vid} reverse timeline (measured segments)")
    ref = otio.schema.ExternalReference(target_url=f"private://afp/{a.source_id}/{vid}.mkv",
                                        available_range=otio.opentime.TimeRange(
                                            otio.opentime.RationalTime(0, RATE),
                                            otio.opentime.RationalTime(a.n_frames, RATE)))
    ref.metadata["sha256"] = media_sha
    vt = otio.schema.Track(name="V1 measured segments", kind=otio.schema.TrackKind.Video)
    for s in segs:
        clip = otio.schema.Clip(name=s["id"], media_reference=ref.clone(),
                                source_range=otio.opentime.TimeRange(
                                    otio.opentime.RationalTime(s["frame_in"], RATE),
                                    otio.opentime.RationalTime(min(s["frame_out_excl"], a.n_frames) - s["frame_in"], RATE)))
        clip.metadata["afp"] = {"kind": s["kind"], "boundary_in": s["in_boundary"], "sequence": s.get("sequence")}
        vt.append(clip)
    at = otio.schema.Track(name="A1 speech cues (post-filtered ASR; timing only)", kind=otio.schema.TrackKind.Audio)
    cur = 0
    for c in sorted(cal["cues"], key=lambda c: c["start"]):
        fi, fo = round(c["start"] * RATE), round(c["end"] * RATE)
        if fi < cur:
            fi = cur
        if fo <= fi:
            continue
        if fi > cur:
            at.append(otio.schema.Gap(source_range=otio.opentime.TimeRange(
                otio.opentime.RationalTime(0, RATE), otio.opentime.RationalTime(fi - cur, RATE))))
        cl = otio.schema.Clip(name=f"cue{c['cue']}", media_reference=otio.schema.MissingReference(),
                              source_range=otio.opentime.TimeRange(otio.opentime.RationalTime(fi, RATE),
                                                                   otio.opentime.RationalTime(fo - fi, RATE)))
        at.append(cl)
        cur = fo
    for g in seg["gradual_candidates"]:
        m = otio.schema.Marker(name="CANDIDATE_GRADUAL", marked_range=otio.opentime.TimeRange(
            otio.opentime.RationalTime(round(g["t_start"] * RATE), RATE),
            otio.opentime.RationalTime(max(1, round((g["t_end"] - g["t_start"]) * RATE)), RATE)))
        m.metadata["afp"] = {"class": "INFERRED", "max_l1": g["max_l1"]}
        vt.markers.append(m)
    tl.tracks.append(vt)
    tl.tracks.append(at)
    otio.adapters.write_to_file(tl, str(P / "timeline.otio"))

    # ---- claims
    C = Claims(a.source_id, f"youtube:{vid} uploaded {info.get('upload_date')}; local mkv", media_sha)
    C.add("S1-SRC-001", "SOURCE_EVIDENCE", f"{vid}.info.json title/channel/upload_date",
          f"Title「{info['title']}」; channel {info['channel']}; uploaded {info['upload_date']}; duration {info['duration']} s.",
          limits="Platform metadata as fetched 2026-11-26/27 UTC+8.")
    C.add("S1-UVC-001", "UNVERIFIED_CLAIM", f"{vid}.description",
          "Channel description states the work is ICC exhibition documentation, exhibition period 2017-12-09 – 2018-03-11, ICC Gallery A.",
          inference=None, alternative="Statement by the uploading channel; not independently verified here.",
          unknowns=["director/editor credits", "shooting dates per shot"], limits="Channel statement only.")
    vs = next(s for s in probe["streams"] if s["codec_type"] == "video")
    C.add("S1-MEA-001", "MEASURED", "media-probe.json streams[0], format.duration",
          f"Video {vs['codec_name']} {vs['width']}x{vs['height']} @ {vs['r_frame_rate']}; duration {duration:.3f} s; "
          f"full decode 69,931 frames.", evidence_file="media-probe.json", limits="This is the YouTube delivery encode, not a master.")
    r = seg["rhythm"]
    C.add("S1-MEA-002", "MEASURED", "shots/segments.json rhythm, hard_cuts",
          f"{r['n_hard_cuts']} hard cuts (scene score >= 0.30); {r['n_shots']} SHOT and {r['n_black_segments']} NEAR_BLACK segments; "
          f"O3 automated re-check confirmed {checks['O3']['confirmed_fraction']*100:.0f}% of hard cuts, negative control false-confirm "
          f"{checks['O3']['negative_false_confirm_fraction']*100:.0f}%.", evidence_file="shots/segments.json",
          limits="Recall of dissolves/soft cuts NOT_RUN; near-black boundaries are luminance crossings.")
    sd = r["shot_duration_s"]
    C.add("S1-MEA-003", "MEASURED", "shots/segments.json rhythm.shot_duration_s",
          f"Segment duration (SHOT kind): mean {sd['mean_ASL']} s, median {sd['median']} s, p10 {sd['p10']} s, p90 {sd['p90']} s, max {sd['max']} s.",
          evidence_file="shots/segments.json",
          limits="Mean/median are depressed by sub-second luminance fragments in dark sequences (Q06/Q08/Q15/Q19); see S1-INF-002.")
    hard_shots = [s for s in segs if s["kind"] == "SHOT"]
    top = sorted(hard_shots, key=lambda s: -s["duration"])[:8]
    C.add("S1-MEA-004", "MEASURED", "; ".join(f"{s['id']}@{s['tc_in']}" for s in top),
          "Longest segments: " + ", ".join(f"{s['id']} {s['duration']:.1f}s" for s in top) + ".",
          evidence_file="shots/segments.json", limits="A segment can contain an undetected dissolve.")
    zero = sum(1 for x in r["cuts_per_minute"] if x == 0)
    C.add("S1-MEA-005", "MEASURED", "shots/segments.json rhythm.cuts_per_minute",
          f"Hard cuts per minute range 0–{max(r['cuts_per_minute'])}; {zero} of {len(r['cuts_per_minute'])} minutes contain no hard cut.",
          evidence_file="shots/segments.json")
    C.add("S1-MEA-006", "MEASURED", "audio/audio_structure.json speech_seconds",
          f"Speech (post-filtered ASR cue coverage) {aud['speech_seconds']} of {aud['n_seconds']} s "
          f"({aud['speech_seconds']/aud['n_seconds']*100:.0f}%).", evidence_file="audio/audio_structure.json",
          limits="Depends on ASR + pre-registered post-filter: 26 segments dropped, a possible false drop at ~1496.9 s, recognition errors; see failure-cases.jsonl.")
    C.add("S1-MEA-007", "MEASURED", "work/passC.log ebur128 summary",
          aud["integrated_loudness_ffmpeg"].replace("\n", " ")[:300], evidence_file="audio/audio_structure.json")
    av = r["av_sync"]
    C.add("S1-MEA-008", "MEASURED", "shots/segments.json rhythm.av_sync",
          f"{av['cuts_within_0.5s_of_speech_cue_edge']*100:.1f}% of hard cuts fall within 0.5 s of a speech-cue start/end vs "
          f"{av['null_random_cut_times_mean']*100:.1f}% (p95 {av['null_random_cut_times_p95']*100:.1f}%) for random cut times; "
          f"median |ΔRMS| across cuts {av['rms_jump_db_at_cuts_median']} dB vs {av['rms_jump_db_random_median']} dB at random times.",
          evidence_file="shots/segments.json", limits="Cue edges are ASR segment edges, not word-level; 200-draw null.")
    nb = sum(s["duration"] for s in segs if s["kind"] == "BLACK")
    C.add("S1-MEA-009", "MEASURED", "shots/segments.json black_segments_ffmpeg",
          f"Near-black (blackdetect pix_th 0.10, >=0.2 s) total {nb:.1f} s in {r['n_black_segments']} intervals; "
          f"{len(seg['gradual_candidates'])} CANDIDATE_GRADUAL windows flagged.", evidence_file="shots/segments.json",
          limits="Near-black ≠ editorial black: much of it is dark installation imagery.")
    ia = obs["role_shots"]["interviewee_A_white_wall_title_lettering"]
    ia_t = sum(by_id[i]["duration"] for i in ia)
    C.add("S1-INF-001", "INFERRED", "observations.agent.json role_shots; sequences Q02,Q04,Q07,Q09,Q12,Q14,Q16–Q19",
          f"A single seated interview (Interviewee A, static MCU against a white wall with the title lettering) recurs in {len(ia)} shots "
          f"({ia_t:.0f} s, {ia_t/duration*100:.0f}% of runtime), spread from 0:47 to 37:35.",
          inference="The interview is the structural anchor; exhibition, build, talk and performance footage is intercut between interview returns.",
          alternative="The film may be organised by exhibition chronology/programme order and the interview used only as connective tissue; parts of the interview audio may run as voice-over across other shots (not checked).",
          unknowns=["editor's intent", "whether interview audio continues under cutaways (J/L cuts)"],
          limits="Role assignment from one keyframe per segment by the producer agent.")
    C.add("S1-INF-002", "INFERRED", "sequences Q06, Q08, Q15, Q19; segments S1-SH032..S1-SH058, S1-SH072..S1-SH112",
          "Dark sequences fragment into many sub-second NEAR_BLACK/SHOT segments with no hard cut; keyframes show the same framing of a lamp hall with lamps on/off.",
          inference="Rhythm in these sequences comes from the installation's light switching inside (near-)continuous takes, not from editing.",
          alternative="Fast cutting between near-identical angles; or exposure changes by the camera.",
          unknowns=["frame-level continuity across pulses"], limits="Needs frame-level human review; boundary reliability LOW.")
    C.add("S1-INF-003", "INFERRED", "S1-MEA-004 long segments; Q11, Q13, Q15",
          "Talks and live performances are presented in long segments (44.8–137.5 s) while build/documentation passages cut every ~3–8 s.",
          inference="Duration is used to separate 'witnessing a performance/talk' from 'documenting process'.",
          alternative="Long segments may hide dissolves or multi-camera switches not caught by the hard-cut detector; CANDIDATE_GRADUAL windows exist inside some.",
          unknowns=["number of cameras", "whether performance audio is continuous"], limits="Dissolve recall NOT_RUN.")
    C.add("S1-INF-004", "INFERRED", "S1-MEA-008",
          "Hard cuts coincide with speech-cue edges ~2.9x more often than random placement.",
          inference="Cuts are placed at phrase boundaries of the interview/talk audio.",
          alternative="ASR segmentation favours pauses created by the edit itself; or music/ambience edits drive both.",
          unknowns=["word-level timing"], limits="Cue-edge proxy only.")
    C.add("S1-INF-005", "INFERRED", "observations.agent.json sequences Q01–Q20",
          "20 coarse sequences labelled from contact sheets (opening, interview/documentation blocks, talk events, dark installation passages, performances, daylight atrium, ending credits).",
          inference="Macro structure alternates speech-led documentation blocks with non-speech installation/performance passages (see per-sequence speech_fraction).",
          alternative="Sequence boundaries are the producer's reading; an independent viewer may group differently.",
          unknowns=["intended chaptering"], limits="Boundaries snapped to measured segments; labels unreviewed.")
    C.add("S1-INF-006", "INFERRED", "segments in role interviewee_A; measured.visual.motion_mad_mean",
          "Interview shots have low inter-frame motion (motion proxy) and stable framing in keyframes.",
          inference="Interview filmed locked-off (tripod).",
          alternative="Stabilised handheld; very slow push-ins below the proxy's sensitivity.",
          unknowns=["camera support"], limits="2 fps 160x90 motion proxy.")
    for k, txt in [("lens", "Lens type / focal length for any shot"), ("camera", "Camera bodies, settings, number of cameras"),
                   ("grade", "Grade / post pipeline and LUTs"), ("mix", "Whether performance sound is sync/live or laid/remixed"),
                   ("credits", "Director/editor/camera credits beyond channel metadata")]:
        C.add(f"S1-UNK-{k}", "UNKNOWN", "n/a", txt + " — not observable from delivered frames/audio.",
              alternative="n/a", unknowns=[txt], limits="Frames do not reveal these by themselves (handoff §4).")
    with open(P / "claims-evidence.jsonl", "w", encoding="utf-8") as fh:
        for row in C.rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    # ---- unknowns / failure cases
    unknowns = {"schema": "studio.reverse.unknowns.v1", "items": [
        {"id": "U-01", "what": "Cut recall (dissolves, soft cuts, fades not reaching near-black)", "status": "NOT_RUN", "needs": "human frame-level review"},
        {"id": "U-02", "what": "Editorial vs luminance boundaries in Q06/Q08/Q15/Q19", "status": "INCONCLUSIVE", "needs": "human review or optical-flow check (OpenCV not admitted on box)"},
        {"id": "U-03", "what": "Shot scale / composition / blocking per segment", "status": "INFERRED only", "needs": "independent reviewer (V2)"},
        {"id": "U-04", "what": "Camera movement type (pan/tilt/dolly/handheld)", "status": "NOT_RUN", "needs": "optical-flow tool admission or human review"},
        {"id": "U-05", "what": "Music vs ambience vs installation sound in non-speech sections", "status": "NOT_RUN", "needs": "admitted audio analyser (librosa HOLD) or human listening"},
        {"id": "U-06", "what": "Lens, camera, grade, mix, credits", "status": "UNKNOWN", "needs": "creator statement"},
        {"id": "U-07", "what": "Transcript correctness", "status": "INCONCLUSIVE", "needs": "native-speaker review of SRT (private)"},
        {"id": "U-08", "what": "Reverse-method comparison (REA-Video vs HyperFrames vs film baseline)", "status": "NOT_RUN", "needs": "pin + licence audit + Neon approval for REA-Video/HyperFrames"},
    ]}
    json.dump(unknowns, open(P / "unknowns.json", "w"), ensure_ascii=False, indent=1)
    fails = [
        {"id": "F-01", "stage": "segmentation", "what": "blackdetect labels dark installation imagery as near-black; produces 120 NEAR_BLACK intervals and many sub-second SHOT fragments", "effect": "ASL/median understated; boundary reliability LOW in dark sequences", "kept": True},
        {"id": "F-02", "stage": "keyframes", "what": "first single-pass select expression with 319 terms failed (ffmpeg filter init: Cannot allocate memory); switched to per-segment accurate seek", "effect": "none on output; logged", "kept": True},
        {"id": "F-03", "stage": "runner", "what": "first background launch of passes B/C ran in wrong cwd (shell & precedence) and failed with exit 254; rerun via script", "effect": "none on output", "kept": True},
        {"id": "F-04", "stage": "ASR", "what": f"post-filter dropped {len(pf['dropped_segments'])} Whisper segments (pre-registered rules); possible false drop of real speech at ~1496.9 s; residual recognition errors", "effect": "speech coverage and cue-edge sync stats carry this limit", "kept": True},
        {"id": "F-06", "stage": "timebase", "what": f"container duration x 29.97 rounds to {round(duration * RATE)} frames but full decode counted {a.n_frames}; last segment frame_out_excl clamped to {a.n_frames} in timeline.otio only", "effect": "1-frame tail difference; segments.json keeps the unclamped value", "kept": True},
        {"id": "F-05", "stage": "gradual", "what": "CANDIDATE_GRADUAL fires on camera moves, lighting changes and object motion as well as dissolves", "effect": "candidates are INFERRED, not boundaries", "kept": True},
    ]
    with open(P / "failure-cases.jsonl", "w", encoding="utf-8") as fh:
        for f in fails:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")

    # ---- methodology.json (candidate only, per handoff §5 skill contract shape)
    meth = {"skill": {"id": "s1-documentary-installation-cutting", "version": "0.0.1-candidate", "domain": "editorial/documentary",
            "source": {"evidence_refs": ["S1-INF-001", "S1-INF-002", "S1-INF-003", "S1-INF-004", "S1-MEA-004", "S1-MEA-008"],
                       "license_status": "HOLD (source is private_analysis only; no distillation from unapproved content)"},
            "applicability": {"triggers": [], "preconditions": [], "exclusions": []},
            "methodology": {"observations": [
                "Interview anchor recurring across the film (S1-INF-001)",
                "Installation light switching supplies rhythm inside takes (S1-INF-002)",
                "Long takes for talks/performances vs short cuts for process (S1-INF-003)",
                "Cuts on speech phrase edges (S1-INF-004)"],
                "decisions": [], "rationales": [], "operations": [], "failure_patterns": []},
            "compilation": {"input_schema": None, "output_schema": None, "provider_independent": True},
            "verification": {"reference_oracle": None, "holdout_cases": [], "regression_cases": [], "status": "NOT_RUN"},
            "promotion": {"human_approval": "required"}},
            "note": "L1 observations only. No L2+ mechanism or reusable skill is claimed; V3 reference and V4 distillation are NOT_RUN."}
    json.dump(meth, open(P / "methodology.json", "w"), ensure_ascii=False, indent=1)

    # ---- manifest / rights / probe
    manifest = {"schema": "studio.source-manifest.v1", "source_id": a.source_id, "video_id": vid,
                "url": f"https://www.youtube.com/watch?v={vid}", "title": info["title"], "channel": info["channel"],
                "upload_date": info["upload_date"], "duration_s": duration, "handoff_pin": a.handoff_pin,
                "admission": {"V0": "PASS (scoped: private_analysis)", "basis": "rights.json OWNER_DECISION_RISK_ACCEPTED",
                              "H01_YT0_YT4": "PASS (yt_gates.py, docs/.../yt_gates_S1_final_2026-11-27.json)"},
                "media": {k: sums[k] for k in [f"{vid}.mkv", f"{vid}.audio.wav", f"{vid}.ja.srt", f"{vid}.ja.raw-asr.srt"]},
                "private_storage": {"box": str(P.parent), "drive_folder": a.drive_folder, "drive_sharing": "owner only"},
                "tools": {**{k: {"version": v.get("version"), "license": v.get("license")} for k, v in tools.items() if isinstance(v, dict)},
                          "numpy": {"version": np.__version__, "license": "BSD-3-Clause"},
                          "opentimelineio": {"version": otio.__version__, "license": "Apache-2.0"},
                          "pillow": {"version": __import__("PIL").__version__, "license": "MIT-CMU (contact sheets only)"}}}
    json.dump(manifest, open(P / "source-manifest.json", "w"), ensure_ascii=False, indent=1)
    rr = dict(rights)
    rr["h02_scope"] = {"operations": ["frame extraction", "audio measurement", "transcript alignment"],
                       "outputs_private": ["keyframes/*.jpg", "keyframes/contact/*.jpg", "transcript/*.srt", "work/*"],
                       "outputs_git": "small derived JSON/MD without frames or transcript text", "redistribution": "none"}
    json.dump(rr, open(P / "rights.json", "w"), ensure_ascii=False, indent=1)
    shutil.copy(S / "media-probe.json", P / "media-probe.json")
    (P / "transcript").mkdir(exist_ok=True)
    for f in [f"{vid}.ja.srt", f"{vid}.ja.raw-asr.srt"]:
        shutil.copy(S / f, P / "transcript" / f)
    kf = [{"id": s["id"], "frame": (s["frame_in"] + s["frame_out_excl"] - 1) // 2,
           "sha256": sha(P / "keyframes" / f"{s['id']}.jpg")} for s in segs]
    json.dump({"schema": "studio.reverse.keyframes.v1", "storage": "private (box + Drive)", "size": "640x360 JPEG q3",
               "items": kf}, open(P / "keyframes/index.json", "w"), indent=1)

    # ---- VIDEO.md + report.html
    lines = [f"# VIDEO.md — {a.source_id} `{vid}`", "",
             f"**{info['title']}** · {info['channel']} · uploaded {info['upload_date']} · {duration:.1f} s · {vs['width']}x{vs['height']} {vs['r_frame_rate']}",
             "", "Rights scope: private_analysis (owner risk-accepted). No frames or transcript text in this file.", "",
             "## Measured overview", "",
             f"- {r['n_hard_cuts']} hard cuts, {r['n_shots']} SHOT + {r['n_black_segments']} NEAR_BLACK segments (S1-MEA-002)",
             f"- SHOT duration mean {sd['mean_ASL']} s / median {sd['median']} s / max {sd['max']} s (S1-MEA-003/004)",
             f"- Speech coverage {aud['speech_seconds']}/{aud['n_seconds']} s (S1-MEA-006); loudness: {aud['integrated_loudness_ffmpeg'].splitlines()[1].strip() if aud['integrated_loudness_ffmpeg'] else ''}",
             f"- Cuts near speech-cue edges {av['cuts_within_0.5s_of_speech_cue_edge']*100:.1f}% vs random {av['null_random_cut_times_mean']*100:.1f}% (S1-MEA-008)",
             "", "## Sequences (INFERRED labels by producer agent; measured columns)", "",
             "| Seq | TC in–out | Dur s | Segs | Hard cuts | Speech | Luma | Label |", "|---|---|---|---|---|---|---|---|"]
    from studio.reverse.film_baseline import tc
    for q in seqs:
        m = q["measured"]
        lines.append(f"| {q['id']} | {tc(q['start_snapped'])}–{tc(q['end_snapped'])} | {m['duration']:.1f} | {m['n_segments']} | {m['n_hard_cuts']} | {m['speech_fraction']:.2f} | {m['luma_mean_timeweighted']:.0f} | {q['label']} |")
    lines += ["", "## Claims", "", "See `claims-evidence.jsonl` (classes SOURCE_EVIDENCE / MEASURED / INFERRED / UNVERIFIED_CLAIM / UNKNOWN).",
              "", "## Limits", "", "See `failure-cases.jsonl` and `unknowns.json`. ASR caveats: 26 post-filtered segments, possible false drop near 1496.9 s, recognition errors.", ""]
    (P / "VIDEO.md").write_text("\n".join(lines), encoding="utf-8")

    def report(with_frames: bool):
        rows = []
        for s in ir_rows:
            img = f'<img src="keyframes/{s["id"]}.jpg" width="160">' if with_frames else ""
            v, au = s["measured"]["visual"], s["measured"]["audio"]
            rows.append(f"<tr><td>{s['id']}</td><td>{img}</td><td>{s['tc_in']}</td><td>{s['duration_s']:.2f}</td><td>{s['kind']}</td>"
                        f"<td>{s['boundary_in']}</td><td>{v['luma_mean']}</td><td>{v['saturation_mean']}</td><td>{v['motion_mad_mean']}</td>"
                        f"<td>{au['rms_dbfs_mean']}</td><td>{au['speech_fraction']}</td><td>{s['sequence']}</td><td>{html.escape(str(s['observed_inferred']['role'] or ''))}</td></tr>")
        claims = "".join(f"<li><b>{c['claim_id']}</b> [{c['class']}] {html.escape(c['observation'])}</li>" for c in C.rows)
        return (f"<!doctype html><meta charset=utf-8><title>{a.source_id} Reverse Evidence Pack</title>"
                f"<style>body{{font:13px sans-serif}}td,th{{border:1px solid #ccc;padding:2px 4px}}table{{border-collapse:collapse}}</style>"
                f"<h1>{a.source_id} {vid} — Reverse Evidence Pack</h1><p>Rights scope private_analysis. "
                f"{'Private copy with keyframes.' if with_frames else 'Frame-free copy.'} V2 inference acceptance: NOT_RUN.</p>"
                f"<h2>Claims</h2><ul>{claims}</ul><h2>Segments</h2><table><tr><th>id</th><th>frame</th><th>tc</th><th>dur</th><th>kind</th>"
                f"<th>in</th><th>luma</th><th>sat</th><th>motion</th><th>dBFS</th><th>speech</th><th>seq</th><th>role (INFERRED)</th></tr>{''.join(rows)}</table>")
    (P / "report.html").write_text(report(False), encoding="utf-8")
    (P / "report.with-keyframes.html").write_text(report(True), encoding="utf-8")

    # ---- SHA256SUMS over pack (excluding work/ raw intermediates which are listed separately)
    files = sorted(p for p in P.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    with open(P / "SHA256SUMS", "w") as fh:
        for p in files:
            fh.write(f"{sha(p)}  {p.relative_to(P)}\n")

    # ---- git-safe subset
    G = a.git_out
    G.mkdir(parents=True, exist_ok=True)
    git_files = ["source-manifest.json", "rights.json", "media-probe.json", "VIDEO.md", "reverse-ir.json",
                 "methodology.json", "claims-evidence.jsonl", "unknowns.json", "failure-cases.jsonl", "report.html",
                 "timeline.otio", "observations.agent.json", "shots/segments.json", "audio/audio_structure.json",
                 "transcript/cue_segment_alignment.json", "keyframes/index.json"]
    for f in git_files:
        (G / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(P / f, G / f)
    with open(G / "SHA256SUMS", "w") as fh:
        for f in git_files:
            fh.write(f"{sha(G / f)}  {f}\n")
    with open(G / "PRIVATE_SHA256SUMS", "w") as fh:
        fh.write((P / "SHA256SUMS").read_text())
    print("pack written", len(files), "files; git subset", len(git_files))


if __name__ == "__main__":
    main()
