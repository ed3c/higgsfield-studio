# Handoff breakpoint fixes — addendum 2026-11-23

Branch `fix/handoff-breakpoints-20261123`, based on the audited PR #1 head `f564073f64bf1298ae82e08167b474a97a87496b`. Append-only: no earlier doc, prompt, source version or contract was rewritten. Work and verification ran on the Grok Bot box only (not the owner's Mac), 2026-11-23 ~20:00–20:40 Asia/Taipei.

Status rule: PASS only where the check was re-run on the box after the fix. GitHub CI is not a Mac/Safari playback or artistic-quality pass.

## Breakpoint matrix

| ID | handoff.md expectation | Before (audit 2026-11-22) | Fix commit | After evidence (box re-run) | Status |
|---|---|---|---|---|---|
| G-13 | `python budget/test_track.py` runs on the owner's Python | FAIL on Python 3.15: argparse rejects bare `80%` in help | `b02981c` (+ CI `f225cba` adds 3.15 matrix) | budget 7/7 OK on 3.13.5 and 3.15.2; new strict-argparse regression test | PASS |
| G-14 | Inventory gate proves 267/267 | FAIL: missing manifest gave vacuous 0/0 PASS | `7732da1` | empty assets dir → inventory BLOCKED 0/267 + startup WARNING; real assets → PASS 267/267 | PASS |
| HOF-07 | Git preserves every vetted text/code source byte-exact | FAIL: 32 CSVs only as parsed JSON, 42 `.py` (+3 `.js`) only in the ZIP | `ed566cb` | 77 files byte-exact vs ZIP (SHA-256 manifest + test); `files/** -text`; fresh-clone check | PASS (licence flag on 2 third-party citation CSVs, see README there) |
| HOF-09 | Review tool reusable for a second film, J4 only one project | FAIL: UI/JS hardcoded J4, S18, IMG names; one shared DB | `96d88f8`, `5d9aeb9` | 0 J4/S18/IMG strings in `review_site/`; second-film namespace tests; DB bound per project (other slug refused live); startup line names the slug | PASS (code); method promotion to shared still owner/rights decision |
| ZIP-pre | "Verify ZIP SHA-256 before extraction" | Not implemented (hash only after extract) | `a8e52cb` | wrong hash → `nothing extracted`, dest absent; PROJECT.json hash → 267 verified, `archive_sha256_checked: true` | PASS |
| HOF-05 | Review decisions survive restart and can be backed up/restored | BLOCKED: no backup/restore path | `ef42f90` | live write DEFER → restart → still present; backup integrity ok + receipt; overwrite refused; restore 1 row; tampered backup refused | PASS (box). Mac copy not re-run |
| HOF-11 | Readback/DR tooling | NOT_RUN | `a8e52cb`, `ef42f90` | `verify-assets` PASS 267, backup/restore above | NOT_RUN (retention/DR policy is an owner decision; tooling only) |
| HOF-03 / 12 UI | Usable local review in Safari, desktop + mobile | BLOCKED; box GUI audit found CSP inline-style errors, favicon 404, mobile drawer unusable, search closing drawer | `79990f1` | 0 `style="` left; `/favicon.ico` 204; Playwright desktop/mobile smoke PASS (headless Chrome) | BLOCKED (Safari + human A/V on the Mac still required) |
| CI | Tests guard archives and budget tools | CI path filter only `studio_factory/**`; Python 3.12 only | `f225cba` | YAML parsed; filters include `budget/**`, `projects/**` | NOT_RUN until GitHub Actions runs on the PR |

## Other HOF items

| ID | Status | Reason |
|---|---|---|
| HOF-01, 02, 04 | PASS (unchanged) | Re-confirmed: catalog 267 / 25 shots / 17 managers / 4 tests; Range 206 ×3 + 416 on IMG_7835/7836/7876 |
| HOF-06 | BLOCKED | Verbatim chat export does not exist; not invented |
| HOF-08 | NOT_RUN | Rights, likeness, contest eligibility: human review only |
| HOF-10 | NOT_RUN | Remote-access design is an owner decision; server stays loopback-only |

## Re-run evidence (box)

- unittest: 31 tests OK on Python 3.13.5 and 3.15.2; `budget/test_track.py` 7 OK on both.
- Live server port 8775 (fresh DB): `/` 200, `/api/health` READY, `Server: StudioReview/1.0`, `/favicon.ico` 204, assets 267/267, all 4 tests PASS.
- Live server port 8776 (empty assets): assets 0/267, WARNING, inventory BLOCKED, other tests PASS.
- The earlier GUI audit server (port 8765, PR #1 head) was not touched.

## Not fixed, by choice

- `pipeline/build_animatic.py` legacy schema: file is absent from the PR head and the ZIP; not invented.
- JSON/MD/HTML/TXT/SRT originals: already represented by the versioned JSON archives.
- Native `<video>` time readout: browser-owned.
- No media, footage, Drive IDs or emails committed.

## Merge note

PR #3 (`fix/j4-art-mechanism-compiler-g2-20261123`) edits `review_web.py`, `app.js`, `index.html`, `LOCAL_REVIEW.md` and UI tests; expect conflicts with this branch.
