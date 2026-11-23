# NOT_RUN — run-20261123-grokbot-01 (2026-11-23, Asia/Taipei)

**Benchmark: `BLOCKED_SOURCE`. 0 jobs submitted, P1 0/18, P2 0/12, 0 additional Credits, no scores, no winner.**

Exact missing evidence, in dependency order:

1. **G0 — reference stills (MS-004).** `manifest_v2.json` cases C01/C02/C03 have `url=null`, `sha256=null`, `analysis_rights=UNVERIFIED`, `external_provider_transfer_allowed=false`. The @tupacabra NUREMBERG trailer was *located* (X post `2121357879341166683`, via secondary sources) but not opened, captured or hashed. Sending a third-party frame to a hosted vision model (which every reverse Skill needs) is permission (B) in scope §7 and is `UNKNOWN`, so this run did not do it.
2. **P0 — prompt lock.** Without G0 no Skill can run, so 0/9 P1 prompts and 0/6 P2 prompts exist. The 30 job slots in `job_slots.json` carry `prompt=null` on purpose. No prompt was written by hand.
3. **P2 subjects (MS-008).** Must be frozen before P1. A proposal exists (`p2_subjects_PROPOSED.json`) and needs owner approval.
4. **G1 — live entitlement.** Not rechecked by this run (it has no browser step here). PR #5's observation says GPT Image 2.6 Unlimited expires **2026-11-27**; after that the benchmark becomes `EXPIRED_OR_PAID` unless a new allowance is verified.

Nothing in v1, the v2 spec pack, PR #5, or `research/*.json` was modified.
