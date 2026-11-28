# S1 V2 round 2 rubric (RUBRIC_V2R2, new pre-registration)

This file is new. It does not change RUBRIC.md v1, the round-1 package, the round-1 answers or the round-1 results
(`runs/2026-11-27-v2-prep/`, `runs/2026-11-27-v2-result/`). It was committed **before** the round-2 package was built and before any
round-2 review. Thresholds below are not changed after a review; a later change would be a new versioned file.

Outcome label: **agent review** (not a human Oracle; cf. GAP-EVAL-01). Reviewer must be a **different identity** from the author
(the author is Grok Bot). The reviewer states its identity in `answers/REVIEW_SUMMARY.md`.

## Package design (fixes for F-07 .. F-15)

| Defect (round 1) | Round-2 rule |
|---|---|
| F-09 stage A saw author cut list | Stage A gets **no** author segment ids, cut/black lists, segment-labelled keyframes, sections or inferences. Stage A = full MKV (byte-identical to the admitted source, SHA-256 `7309020b…ef45c`), media probe, machine-ASR SRT (unreviewed), neutral stills / strips / timeline sheets labelled only by time. |
| F-08 no video | Full MKV included (read-only copy). |
| F-07 cited files missing | Stage B bundles every file a claim cites: trimmed `info.json` (download URLs/headers removed), `.description`, `passC.log`, O3 re-check (`checks_O1-O4.json`), decode summary, `id_index.json` for internal ids, observations, reverse-ir, ext outputs (incl. PySceneDetect after the tqdm/soxr owner exception), keyframes, author contact sheets. |
| F-13 repeated / overlapping strips | Fresh windows from a **new secret seed** (logged inside the sealed key, SHA-256 commitment of `seed:nonce` published); no window or span overlaps another (0.5 s pad) or any round-1 window. |
| decoys reused | 4 **fresh** decoys (2 MEASURED, 2 INFERRED), different from round-1 C002/C003/C017/C023; decoy text kept out of git until after scoring. |
| F-15 oracle on the same tree | Oracle key built in memory, written only as AES-256-CBC (PBKDF2-SHA256, 600k iterations, salted, `openssl enc`) ciphertext in a separate directory outside the package (directory also `chmod 000`). Plaintext SHA-256 (with an internal 128-bit nonce) is published so the decrypted key can be verified. Passphrase is held only in the author's report to the owner. |
| A→B order only by log | Stage B is also encrypted. The dispatcher gives the reviewer the stage-B passphrase **only after** the reviewer reports the SHA-256 of `answers/stage_A_answers.json`. |
| F-14 R4 ignored near-black cuts | R4 reference = all author boundaries (hard cuts **and** near-black edges). |
| F-12 same bot | Different reviewer identity required; same identity → verdict capped at INCONCLUSIVE. |

## Stage A tasks (blind)

- **A1** 30 timestamps: people role, shot scale, lighting, content (stills given; MKV for checking).
- **A2** 60 four-second windows: every transition with time (s, from MKV at native rate) and type.
- **A3** 6 thirty-second spans: complete transition listing at native frame rate.
- **A4** 20 camera spans: movement label.
- **A5** sequence starts (s) from timeline sheets + MKV.

## Gates

Matching tolerance for transitions: reviewer time within **±0.5 s** of an author boundary.
"Cut events" = reviewer types HARD_CUT, CUT_TO_BLACK, CUT_FROM_BLACK.

| Id | Rule | Threshold |
|---|---|---|
| R1 | all 4 decoys judged NOT_SUPPORTED | else verdict INVALID_REVIEW |
| R2-inf | author INFERRED claims SUPPORTED or PARTIALLY_SUPPORTED | ≥ 75% |
| R2-mea | author MEASURED claims SUPPORTED | ≥ 90%. If the shortfall consists only of CANNOT_DETERMINE with reason EVIDENCE_MISSING_FROM_PACKAGE, R2-mea is INCONCLUSIVE instead of FAIL. |
| R3-role | A1 agreement with author role labels (interview roles vs not, and which interview role) | ≥ 80% of determinate answers; < 10 determinate → INCONCLUSIVE |
| R3-seq | A5 sequence starts vs author sequence starts, ±10 s | F1 ≥ 0.60 |
| R4-prec | A2 windows of stratum V1_HARD_CUT where reviewer reports a cut event within ±0.5 s of the author cut | ≥ 90% |
| R4-rec | reviewer cut events in A2 RANDOM windows + A3 spans that match any author boundary | ≥ 80%; < 5 events → INCONCLUSIVE |
| R4-info | reviewer DISSOLVE / FADE events in A2 + A3, and author boundaries in A3 not matched by any reviewer event | reported, no threshold (dissolve recall was NOT_RUN in the pack) |
| R5 | no real claim flagged for forbidden inference | 0 |
| R6 | A4 STATIC vs MOVING agreement with author E2 labels | ≥ 70% of determinate answers; < 10 determinate → INCONCLUSIVE |
| R6-info | movement-type agreement among spans both call MOVING | reported |

## Verdict

1. R1 fails → **INVALID_REVIEW (agent review)**.
2. Protocol breach → verdict capped at **INCONCLUSIVE**: stage-A hash not logged before the stage-B passphrase was released; reviewer identity same as the author; stage A edited after its hash; reviewer read anything on the "must not read" list.
3. Else any gate FAIL → **FAIL (agent review)**; else any INCONCLUSIVE → **INCONCLUSIVE (agent review)**; else **PASS (agent review)**.

Scorer: `studio/reverse/v2r2_score.py` (committed with this file). Inputs: package answers + decrypted key (verified against the
published plaintext SHA-256). Builder: `studio/reverse/v2r2_build_package.py`.
