# P1 look-gap analysis: locked references vs P1 outputs (2026-11-23 ~19:35 Asia/Taipei)

**Human oracle (Neon, t31u, 19:20):** 「圖片的電影風格具有攝影寫實的感覺，這批圖片風格只有構圖類似，需要修正」. In English: the references have a photographic-realist cinematic look; the P1 batch matches only the composition.
→ Recorded verdict: **style fidelity FAIL, composition PASS-ish**, for all 17 P1 outputs.

- **Method.** The executor examined each locked masked reference against the outputs of its own case only, through the anonymised blind packet. Skill identity was not looked up and the key stays sealed. This is a diagnosis by the prompt author, **not a blind score**, and it does not replace the R1/R2 review.
- **Global look.** Taken from `research/live/creator-intelligence/2026-11-23-tupacabra/NUREMBERG_TRAILER_ANALYSIS.md`: period-cinema realism rather than AI gloss, soft halation, a desaturated teal-slate base with warm practicals, long-lens shallow DOF on portraits, and dirty through-glass foreground occlusion.
- **Measurements.** All images were resized to 1344×752 with OpenCV:
  - luma: mean, p1 and p99 (0–255)
  - mean HSV saturation
  - Lab a/b means
  - Laplacian variance in the central area vs the top and bottom sixth, as a sharpness and depth-of-field proxy
  - high-pass residual std in flat regions, as a texture/noise proxy

  Values are given per case as the reference vs the range across that case's outputs. Per-image values are kept private in `/workspace/hs-bench-review/lookgap/`, so reviewers cannot be anchored by them.
- **Measurement caveat.** The references are downscaled about 2.9× from 3840 px, while the outputs are nearly native. Downscaling suppresses noise and *raises* per-pixel sharpness, so the reference is softer than the outputs **in spite of** this bias. The noise proxy cannot tell real grain from synthetic texture, so it is used only as a supporting signal.

## Cross-case diagnosis (applies to all 17)

1. **Deep-focus, edge-to-edge crispness is the main CG tell.**
   - Central Laplacian variance, reference vs outputs:

     | case | reference | outputs |
     | --- | --- | --- |
     | C01 | 18 | 109–554 |
     | C02 | 114 | 385–776 |
     | C03 | 50 | 64–170 |

   - The top and bottom bands, which are out of focus in the references, are 5–50× sharper in the outputs.
   - The references look like soft 24 fps motion-picture frames with real optical falloff. The outputs look like stills with uniform micro-contrast.
2. **Synthetic micro-texture instead of photographic texture.** The outputs carry stippled, uniformly distributed detail: freckle "dot fields", every lace thread resolved, cloud sculpting. The references are smooth and slightly diffused, with uneven organic texture.
3. **Generic "cinematic" exposure instead of the shot's actual exposure.** Each case was mis-exposed in a different direction (see below). The prompts gave relative cues ("low contrast", "deep shadows", "late-afternoon light", "lifted blacks"). The model resolved these into its default glossy grade rather than the reference's key.
4. **Film emulation cues were ignored.** Every P1 prompt already asked for film grain, halation and shallow DOF, yet the outputs show none of them convincingly. These words alone are too weak for GPT Image 2.6. The fix needs (a) an explicit statement of the medium (a live-action frame grab, not illustration or render), (b) explicit negatives for the CG tells, and (c) per-case absolute exposure statements.
5. **Composition.** This roughly matches, as Neon says. The one minor note is C01: the reference subject sits left of centre with a tighter top crop. All three Skills said "centered", and the outputs are centred and symmetrical. Not changed in P1b, to keep the intervention style-only.

## C01 — portrait (S30)

| property | reference | P1 outputs (6) | gap |
| --- | --- | --- | --- |
| exposure / lighting ratio | high-key face; skin and ruff are the brightest areas, near clipping (luma mean 74, p99 188) | dark, evenly lit faces (mean 47–64, p99 139–156) with no bright key | **large**: faces are 1–1.5 stops under, with no highlight roll-off |
| lens / DOF | about 85 mm at f/1.4 look; background figure is an unrecognisable blur; candle is a big bokeh orb | background man is readable, nearly in focus; candle is small and sharp | **large** |
| halation / bloom | soft bloom on candle and lace highlights | small sharp flames, no bloom on lace | medium |
| skin texture | smooth, gauzy; uneven pink flush, moist red eyes; few freckles | uniform stippled freckle fields, crisp pores, dry "doll" eyes | **large**: CG tell |
| colour / palette | pale pink flesh, cool neutral surround (b\* +2.4) | warmer, more yellow-gold (b\* +5…+7), some more saturated | medium |
| contrast / blacks | p1 10, soft mids | p1 7–19; lower overall contrast because highlights are missing | medium |
| material | lace bloom-softened; brocade reads in shadow | every lace thread resolved; jewels glossy-CG | medium |
| CG / illustration tells | — | symmetrical "portrait painting" pose, posed gaze, over-ornamented headdress | **large** |

## C02 — car-hood POV down the avenue (S16)

| property | reference | P1 outputs (6) | gap |
| --- | --- | --- | --- |
| exposure / lighting | dim, low-key, overcast, no visible sun (luma 70) | bright sunny golden-hour postcard, visible sun disc in some, sculpted clouds (luma 117–128) | **largest gap in the run**: about +1.5 stops; time of day and weather are wrong |
| lens / DOF | camera very close to the hood; hood and pods loom large and are sharp; city soft and hazy | wide deep focus; every spire and window crisp to infinity | **large** |
| colour / palette | teal-grey, cool (a\* −2.2, b\* +1.3), sat 58 | warm cream-gold (b\* +5…+7.5), lower saturation but warm cast | large |
| contrast / blacks | bottom third is deep shadow (dashboard and hood underside) | thin dark band only; bright hood | large |
| atmosphere | thick haze, slight motion blur, through-glass feel | clear air, static | large |
| material | imperfect real reflections on the hood | mirror-perfect chrome, clean CG reflections | medium |
| CG / illustration tells | — | symmetrical architectural concept-art render | **large** |

## C03 — flying wing over the sea (S06), the closest case

| property | reference | P1 outputs (5; job 15 refused) | gap |
| --- | --- | --- | --- |
| contrast / blacks | **crushed true black** in the cockpit occluder (p1 = 1) | lifted (p1 18–24); caph's prompt explicitly asked for "lifted blacks" | **large** |
| colour / palette | dark teal-green sea, sat 43 | grey, washed (sat 19–39) | medium |
| atmosphere / horizon | haze swallows the horizon; coastline barely visible | prominent white chalk cliffs (unimage and niobium617 named "pale cliffs") | medium |
| lens / motion | long lens; aircraft slightly soft, motion-softened | aircraft crisp | medium |
| material | matte, weathered | clean matte CG | small–medium |
| lighting | flat overcast | flat overcast ✓ | small |
| halation | soft glow on engines | glow present ✓ | small |

## Fix design → `LOOK_LOCK_SPEC.json`

- **Structure.** The P1b prompt is the locked P1 Skill prompt, unchanged, plus a shared GLOBAL look lock and a per-case look lock. The look lock is identical for all three Skills in a case and declares precedence over any conflicting style, light, colour or lens wording.
- **What it changes.** It states:
  - the medium: an unretouched frame grab from a live-action film shot on a digital cinema camera with vintage primes, not illustration, painting, concept art or render
  - optical behaviour: real shallow DOF, 24 fps softness, highlight roll-off and halation
  - CG-tell negatives: no HDR, no clarity, no oversharpening, no waxy surfaces, no edge-to-edge crispness
  - the absolute exposure of each case: C01 high-key face; C02 dim and overcast with no sun; C03 crushed blacks and haze-swallowed horizon
- **What it does not change.** Composition.
