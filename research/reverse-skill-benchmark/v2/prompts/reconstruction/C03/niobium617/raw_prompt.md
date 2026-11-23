# niobium617 @8eb9b0d — image branch, target gpt_image, kind=prompt (text-to-image)

Pipeline: `analyze_image.py <masked ref> -o local_features.json` (network namespace disabled via `unshare -rn`) → agent semantic_analysis (vision review of the frame) → `prompt_compiler.py all --analysis semantic.json --models gpt_image --auto -o compiled.json` (network disabled).

Compiler prompt sha256 (as reported by the tool): `2b310639a5099b1e1d24f18e0f6204740ff685f09479d587a732edfdfe17373a`; template `gpt_image` (display name 'GPT Image 2.5' — no 2.6 template exists at this commit).
Filter: blocked=False, matches=[]; auto score 80.5 (B, approximate).

## Compiled prompt (verbatim)

```text
Create an image with the following specification.

Subject: a large dark grey tailless flying-wing aircraft with a small glass canopy bubble and boxy intake on top at the center, three engines glowing orange-white beneath the center trailing pale exhaust haze to the left, faint darker markings near the outer wings
Position: centered horizontally just below the middle of the frame, nearly head-on and seen slightly from above
Scale: wingspan covers about 80% of the frame width
Spatial layout: foreground lower right: a dark out-of-focus cockpit frame intruding; midground: the aircraft low over the water; background: hazy horizon with distant pale cliffs about one third down; upper half: flat pale overcast sky
Scene: a calm grey-green sea under an overcast sky near a coastline
Shot: wide shot
Camera angle: slightly high angle from a chase aircraft
Style: cinematic documentary-style aerial film still, photorealistic
Lighting: flat diffuse overcast daylight, no hard shadows, small hot engine glows
Color: desaturated slate-teal, grey and cold green, low contrast
Composition: strong horizontal silhouette across the center; large negative space of sky above and sea below
Camera: telephoto compression, atmospheric haze, soft film grain
Material: matte dark grey airframe, glass canopy, fine choppy water
Constraints: render all text exactly as written; no extra text, logos, or watermarks. no blue sky, no bright sunlight, no extra aircraft
```
