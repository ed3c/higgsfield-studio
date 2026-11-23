# Higgsfield Studio — Full Project Standard v1.0

> Status: `SPEC_DEFINED / IMPLEMENTATION_NOT_RUN`  
> Reviewed: 2026-11-24 (Asia/Taipei)  
> Scope: entire reusable production system; non-destructive migration from existing `projects/_template` and J4.  
> This standard is **not** a claim that the local viewer, compiler, sync, benchmark, or CI already works.

## 1. Reference authority and evidence

**Observed through read-only Higgsfield project connector**, from publicly shared [Cully Hill Boys](https://higgsfield.ai/@higgsfield.studio/projects/cully-hill-boys), project ID `b619c13c-83ba-4ea3-b85c-de9be41bd01b`:

- Root: `PRE  PROD`, `1 ACT (1-49)`, `2 ACT (50-93)`, `3 ACT (93-120)`, `4ACT_Epilogue (121-137)`, `0 Regenerations`.
- `PRE  PROD`: `Character Test`, `Costumes`, `ASSETS`, `CLEAN UP`, `Test_v1`…`Test_v5`, `Test_scene16`.
- Act folders contain scene-number or scene-group subfolders, such as `04 scene`, `40-45 scene`, `52-55`, `121`, and `131 scene`.
- An inspected pre-production asset was a completed `nano_banana_pro` image job; an inspected Scene 04 asset was a completed `seedance_2_0` video job. Their accessible prompts exposed distinct blocks for style/optics/camera/lighting, reference bindings, timed cuts, physical behavior, audio and prohibitions. This is a **sample**, not an exhaustive inventory.
- Some source scene labels overlap or duplicate (e.g., ACT 2/3 boundary 93; scene numbers reused); do **not** adopt source folder names as canonical IDs.
- The connector confirmed read-only capabilities on this externally owned project. Do **not** mutate, mass-download, or republish its assets. The full original Brief, all generated assets, all Elements and all prompts were **not** comprehensively audited.

**Official product contracts**:
- [Open Project: result, brief, folders, models and prompts](https://higgsfield.ai/creator-hub/help-center/community/how-do-projects-work)
- [Cinema Studio Projects: Brief sections, Elements, folders, asset review, roles, filters](https://higgsfield.ai/enterprise-help-center/manage-account/projects)
- [Cinema Studio 4.0: project/global versus per-shot controls](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio)

**Local repository evidence**: `README.md`, `projects/_template/`, `prompts/`, `research/reverse-skill-benchmark/v2/`, `projects/j4-async-succession/J4-S13-Dot-Handoff.md`. Existing generated Markdown from `prompts/_render_library.py` is **not** the source of truth.

## 2. Authority and storage boundaries

1. **Git = semantic source of truth** for Project/Shot/Optical/Art IR, final exact prompts, IDs, manifests, decisions, QC, rights, provenance, scripts, tests and lightweight evidence. Preserve existing `prompts/`, `research/`, `skills/`, `budget/`, `templates/`, `creators/`, and `plan/` without moving them in this migration.
2. **Higgsfield Cinema Studio = execution surface and visual placement system**. Keep a stable mapping from local project/scene/shot/run IDs to Higgsfield `project_id`, `folder_id`, `placement_id`, `item_id` and model version. A source ID and a folder placement ID are distinct.
3. **Google Drive or a designated external object store = large-media source** for original stills, clips, WAV/FLAC, masters and comparison montages. Store a Drive file ID or durable URI, SHA-256, size, codec and usage rights in Git; never commit signed temporary URLs or credentials.
4. **Local web = review and acceptance surface**. It must render actual referenced media and prompts, allow playback, compare versions, and expose gate outcomes. A visual mockup is not acceptance.
5. **Notion = optional published research index**, not a conflicting canonical editor for prompt/run/rights state. All imported external records retain source URL, retrieval timestamp and uncertainty labels.

Never silently convert a missing file, unknown model setting, untested comparison, absent license or unavailable asset into PASS.

## 3. Project identity and native Higgsfield folder convention

Each production has one stable `project_slug` and one project manifest. Use **Act → Scene → Generation** to organize the actual Higgsfield folders, inspired by the verified example.

Suggested native Cinema Studio tree (a target convention, **not** a claim that these folders already exist):

```text
<project-name>/
├── 00_PREPROD/
│   ├── CHARACTERS/
│   ├── LOCATIONS/
│   ├── PROPS_COSTUMES/
│   ├── ARTWORK_STYLE_TESTS/
│   └── LOOKDEV_TESTS/
├── 01_ACT/
│   └── SC-001__scene-slug/
├── 02_ACT/
│   └── SC-050__scene-slug/
├── 03_ACT/
│   └── SC-094__scene-slug/
├── 04_EPILOGUE/
├── 90_REGENERATIONS/
└── 99_SELECTED_DELIVERABLES/
```

For shorts/art installations, `ACT` can be a sequence/section, but `scene_id` and `shot_id` are still mandatory. Avoid using model names as the primary hierarchy; model is a filter on generation runs. A scene group is a **view** (multiple scene IDs), not an excuse to merge immutable shot IDs.

**Canonical Git project layout** (new target; keep the current simpler `projects/_template` compatible):

```text
projects/<project_slug>/
├── project.manifest.yaml       # identity / native folder binding / publication policy
├── brief.md                    # Context, Narrative, Visuals, Production, Status, Resources, Notes
├── bibles/                     # story, world, art style, audio, continuity
├── elements/                   # @character / @location / @prop ID + versions + rights
├── acts/
│   └── act-01/
│       └── scenes/
│           └── SC-001/
│               ├── scene.yaml  # scene scope; shot order; geography and timing
│               └── shots/
│                   └── SH-001/
│                       ├── shot.ir.json
│                       ├── prompts/
│                       │   ├── artwork-only.txt
│                       │   ├── shot-only.txt
│                       │   ├── fused-final.txt
│                       │   └── prompt-lock.json
│                       ├── runs.jsonl
│                       └── qc.jsonl
├── experiments/               # comparisons, frozen conditions and blinded ratings
├── assets/                     # manifest.jsonl, external storage pointers, hashes
├── post/                       # edit decision list, music rights, subtitles, sound notes
├── deliverables/               # platform manifests and publication links, no large media in git
└── evidence/                   # human approvals, rights, billing, coverage gaps
```

Existing `projects/_template/brief.md`, `prompts-used.md`, `generations.csv`, `edit-notes.md` and `published.md` remain valid as legacy-compatible views. Do not delete or bulk-rename them before an explicit mapping and diff review. The current budget ledger remains the authoritative cost ledger until a migration parity check passes.

## 4. Structured prompt contract: two independently testable branches

```text
Research artwork + rights evidence
  -> ArtworkMechanismIR -> artwork-only prompt -> artwork-only visual QC
Original narrative + scene geography + camera + causality
  -> ShotIR          -> shot-only prompt    -> shot-only visual QC
[approved artwork mechanism + approved shot behavior]
  -> CompositionIR   -> fused-final prompt  -> combined visual QC
  -> generation job -> raw run evidence -> independent verifier -> selected take
```

- **Artwork branch** describes a transferable visual/physical *mechanism*, observable composition, material and temporal behavior; references are source-linked. It must not claim to reproduce copyrighted artwork or contain an unlicensed direct copy.
- **Shot branch** contains original dramatic action, participants, physical geometry, camera, duration, continuity and hard negatives. It must not rely on artwork-style wording to assert correct action.
- **Fusion branch** is a deterministic composition of two *approved* branches. A beautiful image is not a substitute for the intended causal action.
- **Exact final prompt** is a frozen compiler artifact with compiler version and SHA-256. Preserve separately the pre-generation text that was **actually sent** to Higgsfield, including UI edits, model settings, references and seed when exposed.
- **Higgsfield references** may use UI `@element` names or job/media reference IDs. Store them in typed `reference_bindings` so prompt text alone is not the only provenance. Preserve missing fields as `null`/`UNKNOWN` instead of inventing them.
- **Global and per-shot split**: project visual bible, color, lighting, genre, era, character/world locks belong at the global level; scene spatial graph, motion, shot duration, camera, audio, and prohibitions belong at scene/shot level. Resolve conflicts explicitly before compilation.
- **Long-prompt guard**: require shot-level duration/shot-count consistency, model capability checks, contradictions check, and reference count validation. A prompt describing four 6-second cuts does not prove a single generation ran for 24 seconds.

Each shot exposes `artwork_prompt`, `shot_prompt`, and `fused_prompt` as distinct versioned resources. Refer to `schemas/higgsfield-shot-ir.v1.schema.json` for the machine-readable minimum.

## 5. Asset and generation lineage

One asset may appear in several folders without duplicating the underlying media. Keep these as separate concepts:

| Record | Minimum immutable linkage |
|---|---|
| Project | `project_slug`, `project_id`, `workspace_id`, `brief_revision` |
| Scene / Shot | `scene_id`, `shot_id`, `act_id`, `source_folder_id`, `duration_contract` |
| Element | `element_id`, `version`, `kind`, `rights_status`, `reference_media_id` |
| Prompt | `prompt_id`, `branch`, `source_ir_sha256`, `compiler_version`, `sent_text_sha256` |
| GenerationRun | `run_id`, `item_id`, `placement_id`, `folder_id`, `model_id`, `settings`, `prompt_id`, `created_at`, `credit_delta`, `status` |
| Asset | `asset_id`, `run_id`, `kind`, `storage_uri`, `sha256`, `dimensions/duration`, `license_scope` |
| Review | `asset_id`, `oracle_id`, `criterion_id`, `result`, `observable_evidence`, `reviewed_at` |
| Publication | `selected_asset_ids`, `type`, `slug`, `show_prompts`, `rights_approval`, `public_url` |

No source bytes → no claim of SHA validation. A `placement_id` is not interchangeable with `item_id`. Store native source folder name and ID even when canonical slug is normalized, for reversible imports.

## 6. Required local web information architecture

```text
Header: Project title · brief revision · gate status · credits · publication state

Left rail: Project
  Overview / Brief / Acts & Scenes / Elements / References
  Prompt Lab / Generations / Visual QC / Edit & Audio
  Delivery / Provenance & Rights / Budget / Lessons

Centre:
  folder/scene tree → Square or Masonry media gallery
  search + filters: act, scene, shot, type, model, version, status, QC, date
  image lightbox OR video player with scrub, speed, audio and timecode
  artwork-only vs shot-only vs fused side-by-side visual comparisons

Right inspector (selected asset):
  thumbnail, immutable ID, source URI, hash, model, settings and cost
  exact sent prompt + compiler output + prompt diff
  active Elements/reference thumbnails and licensing/source links
  expected invariants vs observed frames, status and reviewer evidence
  source → contract → producer → consumer → oracle chain

Bottom:
  run history, version timeline, rejected/approved takes, reg-test links
```

Recommended cards expose: image/video preview, `SC/SH` IDs, branch `ART/SHOT/FUSED`, `run_id`, model, duration, cost, `DRAFT/NEEDS_REVIEW/APPROVED/REJECTED`, and selected-take marker. Clicking a card must open the **exact** source and its prompt; never substitute a prettier sibling generation. Support Higgsfield-native Square/Masonry, favorites, filters and reviews, but keep local experiment-specific fields as extensions.

A full project overview uses **Feature / Series / Carousel** presentation modes and covers. Publishing with visible prompts and publishing with hidden prompts are distinct rights choices. Never toggle publication or expose protected reference files by default.

## 7. Manager boundaries and deterministic gates

Existing Creator Intelligence, Provenance/Rights, Narrative, Art Direction, Character/World, Cinematography, Compiler, Generation/Cost, Independent Evals, Post/Audio, Distribution and Knowledge Managers remain separate **contract owners** even if a small team shares agent processes.

Workflow states: `DRAFT → IR_LOCKED → PROMPT_COMPILED → PREFLIGHT_APPROVED → GENERATED → QC_PENDING → QC_APPROVED | QC_REJECTED → SELECTED → PUBLISHED`. Each transition has immutable `source_revision`, owner, evaluator and evidence. No automatic `QC_REJECTED → SELECTED`. Failure creates a new run, never overwrites an earlier run.

For J4 S13, preserve all historical `NOT_RUN`, `UNKNOWN`, A/B fixed conditions and two independent human review obligations. **No generation may start** until the website-specific zero-credit entitlement and the actual Generate price are observed. API/MCP eligibility is not evidence of web Unlimited eligibility.

## 8. Minimal acceptance matrix

| Gate | Acceptance oracle | Current status |
|---|---|---|
| `TREE-01` | Root and all scene folders indexed with stable IDs, no lost mappings | NOT_RUN |
| `BRIEF-01` | All seven official Brief sections visible with edit/source history | NOT_RUN |
| `PROMPT-01` | ART, SHOT, FUSED separately diffable; compiler hash equals submitted text or logged override | NOT_RUN |
| `ASSET-01` | Clicked media matches run/placement, playable, bytes/hash and provenance verified | NOT_RUN |
| `ELEMENT-01` | All @references bind to versioned Elements or explicit missing source | NOT_RUN |
| `QC-01` | Independent artwork, shot and combined QC; hard failures reject | NOT_RUN |
| `COST-01` | Generation ledger parity; J4 web-only zero-credit preflight gate | NOT_RUN |
| `RIGHTS-01` | Third-party reference rights, consent, prompt disclosure, no public secrets | NOT_RUN |
| `PUBLISH-01` | Feature/Series/Carousel, cover, slug, visibility and public preview confirmed | NOT_RUN |
| `MIGRATE-01` | Existing J4, research, prompt IDs, budget and handoffs preserved byte-for-byte or migrated with diff | NOT_RUN |

No CI, browser playback, physical media hashing, bulk backfill or publication was performed by this documentation-only PR.

## 9. Staged, non-destructive rollout

1. **Inventory** all Git files, actual Higgsfield project folders and owned assets, Drive file IDs, active PR branches, and current J4 obligations. Produce a gap report without deleting/moving.
2. **Map** current `_template` and J4 historical IDs to canonical Project/Scene/Shot/Asset IDs. Handle duplicate scenes by explicit source folder ID and human review; do not deduplicate by display name alone.
3. **Compiler** implement ART-only, SHOT-only and FUSED outputs with deterministic prompt lock, version and hash, followed by independent visual QC.
4. **Viewer** build the smallest full loop first: one project → one scene → one shot → three prompt branches → three media candidates → diff/QC/player. Expand to full film only when the loop is accepted.
5. **Import & reconcile** external media as linked sources, not Git blobs. Run budget and rights checks, test preview/playback, then expose publication controls behind explicit approval.

## 10. Out of scope / prohibited assumptions

- This branch does **not** copy or own Cully Hill Boys artwork, prompts, character likenesses or videos.
- No actual native Higgsfield folder changes, media generation, paid jobs, Drive writes, website deployment, benchmark result or GitHub main merge is implied.
- No permission to publish third-party media is inferred from a public Open Project.
- Preserve raw examples for source analysis, but reusable production Skills must use original abstractions, rights-cleared references and verified contracts.
