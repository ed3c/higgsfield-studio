# J4 byte-exact text/code originals (added 2026-11-23, HOF-07)

Append-only. Nothing in `archive/v2_6` … `archive/v4_0` was changed.

- `files/` holds 77 files copied byte-for-byte from the private archive
  `j4_all_available_resources_lossless_2026-11-22.zip` (SHA-256 `4efe79aa…0ca3011e`):
  - 32 original CSVs whose Git slots hold a tool-parsed rendering
    (`<PARSED TEXT FOR SHEET…>` + pandas index column). The parsed slots stay as historical
    records; `git_slot` in the manifest points at each one.
  - 42 `.py` + 3 `.js` build/validation helpers that existed only in the private ZIP.
- `ORIGINALS_MANIFEST.json` lists source path, SHA-256 and bytes; `studio_factory/tests/test_j4_originals.py`
  fails CI on any drift.
- Scripts hard-code the original sandbox paths (`/mnt/data/...`). They are preserved as historical
  sources, not maintained tools; do not run them against private media.
- Not included (stay private, `BLOCKED_PUBLIC_REPO_MEDIA_POLICY`): videos, photos, screenshots, ZIPs.
  JSON/MD/HTML/TXT/SRT originals remain represented by the versioned JSON archives.
- Licence note: `SOURCE_REGISTER_v3_3.csv` and `ART_METHOD_SOURCES_v4_0.csv` are citation lists of
  third-party artworks (method references, rights unreviewed). Citing ≠ permission to copy; the same
  rows were already public in parsed form.
