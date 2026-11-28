# S1 Segmentation v3 — pre-registration (2026-11-27)

Committed **before** any v3 detector is run, tuned or validated. Nothing in v1/v2 is changed; v3 writes a new pack version `pack-v3/` (box, private).
Producer: Grok Bot. Addresses F-27 (near-black cuts), F-29 (light changes accepted as cuts), F-30 (low-contrast jump cuts), F-31 (dissolve detector).
Code: `studio/reverse/seg_v3.py` (committed with this file or before the run).

## 0. Data
- `F_k`: every decoded frame at native rate (30000/1001 fps, 69,931 frames), luma, area-scaled to 128x72 (`pack-v3/work/frames_full_128x72.gray`). Boundary k = first frame of the new picture; t = k·1001/30000.
- `P_i`: the existing 5 fps 320x180 luma file, downscaled to 80x45 (dissolves only).
- `z(F)` = (F − mean)/max(std, 1). `E(F)` = z-scored Sobel gradient magnitude of F blurred with a Gaussian σ = 1 px. `S(a,b)` = ZNCC of E(a), E(b) (gain- and offset-invariant structure similarity).
- v2 inputs reused unchanged: merged candidates + O3 confirmations (`pack-v2/seg/cut_candidates_v2.json`), BLACK intervals (v1), v2 SHOT segments.

## 1. Tuning data (declared) and exclusion from round 4
Every time below comes from round-2/3 reviewer findings or the round-3 post-hoc check. They are **tuning data**: they may be used to choose thresholds, never as held-out evidence, and every round-4 sample (A1–A4) must exclude ±2.0 s around each, plus the listed intervals:
- Light changes (F-29): 802.2348, 2184.516, 2184.783, 2185.2497.
- Jump cuts (F-30): 83.35, 1723.755, 1899.164, 1694.76.
- Near-black cuts (F-27): 2182.647, 2157.99, 2170.97, 437.837.
- Other round-2/3 reviewer cut times: 858.39, 864.46, 876.74, 2089.39, 285.752, 136.2.
- Dissolves (F-31): positives 1412.45, 1759.12, 2247.3; negatives 130.9–135.6 (still photo + hard cut), 1441.1–1442.7 (focus/exposure change).
Round-4 samples also never overlap any round-1/2/3 window, span, camera span or A1 timestamp (±0.5 s for timestamps).

## 2. Synthetic sets and splits (seeds published; synthetic data needs no secrecy)
- Segment pool: v2 SHOT segments ≥ 6 s, sorted by start; **tuning pool = even positions, held-out pool = odd positions** (disjoint footage). Tuning seed T = 3001, held-out seed H = 3002. Sizes: 60 positives and 100 negatives per set unless stated.
- v1 hard cuts (83, all O3-confirmed): odd positions = tuning, even positions = held-out.
- Synthetic constructions:
  - *Exposure step* (light change): 4 consecutive real frames k−2..k+1 from a pool segment interior; frames k, k+1 get gain g ∈ U(0.4,0.7) ∪ U(1.4,2.5), gamma γ ∈ U(0.7,1.4), offset ∈ U(−10,10); clipped to 0–255.
  - *Exposure ramp* (dissolve negative): 3 s of real 5 fps frames from one segment with gain ramping linearly from 1 to g as above.
  - *Jump cut*: 1 s of real frames ending at position p, then real frames from p + Δ (Δ ∈ U(2,6) s) of the same segment; with probability 0.5 the second part is centre-cropped by 5–12 % and rescaled (punch-in). Segment must be ≥ 10 s.
  - *Static negative*: a 2 s window of real frames inside a pool segment, ≥ 1 s from any v2 candidate (confirmed or not).
  - *Dark cut*: 0.5 s from segment A then 0.5 s from segment B (different segments), both multiplied by gain ∈ U(0.04,0.12), Gaussian noise σ ∈ U(0.5,1.0) added per frame, quantised to uint8. Population rule: after scaling both sources have spatial std ≥ 0.8.
  - *Dark negative*: a 2 s window inside a v1 BLACK interval, ≥ 1 s from its edges and from any candidate; and 1 s of segment A scaled dark with fresh noise per frame.
  - *Synthetic dissolve*: real frames of segment A then segment B (5 fps), cross-dissolved linearly over L ∈ {1, 2, 3} s with real moving frames on both sides. **Population rule (fixed now):** A and B from different segments, both end frames with spatial std ≥ 3 (8-bit). The detector may not reject population members by extra gates without counting them as misses.

## 3. Detectors, threshold grids and selection rules
Thresholds are chosen **only on the tuning set** by the stated rule, frozen in `pack-v3/seg/thresholds_v3.json`, then the held-out set is run once. The held-out criteria are binding. A detector that fails held-out is not used; its output is reported as INCONCLUSIVE and the v2 behaviour is kept for that aspect.

Cross/within structure around boundary k: `S_x` = median of S(k−1,k), S(k−2,k+1), S(k−1,k+1), S(k−2,k); `S_w` = median of S(k−2,k−1), S(k,k+1); `Q = S_x / max(S_w, 0.05)`.

**(a) Light change vs cut.** A v2-confirmed cut is reclassified LIGHT_CHANGE when Q ≥ τa. Grid τa ∈ {0.5, 0.6, 0.7, 0.8, 0.9}. Selection: maximise balanced accuracy on tuning (positives = tuning v1 cuts as CUT; light = 4 known light changes + tuning exposure steps); ties → larger τa.
Held-out PASS: held-out v1 cuts kept as CUT ≥ 95 % **and** held-out exposure steps classified LIGHT ≥ 90 %.

**(b) Jump cuts.** `D_k = 1 − S(k−1,k)`; local base `m_k` = median of D over k−15..k+15 excluding k−1..k+1. Detect at k when D_k ≥ rb·max(m_k, 0.01), D_k ≥ Dmin, D_k ≥ 2·max(D_{k−1}, D_{k+1}), frame mean luma ≥ 25 on both sides, and (a) does not call it LIGHT_CHANGE (if (a) passed). Grid rb ∈ {4, 6, 8, 12}, Dmin ∈ {0.05, 0.1, 0.2}. Selection: maximise recall − FP-rate on tuning (positives = 4 known jump cuts + tuning synthetic jump cuts; negatives = tuning static windows, FP = any detection in the window) subject to tuning FP ≤ 5 %; ties → larger rb, then larger Dmin.
Held-out PASS: synthetic jump-cut recall ≥ 80 % **and** static-negative FP ≤ 5 %.

**(c) Near-black cuts.** Scope: boundaries where both sides have mean luma < 25. Frames are robust-normalised (median, MAD·1.4826 floored at 0.6), blurred σ = 1.5, and `C_k` = ZNCC(k−1,k); `D_k = 1 − C_k`; local base as in (b). Detect when both frames have std ≥ smin, D_k ≥ rc·max(m_k, 0.01), D_k ≥ Dmin_c, D_k ≥ 2·max(D_{k−1}, D_{k+1}). Grid rc ∈ {3, 5, 8}, Dmin_c ∈ {0.2, 0.3, 0.5}, smin ∈ {0.8, 1.5}. Selection as (b) (positives = 4 known near-black cuts + tuning dark cuts; negatives = tuning dark negatives).
Held-out PASS: dark-cut recall ≥ 80 % **and** dark-negative FP ≤ 5 %.

**(d) Dissolves (revised).** On P (5 fps, 80x45), windows of L ∈ {1, 2, 3, 4} s at 0.4 s stride; A = first frame, B = last frame. Per-frame α_i = ⟨P_i − B, A − B⟩/‖A − B‖²; residual r = median_i RMS(P_i − (α_i A + (1−α_i) B)) / RMS(A − B). Detect when RMS(A − B) ≥ 4, S(A,B) < τs (structure differs, gain-invariant), Spearman(α, i) ≤ ρ, α of the first 20 % ≥ 0.7, α of the last 20 % ≤ 0.3, ≥ 2 frames with α ∈ (0.15, 0.85), r ≤ τr, and no v3 hard cut strictly inside. Overlapping detections merge into one span. No luma gate. Grid τr ∈ {0.25, 0.35, 0.5}, τs ∈ {0.5, 0.7}, ρ ∈ {−0.8, −0.9}. Selection: maximise tuning recall subject to tuning static FP ≤ 5 % and tuning ramp FP ≤ 10 %; ties → smaller τr, smaller τs, ρ = −0.9. Real tuning items (3 positives, 2 negatives) are reported.
Held-out PASS (binding, owner-specified): synthetic-dissolve recall ≥ 80 % **and** static FP ≤ 5 %; also exposure-ramp FP ≤ 10 %. Otherwise DISSOLVE stays INCONCLUSIVE (used only to exclude camera spans).

## 4. Assembly (v3 segments)
1. Start from v2 confirmed cuts. If (a) PASS, cuts with Q ≥ τa become LIGHT_CHANGE events (removed from boundaries, listed).
2. If (b) PASS, add jump cuts ≥ 3 frames from existing boundaries. If (c) PASS, add near-black cuts likewise (they may split BLACK intervals; pieces keep kind BLACK).
3. If (d) PASS, dissolve spans become DISSOLVE segments; else INCONCLUSIVE, exclusion only.
4. Segments via the v2 `build_segments` rule (2-frame boundary merge, BLACK edge preferred). Stats vs v2 reported. Tuning-data hits are reported separately and never counted as validation.

## 5. Outputs
`pack-v3/seg/`: thresholds_v3.json, controls_v3.json (tuning and held-out results per detector), light_changes_v3.json, jump_cuts_v3.json, near_black_cuts_v3.json, dissolves_v3.json, segments_v3.json, seg_v3_stats.json, run.log. Git gets timestamp-only JSON and a result note; no frames.
