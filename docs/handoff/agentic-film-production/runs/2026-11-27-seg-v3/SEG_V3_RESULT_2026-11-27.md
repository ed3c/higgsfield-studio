# S1 Segmentation v3 — result (2026-11-27)

Pre-registration `PREREG_SEG_V3_2026-11-27.md` (commit bf87fac); code `studio/reverse/seg_v3.py` (commit b272f33, committed before the run). One run, 46 s; no rerun or retuning.
Private outputs: box `afp-private/sources/onNBysMf9WM/pack-v3/` (frames/features private). Git copies here are timestamp-only JSON. Producer: Grok Bot; not ground truth.

## Detector controls (thresholds chosen on tuning data only, then one held-out run)
| Detector | Frozen thresholds | Tuning | Held-out (binding) | Status |
|---|---|---|---|---|
| (a) light change vs cut | τa = 0.6 | v1 cuts kept 41/41; known light changes 2/4; exposure steps 60/60 | v1 cuts kept 42/42 (≥ 95 %); exposure steps 59/60 (≥ 90 %) | **PASS** |
| (b) jump cuts | rb = 8, Dmin = 0.2 (only grid point family with FP ≤ 5 %) | recall 0.27 (known 1/4); FP 0.01 | synthetic recall 9/60 (≥ 80 % needed); FP 0/100 | **FAIL** → not used (INCONCLUSIVE) |
| (c) near-black cuts | rc = 5, Dmin_c = 0.3, smin = 0.8 | recall 0.86 (known 4/4); FP 0.03 | dark-cut recall 55/60; FP 1/100 | **PASS** |
| (d) dissolves (revised) | τr = 0.25, τs = 0.5, ρ = −0.9 | recall 0.83; static FP 0.03; ramp FP 0.04; known 3/3 positives, 0/2 negatives flagged | recall 0.983 (≥ 80 %); static FP 0.01 (≤ 5 %); ramp FP 0.03 (≤ 10 %) | **PASS** |

## Stats vs v2
| Measure | v2 | v3 |
|---|---|---|
| Cut events | 211 confirmed | 234 = 181 kept from v2 + 53 near-black (0 jump cuts) |
| Reclassified LIGHT_CHANGE | — | 30 (2 are tuning items: 802.23, 2184.78) |
| SHOT / BLACK / DISSOLVE segments | 285 / 120 / 0 used (20 INCONCLUSIVE) | 333 / 198 pieces / 39 (88 soft-transition spans; 68 fade-like) |
| SHOT median / mean | 3.203 / 7.127 s | 3.259 / 5.833 s |
| Longest SHOT | 80.9 s | 66.9 s (S1-SH133 talk) |

Tuning items are reported separately and never count as validation: all 4 near-black tuning cuts and all 6 other reviewer cut times are in v3; 0 of 4 jump-cut tuning items.

## Post-hoc author frame check (informational only; nothing changed) — `seg_v3_posthoc_informational.json`
- (a) removed the real cut at 115.415 s (hall → interview) as a light change; dark-scene structure noise can inflate Q. Removals at 1513.3 s and 2015.3 s look correct.
- (c) several near-black detections in the lamp-pulse passages (e.g. 654.65 s) look like lamp events; 699.50 s is ambiguous (lights on vs cut).
- (d) spans inside the Speaker B talk at 919–1000 s (e.g. 942–944 s) are head motion on a plain wall: false positives.
These are recorded as F-32..F-34 and are exactly what round 4 measures (strata SEG3_LIGHT, SEG3_DARK_NEW, SEG3_DISSOLVE).

Claims: `claims-evidence.v7.jsonl` (S1-SEG3-MEA-001..004, S1-INF-003@v5), O5 PASS.
