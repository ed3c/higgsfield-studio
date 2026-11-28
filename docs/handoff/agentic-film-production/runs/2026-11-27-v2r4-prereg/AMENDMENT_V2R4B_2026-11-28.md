# RUBRIC_V2R4 — amendment for round 4b (2026-11-28, before the 4b build and before any 4b review)

Round 4 is VOID (F-36, `VOID_V2R4_2026-11-28.md`). Round 4b replaces it.

- **Same pre-registration:** RUBRIC_V2R4 (7aef91b), scorer `studio/reverse/v2r4_score.py` and builder `studio/reverse/v2r4_build_package.py` (7aef91b + 9c32ae6). Gates, thresholds, strata, F-26 whitelist/guard and the claim-exclusion rule are unchanged.
- **New secrets:** a new secret seed (new SHA-256 commitment), new nonce, new stage-B and scoring-key passphrases, and 4 fresh decoys not used in rounds 1–4.
- **No overlap:** 4b samples must not overlap rounds 1–3 items, the seg-v3 tuning exclusions (±2 s), or the voided round-4 stage-A items (A1 ±0.5 s, A2, A3, A4). The only builder change is an exclusion-only option `--exclude-stageA <template>` that reads the voided round's public stage-A template (never its answers) and adds those intervals to the exclusion list. Sampling, labelling and scoring code are untouched.
- **Paths:** package `/workspace/afp-private/v2_review_package_r4b/`, sealed key `/workspace/afp-private/v2r4b_oracle_sealed/` (mode 000; the file keeps the builder's name `oracle_key_r4.json.enc`).
- **Secret custody (F-36 fix):** passphrases exist only in memory and in the builder's final text report to the owner; not in any file, log, shell history or Drive. Item ids (W/U/C/R/claims) reuse the builder's prefixes; 4b items are identified by the 4b seal record.
- Verdict cap unchanged: Grok Bot reviewer = same identity (F-12) → INCONCLUSIVE (agent review).
