# Grok Bot takeover — Higgsfield Studio / J4 (2026-11-22)

## G2 v4.2 candidate evidence — private local workflows

- Git source: studio_factory/evidence_gate.py; studio_factory/tests/test_evidence_gate.py.
- Contract and runbook: docs/G2_EVIDENCE_GATE_V4_2.md; docs/LOCAL_REVIEW.md.
- On the Mac: $HOME/Higgsfield-Private/J4/extra/candidates/, g2_receipts/, g2_reviews/, g2_reports/.
- Local review UI candidate tab: media preview, exact receipt and two independently attested static review records.
- Never claim an uploaded six-panel montage is six authenticated provider outputs. For each shot, the exact provider prompt, output bytes, model, seed and run ID remain unknown until recovered.
- Two reviewer names are self-attested, not cryptographically verified; neither source/hash check nor report completion is an art/rights/human Director approval.
- Any missing provider receipt, image digest, model permission or reviewer evidence is BLOCKED. Never fabricate a provider-run ID or claim historical external approvals.

---
## G2 failed-keyframe repair — newer proposed branch (2026-11-23)

- Separate Draft PR #3: https://github.com/ed3c/higgsfield-studio/pull/3
- Repair branch: fix/j4-art-mechanism-compiler-g2-20261123 (built on PR #1, NOT main).
- Root-cause and test contract: docs/G2_ART_REPAIR.md.
- Six executable Art/Optical scene graphs + 33 P0 cues: projects/j4-async-succession/contracts/art_mechanism_v4_1.json.
- Forensic observation fixture (manually labeled, NOT pixel-CV-verified): projects/j4-async-succession/qc/six_panel_observations_v4_1.json.
- Compiler and fail-closed reported-observation oracle: studio_factory/art_contracts.py.
- Local review site G2 tab; manual PASS blocked server-side, but actual media and Director acceptance NOT_RUN.
- Six-panel image stored in the existing private Google Drive J4 folder under name j4_G2_failed_six_panel_2026-11-23.jpg; its original attachment SHA-256 is 262fb1137db9f29154eae611c23935885c8facfc012d3349fc9001f6195c57d9. Drive metadata/name/size/private confirmed; download hash NOT_RUN. Never publicly copy that media.
- Actual sent prompts, model/seed, six original image outputs and individual take hashes remain unavailable. Do NOT infer exact producer cause from the human-annotated contact sheet.
- Validate with python3 -m studio_factory.art_contracts --repo . validate and python3 -m unittest discover -s studio_factory/tests -v.

---

## Scope and authority

Take over the reusable creative factory and local review website, including J4 provenance and all currently available sources. This is an inspection, testing and evidence-collection handoff, not approval to pay for AI generation, publish, share private assets, or merge PR #1.

## GitHub source map (PR branch, not main)

- Repo: https://github.com/ed3c/higgsfield-studio
- Draft PR: https://github.com/ed3c/higgsfield-studio/pull/1
- Branch: feat/creative-factory-managers-j4-archive-20261122
- Baseline verified commit before this document: f034789cbf762f5d8a3b90633bdd816150a1c008. Verify current PR head with git rev-parse HEAD and report it.
- docs/LOCAL_REVIEW.md — Mac install, playback, origin/CSRF controls, local database
- studio_factory/review_web.py — HTTP localhost server, media Range, safe archive import, reviews
- studio_factory/review_site/ — responsive offline UI
- studio_factory/README.md, core.py, managers.py — 17 Domain Managers, handoffs/ACK, immutable artifact registry
- studio_factory/seed_archive.py, archive.py and cli.py — archive restore, catalog seeding, user commands
- studio_factory/tests/, .github/workflows/ — test and CI sources
- projects/j4-async-succession/PROJECT.json — canonical project status and timeline
- projects/j4-async-succession/archive/v2_6/ — eight canonical source-derived text files
- projects/j4-async-succession/archive/v2_7/ through v4_0/ — 14 versioned text JSON archives, 124 recoverable items
- projects/j4-async-succession/archive/conversation_attachment_index.json — catalog of 312 surfaced conversation entries
- docs/GROK_BOT_SOURCE_MAP.csv — explicit version→source filename→Manager lookup; 31 high-priority J4 assets and sources
- projects/j4-async-succession/archive/MEDIA_CUSTODY.md — media hashes and missing evidence
- skills/creative-production-factory/SKILL.md — reusable manager workflow
- budget/track.py, budget/ledger.csv, budget/allocation.csv — original cost authority
- prompts/, research/, creators/, templates/, projects/_template/ — shared production library
- skills/vendor/higgsfield-ai-skills/ — pinned historical vendor source and license

Review UI method reference: ed3c/medium-compiler commit 6235a905bb552ce82ff7f239327c5f271c7dc446, file .agents/skills/build-review-interface/SKILL.md. Do not run Medium article-writing stages to build the local J4 review page.

## Google Drive private-asset path

The connected Google Drive account has a NOT-SHARED parent folder Higgsfield-Studio-Private-Assets and a child J4-ASYNC-SUCCESSION. The child contains:
- j4_all_available_resources_lossless_2026-11-22.zip: 76,407,296 bytes, SHA-256 4efe79aa309c193382a82e6c4c56654881df5dbba66df7cfc45df84f0ca3011e
- IMG_7835.mp4, IMG_7836.mp4, IMG_7876.mp4
- IMG_7870.jpeg, IMG_7899.jpeg
The parent additionally contains j4_inventory_2026-11-22.json.

Connected Drive write and metadata readback succeeded. 267 source file entries were SHA-verified before upload, but post-upload full-archive byte-for-byte hash readback has NOT_RUN. Private Drive file IDs/URLs and credentials must be supplied through an authenticated private channel; never put them in this public repo or assume Grok can open the files without explicit authorization.

## Local host paths (proposed; existence on Mac NOT VERIFIED)

- Repository working copy: <REPO_DIR> (PR branch)
- Input archive: $HOME/Downloads/j4_all_available_resources_lossless_2026-11-22.zip
- Extracted asset root: $HOME/Higgsfield-Private/J4
- Asset inventory: $HOME/Higgsfield-Private/J4/MANIFEST/inventory.json
- Extracted files: $HOME/Higgsfield-Private/J4/files/
- Private review database: $HOME/Higgsfield-Private/reviews.sqlite3
- Private optional Drive map: $HOME/Higgsfield-Private/drive_manifest.json
- Runtime Manager registry: <REPO_DIR>/.factory/registry.sqlite3
- Local website: http://127.0.0.1:8765 (accessible ONLY from the running Mac)

Bootstrap and verification commands live in docs/LOCAL_REVIEW.md. Archive import MUST produce verified=267, missing=[], mismatch=[]. Verify ZIP SHA-256 BEFORE extraction. Run python -m unittest discover -s studio_factory/tests -v and python budget/test_track.py. Run python -m studio_factory.seed_archive projects/j4-async-succession --db .factory/registry.sqlite3. Serve via python -m studio_factory.review_web serve --repo . --project j4-async-succession --assets "$HOME/Higgsfield-Private/J4" --db "$HOME/Higgsfield-Private/reviews.sqlite3" --port 8765.

A cloud Grok Bot CANNOT use the Mac's loopback URL. Use a user-authorized local runner or separately approved authenticated private gateway. NEVER bind server to 0.0.0.0, disable CSRF/Origin protections, or expose private assets to a public tunnel to work around permissions.

## J4 hard locks and no-loss rules

25 shots, 90 seconds, 30 fps, 2,700 frames; 9:16 original art film. S18 at 63.700 seconds is the sole global six-cycle interruption, while the sine tone survives. S10 coat B is NOT the main coat A, which has a LEFT hem repair. S11 and S22 paper buildings share origami method but NOT physical identity. S04 and S24 use the same original filament bird. S19 is a fictional broadcast set, NOT real news/summit. S22 paper coastline is an original metaphor, not protected game imagery. Original music and all art-method references require separate rights clearance; studying an installation does not grant permission to copy it. Preserve exact accepted decisions and all historical source versions.

17 Manager domains: portfolio, research, story, art_direction, character, asset, prompt, shot, optical, sound, generation, budget, rights, qc, delivery, provenance, experiment. Owner-only mutation, immutable revision with expected_previous, evidence-backed handoff, consumer ACK, cross-project references only to shared approved methods. New productions do NOT inherit J4's character, rights, budget or paid-generation approval.

## Missing evidence / actionable handoff gates

- HOF-01 P0: Confirm Bot runtime and scopes; clone exact branch, record commit SHA, issue/PR permission.
- HOF-02 P0: Confirm Bot can auth-read Drive; inspect downloaded ZIP and recompute SHA-256. URL does not imply access.
- HOF-03 P0: Perform actual Mac localhost browser end-to-end: 25 shots, 17 Managers, actual MP4 play/pause/seek HTTP Range, image render, text/CSV/JSON/HTML viewer, mobile viewport, PASS/FAIL/DEFER and SQLite persistence across reload.
- HOF-04 P0: Obtain explicit owner-approved filesystem write scope, protected review evidence destination and authority to open PRs. NO merge or paid operations.
- HOF-05 P1: Secure reviews.sqlite3 backup and restoration test. It is not currently preserved in Git or Drive.
- HOF-06 P1: Obtain verbatim full chat export; standardized v2.6 Prompt Book is NOT verbatim. Some intermediate duplicate generated artifacts were only indexed.
- HOF-07 P1: Reconcile auxiliary build code, independent original sources, prior UX evidence and legacy build_animatic schema; do not invent missing inputs.
- HOF-08 P1: Separate art/originality, music, copyrighted media, likeness, rights, contest eligibility and real viewer acceptance from source/CI status.
- HOF-09 P1: Demonstrate a second film namespace reusing shared sources with no cross-project state/rights/budget leakage.
- HOF-10 P2: If remote control is required, design narrowly scoped authenticated Tailscale/private access with an owner-approved local executor; no public localhost proxy.
- HOF-11 P2: Specify Drive object retention, checksum/readback, permission audits, privacy and disaster recovery.
- HOF-12 P2: Test codecs and playback on target Mac browsers/devices and produce reproducible screenshots and media receipts.

## Deliverables Grok must return

1. Current repo exact HEAD, source-to-contract map and complete file inventory with SHA references.
2. Run evidence for Python/CI and actual Mac browser playback. Never report a fixture smoke test as actual production video validation.
3. HOF-01 to HOF-12 evidence matrix: PASS, FAIL, BLOCKED or NOT_RUN with source, producer/owner, consumer, oracle/test command, output path and proof.
4. Minimal non-destructive changes through a reviewable PR, retaining pre-existing owners, historical texts, all prompt revisions and licensing records.
5. READY_FOR_HUMAN_REVIEW or BLOCKED decision. NEVER treat that decision as paid model-generation, social publishing, private-Drive sharing or merge approval.

## Generation / sharing safety

J4 status PRE_PRODUCTION. Generation Gate BLOCKED; latest artistic review/rights/media tests are NOT_RUN. No Higgsfield model API calls or points, no public sharing of originals, no auto-publish, and no merging to main without explicit new owner approval. Preserve the existing 9000-credit monthly plan and 80% guard from budget/track.py. No fake pass states, media, citations, screenshot claims or source paths.
