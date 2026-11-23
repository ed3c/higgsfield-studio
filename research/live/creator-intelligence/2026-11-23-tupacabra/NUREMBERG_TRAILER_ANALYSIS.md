# NUREMBERG 1561 — Official Trailer: style analysis (research only)

- **Work:** AW-NUREMBERG-TRAILER, creator CR-TUPACABRA. Sources SRC-T001 (X, 720p) and SRC-T002 (YouTube 4K). Private copies only.
- **Analyst:** Grok Bot, 2026-11-23 Asia/Taipei. Labels: `MEASURED` = computed from the file; `INFERRED` = visual reading of sampled frames; `UNVERIFIED_CLAIM` = third-party statement.
- **Not done:** no frame-by-frame viewing of the full motion, no audio listening/transcription by this analyst. Analysis of motion, sound and performance stays `NOT_RUN`.

## MEASURED

| Metric | Value |
| --- | --- |
| Duration | 86.72 s (X) / 87 s (YouTube) |
| Frame | 24 fps; X 1280×720; YouTube 3840×2150 (≈1.786:1, slightly wider than 16:9) |
| Cuts (ffmpeg `scene>0.3` on X file) | 55 shots → mean 1.58 s, median 1.00 s, min 0.38 s, max 6.57 s |
| Cut density | 0–30 s: 24 cuts · 30–60 s: 22 · 60–87 s: 9 (final third holds longer shots incl. title card) |
| Audio | AAC track present; silence only from 85.64 s to end (−40 dB) |
| Watermark | small "TUPACABRA" text bottom-centre on sampled frames |

Shot list with timecodes: `nuremberg_trailer_shotlist_scenedetect.tsv`. Candidate-frame pixel stats: `c_candidates_measured.json`.

## INFERRED — signature visual grammar

1. **Period-cinema realism, not "AI gloss":** soft halation on practicals, lifted blacks, fine grain, slightly crushed teal-grey midtones; feels like a 35 mm prestige-war/historical film grade.
2. **Desaturated teal / slate base with warm practical accents** (candles, fire, sodium sparks); mean saturation of the candidate frames 42–92/255.
3. **Era collage as structure:** 16th-century court and armour → early-20th-century inventor → WWII-era uniforms, flying wings, Antarctic fleets → Cold-War Washington → a modern data war-room. Recurring motif: a **glowing ring / portal** and sky objects, tying every era together.
4. **Scale contrast:** tiny figures against giant objects (redwoods, portals, aircraft, ice fleets); frequent wide establishing frames cut against tight portraits.
5. **Composition:** strong central symmetry for spectacle (portal rings, domed hall, star floor), off-centre rule-of-thirds for portraits with soft background faces.
6. **Lens language (INFERRED):** long-lens shallow-DOF portraits (≈85–135 mm look), wide 24–35 mm look for halls and landscapes, through-glass/cockpit framing with dirty foreground occlusion.
7. **Edit rhythm:** ~1 s median shots in the first two thirds (montage), slowing for the reveal and title. Silence only at the tail.
8. **Sound (UNVERIFIED_CLAIM, secondary sources):** march-cadence reading of Kipling's "Boots", no dialogue. Not verified by listening.
9. **Tooling (creator's own claim, SRC-T003):** "Videos generated with @VeniceAI"; underlying model(s) unknown.

## Content cautions for reuse (not for analysis)

Contains WWII-era German-coded uniforms and occult/esoteric imagery, a crucifixion silhouette, real historical persons as lookalikes (an R. E. BYRD name patch; a Tesla-like inventor), real landmarks and national flags. Research analysis is authorized; **P2 outputs must not reproduce any of these** (see `p2_subjects_APPROVED.json` banned motifs).
