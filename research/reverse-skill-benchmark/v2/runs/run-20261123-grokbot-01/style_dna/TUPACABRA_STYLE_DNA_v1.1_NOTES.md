# TUPACABRA style DNA — v1.1 notes (append-only; v1 untouched) — 2026-11-23 ~20:55 Asia/Taipei

Phase `STYLE_DNA_EXTRACTION`. These notes strengthen `TUPACABRA_STYLE_DNA.md` (v1) using the open-source **method references** from Neon's two Notion pages, as instructed in t35u.

**Citation format:** `[OSR-id repo@sha:path]`. Each cited file was fetched at that sha on 2026-11-23 and read; the inventory is in `../open_source_resources/`.

**Evidence labels:**
- `MEASURED`: computed from our pixels.
- `METHOD`: what the cited resource prescribes.
- `APPLIED`: how this changes our spec.

Citing a resource supports *the method*, not the factual claim about @tupacabra. Every @tupacabra fact still rests on the refs, the trailer frames or the metrics.

## N1. DNA axes and output contract
- **METHOD.** The source is decomposed into Story, Character, Motion, Expression, Costume, Scene, Camera, Lighting, Color and Editing DNA, then run through consistency, director intent, reconstruction and creative distance. Evidence, inference and recommendation are kept separate. [OSR-F046 WhQ-cc/Cinematic-Video-Reverse-Engineering-Skill@eeb5f75:SKILL.md]
- **APPLIED.** v1 already covers Camera, Lighting and Color for stills. Story, Motion and Editing DNA of the trailer are still `NOT_RUN` (v1 §10). Expression and Costume DNA are deliberately **excluded from the style core**, because they are content and must be rebuilt per shot. See N6.

## N2. Camera DNA → shot locks
- **METHOD.** Report the lens profile, framing logic, movement grammar and camera intention, plus **shot locks** (the rules that must survive). Its listed failure mode is "naming shot types without intent". [OSR-F053 …@eeb5f75:references/07-camera-dna.md]
- **METHOD.** Lens semantics:
  - 28–35 mm = naturalistic documentary presence;
  - 75–100 mm = portrait compression, isolation, emotional scrutiny;
  - macro = tactile evidence.

  [OSR-F075 0xhughs/director-skills@35ca0a2:…/camera_lens_movement.md]
- **APPLIED (shot locks for the style core).**
  1. One declared focus plane, with everything else optically defocused.
  2. A long lens for people and objects; 24–35 mm only for establishing views.
  3. Off-centre subjects, with symmetry reserved for spectacle.
  4. Soft foreground occluders at the frame edge.
- **Evidence:** the 3 refs, trailer analysis items 5–6, and A3 of style_v1 (5/6 pass). The 04 failure shows wide shots still need a focus target in the **shot** prompt. This is a shot-side lock, not a style one.

## N3. Lighting DNA: describe source behaviour, not warm or cool
- **METHOD.** Map the key, fill, rim and ambient light, plus colour temperature, shadow direction and highlight placement. Its listed failure mode is "saying warm or cool without describing source behavior". [OSR-F054 …@eeb5f75:references/08-lighting-dna.md]
- **MEASURED (style_v1).** In the two scenes with a warm practical light (01 bulb, 03 kiln), the warmth leaked into the whole frame: b\* 7.9 and 6.9, saturation 88 and 86.
- **APPLIED.** v2's `Colour:` line already confines warm light to "the surfaces it touches". The v1.1 recommendation for later rounds, one variable at a time, is to state source behaviour **inside the shot prompt's `Light sources in scene` slot**: direction, size, falloff, and what it does *not* reach.

## N4. Color DNA: black point, white point, skin, digital vs filmic
- **METHOD.** Colour DNA must state the exposure bias, black point, white point, skin-tone handling, contrast feel, saturation behaviour and "filmic vs digital cleanliness". Its listed failure mode is "treating color as style keywords only". [OSR-F055 …@eeb5f75:references/09-color-dna.md]
- **APPLIED.** This confirms that v1's numeric anchors are the right representation.
  - Values: p1, p99, luma, saturation and Lab are in `style_targets_v1.json`, enforced by `check_style_v1.py`.
  - Medium impression, an inference from the refs' residual noise of 0.5–1.0 and from the trailer: **clean digital capture with a filmic grade**, not film emulation.
- **METHOD.** In practice, generated shots run "warm, oversaturated next to the originals". The fix is lower saturation and a red-down/blue-up balance. The film-wide look is "cool shadows, warm highlights". [OSR-F087 AustinZ21/cinematic-skills@0e5b3fe:…/still-to-film/references/finishing.md]
- **APPLIED.** This independently matches our style_v1 A1 failure: b\* median 5.71. It supports v2's single-variable colour fix. The split tone "cool shadows / warm highlights" is recorded as a **candidate v3 variable**. It is not added now, to keep one variable per round.

## N5. Photorealism and anti-CG anchors
- **METHOD.** Describe physical light and material response instead of quality words. Realism anchors include skin pores and asymmetry, fabric weave and wear, environmental dust and scratches, and the optics of shallow DOF and halation. There is an "anti-plastic" guardrail. [OSR-F074 0xhughs/director-skills@35ca0a2:…/lighting_and_photorealism.md]
- **METHOD.** The Cinematic Prompt Engine says:
  - A **softening budget**: at most two full-strength softening signals among grain, halation, fog, diffusion and bloom.
  - For GPT Image, *"mentioning grain or halation can trigger visible noise"*, so fine grain is omitted or described as barely visible.
  - A **clarity anchor**: "optical sharpness, not digital sharpening".
  - A **tonal-density anchor**: full tonal range, filmic highlight shoulder, dense midtones, deep blacks that are not grey.

  [OSR-A015 Leo414x/AI_Cinematic_Prompt@44fb292:SKILL.md; licence NOASSERTION, cited only as a method reference]
- **MEASURED.** This explains two of our observations:
  - P1 "film grain" produced stipple. v1 already moved to "very fine sensor noise".
  - The 06 macro came out CG-crisp (sharp_c 349). That needs a *clarity-vs-sharpening* distinction, not more softening.
- **APPLIED.** Two later candidate variables, one per round:
  - (a) Replace "very fine sensor noise" with an optical clarity anchor.
  - (b) Audit the v1 block against the softening budget. It currently stacks halation, haze, moving-picture softness and defocus.

## N6. Reconstruction and Creative Distance = Neon's "learn style, not subject"
- **METHOD.** "Preserve cinematic law. Rebuild concrete expression."
  - **Preserve:** lens language, movement logic, light relationships, colour hierarchy, edit pacing.
  - **Rebuild:** identity, setting, costume, props, plot, cultural markers, text.
  - **Failure modes:** keeping specific content, or over-abstracting until the method is lost.

  [OSR-F059 …@eeb5f75:references/13-reconstruction-engine.md; OSR-F060 …@eeb5f75:references/14-creative-distance.md]
- **METHOD.** Keep scene locks out of the global style core. A content-free prompt starts with a subject slot. Six or more varied samples are needed for series-level evidence. [OSR-A010 ajinnaaa/extract-visual-style-2@7b7d2c2:extract-visual-style-2/SKILL.md]
- **APPLIED.**
  - The v1 slot template, the subject-free block (checked by word-boundary scan) and the B2 leak gate implement this.
  - Six varied validation shots meet the "≥ 6 varied samples" bar for the *validation* set.
  - The *source* evidence is the 3 refs plus 55 trailer frames, measured. Only 3 frames were read closely, so the textural claims stay `INFERRED`.

## N7. Editing DNA (preparation only; NOT_RUN)
- **METHOD.** Record shot-duration clusters, pause placement, the build-and-release pattern, and whether cuts follow emotion, action or information. [OSR-F056 …@eeb5f75:references/10-editing-dna.md]
- **Have:** cut statistics only, 55 shots with a median of 1.0 s, slowing in the final third (trailer analysis).
- **Next:** classify the 55 cuts against this checklist. This needs no generation and no credits.

## N8. Process lessons adopted
- **METHOD.**
  - "Notes work when they're physical and timed; adjectives ('more cinematic') don't."
  - "An agent can't watch in real time or hear… a human must watch the final."

  [OSR-F086 AustinZ21/cinematic-skills@0e5b3fe:…/still-to-film/references/pitfalls.md]
- **APPLIED.** This supports keeping metric gates (A1, A3) **plus** the human or model oracle (A2, Neon). An agent's self-assessment is never the final style verdict.

## Changes to deliverables
- **None in place.** v1 files, `STYLE_PROMPT_v2.txt` and the targets are unchanged.
- **Candidate variables queued for later single-variable rounds**, in priority order:
  1. Split tone (N4).
  2. Clarity anchor replacing the noise wording (N5a).
  3. Softening-budget audit (N5b).
  4. A light-behaviour slot in the shot template (N3).
