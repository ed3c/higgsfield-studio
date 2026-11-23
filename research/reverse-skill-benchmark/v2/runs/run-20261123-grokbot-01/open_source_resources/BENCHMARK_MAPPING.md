# Open-source resources → Benchmark v2 / research mapping (2026-11-23 ~20:50 Asia/Taipei)

**Sources:** Neon's two Notion pages, read-only:
- Higgsfield 電影風格逆向 (100 entries)
- Higgsfield × 當代藝術 (100 entries)

**Data:** `open_source_resources_inventory.json`.

**Not changed:** the spec, the manifest, the locked P1 Skill set (`unimage`, `caph`, `niobium617`), and every result and score.

## Counts

| category | n | link status | benchmark role |
| --- | --- | --- | --- |
| Higgsfield official skills (film A) | 10 | 10 × 200 | Platform reference: prompt engineering, model catalog. Its MCP/CLI path is a paid surface → not used. |
| Higgsfield prompt suite (film B, OSideMedia, **archived**) | 15 | 15 × 200 | Forward prompting: Camera, Style, Motion method reference. |
| Director style modules (film C) | 20 | 20 × 200 | Comparative reference only. **No director attribution to @tupacabra.** |
| Cinematic reverse-engineering DNA (film D, WhQ-cc) | 18 | 18 × 200 | **DNA method:** Story, Character, Motion, Expression, Costume, Scene, Camera, Lighting, Color, Editing, Consistency, Reconstruction, Creative Distance. |
| Film production / prompt compilation (film E, 0xhughs) | 14 | 14 × 200 | Shot IR and prompt compilation; lighting/photorealism and lens references. |
| Cinematography / still-to-film (film F, AustinZ21) | 10 | 10 × 200 | Shot review, pitfalls, finishing grade. |
| Production engineering (film G, MRCalderon3D) | 13 | 13 × 200 | Reference bible, continuity, independent self-evaluation, provenance. |
| Agent skills: style reverse and art direction (art #1–20) | 20 | 20 × 200 | **Candidate reverse Skills** (#6–#10); art-direction and LOOK methods (#12–#16). #5 = caph (locked). #20 excluded (I2I). |
| Comfy Open-Source-Higgsfield projects (art #21–36) | 16 | 16 × 200 | Out of scope for the still benchmark; production-pipeline tooling (3D, video, audio). |
| Prompt libraries (art #37–40) | 4 | 4 × 200 | Vocabulary only. |
| Artist style cards (art #41–100) | 60 | No URL by design; **60/60 names found** in the index `data.js` | Art-domain reference cards; not used for @tupacabra. |

**Link totals:**
- 200 entries in all; 140 have a GitHub link. These are 139 unique URLs: film #1 and art #1 are the same file.
- The links span 42 repositories.
- **140/140 return HTTP 200. MISSING_SOURCE: 0.**
- The extra links also return 200: 7 repo roots, the Comfy event page and the Higgsfield winners page.

**Licence checks:**
- `LICENSE_UNVERIFIED`: A006, A015, A018, A019, A037, A039.
- Art #37's "CC BY 4.0" is **not** confirmed by the GitHub API (it reports NOASSERTION).

**14 award works:**
- All 14 creators are already in the registry.
- Only 5/14 works have an `artworks.jsonl` row. This is GAP-OSR-01.

## Additional Skills → P1-ext / P2-ext addendum (`P1_EXT_PROPOSAL.json`, **NOT_RUN**)
- **P1-ext core**, 3 × 3 × 2 = **18** renders. Same refs, same brief, same rubric, but a **separate ranking**; it cannot become P2 candidate B.
  - A007 `DaYePython/image-to-prompt-skill` (MIT)
  - A008 `MCamner/mq-image-analyze` reverse-prompt (MIT; may need a local model, so it must pass the G2 audit first)
  - A009 `fluentlc/shiny-skills` image-to-prompt (MIT; Prompt Case mode)
- **P2-ext (optional)**, 2 × 3 × 2 = **12** renders, using the approved P2 subjects:
  - A010 `extract-visual-style-2` (MIT)
  - A009 in Template mode
- **Conditional:** A006 `style-prompt-extractor`, +6 renders. The repo has no licence, so it needs owner approval.
- **Excluded:**
  - A020: image-to-image and a paid provider.
  - F046: video input. It is a method reference and is reserved for a future video-DNA phase.
  - A015: forward LOOK prompter.
  - A005: this is `caph`, which is already locked.

## Applies to @tupacabra (38 entries flagged in the inventory)
- **DNA extraction:** F046–F063.
  - Camera, Lighting, Color and Creative Distance are applied in `style_dna/TUPACABRA_STYLE_DNA_v1.1_NOTES.md`.
  - Motion, Editing and Story DNA on the 87 s trailer remain `NOT_RUN`. They are the natural next research step and need no generation.
- **Look and photorealism:** F068, F073–F075, F084, F086, F087, F090, F093, F098; also A014, A015 and F016/F018.
- **Candidate Skills:** A006–A010. These would run on the same @tupacabra refs.

The @tupacabra focus does **not** narrow the scope. The other 13 named obligations and the 79 historical creators keep their registry rows and `NOT_RUN` states.
