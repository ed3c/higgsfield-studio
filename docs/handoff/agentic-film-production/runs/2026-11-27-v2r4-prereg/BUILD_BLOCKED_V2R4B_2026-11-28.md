# Round 4b build — BLOCKED (2026-11-28, nothing built, no secrets created)

The 4b build under RUBRIC_V2R4 + amendment `AMENDMENT_V2R4B_2026-11-28.md` (95a4f56) stopped at its first sampling step: `only 0 free 12 s spans`.
The builder exited before writing any package, key or passphrase (`v2_review_package_r4b/` and `v2r4b_oracle_sealed/` do not exist).

Feasibility (free film time after each exclusion set, film 2333.4 s):

| Cumulative exclusions | Free time | Free gaps ≥ 12 s | Longest free gap |
|---|---|---|---|
| round 1 (60 items) | 2115 s | 41 | 258.4 s |
| + round 2 (116) | 1523 s | 45 | 49.1 s |
| + round 3 (116) | 884 s | 16 | 23.3 s |
| + seg-v3 tuning (23, ±2 s) | 871 s | 16 | 23.3 s |
| + voided round-4 stage A (116) | 377 s | **0** | 6.8 s |

RUBRIC_V2R4 needs 6 A3 spans of 12 s and at least 12 A4 spans of ≥ 3 s, so with the voided round-4 items excluded the pre-registered design cannot be sampled. No rule was changed and no workaround was applied; the owner decides how to proceed (see the 2026-11-28 report).
