# S1 V2 round 2: protocol for an independent reviewer agent

You are an **independent reviewer**, a different identity from the author (the author is Grok Bot). Do not contact the author.
The result is recorded as **agent review**. It is not a human Oracle (cf. GAP-EVAL-01). Scoring follows `RUBRIC_V2R2.md`, which was pre-registered before this package was built.

Source: S1 = YouTube `onNBysMf9WM`, an exhibition documentary (2333.388 s, AV1 3840x2160, 30000/1001 fps, Opus audio).
Rights scope: **private_analysis only**. Do not upload, post, share or send any video, frame, audio or transcript off this box.
Do not web-search this film or the people in it. **Do not identify anyone from their face**; describe people by role only. Lens, focal length, camera body, prompt and seed cannot be determined from frames.

## Read scope

You may read only `/workspace/afp-private/v2_review_package_r2/`, and you write only to `answers/` (plus the folder you extract stage B into).
**Do NOT read**, even though the shared box lets you:
- `/workspace/afp-private/v2r2_oracle_sealed/` (the sealed scoring key)
- `/workspace/afp-private/sources/` (the author's pack, claims and inferences)
- `/workspace/afp-private/v2_review_package/`, `v2_oracle_key/`, `v2_oracle_key.SHA256SUMS`, `v2_review_package*.tar` (round 1, including the earlier reviewer's answers)
- every other path under `/workspace/afp-private/` (srt_proofreading_kit*, passport*, notion, drive_out, …)
- the repository `/workspace/hs-afp/` and GitHub `ed3c/higgsfield-studio` (it holds the author's claims and round-1 results)
- Neon's Google Drive AFP folders, and any Grok Bot transcript or memory

If you read any of these by accident, say so in `REVIEW_SUMMARY.md`. That caps the verdict at INCONCLUSIVE; it does not invalidate your work.

## Contents

| Path | Content |
|---|---|
| `stage_A/media/onNBysMf9WM.mkv` | full source video, byte-identical to the admitted source (SHA-256 `7309020bcd547d4527f3fd9a36c585ac36fdb605b107b7b2242315b65b1ef45c`), read-only |
| `stage_A/evidence/` | `media-probe.json` (ffprobe), `onNBysMf9WM.ja.machine-asr.srt` (Whisper large-v3 machine ASR, post-filtered, **not proofread**) |
| `stage_A/stills/Pxx.jpg` | frame at each A1 timestamp (1280 px wide, from the MKV) |
| `stage_A/strips/Xxx.jpg` + `windows.json` | A2 windows: 16 frames at 4 fps from a 480x270 proxy, laid out 4x4 row-major; frame i ≈ t_start + i·0.25 s. Use these as a guide only; give times from the MKV. |
| `stage_A/timeline_sheets/Txx.jpg` | one frame every 5 s across the whole film, labelled by time only |
| `stage_A/stage_A_answers.template.json` | all stage A questions (A1–A5) |
| `stage_B_sealed.tar.gz.enc` | **encrypted** author claims plus every file they cite. You get the passphrase only after step 2. |
| `RUBRIC_V2R2.md` | how you are scored |
| `answers/` | your outputs go here |

Tools: `ffmpeg`/`ffprobe` are on the box. Inspect transitions at native frame rate, for example `ffmpeg -ss <t-1> -i stage_A/media/onNBysMf9WM.mkv -t 2 -vf "scale=640:-2" /tmp/r2_%03d.png`. Delete temporary frames afterwards, and keep them off any shared location.

## Protocol

1. **Stage A (blind).** Copy the template to `answers/stage_A_answers.json` and fill it in:
   - A1: role, shot scale, lighting and content at each timestamp.
   - A2: every transition in each 4-second window, with time in seconds and type.
   - A3: a complete transition list for each 30-second span.
   - A4: the camera movement in each span.
   - A5: the times where major sequences begin.
   
   Use `CANNOT_DETERMINE` instead of guessing. Fill in `reviewer.identity`.
2. Run `sha256sum answers/stage_A_answers.json`. Append the hash with a timestamp in UTC+8 to `answers/REVIEW_LOG.md`, then `chmod 444` the file. **Report that hash to the dispatcher.** The dispatcher logs it and only then gives you the stage-B passphrase. Do not edit stage A afterwards.
3. **Stage B.** Decrypt and extract:
   `openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt -md sha256 -d -pass env:R2_PASS -in stage_B_sealed.tar.gz.enc | tar -xzf - -C answers/..`
   (`R2_PASS` = the passphrase). Optional check: the decrypted tar.gz has SHA-256 `9de58be0dfb675fc445d50e2a775c3d3406e661e93f69b31f95db343d489c5bf`. Log the time you opened it.
   For every claim in `stage_B/claims_to_review.jsonl`, open the cited evidence yourself (see `stage_B/PATHS.md` and `stage_B/evidence/id_index.json`). Use the MKV wherever frames, frame counts, dissolves or camera motion matter. Then fill in `stage_B_answers.template.json` → `answers/stage_B_answers.json`:
   - verdict;
   - for CANNOT_DETERMINE, a reason: `EVIDENCE_MISSING_FROM_PACKAGE`, `AMBIGUOUS` or `OTHER`;
   - whether the claim's class is appropriate;
   - any forbidden inference;
   - the exact file and locator you checked.
   
   Claims can be wrong; judge each one only on the evidence.
4. Write `answers/REVIEW_SUMMARY.md`:
   - your identity (agent / model / person, as known), and whether it differs from the author;
   - start and finish times;
   - what you could not check;
   - any path you read outside the read scope;
   - any concern about the package.
5. Stop. Do not score yourself. Do not edit anything outside `answers/` and the extracted `stage_B/`.
