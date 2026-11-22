# J4 G2 v4.2 — Evidence-Bound Candidate Intake

Status: **OFFLINE PROVENANCE AND STATIC REVIEW INTAKE; NOT IMAGE-UNDERSTANDING; NO PAID GENERATION.**

## Why this exists

v4.1 rejected six failed visual concepts from a supplied contact sheet, but still lacked original model receipts, submitted prompt hashes, separately addressable outputs, review-evidence binding and two reviewers. A human describing an image is not a machine-verified visual oracle.

v4.2 adds a second, stricter gate. It never calls Higgsfield or any provider. It verifies **files and claims** without pretending the claims were automatically recognized in the image.

## Source ownership and where to put files

- Git: `studio_factory/evidence_gate.py` — read-only byte digest + receipt checks; no provider API.
- Git: `studio_factory/tests/test_evidence_gate.py` — positive fixture and adversarial negative tests (tiny test PNG, not artistic output).
- PRIVATE local asset root: `$HOME/Higgsfield-Private/J4/` — continue using the existing SHA-verified Drive archive restoration.
- New original candidate media: `$HOME/Higgsfield-Private/J4/extra/candidates/<candidate-id>.png` or `.mp4`.
- One evidence receipt per actual candidate: `$HOME/Higgsfield-Private/J4/extra/g2_receipts/<candidate-id>.json`.
- Exactly two independent attested reviewer records: `$HOME/Higgsfield-Private/J4/extra/g2_reviews/<candidate-id>/<reviewer-id>.json`.
- Evaluated report (local): `$HOME/Higgsfield-Private/J4/extra/g2_reports/<candidate-id>.json`.
- Local site: `http://127.0.0.1:8765`, **Candidate Evidence** tab. The site scans new files only during server startup; restart after adding local receipts.

The new folder paths above are conventions, **not claims that the files exist on the user's Mac**. Never place receipts, raw media, private Drive credentials or reviewer identities in the public Git repository. The existing UI indexes these assets without uploading them.

## Compile before the externally authorized generation

~~~bash
python3 -m studio_factory.art_contracts --repo . validate
python3 -m studio_factory.art_contracts --repo . compile S14 --output /tmp/S14-compiled.json
~~~

The compiled JSON contains the exact `prompt`, `global_negative_prompt` and `payload_sha256`, plus Canonical motion/sound and prop/character continuity. The **actual externally sent payload must match these exact values** to enter the v4.2 strict path. If it does not match, record as an investigation/legacy candidate, never relabel it as a matched v4.2 production.

## Receipt schema (operator-filled, no automatic fake receipts)

~~~json
{
  "schema": "studio.generation-receipt.v2",
  "project": "j4-async-succession",
  "shot_id": "S14",
  "candidate_id": "S14-take-001",
  "producer": "ACTUAL_OPERATOR_ID",
  "provider": "ACTUAL_PROVIDER",
  "provider_run_id": "ACTUAL_EXTERNAL_RUN_ID",
  "model": "ACTUAL_MODEL",
  "model_version": "ACTUAL_VERSION",
  "generated_at": "2026-11-23T00:00:00Z",
  "seed": null,
  "settings": { "aspect_ratio": "9:16" },
  "credits": 0,
  "sent_prompt": "MUST_EQUAL_COMPILER_PROMPT_EXACTLY",
  "sent_negative_prompt": "MUST_EQUAL_CANONICAL_NEGATIVE_EXACTLY",
  "compiled_payload_sha256": "64_HEX_DIGITS_FROM_COMPILED_RECORD",
  "generation_gate_at_time": "EXTERNALLY_APPROVED",
  "authorization_evidence": {
    "owner": "ACTUAL_EVIDENCE_REFERENCE",
    "director_estimate": "ACTUAL_EVIDENCE_REFERENCE",
    "account_balance": "ACTUAL_EVIDENCE_REFERENCE",
    "rights": "ACTUAL_EVIDENCE_REFERENCE"
  },
  "reference_assets": [],
  "output": {
    "relative_path": "extra/candidates/S14-take-001.png",
    "media_type": "still",
    "sha256": "64_HEX_DIGITS_OF_ACTUAL_ORIGINAL_OUTPUT"
  }
}
~~~

All uppercase placeholders above must be replaced with actual receipts. The example is **not a valid intake record**. `EXTERNALLY_APPROVED` is a historical assertion, not a way for this software to grant approval. The checker currently verifies the structure/existence of external authorization reference strings, **not their authenticity or signatures**. No output from this script may authorize any new generation.

## Reviewer evidence schema

Two different review records must each bind to the exact same `candidate_id`, `shot_id`, output-media SHA-256 and compiled-payload SHA-256. The `reviewer_id`s must be different from one another and the Producer. Each required **still-mode** check must include:

~~~json
{
  "schema": "studio.g2-review.v2",
  "candidate_id": "S14-take-001",
  "shot_id": "S14",
  "reviewer_id": "INDEPENDENT_REVIEWER_ID",
  "media_sha256": "EXACT_OUTPUT_MEDIA_SHA256",
  "compiled_payload_sha256": "EXACT_COMPILED_PAYLOAD_SHA256",
  "observations": {
    "S14.AUDIENCE_PRESENT": {
      "observed": false,
      "media_sha256": "EXACT_OUTPUT_MEDIA_SHA256",
      "full_frame": true,
      "frame_at_ms": 0,
      "evidence_note": "Explain observable action and its contradiction"
    }
  }
}
~~~

The observation object above shows **only one** check, so it will be blocked until every S14 still-mode P0 is independently reviewed. For localized clues, use a normalized `roi_norm:[x,y,w,h]` box instead of `full_frame:true`. The program checks box validity but does **not** visually determine whether the object exists.

## Run exact verification

~~~bash
python3 -m studio_factory.evidence_gate \
  --repo . \
  --assets "$HOME/Higgsfield-Private/J4" \
  --receipt "$HOME/Higgsfield-Private/J4/extra/g2_receipts/S14-take-001.json" \
  --review "$HOME/Higgsfield-Private/J4/extra/g2_reviews/S14-take-001/reviewer-A.json" \
  --review "$HOME/Higgsfield-Private/J4/extra/g2_reviews/S14-take-001/reviewer-B.json" \
  --output "$HOME/Higgsfield-Private/J4/extra/g2_reports/S14-take-001.json"
~~~

Then restart the normal local review server (`docs/LOCAL_REVIEW.md`) and open the **候選證據** tab. It shows local media preview, receipt, reviewer consensus, disputed cues and still-incomplete temporal requirements. The server refuses generic PASS on both G2 art contract and candidate entries.

## Result taxonomy

| State | Meaning | Can proceed to final art acceptance? |
| --- | --- | --- |
| `BLOCKED_INVALID_RECEIPT` | Missing/wrong source prompt, wrong output digest, unsafe or missing path, unsupported media | No |
| `BLOCKED_INDEPENDENT_REVIEW` | Fewer/more than two independent reviews | No |
| `BLOCKED_EVIDENCE_INVALID` | Reviewer IDs, check evidence or source hashes inconsistent | No |
| `STATIC_REJECTED_BY_TWO_REVIEWERS` | Both viewers saw a required P0 failure | No |
| `STATIC_DISPUTED_NEEDS_ADJUDICATION` | Reviewers disagree on at least one P0 | No |
| `STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN` | Static claims agree and bytes/receipt are well formed | Not yet: temporal, sound, rights, director and actual pixel semantics remain unproven |

## Proof boundary

Real uploaded stills and model receipts for the original six-panel failure are not recoverable from the contact sheet alone. The six negative v4.1 observations remain **forensic** rather than authentic provider receipts. Do not forge `provider_run_id`, exact sent prompts, seed or approvals to satisfy this gate.

Current v4.2 media signature check is intentionally coarse (PNG/JPEG/WebP or MP4/WebM header); decoder/playback and visual truth must be independently tested. Review identities are **self-attested strings** and require a later authenticated reviewer/authorization service for enterprise-grade signing. No temporal Gestalt/optical change, S04/S24 prop identity, S11/S22 origami continuity or S14 audio interpretation can be approved with a still.

Zero image/video generation, no pay-per-use calls, no publishing, no original Canon edits and no merge to main.
