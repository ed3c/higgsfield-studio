# Creative Research Scope — Complete Conversation Handoff

- **Contract ID:** `higgsfield-creative-research-scope-v1`
- **Scope captured:** 2026-11-23 (Asia/Taipei)
- **Repository:** https://github.com/ed3c/higgsfield-studio
- **Primary benchmark:** [BENCHMARK_SPEC_V2.md](BENCHMARK_SPEC_V2.md), [manifest_v2.json](manifest_v2.json), [EXECUTION_PROMPT.md](EXECUTION_PROMPT.md)
- **Downstream consumer:** dot / Codex / Creator Research Managers / Film Factory Managers
- **Status:** `SCOPE_DEFINED`; **not** `RESEARCH_COMPLETE` or `BENCHMARK_COMPLETE`
- **Principle:** preserve original creator/artwork context with explicit source and uncertainty. Do not silently shrink this research program to three reverse-image Skills.

## 0. Authority, evidence, and precedence

1. This file defines the **long-lived, cross-creator creative-research scope** and handoff coverage. The v2 benchmark files continue to govern **the fixed 30-image experiment**, scoring and website-only 0-credit generation.
2. The underlying canonical research inventory is `research/creators.json`, `research/creators.csv`, `research/profiles_raw.json`, `research/prompt_libraries.json`, plus `creators/index.md` and `creators/study-queue.md`. The repository describes **79 listed creators** as of 2026-11-21; this is a historical inventory, **not a claim that every creator has been fully analyzed**.
3. This file consolidates creator/artwork names and resources explicitly discussed in the current conversation together with the checked repository. Where a claimed award, creator attribution, tool support, license, URL, audience metric or technique was mentioned in conversation but not independently established, retain it as a **research target / claim requiring verification**, not an established observation.
4. dot may **not** have access to the complete original ChatGPT conversation or attachments. Do not claim that it does. Use the current repository as a first durable index; require a `coverage_gap` entry for any referenced chat material or media that the agent cannot actually retrieve. Do not infer that missing assets were analyzed.
5. If the user provides further materials in future conversations, add them incrementally with source ID, batch ID and coverage status. **Never silently omit any user-supplied creative reference**; missing access means `MISSING_SOURCE`, not deletion.
6. Keep a four-way distinction: `SOURCE_EVIDENCE` (direct artifact), `MEASURED` (instrument readings), `INFERRED` (agent interpretation), `UNVERIFIED_CLAIM` (unconfirmed statements). Prompt/model/seed actually used by a creator cannot be known merely by visual inspection.

## 1. Mandatory creator and artwork inventory

These are **named coverage obligations**. A person, studio, artwork or URL must have a stable individual record, sources and analysis status. Do not collapse creators into works or treat associations as interchangeable.

| Coverage ID | Creator/studio or source | Artwork, practice or contribution to study | Starting evidence / verification |
| --- | --- | --- | --- |
| CR-TUPACABRA | [@tupacabra](https://x.com/tupacabra) | `NUREMBERG` AI cinematic trailer; other publicly accessible works; science-fiction trailer visual grammar, hook, cut rhythm, cinematography, sound | User supplied X handle; locate exact posts/versions and record IDs; technical tool attributions remain unverified until sourced |
| CR-ROCOCO | `rococo_table_radical` | `Listen to Meh`: humor, cinematic composition, narrative arc, sound | [Higgsfield festival winners](https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=winners); see `creators/study-queue.md` |
| CR-PURGA | PURGA Studio and named collaborators in existing research | `Lorem Ipsum`; professional studio workflow, character/world-first approach, ads and narrative | `creators/study-queue.md` and referenced sources; preserve attribution to `Listen to Meh` as documented and reconcile studio/person/award roles with provenance |
| CR-AIST | `aist` | `Fukushima`: realism, facial performance, catastrophe and sound | Festival winners and [Higgsfield profile](https://higgsfield.ai/@aist) |
| CR-ZACK | `zackmmurray` | `The Field Agent`: concept, story structure, film execution | Festival winners; verify work/handle linkage |
| CR-JOEY | `JOEY / joeysnoisygroup` | Story Bible, Castkit, Scenecraft, Shotcaller, Motiondojo; teachable filmmaking pipeline | [Public creator profile](https://higgsfield.ai/@joeysnoisygroup) and `creators/study-queue.md` |
| CR-TSEILY | Tseily | Cinematic daily-life transformations | Existing study queue; [profile](https://higgsfield.ai/@tseily) |
| CR-ALEKSANDRA | Aleksandra | Fashion/editorial visual direction and art instruction | Existing study queue; [profile](https://higgsfield.ai/@aleksandra) |
| CR-YOAV | Yoav Yariv | `Soulless`: human/machine sci-fi narratives | Existing study queue; [profile](https://higgsfield.ai/@yoav_yariv) |
| CR-AUTHORS | Authors First | Literary storyboard-to-video process | Existing study queue; official case study link therein |
| CR-TAMBV | TAMBV | `GIRLS / DEMONS`; fashion, animation, music video | Existing study queue; [profile](https://higgsfield.ai/@tambv) |
| CR-ONEOFONE | One of One Studio | Licensed apparel + brand world-building | Existing study queue; official case study links therein |
| CR-BOXEL | Boxel Studio | Previsualization, VFX studio workflow, multiple video-model coordination | Existing study queue; official case study links therein |
| CR-MORE | All other records already in `research/creators.json` | Full existing **79-creator inventory**, overlapping domain tags and additional artwork | Read each source record; preserve stable row-level source links and verification status, and do not replace with a short curated list |

The ten-person `creators/study-queue.md` is a **prioritized teaching selection**, not the full research scope. The conversation's named `The Field Agent` and @tupacabra still need distinct records even if absent from the historical top-ten queue. Do not fabricate full 79-person coverage without enumerating actual JSON entries.

### Additional supplied creative references

All user-supplied stills, trailer clips, film references, music, prompts, code, videos, screenshots, source files, creator links and references from **this or later conversations** belong in the inventory. The user explicitly wants **reverse-analysis of every supplied creative resource**. Failure to locate an attachment must be represented as `MISSING_SOURCE` with user-visible gap evidence, not as a non-required task.

An image showing a subscription/Unlimited entitlement is **billing evidence**, not a cinematic reference; keep such evidence private and separately keyed by hash.

## 2. Domain taxonomy (cross-disciplinary, not merely AI image prompts)

The system must support `art`, `fashion`, `film`, `literature`, `tech`, `scifi`, `music-video`, `ads`, `shorts`, `daily-life`, `social-distribution`. A creator may belong to several domains. Production studies must track:

- Narrative / Story / emotion / hooks / dramatic structure
- Art Direction / color / costume / set / materials / world building
- Cinematography / shot size / lens hypothesis / composition / camera geometry / motion
- Character / location / prop continuity across shots
- Image-to-Prompt reconstruction and transferable style grammar
- Video reverse analysis (cuts, beats, shot graph, optical motion, sound)
- Audio / voice / music / sound design / mix and pacing
- Higgsfield Studio workflows: Soul, AI Cast, Elements, Cinema Studio, Genjutsu, Canvas, official Skills (record availability and paid/free execution surface separately)
- Social research: TikTok, Instagram, YouTube, Reddit, X, LinkedIn; outliers, audience questions, reactions and content formats
- Production QC, independent blinded evaluation, regression / verification, versioning, model/vendor cost
- Distribution versions, original IP, creator business and monetization research

## 3. Referenced open-source Skills and engines (candidate catalogue; not performance winners)

Preserve references to **all** these discussed tools as candidate dependencies; read up-to-date `SKILL.md` / scripts and pin SHA/license before executable use:

| Stage | References |
| --- | --- |
| Social discovery and transcripts | [ScrapeCreators/social-media-research-skills](https://github.com/ScrapeCreators/social-media-research-skills), [browser-act/skills](https://github.com/browser-act/skills), [hoodini/ai-agents-skills](https://github.com/hoodini/ai-agents-skills), [TubeLabHQ/youtube-research-skills](https://github.com/TubeLabHQ/youtube-research-skills) |
| Still reverse benchmark (fixed v2 candidates) | [huanmu-team/unimage](https://github.com/huanmu-team/unimage), [Caph-dev/image-style-prompt-reverse-engineer](https://github.com/Caph-dev/image-style-prompt-reverse-engineer), [niobium617/prompt-reverse-engineer-skill](https://github.com/niobium617/prompt-reverse-engineer-skill) |
| Video reverse | [dotslashsimran/simcraft](https://github.com/dotslashsimran/simcraft), [LunarXuan/video-prompt-reverse](https://github.com/LunarXuan/video-prompt-reverse), [SamurAIGPT/rea-video-turbo](https://github.com/SamurAIGPT/rea-video-turbo), [kevinbadi/open-edits](https://github.com/kevinbadi/open-edits), [shivam098/video-deconstructor](https://github.com/shivam098/video-deconstructor), [brenoepics/video-to-skill](https://github.com/brenoepics/video-to-skill) |
| Viral / multi-film research | [creatify-ai/video-ad-reverse-engineer](https://github.com/creatify-ai/video-ad-reverse-engineer), [kennyzheng-builds/seek-and-analyze-video](https://github.com/kennyzheng-builds/seek-and-analyze-video) |
| Film directing and assembly | [wuwangzhang1216/DirectorSKILL](https://github.com/wuwangzhang1216/DirectorSKILL), [nigo-studio/ai-film-skills](https://github.com/nigo-studio/ai-film-skills), [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills), FFmpeg/ffprobe, PySceneDetect; optional depth and motion trackers subject to license audit |

Skill compatibility, model versions, commercial use and accuracy are **claims to test**, not verified by listing a repo here. A reference code repo's license does not automatically grant rights to media used by its demos or to model weights.

## 4. Production Managers, contracts and interaction graph

Minimum responsibilities (may combine internal agents but **must retain distinct contract ownership**):

| Domain Manager | Producer input → output contract | Consumer | Independent Oracle / gate |
| --- | --- | --- | --- |
| Creator Intelligence | Source URLs / media / metrics → creator, artwork, audience and outlier registry | Story + Research | Source IDs, capture timestamps, deduplication, baseline/sample confidence |
| Provenance / Rights | Supplied files + creator claim → permission/research-use flags, hashed provenance and gaps | All stages | Exact source linkage, access/usage scopes, no false authorship |
| Narrative / Script | Creator studies + original brief → Logline, Story Bible, beat sheet | Director, Audio | Director approval, identifiable original narrative |
| Art Direction | References + script → Visual Style Bible, palette, lighting, costumes | Shot / Prompt | Style samples tied to evidence; reproducible style rules |
| Character / World | Approved concepts → Character/Location/Prop Bibles, continuity IDs | Shot Production | Appearance and location continuity checks |
| Cinematography / Motion | Story + styles + references → Shot IR, camera and movement hypotheses | Image/Video Prompt | Raw timecode/evidence, physical plausibility labels, shot-level constraints |
| Image / Prompt Compiler | Shot IR + style + selected reverse Skill → exact, versioned image prompt | Website generation | Deterministic prompt freeze, hash, task constraints |
| Video / Editing / Audio | Shot IR + selected takes → picture edit, motion, sound and platform variants | Master + Distribution | Cuts/timecode/beat metrics, audio checks, continuity |
| Generation / Cost Ops | Approved prompt + model + entitlement → job evidence and media hash | Evals + Post | Zero-credit website proof, credit deltas, job provenance |
| Independent Evals / Verification | Original references + blinded takes → score, hard fails, adjudication | Director + Knowledge | Independent ratings, paired cases, regression matrix |
| Knowledge / Registry | All verified artifacts + decisions → linked reusable Skill/Style Bible/lessons | All managers | Source→Contract→Producer→Consumer→Oracle completeness |
| Distribution / Market | Approved master + public trend evidence → X, IG, TikTok, YouTube formats and review | Publishing | Platform specs, ownership/usage rights and engagement evidence |

**Cross-manager dataflow (conceptual DAG):**

```text
Raw creator works / user attachments / public posts
  -> [Creator Intelligence] <-> [Provenance & Rights] -> [Research Registry]
  -> [Narrative] <-> [Art Direction] <-> [Character & World]
  -> [Director / Shot IR] -> [Image & Video Prompt Compiler]
  -> [Generation & Cost Ops] -> [Independent Evals]
  -> [Video Editing / Sound / Post] -> [Director Approval]
  -> [Distribution & Audience Feedback]
                        `-> [Knowledge / Regression / Skill improvements] -> next experiment
```

A Manager handoff must record `source_ids`, `producer`, `consumer`, `contract_version`, `oracle`, `decision`, `uncertainty`, `NOT_RUN` obligations. Evaluation regressions cannot erase original human decisions or source evidence.

## 5. Data records and storage policy

Do not move or overwrite `research/creators.json`, `profiles_raw.json`, `prompt_libraries.json`, previous v1 benchmark, historical experiment manifests or output evidence. Append new batch-specific research:

```text
research/live/creator-intelligence/<date>-<creator>/...
research/creator-artwork-registry/<batch-id>/creators.jsonl
research/creator-artwork-registry/<batch-id>/artworks.jsonl
research/creator-artwork-registry/<batch-id>/sources.jsonl
research/creator-artwork-registry/<batch-id>/coverage_gaps.md
research/reverse-skill-benchmark/v2/...             # original v2 spec/manifest remain intact
research/reverse-skill-benchmark/v2/runs/<run-id>/... # append actual execution evidence only
```

Minimal registry fields: `creator_id`, `artwork_id`, `source_id`, `source_url`, `provided_by_user`, `media_kind`, `capture_timestamp`, `original_work_link`, `reference_asset_sha256` (when available), `domain_tags`, `claim_type`, `confidence`, `analysis_status`, `use_scope`, `rights_status`, `consumer_ids`, `provenance_notes`. Give work and creator distinct stable IDs; never rely on display names alone.

Public GitHub stores schema, analysis, citations, prompt metadata, evidence hashes, NOT_RUN records and small artifacts only. Raw copyrighted media, generated high-resolution outputs, sessions/cookies, API keys and private billing/identity evidence stay in authorized private storage, referenced by opaque IDs and checksums; honor the repo's `.gitignore` and storage rules.

## 6. Separate completion gates (must never be conflated)

### G-R: Research Completeness Gate

- Enumerate all **79 existing creator records** without inventing new entries; preserve the per-record provenance and confidence.
- Confirm named creator/artwork requirements in §1 are linked or explicitly marked `MISSING_SOURCE` / `NOT_YET_ANALYZED` / `NEEDS_VERIFICATION`.
- Inventory all sources supplied in the available chat/material; explicitly flag that the original conversation and attachments may be inaccessible to dot.
- For each available source, capture what was actually inspected vs what was inferred. Record cross-domain coverage and missing Domain Manager outputs.
- `RESEARCH_COMPLETE` requires actual coverage of the scoped source set, not just the three images. If entire source universe can't be inspected, state `PARTIAL_RESEARCH_SCOPE` and describe blockers.
- This gate may progress separately from (and **must not delay**) an otherwise legitimate v2 experiment, provided the experiment's own source and access gates pass.

### G-B: Benchmark Completion Gate

Benchmark v2's [immutable core contract](manifest_v2.json):

- **P1 Reconstruction:** 3 reference stills × 3 Skills × 2 replicates = **18 actual images**.
- **P2 Style Transfer:** 3 reference stills × 2 selected Skills × 2 replicates = **12 actual images**.
- Two independent blinded reviewers and preserved raw ratings.
- Fixed genuine source SHA256, Skill Git commit, prompt hash, same website model/settings, website generation job/evidence IDs, output hashes and hard-fail records.
- **0 additional Higgsfield Credits**, website **Unlimited ON + 0 Credits** confirmed on the live website at submission. Do not substitute MCP/API/CLI/Canvas, paid Credits, or unverified entitlements.
- Screenshot showing `Nov 20, 2026` is **historical and date-column meaning remains unverified**; current entitlement must be rechecked. If unavailable, `BLOCKED_ENTITLEMENT_RECHECK` / `NOT_RUN`, no fake images or ranks.
- Only a fully audited P1 can have `Reconstruction Winner`; P2 winner is **among the two entrants** and cannot rank the excluded third.
- The 30-image test is **not** a benchmark of all 79 creators; @tupacabra is the seed case for a reusable research system.

### G-P: Creative Production and Distribution Gate

Separately validate original work's Story Bible, character/world consistency, continuity, camera constraints, edit/audio mix, technical QC, release formats and rights for any *actual distribution*. Research scope does not imply public reuse rights.

## 7. User-supplied reference analysis and access policy

**Accepted scope:** analyze **every user-supplied creative resource** (images, clips, prompts, source code and creator links), including third-party authored material and references whose commercial reproduction rights are not yet confirmed. **Do not automatically exclude source analysis** on that basis. Analyze composition/style/shot language/cut/audio/narrative; label inference and rights status.

**Separate permissions:** (A) inspect and learn from materials accessible to the user/agent; (B) upload/process with an external provider; (C) reproduce or transform protected work; (D) distribute commercially. Rights and platform terms differ by stage. Keep `use_scope`, `rights_status` and `external_processing_allowed` explicitly tri-stated `YES/NO/UNKNOWN`; `UNKNOWN` is not silent approval for third-party upload or publication.

Use authenticated and authorized browsing where required. Do not bypass website authentication, access controls, rate limits or paywalls, and do not switch to paid credits on a supposedly free run. No user instruction requires losing a source from the research registry if a specific operation is blocked; write `NOT_RUN` with the exact reason.

## 8. Acceptance, verification and report artifacts

Each new research batch must produce:

1. `creator-artwork-inventory` with artwork/creator/source links (includes all checked original 79 + explicitly discussed works), de-duplication, source-confidence and missing-source list.
2. Domain analysis with separate observed/estimated/inferred facts and timestamped evidence.
3. Creator Bible(s), Artwork Analysis, Visual Style Bible(s), Shot IR / storyboard, Prompt Library, camera/lighting/editing rule set as applicable — each marked `NOT_RUN` until truly produced.
4. P1/P2 results only when actual image jobs and independent blind scores exist; per-model and per-replicate metadata plus a 0-credit reconciliation.
5. Cross-domain manager contracts, acceptance matrices and failed assumptions promoted to reusable regression tests/Skills.
6. GitHub PR/commit (no overwrites) and final report listing artifacts, coverage counts, missing references, blockers, actual generation count, Credits delta and unresolved source obligations.

**Source→Contract→Producer→Consumer→Oracle audit for each obligation:** `SOURCE_EVIDENCE | IMPLEMENTED | VERIFIED | NOT_RUN`; do not assert `VERIFIED` solely from agent prose. If no live browser / API / account permission / audio or video access, record each item as unavailable rather than claim execution. Reject silent degradation of source or accepted constraints.

## 9. dot / execution handoff

Read in order:

1. This file: `CREATIVE_RESEARCH_SCOPE.md`
2. [Benchmark Spec](BENCHMARK_SPEC_V2.md), [Manifest](manifest_v2.json), [Execution Prompt](EXECUTION_PROMPT.md), [Validator](validate_spec.py), [Report Template](REPORT_TEMPLATE.md)
3. `creators/study-queue.md`, `research/README.md`, **all actual entries** in `research/creators.json`, related `profiles_raw.json` and `prompt_libraries.json`
4. [dot-specific execution message](DOT_HANDOFF.md)

Begin by reconciling existing evidence and building a `coverage_gaps.md`, then verify current website Unlimited zero-credit entitlement. Work only where the executing agent actually has capabilities and user-authorized access. If it cannot access full chat, some assets or website controls, report that limitation; **a GitHub handoff file does not itself send a message to dot or grant browser access**.

## 10. Non-negotiable state semantics

- `SCOPE_DEFINED` != `RESEARCH_COMPLETE` != `BENCHMARK_COMPLETE`.
- `DOCUMENT_COMMITTED` != `DOT_RECEIVED` != `DOT_EXECUTED`.
- All experiment quality scores and winners remain `NOT_RUN` until generated and independently reviewed.
- Higgsfield website Unlimited only after live 0 Credits confirmation; additional paid Credits cap = 0.
- If a capability or evidence cannot be obtained, record an explicit `NOT_RUN`, `PARTIAL` or `MISSING_SOURCE`, with the last valid state and independent oracle.
