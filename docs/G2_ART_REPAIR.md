# G2 v4.1｜Art Mechanism Compiler / Semantic Fidelity Repair

Status: SIX-SHOT VERTICAL SLICE / CANDIDATE_NOT_APPROVED / GENERATION BLOCKED.

## Root-cause boundary
The six-panel contact sheet resembles S02, S04, S06, S11, S13, S14. A human review found missing action/causality/optical evidence. The exact prompts sent to the image provider, model, seed, source references and output hashes are UNKNOWN. No specific provider or Grok step can yet be assigned definitive causal responsibility.

## Newly executable contracts
Input: v2.6 canonical Shot IR and v3.3 optical methods, both pinned to exact historical Git blob SHA-1 values.
Output: project-local contract JSON for six images, each with ranked primary action, scene graph, camera/optical time logic, negatives, and P0 review assertions.
The generic prompt compiler is studio_factory/art_contracts.py. It emits only a non-executable compiled payload. It cannot call Higgsfield, cannot generate images, and cannot unlock paid generation.

Versioned machine artifacts:
- projects/j4-async-succession/contracts/art_mechanism_v4_1.json — source-locked scene graphs and 33 P0 obligations
- projects/j4-async-succession/qc/six_panel_observations_v4_1.json — six manual observations from provided contact sheet, explicitly WITHOUT a verified output binary
- studio_factory/tests/test_art_contracts.py — negative/regression, revision lock, modality, role-separation tests
- docs/G2_ART_REPAIR.md — this handoff

## Six hard failures
| Shot | Hard condition | Cross-frame effect NOT proven by a still |
| --- | --- | --- |
| S02 | Two humans transferring ONE bowl; visible local lamp and wet steel reflection | S02/S03 reflection-contour comparison |
| S04 | Initial raw asymmetrical wire with three stable junctions, not pre-completed gold bird | focal rotation/gestalt recognition and S24 joint identity |
| S06 | ONE continuous workshop, repairable lamp handoff, technical sealed light behind glass, NO split screen | focus transfer without scene cut |
| S11 | blue stools and gloves + recognisable miniature unfinished paper house with offset roof/window | same fabrication grammar in S22, not identical prop |
| S13 | piano INSIDE coastal precision-engineering lab, key press and wafer reflection, NOT on beach | failed musical note and material-role reversal |
| S14 | visible applauding people, an EMPTY performer stage, physical audience reflection, no hero gold robe | spatial original applause tied to spectators |

## How to run — no model provider connection
~~~bash
python3 -m studio_factory.art_contracts --repo . validate
python3 -m studio_factory.art_contracts --repo . compile S14 --output /tmp/S14-compiled.json
python3 -m unittest discover -s studio_factory/tests -v
~~~

Independent observation review, once real media and attribution are available:
~~~bash
python3 -m studio_factory.art_contracts --repo . judge /private/candidate-review.json
~~~

Candidate review JSON: shot_id, candidate_id, producer, independent reviewer, media_type (still/video), media_path, media_sha256, observations keyed by exact check IDs; each observation has observed=true/false and evidence_uri. A positive statement does NOT prove imagery when media and evidence are absent.

## Oracle semantics
- Source lock validation: machine check; failures BLOCKED, never silent auto-update.
- Negative cues from the user contact sheet: human-reported REJECTED_BY_OBSERVATION. This is a reason to stop candidate promotion, NOT an assertion that the program performed image recognition.
- Missing real media: media_sha256_verified=false. Human image observations are not cryptographically bound to this screenshot until original bytes are provided.
- Static image: useful to reject missing paper house, split screen, beach piano, empty seats, decorative full bird; cannot prove gradual movement, two-shot identity, audio or viewer recall. Such checks remain pending.
- **Superseded by v4.2:** the original v4.1 single-observer positive review is now always `BLOCKED_V4_2_INDEPENDENT_EVIDENCE_REQUIRED`, even when its output media digest matches. Use `studio_factory/evidence_gate.py` with two independent media-bound reviewers instead. Its best possible outcome `STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN` also does NOT mean artistic, rights, Director or generation approval.
- Actual producer and reviewer identity are presently self-asserted strings, not authenticated signatures. A dedicated identity/evidence layer is required before enterprise approval.
- Rights, generated originality, director acceptance, IP similarity, model credits and actual audiovisual validation remain NOT_RUN/BLOCKED.

For the exact v4.2 receipt/reviewer schemas and private local file paths, see [G2_EVIDENCE_GATE_V4_2.md](G2_EVIDENCE_GATE_V4_2.md). No web UI review PASS can approve the failed six-shot contract.

## Non-goals
No Canonical IR overwrite, historical prompt deletion, reference-artwork copying, image upscaling, image/video generation, provider spend, real audience test, or automatic merge to main.

## Next work
Retrieve the six exact sent prompts, generator/model/version, seed, ref hashes and media SHA-256; attach media privately; independent frame-level and time-based review with reviewer identity; verify original source/reference rights; enforce a generation workflow fail-closed gate before any spend. Extend this schema to the other 19 shots only after these six prove useful.
