# Job slots — run-20261123-grokbot-01

Machine-readable: [`job_slots.json`](job_slots.json) (built by `build_job_slots.py`, shuffle seed 20261123). Same file is mirrored privately at `/workspace/hs-bench-jobs/jobs.json` on the executor box.

**30 slots = P1 18 (3 cases × unimage/caph/niobium617 × 2) + P2 12 (3 cases × caph/B × 2). Ready to submit: 0.**

## Fixed settings for every slot (spec §4–5, manifest `primary_model`)

| Setting | Value |
| --- | --- |
| Surface | higgsfield.ai website, ordinary image page. Never MCP / CLI / API / Canvas / Marketing Studio / Presets |
| Model | **GPT Image 2.6** (not Flare). Spec does *not* allow Seedream; Nano Banana Pro only as a separate, separately verified run, never mixed |
| Ratio / resolution / quality | 16:9 · 1K · same 0-credit tier for all 30 (PR #5 saw Medium, PNG) |
| Unlimited | ON and the submit control shows Unlimited / 0 Credits on the filled form, every time |
| Reference upload to Higgsfield | **Forbidden** (no image-to-image). So no slot should trigger a "Media upload agreement" dialog; if one appears, refuse and stop |
| Order | Serial, in `submit_order`; one job at a time |
| Output | `artifacts/reverse-benchmark-v2/run-20261123-grokbot-01/output/<job_id>.png` outside Git; blind IDs B0001–B0030 assigned privately later |

## Slots

| # | job_id | Status | Blocked by |
| --- | --- | --- | --- |
| 1 | `P1-C01-niobium617-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 2 | `P1-C01-caph-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 3 | `P1-C01-unimage-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 4 | `P1-C01-unimage-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 5 | `P1-C01-caph-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 6 | `P1-C01-niobium617-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 7 | `P1-C02-unimage-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 8 | `P1-C02-unimage-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 9 | `P1-C02-caph-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 10 | `P1-C02-niobium617-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 11 | `P1-C02-caph-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 12 | `P1-C02-niobium617-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 13 | `P1-C03-caph-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 14 | `P1-C03-caph-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 15 | `P1-C03-unimage-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 16 | `P1-C03-niobium617-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 17 | `P1-C03-niobium617-r2` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 18 | `P1-C03-unimage-r1` | BLOCKED_SOURCE | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN |
| 19 | `P2-C01-caph-r2` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 20 | `P2-C01-B-r2` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 21 | `P2-C01-B-r1` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 22 | `P2-C01-caph-r1` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 23 | `P2-C02-caph-r1` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 24 | `P2-C02-B-r2` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 25 | `P2-C02-caph-r2` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 26 | `P2-C02-B-r1` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 27 | `P2-C03-caph-r2` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 28 | `P2-C03-B-r2` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 29 | `P2-C03-caph-r1` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
| 30 | `P2-C03-B-r1` | BLOCKED_ON_P1_SCORES | MS-004 no C01-C03 stills; P0 prompt lock NOT_RUN; G1 live recheck NOT_RUN; P1 blind scores; candidate B undecided; MS-008 subjects not locked |
