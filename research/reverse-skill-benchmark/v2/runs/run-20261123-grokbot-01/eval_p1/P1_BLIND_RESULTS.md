# P1 blind results (Reconstruction), run-20261123-grokbot-01 — 2026-11-23 ~20:40 Asia/Taipei

## Chain of custody
1. **Sheets.** The orchestrator reported that R1 and R2 completed their reviews independently, each reading only `/workspace/hs-bench-review/p1-blind/`. The executor verified the sheet hashes against the values reported:

   | sheet | sha256 |
   | --- | --- |
   | `scores_R1.csv` | `be54f458…04f2` ✓ |
   | `scores_R2.csv` | `b2e4a0f5…a1a7` ✓ |

   Each sheet has 102 rows (17 images × 6 criteria) and no hard fails. The blank `ratings_R*_TEMPLATE_empty.csv` files are kept unchanged.
2. **Lock before unsealing.** Both sheets were committed to the repo **before** the key was opened, in commit `31e5bd6`.
3. **Key.** The sealed key's sha256 was verified as `0a49df5e…64fe` ✓, then unsealed. The key is published as `blind_key_UNSEALED.json`; it contains only job IDs and hashes, no private data.
4. **Aggregation.** `compute_p1_scores.py` was run unchanged (sha256 `e3985503…94c7`, committed at `816cc81`, before any score existed). Output: `P1_RESULT_compute_output.json`.

## Per-Skill weighted scores (0–5, spec §7 weights, mean of R1 and R2, averaged over replicates)

| Skill | C01 portrait | C02 car POV | C03 flying wing | mean over cases | range | hard fails |
| --- | --- | --- | --- | --- | --- | --- |
| **niobium617** | **3.750** | **2.600** | **4.088** | **3.479** | 1.488 | 0 |
| unimage | 3.650 | 2.475 | 4.000 (1 replicate, GAP-P1-01) | 3.375 | 1.525 | 0 |
| caph | 3.300 | 2.350 | 3.775 | 3.142 | 1.425 | 0 |

- **Point ranking:** niobium617 > unimage > caph.
- **By case:** every Skill scored lowest on C02, which is consistent with the look-gap analysis (bright golden-hour postcard against a dim, overcast reference). C03 was the easiest case.

## Pre-registered decision rule (fixed in `EVAL_SETUP.md`, commit `816cc81`; not changed)
"The leading non-Caph Skill becomes B only if its mean exceeds the other by **≥ 0.25** **and** it leads in **≥ 2 of 3 cases**; otherwise `INCONCLUSIVE`."

| check | value | pass? |
| --- | --- | --- |
| mean gap, niobium617 − unimage | **0.104** | ✗ (< 0.25) |
| cases led by niobium617 | 3/3 | ✓ |

**→ P1 outcome: `INCONCLUSIVE`. No P1 winner.** The result is also PROVISIONAL because of GAP-P1-01: the C03 × unimage cell has a single replicate after the moderation refusal of job 15.

Descriptive sensitivity checks (`sensitivity_descriptive_only.json`) do not change the rule's outcome:
- Replicate 1 only: gap 0.083, niobium617 leads 2/3 cases.
- Excluding C03: gap 0.112, leads 2/2.

Both remain INCONCLUSIVE.

## Inter-rater agreement (`agreement.json`)

| measure | value |
| --- | --- |
| exact agreement | 85.3% |
| within 1 point | 100% |
| mean absolute difference | 0.147 |
| maximum absolute difference | 1 |
| quadratic-weighted κ | **0.888** |
| image-score Pearson | 0.981 |
| image-score Spearman | 0.936 |
| ICC(2,1) absolute | **0.950** |
| adjudication flags (difference > 2) | 0 |

- **Bias by criterion** (R1 − R2): material +0.35, composition +0.24, lighting −0.12, palette −0.12, perspective 0, artifact_control +0.06.
- **Caveats** (recorded, not used to change anything):
  - Both reviewers scored the two replicates of a cell **identically on all 6 criteria in 6/8 pairs**, so within-cell discrimination was low.
  - The reviewers' identities and isolation details (human or model, which model, separate contexts) were **not supplied** to this executor. This is GAP-EVAL-01.
  - Agreement this high is consistent with real agreement, but also with correlated reviewers. Treat independence as **reported, not verified**.

## Non-score engineering comparison (spec §7)
- **niobium617:** deterministic local scripts (`analyze_image.py`, compiler) plus a semantic layer. It produces the most structured output. Its scripts ran with networking disabled.
- **unimage:** a Markdown-only Skill; compact prompts. Its C03 prompt triggered one moderation refusal (job 15), even though the identical prompt succeeded on job 18.
- **caph:** a style-grammar Skill. It strips the subject and needed one deterministic placeholder removal. Lowest reconstruction scores, which is expected: it is designed for style rather than reconstruction (spec R2).
- **All three:** MIT licence, pinned SHAs. Static script audit is still `audited=false`.
- **Owner oracle:** Neon (t31u) judged **style fidelity FAIL** for the whole P1 batch, composition only. The blind rubric scores composition, perspective, lighting, palette, material and artifacts. Its "acceptable–strong" mid-range scores do not contradict Neon's look verdict, which the rubric does not isolate.

## P2 pairing: what the locked spec says
- **Spec §5:** "Candidate B is the **highest-scoring eligible non-Caph Skill in P1**, predeclared by its P1 result after P1 scores lock. **If none eligible, mark P2 NOT_RUN.**"
- **Spec §7:** "If score differences are small/discordant, label `INCONCLUSIVE`…"
- **Pre-registration (EVAL_SETUP):** B is set only if the ≥ 0.25 / ≥ 2-case rule passes; otherwise candidate B = `INCONCLUSIVE`.

**Determination under the locked rules:** no eligible candidate B was established. **P2 = `NOT_RUN` (blocked: `P2_CANDIDATE_B_INCONCLUSIVE`).** This executor does not override that.

**Options that need an explicit owner decision.** Each would be recorded as a deviation; none is taken here.
1. **Keep P2 NOT_RUN.** This is the strict spec outcome.
2. **Owner override, literal "highest-scoring":** run Caph vs **niobium617**. niobium617 is the point leader, ahead in 3/3 cases, but by only 0.104 against the 0.25 bar. 12 renders, labelled `P2_PROVISIONAL_OWNER_OVERRIDE`. Its P2 result cannot back-validate P1.
3. **Owner override, include both non-Caph Skills:** Caph + niobium617 + unimage = 3 × 3 × 2 = **18 renders**, instead of 12. This deviates from the 30-image budget, but avoids picking a B on a non-significant gap. It also honours the brief's "do not treat the non-entrant as a style loser".

Before any P2 run:
- re-check Unlimited / 0 credits live (expiry observed 2026-11-27);
- use the approved P2 subjects (`p2_subjects_APPROVED.json`);
- run a separate blind review.

## Gate effects
- **G3:** `PARTIAL_P1` (unchanged).
- **G4 P1 blind eval:** **`P1_SCORED_INCONCLUSIVE`** (2/2 reviewers, 17/17 images).
- **G5:** `NOT_RUN`, because candidate B is inconclusive.
- **P1 winner:** none.
