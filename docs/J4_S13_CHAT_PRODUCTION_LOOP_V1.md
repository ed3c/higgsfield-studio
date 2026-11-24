# J4 S13｜Chat-first Production Loop v1

**Status:** engineering candidate / NOT_RUN for this newly added chat surface. No new image has been submitted, reviewed or approved by this change.

This is a thin adapter on top of the **existing** S13 art compiler, pinned historical replay, v4.2 evidence gate, Review Studio and shot IR schema. It is **not** a second Studio, scheduler, human-oracle service, full asset registry, or authorization mechanism. The production Controller is the conversation; the deterministic decisions live in `studio_factory.chat_loop`.

## Why this is separate from historical S13 A/B

The accepted S13 A1/B1/A2/B2 experiment used **Higgsfield website-only Unlimited**, with 9:16, no reference-image uploads, exact Canonical A and Compiler B text and frozen comparison parameters. Its historical results and cost/provenance remain under `studio_factory.s13_eval` and `docs/J4_S13_EVAL_V1.md`.

The **new** chat bridge is a distinct generation surface, triggered by the owner's request to use Higgsfield from conversation. It never claims that website Unlimited grants MCP/Chat free access or that this would complete the original matched A/B. Any chat generation is a separately versioned branch and may proceed **only with a fresh, authoritative zero-credit quote and actual receipt**. Do not convert a rejected free quote to a paid one. Do not re-submit an unknown job. The quote must match the unchanged model/settings/prompt; if the service changes parameters, recompile/reprice. The program does not authenticate a copied quote: a human operator must retain the actual provider response privately.

**Observed on 2026-11-24:** Higgsfield image catalog included `gpt_image_2_6` as capable of Unlimited, but the connected account rejected the requested `use_unlim=true` image cost estimate: `Unlimited generations aren't available on this account`. **No chat image generation is authorized or run.**

## Direct conversation operator protocol

1. **Research:** Ask ChatGPT to search the contemporary artwork or film, inspect primary museum/artist/official sources, and show source images for analysis. For S13, the primary mechanism is Sakamoto/Takatani's *IS YOUR TIME* (salt/water-damaged piano as altered physical object); Horn's *Concert for Anarchy* is a contrastive negative case (suspended/inverted kinetic piano). Record the actual reference URL, rights scope and observable mechanism. Never copy the artwork's installation layout or upload a third-party artwork image to Higgsfield without authorization.
2. **Compile:** From the repository root, load the existing v4.1 compiler and pinned `s13_chat_loop_v1.json` spec. Call `studio_factory.chat_loop.compile_plan(repo, model_catalog_item)` using the **live exact** `models_get` catalog object. Its branches `artwork`, `shot`, `fusion` each have a prompt SHA-256 and dependencies. Artwork-only and Shot-only must generate and pass independently before Fusion can run.
3. **Cost:** In this conversation call Higgsfield `estimate_image_cost` for exactly one still (9:16, chosen model and resolution) with explicitly free/Unlimited selection. Record the **actual** response including its quote reference. The catalog flag `supports_unlim` alone is insufficient. An error, nonzero Credits, unavailable entitlement, or `unlim_choice` awaiting user's decision => BLOCKED. No website entitlement screenshot can stand in for a chat-tool cost response.
4. **Generate:** Only after successful zero-credit preflight, send the **same quoted request** through `generate_image` (never modify settings on a quote reference), observe the Job ID and terminal status, display the image in chat and preserve the original outside Git. Reconcile UNKNOWN before any retry. For serial S13 stages, do not auto-run multiple branches.
5. **Bind output:** Save the image in a private asset root, compute SHA-256 over original bytes; extract the exact submitted prompt, job ID, model, final charge and quote from real provider responses. Use `record_image` with the evidence envelope defined by `schemas/higgsfield-chat-evidence.v1.schema.json`. A synthetic fixture is not valid production evidence. The manifest is an immutable revision; never rewrite the original.
6. **Evaluate:** Reuse the existing S13 Artwork/Shot/Composition Review Studio and Soodles `eval-audit` / `error-discovery` / `write-code-eval` methods. Two *different* independent human reviewers each submit every mandatory observation against **the exact image and prompt digests**. A VLM judge is diagnostic only until held-out calibration; automatic aesthetic PASS is forbidden. Call `evaluate_human_qc` only after real review. Do not treat identity strings alone as authenticated reviewer identities.
7. **Converge:** On `QC_PASS`, freeze the exact stage evidence. On `QC_FAIL`, record the earliest grounded `root_cause_id`, allow **one** proposed correction and new validation only. If no new evidence appears or the correction fails, stop; never broaden prompt search. The deterministic `dry_run_shot_change` must invalidate Shot and Fusion but preserve Artwork. An updated QC rubric can invalidate QC without regenerating pixels.
8. **Release:** Only after artwork, shot and fusion pass human QC, and the owner signs off on exact media, can a static Golden Candidate be proposed. `approve_golden` is an **offline attestation helper**, not authentication, production G2 acceptance, audiovisual approval or GitHub merge authorization. Recipe reuse still requires a second independent successful run and regression.

## Source → Owner → Consumer → Oracle

| Source | Owner | Consumer | Oracle |
|---|---|---|---|
| Museum/artist film references | Art Direction / Rights | Artwork IR | Exact citation, method-only rights, source check |
| S13 v2.6 and v4.1 G2 compiler | Shot Owner | SHOT-only + FUSION | `load_contract` source locks, prompt hash |
| Higgsfield live model specification | Execution Owner | Capability compiler | `models_get` supported 9:16, typed parameters |
| Fresh price/eligibility/Job receipt | Generation / Budget | Evidence Intake | Live 0 Credits, exact settings, completed Job |
| Original images + review observations | Independent Human QC | Freeze / Fusion | Two human reviewers, all hard gates, exact hashes |
| Immutable plan and evidence versions | Artifact / Release Owner | Review Studio, next recipe | Source and output hashes, owner approval, regression |

## Acceptance (Soodles Evals)

| Eval | Required property | Failure classification |
|---|---|---|
| EV01 | Pinned compiler provenance; no prompt/model drift | FAIL |
| EV02 | Live chat zero-credits entitlement; no auto-paid fallback | BLOCKED |
| EV03 | Artwork mechanism observed in actual artwork-only image | HUMAN_FAIL / INCONCLUSIVE |
| EV04 | S13 closed lab, local salt damage, finger/key contact, wafer reflection; no beach piano | HUMAN_FAIL / INCONCLUSIVE |
| EV05 | Fusion retains EV03 and EV04 simultaneously | HUMAN_FAIL / INCONCLUSIVE |
| EV06 | Historical A1/B1/A2/B2 remains separately evidenced, unaltered | INCONCLUSIVE |
| EV07 | Frozen stage/version/bytes never silently overwritten | FAIL |
| EV08 | Shot-only change invalidates Shot+Fusion, reuses Artwork | FAIL |
| EV09 | One proposed repair per rooted failure, no retry without new evidence | BLOCKED |
| EV10 | Failure reports name earliest observable breakpoint, not a guessed cause | INCONCLUSIVE |
| EV11 | Exact generated original + prompt + provider receipt and image hash retained privately | INCONCLUSIVE |
| EV12 | Two independent reviews and owner release; VLM triage cannot promote | BLOCKED |

**Success claim boundary:** production-ready requires actual rendered images, complete human QC and existing formal G2 verification. Mechanical tests can prove refusal, determinism, hashes and state transitions only.

## Minimal dry-run

```sh
python3 -m unittest studio_factory.tests.test_chat_loop -v
python3 -m unittest studio_factory.tests.test_s13_eval -v
```

```python
from pathlib import Path
from studio_factory.chat_loop import compile_plan, dry_run_shot_change

# model_item must come from a fresh Higgsfield models_get readback.
model_item = {"id": "gpt_image_2_6", "output_type": "image",
              "aspect_ratios": ["9:16"]}  # Example, not a live check.
plan = compile_plan(Path("."), model_item)
assert not plan["submissions_authorized"]
assert dry_run_shot_change(plan, plan["branches"]["shot"]["prompt"] + " delta")["invalidated"] == ["shot", "fusion"]
```

This script intentionally has no provider HTTP client, credentials, auto-retry or upload. Chat's connector handles provider effects, the existing repository owns durable production evidence, and original image bytes remain in a private store. The test images are deliberately synthetic and never count as S13 QC.
