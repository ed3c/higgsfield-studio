# Higgsfield Studio — Local Review & Playback

**Source methodology:** [`ed3c/medium-compiler` / `.agents/skills/build-review-interface/SKILL.md`](https://github.com/ed3c/medium-compiler/blob/6235a905bb552ce82ff7f239327c5f271c7dc446/.agents/skills/build-review-interface/SKILL.md), pinned at `6235a905bb552ce82ff7f239327c5f271c7dc446`. The review-interface Skill, not the Medium article-writing compiler, is the reusable component. The interface is independently implemented in `studio_factory/review_web.py` and `studio_factory/review_site/`.

## One Mac — local/private setup

You need Python 3.10+, your local checkout of `ed3c/higgsfield-studio`, and authorized access to the private Google Drive asset vault. No frontend package installation or remote web host is required.

1. Clone/checkout the Draft PR branch and obtain the **private** `j4_all_available_resources_lossless_2026-11-22.zip` from the Google Drive folder `Higgsfield-Studio-Private-Assets/J4-ASYNC-SUCCESSION`. Do not publish this archive or its source videos into the public GitHub repo.
2. In the repo root, extract and verify the original media and artifact files:

   ```bash
   python3 -m studio_factory.review_web import-archive \
     --archive "$HOME/Downloads/j4_all_available_resources_lossless_2026-11-22.zip" \
     --destination "$HOME/Higgsfield-Private/J4"
   ```

   Verification **must** report `verified: 267`, `missing: []`, `mismatch: []`. The archive is 76,407,296 bytes, SHA-256 `4efe79aa309c193382a82e6c4c56654881df5dbba66df7cfc45df84f0ca3011e`.
3. Start the local UI:

   ```bash
   python3 -m studio_factory.review_web serve \
     --repo . \
     --project j4-async-succession \
     --assets "$HOME/Higgsfield-Private/J4" \
     --db "$HOME/Higgsfield-Private/reviews.sqlite3" \
     --port 8765
   ```

4. Open `http://127.0.0.1:8765` **on the same Mac**. The server binds only to the loopback address. No public media URLs, Vercel deployment, model credentials or network-exposed web service are configured.

Use one asset directory per film and a new `--project <slug>`/`--assets` combination. If present, the project's `PROJECT.json` supplies the shot count, fps and title; the UI does not copy J4's human approvals, objects or story to new films.

## What the browser can display and play

| Kind | Review behavior | Limits |
| --- | --- | --- |
| Canonical shots | 25 shots, timecode/30 fps, full Image/Motion/Sound prompts, art method, props, story transition, review notes | These remain **text previs**, not generated takes |
| Video (`.mp4`, `.mov`, `.webm`) | HTML5 native `<video controls>`; HTTP `Range` for seek/scrub; original file, resolution and provenance | Source footage is for licensed local reference only, not a claim of contest-ready output |
| Audio (`.wav`, `.mp3`, `.flac`…) | HTML5 audio playback, cue review and local notes | No generated J4 score exists yet; missing cues show NOT_RUN |
| Images (`.png`, `.jpeg`, `.webp`) | Inline image and original download | Existing source photos must not be mistaken for generated keyframes |
| Historical experiment HTML | Sandboxed iframe for the legacy G1/G2/Lab interfaces, with scripts restricted to local content | Older mock/rehearsal PASS must not be treated as real media acceptance |
| Markdown / prompt / code | Readable styled Markdown, complete source text | HTML escaped to prevent model/source injection |
| JSON / CSV | JSON prettified, tabular CSV with headers; full raw source download | Initial CSV table limits 150 rows; raw bytes remain unchanged |
| ZIP and other binaries | File metadata, digest and explicit download | Not previewable as video/audio |
| 17 Domain Managers | Domain ownership, provenance and required handoff mechanics | UI records reviews; it does not perform unauthorized manager actions |
| Built-in tests | Only four whitelisted read-only checks (manager tests, budget, source inventory hashes, timecode) | No arbitrary shell command execution or paid generation |

Every item supports `PASS / FAIL / DEFER / NOT_RUN`, reviewer, notes and evidence link in an auto-saving local SQLite database. Shortcut keys: ←/→ items, 1/2 pass/fail, D defer, U undo, ⌘S save, ⌘↵ save/next. Explicit human review labels **do not** change generation, rights or contest approval gates.

The J4 archive has 267 inventoried files, including 21 audiovisual/image source artifacts. The local application adds 25 canonical shots, 17 Manager domains and 4 whitelisted tests. If you add new draft/render/audio files under `$HOME/Higgsfield-Private/J4/extra/`, restart the app to index them as supplemental candidates. They start with NOT_RUN, not an assumed PASS.

## Google Drive as the durable media store

The private Drive vault contains the entire 76 MB ZIP, the three original MP4s and two original JPEGs as **independent** files, and an inventory JSON. Google Drive confirmed `shared=false` on the media objects. Verified filenames and their source hashes are recorded in `projects/j4-async-succession/archive/MEDIA_CUSTODY.md`; no private file ID, OAuth token or signed download URL is committed.

The **local site plays local cached bytes**, not unauthenticated Google Drive share URLs. This is intentional: private Drive files generally cannot be streamed as public anonymous media, and the site cannot silently assume a Drive OAuth session. Restore from the downloaded private ZIP, or configure an authenticated rclone remote locally. Example (after configuring your own rclone remote and validating source/destination):

```bash
# optional only, run locally; adapt remote and path to your own Drive setup
rclone copy 'gdrive:Higgsfield-Studio-Private-Assets/J4-ASYNC-SUCCESSION' \
  "$HOME/Higgsfield-Private/J4/from-drive" --progress
```

Directly synced original videos can be placed under `extra/`, or use the SHA-verified archive import to recreate the full historical asset tree. For file-specific Drive links in the UI, pass `--drive-manifest <private-json>` containing `{"folder_url":"https://drive.google.com/drive/folders/...","objects":[{"name":"IMG_7835.mp4","url":"https://drive.google.com/file/d/.../view"}]}`. Keep this JSON private (e.g. outside the Git checkout).

## Security & testing

- Server listens on `127.0.0.1`, validates Host/Origin and CSRF on POSTs, and serves media only through allowlisted inventory IDs.
- Reviews live outside Git, and the website never uploads raw personal material, sends network requests to provider APIs, performs a render, or calls paid model endpoints.
- Test with `python3 -m unittest discover -s studio_factory/tests -v` and `python3 budget/test_track.py`.
- Optional Playwright visual smoke (requires `pip install playwright` and `python -m playwright install chromium`): `python3 studio_factory/tests/ui_review_smoke_ci.py --out /tmp/review-screens`.
- Media testing is separate: verify the ZIP SHA before extraction and use the site’s `Local media inventory SHA-256` test button. Chromium in some hosted sandboxes disallows direct localhost navigation; this test suite separates offline browser-component checks from actual HTTP/Range/SQLite integration checks. Actual Mac playback needs local browser acceptance.
- Renderer cannot perform legal rights clearance, contest eligibility validation or camera-motion judging automatically. Those remain explicitly NOT_RUN until grounded media and human review exist.

## Work across many films

Each new `projects/<slug>/PROJECT.json` remains a separate production. Generic research, art method, sound technique, optical principles, tests and Manager skill contracts can be promoted to immutable shared records via `studio_factory`; media, paid budgets, personal identities, story and licensing rights remain project-private. A second film never inherits the J4 owner approval.

## Addendum 2026-11-23: integrity, backup and per-production commands

Appended by the handoff-breakpoint fix branch; nothing above is changed.

- `import-archive --archive <zip> --destination <dir> --repo . --project <slug>` reads `asset_archive.sha256` from `PROJECT.json` and hashes the ZIP **before** extraction; on mismatch nothing is extracted. `--expect-sha256 <hex>` overrides. Without either, a warning is printed.
- `verify-assets --assets <dir>` re-reads every file against `MANIFEST/inventory.json` and prints PASS / FAIL / BLOCKED (exit 1 unless PASS).
- The inventory test is BLOCKED when the manifest is missing and FAIL when verified ≠ `PROJECT.json` `expected_asset_files`; a 0/0 PASS is no longer possible.
- `backup-reviews --db <db> --out <new file>` makes an SQLite online backup, runs `integrity_check`, writes `<out>.receipt.json` with its SHA-256 and never overwrites. `restore-reviews --backup <file> --db <db>` verifies the receipt and keeps any existing DB as `<db>.pre-restore-<timestamp>`. Keep backups private, next to the assets, never in Git.
- A review DB is bound to the first production that opens it (`store_meta`); opening it for another slug is refused. Use one DB per film.
- A new production supplies `shots.json` (or `PROJECT.json` `shots_file`) and optionally `global_interrupt {shot, at_ms, label_zh}`; the UI no longer contains J4 names.
