# S1 Segmentation v2 — result (2026-11-27)

Pre-registration: `PREREG_SEG_V2_2026-11-27.md` (commit 1959fa9). Code: `studio/reverse/seg_v2.py`. Private outputs: box `afp-private/sources/onNBysMf9WM/pack-v2/seg/` (git copies of the timestamp-only JSON in this folder; no frames or media).
Producer: Grok Bot. Class: producer measurement, **not** ground truth.

## Stats vs v1

| Measure | v1 | v2 |
|---|---|---|
| Hard-cut picture boundaries (not at a BLACK edge) | 83 | 151 (83 v1 re-confirmed + 68 new) |
| Confirmed cut events incl. those at BLACK edges | — | 211 (128 not in v1; 60 coincide with BLACK edges within 2 frames) |
| Candidates (raw events → merged ±3 frames) | — | 801 → 305; 28 dropped inside black; 94 unconfirmed |
| New-cut sources (multi-source) | — | PySceneDetect content 97, adaptive 110, ffmpeg scene ≥ 0.10 104 |
| SHOT segments | 199 | 285 |
| BLACK segments | 120 | 120 |
| DISSOLVE segments | — | 20 (43.2 s) — INCONCLUSIVE |
| SHOT median / mean | 4.972 s / 10.424 s | 3.203 s / 7.127 s |
| Longest SHOT | 137.538 s (S1-SH145) | 80.914 s (S2-SH180 ⊂ S1-SH132) |

## Controls
- S2 decode confirmation: v1 re-confirmed 83/83 (≥ 0.95), negative control 0/211 (≤ 0.10) → **PASS**.
- S3 dissolve detector: synthetic blends 22/50 (28 rejected by the end-frame gates), static negatives 0/80 → **FAIL**. Per pre-registration the DISSOLVE spans are **INCONCLUSIVE**; they are used only to exclude camera spans and to define the SEG2_DISSOLVE stratum, never as positive claims. Thresholds were not retuned.
- Informational only (round-2 reviewer observations are not truth): the reviewer's dissolves at 1412.45 s and 1759.12 s were not detected; 5 of 6 round-2 unmatched reviewer cuts were already decode-confirmed post hoc.

## Implementation fixes (not methodology changes)
1. Spearman ranks with ties: average ranks instead of argsort (before any result was read).
2. S4 first pass produced zero-length slivers/gaps where a confirmed cut coincided with a BLACK edge (4-decimal rounding). Boundaries within 2 frames are now one boundary (BLACK edge preferred); `v1_overlap` requires > 2 frames of overlap. First-pass file kept privately as `segments_v2.firstpass_sliver_bug.json`. Counts above are from the fixed pass (first pass: 301 SHOT / 121 BLACK).

## Consequences
- Claims v5 (`claims-evidence.v5.jsonl`): S1-SEG2-MEA-001..004 (new), S1-INF-003@v3, S1-INF-001@v2 (interview ≤ 396.6 s, MS framing), S1-EXT-INF-E2@v2 (no supported push/pull), S1-INF-004@v2 (narrowed).
- V2 round 3 uses seg v2 as the pre-registered reference (RUBRIC_V2R3.md); R7 is INCONCLUSIVE by rule because the dissolve controls failed.
