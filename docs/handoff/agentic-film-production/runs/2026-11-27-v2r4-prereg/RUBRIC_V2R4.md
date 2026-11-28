# S1 V2 round 4 rubric (RUBRIC_V2R4, new pre-registration)

New file; changes no earlier rubric, package, answer file or result. Committed **before** the round-4 package is built and before any round-4 review. Thresholds are fixed now.

**Outcome label: agent review.** Owner standing rule: every round first uses a Grok Bot reviewer agent → same identity as the author (F-12) → reported verdict **capped at INCONCLUSIVE** (passed to the scorer as `--breach`); the uncapped gate verdict is reported next to it.

**Reference truth:** segmentation v3 (`PREREG_SEG_V3_2026-11-27.md`, output `pack-v3/seg/`): v3 cut events (v2 cuts kept by detector (a) + near-black cuts from (c)), BLACK edges, v3 DISSOLVE segments (detector (d) passed its controls), and the v3 LIGHT_CHANGE list (author says: not a cut). Plus author labels/claims. Round-1/2/3 answers are never reference, decoys or sampling input.

## Changes vs RUBRIC_V2R3
| Issue | Round-4 rule |
|---|---|
| F-26 anchoring | Stage B contains **no** earlier-round scoring, post-hoc, answer, failure-case, oracle or strata files. Files are whitelisted (core evidence + files cited by included claims); the build fails if any bundled name matches `score|posthoc|answer|failure|oracle|strata|REVIEW`. Claims that cite or quote earlier-round reviewer findings are **excluded**: S1-MEA-002, S1-MEA-004, S1-INF-002, S1-UNK-credits, S1-EXT-INF-E2, S1-EXT-INF-E3, S1-EXT-INF-E2-labels, S1-SEG2-MEA-001, S1-SEG2-MEA-003. |
| Tuning circularity | Every seg-v3 tuning item (PREREG_SEG_V3 §1) is excluded from all round-4 samples with ±2.0 s padding; so are all round-1/2/3 windows, spans, camera spans and A1 timestamps (±0.5 s). |
| F-29/F-30/F-27/F-31 | New strata SEG3_LIGHT, SEG3_DARK_NEW, SEG3_DISSOLVE and gates R4-dark, R8, R7 (scored, because detector (d) passed). Jump cuts: detector (b) failed, nothing added; reviewer jump cuts in RANDOM/A3 count against R4-rec. |
| Space | Free time after exclusions is about 870 s, so A3 spans are 12 s (not 30 s). A2 targets 60 windows (minimum 40); A4 targets 20 spans (minimum 12). Sampling order A3 → A4 → A2 → A1. |
| Freshness | New secret seed (SHA-256 commitment published), 4 new decoys, new ids (A2 W01.., A3 U01.., A1 R01.., A4 C01.., claims L01..). |
| Isolation | As round 3: MKV included; stage B encrypted, passphrase released only after the stage-A hash is logged in git; oracle key as AES-256 ciphertext in a separate `chmod 000` dir; forbidden-path list now also names `v2_review_package_r3/` and `v2r3_oracle_sealed/`. |

## Stage A (blind)
A1 30 timestamps (v3 SHOT segments lying in one v1 segment) · A2 ≤ 60 four-second windows · A3 6 twelve-second spans · A4 ≤ 20 camera spans (sub-intervals ≥ 3 s of v3 SHOT interiors with no v3 cut, light change, dissolve span, near-black or jump detection, v2 unconfirmed candidate, v2 dissolve span or BLACK inside; native-rate decode check; author label = E2 on the exact span) · A5 sequence starts. A2 strata targets (sealed): SEG3_CUT_V1 6, SEG3_CUT_NEW 7, SEG3_DARK_NEW 7, SEG3_LIGHT 7, SEG3_DISSOLVE 7, SEG3_BLACK_EDGE 5, RANDOM the rest.

## Gates (±0.5 s; cut events = HARD_CUT, CUT_TO_BLACK, CUT_FROM_BLACK; soft events = DISSOLVE, FADE_TO_BLACK, FADE_FROM_BLACK)
| Id | Rule | Threshold |
|---|---|---|
| R1 | 4 decoys NOT_SUPPORTED | else INVALID_REVIEW |
| R2-inf | INFERRED SUPPORTED or PARTIALLY_SUPPORTED | ≥ 75 % |
| R2-mea | MEASURED SUPPORTED | ≥ 90 % (shortfall only CANNOT_DETERMINE + EVIDENCE_MISSING_FROM_PACKAGE → INCONCLUSIVE) |
| R3-role | A1 role agreement | ≥ 80 % of determinate (needs ≥ 10) |
| R3-seq | A5 vs author sequence starts ±10 s | F1 ≥ 0.60 |
| R4-prec | SEG3_CUT_V1 + SEG3_CUT_NEW windows: reviewer cut event at target ±0.5 s | ≥ 90 % |
| R4-new | SEG3_CUT_NEW only | ≥ 80 % (needs ≥ 5) |
| R4-dark | SEG3_DARK_NEW: reviewer cut event at target ±0.5 s | ≥ 80 % (needs ≥ 5) |
| R4-rec | reviewer cut events in RANDOM + A3 matched by a v3 cut / BLACK edge ±0.5 s or inside a v3 DISSOLVE segment | ≥ 80 % (needs ≥ 5) |
| R5 | no real claim flagged for forbidden inference | 0 |
| R6 | A4 STATIC-vs-MOVING agreement | ≥ 70 % of determinate (needs ≥ 10) |
| R7 | SEG3_DISSOLVE: reviewer soft event overlapping the span ±0.5 s | ≥ 70 % (needs ≥ 5) |
| R8 | SEG3_LIGHT: reviewer reports **no** cut event within ±0.5 s of the target | ≥ 80 % (needs ≥ 5) |
| info | soft events in RANDOM + A3 matched by v3 dissolves; v3 boundaries in A3 matched; R6 type agreement | no threshold |

## Verdict
R1 fails → INVALID_REVIEW. Any of R2–R8 FAIL → FAIL; else any INCONCLUSIVE → INCONCLUSIVE; else PASS. Breaches (same identity — always true for Grok Bot reviewers; stage-A hash not logged before release; stage A edited after hash; forbidden-path read) cap the reported verdict at **INCONCLUSIVE (agent review)**; writes outside `answers/` are logged as limitations.

Scorer `studio/reverse/v2r4_score.py`; builder `studio/reverse/v2r4_build_package.py`; both committed with this file.
