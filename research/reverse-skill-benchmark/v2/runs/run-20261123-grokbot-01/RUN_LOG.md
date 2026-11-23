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
