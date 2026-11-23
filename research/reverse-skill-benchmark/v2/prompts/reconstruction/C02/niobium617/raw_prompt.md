# niobium617 @8eb9b0d — image branch, target gpt_image, kind=prompt (text-to-image)

Pipeline: `analyze_image.py <masked ref> -o local_features.json` (network namespace disabled via `unshare -rn`) → agent semantic_analysis (vision review of the frame) → `prompt_compiler.py all --analysis semantic.json --models gpt_image --auto -o compiled.json` (network disabled).

Compiler prompt sha256 (as reported by the tool): `2223f1b93f1f6521800e4463a2381453fc14d0faa1d09ee013736c9551addff2`; template `gpt_image` (display name 'GPT Image 2.5' — no 2.6 template exists at this commit).
Filter: blocked=False, matches=[]; auto score 80.5 (B, approximate).

## Compiled prompt (verbatim)

```text
Create an image with the following specification.

Subject: the long polished silver hood of a retro-futuristic car with two rounded white fender pods, each carrying a small American flag on a thin staff
Position: hood spans the full width of the lower third; pods at the left and right edges; flags just above each pod
Scale: hood occupies about the bottom third of the frame
Spatial layout: foreground: the hood and pods; midground: a wide empty avenue with a few vintage cars and small pedestrians on sidewalks with globe street lamps; background: a tall pale stone obelisk at the exact center of the horizon, flanked by neoclassical colonnaded buildings and tall white streamlined towers with ring-shaped platforms; a thin dark band of dashboard along the bottom edge
Scene: a ceremonial city avenue in an alternate retro-futurist mid-century capital, late afternoon
Shot: wide shot
Camera angle: low eye level, straight ahead from behind the windshield
Style: cinematic retro-futurist film still, photorealistic
Lighting: soft hazy late-afternoon daylight from the upper left, gentle reflections on the hood
Color: muted teal-grey, warm stone and silver, low saturation
Composition: strict one-point perspective and left-right symmetry converging on the centered obelisk; empty asphalt corridor as negative space down the middle
Camera: normal lens perspective, slightly soft distance, fine film grain
Material: polished chrome hood with panel seams and rivets, glossy white pods, pale stone, glass towers, asphalt
Constraints: render all text exactly as written; no extra text, logos, or watermarks. no off-center horizon, no modern cars, no saturated colors
```
