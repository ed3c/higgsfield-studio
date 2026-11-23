# unimage @db916e7 — Reverse Prompt Mode — C01 (masked S30)

Intake: use case = replication (benchmark P1); backend = GPT Image 2.6 web, text-only; priority = layout, lighting, materials.

## Scene Auditor
Compliance: OK (period costume portrait, no disallowed content).
Entity Recognition: Unknown person (period court costume; no high-confidence identity).
Asset Classification: other — cinematic narrative film still. Typography-Driven: no. Requires Coordinate Mapping: yes (main subject + background figure + candle).
Art Direction: muted, low-key historical-drama cinematography.
Key Subject: young pale woman with copper-red hair and freckles in a huge white lace cartwheel ruff and a pearl-studded jeweled headdress, facing camera.
Observed Facts: centered frontal medium close-up; ruff fills lower half; pearl drop earrings; dark beaded gown with gold; bearded man out of focus right background; lit candle upper left; dark wood interior.
Weak Inferences: eyes slightly wet / solemn mood; interior is a palace chamber.
Fidelity Anchors: 16:9 medium close-up, subject centered; enormous white lace ruff; out-of-focus bearded man right; single candle flame upper left; low-key dark background.

## Detail Scanner
Materials: fine white lace, pearls, gold and jewel settings, black beaded embroidery, matte skin with freckles, wax candle.
Visible Imperfections: light film grain, slight halation around the flame.
Detected Text: none (watermark area masked; ignored per rule).
UI / Info Details: n/a.
High-Value Micro Details: freckles across nose and cheeks; pearl drop earrings; tiny jewels in the headdress band.

## Spatial Architect
Orientation and Crop: landscape 16:9; medium close-up, chest up.
Lighting and Camera Feel: soft diffuse key from front-left, deep shadows, warm candle practical; long-lens portrait feel with shallow depth of field.
Layout and Visual Flow: face at center (x≈47, y≈30); ruff spans x≈15–80, y≈35–100; eye moves face → candle (x≈4, y≈10) → blurred man (x≈90, y≈35).
Negative Space: dark soft background upper left and right.
Coordinate Map: woman center; candle top-left corner; bearded man right edge, out of focus.

## Prompt Engine — final prompt
A cinematic 16:9 film still, medium close-up of a young pale woman with copper-red hair and light freckles, centered and facing the camera with a still, solemn, slightly teary expression. She wears an enormous white lace cartwheel ruff that fans out around her neck and fills the lower half of the frame, a pearl-and-jewel studded headdress framing her hairline, small pearl drop earrings, and a dark gown embroidered with gold and black beads. Behind her on the right, a bearded man in dark clothing stands out of focus; in the upper left a single lit candle glows as a soft orb, and the dim wood-paneled interior falls into darkness. Soft diffuse key light from the front left, deep shadows, muted desaturated palette of ivory, warm skin and near-black, shallow depth of field, gentle film grain and slight halation on the candle flame. Avoid: sharp background, saturated colors, extra people in focus.

Config:
- aspect_ratio: 16:9
- enhance_prompt: off
