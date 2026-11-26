# S1 H02 extension (OpenCV / PySceneDetect / librosa; owner exception 2026-11-27)

New files only; v1 pack unchanged. Pre-registration: `PREREG_EXT_2026-11-27.md`.

| Analysis | Result | Status |
|---|---|---|
| E1 PySceneDetect content | 209 cuts, 83/83 v1 cuts matched | MEASURED; agreement only |
| E1 PySceneDetect adaptive | 298 cuts, 82/83 v1 cuts matched | MEASURED; agreement only |
| E2 camera movement | {'ZOOM_OR_PUSH_IN': 24, 'STATIC': 56, 'PAN_OR_TRACK_H': 11, 'ZOOM_OR_PULL_OUT': 19, 'HANDHELD_OR_IRREGULAR': 13, 'UNDETERMINED_LOW_TEXTURE': 8, 'TILT_OR_PEDESTAL_V': 2} | MEASURED fit, INFERRED labels; acceptance NOT_RUN |
| E3 dark boundaries | calibration PASS; {'NOT_APPLICABLE (no SHOT on both sides)': 11, 'EDITORIAL_CUT': 41, 'SAME_TAKE_LIGHTING': 23, 'UNDETERMINED': 45} | INFERRED labels; acceptance NOT_RUN |
| E4 music | {'MUSIC_LIKELY': 150, 'SPEECH': 284, 'UNDETERMINED': 21, 'RHYTHMIC': 10, 'NOISE_OR_AMBIENCE': 2}; non-speech MUSIC_LIKELY 145/178 | INFERRED; human listening NOT_RUN |

Unknowns updated (no v1 overwrite): U-02 → partially addressed by E3 (still INCONCLUSIVE for UNDETERMINED); U-04 → E2 labels (INFERRED); U-05 → E4 labels (INFERRED).