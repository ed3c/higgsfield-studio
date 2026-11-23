# unimage @db916e7 — Reverse Prompt Mode — C02 (masked S16)

Intake: use case = replication (benchmark P1); backend = GPT Image 2.6 web, text-only; priority = layout, perspective, lighting.

## Scene Auditor
Compliance: OK.
Entity Recognition: tall stone obelisk on a ceremonial avenue (resembles a real landmark, but city is altered with futuristic towers → not named); small American flags (high confidence); vehicle model unknown.
Asset Classification: other — cinematic narrative film still (retro-futurist). Typography-Driven: no. Requires Coordinate Mapping: yes (symmetrical foreground pods, flags, vanishing point).
Art Direction: retro-futurist Americana, muted cinematic realism.
Key Subject: the polished silver hood of a long retro-futuristic car looking straight down a wide avenue toward a distant obelisk.
Observed Facts: hood fills lower third; two rounded white fender pods left and right, each with a small US flag on a staff; one-point perspective to centered obelisk; neoclassical colonnaded buildings and tall white streamlined towers with ring platforms both sides; few vintage cars and pedestrians; dark band at bottom edge.
Weak Inferences: late afternoon; motorcade/parade context.
Fidelity Anchors: low POV behind long silver hood; symmetrical twin pods with flags; one-point perspective to centered obelisk; retro-futurist towers + neoclassical buildings; muted hazy light.

## Detail Scanner
Materials: polished chrome/silver hood with panel seams and rivets, white glossy pods, pale stone, glass towers, asphalt.
Visible Imperfections: soft focus in distance, film grain.
Detected Text: none.
UI / Info Details: n/a.
High-Value Micro Details: thin antenna on hood; small chrome strips on pods; street lamps with globe lights on both sidewalks.

## Spatial Architect
Orientation and Crop: landscape 16:9; wide scene, low eye-level POV.
Lighting and Camera Feel: hazy late-day daylight from upper left, soft reflections on hood; normal lens, centered.
Layout and Visual Flow: hood y≈58–88 across x≈5–95; pods at x≈5–23 and x≈76–94; flags at x≈8–16 / x≈76–83, y≈35–46; obelisk x≈50, y≈0–30; eye travels from hood straight down the avenue to the obelisk.
Negative Space: the empty asphalt avenue in the center.
Coordinate Map: strict left/right symmetry around x=50.

## Prompt Engine — final prompt
A cinematic 16:9 film still from a low viewpoint just behind the windshield of a long, polished silver retro-futuristic car, its curved hood filling the lower third with two rounded white fender pods at left and right, each carrying a small American flag on a thin staff. The car faces straight down a wide, nearly empty city avenue in strict one-point perspective that converges on a tall pale stone obelisk at the center of the horizon. Neoclassical colonnaded stone buildings and towering white streamlined spires with ring-shaped platforms line both sides, with a few vintage cars, distant headlights and small pedestrians on the sidewalks. Soft hazy late-afternoon light from the upper left, muted teal-grey and warm stone palette, glossy reflections on the hood, slightly soft background, film grain, and a thin dark band of dashboard along the bottom edge. Avoid: off-center horizon, modern cars, saturated colors.

Config:
- aspect_ratio: 16:9
- enhance_prompt: off
