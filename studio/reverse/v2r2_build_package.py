"""Build the S1 V2 round-2 agent-review package (pre-registration RUBRIC_V2R2.md).

Fixes over round 1 (failure cases F-07..F-15):
- stage A carries no author cut lists, segment ids, segment-labelled keyframes or inferences; it gets the full MKV,
  neutral timestamp-labelled frames, fresh random windows/spans (new secret seed), machine ASR SRT and media probe only;
- stage B bundles every file any claim cites (trimmed info.json, description, passC.log, O3 re-check, decode summary,
  id index, observations, ext files including PySceneDetect after the owner licence exception);
- stage B archive is encrypted (passphrase released by the dispatcher only after the stage-A hash is logged);
- the oracle key never touches disk in plaintext: it is built in memory, its SHA-256 is computed (with a 128-bit nonce
  inside so the hash can't be brute-forced), and it is written only as AES-256-CBC/PBKDF2 ciphertext outside the
  reviewer tree; passphrases are printed once to stdout and not stored.
Decoy texts come from a private input file so they never appear in git before the review.
"""
from __future__ import annotations

import argparse, hashlib, io, json, os, random, secrets, shutil, subprocess, tarfile, time
from pathlib import Path

FPS = 30000 / 1001
OPENSSL = ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "600000", "-salt", "-md", "sha256"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def encrypt(data: bytes, passphrase: str) -> bytes:
    env = dict(os.environ, V2R2_PASS=passphrase)
    return subprocess.run(OPENSSL + ["-e", "-pass", "env:V2R2_PASS"], input=data, capture_output=True, check=True, env=env).stdout


def decrypt(data: bytes, passphrase: str) -> bytes:
    env = dict(os.environ, V2R2_PASS=passphrase)
    return subprocess.run(OPENSSL + ["-d", "-pass", "env:V2R2_PASS"], input=data, capture_output=True, check=True, env=env).stdout


def overlaps(a, b, pad=0.0):
    return a[0] < b[1] + pad and b[0] < a[1] + pad


def tc(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True, help="private source dir (sources/onNBysMf9WM)")
    ap.add_argument("--v1key", type=Path, required=True, help="round-1 oracle key dir (to avoid reusing windows)")
    ap.add_argument("--v1pkg", type=Path, required=True, help="round-1 package (author contact sheets for stage B)")
    ap.add_argument("--repo-runs", type=Path, required=True)
    ap.add_argument("--decoys", type=Path, required=True, help="private decoy definitions (deleted after build)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sealed", type=Path, required=True)
    a = ap.parse_args()
    src, out = a.src, a.out
    pack, ext = src / "pack", src / "pack-ext"
    seed = secrets.randbits(64)
    nonce = secrets.token_hex(16)
    rng = random.Random(seed)
    S = json.load(open(pack / "shots/segments.json"))
    segs = S["segments"]
    dur = segs[-1]["end"]
    obs = json.load(open(pack / "observations.agent.json"))
    cam = {r["id"]: r for r in json.load(open(ext / "camera_motion.json"))["rows"]}
    hard = [c["t"] for c in S["hard_cuts"]]
    bounds = [s["start"] for s in segs[1:]]
    kind_at = {round(s["start"], 3): s["in_boundary"] for s in segs[1:]}
    nb_edges = [s["start"] for s in segs[1:] if s["in_boundary"] in ("black_start", "black_end")]
    v1win = [(w["t_start"], w["t_end"]) for w in json.load(open(a.v1key / "strata_key.json"))["strips"]]
    role_of = {}
    rmap = {"interviewee_A_white_wall_title_lettering": "SEATED_INTERVIEW_SINGLE", "speaker_B_with_microphone_white_wall": "SPEAKER_WITH_MIC",
            "speaker_C_seated_with_microphone": "SPEAKER_WITH_MIC"}
    for r, ids in obs["role_shots"].items():
        for i in ids:
            role_of[i] = rmap[r]
    taken: list[tuple[float, float]] = []

    def free(iv, pad=0.5):
        return not any(overlaps(iv, t, pad) for t in taken) and not any(overlaps(iv, w, 0.0) for w in v1win)

    # ---- A2 windows (4 s, boundary offset random) ----
    windows = []
    def add_win(stratum, centre=None, tries=400):
        for _ in range(tries):
            if centre is None:
                t0 = rng.uniform(0, dur - 4)
            else:
                t0 = centre - rng.uniform(0.6, 3.4)
            t0 = round(max(0.0, min(dur - 4, t0)), 3)
            iv = (t0, t0 + 4)
            if free(iv):
                taken.append(iv)
                inside = [b for b in bounds if iv[0] <= b < iv[1]]
                windows.append({"stratum": stratum, "t_start": t0, "t_end": t0 + 4, "target": centre,
                                "v1_boundaries_inside": [{"t": round(b, 3), "kind": kind_at[round(b, 3)]} for b in inside]})
                return True
        return False
    for c in rng.sample(hard, len(hard)):
        if sum(w["stratum"] == "V1_HARD_CUT" for w in windows) >= 15: break
        add_win("V1_HARD_CUT", c)
    for c in rng.sample(nb_edges, len(nb_edges)):
        if sum(w["stratum"] == "V1_NEAR_BLACK_EDGE" for w in windows) >= 10: break
        add_win("V1_NEAR_BLACK_EDGE", c)
    gc = [ (g["t_start"] + g["t_end"]) / 2 for g in S["gradual_candidates"]]
    for c in rng.sample(gc, len(gc)):
        if sum(w["stratum"] == "V1_GRADUAL_CANDIDATE" for w in windows) >= 5: break
        add_win("V1_GRADUAL_CANDIDATE", c)
    while sum(w["stratum"] == "RANDOM" for w in windows) < 30:
        add_win("RANDOM")
    windows.sort(key=lambda w: w["t_start"])
    for i, w in enumerate(windows, 1):
        w["window"] = f"X{i:02d}"
    # ---- A3 spans (30 s, full transition listing) ----
    spans = []
    while len(spans) < 6:
        t0 = round(rng.uniform(0, dur - 30), 3); iv = (t0, t0 + 30)
        if free(iv):
            taken.append(iv)
            spans.append({"t_start": t0, "t_end": t0 + 30,
                          "v1_boundaries_inside": [{"t": round(b, 3), "kind": kind_at[round(b, 3)]} for b in bounds if iv[0] <= b < iv[1]]})
    spans.sort(key=lambda s: s["t_start"])
    for i, s in enumerate(spans, 1):
        s["span"] = f"Y{i:02d}"
    # ---- A1 timestamps (30; 12 from author role shots, 18 other SHOT) ----
    shots = [s for s in segs if s["kind"] == "SHOT" and s["duration"] >= 1.5]
    role_shots = [s for s in shots if s["id"] in role_of]
    other = [s for s in shots if s["id"] not in role_of]
    pick = rng.sample(role_shots, 12) + rng.sample(other, 18)
    stamps = []
    for s in pick:
        t = round(rng.uniform(s["start"] + 0.5, s["end"] - 0.5), 3)
        stamps.append({"t": t, "segment_id": s["id"], "author_role": role_of.get(s["id"])})
    stamps.sort(key=lambda x: x["t"])
    for i, s in enumerate(stamps, 1):
        s["sample"] = f"P{i:02d}"
    # ---- A4 camera spans (20; 8 STATIC + 12 moving by author E2 label) ----
    elig = [s for s in shots if s["duration"] >= 3 and s["id"] in cam and cam[s["id"]]["label"] != "UNDETERMINED_LOW_TEXTURE"]
    st = [s for s in elig if cam[s["id"]]["label"] == "STATIC"]
    mv = [s for s in elig if cam[s["id"]]["label"] != "STATIC"]
    camspans = []
    for s in rng.sample(st, 8) + rng.sample(mv, 12):
        m0, m1 = rng.uniform(0.3, 1.0), rng.uniform(0.3, 1.0)
        camspans.append({"t_start": round(s["start"] + m0, 3), "t_end": round(s["end"] - m1, 3), "segment_id": s["id"], "author_label": cam[s["id"]]["label"]})
    camspans.sort(key=lambda x: x["t_start"])
    for i, s in enumerate(camspans, 1):
        s["cam"] = f"M{i:02d}"
    author_seq_starts = [q["start"] for q in obs["sequences"] if q["start"] > 0]

    # ---- write stage A ----
    A = out / "stage_A"
    for d in ("media", "evidence", "stills", "strips", "timeline_sheets"):
        (A / d).mkdir(parents=True, exist_ok=True)
    mkv = src / "staging/onNBysMf9WM.mkv"
    dst = A / "media/onNBysMf9WM.mkv"
    if not dst.exists():
        shutil.copyfile(mkv, dst)
    os.chmod(dst, 0o444)
    shutil.copyfile(pack / "media-probe.json", A / "evidence/media-probe.json")
    srt = pack / "transcript/onNBysMf9WM.ja.srt"
    shutil.copyfile(srt, A / "evidence/onNBysMf9WM.ja.machine-asr.srt")
    proxy = pack / "work/proxy_480x270.mp4"
    jobs = []
    for w in windows:
        jobs.append(["ffmpeg", "-v", "error", "-y", "-ss", f"{w['t_start']:.3f}", "-i", str(proxy), "-t", "4",
                     "-vf", "fps=4,scale=480:270,tile=4x4", "-frames:v", "1", "-q:v", "3", str(A / f"strips/{w['window']}.jpg")])
    for s in stamps:
        jobs.append(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['t']:.3f}", "-i", str(mkv), "-frames:v", "1",
                     "-vf", "scale=1280:-2", "-q:v", "3", str(A / f"stills/{s['sample']}.jpg")])
    tl = out / "_tl"; tl.mkdir(exist_ok=True)
    jobs.append(["ffmpeg", "-v", "error", "-y", "-i", str(proxy), "-vf", "fps=1/5,scale=320:180", "-q:v", "4", str(tl / "f%04d.jpg")])
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda j: subprocess.run(j, check=True), jobs))
    from PIL import Image, ImageDraw
    frames = sorted(tl.glob("f*.jpg"))
    per = 36
    for k in range(0, len(frames), per):
        sheet = Image.new("RGB", (6 * 320, 6 * 200), "black"); dr = ImageDraw.Draw(sheet)
        for j, f in enumerate(frames[k:k + per]):
            im = Image.open(f); x, y = (j % 6) * 320, (j // 6) * 200
            sheet.paste(im, (x, y))
            idx = k + j
            dr.text((x + 4, y + 182), f"t={tc(idx * 5 + 2.5)}", fill="white")
        sheet.save(A / f"timeline_sheets/T{k // per + 1:02d}.jpg", quality=85)
    shutil.rmtree(tl)
    pub = lambda xs, keys: [{k: x[k] for k in keys} for x in xs]
    json.dump(pub(windows, ["window", "t_start", "t_end"]), open(A / "strips/windows.json", "w"), indent=1)
    roles = "SEATED_INTERVIEW_SINGLE | SPEAKER_WITH_MIC | PERFORMER | CREW_OR_TECHNICIAN | VISITORS_OR_CROWD | NO_PEOPLE | OTHER | CANNOT_DETERMINE"
    ttypes = "HARD_CUT | CUT_TO_BLACK | CUT_FROM_BLACK | DISSOLVE | FADE_TO_BLACK | FADE_FROM_BLACK | LIGHT_CHANGE_SAME_SHOT | WIPE_OR_OTHER | CANNOT_DETERMINE"
    tmpl = {
        "A1_timestamps": [{"sample": s["sample"], "t": s["t"], "still": f"stills/{s['sample']}.jpg",
                           "answer": {"content_description": "", "people_role": roles, "shot_scale": "ECU | CU | MCU | MS | WS | EWS | CANNOT_DETERMINE",
                                      "lighting": "BRIGHT_EVEN | DARK | BACKLIT_SILHOUETTE | MIXED | CANNOT_DETERMINE", "confidence": "0-1", "evidence_note": ""}} for s in stamps],
        "A2_windows": [{"window": w["window"], "t_start": w["t_start"], "t_end": w["t_end"], "strip": f"strips/{w['window']}.jpg",
                        "answer": {"transitions": [{"t_seconds": "time of the first frame of the new picture, from the MKV at native frame rate", "type": ttypes, "confidence": "0-1"}],
                                   "no_transition": "true/false", "evidence_note": ""}} for w in windows],
        "A3_spans": [{"span": s["span"], "t_start": s["t_start"], "t_end": s["t_end"],
                      "answer": {"transitions": [{"t_seconds": "", "type": ttypes, "confidence": "0-1"}], "evidence_note": ""}} for s in spans],
        "A4_camera": [{"cam": c["cam"], "t_start": c["t_start"], "t_end": c["t_end"],
                       "answer": {"movement": "STATIC | PAN_OR_TRACK_H | TILT_OR_PEDESTAL_V | ZOOM_OR_DOLLY_IN | ZOOM_OR_DOLLY_OUT | HANDHELD_OR_IRREGULAR | CANNOT_DETERMINE",
                                  "evidence_note": ""}} for c in camspans],
        "A5_sequences": {"sequence_start_seconds": [], "note": "times (s) where a new major sequence begins, from timeline_sheets/ and the MKV; exclude t=0"},
        "reviewer": {"identity": "", "model_or_agent_if_known": "", "started_at": "", "finished_at": ""},
    }
    json.dump(tmpl, open(A / "stage_A_answers.template.json", "w"), ensure_ascii=False, indent=1)

    # ---- stage B (in memory, encrypted) ----
    runs = a.repo_runs
    def load(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
    v1 = load(pack / "claims-evidence.jsonl") + load(ext / "claims-evidence.ext.jsonl")
    v2 = load(runs / "2026-11-27-v2-result/claims-evidence.v2.jsonl")
    v3 = load(runs / "2026-11-27-v2r2-prereg/claims-evidence.v3.jsonl")
    head: dict[str, dict] = {}
    for c in v1:
        head[c["claim_id"]] = dict(c, version=c.get("version", "v1"))
    for c in v2 + v3:
        head[c["claim_id"]] = c
    pathmap = {"shots/segments.json": "evidence/segments.json", "audio/audio_structure.json": "evidence/audio_structure.json",
               "media-probe.json": "evidence/media-probe.json", "../pack-ext/": "evidence/ext/",
               "../pack-v2/evidence/checks_O1-O4.json": "evidence/checks_O1-O4.json",
               "../pack-v2/evidence/s1_full_decode_summary_2026-11-27.txt": "evidence/s1_full_decode_summary.txt"}
    def remap(p):
        if not p: return p
        for k, v in pathmap.items():
            if p.startswith(k): return v + p[len(k):]
        return p
    drop = {"claim_id", "version", "supersedes", "change_reason", "reviewer", "status", "licence_status"}
    review_fields = ["class", "source_id", "source_version", "media_sha256", "creator_statement", "locator", "observation",
                     "inference", "alternative_explanation", "unknowns", "confidence_limits", "evidence_file"]
    items = []
    for cid, c in head.items():
        r = {k: c.get(k) for k in review_fields}
        r["evidence_file"] = remap(r["evidence_file"])
        items.append(({"original_id": cid, "version": c["version"], "class": c["class"], "decoy": False}, r))
    dec = json.load(open(a.decoys))
    base = {k: v1[0][k] for k in ("source_id", "source_version", "media_sha256")}
    for d in dec:
        r = {k: None for k in review_fields}; r.update(base); r["unknowns"] = []
        r.update({k: v for k, v in d.items() if k in review_fields})
        items.append(({"original_id": None, "version": None, "class": d["class"], "decoy": True, "decoy_truth": d["truth"]}, r))
    rng.shuffle(items)
    claims_key, lines = [], []
    for i, (meta, r) in enumerate(items, 1):
        rid = f"K{i:02d}"
        claims_key.append(dict(meta, review_id=rid))
        lines.append(json.dumps(dict(review_id=rid, **r), ensure_ascii=False))
    B: dict[str, bytes] = {}
    B["claims_to_review.jsonl"] = ("\n".join(lines) + "\n").encode()
    B["stage_B_answers.template.json"] = json.dumps({"claims": [{"review_id": m["review_id"], "verdict": "SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED | CANNOT_DETERMINE",
        "cannot_determine_reason": "if CANNOT_DETERMINE: EVIDENCE_MISSING_FROM_PACKAGE | AMBIGUOUS | OTHER", "class_appropriate": "YES | NO (+ why)",
        "forbidden_inference": "NONE | LENS_OR_CAMERA_FACT | PROMPT_OR_SEED | IDENTITY", "checked": "file + locator you opened", "note": ""} for m in claims_key]}, ensure_ascii=False, indent=1).encode()
    ev = {"evidence/segments.json": pack / "shots/segments.json", "evidence/audio_structure.json": pack / "audio/audio_structure.json",
          "evidence/cue_segment_alignment.json": pack / "transcript/cue_segment_alignment.json",
          "evidence/media-probe.json": pack / "media-probe.json", "evidence/onNBysMf9WM.description": src / "staging/onNBysMf9WM.description",
          "evidence/passC.log": pack / "work/passC.log", "evidence/checks_O1-O4.json": pack / "work/checks_O1-O4.json",
          "evidence/s1_full_decode_summary.txt": src / "pack-v2/evidence/s1_full_decode_summary_2026-11-27.txt",
          "evidence/observations.agent.json": pack / "observations.agent.json", "evidence/reverse-ir.json": pack / "reverse-ir.json",
          "evidence/unknowns.json": pack / "unknowns.json", "evidence/timeline.otio": pack / "timeline.otio",
          "evidence/methodology.json": pack / "methodology.json", "evidence/failure-cases.v1.jsonl": pack / "failure-cases.jsonl",
          "evidence/failure-cases.v2.jsonl": runs / "2026-11-27-v2-result/failure-cases.v2.jsonl"}
    for f in ("camera_motion.json", "dark_boundary_disambiguation.json", "music_analysis.json", "scenedetect_cuts.json", "EXT.md"):
        ev[f"evidence/ext/{f}"] = ext / f
    missing = [k for k, p in ev.items() if not Path(p).is_file()]
    if missing:
        raise SystemExit(f"missing evidence: {missing}")
    for k, p in ev.items():
        B[k] = Path(p).read_bytes()
    info = json.load(open(src / "staging/onNBysMf9WM.info.json"))
    keep = ["id", "title", "fulltitle", "channel", "channel_id", "uploader", "uploader_id", "upload_date", "duration", "duration_string",
            "description", "categories", "tags", "license", "language", "width", "height", "fps", "vcodec", "acodec", "format_id", "format",
            "webpage_url", "view_count", "like_count", "availability", "live_status", "subtitles", "automatic_captions"]
    trimmed = {k: info.get(k) for k in keep}
    trimmed["subtitles"] = sorted((info.get("subtitles") or {}).keys())
    trimmed["automatic_captions"] = sorted((info.get("automatic_captions") or {}).keys())
    trimmed["_note"] = "trimmed copy: per-format download URLs/HTTP headers removed (they embed session parameters); all other listed fields verbatim"
    B["evidence/onNBysMf9WM.info.trimmed.json"] = json.dumps(trimmed, ensure_ascii=False, indent=1).encode()
    # id index for internal ids cited in locators
    idx = {cid: {"class": c["class"], "locator": c["locator"], "evidence_file": remap(c.get("evidence_file"))}
           for cid, c in head.items() if any(cid in (x.get("locator") or "") for x in head.values() if x is not c)}
    idx["_sequences"] = "Q01..Q20 are defined in evidence/observations.agent.json sequences[] (author INFERRED)"
    idx["_segments"] = "S1-SHxxx / S1-BKxx are evidence/segments.json segments[].id; keyframes/<id>.jpg"
    B["evidence/id_index.json"] = json.dumps(idx, ensure_ascii=False, indent=1).encode()
    for f in sorted((pack / "keyframes").glob("*.jpg")):
        B[f"keyframes/{f.name}"] = f.read_bytes()
    for f in sorted((a.v1pkg / "stage_A_blind/contact_sheets").glob("*")):
        B[f"author_contact_sheets/{f.name}"] = f.read_bytes()
    B["PATHS.md"] = ("Claim paths → archive paths: shots/segments.json → evidence/segments.json; audio/audio_structure.json → evidence/audio_structure.json; "
                     "pack-ext/*.json → evidence/ext/*.json; work/passC.log → evidence/passC.log; onNBysMf9WM.info.json → evidence/onNBysMf9WM.info.trimmed.json; "
                     "onNBysMf9WM.description → evidence/onNBysMf9WM.description; keyframes/<id>.jpg → keyframes/<id>.jpg; internal ids → evidence/id_index.json.\n"
                     "The video is ../stage_A/media/onNBysMf9WM.mkv.\n").encode()
    B["_nonce.txt"] = secrets.token_hex(16).encode()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for k in sorted(B):
            ti = tarfile.TarInfo("stage_B/" + k); ti.size = len(B[k]); ti.mtime = int(time.time()); ti.mode = 0o444
            tf.addfile(ti, io.BytesIO(B[k]))
    tarb = buf.getvalue()
    pass_b = secrets.token_urlsafe(24)
    encb = encrypt(tarb, pass_b)
    assert decrypt(encb, pass_b) == tarb
    (out / "stage_B_sealed.tar.gz.enc").write_bytes(encb)

    key = {"schema": "s1-v2r2-oracle-key.v1", "nonce": nonce, "seed": seed, "rubric": "RUBRIC_V2R2.md",
           "claims": claims_key, "A1_timestamps": stamps, "A2_windows": windows, "A3_spans": spans, "A4_camera": camspans,
           "A5_author_sequence_starts": author_seq_starts, "author_hard_cuts": hard, "author_boundaries": [{"t": round(b, 3), "kind": kind_at[round(b, 3)]} for b in bounds],
           "stage_B_plain_sha256": sha(tarb)}
    keyb = json.dumps(key, ensure_ascii=False, indent=1).encode()
    pass_k = secrets.token_urlsafe(24)
    enck = encrypt(keyb, pass_k)
    assert decrypt(enck, pass_k) == keyb
    a.sealed.mkdir(parents=True, exist_ok=True)
    (a.sealed / "oracle_key_r2.json.enc").write_bytes(enck)
    meta = {"oracle_key_plain_sha256": sha(keyb), "oracle_key_cipher_sha256": sha(enck), "stage_B_plain_sha256": sha(tarb),
            "stage_B_cipher_sha256": sha(encb), "seed_commitment_sha256": sha(f"{seed}:{nonce}".encode()),
            "cipher": " ".join(OPENSSL), "counts": {"claims_total": len(claims_key), "decoys": len(dec), "A1": len(stamps), "A2": len(windows),
            "A2_strata": {s: sum(w["stratum"] == s for w in windows) for s in ("V1_HARD_CUT", "V1_NEAR_BLACK_EDGE", "V1_GRADUAL_CANDIDATE", "RANDOM")},
            "A3": len(spans), "A4": len(camspans), "A5_author_sequences": len(author_seq_starts), "timeline_sheets": len(list((A / 'timeline_sheets').glob('*.jpg')))}}
    (out / "SEAL_META.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))
    print("PASSPHRASE_STAGE_B=" + pass_b)
    print("PASSPHRASE_ORACLE_KEY=" + pass_k)


if __name__ == "__main__":
    main()
