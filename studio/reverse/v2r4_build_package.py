"""Build the S1 V2 round-4 agent-review package (pre-registration RUBRIC_V2R4.md).

Reference = segmentation v3 (pack-v3/seg). Isolation as round 3. F-26 fix: stage B is whitelisted (core evidence + files cited
by included claims) and the build fails if any bundled evidence name looks like earlier-round scoring/answers/post-hoc/failure
files; claims citing or quoting earlier-round reviewer findings are excluded. All seg-v3 tuning items (±2 s) and all round-1/2/3
items are excluded from sampling. Round-1/2/3 answers are never read; their sealed keys are decrypted in memory for windows only.
"""
from __future__ import annotations

import argparse, io, json, math, os, random, secrets, shutil, subprocess, tarfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .v2r2_build_package import sha, encrypt, decrypt, overlaps, tc, OPENSSL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--v1key", type=Path, required=True)
    ap.add_argument("--r2key", type=Path, required=True, help="round-2 sealed key ciphertext (passphrase in env R2_KEY_PASS); windows only")
    ap.add_argument("--r3key", type=Path, required=True, help="round-3 sealed key ciphertext (passphrase in env R3_KEY_PASS); windows only")
    ap.add_argument("--v1pkg", type=Path, required=True)
    ap.add_argument("--repo-runs", type=Path, required=True)
    ap.add_argument("--decoys", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sealed", type=Path, required=True)
    a = ap.parse_args()
    src, out = a.src, a.out
    pack, ext, seg2d, seg = src / "pack", src / "pack-ext", src / "pack-v2/seg", src / "pack-v3/seg"
    mkv = src / "staging/onNBysMf9WM.mkv"
    seed = secrets.randbits(64); nonce = secrets.token_hex(16); rng = random.Random(seed)
    v1 = json.load(open(pack / "shots/segments.json"))["segments"]
    S3 = json.load(open(seg / "segments_v3.json")); segs2 = S3["segments"]
    cands = json.load(open(seg2d / "cut_candidates_v2.json"))["candidates"]
    S2d = json.load(open(seg2d / "segments_v2.json"))["dissolves"]
    D3 = json.load(open(seg / "dissolves_v3.json")); dctl = {"PASS": D3["PASS"]}
    light = S3["light_changes"]
    nb_all = json.load(open(seg / "near_black_cuts_v3.json")); jb_all = json.load(open(seg / "jump_cuts_v3.json"))
    dur = segs2[-1]["end"]
    obs = json.load(open(pack / "observations.agent.json"))
    v1src = {round(c["t"], 4) for c in cands if "v1" in c["sources"]}
    unconf = [c["t"] for c in cands if c.get("confirmed") is not True]
    blacks = [(s["start"], s["end"]) for s in v1 if s["kind"] == "BLACK"]
    black_edges = sorted({x for b in blacks for x in b if 0 < x < dur})
    near_edge = lambda t: any(abs(t - e) <= 2 / 29.97 for e in black_edges)  # cut events at a BLACK edge are that edge
    nb_added = set(nb_all["added"])
    kept = [t for t in S3["cuts"] if t not in nb_added]
    cut_old = [t for t in kept if round(t, 4) in v1src and not near_edge(t)]
    cut_new = [t for t in kept if round(t, 4) not in v1src and not near_edge(t)]
    dark_new = [t for t in nb_all["added"] if not near_edge(t)]
    dss = [{"start": s["start"], "end": s["end"]} for s in segs2 if s["kind"] == "DISSOLVE"] if D3["PASS"] else []
    all_soft = D3["spans"] + S2d
    bounds = [{"t": round(t, 3), "kind": ("dark_cut" if t in nb_added else "cut")} for t in S3["cuts"] if not near_edge(t)] + [{"t": round(t, 3), "kind": "black_edge"} for t in black_edges]
    bounds.sort(key=lambda b: b["t"])
    from .seg_v3 import tuning_exclusions
    prev = [(w["t_start"], w["t_end"]) for w in json.load(open(a.v1key / "strata_key.json"))["strips"]]
    for kp, env in ((a.r2key, "R2_KEY_PASS"), (a.r3key, "R3_KEY_PASS")):
        rk = json.loads(decrypt(kp.read_bytes(), os.environ[env]))
        prev += [(w["t_start"], w["t_end"]) for w in rk["A2_windows"]] + [(s["t_start"], s["t_end"]) for s in rk["A3_spans"]]
        prev += [(c["t_start"], c["t_end"]) for c in rk["A4_camera"]] + [(p["t"] - 0.5, p["t"] + 0.5) for p in rk["A1_timestamps"]]
        del rk
    prev += tuning_exclusions(2.0)
    taken = []
    def free(iv, pad=0.5):
        return not any(overlaps(iv, t, pad) for t in taken) and not any(overlaps(iv, w, 0.0) for w in prev)
    inside = lambda iv: [b for b in bounds if iv[0] <= b["t"] < iv[1]]
    windows = []
    def add(stratum, centre=None, span=None, tries=400):
        for _ in range(tries):
            if centre is None:
                t0 = rng.uniform(0, dur - 4)
            else:
                t0 = centre - rng.uniform(0.6, 3.4)
            t0 = round(max(0.0, min(dur - 4, t0)), 3); iv = (t0, t0 + 4)
            if span and not (iv[0] <= span["start"] - 0.2 and span["end"] + 0.2 <= iv[1]):
                continue
            if free(iv):
                taken.append(iv)
                windows.append({"stratum": stratum, "t_start": t0, "t_end": t0 + 4, "target": centre, "target_span": span,
                                "seg3_boundaries_inside": inside(iv), "seg3_dissolves_inside": [d for d in dss if overlaps((d["start"], d["end"]), iv)]})
                return True
        return False
    def fill(stratum, pool, n, **kw):
        for c in rng.sample(pool, len(pool)):
            if sum(w["stratum"] == stratum for w in windows) >= n:
                break
            if kw.get("span"):
                add(stratum, centre=(c["start"] + c["end"]) / 2, span=c)
            else:
                add(stratum, c)
    # A3 spans first (12 s; RUBRIC_V2R4)
    spans = []
    for _ in range(200000):
        if len(spans) == 6:
            break
        t0 = round(rng.uniform(0, dur - 12), 3); iv = (t0, t0 + 12)
        if free(iv):
            taken.append(iv)
            spans.append({"t_start": t0, "t_end": t0 + 12, "seg3_boundaries_inside": inside(iv),
                          "seg3_dissolves_inside": [d for d in dss if overlaps((d["start"], d["end"]), iv)]})
    if len(spans) < 6:
        raise SystemExit(f"only {len(spans)} free 12 s spans")
    spans.sort(key=lambda s: s["t_start"])
    for i, s in enumerate(spans, 1):
        s["span"] = f"U{i:02d}"
    # A4 verified camera spans
    from .seg_v2 import native_cut_free
    from .ext_analyses import Gray5, camera_motion
    g = Gray5(pack / "work/frames_5fps_320x180.gray")
    pool = [s for s in segs2 if s["kind"] == "SHOT" and s["duration"] >= 3.5]
    rng.shuffle(pool)
    camspans, rejected = [], []
    need = {"STATIC": 8, "MOVING": 12}
    for s in pool:
        if need["STATIC"] == 0 and need["MOVING"] == 0:
            break
        x0, x1 = round(s["start"] + 0.5, 3), round(s["end"] - 0.5, 3)
        pts = unconf + light + nb_all["all_detections"] + jb_all["all_detections"] + S3["cuts"]
        if any(x0 < u < x1 for u in pts) or any(overlaps((d["start"], d["end"]), (x0, x1)) for d in all_soft) or any(overlaps(b, (x0, x1)) for b in blacks):
            rejected.append({"seg3_id": s["id"], "reason": "event/dissolve/black inside"}); continue
        # largest sub-interval of the verified interval that is free of rounds 1-2 and earlier round-3 items
        cuts_ = sorted([(max(x0, t0 - 0.5), min(x1, t1 + 0.5)) for t0, t1 in taken] + [(max(x0, t0), min(x1, t1)) for t0, t1 in prev])
        cuts_ = [c for c in cuts_ if c[0] < c[1]]
        best, cur = (0, 0), x0
        for c0, c1 in cuts_:
            if c0 > cur and c0 - cur > best[1] - best[0]:
                best = (cur, c0)
            cur = max(cur, c1)
        if x1 - cur > best[1] - best[0]:
            best = (cur, x1)
        if best[1] - best[0] < 3.0:
            continue
        x0, x1 = round(best[0] + 0.05, 3), round(best[1] - 0.05, 3)
        lab = camera_motion(g, [{"id": s["id"], "kind": "SHOT", "start": x0, "end": x1, "duration": x1 - x0, "tc_in": tc(x0)}])
        if not lab or lab[0]["label"] == "UNDETERMINED_LOW_TEXTURE":
            rejected.append({"seg3_id": s["id"], "reason": "low texture"}); continue
        cls = "STATIC" if lab[0]["label"] == "STATIC" else "MOVING"
        if need[cls] == 0:
            continue
        ok, info = native_cut_free(mkv, x0, x1)
        if not ok:
            rejected.append({"seg3_id": s["id"], "reason": "native decode flagged", **(info or {})}); continue
        need[cls] -= 1
        taken.append((x0, x1))
        camspans.append({"t_start": x0, "t_end": x1, "seg3_id": s["id"], "author_label": lab[0]["label"], "e2_span": lab[0], "native_check": info})
    camspans.sort(key=lambda c: c["t_start"])
    for i, c in enumerate(camspans, 1):
        c["cam"] = f"C{i:02d}"
    if len(camspans) < 12:
        raise SystemExit(f"only {len(camspans)} A4 spans")
    fill("SEG3_CUT_NEW", cut_new, 7)
    fill("SEG3_CUT_V1", cut_old, 6)
    fill("SEG3_DARK_NEW", dark_new, 7)
    fill("SEG3_LIGHT", light, 7)
    fill("SEG3_DISSOLVE", [d for d in dss if d["end"] - d["start"] <= 3.6], 7, span=True)
    fill("SEG3_BLACK_EDGE", black_edges, 5)
    for _ in range(3000):
        if len(windows) >= 60:
            break
        add("RANDOM", tries=50)
    if len(windows) < 40:
        raise SystemExit(f"only {len(windows)} A2 windows")
    windows.sort(key=lambda w: w["t_start"])
    for i, w in enumerate(windows, 1):
        w["window"] = f"W{i:02d}"
    # A1 timestamps: S2 SHOT wholly inside one v1 segment
    rmap = {"interviewee_A_white_wall_title_lettering": "SEATED_INTERVIEW_SINGLE", "speaker_B_with_microphone_white_wall": "SPEAKER_WITH_MIC",
            "speaker_C_seated_with_microphone": "SPEAKER_WITH_MIC"}
    role_of = {i: rmap[r] for r, ids in obs["role_shots"].items() for i in ids}
    v1by = {s["id"]: s for s in v1}
    ok1 = [s for s in segs2 if s["kind"] == "SHOT" and s["duration"] >= 1.5 and len(s["v1_overlap"]) == 1 and v1by[s["v1_overlap"][0]]["kind"] == "SHOT"]
    rs_ = [s for s in ok1 if s["v1_overlap"][0] in role_of]; ot_ = [s for s in ok1 if s["v1_overlap"][0] not in role_of]
    stamps = []
    for pool_, n_ in ((rs_, 12), (ot_, 18)):
        got = 0
        for s in rng.sample(pool_, len(pool_)):
            if got == n_:
                break
            for _ in range(50):
                t = round(rng.uniform(s["start"] + 0.5, s["end"] - 0.5), 3)
                if free((t - 0.5, t + 0.5), 0.0):
                    taken.append((t - 0.5, t + 0.5)); got += 1
                    stamps.append({"t": t, "seg3_id": s["id"], "v1_id": s["v1_overlap"][0], "author_role": role_of.get(s["v1_overlap"][0])})
                    break
        if got < n_:
            raise SystemExit("not enough free A1 timestamps")
    stamps.sort(key=lambda x: x["t"])
    for i, s in enumerate(stamps, 1):
        s["sample"] = f"R{i:02d}"
    author_seq_starts = [q["start"] for q in obs["sequences"] if q["start"] > 0]

    # ---- stage A
    A = out / "stage_A"
    for d in ("media", "evidence", "stills", "strips", "timeline_sheets"):
        (A / d).mkdir(parents=True, exist_ok=True)
    dst = A / "media/onNBysMf9WM.mkv"
    if not dst.exists():
        shutil.copyfile(mkv, dst)
    os.chmod(dst, 0o444)
    shutil.copyfile(pack / "media-probe.json", A / "evidence/media-probe.json")
    shutil.copyfile(pack / "transcript/onNBysMf9WM.ja.srt", A / "evidence/onNBysMf9WM.ja.machine-asr.srt")
    proxy = pack / "work/proxy_480x270.mp4"
    jobs = [["ffmpeg", "-v", "error", "-y", "-ss", f"{w['t_start']:.3f}", "-i", str(proxy), "-t", "4", "-vf", "fps=4,scale=480:270,tile=4x4",
             "-frames:v", "1", "-q:v", "3", str(A / f"strips/{w['window']}.jpg")] for w in windows]
    jobs += [["ffmpeg", "-v", "error", "-y", "-ss", f"{s['t']:.3f}", "-i", str(mkv), "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "3",
              str(A / f"stills/{s['sample']}.jpg")] for s in stamps]
    tl = out / "_tl"; tl.mkdir(exist_ok=True)
    jobs.append(["ffmpeg", "-v", "error", "-y", "-i", str(proxy), "-vf", "fps=1/5,scale=320:180", "-q:v", "4", str(tl / "f%04d.jpg")])
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda j: subprocess.run(j, check=True), jobs))
    from PIL import Image, ImageDraw
    frames = sorted(tl.glob("f*.jpg"))
    for k in range(0, len(frames), 36):
        sheet = Image.new("RGB", (6 * 320, 6 * 200), "black"); dr = ImageDraw.Draw(sheet)
        for j, f in enumerate(frames[k:k + 36]):
            x, y = (j % 6) * 320, (j // 6) * 200
            sheet.paste(Image.open(f), (x, y)); dr.text((x + 4, y + 182), f"t={tc((k + j) * 5 + 2.5)}", fill="white")
        sheet.save(A / f"timeline_sheets/T{k // 36 + 1:02d}.jpg", quality=85)
    shutil.rmtree(tl)
    json.dump([{k: w[k] for k in ("window", "t_start", "t_end")} for w in windows], open(A / "strips/windows.json", "w"), indent=1)
    roles = "SEATED_INTERVIEW_SINGLE | SPEAKER_WITH_MIC | PERFORMER | CREW_OR_TECHNICIAN | VISITORS_OR_CROWD | NO_PEOPLE | OTHER | CANNOT_DETERMINE"
    ttypes = "HARD_CUT | CUT_TO_BLACK | CUT_FROM_BLACK | DISSOLVE | FADE_TO_BLACK | FADE_FROM_BLACK | LIGHT_CHANGE_SAME_SHOT | WIPE_OR_OTHER | CANNOT_DETERMINE"
    tmpl = {
        "A1_timestamps": [{"sample": s["sample"], "t": s["t"], "still": f"stills/{s['sample']}.jpg", "answer": {"content_description": "", "people_role": roles,
            "shot_scale": "ECU | CU | MCU | MS | WS | EWS | CANNOT_DETERMINE", "lighting": "BRIGHT_EVEN | DARK | BACKLIT_SILHOUETTE | MIXED | CANNOT_DETERMINE",
            "confidence": "0-1", "evidence_note": ""}} for s in stamps],
        "A2_windows": [{"window": w["window"], "t_start": w["t_start"], "t_end": w["t_end"], "strip": f"strips/{w['window']}.jpg",
            "answer": {"transitions": [{"t_seconds": "first frame of the new picture (cuts) or midpoint (dissolves/fades), from the MKV at native frame rate",
                                        "t_end_seconds": "for DISSOLVE/FADE: last frame of the transition (optional)", "type": ttypes, "confidence": "0-1"}],
                       "no_transition": "true/false", "evidence_note": ""}} for w in windows],
        "A3_spans": [{"span": s["span"], "t_start": s["t_start"], "t_end": s["t_end"], "answer": {"transitions": [{"t_seconds": "", "type": ttypes, "confidence": "0-1"}],
            "evidence_note": ""}} for s in spans],
        "A4_camera": [{"cam": c["cam"], "t_start": c["t_start"], "t_end": c["t_end"], "answer": {"movement":
            "STATIC | PAN_OR_TRACK_H | TILT_OR_PEDESTAL_V | ZOOM_OR_DOLLY_IN | ZOOM_OR_DOLLY_OUT | HANDHELD_OR_IRREGULAR | CANNOT_DETERMINE", "evidence_note": ""}} for c in camspans],
        "A5_sequences": {"sequence_start_seconds": [], "note": "times (s) where a new major sequence begins; exclude t=0"},
        "reviewer": {"identity": "", "model_or_agent_if_known": "", "started_at": "", "finished_at": ""},
    }
    json.dump(tmpl, open(A / "stage_A_answers.template.json", "w"), ensure_ascii=False, indent=1)

    # ---- stage B
    runs = a.repo_runs
    load = lambda p: [json.loads(l) for l in open(p, encoding="utf-8")]
    head = {}
    for c in load(pack / "claims-evidence.jsonl") + load(ext / "claims-evidence.ext.jsonl"):
        head[c["claim_id"]] = dict(c, version=c.get("version", "v1"))
    for f in ("2026-11-27-v2-result/claims-evidence.v2.jsonl", "2026-11-27-v2r2-prereg/claims-evidence.v3.jsonl",
              "2026-11-27-v2r2-result/claims-evidence.v4.jsonl", "2026-11-27-seg-v2/claims-evidence.v5.jsonl",
              "2026-11-27-v2r3-result/claims-evidence.v6.jsonl", "2026-11-27-seg-v3/claims-evidence.v7.jsonl"):
        for c in load(runs / f):
            head[c["claim_id"]] = c
    EXCLUDED = {"S1-MEA-002", "S1-MEA-004", "S1-INF-002", "S1-UNK-credits", "S1-EXT-INF-E2", "S1-EXT-INF-E3", "S1-EXT-INF-E2-labels",
                "S1-SEG2-MEA-001", "S1-SEG2-MEA-003"}  # cite or quote earlier-round reviewer findings (RUBRIC_V2R4, F-26)
    head = {k: v for k, v in head.items() if k not in EXCLUDED}
    pathmap = [("../pack-v3/seg/", "evidence/seg3/"), ("../pack-v3/evidence/", "evidence/v3/"), ("shots/segments.json", "evidence/segments.json"), ("audio/audio_structure.json", "evidence/audio_structure.json"),
               ("media-probe.json", "evidence/media-probe.json"), ("../pack-ext/", "evidence/ext/"), ("../pack-v2/seg/", "evidence/seg/"),
               ("../pack-v2/evidence/", "evidence/")]
    def remap(p):
        if not p:
            return p
        for k, v in pathmap:
            if p.startswith(k):
                return v + p[len(k):]
        return p
    fields = ["class", "source_id", "source_version", "media_sha256", "creator_statement", "locator", "observation", "inference",
              "alternative_explanation", "unknowns", "confidence_limits", "evidence_file"]
    items = []
    for cid, c in head.items():
        r = {k: c.get(k) for k in fields}; r["evidence_file"] = remap(r["evidence_file"])
        items.append(({"original_id": cid, "version": c["version"], "class": c["class"], "decoy": False}, r))
    first = next(iter(head.values()))
    for d in json.load(open(a.decoys)):
        r = {k: None for k in fields}; r.update({k: first[k] for k in ("source_id", "source_version", "media_sha256")}); r["unknowns"] = []
        r.update({k: v for k, v in d.items() if k in fields})
        items.append(({"original_id": None, "version": None, "class": d["class"], "decoy": True, "decoy_truth": d["truth"]}, r))
    rng.shuffle(items)
    ck, lines = [], []
    for i, (m, r) in enumerate(items, 1):
        rid = f"L{i:02d}"; ck.append(dict(m, review_id=rid)); lines.append(json.dumps(dict(review_id=rid, **r), ensure_ascii=False))
    B = {"claims_to_review.jsonl": ("\n".join(lines) + "\n").encode()}
    B["stage_B_answers.template.json"] = json.dumps({"claims": [{"review_id": m["review_id"], "verdict": "SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | CANNOT_DETERMINE",
        "cannot_determine_reason": "EVIDENCE_MISSING_FROM_PACKAGE | AMBIGUOUS | OTHER", "class_appropriate": "YES | NO (+ why)",
        "forbidden_inference": "NONE | LENS_OR_CAMERA_FACT | PROMPT_OR_SEED | IDENTITY", "checked": "", "note": ""} for m in ck]}, ensure_ascii=False, indent=1).encode()
    ev = {"evidence/segments.json": pack / "shots/segments.json", "evidence/audio_structure.json": pack / "audio/audio_structure.json",
          "evidence/cue_segment_alignment.json": pack / "transcript/cue_segment_alignment.json", "evidence/media-probe.json": pack / "media-probe.json",
          "evidence/onNBysMf9WM.description": src / "staging/onNBysMf9WM.description", "evidence/passC.log": pack / "work/passC.log",
          "evidence/checks_O1-O4.json": pack / "work/checks_O1-O4.json", "evidence/observations.agent.json": pack / "observations.agent.json",
          "evidence/reverse-ir.json": pack / "reverse-ir.json", "evidence/unknowns.json": pack / "unknowns.json", "evidence/timeline.otio": pack / "timeline.otio",
          "evidence/methodology.json": pack / "methodology.json"}
    for f in ("camera_motion.json", "dark_boundary_disambiguation.json", "music_analysis.json", "scenedetect_cuts.json", "EXT.md"):
        ev[f"evidence/ext/{f}"] = ext / f
    for f in ("segments_v2.json", "cut_candidates_v2.json", "dissolves_v2.json", "seg_v2_stats.json", "o3_negative_control_v2.json"):
        ev[f"evidence/seg/{f}"] = seg2d / f
    for f in ("segments_v3.json", "seg_v3_stats.json", "controls_v3.json", "thresholds_v3.json", "light_changes_v3.json", "jump_cuts_v3.json",
              "near_black_cuts_v3.json", "dissolves_v3.json"):
        ev[f"evidence/seg3/{f}"] = seg / f
    # files under pack-v2/evidence or pack-v3/evidence only when an included claim cites them
    for c in head.values():
        p = c.get("evidence_file") or ""
        for pre, d in (("../pack-v2/evidence/", src / "pack-v2/evidence"), ("../pack-v3/evidence/", src / "pack-v3/evidence")):
            if p.startswith(pre):
                ev[remap(p)] = d / p[len(pre):]
    import re as _re
    bad_names = [k for k in ev if _re.search(r"score|posthoc|answer|failure|oracle|strata|REVIEW", k)]
    if bad_names:
        raise SystemExit(f"F-26 guard: earlier-round scoring/answer-like files in stage B: {bad_names}")
    miss = [k for k, p in ev.items() if not Path(p).is_file()]
    if miss:
        raise SystemExit(f"missing evidence {miss}")
    for k, p in ev.items():
        B[k] = Path(p).read_bytes()
    # every evidence_file cited must exist in the archive
    cited = {json.loads(l)["evidence_file"] for l in lines} - {None}
    bad = [c for c in cited if c not in B]
    if bad:
        raise SystemExit(f"claims cite files not bundled: {bad}")
    info = json.load(open(src / "staging/onNBysMf9WM.info.json"))
    keep = ["id", "title", "fulltitle", "channel", "channel_id", "uploader", "uploader_id", "upload_date", "duration", "duration_string", "description",
            "categories", "tags", "license", "language", "width", "height", "fps", "vcodec", "acodec", "format_id", "format", "webpage_url", "view_count",
            "like_count", "availability", "live_status"]
    tr = {k: info.get(k) for k in keep}
    tr["subtitles"] = sorted((info.get("subtitles") or {}).keys()); tr["automatic_captions"] = sorted((info.get("automatic_captions") or {}).keys())
    tr["_note"] = "trimmed copy: per-format download URLs/HTTP headers removed; listed fields verbatim"
    B["evidence/onNBysMf9WM.info.trimmed.json"] = json.dumps(tr, ensure_ascii=False, indent=1).encode()
    idx = {cid: {"class": c["class"], "locator": c["locator"], "evidence_file": remap(c.get("evidence_file"))}
           for cid, c in head.items() if any(cid in (x.get("locator") or "") for x in head.values() if x is not c)}
    idx["_sequences"] = "Q01..Q20 = evidence/observations.agent.json sequences[] (author INFERRED)"
    idx["_segments"] = "S1-SHxxx/S1-BKxx = evidence/segments.json (v1); S2-* = evidence/seg/segments_v2.json (v2); S3-* = evidence/seg3/segments_v3.json (v3)"
    B["evidence/id_index.json"] = json.dumps(idx, ensure_ascii=False, indent=1).encode()
    for f in sorted((pack / "keyframes").glob("*.jpg")):
        B[f"keyframes/{f.name}"] = f.read_bytes()
    for f in sorted((a.v1pkg / "stage_A_blind/contact_sheets").glob("*")):
        B[f"author_contact_sheets/{f.name}"] = f.read_bytes()
    B["PATHS.md"] = ("Claim paths → archive paths: shots/segments.json → evidence/segments.json; audio/audio_structure.json → evidence/audio_structure.json; "
                     "pack-ext/*.json → evidence/ext/*.json; pack-v2 segmentation files → evidence/seg/*.json; pack-v3 segmentation files → evidence/seg3/*.json; pack-v3/evidence → evidence/v3/; work/passC.log → evidence/passC.log; "
                     "onNBysMf9WM.info.json → evidence/onNBysMf9WM.info.trimmed.json; internal ids → evidence/id_index.json; keyframes/<v1 id>.jpg.\n"
                     "The video is ../stage_A/media/onNBysMf9WM.mkv.\n").encode()
    B["_nonce.txt"] = secrets.token_hex(16).encode()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for k in sorted(B):
            ti = tarfile.TarInfo("stage_B/" + k); ti.size = len(B[k]); ti.mtime = int(time.time()); ti.mode = 0o444
            tf.addfile(ti, io.BytesIO(B[k]))
    tarb = buf.getvalue()
    pb = secrets.token_urlsafe(24); encb = encrypt(tarb, pb); assert decrypt(encb, pb) == tarb
    (out / "stage_B_sealed.tar.gz.enc").write_bytes(encb)
    key = {"schema": "s1-v2r4-oracle-key.v1", "nonce": nonce, "seed": seed, "rubric": "RUBRIC_V2R4.md", "claims": ck,
           "A1_timestamps": stamps, "A2_windows": windows, "A3_spans": spans, "A4_camera": camspans, "A4_rejected": rejected,
           "A5_author_sequence_starts": author_seq_starts, "author_boundaries": bounds, "author_dissolves": dss, "author_light_changes": light, "excluded_claims": sorted(EXCLUDED),
           "dissolve_controls_pass": bool(dctl.get("PASS")), "stage_B_plain_sha256": sha(tarb)}
    kb = json.dumps(key, ensure_ascii=False, indent=1).encode()
    pk = secrets.token_urlsafe(24); enck = encrypt(kb, pk); assert decrypt(enck, pk) == kb
    a.sealed.mkdir(parents=True, exist_ok=True)
    (a.sealed / "oracle_key_r4.json.enc").write_bytes(enck)
    strata = {s: sum(w["stratum"] == s for w in windows) for s in ("SEG3_CUT_NEW", "SEG3_CUT_V1", "SEG3_DARK_NEW", "SEG3_LIGHT", "SEG3_DISSOLVE", "SEG3_BLACK_EDGE", "RANDOM")}
    meta = {"oracle_key_plain_sha256": sha(kb), "oracle_key_cipher_sha256": sha(enck), "stage_B_plain_sha256": sha(tarb), "stage_B_cipher_sha256": sha(encb),
            "seed_commitment_sha256": sha(f"{seed}:{nonce}".encode()), "cipher": " ".join(OPENSSL),
            "counts": {"claims_total": len(ck), "decoys": sum(m["decoy"] for m in ck), "A1": len(stamps), "A2": len(windows), "A3": len(spans),
                       "A4": len(camspans), "A4_rejected": len(rejected), "timeline_sheets": len(list((A / "timeline_sheets").glob("*.jpg")))},
            "sealed_only": {"A2_strata": strata, "A4_static": sum(c["author_label"] == "STATIC" for c in camspans)}}
    (a.sealed / "SEAL_META.private.json").write_text(json.dumps(meta, indent=1))
    pub = {k: v for k, v in meta.items() if k != "sealed_only"}
    print(json.dumps(pub, indent=1))
    print("PASSPHRASE_STAGE_B=" + pb)
    print("PASSPHRASE_ORACLE_KEY=" + pk)


if __name__ == "__main__":
    main()
