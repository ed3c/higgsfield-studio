# J4 S13｜靜幀 Eval v1

`HFC-EVAL-DELTA-v1` · HFC-07～10=A · HFC-E11=B · S13 first.

## Accepted delta

Use the pinned, rights-reviewed artwork images to judge the transferable optical/material method. Keep Artwork and Shot evidence separate, and require both review panels before considering Fusion. Reconcile the earlier A/B only when the original bytes, sent text and comparable settings bind to the pinned run. Keep the Vision Judge advisory. Save the exact media, prompts, evidence and Owner decision in the versioned run or freeze record. Promote a recipe only after a second independently accepted, comparable success and its regression replay. Stop on no information gain, unresolved hard failure, unsupported source or effect, or missing rights or execution authority.

The pilot scope is S13 key contact on the official Higgsfield website with zero-credit preflight. The extracted diagnostic package is read-only input. A batch-level balance reconciliation cannot authorize another run. Earlier A/B and six-panel reviews remain historical evidence with their original limits.

## Evaluation and authority

| Gate | Owner → Consumer and independent Oracle | PASS test | Negative / incomplete test | Actual S13 |
|---|---|---|---|---|
| E01 Source lock | Canonical/Compiler → Test Manager. Exact pinned manifest and local compiler oracle | S13 project, run and compiler hashes match | Changed manifest, project, shot or compiler rejected | PASS |
| E02 Artwork provenance | Research/Rights → Art Direction. Rights reviewer and actual image bytes | Each pinned original is bound to reviewed images and private-review rights | Wrong source or hash, missing original, or incompatible rights prevents visual acceptance | NOT_RUN |
| E03 A/B reconciliation | Evidence → Shot. Expected role, exact prompt and distinct output records | A1/B1/A2/B2 replay against the compatible bundle | Swapped prompt label or duplicate output rejected | PASS for this fresh diagnostic A/B. Older six-panel cause UNKNOWN |
| E04 Cost | Generation/Cost → Test Manager. Official owner-facing service readback | Historical counters reconcile seven Unlimited results and zero credits | Changed balance, wrong surface or counter mismatch rejected. Fresh per-submit preflight needs separate evidence | PASS for batch replay. Live preflight NOT_RUN |
| E05 Bytes and sent prompt | Evidence → Eval. Compiler and recomputed SHA-256 | Seven originals and all five sent prompt texts match. B matches the compiler exactly | Missing bytes are inconclusive. Substituted bytes or prompt rejected | PASS |
| E06 Artwork | Art Direction → Composition. Two independent human reviewers | Material method visible in the pinned artwork and the separate ART study | One reviewer, virtual reviewer, missing indication or hard fail prevents promotion | NOT_RUN |
| E07 Shot | Director/Shot → Composition. Two independent human reviewers | B3 passes all five canonical static checks | Exterior piano, missing contact/reflection, or self-review prevents promotion | NOT_RUN |
| E08 Fusion | Composition → Review. Exact prompt lineage and two independent human reviewers | C1 binds B3 and ART. Both source panels pass and all static/fusion criteria survive | Cross-tagged takes, missing branch review or disagreement blocks fusion approval | Mechanical lineage PASS. Human QC NOT_RUN |
| E09 Freeze | Project Owner → Review Studio. Explicit human decision for exact bytes | Approval binds C1, run, prompt and media hashes. Freeze includes attestation manifest digest | Wrong hash, missing approval or a producer self-approval yields no frozen take | NOT_RUN |
| E10 Recipe | Test Manager → Production. Another independent, comparable success and the regression replay | A genuinely distinct, rights-cleared and independently accepted run reproduces the credited method | Same run, same artifact or merely similar output cannot establish reusability | NOT_RUN |
| E11 Vision | Vision Judge → independent human reviewers | Findings remain advisory and cannot satisfy any panel or approve/freeze | A vision result submitted as a review is rejected | Enforcement PASS. Vision Judge invocation NOT_RUN |

Shot QC inherits the IDs and polarities from the canonical G2 contract. For ART, reviewers record the identifiable method in the direct artwork source, the visible salt deposits on the study's mechanism, and the lever contact and obstruction. For Fusion, reviewers additionally record how material damage and function coexist, and whether the wafer-to-key reflection reads without decorative notation. Attach a region or a full-frame reason to every observation. If two reviewers disagree, the hard gate stays closed until adjudication.

## Run the real replay

Use the private `J4-S13-image-loop.zip` previously delivered to the owner. Compare its SHA-256 to the pinned contract before extracting. Execute from the integrated branch:

~~~sh
python3 -m studio_factory.s13_eval --evidence /path/to/extracted-private-evidence
python3 -m unittest studio_factory.tests.test_s13_eval -v
~~~

Optional `--attestations /path/to/private-attestations.json` consumes a run-bound file with these records:

- `run_sha256` and actual `producer_id`.
- `artwork_sources`: one entry per pinned `source_url`, with `scope: PRIVATE_REVIEW`, actual `reviewer_id`, `rights_evidence_ref`, asset-root-relative `image`, and `image_sha256`.
- `reviews.ART`, `reviews.B3`, `reviews.C1`: two records per take with `kind: human`, actual `reviewer_id`, `media_sha256`, `prompt_sha256`, and `observations` keyed by the criterion IDs emitted by the CLI. Each observation has `observed`, matching `media_sha256`, `evidence_note`, and `full_frame: true` or `roi_norm`. Use `observed: false` when a prohibited beach piano is absent.
- `owner_approval`: actual `owner_id`, `decision: APPROVE_STATIC_FREEZE`, `take: C1`, and matching `run_sha256`, `media_sha256`, `prompt_sha256`.

Only actual independent human and rights evidence belongs in this file. The program checks attested fields and digests. It does not authenticate reviewer identity, infer rights, or inspect image meaning. Keep original files and human records private.

A clean replay returns `DIAGNOSTIC_VERIFIED_FORMAL_HOLD`. Exit status zero means diagnostic replay succeeded. A later, valid static freeze returns `STATIC_FROZEN_RECIPE_PENDING`. The current CLI stops there until a separate qualifying run exists. Existing G2 v4.2 formal receipt acceptance, live generation approval, audiovisual timing and publication remain separate. The previous experimental C1 is not a canonical G2 compiler receipt or evidence that its original branch inputs were independently approved before submission.
