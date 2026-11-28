"""Film-baseline reverse measurements for one admitted source (handoff §4 / §10 step 2).

Studio-specific adapter under the HF-Q01 scoped exception: ffmpeg is invoked only as an
independent external tool (outputs are text logs / raw frames produced beforehand by the
runner); this module itself only parses those outputs with the Python stdlib + numpy and
writes JSON. It does not download, generate, upload or publish anything.

Every number written here is MEASURED with a file + locator. Nothing here infers lens,
focal length, prompts, seeds, camera paths or model parameters.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

PARAMS = {
    "cut_threshold": 0.30,
    "cut_merge_s": 0.5,
    "min_segment_s": 0.25,
    "black": {"d": 0.2, "pix_th": 0.10},
    "gradual": {"hist_bins": 16, "lag_s": 2.0, "l1_threshold": 0.5},
    "frames": {"fps": 2, "w": 160, "h": 90},
    "edge_grad_threshold": 24,
    "audio": {"sr": 16000, "silence_dbfs": -45.0, "section_min_s": 3},
    "prereg": "docs/handoff/agentic-film-production/runs/2026-11-27-h02-s1/ORACLE_PREREG_S1_H02.md",
}


def parse_scene_scores(path: Path):
    t, s = [], []
    cur = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("frame:"):
                cur = float(line.split("pts_time:")[1])
            elif line.startswith("lavfi.scene_score="):
                t.append(cur)
                s.append(float(line.split("=", 1)[1]))
    return np.array(t), np.array(s)


def parse_black(log: Path):
    out = []
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", log.read_text(errors="replace")):
        out.append((float(m.group(1)), float(m.group(2))))
    return out


def parse_silence(log: Path):
    txt = log.read_text(errors="replace")
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", txt)]
    ends = [(float(a), float(b)) for a, b in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", txt)]
    out = []
    for i, st in enumerate(starts):
        en = ends[i][0] if i < len(ends) else None
        out.append({"start": max(0.0, st), "end": en})
    return out


def parse_ebur128_m(path: Path):
    t, v = [], []
    cur = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("frame:"):
                cur = float(line.split("pts_time:")[1])
            elif line.startswith("lavfi.r128.M="):
                t.append(cur)
                v.append(float(line.split("=", 1)[1]))
    return np.array(t), np.array(v)


def parse_srt(path: Path):
    cues = []
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 2:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1])
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        st = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        en = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append({"index": int(lines[0]), "start": st, "end": en, "text": "\n".join(lines[2:])})
    return cues


def tc(sec: float, fps: float = 30000 / 1001) -> str:
    """Wall-clock timecode HH:MM:SS.mmm plus frame index at the source rate."""
    ms = int(round(sec * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def detect_cuts(t, s, blacks, p=PARAMS):
    idx = np.where(s >= p["cut_threshold"])[0]
    cuts = []
    for i in idx:
        ti, si = float(t[i]), float(s[i])
        if cuts and ti - cuts[-1][0] < p["cut_merge_s"]:
            if si > cuts[-1][1]:
                cuts[-1] = (ti, si)
            continue
        cuts.append((ti, si))
    # cuts inside / at the edge of a black segment are fade artefacts, not hard cuts
    kept, dropped = [], []
    for ti, si in cuts:
        if any(bs - 0.5 <= ti <= be + 0.5 for bs, be in blacks):
            dropped.append({"t": ti, "score": si, "reason": "within 0.5 s of a black segment"})
        else:
            kept.append({"t": ti, "score": si})
    return kept, dropped


def build_segments(cuts, blacks, duration, p=PARAMS):
    marks = [(0.0, "start")] + [(c["t"], "cut") for c in cuts]
    for bs, be in blacks:
        marks += [(bs, "black_start"), (be, "black_end")]
    marks.append((duration, "end"))
    marks.sort(key=lambda x: x[0])
    kept = []
    for tm, kind in marks:
        tm = min(max(tm, 0.0), duration)
        if kept and tm - kept[-1][0] < p["min_segment_s"]:
            # prefer black edges / end over cuts when collapsing
            if kind in ("black_start", "black_end", "end") and kept[-1][1] not in ("start",):
                kept[-1] = (tm if kind == "end" else kept[-1][0], kind if kind == "end" else kept[-1][1])
            continue
        kept.append((tm, kind))
    if kept[-1][0] < duration:
        kept.append((duration, "end"))
    segs = []
    for (a, ka), (b, kb) in zip(kept, kept[1:]):
        mid = (a + b) / 2
        is_black = any(bs <= mid <= be for bs, be in blacks)
        segs.append({"start": round(a, 3), "end": round(b, 3), "kind": "BLACK" if is_black else "SHOT",
                     "in_boundary": ka, "out_boundary": kb})
    shot_n = black_n = 0
    for sg in segs:
        if sg["kind"] == "SHOT":
            shot_n += 1
            sg["id"] = f"S1-SH{shot_n:03d}"
        else:
            black_n += 1
            sg["id"] = f"S1-BK{black_n:02d}"
        sg["duration"] = round(sg["end"] - sg["start"], 3)
        sg["tc_in"], sg["tc_out"] = tc(sg["start"]), tc(sg["end"])
        sg["frame_in"] = int(round(sg["start"] * 30000 / 1001))
        sg["frame_out_excl"] = int(round(sg["end"] * 30000 / 1001))
    return segs


@dataclass
class Frames:
    arr: np.ndarray  # (N, H, W, 3) uint8
    fps: float

    def times(self):
        return np.arange(len(self.arr)) / self.fps


def load_frames(path: Path, p=PARAMS) -> Frames:
    f = p["frames"]
    raw = np.memmap(path, dtype=np.uint8, mode="r")
    n = raw.size // (f["w"] * f["h"] * 3)
    return Frames(np.asarray(raw[: n * f["w"] * f["h"] * 3]).reshape(n, f["h"], f["w"], 3), f["fps"])


def frame_metrics(fr: Frames, p=PARAMS):
    a = fr.arr.astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mx, mn = a.max(-1), a.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    rg, yb = r - g, 0.5 * (r + g) - b
    colorful = np.sqrt(rg.std((1, 2)) ** 2 + yb.std((1, 2)) ** 2) + 0.3 * np.sqrt(rg.mean((1, 2)) ** 2 + yb.mean((1, 2)) ** 2)
    gx = np.abs(np.diff(luma, axis=2))[:, :-1, :]
    gy = np.abs(np.diff(luma, axis=1))[:, :, :-1]
    edge = ((gx + gy) > p["edge_grad_threshold"]).mean((1, 2))
    h, w = luma.shape[1:]
    ys, xs = np.mgrid[0:h, 0:w]
    tot = luma.sum((1, 2)) + 1e-6
    cx = (luma * xs).sum((1, 2)) / tot / (w - 1)
    cy = (luma * ys).sum((1, 2)) / tot / (h - 1)
    motion = np.concatenate([[np.nan], np.abs(np.diff(luma, axis=0)).mean((1, 2))])
    return {"luma": luma.mean((1, 2)), "luma_std": luma.std((1, 2)), "sat": sat.mean((1, 2)),
            "colorfulness": colorful, "edge": edge, "cx": cx, "cy": cy, "motion": motion}


def hue_hist(frames: np.ndarray, bins=12):
    a = frames.reshape(-1, 3).astype(np.float32) / 255
    mx, mn = a.max(1), a.min(1)
    d = mx - mn
    ok = (d > 0.08) & (mx > 0.15)
    if not ok.any():
        return [0.0] * bins
    r, g, b = a[ok].T
    d = d[ok]
    mxk = mx[ok]
    hh = np.where(mxk == r, ((g - b) / d) % 6, np.where(mxk == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    hist, _ = np.histogram(hh, bins=bins, range=(0, 1))
    return (hist / max(1, len(a))).round(4).tolist()


def gradual_candidates(fr: Frames, segs, p=PARAMS):
    gp = p["gradual"]
    bins = gp["hist_bins"]
    q = (fr.arr // (256 // bins)).astype(np.int32)
    code = q[..., 0] * bins * bins + q[..., 1] * bins + q[..., 2]
    n = len(code)
    hists = np.stack([np.bincount(c.ravel(), minlength=bins ** 3) for c in code]).astype(np.float32)
    hists /= hists.sum(1, keepdims=True)
    lag = int(gp["lag_s"] * fr.fps)
    bounds = [(s["start"], s["end"]) for s in segs]
    hard = sorted({s["start"] for s in segs} | {s["end"] for s in segs})
    blacks = [(s["start"], s["end"]) for s in segs if s["kind"] == "BLACK"]
    cands = []
    for i in range(n - lag):
        t0, t1 = i / fr.fps, (i + lag) / fr.fps
        if any(t0 <= hb <= t1 for hb in hard) or any(not (be < t0 or bs > t1) for bs, be in blacks):
            continue
        d = float(np.abs(hists[i] - hists[i + lag]).sum())
        if d >= gp["l1_threshold"]:
            if cands and t0 - cands[-1]["t_end"] <= 0.5:
                cands[-1]["t_end"] = t1
                cands[-1]["max_l1"] = max(cands[-1]["max_l1"], round(d, 3))
            else:
                cands.append({"t_start": t0, "t_end": t1, "max_l1": round(d, 3)})
    for c in cands:
        mid = (c["t_start"] + c["t_end"]) / 2
        c["segment"] = next((s["id"] for s in segs if s["start"] <= mid < s["end"]), None)
        c["class"] = "INFERRED"
        c["label"] = "CANDIDATE_GRADUAL (dissolve / camera move / lighting change / object motion — undetermined)"
    return cands


def audio_measures(s16_path: Path, duration: float, cues, silences, p=PARAMS):
    sr = p["audio"]["sr"]
    x = np.fromfile(s16_path, dtype="<i2").astype(np.float32) / 32768.0
    n_sec = int(math.ceil(len(x) / sr))
    rms_db, centroid, flat = [], [], []
    freqs = np.fft.rfftfreq(sr, 1 / sr)
    win = np.hanning(sr)
    for i in range(n_sec):
        seg = x[i * sr:(i + 1) * sr]
        if len(seg) < sr:
            seg = np.pad(seg, (0, sr - len(seg)))
        r = float(np.sqrt(np.mean(seg ** 2)) + 1e-12)
        rms_db.append(round(20 * math.log10(r), 2))
        mag = np.abs(np.fft.rfft(seg * win)) + 1e-12
        centroid.append(round(float((freqs * mag).sum() / mag.sum()), 1))
        flat.append(round(float(np.exp(np.mean(np.log(mag))) / np.mean(mag)), 4))
    speech = np.zeros(n_sec, bool)
    for c in cues:
        speech[int(c["start"]):min(n_sec, int(math.ceil(c["end"])))] = True
    rms = np.array(rms_db)
    label = np.where(speech, "SPEECH", np.where(rms < p["audio"]["silence_dbfs"], "SILENCE", "NONSPEECH_SOUND"))
    # run-length sections, absorbing runs shorter than section_min_s into the previous section
    sections = []
    for i, lab in enumerate(label):
        if sections and sections[-1]["label"] == lab:
            sections[-1]["end"] = i + 1
        else:
            sections.append({"label": str(lab), "start": i, "end": i + 1})
    merged = []
    for s in sections:
        if merged and (s["end"] - s["start"]) < p["audio"]["section_min_s"]:
            merged[-1]["end"] = s["end"]
            merged[-1].setdefault("absorbed", []).append(f'{s["label"]}@{s["start"]}-{s["end"]}')
        elif merged and merged[-1]["label"] == s["label"]:
            merged[-1]["end"] = s["end"]
        else:
            merged.append(dict(s))
    for s in merged:
        sl = slice(s["start"], s["end"])
        s.update({"duration": s["end"] - s["start"], "rms_db_mean": round(float(rms[sl].mean()), 2),
                  "centroid_hz_mean": round(float(np.mean(centroid[sl])), 1),
                  "flatness_mean": round(float(np.mean(flat[sl])), 4)})
    return {"per_second": {"rms_dbfs": rms_db, "spectral_centroid_hz": centroid, "spectral_flatness": flat,
                           "speech_mask": speech.astype(int).tolist()},
            "sections": merged, "silences_ffmpeg": silences,
            "speech_seconds": int(speech.sum()), "n_seconds": n_sec}


def _overlap(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def attach(segs, fm, fr: Frames, audio, lt, lv, cues):
    ft = fr.times()
    rms = np.array(audio["per_second"]["rms_dbfs"])
    for sg in segs:
        sel = np.where((ft >= sg["start"] + 0.1) & (ft < sg["end"] - 0.1))[0]
        if len(sel) == 0:
            sel = np.array([min(len(ft) - 1, int(round((sg["start"] + sg["end"]) / 2 * fr.fps)))])
        msel = sel[1:] if len(sel) > 1 else sel  # motion uses within-segment diffs only
        mv = fm["motion"][msel]
        mv = mv[~np.isnan(mv)]
        sg["visual"] = {
            "n_samples_2fps": int(len(sel)),
            "luma_mean": round(float(fm["luma"][sel].mean()), 2),
            "luma_std_mean": round(float(fm["luma_std"][sel].mean()), 2),
            "saturation_mean": round(float(fm["sat"][sel].mean()), 4),
            "colorfulness_mean": round(float(fm["colorfulness"][sel].mean()), 2),
            "edge_density_mean": round(float(fm["edge"][sel].mean()), 4),
            "luma_centroid_xy": [round(float(fm["cx"][sel].mean()), 3), round(float(fm["cy"][sel].mean()), 3)],
            "motion_mad_mean": round(float(mv.mean()), 3) if len(mv) else None,
            "motion_mad_max": round(float(mv.max()), 3) if len(mv) else None,
            "hue_hist12": hue_hist(fr.arr[sel]),
            "locator": f"work/frames_2fps_160x90.rgb frames {int(sel[0])}..{int(sel[-1])}",
        }
        s0, s1 = int(sg["start"]), max(int(sg["start"]) + 1, int(math.ceil(sg["end"])))
        lm = lv[(lt >= sg["start"]) & (lt < sg["end"])]
        lm = lm[lm > -70]
        ov = [c for c in cues if _overlap(sg["start"], sg["end"], c["start"], c["end"]) > 0]
        sp = sum(_overlap(sg["start"], sg["end"], c["start"], c["end"]) for c in ov)
        sg["audio"] = {
            "rms_dbfs_mean": round(float(rms[s0:s1].mean()), 2),
            "loudness_M_lufs_median": round(float(np.median(lm)), 2) if len(lm) else None,
            "speech_fraction": round(min(1.0, sp / max(sg["duration"], 1e-6)), 3),
            "cue_indices": [c["index"] for c in ov],
            "locator": f"audio/audio_structure.json per_second[{s0}:{s1}]; work/ebur128_M.txt",
        }
    return segs


def rhythm_and_sync(segs, cues, audio, duration, rng_seed=20261127):
    shots = [s for s in segs if s["kind"] == "SHOT"]
    d = np.array([s["duration"] for s in shots])
    cut_times = np.array([s["start"] for s in segs if s["in_boundary"] == "cut"])
    per_min = np.histogram(cut_times, bins=np.arange(0, duration + 60, 60))[0].tolist()
    ev = sorted([c["start"] for c in cues] + [c["end"] for c in cues])
    ev = np.array(ev)

    def near_frac(ts, tol=0.5):
        if len(ts) == 0 or len(ev) == 0:
            return None
        return float(np.mean([np.min(np.abs(ev - t)) <= tol for t in ts]))

    rng = np.random.default_rng(rng_seed)
    null = [near_frac(rng.uniform(0, duration, len(cut_times))) for _ in range(200)]
    rms = np.array(audio["per_second"]["rms_dbfs"])
    jumps = []
    for t in cut_times:
        i = int(t)
        if 2 <= i < len(rms) - 2:
            jumps.append(float(abs(rms[i:i + 2].mean() - rms[i - 2:i].mean())))
    rjumps = []
    for t in rng.uniform(2, duration - 2, 500):
        i = int(t)
        rjumps.append(float(abs(rms[i:i + 2].mean() - rms[i - 2:i].mean())))
    return {
        "n_shots": len(shots), "n_black_segments": sum(1 for s in segs if s["kind"] == "BLACK"),
        "n_hard_cuts": int(len(cut_times)),
        "shot_duration_s": {"mean_ASL": round(float(d.mean()), 2), "median": round(float(np.median(d)), 2),
                             "p10": round(float(np.percentile(d, 10)), 2), "p90": round(float(np.percentile(d, 90)), 2),
                             "min": round(float(d.min()), 2), "max": round(float(d.max()), 2)},
        "cuts_per_minute": per_min,
        "av_sync": {
            "cuts_within_0.5s_of_speech_cue_edge": near_frac(cut_times),
            "null_random_cut_times_mean": round(float(np.mean(null)), 3),
            "null_random_cut_times_p95": round(float(np.percentile(null, 95)), 3),
            "rms_jump_db_at_cuts_median": round(float(np.median(jumps)), 2) if jumps else None,
            "rms_jump_db_random_median": round(float(np.median(rjumps)), 2),
            "note": "null = 200 draws of uniformly random cut times (seed 20261127); jump = |mean dBFS 2 s after − 2 s before|",
        },
    }
