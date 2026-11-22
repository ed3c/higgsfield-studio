# Creative Production Factory — reusable Domain Managers

This is an **additive** subsystem. Nothing in the pre-existing \`budget/\`, \`projects/_template/\`, \`skills/vendor/\`, or \`prompts/\` has been overwritten. It does **not** call Higgsfield or spend credits.

## Ownership & isolation

A **Production Orchestrator** coordinates 17 explicitly typed Managers in \`studio_factory/managers.py\`. Each Manager owns its own domain and can only register immutable revisions for that domain. A consumer must ACK a handoff; the producer's output is never silently overwritten. Shared research and methods live under \`shared\`; story-specific records live under \`projects/<slug>\`. A project may reference shared artifacts but cannot directly borrow mutable artifacts from a different project.

| Manager | Owns | Main consumers |
| --- | --- | --- |
| PortfolioManager | production identity, reuse policy | Research, Story, Budget |
| ResearchManager | claims, sources, creator/artwork study | Story, Art Direction, Rights, Provenance |
| StoryManager | script, act/beat contracts, narrative locks | Art, Character, Shot, Sound |
| ArtDirectionManager | style, reference methods, physical material rules | Character, Asset, Prompt, Optical |
| CharacterManager | fictional identity/wardrobe/pose consistency | Asset, Prompt, Shot, QC |
| AssetManager | immutable media/prop references, provenance digests | Prompt, Shot, Optical, Sound |
| PromptManager | image/motion/sound prompt templates and deltas | Shot, Sound, Generation |
| ShotManager | canonical 30 fps Shot IR and take eligibility | Optical, Sound, Generation, QC |
| OpticalManager | illusion IR, object states, recall arcs | Shot, Experiment, QC |
| SoundManager | 5 stems, sonic object registry, phase continuity | QC, Delivery, Experiment |
| GenerationManager | candidate generation request/result IDs | QC, Budget, Provenance |
| BudgetManager | credit estimates and external-ledger cross-checks | Generation, QC |
| RightsManager | public/private licensing, human likeness, contest eligibility | Generation, QC, Delivery |
| QCManager | evidence-backed machine/creative/rights gates | Generation, Delivery |
| DeliveryManager | export profile, publish receipts, provenance | Provenance, Portfolio |
| ProvenanceManager | claim ↔ source ↔ producer ↔ consumer mapping | Research, Rights, QC |
| ExperimentManager | preregistration, randomization, blinded results | Art, Prompt, QC |

Only explicit allowed edges in \`HANDOFFS\` may exchange events. For example:

\`\`\`text
Research -> Story -> ArtDirection -> Prompt -> Shot -> Generation -> QC -> Delivery
                  |                        |             ^       ^
                  +-> Character -> Asset ---+             |       |
                  +-> Sound -------------------------------+       |
Rights -----------------------------------------------> Generation/QC
Budget -----------------------------------------------> Generation
Optical -> Experiment -> QC
Provenance <--- source references, hashes, handoffs, delivery receipts
\`\`\`

This is a **DAG of accountable artifacts**, not a claim that all 17 agents should run simultaneously. A domain remains the owner of its evidence and decisions. Review/repair paths are new immutable versions rather than erasing historical records.

## Data contracts

An immutable artifact is \`{id, namespace, domain, key, revision, digest, uri, payload, supersedes}\`. Cross-domain handoffs are \`{event_id, project, producer, consumer, asset_id, idempotency_key, evidence, state}\`. Downstream ACK records acceptance of the **exact artifact ID**, not an ambiguous latest path.

\`publish\` uses optimistic revision matching: the caller must pass \`expected_previous\` for an update. \`handoff\` is idempotent; reusing a key with different content fails. \`shared\` artifacts require explicit source and rights fields. External media remains at its original location; references include its SHA-256 in the payload.

State labels: \`NOT_RUN\`, \`PENDING\`, \`ACK\`, \`BLOCKED\`, \`APPROVED\`. There is no manufactured "PASS" without an evidence record.

## Eight reusable phases

1. **Reverse engineering / research** — original sources and allowed methods
2. **Story development** — logline, screenplay, causal/time contracts
3. **Visual development** — character, location, props, keyframe composition
4. **Previs** — Shot IR, Sound IR, animatic, timeline and continuity checks
5. **Production** — only after separate generation approval and budget/rights gates
6. **Post** — edit, original sound, subtitles and deliverable profiles
7. **QC** — mechanical/creative/sound/rights/contest evaluations with real evidence
8. **Delivery and knowledge capture** — immutable references, receipts, library promotion

## CLI

Python 3.10+, standard library only:

\`\`\`bash
python -m studio_factory.cli --db /tmp/factory.sqlite3 init j4-async-succession
python -m studio_factory.cli --db /tmp/factory.sqlite3 publish research shared study-01 https://museum.example/ '{"source":"https://museum.example/","rights":"method-only"}'
python -m studio_factory.cli --db /tmp/factory.sqlite3 manifest j4-async-succession --output /tmp/manifest.json
python -m unittest discover -s studio_factory/tests -v
\`\`\`

To rebuild historical text from a repository-archived version:

\`\`\`bash
python -m studio_factory.archive projects/j4-async-succession/archive/v3_9/conversation_text_archive.json /tmp/j4-v3_9
\`\`\`

\`registry.sqlite3\` is runtime state: store it in a secured persistent volume and back it up independently. The Git repository retains immutable snapshots, contracts, schemas and provenance. Do not commit credentials or personally identifying raw media.

## Credit safeguards

\`require_generation_gate\` returns eligibility information only. It does not contact Higgsfield, grant authority, debit points, or execute any render. Four independent evidence gates are required: \`owner_approval\`, \`director_estimate_posted\`, \`live_balance_checked\`, \`rights_review\`. The project credit limit is a **planning cap**, not verified account balance; verify the existing \`budget/track.py\` ledger and the provider's live price and available credits immediately before every paid operation.

The project J4 approval remains **BLOCKED**, independent of stored prompt readiness. Existing 9,000 point allocation buckets and historical ledger remain authoritative.

## Limits / next engineering steps

Current implementation is a tested **offline metadata/control-plane minimum slice**, not a deployed agent swarm or production media store. Database concurrency, verified external signatures, server-side authentication, immutable object-store retention, encrypted private footage, GitHub Actions protection and provider integrations require separate owner-approved implementation. Do not label these \`PASS\` before real tests.
