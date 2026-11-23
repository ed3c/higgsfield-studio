# Coverage gaps — batch-20261123-grokbot (Research Completeness track, G-R)

- **Gate G-R state:** `PARTIAL_RESEARCH_SCOPE`. Not `RESEARCH_COMPLETE`.
- **Separate from G-B:** this file does not decide, delay or advance the 30-image benchmark (see `research/reverse-skill-benchmark/v2/runs/run-20261123-grokbot-01/GATES.json`).
- **Built by:** `build_registry.py` (deterministic, read-only over `research/creators.json`, sha256 `fcfddb8a…9819`).

## What this batch actually did (SOURCE → IMPLEMENTED; nothing VERIFIED)

| Item | Status | Evidence |
| --- | --- | --- |
| Enumerate all 79 historical creator records | `IMPLEMENTED` — 79/79 rows, indexes 0–78, fields copied unmodified | `creators.jsonl` rows `HC79-000…078`; assertion in `build_registry.py` |
| Preserve 3 lower-confidence candidates | `IMPLEMENTED` (not counted in the 79) | rows `HCLOW-000…002` |
| Named obligations §1 (13 IDs) | 12 linked to historical rows; `CR-TUPACABRA` added as a new record | `named_obligations` field |
| Source list | 95 source rows (89 historical URLs de-duplicated + 6 @tupacabra / NUREMBERG URLs) | `sources.jsonl` |
| Artwork records | 9 named works only | `artworks.jsonl` |
| Re-verification of any historical claim | `NOT_RUN` | — |
| Creator Bible / Artwork Analysis / Visual Style Bible / Shot IR / Domain analysis | `NOT_RUN` | — |

## MISSING_SOURCE records

| ID | Missing source | Why it matters | What would close it |
| --- | --- | --- | --- |
| MS-001 | The **original ChatGPT conversation** that produced `CREATIVE_RESEARCH_SCOPE.md` / `DOT_HANDOFF.md` | Scope §0.4/§1: every resource supplied there is a coverage obligation. This executor has no access to it. **Not assumed obtained.** | Owner exports the conversation (or a list of its links/attachments) to private storage |
| MS-002 | **All attachments** in that conversation (stills, trailer clips, prompts, code, screenshots) | Same; count unknown | Owner provides files or a manifest with hashes |
| MS-003 | The user **Subscription screenshot** showing `Nov 20, 2026` | Billing evidence (private), not a creative reference. Not in repo by design; not held by this executor | Keep private; PR #5 later observed the live table (Starts Nov 20 / Expires Nov 27) |
| MS-004 | **C01/C02/C03 reference stills** (URL, frame/timestamp, crop, SHA-256, rights scope) | Blocks G0 and every P0 prompt → blocks all 30 renders | Owner picks 3 stills and sets `analysis_rights` + `third_party_upload_allowed` (YES/NO) |
| MS-005 | NUREMBERG trailer **media** (X video `2121357879341166683`) | Located via secondary sources, **not opened, not downloaded, not inspected**; tool attribution (Venice AI) and metrics are `UNVERIFIED_CLAIM` | Authorized viewing/capture; record capture method + hash privately |
| MS-006 | **Other public @tupacabra works** | Scope asks for "other publicly accessible works"; X timeline not enumerated | Authorized X read of the profile timeline |
| MS-007 | Ownership of YouTube `Xeto4CMwvzA` ("NUREMBERG 1561 - Official Trailer") | Possible earlier clip; channel ↔ @tupacabra link unverified | Open channel page, match handle |
| MS-008 | P2 **original replacement subjects** frozen before P1 | Spec §5 P2; manifest `style_transfer_new_subject` all `null` | Owner approves or edits the proposal in `runs/run-20261123-grokbot-01/p2_subjects_PROPOSED.json` |
| MS-009 | ScrapeCreators data (`visual_candidates.json`, outlier ranks, comments) | Optional; API key absent → `NOT_RUN` | Only if owner provides key; not required if MS-004 closes |
| MS-010 | Media/links behind `profiles_raw.json` socials (Instagram/TikTok/YouTube) | Historical method note: not all were HTTP-opened | Per-creator authorized fetch |
| MS-011 | JOEY TinyURL skill pack | Study queue: no repo, "save before use"; not archived | Archive privately with hash |
| MS-012 | Official case-study media for Authors First / One of One / Boxel | Only link-level evidence in historical rows | Fetch pages, record capture timestamps |

## Other coverage gaps (non-source)

| ID | Gap | State |
| --- | --- | --- |
| G-07 | `CR-ROCOCO` and `CR-PURGA` share one historical record (index 0). Scope requires distinct records for studio vs. account vs. award role | `NEEDS_VERIFICATION`; historical row left untouched |
| G-08 | Artwork extraction from the free-text `notable` field of all 79 records | `NOT_RUN` (only 9 named works extracted) |
| G-09 | Domain-manager outputs (Narrative, Art Direction, Character/World, Cinematography, Prompt Compiler, Video/Audio, Generation Ops, Evals, Knowledge, Distribution) | All `NOT_RUN` for this batch; contracts unchanged in scope §4 |
| G-10 | Cross-domain coverage counts: historical tags film 68, ads 24, art 21, scifi 13, mv 12, shorts 11, fashion 8, tech 6, literature 2, sports 1 (from `research/README.md`) — literature and tech are thin | Scope must not shrink; flagged for future batches, no creators invented |
| G-11 | User-supplied references from **Grok Bot conversations** (personal footage, J4 project files, a TV-news screenshot, a film-character still) | Exist only in private storage; contain identifiable/third-party media → **not committed**, not analyzed under this scope; should be registered privately by opaque ID |
