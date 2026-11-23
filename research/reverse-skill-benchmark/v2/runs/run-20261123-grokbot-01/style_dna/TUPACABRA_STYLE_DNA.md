# TUPACABRA style DNA: subject-agnostic look spec (v1, 2026-11-23 ~20:15 Asia/Taipei)

**Phase `STYLE_DNA_EXTRACTION`.** This phase is separate from the reverse-Skill benchmark score. It changes no P1 or P1b result, score or gate.

**Goal (Neon t33u):** 「逆向到提示詞生成圖片風格可以自由發揮為止，只學習風格不寫死對象」. Learn the style only; never hard-code the subject.

**Evidence:**
- The 3 locked refs: C01_S30, C02_S16, C03_S06.
- `research/live/creator-intelligence/2026-11-23-tupacabra/NUREMBERG_TRAILER_ANALYSIS.md`: 55 shots.
- New: look metrics over all 55 shot-midpoint frames (`trailer_55_look_stats.json`). These are 4K frames with the bottom 8% cropped to remove the watermark band; the S42 title card is excluded.
- The P1 and P1b look-gap metrics in `../p1b_style_fix/`.

**Labels used below:**
- `MEASURED`: computed from pixels.
- `INFERRED`: visual reading by this executor.
- `LESSON`: learned from the P1 and P1b failures.

**Method alignment:** Neon's Notion page *Higgsfield 電影風格逆向* (read-only). It defines DNA axes (Story / Camera / Light / Color / Motion / Editing). It keeps the Style Prompt and the Shot Prompt separate, each with its own acceptance. It sets 6 metrics. This spec covers the **Camera, Light and Color DNA of stills**. Story, Motion, Editing and Sound DNA are listed at the end as `NOT_RUN` or partial.

## 0. Numbers (MEASURED, same pipeline as `check_style_v1.py`)

| metric | C01 | C02 | C03 | 54 trailer shots, p10 / p25 / **p50** / p75 / p90 |
| --- | --- | --- | --- | --- |
| mean luma | 74.0 | 69.5 | 114.6 | 46 / 55 / **74** / 102 / 121 |
| black point p1 | 10 | 17 | 1 | 4 / 7 / **10.5** / 20 / 26 |
| highlight p99 | 187 | 195 | 192 | 174 / 189 / **224** / 248 / 250 |
| saturation (HSV S) | 56.5 | 58.3 | 42.7 | 44 / 51 / **57** / 74 / 97 |
| Lab a\* | +0.7 | −2.2 | −4.9 | −5.2 / −4.3 / **−2.4** / −1.3 / +0.7 |
| Lab b\* | +2.4 | +1.3 | −1.1 | −4.4 / −2.7 / **−0.7** / +1.6 / +4.2 |
| centre sharpness (Laplacian var) | 18 | 113 | 50 | 18 / 34 / **95** / 157 / 383 |

For comparison, the failed rounds:
- **P1:** p99 139–228, luma 47–128, sharpness 64–776.
- **P1b:** p99 147–172 (compressed), sharpness 23–107.

## 1. Capture medium and film emulation
- **Medium.** The images read as frames from a 24 fps live-action prestige feature on a large-format digital cinema camera. They are **clean**: grain is very fine and close to digital noise, not heavy 35 mm grain. The residual-noise proxy of the refs is 0.5–1.0, below every P1 output.
  - **LESSON:** the words "film grain" made GPT Image add synthetic stipple. Ask for "very fine sensor noise" instead.
- **Softness.** Frames have the slight softness of moving pictures: optical, not sharpened.
  - MEASURED: centre sharpness of the refs is 18–113 and the trailer median is 95.
  - The P1 CG look was 311–576. P1b overshot to 23–107, which is acceptable, but must not be pushed softer.

## 2. Lens and depth of field (INFERRED, plus LESSON)
- Portraits and objects use a long-lens look (≈85–135 mm) with shallow depth of field. Background people dissolve into unrecognisable shapes, and practical lights become large bokeh orbs.
- Wide establishing shots use a 24–35 mm look. Distance still softens through haze and defocus; there is **never deep focus to the horizon**.
- **One focus plane.** C02 has a sharp near object and a defocused city (MEASURED edge/centre ratio 0.07). P1b softened the whole frame evenly (0.41).
  - **LESSON:** the style block must demand a declared `FOCUS PLANE` from the shot prompt. Generic "shallow depth of field" wording does not create differential focus.
- Out-of-focus foreground occluders at the frame edge are common: dirty glass, cockpit frames, shoulders.

## 3. Exposure anchors and contrast curve (MEASURED)
- **Highlights reach near white.**
  - Refs: p99 187–195. Trailer median 224, upper quartile 248, so practicals and skies often clip softly.
  - **LESSON (P1b):** "muted / no HDR / roll-off" wording pulled p99 down to about 162 and made the images read darker. The style block must say *bright highlights near pure white, soft roll-off* and *do not dim the highlights*.
- **True blacks.**
  - Refs: p1 1–17. Trailer median 10.5.
  - **LESSON:** C03 P1 said "lifted blacks" and landed at p1 21; P1b reached 11. The block demands true black in the deepest shadows and occluders.
- **Mean key is low to mid.** Trailer IQR 55–102, median 74. Portraits are lit as **high-key faces in a dark surround**: C01 has the face and the white fabric as the brightest areas.
- **Curve.** A gentle S-curve with full range (from about 0–10 up to about 190–250) and rich lower mids. It is *not* a flat log look, and *not* a crushed music-video look.

## 4. Palette and saturation (MEASURED, plus INFERRED)
- **Base.** Cool slate-teal in shadows and ambient light: trailer a\* median −2.4 and b\* −0.7. Warm accents appear only where a warm source motivates them (candle, fire, tungsten, sparks); this is where the trailer's b\* p90 of +4.2 comes from.
- **Saturation** is moderate and natural: refs 43–58, trailer median 57. It is **not desaturated**.
  - **LESSON (P1b C01):** asking for "muted / desaturated" overshot to 40 and the skin lost its pink flush.
- **Skin** keeps a living pink-red flush, with redness around the nose and eyes.

## 5. Halation, grain and texture (INFERRED)
- Soft halation and bloom on practicals and on specular or white highlights. It is subtle, not a glow filter.
- Very fine noise. Organic, uneven surface texture.
- Skin has natural redness and visible pores at normal distance. It is **not** stippled freckle fields and **not** airbrushed.
- Fabrics, metal and stone look worn.

## 6. Lighting philosophy (INFERRED)
- Light is motivated by sources in the scene: one dominant soft key with deep natural falloff, and uneven, imperfect fill.
- Atmospheric haze where light travels through air (interiors with smoke and dust, exteriors with mist).
- Weather and time of day belong to the **shot**. The style does not force overcast; it only forbids the postcard golden-hour glow unless the shot requests it.

## 7. Production design (INFERRED, era-agnostic)
- The trailer spans the 16th century through to the present day (see the trailer analysis). What is constant is not the era but **physically built, worn, lived-in sets, costumes and props**, plus plausible engineering for invented objects.
- The era is a shot-prompt variable and must never be fixed by the style.

## 8. Framing tendencies (INFERRED from 55 shots)
- Portraits sit off-centre on a third with soft background faces.
- Strict central symmetry is reserved for monumental spectacle.
- Wide shots show strong scale contrast: tiny figures against giant objects.
- Through-glass and occluded foregrounds are common.

## 9. What the style is NOT
- Not illustration, painting, concept art, a game-engine render or 3D CG.
- Not an HDR look, a clarity or micro-contrast boost, oversharpening, or crisp detail from edge to edge (the P1 tell).
- Not waxy, plastic or airbrushed skin, and not uniform stippled freckles.
- Not glossy CG metal with perfect reflections.
- Not a golden-hour postcard, and not sculpted hero clouds by default.
- Not a desaturated, washed or monochrome grade (the P1b C01 overshoot).
- Not compressed grey highlights (the P1b tell), and not lifted grey blacks (the P1 C03 tell).
- Not heavy vintage film grain, light leaks or scratches.
- Not tied to any subject: no ruffs, obelisks, flying wings, WWII-coded uniforms, portals, flags, the TUPACABRA watermark or any text.

## 10. DNA axes not covered by this still-image spec
| axis | status |
| --- | --- |
| Story / Narrative DNA | partial: era collage and scale contrast noted in the trailer analysis; no shot-level narrative extraction |
| Motion DNA | `NOT_RUN` |
| Editing DNA | partial: cut statistics only (55 shots, median 1.0 s) |
| Sound DNA | `NOT_RUN`: the "Boots" march-cadence claim remains `UNVERIFIED_CLAIM` |
| Temporal Consistency metric | `NOT_RUN`: stills only |

## Artifacts
- `STYLE_PROMPT_v1.txt`: slot template plus style block.
- `style_block_v1.txt`: the block alone, exact bytes.
- `style_targets_v1.json`: metric targets.
- `check_style_v1.py`: the metric gate.
- `trailer_55_look_stats.json`: trailer look metrics.
- `validation_v1/`: `ACCEPTANCE.md`, `style_v1_jobs.json`, `prompts/`, `controls_shot_only/`, `metric_gate_calibration.json`.
- Paste copies of the prompts: `/workspace/hs-bench-jobs/style_v1_prompts/`.
- **Status: DRAFT, NOT GENERATED.**
