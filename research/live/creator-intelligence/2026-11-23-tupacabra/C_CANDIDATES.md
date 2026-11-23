# C01–C03 candidate frames — NOT LOCKED (awaiting owner pick)

- **Source:** SRC-T002 4K (sha256 `f376471f…2d3687`), sampled at the midpoint of each scene-detected shot, **deterministic centre crop 3822×2150 → Lanczos 3840×2160 (16:9)**. Crop sha256 per frame in `c_candidates_measured.json`; files are private.
- **Contact sheet (private):** `/workspace/hs-bench-jobs/c_candidates_sheet.jpg` (sha256 `e0a7ef12…dbc1`).
- **Spec criteria (§3):** C01 portrait with intentional foreground/background separation; C02 environment/establishing with distinct vanishing point, lighting and set geometry; C03 prop/action with strong silhouette or scale contrast.
- **Common risk:** every frame carries a small "TUPACABRA" watermark bottom-centre. A reverse Skill that transcribes it would trigger the spec's text/watermark hard-fail. Decide before lock: keep the frame as-is, or apply a fixed, documented mask.
- Analysis below is `INFERRED` except the `MEASURED` line.

## C01 — Portrait

### C01a · S30 @ 39.65 s — Elizabethan woman in ruff (**recommended**)
- **Composition:** medium close-up, subject left-of-centre at the third, eyes on upper third; a bearded man soft in the right background; a lit candle top-left as a practical.
- **Lens:** long-lens look (≈85–100 mm), wide aperture; shallow DOF, background bokeh.
- **Lighting:** soft frontal-side key from the left (window/candle motivation), gentle fill, low contrast on skin; warm candle highlight.
- **Palette/grade:** ivory lace + pale skin vs near-black background; muted warm-neutral grade; MEASURED luma 74, saturation 56, dominants #a9a7a5 / #0b0f11 / #28241e.
- **Texture:** lace ruff micro-detail, freckles, pearl headdress specular, fine grain.
- **Era:** late 16th century court.
- **Signature traits:** period realism, a quiet portrait inserted into a montage, practical-light warmth against cold shadows.
- **Why:** the cleanest fg/bg separation in the trailer; no text, insignia or living-person likeness. The P2 lighthouse keeper maps directly onto it.

### C01b · S28 @ 33.98 s — inventor reading a document
- Close-up, subject right-of-centre, white paper as a bright foreground occluder; long lens, shallow DOF; cool top/side key with a strong shadow side; luma 73, highest contrast (stddev 76). Early-20th-century.
- **Risk:** reads as a lookalike of a real historical person (Tesla-like). Paper has faint printed text.

### C01c · S18 @ 23.52 s — naval officer on a ship bridge
- Medium shot, subject right third, crew soft in the left background, bright window frames behind (high-key backlight); teal-green grade (saturation 92); WWII–1940s polar era.
- **Risk:** legible "R. E. BYRD / USN" name patch and cap eagle insignia → high text-leak / real-person risk.

## C02 — Environment

### C02a · S16 @ 21.10 s — Washington Mall from a car hood (**recommended**)
- **Composition:** textbook one-point perspective. The road converges on the obelisk at centre; flanking neoclassical buildings and a symmetrical car hood with chrome fins in the foreground frame it.
- **Lens:** normal-to-wide (≈35 mm look), deep focus.
- **Lighting:** overcast flat daylight, soft reflections on the chrome hood.
- **Palette/grade:** grey-green slate, muted reds of two small flags; luma 70, saturation 58.
- **Texture:** polished metal, stone, period cars.
- **Era:** retro-futurist 1950s Washington.
- **Signature traits:** an Americana period setting with a sci-fi object (the hood) and symmetrical framing.
- **Why:** best match to "distinct vanishing point + set geometry". It suits the P2 salt-works constraint "keep vanishing-point placement and horizon height".
- **Risk:** real landmark and two small national flags (no text).

### C02b · S23 @ 28.54 s — giant redwoods, tiny soldiers
- Low-angle frontal, four massive trunks as verticals, a haze shaft upper-centre, a tiny group of figures at the bottom for scale; dark green-brown (luma 44, darkest). Very strong scale and atmosphere, but **the vanishing point is weak** (frontal, verticals only). No text. Best alternative if you want to avoid the landmark and flags.

### C02c · S03 @ 3.52 s — domed war-room
- Wide symmetrical hall, ribbed dome, rows of consoles converging, lit LED boards and screens; green-teal (saturation 77). Strong geometry.
- **Risk:** screens contain text, data and documents → text-leak hard-fail risk; many small figures.

## C03 — Prop / action

### C03a · S06 @ 7.44 s — flying-wing aircraft low over the sea (**recommended**)
- **Composition:** the dark wing silhouette spans the middle third horizontally above a flat grey sea, with ~40% empty sky above it as negative space. A dark cockpit or frame edge shows lower-right.
- **Lens:** telephoto compression (≈200 mm look) from an air-to-air position.
- **Lighting:** flat overcast with engine exhaust glow.
- **Palette/grade:** cold slate-teal and grey, the brightest candidate frame (luma 115, saturation 42).
- **Texture:** sea haze, heat shimmer.
- **Era:** 1940s "secret aircraft" myth.
- **Why:** the strongest single-object silhouette and scale contrast. It maps naturally to the P2 moth kite, which is also a winged silhouette.
- **Risk:** the aircraft type is historically associated with WWII Germany, but no insignia is visible.

### C03b · S48 @ 61.46 s — armoured men hauling at a sparking portal ring
- Centred ring of blue-white light, a spark shower, smoke, three armoured figures in action at its base, a cannon wheel at right; cool blue + orange sparks (luma 83). True action, but busier, with motion blur and multiple subjects. The ring is a source-specific motif.

### C03c · S11 @ 13.79 s — glowing ring above a crowd of spears
- Centred bright ring in a dark industrial hall, foreground silhouettes of pikes and helmets, hanging tyre-like coils; low-key (luma 62, high contrast). Strong silhouette, but low detail and a source-specific motif.

## Recommendation

**C01 = C01a (S30), C02 = C02a (S16), C03 = C03a (S06).** Each is the closest fit to its spec criterion and has no legible text or insignia (watermark aside). The three cover different focal lengths (portrait tele, normal perspective, extreme tele) and lighting keys (practical warm low-key, flat daylight, overcast high-key). That spread stresses the reverse Skills on different properties.

If you prefer no real landmark or flags in the set, swap C02 to C02b (S23), at the cost of a weaker vanishing point.
