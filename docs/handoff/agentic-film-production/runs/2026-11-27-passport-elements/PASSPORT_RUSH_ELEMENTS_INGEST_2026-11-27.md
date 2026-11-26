# Passport Rush — Elements CSV ingest (metadata only)

Inputs (owner browser export, private on box `/workspace/afp-private/passport_rush/`): `elements_all_20261127.csv` sha256 `9159d6c05f18a6369a0dcd05b82f0b7569b7996ea4d1a62b46cb075f19b89174` (17 rows); `elements_props_20261127.csv` sha256 `94a1f256f8abe8ee28902fc58a44c7248162f001779266956b4e5ff727f4aa85` (6 rows).
Tool: existing `studio/importer/full_project_importer.py`, new `ElementsCSVAdapter` (evidence class OWNER_EXPORT, `bytes_obtained=false`), plus the saved public publication HTML fixture. Tests: `studio/tests/test_full_project_importer.py` (17 pass).

Schema-level results (no names, descriptions or IDs in git; only SHA-256 of IDs/titles in the redacted JSON):
- 17 unique Elements; props file is a strict subset (6 of 17, all IDs in the all-file); de-duplicated, not double counted.
- By category: character 7, prop 6, environment 2, `auto:character` 2. One distinct author; 0 with a review status; created 2026-08-20 .. 2026-09-04.
- Coverage: `elements` **PARTIAL** (listing only; no element media, no placement mapping to the project); `project` OBTAINED; `assets` PARTIAL; `video` PARTIAL; `audio`, `rights` UNKNOWN; storyboard, previs, prompts, model_params, timeline, canvas BROWSER_REQUIRED. Import status **PARTIAL**; acceptance NOT_RUN.
- Provenance flag (for Neon): the Elements' author username differs from the publication author (`higgsfield.studio`) and all Elements predate the publication (2026-09-25). The CSVs show these are Elements named "Passport Rush …" in the exporting account's library; they are **not proven** to be the film's placed Elements. Treated as OWNER_EXPORT, never OFFICIAL.
- Descriptions contain non-English free text that may be non-public → full inventory stays private: `/workspace/afp-private/passport_rush/inventory/passport_rush_inventory_with_elements_20261127.private.json` (sha256 `e44306f959cc996a324c9cb6150645914d0e2c9af0f3c9ed00eeba98c4f41034`). Committed: `passport_rush_inventory_redacted_20261127.json`.
- Still browser-only / not downloaded (per "metadata only, no download"): element images, storyboard, previs, prompts, model parameters, timeline, canvas.
