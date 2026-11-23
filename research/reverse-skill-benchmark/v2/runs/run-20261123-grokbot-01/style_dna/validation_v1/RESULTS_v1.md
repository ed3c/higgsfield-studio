# style_v1 validation results (2026-11-23 ~20:25 Asia/Taipei)

**Generation:** 6 of 6 generated, 0 refusals, UNLIMITED at 0 credits. Per-file details are in `../../generations_style_v1.csv`.
- Each PNG's `hf-job-id` equals the reported UUID, and each file's length equals its pasted length.
- The S0 shot-only controls were **not** run, so B3 is `NOT_RUN`.

## A1: metric gate (`A1_results_v1.json`) → **FAIL (set)**

| # | luma | p1 | p99 | sat | a\* | b\* | sharp_c | failed hard gates | image |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 night market | 57.3 | 2 | 210 | **88.0** | **+1.2** | **+7.9** | 57.9 | sat, a, b | FAIL |
| 02 desert | 107.6 | 19 | 224 | 43.0 | −0.1 | 4.2 | 147.3 | — | PASS |
| 03 potter | 53.9 | 5 | 241 | **85.7** | **+1.4** | **+6.9** | 89.6 | sat, a, b | FAIL |
| 04 horses | 83.5 | 13 | 223 | 43.4 | +0.3 | **+5.0** | 157.7 | b | PASS |
| 05 subway | 59.4 | 7 | 233 | 79.5 | −1.9 | **+6.4** | 80.5 | b | PASS |
| 06 watch | 74.1 | 18 | 206 | 45.3 | −1.4 | 4.2 | **349.2** | sharp_c | PASS |

Set rules:
- Images passing: 4/6 against a required 4 → OK.
- Soft black target (p1 ≤ 12): 3/6 against a required 3 → OK.
- Every metric median inside its hard range: **b\* median 5.71 > 4.5 → FAIL.**

**Fixed versus P1b:** highlights reach white in every image (p99 206–241; P1b was about 162), and blacks are true black.

**Remaining failure:** a warm cast in 5 of 6 images (b\* 5.0–7.9), and over-saturation where warm practical light dominates (01 and 03). The 06 macro is CG-crisp (sharp_c 349).

## A2: Style Fidelity (blind reviewers and Neon) → **PENDING**
The model blind reviewers have not run. Neon is the final photoreal judge.

## A3: focus plane (`A3_dof_v1.json`) → **PASS (5/6)**
Ratio = Laplacian variance of the background cells ÷ the focus cells, on a 6×8 grid.

| # | ratio | limit | result |
| --- | --- | --- | --- |
| 01 | 0.21 | 0.35 | ✓ |
| 02 | 0.03 | 0.35 | ✓ (low-texture background caveat) |
| 03 | 0.04 | 0.35 | ✓ |
| 04 | **2.29** | 0.6 | **✗**: far hills are sharper than the horses |
| 05 | 0.09 | 0.35 | ✓ |
| 06 | 0.02 | 0.35 | ✓ |

The cells were chosen by the executor, which knows the prompts. The spec asks for blind reviewer boxes, so treat this as provisional.

## B1: shot adherence (executor visual check plus the operator's notes; not blind) → **PASS (5/6)**
- **01:** cook ladling broth, steam, single bulb, wet alley; distant signs blurred and unreadable. ✓
- **02:** young mechanic crouching to true the wheel, fuel pump, empty road. ✓
- **03:** potter's hands on the jar, kiln fire, mud-brick and reed setting. ✓
- **04:** ✗. The horses are tiny and do not clearly read as galloping, though there is dust. No lead horse holds focus. The rider is small, in the lower-left third. The sky is dramatic with a glowing sun.
- **05:** profile, yellow raincoat, streaking train, pillar framing. ✓
- **06:** open watch with a cracked crystal, seeds, linen, window light from the right. ✓ The dial numerals are part of the object, not caption text.

## B2: subject leakage (visual check against the forbidden list) → **PASS (0 leaks)**
None of the following appear in any image:
- ruffs, lace collars, pearl headdresses, red-haired freckled default faces, candle-orb backgrounds
- obelisks, spires, chrome hoods, flags, colonnades
- aircraft, seas with cliffs, cockpit frames
- uniforms, portals, occult symbols
- TUPACABRA or any watermark or caption
- the P2 subjects

No image re-creates a ref composition.

## Verdict
**style_v1 NOT ACCEPTED.** A1 failed on colour (b\*), and A2 is still pending.
- Regression case R-v1-01 (colour): warm-light scenes produce a global warm or orange cast.
- Regression case R-v1-02 (shot side): the wide shot 04 has no focus hierarchy and weak action. It is logged for a **shot-prompt** fix, separate from the style iteration.

## Next round: style_v2 (one variable only)
v2 changes **only** the `Colour:` line of the style block: neutral-to-cool white balance across the whole frame, with warm light kept local. See `../style_block_v1_to_v2.diff`. The shot prompts are unchanged from v1. The files are in `../validation_v2/` and `/workspace/hs-bench-jobs/style_v2_prompts/`. **Not generated.**

Expected effect, to be measured:
- b\* median ≤ 4.5;
- 01 and 03 saturation below 80;
- no change in the p99 and p1 wins.

The 06 crispness (sharp_c 349) and the 04 shot issue are intentionally left for later single-variable rounds.
