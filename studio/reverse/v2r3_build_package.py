"""Build the S1 V2 round-3 agent-review package (pre-registration RUBRIC_V2R3.md).

Same isolation as round 2 (MKV included, blind stage A, encrypted stage B released after the stage-A hash, oracle key only as
AES-256 ciphertext outside the package, passphrases printed once to a foreground shell and stored nowhere).
New: reference = segmentation v2 (pack-v2/seg), A4 spans verified cut/dissolve-free (seg_v2 S5) with span-level E2 labels,
SEG2_CUT_NEW and SEG2_DISSOLVE strata, claims at head versions incl. v4/v5, fresh decoys from a private file, no overlap with
round-1 or round-2 windows. Round-1/2 answers are never read.
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
    ap.add_argument("--v1pkg", type=Path, required=True)
    ap.add_argument("--repo-runs", type=Path, required=True)
    ap.add_argument("--decoys", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sealed", type=Path, required=True)
    a = ap.parse_args()
    src, out = a.src, a.out
    pack, ext, seg = src / "pack", src / "pack-ext", src / "pack-v2/seg"
    mkv = src / "staging/onNBysMf9WM.mkv"
    seed = secrets.randbits(64); nonce = secrets.token_hex(16); rng = random.Random(seed)
    v1 = json.load(open(pack / "shots/segments.json"))["segments"]
    S2 = json.load(open(seg / "segments_v2.json")); segs2 = S2["segments"]
    cands = json.load(open(seg / "cut_candidates_v2.json"))["candidates"]
    dctl = json.load(open(seg / "dissolves_v2.json"))["controls"]
    dur = segs2[-1]["end"]
    obs = json.load(open(pack / "observations.agent.json"))
    conf = [c for c in cands if c.get("confirmed") is True]
    unconf = [c["t"] for c in cands if c.get("confirmed") is not True]
    blacks = [(s["start"], s["end"]) for s in segs2 if s["kind"] == "BLACK"]
    black_edges = sorted({x for b in blacks for x in b if 0 < x < dur})
    near_edge = lambda t: any(abs(t - e) <= 2 / 29.97 for e in black_edges)  # cut events at a BLACK edge are that edge
    cut_new = [c["t"] for c in conf if "v1" not in c["sources"] and not near_edge(c["t"])]
    cut_old = [c["t"] for c in conf if "v1" in c["sources"] and not near_edge(c["t"])]
    dss = S2["dissolves"]
    bounds = [{"t": round(t, 3), "kind": "cut"} for t in S2["confirmed_cuts"] if not near_edge(t)] + [{"t": round(t, 3), "kind": "black_edge"} for t in black_edges]
    bounds.sort(key=lambda b: b["t"])
    prev = [(w["t_start"], w["t_end"]) for w in json.load(open(a.v1key / "strata_key.json"))["strips"]]
    r2 = json.loads(decrypt(a.r2key.read_bytes(), os.environ["R2_KEY_PASS"]))
    prev += [(w["t_start"], w["t_end"]) for w in r2["A2_windows"]] + [(s["t_start"], s["t_end"]) for s in r2["A3_spans"]]
    prev += [(c["t_start"], c["t_end"]) for c in r2["A4_camera"]] + [(p["t"] - 0.5, p["t"] + 0.5) for p in r2["A1_timestamps"]]
    del r2
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
                                "seg2_boundaries_inside": inside(iv), "seg2_dissolves_inside": [d for d in dss if overlaps((d["start"], d["end"]), iv)]})
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
    # A3 spans first: 30 s free intervals are scarce once rounds 1-2 are excluded
    spans = []
    for _ in range(200000):
        if len(spans) == 6:
            break
        t0 = round(rng.uniform(0, dur - 30), 3); iv = (t0, t0 + 30)
        if free(iv):
            taken.append(iv)
            spans.append({"t_start": t0, "t_end": t0 + 30, "seg2_boundaries_inside": inside(iv),
                          "seg2_dissolves_inside": [d for d in dss if overlaps((d["start"], d["end"]), iv)]})
    if len(spans) < 6:
        raise SystemExit(f"only {len(spans)} free 30 s spans")
    spans.sort(key=lambda s: s["t_start"])
    for i, s in enumerate(spans, 1):
        s["span"] = f"V{i:02d}"
    fill("SEG2_CUT_NEW", cut_new, 7)
    fill("SEG2_CUT_V1", cut_old, 8)
    fill("SEG2_BLACK_EDGE", black_edges, 8)
    fill("SEG2_DISSOLVE", [d for d in dss if d["end"] - d["start"] <= 3.0], 7, span=True)
    for _ in range(500):
        if len(windows) >= 60:
            break
        add("RANDOM")
    if len(windows) < 60:
        raise SystemExit(f"only {len(windows)} A2 windows")
    windows.sort(key=lambda w: w["t_start"])
    for i, w in enumerate(windows, 1):
        w["window"] = f"Z{i:02d}"
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
                    stamps.append({"t": t, "seg2_id": s["id"], "v1_id": s["v1_overlap"][0], "author_role": role_of.get(s["v1_overlap"][0])})
                    break
        if got < n_:
            raise SystemExit("not enough free A1 timestamps")
    stamps.sort(key=lambda x: x["t"])
    for i, s in enumerate(stamps, 1):
        s["sample"] = f"Q{i:02d}"
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
        if not free((x0, x1), 0.0):
            continue
        if any(x0 < u < x1 for u in unconf) or any(overlaps((d["start"], d["end"]), (x0, x1)) for d in dss) or any(overlaps(b, (x0, x1)) for b in blacks):
            rejected.append({"seg2_id": s["id"], "reason": "candidate/dissolve/black inside"}); continue
        lab = camera_motion(g, [{"id": s["id"], "kind": "SHOT", "start": x0, "end": x1, "duration": x1 - x0, "tc_in": tc(x0)}])
        if not lab or lab[0]["label"] == "UNDETERMINED_LOW_TEXTURE":
            rejected.append({"seg2_id": s["id"], "reason": "low texture"}); continue
        cls = "STATIC" if lab[0]["label"] == "STATIC" else "MOVING"
        if need[cls] == 0:
            continue
        ok, info = native_cut_free(mkv, x0, x1)
        if not ok:
            rejected.append({"seg2_id": s["id"], "reason": "native decode flagged", **(info or {})}); continue
        need[cls] -= 1
        taken.append((x0, x1))
        camspans.append({"t_start": x0, "t_end": x1, "seg2_id": s["id"], "author_label": lab[0]["label"], "e2_span": lab[0], "native_check": info})
    camspans.sort(key=lambda c: c["t_start"])
    for i, c in enumerate(camspans, 1):
        c["cam"] = f"N{i:02d}"
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
              "2026-11-27-v2r2-result/claims-evidence.v4.jsonl", "2026-11-27-seg-v2/claims-evidence.v5.jsonl"):
        for c in load(runs / f):
            head[c["claim_id"]] = c
    pathmap = [("shots/segments.json", "evidence/segments.json"), ("audio/audio_structure.json", "evidence/audio_structure.json"),
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
        rid = f"J{i:02d}"; ck.append(dict(m, review_id=rid)); lines.append(json.dumps(dict(review_id=rid, **r), ensure_ascii=False))
    B = {"claims_to_review.jsonl": ("\n".join(lines) + "\n").encode()}
    B["stage_B_answers.template.json"] = json.dumps({"claims": [{"review_id": m["review_id"], "verdict": "SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | CANNOT_DETERMINE",
        "cannot_determine_reason": "EVIDENCE_MISSING_FROM_PACKAGE | AMBIGUOUS | OTHER", "class_appropriate": "YES | NO (+ why)",
        "forbidden_inference": "NONE | LENS_OR_CAMERA_FACT | PROMPT_OR_SEED | IDENTITY", "checked": "", "note": ""} for m in ck]}, ensure_ascii=False, indent=1).encode()
    ev = {"evidence/segments.json": pack / "shots/segments.json", "evidence/audio_structure.json": pack / "audio/audio_structure.json",
          "evidence/cue_segment_alignment.json": pack / "transcript/cue_segment_alignment.json", "evidence/media-probe.json": pack / "media-probe.json",
          "evidence/onNBysMf9WM.description": src / "staging/onNBysMf9WM.description", "evidence/passC.log": pack / "work/passC.log",
          "evidence/checks_O1-O4.json": pack / "work/checks_O1-O4.json", "evidence/observations.agent.json": pack / "observations.agent.json",
          "evidence/reverse-ir.json": pack / "reverse-ir.json", "evidence/unknowns.json": pack / "unknowns.json", "evidence/timeline.otio": pack / "timeline.otio",
          "evidence/methodology.json": pack / "methodology.json", "evidence/failure-cases.v1.jsonl": pack / "failure-cases.jsonl",
          "evidence/failure-cases.v2.jsonl": runs / "2026-11-27-v2-result/failure-cases.v2.jsonl",
          "evidence/failure-cases.v3.jsonl": runs / "2026-11-27-v2r2-result/failure-cases.v3.jsonl"}
    for f in sorted((src / "pack-v2/evidence").glob("*")):
        ev[f"evidence/{f.name}"] = f
    ev["evidence/s1_full_decode_summary_2026-11-27.txt"] = src / "pack-v2/evidence/s1_full_decode_summary_2026-11-27.txt"
    for f in ("camera_motion.json", "dark_boundary_disambiguation.json", "music_analysis.json", "scenedetect_cuts.json", "EXT.md"):
        ev[f"evidence/ext/{f}"] = ext / f
    for f in ("segments_v2.json", "cut_candidates_v2.json", "dissolves_v2.json", "seg_v2_stats.json", "o3_negative_control_v2.json"):
        ev[f"evidence/seg/{f}"] = seg / f
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
    idx["_segments"] = "S1-SHxxx/S1-BKxx = evidence/segments.json (v1); S2-SHxxx/S2-BKxx/S2-DSxx = evidence/seg/segments_v2.json (v2)"
    B["evidence/id_index.json"] = json.dumps(idx, ensure_ascii=False, indent=1).encode()
    for f in sorted((pack / "keyframes").glob("*.jpg")):
        B[f"keyframes/{f.name}"] = f.read_bytes()
    for f in sorted((a.v1pkg / "stage_A_blind/contact_sheets").glob("*")):
        B[f"author_contact_sheets/{f.name}"] = f.read_bytes()
    B["PATHS.md"] = ("Claim paths → archive paths: shots/segments.json → evidence/segments.json; audio/audio_structure.json → evidence/audio_structure.json; "
                     "pack-ext/*.json → evidence/ext/*.json; pack-v2 segmentation files → evidence/seg/*.json; work/passC.log → evidence/passC.log; "
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
    key = {"schema": "s1-v2r3-oracle-key.v1", "nonce": nonce, "seed": seed, "rubric": "RUBRIC_V2R3.md", "claims": ck,
           "A1_timestamps": stamps, "A2_windows": windows, "A3_spans": spans, "A4_camera": camspans, "A4_rejected": rejected,
           "A5_author_sequence_starts": author_seq_starts, "author_boundaries": bounds, "author_dissolves": dss,
           "dissolve_controls_pass": bool(dctl.get("PASS")), "stage_B_plain_sha256": sha(tarb)}
    kb = json.dumps(key, ensure_ascii=False, indent=1).encode()
    pk = secrets.token_urlsafe(24); enck = encrypt(kb, pk); assert decrypt(enck, pk) == kb
    a.sealed.mkdir(parents=True, exist_ok=True)
    (a.sealed / "oracle_key_r3.json.enc").write_bytes(enck)
    strata = {s: sum(w["stratum"] == s for w in windows) for s in ("SEG2_CUT_NEW", "SEG2_CUT_V1", "SEG2_BLACK_EDGE", "SEG2_DISSOLVE", "RANDOM")}
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
