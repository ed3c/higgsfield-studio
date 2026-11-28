# S1 H02 extension（新增檔案，不覆寫 v1）— pre-registration

Written and committed **before** the extension analyses run. Owner approval: Neon, 2026-11-27 ~01:37 UTC+8 (relayed by parent session):
"Approved: OpenCV, PySceneDetect, librosa. Record this approval as the explicit owner exception for the bundled-FFmpeg wheels."
See `OWNER_EXCEPTION_BUNDLED_FFMPEG_2026-11-27.md`.

Inputs (private, box): 480x270 H.264 proxy (`work/proxy_480x270.mp4`, made by ffmpeg from the admitted mkv), 5 fps 320x180 gray raw
(`work/frames_5fps_320x180.gray`), 22,050 Hz mono PCM made by ffmpeg (librosa's soxr resampler is not used), v1 `shots/segments.json`.

## E1 PySceneDetect second cut detector

- `ContentDetector()` defaults (threshold 27, min_scene_len 15) and `AdaptiveDetector()` defaults, on the proxy.
- Agreement with v1 hard cuts: match if |Δ| <= 3 frames. Report matched / v1-only / PySceneDetect-only. No detector is treated as truth.

## E2 Camera movement (OpenCV)

- For each v1 SHOT segment >= 1.0 s: consecutive 5 fps frames, `goodFeaturesToTrack(maxCorners=200, qualityLevel=0.01, minDistance=8)`
  on CLAHE-normalised frames, `calcOpticalFlowPyrLK`, `estimateAffinePartial2D` (RANSAC 3 px) → per-step tx, ty, scale, rotation.
- Labels (per segment, INFERRED from MEASURED steps):
  - `UNDETERMINED_LOW_TEXTURE` if < 20 tracked inliers in >= 50% of steps.
  - `STATIC` if median step speed < 0.5 px (at 320 px width) and |Σ log scale| < 0.02.
  - `ZOOM_OR_PUSH_IN` / `ZOOM_OR_PULL_OUT` if Σ log scale >= +0.05 / <= -0.05.
  - `PAN_OR_TRACK_H` / `TILT_OR_PEDESTAL_V` if one axis has >= 60% of steps with the same sign and its median |speed| >= 0.5 px.
  - `HANDHELD_OR_IRREGULAR` otherwise when median speed >= 0.5 px.
- A 2-D affine fit cannot separate pan from track or zoom from dolly; labels say so. Subject motion can bias the fit.

## E3 Near-black boundary disambiguation（cut vs lighting）

- For each v1 NEAR_BLACK segment with SHOT neighbours: frame 0.2 s before black start vs frame 0.2 s after black end (5 fps stream), CLAHE.
- ORB(1000) + BFMatcher Hamming + Lowe ratio 0.75 + homography RANSAC 5 px → inliers; plus edge-map correlation (Canny 50/150, 3x3 blur).
- `SAME_TAKE_LIGHTING` if inliers >= 25 and inlier ratio >= 0.30; `EDITORIAL_CUT` if inliers < 8 and edge corr < 0.20; else `UNDETERMINED`.
- Calibration controls (run first, same code):
  - positive CUT control = every v1 hard cut (frames 0.2 s before / after) → expect `EDITORIAL_CUT` + `UNDETERMINED` <= 20% classified SAME.
  - positive SAME control = up to 80 random pairs 1.0 s apart inside v1 SHOT segments >= 4 s with no hard cut (seed 20261127) → expect >= 80% not classified CUT.
  - If either control fails, all E3 labels are reported as INCONCLUSIVE (not used for claims).

## E4 Music / sound analysis（librosa）

- 22,050 Hz mono, hop 512. Per 5 s window and per v1 audio section: HPSS harmonic energy ratio, onset-strength mean,
  beat-track tempo + inter-beat-interval CV, chroma peakiness (mean of max/sum), spectral flatness, RMS.
- Window labels (exploratory, uncalibrated, INFERRED): `MUSIC_LIKELY` if not speech and harmonic ratio >= 0.60 and chroma peakiness >= 0.25;
  `RHYTHMIC` if IBI CV <= 0.15 and >= 8 beats; `NOISE_OR_AMBIENCE` if flatness >= 0.30; else `UNDETERMINED`. Speech windows (v1 speech mask >= 50%) are `SPEECH`.
- Music vs ambience vs installation sound stays a hypothesis until a human listens.

## Outputs (new files only)

`pack-ext/`：`scenedetect_cuts.json`, `camera_motion.json`, `dark_boundary_disambiguation.json`, `music_analysis.json`, `claims-evidence.ext.jsonl`, `EXT.md`, `SHA256SUMS`.
