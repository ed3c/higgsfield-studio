# Run run-20261123-grokbot-01 — preflight log (append-only)

- **Executor:** Grok Bot (code agent on its own Linux box), on behalf of the repo owner, instruction of 2026-11-23 (Asia/Taipei).
- **Base:** `main` @ `d9eb999` (merge of PR #7). Branch `feat/reverse-benchmark-v2-run-20261123`.
- **State semantics:** `DOCUMENT_COMMITTED` ≠ `DOT_RECEIVED` ≠ `DOT_EXECUTED`. This run is **not dot**; dot did not receive or execute anything through this commit.
- **Immutable inputs:** v1 (`research/reverse-skill-benchmark/README.md`, `manifest.json`), the v2 spec pack, `research/creators.json`, `profiles_raw.json`, `prompt_libraries.json` are **not modified**. Their SHA-256 at read time: [`input_sha256.txt`](input_sha256.txt).

## 1. Files read in full (2026-11-23 ~18:00–18:10 Asia/Taipei)

CREATIVE_RESEARCH_SCOPE.md, DOT_HANDOFF.md, BENCHMARK_SPEC_V2.md, manifest_v2.json, EXECUTION_PROMPT.md, validate_spec.py, README.md, REPORT_TEMPLATE.md, the three CSV templates, v1 README + manifest.json, research/README.md, research/creators.json (79 records + 3 lower-confidence candidates), profiles_raw.json (60 profiles), prompt_libraries.json, creators/study-queue.md. Also read the **unmerged** Draft PR #5 (`079105b`, `v2/NOT_RUN.md` on branch `docs/reverse-benchmark-v2-preflight-20261123`) as prior evidence; it is referenced here, not copied or altered.

## 2. Validator

`python3 research/reverse-skill-benchmark/v2/validate_spec.py` → exit 0. Output verbatim in [`validate_spec_output.txt`](validate_spec_output.txt):

```
SPEC LINT PASS: matrix, score weights, zero-credit gate and NOT_RUN semantics coherent.
EXECUTION STATUS: BLOCKED_ENTITLEMENT_RECHECK — no images or scores produced by this spec pack.
```

This is a schema-coherence lint only; it certifies nothing about execution.

## 3. Skill pins

Upstream HEADs checked read-only via the GitHub API; all three equal the PR #5 pins. See [`skill_pins.json`](skill_pins.json). No candidate Skill was installed or executed in this run.

## 4. Prior entitlement evidence (not re-verified by this commit)

PR #5 (unmerged) records a read-only website observation: GPT Image 2.6 Unlimited **Active, Starts Nov 20 2026, Expires Nov 27 2026**; ordinary image page, GPT Image 2.6 *Sunburst*, 16:9, 1K, Medium, PNG, Unlimited checked → submit control read `Unlimited`. No job was submitted. This run treats that as historical evidence; G1 must be rechecked live at submission (spec §4.6).

## 5. Entries appended later

(append below; never rewrite earlier entries)

### 2026-11-23 ~18:30 Asia/Taipei — registry, job slots, gates

- Registry batch `research/creator-artwork-registry/batch-20261123-grokbot/`: 79/79 historical rows + 3 lower-confidence + new `CR-TUPACABRA`; 95 sources; 9 named artworks; 12 MISSING_SOURCE records.
- 30 job slots emitted (`job_slots.json`, `jobs.md`); all `prompt=null`, 0 ready.
- Gates recorded separately in `GATES.json`: G-R `PARTIAL_RESEARCH_SCOPE`; G-B `BLOCKED_SOURCE`.
- P2 replacement subjects proposed, **not locked**.

### 2026-11-23 ~18:20 Asia/Taipei — owner decisions (t28u)

- D-01: P2 subjects **APPROVED and locked before P1** → `p2_subjects_APPROVED.json` (PROPOSED file kept unchanged). Closes MS-008.
- D-02: model fixed per spec: GPT Image 2.6 *Sunburst*, 16:9, 1K, website Unlimited.
- D-03: live check at 18:07 (orchestrator, private evidence): GPT Image 2.6 Unlimited 0 credits; Seedream 5.0 Pro Unlimited (not used); **Nano Banana Pro 2 credits → fallback unavailable**.
- D-04: C01–C03 not locked; awaiting owner pick. Full record: `DECISIONS.json`.

### 2026-11-23 ~18:40 Asia/Taipei — sources and C-candidates (no lock)

- MS-005/007 closed; trailer obtained from X (720p) and YouTube (4K), private copies hashed (`research/live/creator-intelligence/2026-11-23-tupacabra/SOURCES.md`).
- 55 shots scene-detected; 9 candidates (3 per case) analysed in `C_CANDIDATES.md`; recommendation C01a S30 / C02a S16 / C03a S06. **Not locked**, no prompts generated, job slots unchanged (`prompt=null`).

### 2026-11-23 ~18:45 Asia/Taipei — reference lock + entitlement correction

- C01–C03 **LOCKED** (owner t28s3): S30 / S16 / S06 from the 4K file; the same Telea-inpaint mask at native rect (1740,2035)-(2100,2095) for all three; masked and unmasked hashes recorded in `REFERENCE_LOCK.json`. G0 → sources + hashes + scope present.
- **Correction to DECISIONS.json D-03** (the original is kept): the 18:04–18:07 check ran in the Grok Bot box's own browser, not in Neon's. Six screenshots were hashed (`ENTITLEMENT_EVIDENCE_20261123.json`) and kept private. Caveat: the NBP 2-credit screenshot was taken at 9:16 / 2K / 4 outputs, not at benchmark settings.
- C02 sub-label swap in `C_CANDIDATES.md` noted as an erratum; nothing was erased.

### 2026-11-23 ~19:05 Asia/Taipei — P0 prompt lock (reconstruction)

- Skills cloned at the pinned SHAs into `/workspace/hs-bench-skills/` on the box. Nothing was installed. unimage's optional eval script and API helper, and Caph's `agents/openai.yaml`, were **not run**. niobium617's `analyze_image.py` and `prompt_compiler.py` ran with networking disabled (`unshare -rn`).
- Invocation, per spec §5 P0 and the PR #5 dispositions:
  - unimage: Reverse Prompt Mode, Scene Auditor → Detail Scanner → Spatial Architect → Prompt Engine. Stopped at the first draft; no Draft Validation and no QC/Repair.
  - Caph: SKILL.md workflow, final prompt only.
  - niobium617: image branch → `gpt_image`, kind `prompt`, `--auto` scoring. The step-5 rescore loop was not run.
- **9 prompts = 3 cases × 3 Skills.** Spec: "One prompt per (case, skill, task), reused for both replicate renders", so the 18 P1 jobs use 9 prompts × 2 replicates. Each Skill was not run twice.
- Interpreter for all 9 cells: Grok Bot (this agent), viewing a 1920×1080 downscale of the masked reference. The common brief is `P0_TASK_BRIEF.md`.
- **Limitation:** the interpreter had already seen and described these frames during candidate selection, so its analysis is not naive. The exposure is equal across the three Skills.
- Outputs: `v2/prompts/reconstruction/{C01,C02,C03}/{unimage,caph,niobium617}/`, index in `prompts.csv`. All normalizations are listed in each `prompt_diff.md`. No prompt was polished by hand.

### 2026-11-23 ~19:10 Asia/Taipei — P1 jobs ready

- `job_slots_v2_p1_ready.json` (supersedes `job_slots.json`, which is kept): **18 P1 jobs READY_TO_SUBMIT**, in seeded serial order, using 9 distinct prompts. Settings: GPT Image 2.6 Sunburst, 16:9, Medium, 1K, PNG, 1 output, Unlimited ON, no image attached. **12 P2 jobs NOT_RUN.**
- Copy-paste list: `p1_submit.md`. 0 jobs submitted, 0 credits spent.

### 2026-11-23 ~18:55 Asia/Taipei — P1 jobs 01–09 generated (reported by the generation operator) + Drive storage

Source of these facts: the orchestrating Grok Bot agent, which ran the website generation in its own box browser. This executor did not observe the submissions. It verified the output files, hashes, Drive uploads and Drive permissions.

- **Jobs 01–09: all submitted with the button reading UNLIMITED, 0 credits.** Submit window 2026-11-23 10:31–10:47 UTC (18:31–18:47 Asia/Taipei).

  | # | job | website job id |
  | --- | --- | --- |
  | 01 | P1-C01-niobium617-r2 | 5a8fc498-489a-4245-a3df-f191e019226b |
  | 02 | P1-C01-caph-r1 | ba37eaa2-3df5-4bba-b820-8a0900bdb6bb |
  | 03 | P1-C01-unimage-r1 | ebee4b81-0f75-4c02-a7ef-96f3a7c82274 |
  | 04 | P1-C01-unimage-r2 | a0b27911-4f0e-499c-b954-2757311ea597 |
  | 05 | P1-C01-caph-r2 | 5ad97031-dcaf-4f70-a2de-5444b4b19b16 |
  | 06 | P1-C01-niobium617-r1 | 63ae70f4-7b02-443a-976a-15813ee23863 |
  | 07 | P1-C02-unimage-r2 | 21d67601-a4f6-444a-8df8-277f731f5f37 |
  | 08 | P1-C02-unimage-r1 | 83cd6ca7-0e3f-4697-aca2-8ec4f7f100cd |
  | 09 | P1-C02-caph-r1 | d0097f3f-59be-4f9a-9f0e-7198d70bbf7c |

- **ANOMALY A-01:** at 10:34 UTC, job 01's prompt was submitted a second time by accident (website id `89e69711-ac06-4817-a75e-74dbcccf9405`). It was free and the image was not saved. It is **EXCLUDED** from the benchmark and from blind review, and does not replace job 01.
- **UI note:** the batch display read `1/4`, but each job returned exactly 1 image.
- **Prompt transport:** `file://` was blocked in the browser, so prompts were served from a local HTTP server. The pasted lengths matched the `normalized_prompt.txt` files.
- Per-job rows are in `generations.csv`: output sha256, Drive file id, website job id. Per-job submit and complete timestamps were not supplied and are left blank.
- **Storage (Neon t29u):** 9 outputs and 6 masked reference frames were uploaded to Neon's Google Drive under `Higgsfield-Studio/reverse-benchmark-v2/run-20261123-grokbot-01/{output,refs}/`, which is **private (owner only, verified with get_file_permissions)**. Box copies are kept. Index: `DRIVE_STORAGE_MANIFEST.json`.
- **Pending:** jobs 10–18 were not yet in the box output folder at 18:55. Status: P1 9/18, P2 0/12.

### 2026-11-23 ~19:15 Asia/Taipei — P1 jobs 10–18 (reported by the generation operator) + Drive

Facts below were reported by the orchestrating Grok Bot agent, which ran the generation in its own box browser. This executor verified the output files, their sha256, that the pasted lengths equal the locked prompt lengths, the Drive uploads and the Drive permissions.

| # | job | submit (UTC) | done (UTC) | website id (UUID from downloaded filename) | pasted chars | status |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | P1-C02-niobium617-r2 | 10:50:38 | ~10:52:05 | 4f987b45-02e7-4302-9022-3e789740a2ef | 1664/1664 | GENERATED |
| 11 | P1-C02-caph-r2 | 10:52:50 | ~10:54:15 | 05bbafcd-79fa-4c53-9697-2ff2e6dffb89 | 1282 | GENERATED |
| 12 | P1-C02-niobium617-r1 | 10:55:17 | ~10:56:45 | f228c112-bb3c-42ea-bec5-a73259130fdc | 1664 | GENERATED |
| 13 | P1-C03-caph-r2 | 10:57:38 | ~10:58:55 | a00aaeb2-5534-41e4-a90b-ee43e5688c30 | 1098 | GENERATED |
| 14 | P1-C03-caph-r1 | 10:59:45 | ~11:01:05 | 96410c13-4588-4472-a247-ee9994fcd372 | 1098 | GENERATED |
| 15 | P1-C03-unimage-r2 | ~11:02 | — | — | 861 | **MODERATION_REFUSED** |
| 16 | P1-C03-niobium617-r1 | 11:04:08 | ~11:05:35 | fd2f4c31-89bc-42d2-8628-b6e69acfec4e | 1450 | GENERATED |
| 17 | P1-C03-niobium617-r2 | 11:06:37 | ~11:08:00 | 5b6b674d-c55b-426a-93d0-6698fd1b9027 | 1450 | GENERATED |
| 18 | P1-C03-unimage-r1 | 11:09:09 | ~11:10:35 | 7750727c-a065-4018-924f-648321793bd0 | 861 | GENERATED |

- **All jobs:** the button read UNLIMITED with no credit number, 0 credits, no image attached. Before the first submit of this batch the toggle was OFF and the button showed `✦1`. It was switched ON before any submit.
- **Job 15 (anomaly A-02):** the site refused it with the tile "NSFW — Credits refunded" and produced no image. Its prompt is byte-identical to job 18's (same cell C03/unimage), and job 18 succeeded. **Not retried; pending Neon's decision.**
- **Anomaly A-03:** two pastes failed and were caught by the length check, then redone. Nothing was submitted from a stale prompt.
- **Anomaly A-04:** one stray Generate click did nothing (no job created).
- Verified by the executor: the pasted lengths match `len(normalized prompt)` for every job.
- Rows 10–18 are appended to `generations.csv`. Job 15's row has status MODERATION_REFUSED and no output.
- **Drive:** the 7 new PNGs (jobs 11–14, 16–18) are in the private `output/` folder (`DRIVE_STORAGE_MANIFEST_addendum_02.json`). Job 10 was uploaded earlier (addendum 01). `output/` now holds 17 PNGs, owner only.
- **P1 status: 17/18 generated, 1 moderation refusal, 0 credits** (`P1_STATUS.json`). Gate G3 = `PARTIAL_P1`. P2 0/12 NOT_RUN.

### 2026-11-23 19:19 Asia/Taipei — owner decision on job 15

- Neon (widget answer to t30s4), verbatim: **"Don't retry it; record it as a moderation refusal"**.
- Job 15 `P1-C03-unimage-r2` is now **final MODERATION_REFUSED and will never be retried**.
- **GAP-P1-01:** cell C03 × unimage has a single replicate (r1, job 18). Under spec §7/§8 no P1 winner can be declared, and G3 stays `PARTIAL_P1`. Any P1 ranking, including the choice of the P2 candidate B, is **PROVISIONAL**.
- `P1_STATUS.json`: the refused-job entry was updated in place (`decision_pending` set to null and the decision referenced) and a `history` entry was appended. The earlier counts are unchanged.

### 2026-11-23 19:20–19:45 Asia/Taipei — owner/oracle style verdict, P1 eval setup, P1b-style-fix addendum (DRAFT, not generated)

- **Human owner/oracle observation.** Neon, t31u, 19:20, verbatim: 「圖片的電影風格具有攝影寫實的感覺，這批圖片風格只有構圖類似，需要修正」.
  - Recorded as: **P1 style fidelity = FAIL (all 17 outputs); composition = similar**.
  - This is an owner observation. It is not one of the two blind reviewer scores and does not replace them.
- **P1 blind review is kept as baseline evidence.**
  - Packet: `eval_p1/`, plus a private tar.gz and the sealed key in the private Drive `eval/` folder `1UqLL_TIN0ftynvlM9K2qDdyK-MYJtgB3`. Permissions checked: owner only.
  - State `PARTIAL_EVAL`: **0 of 2 reviewers have scored.**
  - This executor did not self-score, because it is neither blind nor independent (see `eval_p1/EVAL_SETUP.md`).
  - No P1 output, prompt or hash was altered.
- **Look-gap analysis.** `p1b_style_fix/LOOKGAP_ANALYSIS.md`, measured and inferred. Headline findings:
  - (1) Deep-focus, edge-to-edge crispness and synthetic micro-texture are the dominant CG tells.
  - (2) Each case is mis-exposed: C01 face about 1–1.5 stops dark with no high key; C02 bright golden-hour postcard against a dim, overcast reference (about +1.5 stops, wrong weather); C03 blacks lifted against crushed blacks in the reference.
  - (3) Film, halation and shallow-DOF words were already in the P1 prompts and were ignored.
- **SPEC DEVIATION — P1b-style-fix is an ADDENDUM, not a replacement.**
  - It is not one of the 30 core images and does not change P1 results, scores or gates.
  - Design: P1b prompt = the locked P1 normalized prompt, byte-identical (prefix sha verified for all 9), plus a per-case look lock shared by all three Skills (`p1b_style_fix/LOOK_LOCK_SPEC.json`).
  - The look lock is human/executor-authored. It is therefore a controlled, documented prompt intervention and **not** a Skill output; P1b results must never be credited to a Skill on their own.
  - Job list: `p1b_style_fix/p1b_jobs.json`. 9 jobs = 3 cases × 3 Skills × r1.
  - Order: no blind scores exist, so a strongest-to-weakest order is not available. Submit order is a Latin square over Skills per case to spread position effects.
  - Settings: GPT Image 2.6 Sunburst, 16:9, 1K, Medium, website Unlimited at 0 credits, no upload.
  - Paste files: `/workspace/hs-bench-jobs/p1b_prompts/NN_jobid.txt`, with mirror copies in `p1b_style_fix/prompts/`.
  - **Status: NOT GENERATED.**
- **Risk note.** `P1b-C03-unimage-r1` starts with the same text that produced the moderation refusal for job 15. If it is refused, record it as MODERATION_REFUSED and do not retry without Neon.

### 2026-11-23 19:46–19:58 Asia/Taipei — P1b-style-fix generated (ADDENDUM), stored, measured

- **Operator report.** The generation was done by the orchestrating Grok Bot agent in its box browser. 9 of 9 generated, 0 refusals, all UNLIMITED at 0 credits, no image attached. The Unlimited toggle was initially OFF ("GENERATE 1") and was switched ON before any submit. Two accidental non-submit clicks (an image viewer and a nav hover) caused no charge and created no job.
- **Verified by the executor:**
  - Each PNG's embedded `hf-job-id` tEXt chunk equals the UUID reported from its download filename.
  - Each pasted character count equals the prompt file's length.
  - The sha256 hashes are recorded in `generations_p1b.csv`.
  - P1b-C03-unimage-r1 was **not** refused this time.
- **Drive.** Files are in the new private folder `output_p1b/` (`1Q8RQSKKuiBghbWmsmza0od-Ge-LIXwde`): 9 PNGs plus `p1b_compare.jpg`. The folder, 1 PNG, the comparison sheet and `eval/` were permission-checked and are owner-only. Drive sizes equal the box bytes. See `DRIVE_STORAGE_MANIFEST_addendum_03.json`.
- **Metrics.** `p1b_style_fix/P1B_LOOK_METRICS.md` and `look_delta_summary_case_level.json`.
  - Closed: the CG crispness gap (63–87% of the centre-sharpness gap closed), the C02 sunny/warm cast, and the exposure of C01 and C03.
  - Remaining: highlights compressed in every case (p99 about 162 vs 187–195, which is why C01 still reads darker), C01 over-desaturated, C02 depth-of-field structure and camera distance unchanged, C03 blacks not crushed. Softness overshot.
- P1b remains an **addendum** to the spec. It changes no P1 result, score or gate. **No regeneration.**

### 2026-11-23 19:54–20:20 Asia/Taipei — NEW PHASE `STYLE_DNA_EXTRACTION` (separate from the benchmark score)

- **Trigger.** Neon t33u, 19:53, verbatim: 「逆向到提示詞生成圖片風格可以自由發揮為止，只學習風格不寫死對象」.
- **Scope.** This phase does not feed into P1, P1b or P2 scores, gates or Skill rankings. Everything is new files under `style_dna/`. Nothing was overwritten.
- **Method source.**
  - Neon's Notion page "Higgsfield 電影風格逆向｜100 個開源 Prompt / Skills 與 14 部得獎作品（2026-11-23）" (`4213cec0-38da-81cc-beb4-d00869165eab`) was found and read via the Notion connector. It was **not edited**.
  - Adopted from it: the Style vs Shot prompt split with independent acceptance, pixel-only QC (Oracle Validity), and its 6 metrics: Style, Narrative, Camera, Temporal, Creative Distance, Oracle.
- **New evidence.** Look metrics over all 55 trailer shot-midpoint frames (`style_dna/trailer_55_look_stats.json`). Trailer p99 median is 224, so the highlights of the source clip routinely. This confirms that P1b's highlight compression was wrong.
- **Deliverables:**
  - `TUPACABRA_STYLE_DNA.md`
  - `STYLE_PROMPT_v1.txt` and `style_block_v1.txt`. The block is 2,448 characters, with zero subject, place or ref-motif terms (word-boundary check).
  - `style_targets_v1.json` and `check_style_v1.py`.
  - `validation_v1/ACCEPTANCE.md`: 6 S1 prompts plus 6 optional S0 shot-only controls.
- **Metric gate calibration.**
  - Refs 6/6 pass; P1 0/17; P1b 0/9; trailer 28/55.
  - The gate rejects every known failure and accepts the refs.
- **NOT generated.** No credits spent.
