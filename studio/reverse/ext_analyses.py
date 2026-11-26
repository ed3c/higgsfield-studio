"""H02 extension analyses (owner-approved OpenCV / PySceneDetect / librosa exception, 2026-11-27).

Pre-registration: docs/handoff/agentic-film-production/runs/2026-11-27-h02-s1-ext/PREREG_EXT_2026-11-27.md
Writes NEW files only (pack-ext/); never modifies v1 pack outputs.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import cv2
import numpy as np

W5, H5, FPS5 = 320, 180, 5.0
CLAHE = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))


class Gray5:
    def __init__(self, path: Path):
        self.m = np.memmap(path, dtype=np.uint8, mode="r")
        self.n = self.m.size // (W5 * H5)

    def frame(self, i: int) -> np.ndarray:
        i = max(0, min(self.n - 1, i))
        return np.asarray(self.m[i * W5 * H5:(i + 1) * W5 * H5]).reshape(H5, W5)

    def at(self, t: float) -> np.ndarray:
        return self.frame(int(round(t * FPS5)))


# ---------------- E1
def scenedetect_compare(raw: dict, v1_cuts: list[float], fps=30000 / 1001, tol_frames=3):
    out = {}
    v1 = np.array(sorted(v1_cuts))
    for name in ("content", "adaptive"):
        sd = np.array(raw[name]["cuts_s"])
        tol = tol_frames / fps
        matched = [float(t) for t in v1 if len(sd) and np.min(np.abs(sd - t)) <= tol]
        v1_only = [float(t) for t in v1 if not len(sd) or np.min(np.abs(sd - t)) > tol]
        sd_only = [float(t) for t in sd if not len(v1) or np.min(np.abs(v1 - t)) > tol]
        out[name] = {"n_cuts": int(len(sd)), "matched_v1": len(matched), "v1_only": v1_only, "pyscenedetect_only": sd_only,
                     "elapsed_s": raw[name]["elapsed_s"]}
    out["version"] = raw.get("version")
    out["tolerance_frames"] = tol_frames
    return out


# ---------------- E2
def _step(prev, cur):
    p = CLAHE.apply(prev)
    c = CLAHE.apply(cur)
    pts = cv2.goodFeaturesToTrack(p, maxCorners=200, qualityLevel=0.01, minDistance=8)
    if pts is None or len(pts) < 6:
        return None
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(p, c, pts, None)
    ok = st.ravel() == 1
    if ok.sum() < 6:
        return None
    M, inl = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=3.0)
    if M is None:
        return None
    s = math.hypot(M[0, 0], M[1, 0])
    return {"tx": float(M[0, 2]), "ty": float(M[1, 2]), "log_s": float(math.log(max(s, 1e-6))),
            "rot_deg": float(math.degrees(math.atan2(M[1, 0], M[0, 0]))), "inliers": int(inl.sum()) if inl is not None else 0}


def camera_motion(g: Gray5, segments: list[dict]):
    rows = []
    for s in segments:
        if s["kind"] != "SHOT" or s["duration"] < 1.0:
            continue
        i0, i1 = int(math.ceil((s["start"] + 0.1) * FPS5)), int(math.floor((s["end"] - 0.1) * FPS5))
        steps = []
        for i in range(i0, i1):
            r = _step(g.frame(i), g.frame(i + 1))
            steps.append(r)
        n = len(steps)
        good = [r for r in steps if r and r["inliers"] >= 20]
        row = {"id": s["id"], "tc_in": s["tc_in"], "duration": s["duration"], "n_steps": n, "n_good_steps": len(good)}
        if n == 0 or len(good) < 0.5 * n:
            row["label"] = "UNDETERMINED_LOW_TEXTURE"
            rows.append(row)
            continue
        tx = np.array([r["tx"] for r in good]); ty = np.array([r["ty"] for r in good])
        ls = np.array([r["log_s"] for r in good])
        speed = np.hypot(tx, ty)
        med = float(np.median(speed)); cum_s = float(ls.sum())
        sx = max((tx > 0).mean(), (tx < 0).mean()); sy = max((ty > 0).mean(), (ty < 0).mean())
        mx, my = float(np.median(np.abs(tx))), float(np.median(np.abs(ty)))
        if med < 0.5 and abs(cum_s) < 0.02:
            lab = "STATIC"
        elif cum_s >= 0.05:
            lab = "ZOOM_OR_PUSH_IN"
        elif cum_s <= -0.05:
            lab = "ZOOM_OR_PULL_OUT"
        elif sx >= 0.6 and mx >= 0.5 and mx >= my:
            lab = "PAN_OR_TRACK_H"
        elif sy >= 0.6 and my >= 0.5:
            lab = "TILT_OR_PEDESTAL_V"
        elif med >= 0.5:
            lab = "HANDHELD_OR_IRREGULAR"
        else:
            lab = "STATIC"
        row.update({"label": lab, "median_speed_px": round(med, 3), "cum_log_scale": round(cum_s, 4),
                    "median_abs_tx": round(mx, 3), "median_abs_ty": round(my, 3),
                    "sign_consistency_x": round(float(sx), 3), "sign_consistency_y": round(float(sy), 3),
                    "net_tx_px": round(float(tx.sum()), 1), "net_ty_px": round(float(ty.sum()), 1),
                    "median_rot_deg": round(float(np.median([r["rot_deg"] for r in good])), 3)})
        rows.append(row)
    return rows


# ---------------- E3
ORB = cv2.ORB_create(1000)
BF = cv2.BFMatcher(cv2.NORM_HAMMING)


def pair_metrics(a: np.ndarray, b: np.ndarray):
    a2, b2 = CLAHE.apply(a), CLAHE.apply(b)
    ka, da = ORB.detectAndCompute(a2, None)
    kb, db = ORB.detectAndCompute(b2, None)
    inl, ratio, good_n = 0, 0.0, 0
    if da is not None and db is not None and len(ka) >= 8 and len(kb) >= 8:
        ms = BF.knnMatch(da, db, k=2)
        good = [m[0] for m in ms if len(m) == 2 and m[0].distance < 0.75 * m[1].distance]
        good_n = len(good)
        if len(good) >= 8:
            pa = np.float32([ka[m.queryIdx].pt for m in good]); pb = np.float32([kb[m.trainIdx].pt for m in good])
            H, mask = cv2.findHomography(pa, pb, cv2.RANSAC, 5.0)
            if mask is not None:
                inl = int(mask.sum()); ratio = inl / len(good)
    ea = cv2.GaussianBlur(cv2.Canny(a2, 50, 150), (3, 3), 0).astype(np.float32).ravel()
    eb = cv2.GaussianBlur(cv2.Canny(b2, 50, 150), (3, 3), 0).astype(np.float32).ravel()
    corr = float(np.corrcoef(ea, eb)[0, 1]) if ea.std() > 0 and eb.std() > 0 else 0.0
    if inl >= 25 and ratio >= 0.30:
        lab = "SAME_TAKE_LIGHTING"
    elif inl < 8 and corr < 0.20:
        lab = "EDITORIAL_CUT"
    else:
        lab = "UNDETERMINED"
    return {"orb_good": good_n, "inliers": inl, "inlier_ratio": round(ratio, 3), "edge_corr": round(corr, 3), "label": lab}


def dark_boundaries(g: Gray5, segments: list[dict], seed=20261127):
    segs = segments
    hard = [s["start"] for s in segs if s["in_boundary"] == "cut"]
    pos_cut = []
    for t in hard:
        r = pair_metrics(g.at(t - 0.2), g.at(t + 0.2)); r["t"] = t; pos_cut.append(r)
    rng = np.random.default_rng(seed)
    long_shots = [s for s in segs if s["kind"] == "SHOT" and s["duration"] >= 4.0]
    pos_same = []
    tries = 0
    while len(pos_same) < 80 and tries < 5000 and long_shots:
        tries += 1
        s = long_shots[rng.integers(len(long_shots))]
        t = float(rng.uniform(s["start"] + 0.3, s["end"] - 1.3))
        if any(t - 0.1 <= h <= t + 1.1 for h in hard):
            continue
        r = pair_metrics(g.at(t), g.at(t + 1.0)); r["t"] = round(t, 3); r["segment"] = s["id"]; pos_same.append(r)
    cut_as_same = np.mean([r["label"] == "SAME_TAKE_LIGHTING" for r in pos_cut]) if pos_cut else None
    same_as_cut = np.mean([r["label"] == "EDITORIAL_CUT" for r in pos_same]) if pos_same else None
    calib_ok = cut_as_same is not None and cut_as_same <= 0.20 and same_as_cut is not None and same_as_cut <= 0.20
    rows = []
    for i, s in enumerate(segs):
        if s["kind"] != "BLACK":
            continue
        prev = segs[i - 1] if i > 0 else None
        nxt = segs[i + 1] if i + 1 < len(segs) else None
        if not prev or not nxt or prev["kind"] != "SHOT" or nxt["kind"] != "SHOT":
            rows.append({"id": s["id"], "tc_in": s["tc_in"], "label": "NOT_APPLICABLE (no SHOT on both sides)"})
            continue
        r = pair_metrics(g.at(s["start"] - 0.2), g.at(s["end"] + 0.2))
        r.update({"id": s["id"], "tc_in": s["tc_in"], "duration": s["duration"], "prev": prev["id"], "next": nxt["id"]})
        if not calib_ok:
            r["label_reported"] = "INCONCLUSIVE (calibration failed)"
        rows.append(r)
    from collections import Counter
    return {"calibration": {"cut_control_n": len(pos_cut), "cut_control_classified_same": round(float(cut_as_same), 3),
                            "cut_control_label_counts": dict(Counter(r["label"] for r in pos_cut)),
                            "same_control_n": len(pos_same), "same_control_classified_cut": round(float(same_as_cut), 3),
                            "same_control_label_counts": dict(Counter(r["label"] for r in pos_same)),
                            "status": "PASS" if calib_ok else "FAIL"},
            "controls": {"cut": pos_cut, "same": pos_same}, "boundaries": rows,
            "label_counts": dict(Counter(r["label"] for r in rows))}


# ---------------- E4
def music(pcm_path: Path, speech_mask: list[int], sections: list[dict], sr=22050, hop=512, win_s=5):
    import librosa
    y = np.fromfile(pcm_path, dtype="<f4")
    H, P = librosa.effects.hpss(y)
    eh = librosa.feature.rms(y=H, hop_length=hop)[0] ** 2
    ep = librosa.feature.rms(y=P, hop_length=hop)[0] ** 2
    onset = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    chroma = librosa.feature.chroma_stft(y=H, sr=sr, hop_length=hop)
    peak = chroma.max(0) / (chroma.sum(0) + 1e-9)
    flat = librosa.feature.spectral_flatness(y=y, hop_length=hop)[0]
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    fps = sr / hop
    n_win = int(math.ceil(len(y) / sr / win_s))
    wins = []
    for w in range(n_win):
        a, b = int(w * win_s * fps), int((w + 1) * win_s * fps)
        s0, s1 = w * win_s, min(len(speech_mask), (w + 1) * win_s)
        sp = float(np.mean(speech_mask[s0:s1])) if s1 > s0 else 0.0
        seg = y[int(w * win_s * sr):int((w + 1) * win_s * sr)]
        tempo, beats = (0.0, np.array([]))
        if len(seg) > sr:
            tempo, beats = librosa.beat.beat_track(y=seg, sr=sr, hop_length=hop, units="time")
        ibi = np.diff(beats) if len(beats) > 2 else np.array([])
        cv = float(ibi.std() / ibi.mean()) if len(ibi) >= 2 and ibi.mean() > 0 else None
        hr = float(eh[a:b].sum() / (eh[a:b].sum() + ep[a:b].sum() + 1e-12))
        rec = {"t": w * win_s, "speech_frac": round(sp, 2), "harmonic_ratio": round(hr, 3),
               "onset_mean": round(float(onset[a:b].mean()), 3) if b > a else None,
               "tempo_bpm": round(float(np.atleast_1d(tempo)[0]), 1), "n_beats": int(len(beats)),
               "ibi_cv": round(cv, 3) if cv is not None else None,
               "chroma_peakiness": round(float(peak[a:b].mean()), 3), "flatness": round(float(flat[a:b].mean()), 4),
               "rms_db": round(float(20 * np.log10(rms[a:b].mean() + 1e-9)), 2)}
        if sp >= 0.5:
            lab = "SPEECH"
        elif hr >= 0.60 and rec["chroma_peakiness"] >= 0.25:
            lab = "MUSIC_LIKELY"
        elif cv is not None and cv <= 0.15 and len(beats) >= 8:
            lab = "RHYTHMIC"
        elif rec["flatness"] >= 0.30:
            lab = "NOISE_OR_AMBIENCE"
        else:
            lab = "UNDETERMINED"
        rec["label"] = lab
        wins.append(rec)
    sec_out = []
    for s in sections:
        ws = [w for w in wins if s["start"] <= w["t"] < s["end"]]
        from collections import Counter
        sec_out.append({"label_v1": s["label"], "start": s["start"], "end": s["end"],
                        "window_labels": dict(Counter(w["label"] for w in ws)),
                        "harmonic_ratio_mean": round(float(np.mean([w["harmonic_ratio"] for w in ws])), 3) if ws else None,
                        "chroma_peakiness_mean": round(float(np.mean([w["chroma_peakiness"] for w in ws])), 3) if ws else None})
    from collections import Counter
    return {"windows": wins, "sections": sec_out, "label_counts_windows": dict(Counter(w["label"] for w in wins)),
            "params": {"sr": sr, "hop": hop, "win_s": win_s, "librosa": librosa.__version__}}
