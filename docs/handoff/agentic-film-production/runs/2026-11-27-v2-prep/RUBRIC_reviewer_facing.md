# V2 rubric (reviewer-facing; pre-registered 2026-11-27 before any review)

Scored after both stages are delivered. Outcome label: "agent review".

| Id | What | Threshold |
|---|---|---|
| R1 | Review validity checks (hidden negative controls inside the claim set) | all must be handled correctly, otherwise the review is INVALID |
| R2 | Author INFERRED claims judged SUPPORTED or PARTIALLY_SUPPORTED | >= 75% |
| R2 | Author MEASURED claims judged SUPPORTED after checking the measurement file | >= 90% |
| R3 | Blind stage A agreement with author labels: interview/speaker role on the 30 sampled segments | >= 80% (needs >= 10 determinate answers, else INCONCLUSIVE) |
| R3 | Sequence-boundary agreement, ±1 segment tolerance | F1 >= 0.60 |
| R4 | Hard cuts you see in windows → share also present in the author's segmentation (recall) | >= 80% (needs >= 5 hard cuts seen, else INCONCLUSIVE) |
| R4 | Windows where the author has a hard cut: you also see a hard cut | >= 90% |
| R5 | No author claim flagged for forbidden inference (lens/camera fact, prompt/seed, identity) | 0 |

V2 = PASS (agent review) only if R1 is valid and R2–R5 all pass; FAIL if any fails; INCONCLUSIVE if data is insufficient.
