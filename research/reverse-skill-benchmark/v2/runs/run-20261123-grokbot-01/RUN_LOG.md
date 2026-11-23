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
