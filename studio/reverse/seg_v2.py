"""S1 segmentation v2 (pre-registered: runs/2026-11-27-seg-v2/PREREG_SEG_V2_2026-11-27.md, commit 1959fa9).

Union of cut detectors + O3 decode confirmation + linear-blend dissolve detection; verified camera spans helpers.
Writes NEW files only (pack-v2/seg/). v1 pack and pack-ext are read-only inputs.
"""
from __future__ import annotations

import argparse, json, math, subprocess, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import numpy as np

from .evidence_checks import window_diffs, judge
from .film_baseline import parse_scene_scores

FPS = 30000 / 1001
TOL = 3 / FPS
W5, H5, F5 = 320, 180, 5.0
SEED = 20261128


# ---------------- S1 candidates
def candidates(v1_cuts, sd_content, sd_adaptive, st, ss, blacks, thr=0.10):
    score_at = lambda t: float(ss[np.argmin(np.abs(st - t))])
    raw = [(t, "v1") for t in v1_cuts] + [(t, "pysd_content") for t in sd_content] + [(t, "pysd_adaptive") for t in sd_adaptive]
    raw += [(float(t), "ffmpeg_0.10") for t, s in zip(st, ss) if s >= thr]
    raw.sort()
    groups, cur = [], []
    for t, src in raw:
        if cur and t - cur[-1][0] > TOL:
            groups.append(cur); cur = []
        cur.append((t, src))
    if cur:
        groups.append(cur)
    out, dropped_black = [], 0
    for g in groups:
        best = max(g, key=lambda x: (score_at(x[0]), -x[0]))[0]
        inside = any(b0 + 2 / FPS < best < b1 - 2 / FPS for b0, b1 in blacks)
        if inside:
            dropped_black += 1
            continue
        out.append({"t": round(best, 4), "sources": sorted({s for _, s in g}), "scene_score": round(score_at(best), 4)})
    return out, dropped_black, len(raw)


def confirm(mkv, ts, workers=6):
    def run(t):
        try:
            d, c = window_diffs(mkv, t)
            r = judge(d, c)
        except Exception as e:  # decode failure logged
            r = {"confirmed": None, "error": str(e)[:200]}
        return r or {"confirmed": None, "error": "window too short"}
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(run, ts))


# ---------------- S3 dissolves
class G5:
    def __init__(self, path):
        self.m = np.memmap(path, dtype=np.uint8, mode="r"); self.n = self.m.size // (W5 * H5)
    def small(self, i):
        i = max(0, min(self.n - 1, i))
        f = np.asarray(self.m[i * W5 * H5:(i + 1) * W5 * H5]).reshape(H5, W5)
        return cv2.resize(f, (80, 45), interpolation=cv2.INTER_AREA).astype(np.float32)
    def full(self, i):
        i = max(0, min(self.n - 1, i))
        return np.asarray(self.m[i * W5 * H5:(i + 1) * W5 * H5]).reshape(H5, W5)


def edge_corr(a, b):
    ea = cv2.Canny(cv2.GaussianBlur(a.astype(np.uint8), (3, 3), 0), 50, 150).astype(np.float32)
    eb = cv2.Canny(cv2.GaussianBlur(b.astype(np.uint8), (3, 3), 0), 50, 150).astype(np.float32)
    if ea.std() == 0 or eb.std() == 0:
        return 0.0
    return float(np.corrcoef(ea.ravel(), eb.ravel())[0, 1])


def _avg_rank(v):
    v = np.asarray(v, dtype=float)
    order = np.argsort(v, kind="mergesort")
    r = np.empty(len(v))
    r[order] = np.arange(len(v), dtype=float)
    for u in np.unique(v):
        m = v == u
        r[m] = r[m].mean()
    return r


def spearman(x, y):
    """Spearman rho with average ranks for ties."""
    rx, ry = _avg_rank(x), _avg_rank(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def blend_test(frames):
    A, B = frames[0], frames[-1]
    if A.mean() < 20 or B.mean() < 20:
        return None
    diff = A - B
    if np.abs(diff).mean() < 10 or edge_corr(A, B) >= 0.5:
        return None
    nd = float((diff ** 2).sum())
    al, rs = [], []
    for f in frames[1:-1]:
        a = float(((f - B) * diff).sum() / nd)
        a = min(1.0, max(0.0, a))
        fit = a * A + (1 - a) * B
        al.append(a); rs.append(float(np.linalg.norm(f - fit) / math.sqrt(nd)))
    al, rs = np.array(al), np.array(rs)
    mid = (al > 0.15) & (al < 0.85)
    ok = (spearman(np.arange(len(al)), al) <= -0.9 and mid.sum() >= 3 and float(np.median(rs[mid])) <= 0.35
          and al[0] >= 0.7 and al[-1] <= 0.3) if mid.sum() >= 3 else False
    return {"ok": bool(ok), "alphas": al.round(3).tolist(), "mid_resid_median": round(float(np.median(rs[mid])), 3) if mid.any() else None}


def dissolves(g: G5, cuts, blacks, duration):
    hits = []
    excl = [(c - 0.2, c + 0.2) for c in cuts] + [(b0 - 0.2, b1 + 0.2) for b0, b1 in blacks]
    excl.sort()
    def blocked(a, b):
        return any(x0 < b and a < x1 for x0, x1 in excl)
    for L, n in ((2.0, 11), (4.0, 21)):
        c = L / 2
        while c + L / 2 <= duration:
            a, b = c - L / 2, c + L / 2
            if not blocked(a, b):
                i0 = int(round(a * F5))
                fr = [g.small(i0 + k) for k in range(n)]
                r = blend_test(fr)
                if r and r["ok"]:
                    al = np.array(r["alphas"]); ts = a + (np.arange(1, n - 1) / F5)
                    m = (al > 0.15) & (al < 0.85)
                    hits.append({"L": L, "start": round(float(ts[m].min()), 3), "end": round(float(ts[m].max()), 3),
                                 "centre": round(float(ts[np.argmin(np.abs(al - 0.5))]), 3), "resid": r["mid_resid_median"]})
            c += 0.5
    hits.sort(key=lambda h: h["start"])
    spans = []
    for h in hits:
        if spans and h["start"] <= spans[-1]["end"] + 0.2:
            s = spans[-1]; s["end"] = max(s["end"], h["end"]); s["n_windows"] += 1
        else:
            spans.append({"start": h["start"], "end": h["end"], "centre": h["centre"], "n_windows": 1})
    out = []
    for s in spans:
        if s["end"] - s["start"] < 0.4:
            s["end"] = s["start"] + 0.4
        if any(s["start"] <= c <= s["end"] for c in cuts):
            continue
        out.append({k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items()})
    return out


def dissolve_controls(g: G5, v1segs, cam_rows, rng):
    shots = [s for s in v1segs if s["kind"] == "SHOT" and s["duration"] >= 2]
    pos = []
    for k in range(50):
        L, n = (1.0, 6) if k < 25 else (2.0, 11)
        s1, s2 = rng.choice(len(shots), 2, replace=False)
        A = g.small(int((shots[s1]["start"] + shots[s1]["duration"] / 2) * F5))
        B = g.small(int((shots[s2]["start"] + shots[s2]["duration"] / 2) * F5))
        # embed blend inside a 2 s / 4 s test window like the detector does: hold A, ramp, hold B
        W = 11 if L == 1.0 else 21
        ramp = np.linspace(1, 0, n)
        pre = (W - n) // 2
        seq = [A] * pre + [r * A + (1 - r) * B for r in ramp] + [B] * (W - pre - n)
        r = blend_test(seq)
        pos.append(None if r is None else r["ok"])
    static = {r["id"] for r in cam_rows if r.get("label") == "STATIC"}
    cand = [s for s in v1segs if s["id"] in static and s["duration"] >= 6]
    neg = []
    for k in range(80):
        s = cand[rng.integers(len(cand))]
        a = rng.uniform(s["start"] + 0.5, s["end"] - 2.5)
        fr = [g.small(int(round(a * F5)) + j) for j in range(11)]
        r = blend_test(fr)
        neg.append(bool(r and r["ok"]))
    pv = [p for p in pos if p is not None]
    pr = float(np.mean(pv)) if pv else 0.0
    nr = float(np.mean(neg))
    return {"synthetic_positive_detected": f"{sum(pv)}/{len(pos)} (skipped by A/B gates: {sum(p is None for p in pos)})",
            "synthetic_positive_rate_over_all": round(sum(pv) / len(pos), 3), "negative_false_positive": f"{sum(neg)}/{len(neg)}",
            "PASS": bool(sum(pv) / len(pos) >= 0.80 and nr <= 0.10)}


# ---------------- S5 verification helpers
def native_cut_free(mkv, a, b):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{a:.3f}", "-i", str(mkv), "-t", f"{b - a:.3f}", "-an",
           "-vf", "scale=64:36,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 36, 64).astype(np.float32)
    if len(fr) < 3:
        return False, None
    d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
    med = max(float(np.median(d)), 0.5)
    bad = int(((d >= 8) & (d >= 3 * med)).sum())
    return bad == 0, {"n_frames": int(len(fr)), "max_d": round(float(d.max()), 3), "median_d": round(med, 3), "flagged_pairs": bad}


def build_segments(cut_t, blacks, ds, v1, dur):
    """Boundaries = cuts ∪ BLACK edges ∪ dissolve edges. Boundaries closer than 2 frames are one boundary
    (BLACK edge value preferred, then dissolve edge, then cut), so no zero-length slivers or gaps arise."""
    tol = 2 / FPS
    pts = [(x, 0) for b in blacks for x in b] + [(x, 1) for d in ds for x in (d["start"], d["end"])] + [(t, 2) for t in cut_t] + [(0.0, -1), (dur, -1)]
    pts.sort()
    groups, cur = [], []
    for t, pr in pts:
        if cur and t - cur[0][0] > tol:
            groups.append(cur); cur = []
        cur.append((t, pr))
    groups.append(cur)
    bset = [min(g, key=lambda x: (x[1], x[0]))[0] for g in groups]
    snap = lambda x: min(bset, key=lambda b: abs(b - x))
    bl = [(snap(b0), snap(b1)) for b0, b1 in blacks]
    dd = [(snap(d["start"]), snap(d["end"])) for d in ds]
    cnt = {"SHOT": 0, "BLACK": 0, "DISSOLVE": 0}
    pref = {"SHOT": "S2-SH", "BLACK": "S2-BK", "DISSOLVE": "S2-DS"}
    segs = []
    for x0, x1 in zip(bset, bset[1:]):
        if any(b0 <= x0 and x1 <= b1 for b0, b1 in bl):
            k = "BLACK"
        elif any(abs(x0 - a0) < 1e-6 and abs(x1 - a1) < 1e-6 for a0, a1 in dd):
            k = "DISSOLVE"
        else:
            k = "SHOT"
        cnt[k] += 1
        ov = [s["id"] for s in v1 if min(x1, s["end"]) - max(x0, s["start"]) > tol]  # overlap longer than 2 frames
        segs.append({"id": f"{pref[k]}{cnt[k]:03d}", "kind": k, "start": round(x0, 4), "end": round(x1, 4), "duration": round(x1 - x0, 4), "v1_overlap": ov})
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--rebuild-segments-only", action="store_true", help="re-run S4 from saved S1-S3 outputs (no decode)")
    a = ap.parse_args()
    if a.rebuild_segments_only:
        return rebuild(a)
    t0 = time.time()
    pack, ext = a.src / "pack", a.src / "pack-ext"
    mkv = a.src / "staging/onNBysMf9WM.mkv"
    S = json.load(open(pack / "shots/segments.json"))
    v1 = S["segments"]; dur = v1[-1]["end"]
    blacks = [(s["start"], s["end"]) for s in v1 if s["kind"] == "BLACK"]
    v1_cuts = [c["t"] for c in S["hard_cuts"]]
    sd = json.load(open(ext / "scenedetect_cuts.json"))["raw"]
    st, ss = parse_scene_scores(pack / "work/scene_scores.txt")
    cand, dropped, n_raw = candidates(v1_cuts, sd["content"], sd["adaptive"], st, ss, blacks)
    print("candidates", len(cand), "dropped_in_black", dropped, "raw", n_raw, flush=True)
    res = confirm(mkv, [c["t"] for c in cand])
    for c, r in zip(cand, res):
        c.update(r)
    conf = [c for c in cand if c.get("confirmed") is True]
    v1_re = [c for c in cand if "v1" in c["sources"]]
    v1_frac = sum(c.get("confirmed") is True for c in v1_re) / len(v1_re)
    rng = np.random.default_rng(SEED)
    edges = sorted([c["t"] for c in cand] + [x for b in blacks for x in b])
    neg_t = []
    while len(neg_t) < min(300, len(conf)):
        t = float(rng.uniform(2, dur - 2))
        j = np.searchsorted(edges, t)
        near = min(abs(edges[k] - t) for k in (j - 1, j) if 0 <= k < len(edges))
        if near >= 2.0:
            neg_t.append(round(t, 3))
    negr = confirm(mkv, neg_t)
    neg_fp = sum(r.get("confirmed") is True for r in negr) / len(negr)
    s2 = {"v1_reconfirmed": f"{sum(c.get('confirmed') is True for c in v1_re)}/{len(v1_re)}", "v1_reconfirmed_fraction": round(v1_frac, 4),
          "negative_false_confirm": f"{sum(r.get('confirmed') is True for r in negr)}/{len(negr)}", "negative_false_confirm_fraction": round(neg_fp, 4),
          "PASS": bool(v1_frac >= 0.95 and neg_fp <= 0.10), "decode_errors": sum(c.get("confirmed") is None for c in cand)}
    print("S2", s2, flush=True)
    g = G5(pack / "work/frames_5fps_320x180.gray")
    cut_t = [c["t"] for c in conf]
    ds = dissolves(g, cut_t, blacks, dur)
    cam_rows = json.load(open(ext / "camera_motion.json"))["rows"]
    dctl = dissolve_controls(g, v1, cam_rows, np.random.default_rng(SEED))
    print("S3", len(ds), dctl, flush=True)
    # S4 segments
    segs = build_segments(cut_t, blacks, ds, v1, dur)
    new_cuts = [c for c in conf if "v1" not in c["sources"]]
    shots = [s for s in segs if s["kind"] == "SHOT"]
    cnt = {k: sum(x["kind"] == k for x in segs) for k in ("SHOT", "BLACK", "DISSOLVE")}
    d1 = np.array([s["duration"] for s in v1 if s["kind"] == "SHOT"]); d2 = np.array([s["duration"] for s in shots])
    stats = {"v1": {"hard_cuts": len(v1_cuts), "SHOT": int(len(d1)), "BLACK": len(blacks), "shot_median_s": round(float(np.median(d1)), 3),
                    "shot_mean_s": round(float(d1.mean()), 3), "longest": round(float(d1.max()), 3)},
             "v2": {"candidates_after_merge": len(cand), "raw_candidate_events": n_raw, "dropped_inside_black": dropped,
                    "confirmed_cuts": len(conf), "new_vs_v1": len(new_cuts), "v1_not_reconfirmed": [c["t"] for c in v1_re if c.get("confirmed") is not True],
                    "unconfirmed_candidates": sum(c.get("confirmed") is False for c in cand), "dissolve_spans": len(ds),
                    "SHOT": len(shots), "BLACK": cnt["BLACK"], "DISSOLVE": cnt["DISSOLVE"],
                    "shot_median_s": round(float(np.median(d2)), 3), "shot_mean_s": round(float(d2.mean()), 3), "longest": round(float(d2.max()), 3),
                    "new_cut_sources": {k: sum(k in c["sources"] for c in new_cuts) for k in ("pysd_content", "pysd_adaptive", "ffmpeg_0.10")}},
             "informational_reviewer_r2_dissolves_NOT_TRUTH": {str(t): any(d["start"] - 0.5 <= t <= d["end"] + 0.5 for d in ds) for t in (1412.45, 1759.12)},
             "S2_controls": s2, "S3_controls": dctl, "elapsed_s": round(time.time() - t0, 1)}
    a.out.mkdir(parents=True, exist_ok=True)
    json.dump({"schema": "s1-seg-v2.v1", "prereg": "PREREG_SEG_V2_2026-11-27.md@1959fa9", "candidates": cand}, open(a.out / "cut_candidates_v2.json", "w"))
    json.dump({"negatives": [dict(t=t, **r) for t, r in zip(neg_t, negr)]}, open(a.out / "o3_negative_control_v2.json", "w"))
    json.dump({"schema": "s1-seg-v2.v1", "dissolves": ds, "controls": dctl}, open(a.out / "dissolves_v2.json", "w"), indent=1)
    json.dump({"schema": "s1-seg-v2.v1", "segments": segs, "confirmed_cuts": cut_t, "dissolves": ds}, open(a.out / "segments_v2.json", "w"))
    json.dump(stats, open(a.out / "seg_v2_stats.json", "w"), indent=1)
    print(json.dumps(stats, indent=1))


def rebuild(a):
    pack = a.src / "pack"
    S = json.load(open(pack / "shots/segments.json")); v1 = S["segments"]; dur = v1[-1]["end"]
    blacks = [(s["start"], s["end"]) for s in v1 if s["kind"] == "BLACK"]
    cand = json.load(open(a.out / "cut_candidates_v2.json"))["candidates"]
    ds = json.load(open(a.out / "dissolves_v2.json"))["dissolves"]
    cut_t = [c["t"] for c in cand if c.get("confirmed") is True]
    segs = build_segments(cut_t, blacks, ds, v1, dur)
    json.dump({"schema": "s1-seg-v2.v1", "segments": segs, "confirmed_cuts": cut_t, "dissolves": ds}, open(a.out / "segments_v2.json", "w"))
    st = json.load(open(a.out / "seg_v2_stats.json"))
    shots = [s for s in segs if s["kind"] == "SHOT"]; d2 = np.array([s["duration"] for s in shots])
    st["v2"].update({"SHOT": len(shots), "BLACK": sum(s["kind"] == "BLACK" for s in segs), "DISSOLVE": sum(s["kind"] == "DISSOLVE" for s in segs),
                     "shot_median_s": round(float(np.median(d2)), 3), "shot_mean_s": round(float(d2.mean()), 3), "longest": round(float(d2.max()), 3),
                     "min_segment_s": round(min(s["duration"] for s in segs), 4)})
    st["S4_note"] = "boundaries within 2 frames merged (BLACK edge preferred) — fixes zero-length slivers/gaps of the first S4 pass"
    json.dump(st, open(a.out / "seg_v2_stats.json", "w"), indent=1)
    print(json.dumps(st["v2"], indent=1))


if __name__ == "__main__":
    main()
