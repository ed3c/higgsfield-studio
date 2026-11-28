"""S1 segmentation v3 (pre-registered: runs/2026-11-27-seg-v3/PREREG_SEG_V3_2026-11-27.md, commit bf87fac).

(a) light-change vs cut discriminator, (b) jump cuts, (c) near-black cuts, (d) revised dissolves.
Thresholds chosen on declared tuning data by the pre-registered rule, frozen, then validated once on held-out data.
Writes NEW files only (pack-v3/seg/). v1/v2 packs are read-only inputs.
"""
from __future__ import annotations

import argparse, json, math, time
from pathlib import Path

import cv2
import numpy as np

from .seg_v2 import G5, F5, spearman, build_segments

FPS = 30000 / 1001
W, H = 128, 72
SEED_T, SEED_H = 3001, 3002
TUNE = {"light": [802.2348, 2184.516, 2184.783, 2185.2497], "jump": [83.35, 1723.755, 1899.164, 1694.76],
        "dark": [2182.647, 2157.99, 2170.97, 437.837], "other_cuts": [858.39, 864.46, 876.74, 2089.39, 285.752, 136.2],
        "dis_pos": [1412.45, 1759.12, 2247.3], "dis_neg": [(130.9, 135.6), (1441.1, 1442.7)]}


def tuning_exclusions(pad=2.0):
    """Round-4 exclusion intervals for all declared tuning data."""
    ts = TUNE["light"] + TUNE["jump"] + TUNE["dark"] + TUNE["other_cuts"] + TUNE["dis_pos"]
    return [(t - pad, t + pad) for t in ts] + [(a - pad, b + pad) for a, b in TUNE["dis_neg"]]


# ---------------- features
def edge(f):
    g = cv2.GaussianBlur(f.astype(np.float32), (0, 0), 1.0)
    m = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
    s = m.std()
    return None if s < 1e-6 else (m - m.mean()) / s


def S(ea, eb):
    if ea is None or eb is None:
        return 0.0
    return float((ea * eb).mean())


def darknorm(f):
    f = f.astype(np.float32); med = np.median(f); mad = np.median(np.abs(f - med)) * 1.4826
    g = cv2.GaussianBlur((f - med) / max(mad, 0.6), (0, 0), 1.5)
    s = g.std()
    return None if s < 1e-6 else (g - g.mean()) / s


class Full:
    def __init__(self, path):
        self.m = np.memmap(path, dtype=np.uint8, mode="r"); self.n = self.m.size // (W * H)
    def f(self, k):
        k = max(0, min(self.n - 1, k))
        return np.asarray(self.m[k * W * H:(k + 1) * W * H]).reshape(H, W).astype(np.float32)
    def seq(self, k0, k1):
        return [self.f(k) for k in range(k0, k1)]


def seq_feats(frames):
    """Index k compares k-1,k. Returns D_struct, D_dark, mean, std arrays."""
    n = len(frames)
    E = [edge(f) for f in frames]; N = [darknorm(f) for f in frames]
    mean = np.array([f.mean() for f in frames]); std = np.array([f.std() for f in frames])
    Ds, Dd = np.zeros(n), np.zeros(n)
    for k in range(1, n):
        Ds[k] = 1 - S(E[k - 1], E[k]); Dd[k] = 1 - S(N[k - 1], N[k])
    return {"Ds": Ds, "Dd": Dd, "mean": mean, "std": std, "E": E}


def Q_at(E, k):
    """Light-change ratio at boundary k (E: list of edge maps; needs k-2..k+1)."""
    sx = np.median([S(E[k - 1], E[k]), S(E[k - 2], E[k + 1]), S(E[k - 1], E[k + 1]), S(E[k - 2], E[k])])
    sw = np.median([S(E[k - 2], E[k - 1]), S(E[k], E[k + 1])])
    return float(sx / max(sw, 0.05))


def localise(E, k):
    """Boundary = frame within ±1 of the listed one with the largest structure change."""
    return max((k - 1, k, k + 1), key=lambda j: 1 - S(E[j - 1], E[j]))


def spikes(D, k_range, r, dmin, ok=lambda k: True):
    out = []
    for k in k_range:
        if k < 2 or k >= len(D) - 1 or D[k] < dmin or D[k] < 2 * max(D[k - 1], D[k + 1]):
            continue
        lo, hi = max(1, k - 15), min(len(D), k + 16)
        base = [D[j] for j in range(lo, hi) if abs(j - k) > 1]
        if base and D[k] >= r * max(float(np.median(base)), 0.01) and ok(k):
            out.append(k)
    return out


# ---------------- synthetic sets
def pools(v2segs):
    shots = sorted([s for s in v2segs if s["kind"] == "SHOT" and s["duration"] >= 6], key=lambda s: s["start"])
    return shots[0::2], shots[1::2]


def far_from(t, ts, d=1.0):
    return all(abs(t - u) >= d for u in ts)


def exposure_step(F, seg, rng):
    k = int(rng.uniform(seg["start"] + 1, seg["end"] - 1) * FPS)
    fr = F.seq(k - 2, k + 2)
    g = rng.uniform(0.4, 0.7) if rng.random() < 0.5 else rng.uniform(1.4, 2.5)
    gam, off = rng.uniform(0.7, 1.4), rng.uniform(-10, 10)
    for j in (2, 3):
        fr[j] = np.clip(255 * (np.clip(fr[j] * g + off, 0, 255) / 255) ** gam, 0, 255)
    return fr


def jump_seq(F, seg, rng):
    for _ in range(50):
        p = rng.uniform(seg["start"] + 1.5, seg["end"] - 7.5); dl = rng.uniform(2, 6)
        if p + dl + 1.5 < seg["end"]:
            break
    else:
        return None
    k1, k2 = int(p * FPS), int((p + dl) * FPS)
    pre, post = F.seq(k1 - 45, k1), F.seq(k2, k2 + 45)
    if rng.random() < 0.5:
        c = rng.uniform(0.05, 0.12); dx, dy = int(W * c / 2), int(H * c / 2)
        post = [cv2.resize(f[dy:H - dy, dx:W - dx], (W, H), interpolation=cv2.INTER_AREA) for f in post]
    return pre + post  # boundary at 45


def dark_cut(F, sa, sb, rng):
    for _ in range(20):
        g, sg = rng.uniform(0.04, 0.12), rng.uniform(0.5, 1.0)
        ka = int(rng.uniform(sa["start"] + 0.6, sa["end"] - 0.6) * FPS); kb = int(rng.uniform(sb["start"] + 0.6, sb["end"] - 0.6) * FPS)
        A, B = F.seq(ka - 15, ka), F.seq(kb, kb + 15)
        if (A[-1] * g).std() >= 0.8 and (B[0] * g).std() >= 0.8:
            mk = lambda f: np.clip(np.round(f * g + rng.normal(0, sg, f.shape)), 0, 255)
            return [mk(f) for f in A] + [mk(f) for f in B]
    return None


def dark_static(F, seg, rng):
    g, sg = rng.uniform(0.04, 0.12), rng.uniform(0.5, 1.0)
    k = int(rng.uniform(seg["start"] + 0.6, seg["end"] - 1.6) * FPS)
    return [np.clip(np.round(f * g + rng.normal(0, sg, f.shape)), 0, 255) for f in F.seq(k, k + 30)]


# ---------------- (d) dissolves on 5 fps 80x45
def blend_fit(P, i0, n, cut_inside=False):
    A, B = P[i0], P[i0 + n - 1]
    d = A - B; rms = float(np.sqrt((d ** 2).mean()))
    if rms < 4 or cut_inside:
        return None
    nd = float((d ** 2).sum()); al, rs = [], []
    for f in P[i0:i0 + n]:
        a = float(((f - B) * d).sum() / nd); al.append(a)
        rs.append(float(np.sqrt(((f - (a * A + (1 - a) * B)) ** 2).mean()) / rms))
    al = np.array(al); m = max(1, int(math.ceil(0.2 * n)))
    return {"sab": S(edge(A), edge(B)), "rho": spearman(np.arange(n), al), "first": float(al[:m].mean()), "last": float(al[-m:].mean()),
            "mid": int(((al > 0.15) & (al < 0.85)).sum()), "r": float(np.median(rs)), "al": al}


def dis_ok(fit, tr, ts, rho):
    return bool(fit and fit["sab"] < ts and fit["rho"] <= rho and fit["first"] >= 0.7 and fit["last"] <= 0.3 and fit["mid"] >= 2 and fit["r"] <= tr)


def dis_scan(P, t0=0.0, cuts=(), stride=2):
    """All window fits over a 5 fps frame list P (t0 = time of P[0]). Returns list of (start_t, end_t, fit)."""
    out = []
    for L in (1, 2, 3, 4):
        n = 5 * L + 1
        for i0 in range(0, len(P) - n + 1, stride):
            a, b = t0 + i0 / F5, t0 + (i0 + n - 1) / F5
            ci = any(a + 0.1 < c < b - 0.1 for c in cuts)
            out.append((a, b, blend_fit(P, i0, n, ci)))
    return out


def dis_seq(G, sa, sb, L, rng, which="pos"):
    ia = int(rng.uniform(sa["start"] + 0.5, sa["end"] - L - 2.5) * F5); ib = int(rng.uniform(sb["start"] + 0.5, sb["end"] - L - 2.5) * F5)
    A = [G.small(ia + j) for j in range(5 * L + 10)]; B = [G.small(ib + j) for j in range(5 * L + 10)]
    if A[5].std() < 3 or B[5 + 5 * L].std() < 3:
        return None
    w = np.clip((np.arange(5 * L + 10) - 5) / (5 * L), 0, 1)
    return [(1 - x) * a + x * b for x, a, b in zip(w, A, B)], (1.0, 1.0 + L)


def run(a):
    t_start = time.time()
    src = a.src; out = a.out; out.mkdir(parents=True, exist_ok=True)
    log = open(out / "run.log", "w")
    def say(*x):
        s = " ".join(str(v) for v in x); print(s, flush=True); log.write(s + "\n"); log.flush()
    F = Full(src / "pack-v3/work/frames_full_128x72.gray"); say("frames", F.n)
    G = G5(src / "pack/work/frames_5fps_320x180.gray")
    v1 = json.load(open(src / "pack/shots/segments.json"))["segments"]; dur = v1[-1]["end"]
    S2 = json.load(open(src / "pack-v2/seg/segments_v2.json")); v2segs = S2["segments"]
    cands = json.load(open(src / "pack-v2/seg/cut_candidates_v2.json"))["candidates"]
    cand_t = [c["t"] for c in cands]
    conf = [c for c in cands if c.get("confirmed") is True]
    blacks = [(s["start"], s["end"]) for s in v1 if s["kind"] == "BLACK"]
    v1cuts = sorted(c["t"] for c in conf if "v1" in c["sources"])
    tun_pool, ho_pool = pools(v2segs)
    say("pools tuning/held-out", len(tun_pool), len(ho_pool), "v1 cuts", len(v1cuts))
    ctl, thr = {}, {}

    def Ek(t):
        k = int(round(t * FPS)); E = {j: edge(F.f(j)) for j in range(k - 4, k + 4)}
        kk = max((k - 1, k, k + 1), key=lambda j: 1 - S(E[j - 1], E[j]))
        return Q_at(E, kk), kk

    # ---- (a)
    qa_cut_t = [Ek(t)[0] for t in v1cuts[1::2]]; qa_cut_h = [Ek(t)[0] for t in v1cuts[0::2]]
    qa_lc_real = [Ek(t)[0] for t in TUNE["light"]]
    def steps(pool, seed):
        rng = np.random.default_rng(seed); qs = []
        for i in range(60):
            fr = exposure_step(F, pool[rng.integers(len(pool))], rng); E = [edge(f) for f in fr]; qs.append(Q_at(E, 2))
        return qs
    qa_st_t, qa_st_h = steps(tun_pool, SEED_T), steps(ho_pool, SEED_H)
    best = None
    for ta in (0.5, 0.6, 0.7, 0.8, 0.9):
        tpr = np.mean([q < ta for q in qa_cut_t]); tnr = np.mean([q >= ta for q in qa_lc_real + qa_st_t])
        ba = (tpr + tnr) / 2
        if best is None or ba > best[0] or (ba == best[0] and ta > best[1]):
            best = (ba, ta)
    ta = best[1]; thr["a"] = {"tau_a": ta, "tuning_balanced_accuracy": round(best[0], 3)}
    keep_h = np.mean([q < ta for q in qa_cut_h]); lc_h = np.mean([q >= ta for q in qa_st_h])
    ctl["a"] = {"tuning": {"v1_cuts_kept": f"{sum(q < ta for q in qa_cut_t)}/{len(qa_cut_t)}", "known_light_changes_flagged": f"{sum(q >= ta for q in qa_lc_real)}/4",
                           "known_light_Q": [round(q, 3) for q in qa_lc_real], "exposure_steps_flagged": f"{sum(q >= ta for q in qa_st_t)}/60"},
                "held_out": {"v1_cuts_kept": f"{sum(q < ta for q in qa_cut_h)}/{len(qa_cut_h)}", "exposure_steps_flagged": f"{sum(q >= ta for q in qa_st_h)}/60"},
                "PASS": bool(keep_h >= 0.95 and lc_h >= 0.90)}
    say("(a)", json.dumps(ctl["a"]), thr["a"])
    A_ok = ctl["a"]["PASS"]
    def not_light(E, k):
        return (not A_ok) or k < 2 or k + 1 >= len(E) or Q_at(E, k) < ta

    # ---- (b)
    def jump_sets(pool, seed):
        rng = np.random.default_rng(seed); pos, neg = [], []
        big = [s for s in pool if s["duration"] >= 10]
        while len(pos) < 60:
            q = jump_seq(F, big[rng.integers(len(big))], rng)
            if q is not None:
                pos.append(seq_feats(q))
        while len(neg) < 100:
            s = pool[rng.integers(len(pool))]; t = rng.uniform(s["start"] + 1, s["end"] - 3)
            if far_from(t, cand_t) and far_from(t + 2, cand_t):
                k = int(t * FPS); neg.append(seq_feats(F.seq(k - 15, k + 75)))
        return pos, neg
    jp_t, jn_t = jump_sets(tun_pool, SEED_T); jp_h, jn_h = jump_sets(ho_pool, SEED_H)
    jr_t = []
    for t in TUNE["jump"]:
        k = int(round(t * FPS)); jr_t.append((seq_feats(F.seq(k - 45, k + 45)), 45))
    def jdet(ft, rb, dm, rng_k):
        okf = lambda k: ft["mean"][k - 1] >= 25 and ft["mean"][k] >= 25 and not_light(ft["E"], k)
        return spikes(ft["Ds"], rng_k, rb, dm, okf)
    def jscore(pos, neg, real, rb, dm):
        hit = [any(abs(k - 45) <= 2 for k in jdet(p, rb, dm, range(40, 51))) for p in pos]
        hr = [any(abs(k - c) <= 2 for k in jdet(p, rb, dm, range(c - 5, c + 6))) for p, c in real]
        fp = [bool(jdet(n, rb, dm, range(15, 75))) for n in neg]
        return hit, hr, fp
    best = None
    for rb in (4, 6, 8, 12):
        for dm in (0.05, 0.1, 0.2):
            hit, hr, fp = jscore(jp_t, jn_t, jr_t, rb, dm)
            rec = (sum(hit) + sum(hr)) / (len(hit) + len(hr)); fpr = np.mean(fp)
            key = (rec - fpr, rb, dm)
            if fpr <= 0.05 and (best is None or key > best[0]):
                best = (key, rb, dm, rec, fpr, sum(hr))
    if best is None:
        thr["b"] = None; ctl["b"] = {"PASS": False, "note": "no grid point met tuning FP <= 5%"}
    else:
        _, rb, dm, rec, fpr, nhr = best; thr["b"] = {"rb": rb, "Dmin": dm}
        hit, _, fp = jscore(jp_h, jn_h, [], rb, dm)
        ctl["b"] = {"tuning": {"recall_incl_known": round(rec, 3), "known_jump_cuts_hit": f"{nhr}/4", "static_FP": round(fpr, 3)},
                    "held_out": {"synthetic_recall": f"{sum(hit)}/60", "static_FP": f"{sum(fp)}/100"},
                    "PASS": bool(np.mean(hit) >= 0.80 and np.mean(fp) <= 0.05)}
    say("(b)", json.dumps(ctl["b"]), thr["b"])

    # ---- (c)
    def dark_sets(pool, seed):
        rng = np.random.default_rng(seed); pos, neg = [], []
        while len(pos) < 60:
            i, j = rng.choice(len(pool), 2, replace=False); q = dark_cut(F, pool[i], pool[j], rng)
            if q is not None:
                pos.append(seq_feats(q))
        bl = [b for b in blacks if b[1] - b[0] >= 4.5]
        half = bl[0::2] if seed == SEED_T else bl[1::2]
        tries = 0
        while len(neg) < 50 and tries < 5000:
            tries += 1; b0, b1 = half[rng.integers(len(half))]; t = rng.uniform(b0 + 1, b1 - 3)
            if far_from(t, cand_t) and far_from(t + 2, cand_t):
                k = int(t * FPS); neg.append(seq_feats(F.seq(k, k + 60)))
        while len(neg) < 100:
            neg.append(seq_feats(dark_static(F, pool[rng.integers(len(pool))], rng)))
        return pos, neg
    dp_t, dn_t = dark_sets(tun_pool, SEED_T); dp_h, dn_h = dark_sets(ho_pool, SEED_H)
    dr_t = []
    for t in TUNE["dark"]:
        k = int(round(t * FPS)); dr_t.append((seq_feats(F.seq(k - 15, k + 15)), 15))
    def ddet(ft, rc, dm, sm, rng_k):
        okf = lambda k: ft["mean"][k - 1] < 25 and ft["mean"][k] < 25 and ft["std"][k - 1] >= sm and ft["std"][k] >= sm
        return spikes(ft["Dd"], rng_k, rc, dm, okf)
    def dscore(pos, neg, real, rc, dm, sm):
        hit = [any(abs(k - 15) <= 2 for k in ddet(p, rc, dm, sm, range(10, 21))) for p in pos]
        hr = [any(abs(k - c) <= 2 for k in ddet(p, rc, dm, sm, range(c - 5, c + 6))) for p, c in real]
        fp = [bool(ddet(n, rc, dm, sm, range(1, len(n["Dd"])))) for n in neg]
        return hit, hr, fp
    best = None
    for rc in (3, 5, 8):
        for dm in (0.2, 0.3, 0.5):
            for sm in (0.8, 1.5):
                hit, hr, fp = dscore(dp_t, dn_t, dr_t, rc, dm, sm)
                rec = (sum(hit) + sum(hr)) / (len(hit) + len(hr)); fpr = np.mean(fp)
                key = (rec - fpr, rc, dm, sm)
                if fpr <= 0.05 and (best is None or key > best[0]):
                    best = (key, rc, dm, sm, rec, fpr, sum(hr))
    if best is None:
        thr["c"] = None; ctl["c"] = {"PASS": False, "note": "no grid point met tuning FP <= 5%"}
    else:
        _, rc, dmc, sm, rec, fpr, nhr = best; thr["c"] = {"rc": rc, "Dmin_c": dmc, "smin": sm}
        hit, _, fp = dscore(dp_h, dn_h, [], rc, dmc, sm)
        ctl["c"] = {"tuning": {"recall_incl_known": round(rec, 3), "known_near_black_hit": f"{nhr}/4", "dark_FP": round(fpr, 3)},
                    "held_out": {"dark_cut_recall": f"{sum(hit)}/60", "dark_negative_FP": f"{sum(fp)}/100"},
                    "PASS": bool(np.mean(hit) >= 0.80 and np.mean(fp) <= 0.05)}
    say("(c)", json.dumps(ctl["c"]), thr["c"])

    # ---- (d)
    def dsets(pool, seed):
        rng = np.random.default_rng(seed); pos, neg, ramp = [], [], []
        while len(pos) < 60:
            i, j = rng.choice(len(pool), 2, replace=False); L = int(rng.choice([1, 2, 3]))
            q = dis_seq(G, pool[i], pool[j], L, rng)
            if q is not None:
                pos.append((dis_scan(q[0]), q[1]))
        while len(neg) < 100:
            s = pool[rng.integers(len(pool))]; t = rng.uniform(s["start"] + 1, s["end"] - 4)
            if far_from(t, cand_t) and far_from(t + 3, cand_t):
                i0 = int(t * F5); neg.append(dis_scan([G.small(i0 + j) for j in range(16)]))
        while len(ramp) < 100:
            s = pool[rng.integers(len(pool))]; t = rng.uniform(s["start"] + 1, s["end"] - 4)
            if far_from(t, cand_t) and far_from(t + 3, cand_t):
                g = rng.uniform(0.4, 0.7) if rng.random() < 0.5 else rng.uniform(1.4, 2.5); i0 = int(t * F5)
                ramp.append(dis_scan([np.clip(G.small(i0 + j) * (1 + (g - 1) * j / 15), 0, 255) for j in range(16)]))
        return pos, neg, ramp
    dsp_t, dsn_t, dsr_t = dsets(tun_pool, SEED_T); dsp_h, dsn_h, dsr_h = dsets(ho_pool, SEED_H)
    def dscan_hit(sc, span, tr, ts, rho):
        return any(dis_ok(f, tr, ts, rho) and a < span[1] and span[0] < b for a, b, f in sc)
    def dany(sc, tr, ts, rho):
        return any(dis_ok(f, tr, ts, rho) for a, b, f in sc)
    best = None
    for tr in (0.25, 0.35, 0.5):
        for tsv in (0.5, 0.7):
            for rho in (-0.8, -0.9):
                rec = np.mean([dscan_hit(sc, sp, tr, tsv, rho) for sc, sp in dsp_t])
                fps_ = np.mean([dany(sc, tr, tsv, rho) for sc in dsn_t]); fpr_ = np.mean([dany(sc, tr, tsv, rho) for sc in dsr_t])
                if fps_ <= 0.05 and fpr_ <= 0.10:
                    key = (rec, -tr, -tsv, -rho)
                    if best is None or key > best[0]:
                        best = (key, tr, tsv, rho, rec, fps_, fpr_)
    real_d = {}
    if best is None:
        thr["d"] = None; ctl["d"] = {"PASS": False, "note": "no grid point met tuning static FP <= 5% and ramp FP <= 10%"}
    else:
        _, tr, tsv, rho, rec, fps_, fpr_ = best; thr["d"] = {"tau_r": tr, "tau_s": tsv, "rho": rho}
        rh = np.mean([dscan_hit(sc, sp, tr, tsv, rho) for sc, sp in dsp_h])
        sh = np.mean([dany(sc, tr, tsv, rho) for sc in dsn_h]); rmh = np.mean([dany(sc, tr, tsv, rho) for sc in dsr_h])
        for t in TUNE["dis_pos"]:
            i0 = int((t - 3) * F5); sc = dis_scan([G.small(i0 + j) for j in range(31)], t0=i0 / F5)
            real_d[f"pos_{t}"] = dscan_hit(sc, (t - 1, t + 1), tr, tsv, rho)
        for a0, b0 in TUNE["dis_neg"]:
            i0 = int((a0 - 1) * F5); n = int((b0 - a0 + 2) * F5) + 1
            sc = dis_scan([G.small(i0 + j) for j in range(n)], t0=i0 / F5)
            real_d[f"neg_{a0}-{b0}"] = dscan_hit(sc, (a0, b0), tr, tsv, rho)
        ctl["d"] = {"tuning": {"synthetic_recall": round(rec, 3), "static_FP": round(fps_, 3), "ramp_FP": round(fpr_, 3), "real_tuning_items_detected": real_d},
                    "held_out": {"synthetic_recall": round(rh, 3), "static_FP": round(sh, 3), "ramp_FP": round(rmh, 3)},
                    "PASS": bool(rh >= 0.80 and sh <= 0.05 and rmh <= 0.10)}
    say("(d)", json.dumps(ctl["d"]), thr["d"])
    json.dump(thr, open(out / "thresholds_v3.json", "w"), indent=1)
    json.dump(ctl, open(out / "controls_v3.json", "w"), indent=1)

    # ---- film scan
    say("film scan ...")
    Ds = np.zeros(F.n); Dd = np.zeros(F.n); mean = np.zeros(F.n); std = np.zeros(F.n)
    pe = pn = None
    for k in range(F.n):
        f = F.f(k); e = edge(f); nn = darknorm(f); mean[k] = f.mean(); std[k] = f.std()
        if k:
            Ds[k] = 1 - S(pe, e); Dd[k] = 1 - S(pn, nn)
        pe, pn = e, nn
    np.save(out / "feat_Ds.npy", Ds); np.save(out / "feat_Dd.npy", Dd); np.save(out / "feat_mean.npy", mean)
    def Eat(k):
        return {j: edge(F.f(j)) for j in range(k - 3, k + 3)}
    # (a) on v2 confirmed cuts
    light, kept = [], []
    for c in conf:
        q, kk = Ek(c["t"])
        if A_ok and q >= ta:
            light.append({"t": c["t"], "Q": round(q, 3), "sources": c["sources"], "tuning_item": any(abs(c["t"] - u) < 0.1 for u in TUNE["light"])})
        else:
            kept.append(c["t"])
    jumps, darks = [], []
    def qok(k):
        E = Eat(k); return (not A_ok) or Q_at(E, k) < ta
    if ctl["b"].get("PASS"):
        okf = lambda k: mean[k - 1] >= 25 and mean[k] >= 25 and qok(k)
        cand_k = [k for k in range(2, F.n - 1) if Ds[k] >= thr["b"]["Dmin"] and Ds[k] >= 2 * max(Ds[k - 1], Ds[k + 1])]
        for k in spikes(Ds, cand_k, thr["b"]["rb"], thr["b"]["Dmin"], okf):
            jumps.append(round(k / FPS, 4))
    if ctl["c"].get("PASS"):
        okf = lambda k: mean[k - 1] < 25 and mean[k] < 25 and std[k - 1] >= thr["c"]["smin"] and std[k] >= thr["c"]["smin"]
        cand_k = [k for k in range(2, F.n - 1) if Dd[k] >= thr["c"]["Dmin_c"] and Dd[k] >= 2 * max(Dd[k - 1], Dd[k + 1])]
        for k in spikes(Dd, cand_k, thr["c"]["rc"], thr["c"]["Dmin_c"], okf):
            darks.append(round(k / FPS, 4))
    tol = 3 / FPS
    bset = sorted(kept + [x for b in blacks for x in b])
    near = lambda t, L: any(abs(t - u) <= tol for u in L)
    new_j = [t for t in jumps if not near(t, bset)]
    new_d = [t for t in darks if not near(t, bset + new_j)]
    cuts3 = sorted(kept + new_j + new_d)
    # (d) on film
    dspans = []
    if True:
        if thr.get("d"):
            P = [G.small(i) for i in range(G.n)]
            sc = dis_scan(P, 0.0, cuts3)
            hits = sorted((a_, b_) for a_, b_, f in sc if dis_ok(f, thr["d"]["tau_r"], thr["d"]["tau_s"], thr["d"]["rho"]))
            for a_, b_ in hits:
                if any(b0 - 0.2 < a_ and b_ < b1 + 0.2 for b0, b1 in blacks):
                    continue
                if dspans and a_ <= dspans[-1]["end"]:
                    dspans[-1]["end"] = max(dspans[-1]["end"], round(b_, 3)); dspans[-1]["n_windows"] += 1
                else:
                    dspans.append({"start": round(a_, 3), "end": round(b_, 3), "n_windows": 1})
            for d in dspans:
                d["fade_like"] = bool(min(mean[int(d["start"] * FPS)], mean[min(F.n - 1, int(d["end"] * FPS))]) < 25)
    D_ok = ctl["d"].get("PASS", False)
    ds_for_segments = dspans if D_ok else []
    segs = build_segments(cuts3, blacks, ds_for_segments, v1, dur)
    segs = [dict(s, id=s["id"].replace("S2-", "S3-")) for s in segs]
    tun_all = TUNE["light"] + TUNE["jump"] + TUNE["dark"] + TUNE["other_cuts"]
    shots = [s for s in segs if s["kind"] == "SHOT"]; d3 = np.array([s["duration"] for s in shots])
    st = {"v2": {"confirmed_cut_events": len(conf), "SHOT": sum(s["kind"] == "SHOT" for s in v2segs), "BLACK": sum(s["kind"] == "BLACK" for s in v2segs),
                 "DISSOLVE_inconclusive": len(S2["dissolves"])},
          "v3": {"light_changes_removed": len(light), "light_changes_tuning_items": sum(x["tuning_item"] for x in light), "cuts_kept_from_v2": len(kept),
                 "jump_cuts_added": len(new_j), "near_black_cuts_added": len(new_d), "cut_events": len(cuts3),
                 "tuning_hits": {"jump": [t for t in TUNE["jump"] if near(t, new_j)], "dark": [t for t in TUNE["dark"] if near(t, new_d)],
                                 "other": [t for t in TUNE["other_cuts"] if near(t, cuts3)]},
                 "dissolve_spans": len(dspans), "dissolves_used_as_segments": bool(D_ok),
                 "SHOT": len(shots), "BLACK": sum(s["kind"] == "BLACK" for s in segs), "DISSOLVE": sum(s["kind"] == "DISSOLVE" for s in segs),
                 "shot_median_s": round(float(np.median(d3)), 3), "shot_mean_s": round(float(d3.mean()), 3), "longest_s": round(float(d3.max()), 3)},
          "detector_PASS": {k: ctl[k].get("PASS", False) for k in "abcd"}, "elapsed_s": round(time.time() - t_start, 1)}
    json.dump(light, open(out / "light_changes_v3.json", "w"), indent=1)
    json.dump({"all_detections": jumps, "added": new_j}, open(out / "jump_cuts_v3.json", "w"), indent=1)
    json.dump({"all_detections": darks, "added": new_d}, open(out / "near_black_cuts_v3.json", "w"), indent=1)
    json.dump({"PASS": D_ok, "status": "USED" if D_ok else "INCONCLUSIVE (exclusion only)", "spans": dspans}, open(out / "dissolves_v3.json", "w"), indent=1)
    json.dump({"schema": "s1-seg-v3.v1", "segments": segs, "cuts": cuts3, "light_changes": [x["t"] for x in light],
               "dissolves": dspans, "dissolves_status": "USED" if D_ok else "INCONCLUSIVE"}, open(out / "segments_v3.json", "w"))
    json.dump(st, open(out / "seg_v3_stats.json", "w"), indent=1)
    say(json.dumps(st, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    run(ap.parse_args())


if __name__ == "__main__":
    main()
