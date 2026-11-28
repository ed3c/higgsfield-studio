# Owner exception: tqdm (MPL-2.0) and soxr (LGPL-2.1+), local analysis only (new file)

- Decision: Neon accepted `tqdm` (MPL-2.0) and `soxr` / `python-soxr` (LGPL-2.1+) **limited to local analysis only**. Relayed by the parent session 2026-11-27 ~02:14 (UTC+8).
- Context: the transitive dependencies flagged in `OWNER_EXCEPTION_BUNDLED_FFMPEG_2026-11-27.md` (that file is not changed). `tqdm` comes in through PySceneDetect; `soxr` through librosa.
- Scope: run on the box for private analysis only. No redistribution, no bundling into a shipped artifact, no modification of either library. Leaving that scope needs a new owner decision.
- Effect: the `PENDING_LICENCE_DECISION` marker on the PySceneDetect-derived claims is lifted by **new** claim versions (`runs/2026-11-27-v2r2-prereg/claims-evidence.v3.jsonl`, `S1-EXT-MEA-E1-content@v3`, `S1-EXT-MEA-E1-adaptive@v3`). The v2 rows that carry the marker stay as they are.
- Up to this point `soxr` had not been invoked (E4 read PCM produced by ffmpeg). This exception does not re-run anything.
