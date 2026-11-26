# S1 segmentation v2 — pre-registration (committed BEFORE the method is coded or run)

New pack version: outputs go to private `pack-v2/seg/` and git-safe copies to `runs/2026-11-27-seg-v2/`. v1 (`pack/`) and ext (`pack-ext/`) are never modified.
Motivation: V2 round 2 F-23 (v1 hard-cut list misses sub-threshold cuts), F-16/F-25 (dissolves inside segments). Round-2 reviewer answers are **not** used as truth anywhere below; the two reviewer-observed dissolve times (1412.45 s, 1759.12 s) are reported informationally only.

Inputs: admitted MKV (sha256 `7309020b…ef45c`); existing full-rate ffmpeg scene scores (`work/scene_scores.txt`, 320x180, 69,931 frames); PySceneDetect 0.7.3 content/adaptive cut lists (`pack-ext/scenedetect_cuts.json` raw, owner licence exception for tqdm/soxr, local only); v1 blackdetect intervals; 5 fps 320x180 gray frames (`work/frames_5fps_320x180.gray`).

## S1 Cut candidates
Union of: v1 hard cuts; PySceneDetect content cuts; PySceneDetect adaptive cuts; every frame with ffmpeg scene score >= **0.10**.
Candidates within 3 frames (0.1001 s) of each other are merged into one, placed at the member with the highest ffmpeg scene score (ties: earliest).
Candidates strictly inside a v1 BLACK interval (more than 2 frames from both edges) are dropped (cuts in black are not visible).

## S2 Decode confirmation (O3 rule, unchanged)
For each candidate t: ffmpeg input-seek decode of [t−0.25, t+0.25] s at native rate, 64x36 gray; `d_cut` = max adjacent mean-abs diff within ±2 frames of t;
`d_base` = median of the rest. **Confirmed hard cut** iff `d_cut >= 8.0` and `d_cut >= 3*max(d_base,0.5)`. Others are kept as `UNCONFIRMED_CANDIDATE` (logged, not boundaries).
Controls: (a) v1 hard cuts re-confirmed fraction >= 0.95; (b) negative control: N = number of confirmed cuts (cap 300) random times >= 2 s from every candidate and black edge (seed 20261128): false-confirm <= 0.10.
If (a) or (b) fails, segmentation v2 is reported FAIL and not used downstream.

## S3 Dissolve detection
Frames: 5 fps gray, downscaled to 80x45, float. Window lengths L = 2 s (11 frames) and 4 s (21 frames), centres every 0.5 s.
A window is skipped if it overlaps (±0.2 s) a confirmed cut or a v1 BLACK interval, or if mean luma of either end frame < 20.
End frames A (first) and B (last) must differ: mean|A−B| >= 10 and Canny edge-map correlation(A,B) < 0.5.
For each interior frame f_i: α_i = clip(argmin‖f_i − (αA + (1−α)B)‖², 0, 1), r_i = ‖f_i − fit‖ / ‖A − B‖.
**Dissolve** iff: Spearman(i, α_i) <= −0.9; at least 3 interior frames with 0.15 < α_i < 0.85; median r_i over those frames <= 0.35; α of the first interior frame >= 0.7 and of the last <= 0.3.
Overlapping/adjacent detections (any L) merge into one span [first mid frame, last mid frame] (min 0.4 s); a span containing a confirmed cut is dropped.
Controls: synthetic positives = 50 linear blends between frames of two different v1 SHOT segments over 1.0 s (25) and 2.0 s (25), seed 20261128 → detection >= 0.80;
negatives = 80 random windows inside v1 SHOT segments >= 6 s labelled STATIC by E2 (seed 20261128) → false positive <= 0.10.
If either control fails, dissolve spans are reported INCONCLUSIVE (still used conservatively to exclude camera spans, never as positive claims).

## S4 Segments v2
Boundaries = confirmed cuts ∪ v1 BLACK edges ∪ dissolve span edges. Kinds: SHOT, BLACK (v1 blackdetect, unchanged), DISSOLVE.
Ids `S2-SHxxx`, `S2-BKxx`, `S2-DSxx`; a mapping to v1 ids by overlap is written. Stats vs v1: counts, cuts new / dropped, durations.

## S5 Verified camera spans (for V2 round 3)
Candidates: S2 SHOT segments >= 3.5 s, trimmed 0.5 s each end. A span is **verified cut- and dissolve-free** iff:
(1) no confirmed cut, UNCONFIRMED_CANDIDATE, dissolve span or black inside; (2) native-rate 64x36 gray decode of the whole span has no adjacent pair with
d >= 8 and d >= 3×(span median, min 0.5); (3) no S3 window inside it is a dissolve. Spans failing (2) are rejected and logged.
Author label = the E2 `camera_motion` algorithm (unchanged code) applied to the span itself; UNDETERMINED_LOW_TEXTURE spans are not sampled.

## Not claimed
Recall of cuts and dissolves remains unmeasured against ground truth; v2 is a denser producer segmentation, not truth.
