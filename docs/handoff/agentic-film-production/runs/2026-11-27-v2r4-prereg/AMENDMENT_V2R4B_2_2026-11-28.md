# RUBRIC_V2R4 — round 4b amendment 2 (2026-11-28, before the 4b build)

This adds to `AMENDMENT_V2R4B_2026-11-28.md` (95a4f56) and `BUILD_BLOCKED_V2R4B_2026-11-28.md` (3818069); both stay unchanged.

**Owner decision:** Neon, widget answer to t40s460 (2026-11-28): 「允許和作廢的第四輪重疊，換新的審查 agent 重建第四輪」 — allow overlap with the voided round-4 stage-A items and rebuild round 4 with a fresh reviewer agent.

**Relaxation (only this):** the exclusion of the voided round-4 stage-A items is dropped. Justification: round-4 stage B was never released, its passphrases do not exist, and the partial round-4 answers are quarantined unread (`VOID_V2R4_2026-11-28.md`, F-36). The 4b reviewer is a fresh agent that has not seen round 4.

**Unchanged:** exclusions of rounds 1–3 items and the seg-v3 tuning/control data (±2 s); RUBRIC_V2R4 gates, thresholds and strata; scorer; builder (7aef91b + 9c32ae6; the 95a4f56 `--exclude-stageA` option is simply not used); F-26 whitelist/guard; new seed, nonce and secrets; 4 fresh decoys; package `/workspace/afp-private/v2_review_package_r4b/`, sealed key `/workspace/afp-private/v2r4b_oracle_sealed/` (mode 000); passphrases only in the builder's final text report; F-12 cap (INCONCLUSIVE, agent review).
