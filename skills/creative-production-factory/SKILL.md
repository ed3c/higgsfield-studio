---
name: creative-production-factory
description: "Coordinate reproducible multi-project Higgsfield Studio productions using owner-isolated Domain Managers, immutable artifacts, evidence handoffs, reusable references and paid-generation gates."
---

# Creative Production Factory

Read \`studio_factory/README.md\` and \`projects/<slug>/PROJECT.json\` first. This skill coordinates the factory; it does not replace domain ownership or invoke paid generation.

1. Open project and the exact source revision. Resolve \`asset_id@revision\` and provenance before drafting any prompt.
2. Ask the producing Manager for a versioned artifact with source, license, SHA-256 and acceptance evidence. The consumer must ACK an exact version.
3. Keep **shared** art methods, physical phenomena, reference citations, optical theory and generic prompt templates in reusable global records. Store cast, story, locations, shot IR, sound IR, budget, human approval, provider take and delivery per production.
4. Maintain the producer → consumer → oracle → source chain; never conflate \`NOT_RUN\` with \`PASS\`.
5. Do not copy original contemporary artworks, protected character likenesses, real news compositions or copyrighted soundtrack phrases. Images used as reference remain in restricted media unless publicly cleared.
6. Never click a model's generate button or call a provider API from this skill. First check source/rights, explicitly named owner approval, Director's estimate posted to the appropriate service chat, current provider balance and the existing \`budget/track.py\` guard.
7. On completion, promote reusable learnings from reviewed results to \`shared\` as a new immutable revision. Never silently mutate already published shared sources or another film's accepted decisions.

Useful commands:

\`\`\`bash
python -m studio_factory.cli --help
python -m studio_factory.archive projects/j4-async-succession/archive/v4_0/conversation_text_archive.json /tmp/j4-v4_0
python -m unittest discover -s studio_factory/tests -v
\`\`\`

If original files or permissions are absent, record \`BLOCKED / NOT_AVAILABLE\` in the provenance manifest instead of manufacturing content or pretending an upload succeeded.
