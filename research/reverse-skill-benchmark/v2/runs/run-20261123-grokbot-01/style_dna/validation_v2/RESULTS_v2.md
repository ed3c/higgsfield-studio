# style_v2 validation results (2026-11-23 ~20:45 Asia/Taipei)

**What v2 changed versus v1:** the `Colour:` line only. Targets are unchanged (`style_targets_v1.json`, checked with `check_style_v1.py`).

**Generation:** 6 of 6 generated, all UNLIMITED at 0 credits, from 20:16 to 20:28 Asia/Taipei.
- Each PNG's `hf-job-id` equals the reported UUID.
- Pasted lengths match the files: 3125, 3121, 3110, 3120, 3162 and 3053 characters.
- Operator anomalies, none of them submitted:
  - job 2: a stale clipboard was caught by the length check;
  - the button showed +1 while Unlimited was off, and was toggled on before any click.
- Details are in `../../generations_style_v2.csv`.

## A1: metric gate (`A1_results_v2.json`) → **PASS (set)**. v1 was FAIL.

Values are shown as v1 → v2.

| # | luma | p1 | p99 | sat | a\* | b\* | sharp_c | v2 failed gates | v2 image |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | 57→65 | 2→8 | 210→233 | 88.0→**65.9** | +1.18→**+1.05** | 7.90→**1.44** | 58→138 | a (+0.05 over the limit) | PASS |
| 02 | 108→86 | 19→14 | 224→239 | 43.1→49.5 | −0.07→−0.72 | 4.21→3.62 | 147→196 | — | PASS |
| 03 | 54→60 | 5→12 | 241→253 | 85.7→**50.4** | +1.45→−0.48 | 6.90→**2.36** | 90→130 | — | PASS |
| 04 | 84→70 | 13→13 | 223→234 | 43.4→38.6 | +0.29→−2.11 | 5.02→**1.72** | 158→176 | — | PASS |
| 05 | 59→62 | 7→6 | 233→236 | 79.5→**97.6** | −1.90→−4.09 | 6.39→**6.87** | 80→57 | **sat, b** | FAIL (2 gates) |
| 06 | 74→75 | 18→13 | 206→237 | 45.3→48.2 | −1.37→−1.60 | 4.23→3.64 | 349→**324** | **sharp_c** | PASS (1 gate) |

Set medians, v1 → v2:
- luma 66.8 → 67.4
- p1 10.0 → 12.5
- p99 223.5 → 236.5
- sat 62.4 → 50.0
- a\* +0.11 → −1.16
- **b\* 5.71 → 2.99**
- sharp_c 118 → 157

All v2 medians are inside their hard ranges.

Set rules:

| rule | v1 | v2 | required |
| --- | --- | --- | --- |
| images passing | 4/6 | **5/6** | ≥4 |
| images passing every hard gate | 1/6 | 3/6 | — |
| images with p1 ≤ 12 | 3/6 | 3/6 | ≥3 |

**Fixed:** the warm cast. b\* > 4.5 dropped from 5/6 images to 1/6, and the warm-practical over-saturation is gone (01 and 03 went from 86–88 to 50–66).

**Remaining failures:**
1. **06 macro sharp_c 324** against a hard maximum of 200. This is CG-crisp detail. It persists from v1 (349) and is the largest remaining failure (+62% over the limit).
2. **05 sat 97.6 and b\* 6.87.** This **regressed** from v1 (79.5 and 6.39). The yellow raincoat the shot asks for dominates the frame, and the cooler ambient light makes it pop more. The cause is largely the subject's colour, so the style block should not suppress it.
3. 01 a\* +1.05 is marginal.

## A2: photoreal / Style Fidelity → **PENDING**
Neon is the judge.

## A3: focus plane (`A3_dof_v2.json`) → **PASS (5/6)**
Same method as v1. Cells were re-chosen per v2 image because the compositions moved; the executor chose them, so this is not blind.

| # | ratio v1 → v2 | limit | v2 result |
| --- | --- | --- | --- |
| 01 | 0.21 → 0.11 | 0.35 | ✓ |
| 02 | 0.03 → **0.64** | 0.35 | **✗** |
| 03 | 0.04 → 0.04 | 0.35 | ✓ |
| 04 | **2.29 → 0.26** | 0.6 | ✓ (the far hills are now softer than the horses) |
| 05 | 0.09 → 0.28 | 0.35 | ✓ |
| 06 | 0.02 → 0.01 | 0.35 | ✓ |

On 02, the background cells include the mid-ground fuel pump, which keeps an edge. The distant desert itself looks soft by eye. Record this as a fail anyway: the cells were not changed after the result.

## B1: shot adherence (executor visual check, not blind)
- **01–03, 05, 06:** ✓
- **04:** improved but still weak. The herd reads as galloping with dust, but is small in the middle band, and the rider is small in the centre.

## B2: subject leakage → **PASS (0 leaks)**
None of the items on the forbidden list appear: ruffs, lace collars or pearl headdresses; obelisks, spires, flags or colonnades; aircraft, cliffs or cockpits; uniforms, portals or occult symbols; TUPACABRA, watermarks or captions; or the P2 subjects. The neon signs in 01 are blurred and unreadable.

## Next step: v3 (DRAFT, not generated)
`../STYLE_PROMPT_v3.txt`, `../style_block_v3.txt` (sha256 b6280876…3784) and `../style_block_v2_to_v3.diff`.
- **The one change:** the `Texture:` line. It now asks for vintage-lens, near-wide-open acuity and low micro-contrast, with no crisp engraved or pixel-sharp detail, **even in close-ups and macro**.
- **Target:** 06 sharp_c ≤ 200, with no regression on b\*.
- **Not changed:** the 05 saturation. It is caused by the subject's colour, and fixing it would need either a second variable or a shot-side change.
