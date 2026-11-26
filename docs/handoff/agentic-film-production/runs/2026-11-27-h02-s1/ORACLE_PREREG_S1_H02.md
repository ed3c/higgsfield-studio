# S1 H02 — Pre-registered checks (written and committed BEFORE the pack is built or checked)

Source: S1 `onNBysMf9WM` · media SHA-256 `7309020bcd547d4527f3fd9a36c585ac36fdb605b107b7b2242315b65b1ef45c` (mkv) ·
WAV `df7d39d676c5875c4b0e2b033ec2e58b96c91799a708791f84b719b2557b86aa` · SRT `228d5a51faf7eb4f973c4abe466647c8696ce30c8d464c26468510cd738bb2bb`.
Handoff pin: `5b35ce61e25e93447dc21c731214062605aeec08` §4, §9 (V0/V1/V2), §10 step 2. Soodles route pin `939875f` `skills/reverse-route/routes/higgsfield-studio.md`.

## What this is and is not

- These are **automated, independent-algorithm checks** (different decode path / different metric from the producer). They are
  NOT the independent human Oracle of handoff §9, and they never mark V2 (Reverse inference accuracy) PASS.
- Thresholds below are fixed now. They are not tuned after seeing the check results. If a check fails, the failure is recorded
  as-is (Bounded Convergence); a revised check would be a new, separately versioned pre-registration.

## Producer parameters (fixed now)

| Parameter | Value |
|---|---|
| Hard-cut detector | ffmpeg `select` scene score on 320x180 decode; cut when `scene_score >= 0.30`; merge cuts closer than 0.5 s (keep higher score) |
| Black / fade segments | ffmpeg `blackdetect d=0.2 pix_th=0.10`; black interval becomes its own `BLACK` segment |
| Gradual-transition candidates | 2 fps 160x90 RGB, 16-bin-per-channel histogram L1 distance between frames 2 s apart >= 0.5 with no hard cut / black inside the window → flagged `CANDIDATE_GRADUAL` (INFERRED, not a boundary) |
| Visual measures | per 2 fps frame: mean luma (Rec.709), luma std, mean HSV saturation, colourfulness (Hasler–Süsstrunk), edge density (Sobel-like |grad| > 24), luma centroid, inter-frame mean abs diff (motion proxy) |
| Audio measures | 16 kHz mono: per-second RMS dBFS, spectral centroid, spectral flatness; ffmpeg ebur128 momentary loudness; silencedetect n=-45 dB d=1.5 s; speech coverage from post-filtered SRT cues |

## Checks

| ID | Check | PASS rule |
|---|---|---|
| O1 hash | mkv / wav / srt SHA-256 recomputed and equal to the values above | all equal |
| O2 timebase | segments are contiguous, non-overlapping, start at 0, end within 1 frame (1/29.97 s) of media duration; every segment has start < end | all hold |
| O3 cut precision | for EVERY detected hard cut: separate ffmpeg decode (input-seek, 64x36 gray, native frame rate) of 0.5 s around the cut. `d_cut` = max mean-abs-diff of adjacent frames within ±2 frames of the cut; `d_base` = median adjacent-frame diff in the window excluding those ±2 frames. Confirmed if `d_cut >= 8.0` AND `d_cut >= 3 * max(d_base, 0.5)` | confirmed fraction >= 0.90 |
| O3n negative control | same procedure at N = number of cuts random timestamps (seed 20261127) that are >= 2 s from any boundary or black segment | false-confirm fraction <= 0.10 |
| O4 A/V | WAV duration vs mkv duration differ <= 0.10 s; every SRT cue lies inside [0, duration] | both hold |
| O5 claims | every claim in `claims-evidence.jsonl` has all §4 fields; class in {SOURCE_EVIDENCE, MEASURED, INFERRED, UNVERIFIED_CLAIM, UNKNOWN}; MEASURED claims cite a measurement file + locator that resolves; INFERRED claims carry a non-empty alternative explanation and unknowns; no MEASURED/SOURCE_EVIDENCE claim asserts lens/focal length/seed/prompt/camera path/model parameters | all hold |
| O6 privacy | git-bound pack files: no image/audio/video bytes, no SRT cue text of length >= 8 characters copied verbatim | all hold |

## Not checkable here (stay NOT_RUN / INCONCLUSIVE)

- Cut **recall** (missed dissolves / soft cuts): needs human ground truth → NOT_RUN.
- Shot scale, blocking, camera movement type, lens hypotheses, art mechanism, story structure: agent observations are INFERRED;
  V2 inference accuracy needs an independent reviewer → NOT_RUN.
- Comparison of reverse methods (REA-Video vs HyperFrames vs film baseline, §10 step 2): REA-Video and HyperFrames are not
  admitted/pinned/audited for execution → NOT_RUN; only the film baseline (this Studio-specific adapter) runs.
