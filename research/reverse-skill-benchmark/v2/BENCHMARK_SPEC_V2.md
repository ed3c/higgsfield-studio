# Higgsfield Creator Image-Reverse Benchmark v2.0

- **Date:** 2026-11-23 (Asia/Taipei)
- **Scope:** @tupacabra-inspired *research*, not copying a protected finished film
- **Owner:** Image Research Manager
- **Consumers:** Director Manager, Prompt Compiler, Creator Intelligence, Film Production Manager
- **Independent Oracle:** fixed source/reference evidence, website cost proof, blinded evaluators, deterministic validation
- **State:** `BLOCKED_ENTITLEMENT_RECHECK` / `NOT_RUN`
- **Integration target:** `ed3c/higgsfield-studio` Draft PR #4; this v2 package does **not** edit that PR or main.

## 0. Accepted decisions and correction log

1. The generation surface is the logged-in **higgsfield.ai website, ordinary model-generation page**, not MCP/CLI/API/Canvas/Marketing Studio/Presets. Use the website's *Unlimited* control only if the exact request displays 0 incremental credits.
2. The user-provided Subscription screenshot lists GPT Image 2.6, GPT Image 2.6 Flare, Nano Banana Pro, Seedream 5.0 Pro and several plan-included Unlimited models, all with `Nov 20, 2026` displayed. The screenshot has no visible date-column header: **do not assign it to `expires_at` or `activated_at`**. Since today is Nov 23, recheck website entitlement before generation; treat screenshot as historical/ambiguous evidence, not an active entitlement certificate.
3. Official website documentation: Unlimited applies only to supported generation settings on higgsfield.ai; MCP, CLI, Canvas, Supercomputer, Marketing Studio spend Credits. Unlimited toggle must be enabled. https://higgsfield.ai/blog/higgsfield-7-day-unlimited-bonus and https://higgsfield.ai/pricing
4. A previous connector read returned Ultra and 9,010 normal Credits, but `free_trial.unlim_available=false` for MCP. This **does not disprove** a separate website Subscription allowance. Conversely, website Subscription does not authorize free MCP generation.
5. V1 is immutable historical evidence (`NOT_RUN / FREE_IMAGE_NOT_AVAILABLE` for MCP). V2 supersedes the proposed execution route, **not** the historical result. Never claim an actual winner until images and blind scores exist.
6. Zero incremental generation Credits is a marginal-cost constraint, not a claim that the subscription itself costs nothing.

## 1. Objective and falsifiable hypotheses

- **R1 — Reconstruction:** Which reverse Skill best describes the *observable* structure of a source still in a text-only prompt (composition, perspective, light, palette, material, artifacts)?
- **R2 — Style transfer:** Can the Skill carry over visual grammar while substituting a fixed *new, original* subject, without copying source identity or branding?
- **Secondary:** Are prompt outputs traceable, well structured, editable, usable across shot cards, and cost-effective? This is a workflow assessment, **not** part of image-quality blind scoring.

The experiment compares **Skills generating prompts**, not image models. No reference still may be attached to Higgsfield render (no image-to-image), otherwise the model could bypass the reverse-Skill prompt.

## 2. Candidates and role boundaries

| ID | Repo | Expected task specialization | Strict handling |
| --- | --- | --- | --- |
| `unimage` | https://github.com/huanmu-team/unimage | reconstruction + optional repair | extract **first draft prompt only** in R1; repair tested separately |
| `caph` | https://github.com/Caph-dev/image-style-prompt-reverse-engineer | style grammar; subject removal | do not punish subject abstraction in R2 |
| `niobium617` | https://github.com/niobium617/prompt-reverse-engineer-skill | descriptive analysis + prompt compilation | use fixed target model adapter, no hidden extra reference |

Pin each repo to a commit SHA. Audit `SKILL.md`, all called scripts, licenses, external API requirements and outbound network permissions. Do not run unreviewed installation scripts on production machines; use a sandbox with read-only references and no unrelated credentials. If a candidate requires a paid external model, mark `DEPENDENCY_BLOCKED` and do not silently substitute another model.

## 3. Reference selection and rights

Prepare 3 reference stills with distinct shot classes:

- `C01`: portrait/character with intentional foreground-background separation
- `C02`: environment/establishing shot with distinct vanishing point, lighting and set geometry
- `C03`: prop/action composition with a strong silhouette or scale contrast

Record `source_url`, `timestamp_in_video_ms` (if applicable), `capture_method`, `local_sha256`, `aspect_ratio`, `analysis_rights_scope`, `third_party_upload_allowed` and `notes`. Use 16:9 images or document a deterministic, shared crop before SHA-256. Do not commit reference media to Git. Do not send reference stills to a third-party vision provider without permission or another valid authorization for that transfer.

ScrapeCreators optional research path: `creator-profile-teardown -> outlier-post-finder -> comment-mining -> visual_candidates.json`. Requires separate ScrapeCreators API access. **No API key** is not a blocker if three properly sourced research stills are already available; no post-lift claims without a real sample.

## 4. Entitlement Gate G0 — fail closed before any render

1. Open the authenticated **higgsfield.ai** ordinary image generation page in the relevant user's website session (not CLI/MCP/Canvas).
2. Navigate **Manage Account -> Subscription -> Active unlimited models**; capture fresh evidence with date/time and the full column label that explains `Nov 20, 2026` if visible.
3. Select `GPT Image 2.6` (not Flare), **1K, 16:9**, and a quality allowed by the live website's offer. Set *Unlimited* ON. Record model variant, mode, UI labels, resolution and expiry if available. Do not infer the expiry from an unlabeled date.
4. Check actual submission preview/cost indicator reads **0 Credits** / Unlimited with no warning that a paid path will be used. Check current balance snapshot. If the UI instead requires credits, says expired, has missing Unlimited, or switches to a paid surface: **STOP** with `BLOCKED_ENTITLEMENT_RECHECK` or `EXPIRED_OR_PAID`; no generation.
5. If GPT Image 2.6 not covered, predeclare `Nano Banana Pro` as a fallback **only if it independently passes the same website 0-credit gate**. Restart as a distinct run/version; do not mix models within one scored batch. If both unavailable, test a plan-included website model such as Nano Banana/FLUX.2 Pro only as a **separate** run with correctly documented limits, or remain NOT_RUN.
6. Before every submit, verify toggle and amount again. Confirm credit balance unchanged *after* generation; if any unexpectedly charged, abort, log discrepancy, do not auto-retry or request refunds without authorization.
7. Unlimited can have shared concurrency/queue limits. To eliminate rate and queue biases, submit **serially**, randomizing candidate order within each case; do not launch parallel jobs.

**No preflight verification via MCP balance replaces the website proof.** Never upload secrets, cookies, user session data or billing screenshots to the public repository.

## 5. Execution protocol — 30 core images

### Phase P0 — Prompt lock (zero Higgsfield spend)

For each case and each candidate, run the reverse Skill once with identical source image, common task brief and fixed analysis-time budget. Save:

- `raw_prompt.md` (unmodified Skill output)
- `normalized_prompt.txt` (only deterministic model-syntax removal, no creative rewrite)
- `prompt_diff.md` (every normalization and reason)
- `skill_commit`, runtime/dependencies, provider/model used for semantic inference, prompt hash, evidence links, failures and token/API cost

One prompt per `(case, skill, task)`, reused for both replicate renders. All candidates use the same model-agnostic task brief; no human prompt polishing before benchmark completion.

### Phase P1 — Reconstruction: 18 images

`3 refs x 3 skills x 2 replicates = 18`.

- Target: reconstruct source image's visible geometry and visual properties from text alone.
- Inputs: source still to reverse Skill, **no source image to Higgsfield render**.
- Controls: fixed image model, website 0-credit entitlement, 1K, 16:9, same accessible quality tier, and same subject-level constraints. If web UI supports seed, record it; do not assume it does.
- Randomize the order of Skill submissions within each case to reduce time-dependent backend drift.
- Freeze each exact prompt and preserve all outputs; no selection of prettier takes for grading.

### Phase P2 — Style transfer: 12 images

`3 refs x 2 candidates x 2 replicates = 12`.

- Candidate A **must be `caph`** (specialized in subject-independent style extraction).
- Candidate B is the **highest-scoring eligible non-Caph Skill in P1**, predeclared by its P1 result after P1 scores lock. If none eligible, mark P2 NOT_RUN.
- New replacement subject, story context, camera constraints and banned source-specific motifs are **fixed before P1** for each case. They are the same for both P2 candidates.
- Judge *style retention + successful subject change*, not pixel similarity to source. No original character/brand/text/watermark replication.
- **Selection-bias disclaimer:** P2 compares two chosen candidates. A candidate excluded from P2 is **not** considered proven worse at style transfer. For a global 3-way style ranking, run the omitted candidate under the same P2 settings as an explicit extension.

### Optional P3 — Cross-model robustness (not part of primary result)

Secondary model Nano Banana Pro, if 0-credit web eligible; use identical prompts for top two on all three references with one render each (`3 x 2 x 1 = 6`). Analyze model-by-skill interaction, report separately. Never pool across image models in primary scores.

### Optional P4 — Repair efficacy (separate metric)

For failed cases only, allow Unimage's repair stage and an equivalently budgeted competing repair method. Count cycles, prompts, outputs and additional time. Do not retrospectively replace initial P1 results.

## 6. Artifacts and evidence contract

Expected paths (repo stores small text/CSV/JSON only; generated media stored outside Git):

```
research/reverse-skill-benchmark/v2/
  BENCHMARK_SPEC_V2.md
  manifest_v2.json
  prompts/{task}/{case_id}/{skill_id}/raw_prompt.md
  prompts/{task}/{case_id}/{skill_id}/normalized_prompt.txt
  generations.csv
  ratings.csv
  adjudication.md
  REPORT.md
  NOT_RUN.md              # only if blocked / partially blocked

# external or gitignored
artifacts/reverse-benchmark-v2/{run_id}/
  refs/
  output/
  entitlement-evidence/
```

For every render, record `run_id`, task, case, skill, replicate index, blind image ID, source SHA256, prompt SHA256, source-model settings, web URL/job ID where available, submitted/completed timestamps, `unlimited_enabled`, cost shown at submit, credit balance before/after (private), generated media SHA256 and local artifact path. If UI does not expose a job ID, record `not_exposed` plus screen evidence and timestamp; do not fabricate IDs.

Keep identifiable account screenshots private. Public GitHub manifest can say `verified=true` and include only a hash/opaque evidence ID; do not publish billing data or login cookies.

## 7. Independent Evals and decision oracle

Blinding: shuffle filenames/labels to `B0001..B0030`; keep the `blind_id -> skill` mapping sealed until scores lock. Both reviewers independently score every image on a **0–5** anchored scale:

- `0` broken / unrelated; `1` poor; `2` weak; `3` acceptable; `4` strong; `5` excellent.
- P1 weighted criteria: `composition .25`, `perspective .20`, `lighting .15`, `palette .10`, `material .15`, `artifact_control .15`.
- P2 weighted criteria: `style_dna .25`, `new_subject_integrity .25`, `composition .15`, `lighting .15`, `palette .10`, `artifact_control .10`.

`hard_fail` conditions: major malformed geometry/anatomy, unrelated scene, source-specific protected identity copied to P2, or significant watermark/text leakage. Report failure rates separately: do **not** hide these inside means.

For each image: compute weighted score per reviewer; mean both reviewers. Aggregate per case across both replicates; then mean across 3 cases. Compare paired `(same case, replicate)` differences and ranges; never claim statistical significance from 3 reference cases. Include per-criterion scores, deviations and reviewer disagreement (e.g. difference >2 on a criterion requires adjudication, while retaining both original scores).

Decision: report P1 and P2 winners separately only after all required samples, metadata and two independent reviewer scores exist. If score differences are small/discordant, label `INCONCLUSIVE` and prefer interoperable tools. Also give non-score engineering comparison: repeatability, dependencies, token/API cost, quality of evidence, rights compliance, and task relevance.

## 8. Gates and NOT_RUN semantics

| Gate | Pass evidence | Fail behavior |
| --- | --- | --- |
| G0 Rights/Source | 3 image sources + hashes + research/upload scope | `BLOCKED_SOURCE` |
| G1 Web entitlement | current website confirms correct model + Unlimited ON + 0-credit path | `BLOCKED_ENTITLEMENT_RECHECK` / `EXPIRED_OR_PAID` |
| G2 Skill reproducibility | pinned commit, audited scripts, exact prompts for all P1 cells | `BLOCKED_SKILL` |
| G3 P1 generation | 18 real images, uniform model/settings, exact job evidence | `PARTIAL_P1` (no P1 winner) |
| G4 P1 independent eval | 2 independent blind reviewers for all 18 | `PARTIAL_EVAL` |
| G5 P2 generation/eval | 12 real images, Caph + selected competitor, independent blind eval | `PARTIAL_P2` (no P2 winner) |
| G6 Final report | provenance, score tables, cost reconciliation, limitations | no unqualified winner |

Status transition: `NOT_RUN -> BLOCKED_ENTITLEMENT_RECHECK -> ENTITLED_WEB_VERIFIED -> PROMPTS_LOCKED -> P1_COMPLETE -> P1_SCORED -> P2_COMPLETE -> COMPLETE` (or a terminal/partial blocked state). Never set COMPLETE based only on a README, estimated pricing, a screenshot from an earlier date, or an agent's intuition.

## 9. What counts as success

- All **30** core images produced on an identical web model with recorded **zero additional Credits** (or explicitly flagged partial/not-run).
- No unverifiable data or synthetic benchmark scores.
- An auditable P1 recommendation (reconstruction) and P2 recommendation (style-transfer among the two entrants); where uncertain, report inconclusive.
- Reusable `Visual Style Bible` + `Shot IR` suggestions that can be used for **original** film creation, without unauthorized reproduction of finished source work.

## 10. Source references

- Official website entitlement/limits: https://higgsfield.ai/blog/higgsfield-7-day-unlimited-bonus
- Official distinction between web and MCP/CLI: https://higgsfield.ai/pricing
- 11.11 promotions (duration differs by plan): https://higgsfield.ai/blog/higgsfield-11-11-deals
- ScrapeCreators: https://github.com/ScrapeCreators/social-media-research-skills
- Original v1 draft: https://github.com/ed3c/higgsfield-studio/pull/4
