# P1 blind evaluation — setup record (2026-11-23 ~19:25 Asia/Taipei)

**State: `PARTIAL_EVAL` — packet ready, 0/2 reviewers have scored. No scores, no ranking, no P2 candidate B.**

## Blinding
- The 17 generated P1 images were shuffled with `secrets.SystemRandom`, which has no reproducible seed, and renamed `B0001`–`B0017`.
- Pixels were re-encoded. This removed the website's `hf-job-id` tEXt chunk and the C2PA (`caBX`/`jumb`) manifests, which could otherwise reveal the job, and the prompt through the job.
- Locked masked references are included as `refs/C0x_reference.png`. Case membership (C01/C02/C03) is visible to reviewers because they need it to compare against the right reference; Skill identity is not.
- The sealed key `blind_id → case/skill/replicate/job` is kept in `/workspace/hs-bench-private/run-20261123-grokbot-01/eval/blind_key.json` (mode 600) and in the private Drive `eval/` folder (file `1ln5uKqO1LdArFDnLApZ2mJYuMB0no5ou`, owner-only). Key sha256: `0a49df5e08f6ce106aefc227617c836dc62ddb078f4bbf161a9816e27d5d64fe`. It must not be opened until both sheets are hashed and locked.
- The packet is at `/workspace/hs-bench-review/p1-blind/` on the box and as a tar.gz in the private Drive `eval/` folder (`1yRev8ocdht0DufCBd88P7hRVaw8VKkdp`, sha256 `91b33c8e…0ed6`). File hashes are in `packet_sha256.txt`.

## Reviewers — why this executor did NOT score
- The spec requires two **independent** blind reviewers. It does not forbid model reviewers.
- This executor cannot act as an independent reviewer:
  - It ran all three Skills and wrote every prompt, so it can infer the Skill from image content. For example, Caph prompts carry no concrete subject.
  - It cannot open a second, separate context.
- Self-scoring would be neither blind nor independent, so it was not done.
- **Required next step:** two fresh-context reviewers, each given only the packet folder, following `REVIEWER_INSTRUCTIONS.md`. They can be two vision-model subagents dispatched separately by the orchestrator, or Neon plus one other person.
- Record for each reviewer: identity or type (human or model, and which model), its context isolation, and that it had no access to the key, the repo or the prompts.
- **Bias disclosure to record:** reviewers share the box filesystem; they are instructed not to open other folders, but nothing enforces it technically.

## Aggregation (fixed before any score exists)
- `compute_p1_scores.py` implements spec §7:
  - Weighted score per reviewer, then the mean of the two reviewers.
  - Per case: the mean across replicates. Per Skill: the mean across the 3 cases.
  - A criterion difference greater than 2 between reviewers is flagged for adjudication; original votes are kept.
- **Candidate-B rule, declared by the executor before scoring:** the leading non-Caph Skill becomes B only if its mean exceeds the other by **≥ 0.25** and it leads in **≥ 2 of 3 cases**. Otherwise the result is `INCONCLUSIVE`.
- The result is always labelled **PROVISIONAL**, because of GAP-P1-01: C03/unimage has a single replicate.
