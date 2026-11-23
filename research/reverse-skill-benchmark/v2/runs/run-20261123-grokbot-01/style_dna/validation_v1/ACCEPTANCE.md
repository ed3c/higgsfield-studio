# style_v1 validation: acceptance criteria (fixed before any render, 2026-11-23 ~20:15 Asia/Taipei)

**Goal (Neon t33u, verbatim):** 「逆向到提示詞生成圖片風格可以自由發揮為止，只學習風格不寫死對象」

**Method alignment:** Neon's Notion page *Higgsfield 電影風格逆向* (read-only, not edited). It prescribes:
- a separate Style-only prompt and Shot-only prompt, accepted independently;
- QC on rendered pixels only;
- 6 metrics.

Our Style side and Shot side are accepted separately; the combined prompt counts as passing only when both sides pass.

## Arms
- **S1 (required, 6 jobs):** `prompts/NN_<id>.txt`, each a shot prompt plus the unchanged `style_block_v1.txt` (sha256 is in `style_v1_jobs.json`).
- **S0 (optional control, 6 jobs):** `controls_shot_only/` contains the same shot prompts with no style block. It isolates the style block's causal effect, matching the Notion step "Style-only / Shot-only 分開生成".
- **Render settings for both arms:** GPT Image 2.6 Sunburst, 16:9, 1K, Medium, website Unlimited at 0 credits, no reference upload, 1 replicate.
- **Moderation refusals:** a refused job counts as a FAIL for that image and is not retried without Neon.

## A. Style side

### A1. Style Fidelity, metric gate
Measured with `check_style_v1.py` + `style_targets_v1.json`. The script reads pixels only and is deterministic.

Hard gates per image:

| gate | condition |
| --- | --- |
| highlights | `white_p99 ≥ 180` (refs: 187 / 195 / 192) |
| black point | `black_p1 ≤ 20` (refs: 10 / 17 / 1) |
| luma | 40–125 |
| saturation | 38–80 |
| Lab a\* | −6…+1 |
| Lab b\* | −4.5…+4.5 |
| centre sharpness | `sharp_c` 15–200 |

**Image passes** when the highlight and black-point gates both pass and at most one other hard gate fails.

**Set passes** when:
- at least 4 of 6 images pass;
- the median of every metric across the 6 images lies inside its hard range;
- at least 3 of 6 images reach the soft black target `black_p1 ≤ 12`.

**Calibration** (`metric_gate_calibration.json`) shows the gate separates the refs from the known failures:

| image set | images passing |
| --- | --- |
| refs | 6/6 |
| P1 | 0/17 |
| P1b | 0/9 |
| all 55 trailer shots | 28/55 (51%) |

The 51% includes the title card and the fire, neon and spark shots. The 4/6 bar is therefore deliberately a bit stricter than the source's own rate on its most extreme shots.

### A2. Style Fidelity, blind human/model oracle
A reviewer sees the 3 refs, then a shuffled set: the 6 S1 images mixed with the 6 S0 controls, or with 6 P1b images if S0 is not run. The reviewer gets no prompts.

Questions per image:
- (a) "Is this a frame from the same film as the refs?" on a 0–5 scale.
- (b) "Photographic live-action or CG/illustration?" Pick one.

**Pass when:**
- the S1 mean is at least 3.5;
- at least 5/6 S1 images score 3 or more;
- at least 5/6 S1 images are judged *photographic*;
- the S1 mean is at least 1.0 above the decoy or control mean.

**Final owner oracle:** Neon judges "攝影寫實的電影風格" as yes or no for the set. Neon's verdict overrides metrics in the FAIL direction only: a metric pass with a Neon FAIL counts as a FAIL.

### A3. Focus plane, the C02 lesson
The reviewer draws a box on the declared FOCUS PLANE and a box on the far background.

**Pass when:**
- Laplacian variance of the background box ÷ that of the focus box is at most 0.35 (at most 0.6 for the wide shot 04);
- this holds in at least 5/6 images.

## B. Shot side and subject freedom

### B1. Narrative Fidelity and Camera Fidelity
Judged by a reviewer who has read the shot prompt only, never the style block. For each image:
- Is the named subject and action visible?
- Is the place or era plausible?
- Do the shot size and camera height match?
- Is the declared FOCUS PLANE the sharpest region?

**Pass when** at least 5/6 images have all four "yes".

### B2. Creative Distance: no subject leakage, hard gate
**Zero** occurrences in all 6 images, judged from pixels by a reviewer. Leakage includes any of:
- **C01-type:** ruffs or lace collars, pearl or jewelled headdresses, red-haired pale freckled woman as a default face, candle-orb backgrounds, courtly costume;
- **C02-type:** obelisks, white streamlined spires or ring towers, chrome car hoods or fender pods, national flags, colonnaded avenues;
- **C03-type:** flying-wing or other aircraft, sea with chalk cliffs, cockpit-frame occluders;
- **trailer-wide:** WWII-coded uniforms, glowing portal rings, occult symbols, the word TUPACABRA or any watermark or text;
- **P2:** the approved P2 subjects (lighthouse keeper, salt pans, moth kite).

A single leak fails the set for subject freedom. No image may also re-create the composition of a ref, judged side by side.

### B3. Causality, only if S0 is run
For at least 4 of 6 shot pairs, S1 has fewer failed hard gates than S0. This shows the style block, not the shot content, produced the look.

## C. Not applicable for stills
**Temporal Consistency:** `NOT_RUN`. It applies only to video and should be added when a Motion/Editing DNA phase starts. Motion, editing rhythm and sound DNA from the trailer analysis stay `NOT_RUN` here.

## Verdict
**style_v1 ACCEPTED** only if A1, A2, A3, B1 and B2 all pass (and B3 if S0 is run).

Otherwise record the failed gates as regression cases and draft `STYLE_PROMPT_v2`. Change one variable per iteration, and never edit v1 in place.
