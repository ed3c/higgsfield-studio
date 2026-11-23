# niobium617 @8eb9b0d — image branch, target gpt_image, kind=prompt (text-to-image)

Pipeline: `analyze_image.py <masked ref> -o local_features.json` (network namespace disabled via `unshare -rn`) → agent semantic_analysis (vision review of the frame) → `prompt_compiler.py all --analysis semantic.json --models gpt_image --auto -o compiled.json` (network disabled).

Compiler prompt sha256 (as reported by the tool): `848f1263566aa30f7a67c6ceb55950946857eedab73e84f942d98bad3dcf9224`; template `gpt_image` (display name 'GPT Image 2.5' — no 2.6 template exists at this commit).
Filter: blocked=False, matches=[]; auto score 80.5 (B, approximate).

## Compiled prompt (verbatim)

```text
Create an image with the following specification.

Subject: a young pale woman with copper-red hair and light freckles, solemn and still, eyes slightly wet, wearing an enormous white lace cartwheel ruff, a pearl-and-jewel studded headdress, small pearl drop earrings and a dark gown embroidered with gold and black beads
Position: centered, face in the upper-middle of the frame, looking straight at the camera
Scale: head and ruff fill about two thirds of the frame height; chest-up crop
Spatial layout: foreground: the woman in sharp focus; background right: a bearded man in dark clothing, out of focus; upper left corner: a single lit candle as a soft glowing orb; dim wood-paneled interior falling into darkness
Scene: a dim candlelit palace chamber
Shot: medium close-up
Camera angle: eye level, frontal
Style: cinematic historical drama film still, photorealistic
Lighting: soft diffuse key light from the front left, low contrast on the face, deep shadows, warm candle practical with slight halation
Color: muted, desaturated ivory, pale skin, muted gold and near-black; neutral to slightly cool grade
Composition: centered symmetrical portrait framing with the ruff spreading across the lower half; dark negative space in the upper corners
Camera: long-lens portrait look, shallow depth of field, fine film grain
Material: fine white lace, pearls, gold settings, black beaded embroidery, freckled skin
Constraints: render all text exactly as written; no extra text, logos, or watermarks. no sharp background, no saturated colors, no additional people in focus
```
