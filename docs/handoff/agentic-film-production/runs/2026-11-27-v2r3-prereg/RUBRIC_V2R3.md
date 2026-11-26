# S1 V2 round 3 rubric (RUBRIC_V2R3, new pre-registration)

This file is new. It changes no earlier rubric, package, answer file or result. It is committed **before** the round-3 package is built and before any round-3 review.
Thresholds are fixed now and will not be changed after the review.

**Outcome label: agent review.** Owner standing rule: every round first uses a Grok Bot reviewer agent. A Grok Bot reviewer has the same identity as the author (F-12/F-24), so the verdict is **capped at INCONCLUSIVE**. The scorer receives that cap as a `--breach`.

**Reference truth.** The reference is the author's pack: segmentation v2 (`PREREG_SEG_V2_2026-11-27.md`, run output `pack-v2/seg/`) plus author labels and claims.
Answers from round 1 and round 2 are **not** used as reference truth, as decoys, or for sampling. Round-1 and round-2 windows are only used to avoid overlap.

## Changes vs RUBRIC_V2R2

| Issue | Round-3 rule |
|---|---|
| F-23: v1 cut list incomplete | Every boundary reference uses **segmentation v2** (confirmed cuts ∪ BLACK edges ∪ DISSOLVE spans). A confirmed cut event within 2 frames of a BLACK edge is that BLACK edge (one boundary, kind black_edge), and SEG2_CUT_* strata draw only from cuts not at a BLACK edge. |
| F-16: camera spans contaminated | A4 spans are drawn **only** from S5-verified cut- and dissolve-free intervals. The author label is E2 recomputed on the exact span. |
| F-25: dissolves unscored | New gate **R7** (dissolve agreement). A2 stratum `SEG2_DISSOLVE`. |
| Claim defects | Claims are reviewed at their current head versions: v1 → v2/v3/v4 corrections → v5. v4 and v5 are included. |
| Freshness | New secret seed (SHA-256 commitment published), 4 new decoys, new windows/spans with no overlap with round 1 or round 2 (0.5 s pad). |
| Isolation | Same as round 2: the MKV is included; stage B is encrypted and its passphrase is released only after the stage-A hash is reported; the oracle key is AES-256 ciphertext in a separate `chmod 000` directory; there is a forbidden-path list. |

## Stage A (blind)

| Task | Content |
|---|---|
| A1 | 30 timestamps: role / shot scale / lighting / content |
| A2 | 60 four-second windows: every transition, with time (s) and type |
| A3 | 6 thirty-second spans: complete transition list |
| A4 | 20 verified camera spans: movement label |
| A5 | sequence starts |

The A2 strata are sealed; the counts are listed in the sealed key.

A1 timestamps are sampled only from S2 SHOT segments that lie wholly inside a single v1 segment, so the author role label is unambiguous.

## Gates (tolerance ±0.5 s; cut events = HARD_CUT, CUT_TO_BLACK, CUT_FROM_BLACK; soft events = DISSOLVE, FADE_TO_BLACK, FADE_FROM_BLACK)

| Id | Rule | Threshold |
|---|---|---|
| R1 | all 4 decoys NOT_SUPPORTED | else INVALID_REVIEW |
| R2-inf | INFERRED claims SUPPORTED or PARTIALLY_SUPPORTED | ≥ 75% |
| R2-mea | MEASURED claims SUPPORTED | ≥ 90%. A shortfall consisting only of CANNOT_DETERMINE with reason EVIDENCE_MISSING_FROM_PACKAGE → INCONCLUSIVE |
| R3-role | A1 role agreement | ≥ 80% of determinate answers (needs ≥ 10) |
| R3-seq | A5 vs author sequence starts, ±10 s | F1 ≥ 0.60 |
| R4-prec | A2 windows centred on a seg-v2 confirmed cut (strata SEG2_CUT_V1 + SEG2_CUT_NEW): reviewer reports a cut event within ±0.5 s | ≥ 90% |
| R4-new | the same, restricted to SEG2_CUT_NEW (cuts not in v1) | ≥ 80% (needs ≥ 5) |
| R4-rec | reviewer cut events in A2 RANDOM windows + A3 spans that match a seg-v2 cut or BLACK edge (±0.5 s), or fall inside a DISSOLVE span | ≥ 80% (needs ≥ 5) |
| R5 | no real claim flagged for forbidden inference | 0 |
| R6 | A4 STATIC-vs-MOVING agreement with the span-level author label | ≥ 70% of determinate answers (needs ≥ 10) |
| R7 | A2 windows of stratum SEG2_DISSOLVE: reviewer reports a soft event overlapping the author span ±0.5 s | ≥ 70% (needs ≥ 5). If the S3 dissolve controls failed, R7 is INCONCLUSIVE. |
| info | reviewer soft events in RANDOM + A3 matched by seg-v2 dissolves; author seg-v2 boundaries in A3 matched by any reviewer event; R6 movement-type agreement | reported, no threshold |

## Verdict

1. If R1 fails → **INVALID_REVIEW**.
2. If any gate (R2–R7) FAILs → the gate-level verdict is FAIL. Otherwise, if any gate is INCONCLUSIVE → INCONCLUSIVE. Otherwise → PASS.
3. A protocol breach caps the reported verdict at **INCONCLUSIVE (agent review)**. Breaches are: same identity as the author (always true for Grok Bot reviewers); stage-A hash not logged before the passphrase is released; stage A edited after its hash; any read of a forbidden path. The uncapped gate-level verdict is reported next to the capped one.

Scorer: `studio/reverse/v2r3_score.py`. Builder: `studio/reverse/v2r3_build_package.py`. Both are committed with this file.

## Amendment 1 (2026-11-27, before any package was released or reviewed)

The first build attempt hung (no free 30 s A3 span after A2 sampling) and the second produced only 3 A4 spans, because whole verified intervals rarely avoid every round-1/round-2 item. Both builds were discarded unreleased (never shown to a reviewer). Sampling order is now A3 → A4 → A2 → A1. An A4 span is the **largest sub-interval (≥ 3.0 s) of an S5-verified interval** that is free of round-1/round-2 items and earlier round-3 items; the exclusion checks (unconfirmed candidates, DISSOLVE, BLACK) still run on the whole verified interval, E2 is recomputed on the exact sub-span and the native-rate decode check runs on it. Gates and thresholds are unchanged.
