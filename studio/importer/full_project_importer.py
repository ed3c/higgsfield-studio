"""Generic Full Project Importer (HF-AGENTIC-FILM-2026-11-26, handoff §4/§14).

Builds a ``full-project-inventory.v1`` record from evidence that adapters can
legitimately read. It is not tied to any one project: the Higgsfield
publication adapter keys on the page's own serialized ``project`` record, and
other platforms or owner exports plug in as further adapters.

Rules carried from the handoff:
- Coverage per item type is reported separately; the importer never reports
  PASS. ``import_status`` is PARTIAL or COMPLETE_CANDIDATE, and a candidate
  still needs an independent verifier (Oracle) before H03/H04 can move.
- Third-party archives are SUPPLEMENTAL only and never count toward official
  coverage (handoff §3 S6, §14).
- No network access happens here. Callers pass saved bytes (HTML, export
  directories) whose acquisition is logged separately.
- A rendered MP4 is not a full project export.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Protocol

from .seroval_lite import SerovalParseError, parse_assignment_after

SCHEMA_ID = "full-project-inventory.v1"

ITEM_TYPES = (
    "project", "elements", "assets", "storyboard", "previs", "video", "audio",
    "prompts", "model_params", "timeline", "canvas", "rights",
)

# Coverage vocabulary (handoff §9 state words plus acquisition-specific ones).
OBTAINED = "OBTAINED"                  # official evidence read and recorded
PARTIAL = "PARTIAL"                    # some official evidence, known gaps
BROWSER_REQUIRED = "BROWSER_REQUIRED"  # exposed by the source but only via a rendered desktop session
NOT_EXPOSED = "NOT_EXPOSED"            # source explicitly says it is hidden/absent
UNKNOWN = "UNKNOWN"                    # no evidence either way
NOT_RUN = "NOT_RUN"
COVERAGE_STATES = (OBTAINED, PARTIAL, BROWSER_REQUIRED, NOT_EXPOSED, UNKNOWN, NOT_RUN)

OFFICIAL = "OFFICIAL"
OWNER_EXPORT = "OWNER_EXPORT"
THIRD_PARTY_SUPPLEMENTAL = "THIRD_PARTY_SUPPLEMENTAL"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class SourceInput:
    """One piece of saved evidence handed to the importer."""
    kind: str                      # "html_publication" | "export_dir" | "third_party_archive"
    path: Path
    url: str | None = None
    retrieved_at: str | None = None
    note: str = ""


@dataclass
class AdapterResult:
    adapter: str
    evidence_class: str
    source: dict[str, Any]
    project: dict[str, Any] = field(default_factory=dict)
    items: list[dict[str, Any]] = field(default_factory=list)
    coverage: dict[str, dict[str, Any]] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class Adapter(Protocol):
    name: str
    def can_handle(self, src: SourceInput) -> bool: ...
    def collect(self, src: SourceInput) -> AdapterResult: ...


def _cov(state: str, reason: str, **extra: Any) -> dict[str, Any]:
    assert state in COVERAGE_STATES, state
    d = {"state": state, "reason": reason}
    d.update(extra)
    return d


class HiggsfieldPublicationHTMLAdapter:
    """Reads the public Cinema publication record that higgsfield.ai embeds in
    its server-rendered HTML (``project:{...}`` inside the dehydrated router
    state). Works for any published project page, not a specific slug."""

    name = "higgsfield-publication-html"

    def can_handle(self, src: SourceInput) -> bool:
        if src.kind != "html_publication":
            return False
        try:
            return "project:" in src.path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return False

    def collect(self, src: SourceInput) -> AdapterResult:
        raw = src.path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        res = AdapterResult(
            adapter=self.name, evidence_class=OFFICIAL,
            source={"kind": src.kind, "url": src.url, "sha256": sha256_bytes(raw),
                    "bytes": len(raw), "retrieved_at": src.retrieved_at, "note": src.note},
        )
        try:
            proj = parse_assignment_after(text, "project:")
        except SerovalParseError as exc:
            res.errors.append(f"publication record not parseable: {exc}")
            for t in ITEM_TYPES:
                res.coverage[t] = _cov(UNKNOWN, "publication record not parseable")
            return res
        if not isinstance(proj, dict) or "id" not in proj:
            res.errors.append("publication record has no id")
            return res

        author = proj.get("author") or {}
        info = proj.get("info") or {}
        info_kv = {d.get("key"): d.get("value") for d in info.get("information") or [] if isinstance(d, dict)}
        res.project = {
            "platform": "higgsfield",
            "publication_id": proj.get("id"),
            "slug": proj.get("slug"),
            "title": proj.get("title"),
            "description": proj.get("description"),
            "type": proj.get("type"),
            "created_at": proj.get("createdAt"),
            "owner_id": proj.get("ownerId"),
            "author_username": author.get("username"),
            "snapshot_folder_id": proj.get("snapshotFolderId"),
            "source_folder_id": proj.get("sourceFolderId"),
            "root_folder_id": proj.get("rootFolderId"),
            "featured_episode_slug": proj.get("featuredEpisodeSlug"),
            "show_prompts": proj.get("showPrompts"),
            "show_canvas": proj.get("showCanvas"),
            "license": info.get("license"),
            "reported_counters": info_kv,
            "id_kinds_note": "publication_id is the public Cinema publication; it is not a workspace project_id, Elements library ID or Editing Room ID until a source shows otherwise.",
        }
        for a in proj.get("media") or []:
            if isinstance(a, dict):
                res.items.append({
                    "type": "video" if a.get("kind") == "video" else (a.get("kind") or "asset"),
                    "id": a.get("id"), "title": a.get("name"),
                    "duration_seconds": a.get("durationSeconds"),
                    "width": a.get("width"), "height": a.get("height"),
                    "locators": {k: a.get(k) for k in ("src", "originalSrc", "thumbnail") if a.get(k)},
                    "evidence_class": OFFICIAL, "bytes_obtained": False,
                    "role": "publication_media",
                })
        listed_assets = [a for a in proj.get("assets") or [] if isinstance(a, dict)]
        for a in listed_assets:
            if not any(i["id"] == a.get("id") for i in res.items):
                res.items.append({"type": a.get("kind") or "asset", "id": a.get("id"), "title": a.get("title"),
                                  "locators": {"src": a.get("src")} if a.get("src") else {},
                                  "evidence_class": OFFICIAL, "bytes_obtained": False, "role": "publication_asset"})

        n_video = sum(1 for i in res.items if i["type"] == "video")
        res.coverage["project"] = _cov(OBTAINED, "public publication record parsed from server-rendered HTML",
                                       fields=sorted(k for k, v in res.project.items() if v is not None))
        res.coverage["video"] = _cov(
            PARTIAL if n_video else UNKNOWN,
            "final rendered film locator and probe fields recorded; bytes not downloaded (rights unresolved). A rendered MP4 is not a full project export." if n_video
            else "no video in publication record",
            count=n_video)
        res.coverage["assets"] = _cov(
            PARTIAL if listed_assets else UNKNOWN,
            f"publication lists {len(listed_assets)} asset(s) server-side; snapshot folder contents load client-side",
            listed=len(listed_assets), snapshot_folder_id=proj.get("snapshotFolderId"))
        sp, sc = proj.get("showPrompts"), proj.get("showCanvas")
        res.coverage["prompts"] = _cov(
            BROWSER_REQUIRED if sp else (NOT_EXPOSED if sp is False else UNKNOWN),
            "publication sets showPrompts=true but prompt records are not in server HTML" if sp
            else "publication hides prompts" if sp is False else "showPrompts flag absent")
        res.coverage["model_params"] = _cov(
            BROWSER_REQUIRED if sp else UNKNOWN,
            "settings/model per placement expected alongside prompts; not in server HTML")
        res.coverage["canvas"] = _cov(
            BROWSER_REQUIRED if sc else (NOT_EXPOSED if sc is False else UNKNOWN),
            "publication sets showCanvas=true but canvas graph is not in server HTML" if sc
            else "publication hides canvas" if sc is False else "showCanvas flag absent")
        for t in ("elements", "storyboard", "previs", "timeline"):
            res.coverage[t] = _cov(BROWSER_REQUIRED if (sp or sc) else UNKNOWN,
                                   f"no {t} records in server HTML; may live in canvas/snapshot folder rendered client-side")
        has_audio = any(i["type"] == "audio" for i in res.items)
        res.coverage["audio"] = _cov(
            PARTIAL if has_audio else UNKNOWN,
            "standalone audio items listed" if has_audio else
            "no standalone audio listed; final film audio track unverified until bytes are probed")
        lic = info.get("license")
        res.coverage["rights"] = _cov(
            PARTIAL if lic else UNKNOWN,
            f"publication license field: {lic!r}" if lic else
            "publication license field is null; public visibility is not a reuse grant (handoff §3)")
        return res


class LocalExportAdapter:
    """Owner-provided or officially exported directory. Expects an
    ``export_manifest.json`` listing ``{"path","type",...}`` entries; every
    listed file is hashed, unlisted files are reported, missing files fail."""

    name = "local-export-dir"

    def can_handle(self, src: SourceInput) -> bool:
        return src.kind == "export_dir" and (src.path / "export_manifest.json").is_file()

    def collect(self, src: SourceInput) -> AdapterResult:
        man_path = src.path / "export_manifest.json"
        man = json.loads(man_path.read_text(encoding="utf-8"))
        res = AdapterResult(adapter=self.name, evidence_class=man.get("evidence_class", OWNER_EXPORT),
                            source={"kind": src.kind, "manifest_sha256": sha256_file(man_path),
                                    "provided_by": man.get("provided_by"), "retrieved_at": src.retrieved_at})
        if res.evidence_class == OFFICIAL and not man.get("official_export_evidence"):
            res.errors.append("manifest claims OFFICIAL without official_export_evidence; downgraded to OWNER_EXPORT")
            res.evidence_class = OWNER_EXPORT
        res.project = dict(man.get("project") or {})
        listed = set()
        counts: dict[str, int] = {}
        for e in man.get("files") or []:
            p = src.path / e["path"]
            listed.add(p.resolve())
            t = e.get("type", "assets")
            if t not in ITEM_TYPES:
                res.errors.append(f"unknown item type {t!r} for {e['path']}")
                continue
            if not p.is_file():
                res.errors.append(f"listed file missing: {e['path']}")
                continue
            counts[t] = counts.get(t, 0) + 1
            res.items.append({"type": t, "id": e.get("id") or e["path"], "title": e.get("title"),
                              "path": e["path"], "sha256": sha256_file(p), "bytes": p.stat().st_size,
                              "evidence_class": res.evidence_class, "bytes_obtained": True,
                              **{k: v for k, v in e.items() if k in ("prompt_sha256", "model", "settings", "placement_id", "revision")}})
        unlisted = [str(p.relative_to(src.path)) for p in src.path.rglob("*")
                    if p.is_file() and p.resolve() not in listed and p.name != "export_manifest.json"]
        expected = man.get("expected_counts") or {}
        for t in ITEM_TYPES:
            got, exp = counts.get(t, 0), expected.get(t)
            if exp is None:
                res.coverage[t] = _cov(PARTIAL if got else UNKNOWN, "no expected count declared", obtained=got)
            elif got >= exp:
                res.coverage[t] = _cov(OBTAINED, "obtained matches declared expected count", obtained=got, expected=exp)
            else:
                res.coverage[t] = _cov(PARTIAL, "fewer files than declared expected count", obtained=got, expected=exp)
        if unlisted:
            res.errors.append(f"{len(unlisted)} unlisted file(s) present: {unlisted[:5]}")
        return res


class ThirdPartyArchiveAdapter:
    """Indexes a third-party prompt archive for cross-checking only."""

    name = "third-party-archive"

    def can_handle(self, src: SourceInput) -> bool:
        return src.kind == "third_party_archive" and src.path.exists()

    def collect(self, src: SourceInput) -> AdapterResult:
        files = [p for p in (src.path.rglob("*") if src.path.is_dir() else [src.path]) if p.is_file()]
        res = AdapterResult(adapter=self.name, evidence_class=THIRD_PARTY_SUPPLEMENTAL,
                            source={"kind": src.kind, "url": src.url, "files": len(files)})
        for p in files:
            res.items.append({"type": "prompts", "id": str(p.name), "sha256": sha256_file(p),
                              "evidence_class": THIRD_PARTY_SUPPLEMENTAL, "bytes_obtained": True})
        # Never contributes official coverage.
        return res


DEFAULT_ADAPTERS: tuple[Adapter, ...] = (
    HiggsfieldPublicationHTMLAdapter(), LocalExportAdapter(), ThirdPartyArchiveAdapter(),
)

_RANK = {OBTAINED: 5, PARTIAL: 4, BROWSER_REQUIRED: 3, NOT_EXPOSED: 2, UNKNOWN: 1, NOT_RUN: 0}


class FullProjectImporter:
    def __init__(self, adapters: Iterable[Adapter] = DEFAULT_ADAPTERS):
        self.adapters = list(adapters)

    def run(self, sources: Iterable[SourceInput], *, source_url: str | None = None,
            source_id: str | None = None) -> dict[str, Any]:
        results: list[AdapterResult] = []
        unhandled: list[str] = []
        for src in sources:
            ad = next((a for a in self.adapters if a.can_handle(src)), None)
            if ad is None:
                unhandled.append(f"{src.kind}:{src.path}")
                continue
            results.append(ad.collect(src))

        coverage = {t: _cov(NOT_RUN, "no adapter produced evidence") for t in ITEM_TYPES}
        project: dict[str, Any] = {}
        items: list[dict[str, Any]] = []
        supplemental: list[dict[str, Any]] = []
        errors: list[str] = [f"no adapter for {u}" for u in unhandled]
        for r in results:
            errors += [f"{r.adapter}: {e}" for e in r.errors]
            if r.evidence_class == THIRD_PARTY_SUPPLEMENTAL:
                supplemental += r.items
                continue
            for k, v in r.project.items():
                project.setdefault(k, v)
            items += r.items
            for t, c in r.coverage.items():
                if _RANK[c["state"]] > _RANK[coverage[t]["state"]]:
                    coverage[t] = dict(c, adapter=r.adapter)

        required = [t for t in ITEM_TYPES if t != "rights"]
        complete = all(coverage[t]["state"] in (OBTAINED, NOT_EXPOSED) for t in required) \
            and coverage["rights"]["state"] == OBTAINED
        return {
            "schema": SCHEMA_ID,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": {"url": source_url, "source_id": source_id},
            "project": project,
            "coverage": coverage,
            "items": items,
            "supplemental_items": supplemental,
            "adapters": [{"adapter": r.adapter, "evidence_class": r.evidence_class, "source": r.source} for r in results],
            "errors": errors,
            "import_status": "COMPLETE_CANDIDATE" if complete else "PARTIAL",
            "acceptance": {"status": NOT_RUN,
                           "note": "Importer output is producer evidence only. Full export PASS needs an independent Oracle check of the complete authorized inventory (handoff §14)."},
        }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--html", action="append", default=[], help="saved publication HTML (repeatable)")
    ap.add_argument("--export-dir", action="append", default=[], help="owner/official export dir with export_manifest.json")
    ap.add_argument("--supplemental-archive", action="append", default=[], help="third-party archive path (supplemental only)")
    ap.add_argument("--url"); ap.add_argument("--source-id"); ap.add_argument("--retrieved-at")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    srcs = [SourceInput("html_publication", Path(p), a.url, a.retrieved_at) for p in a.html]
    srcs += [SourceInput("export_dir", Path(p), retrieved_at=a.retrieved_at) for p in a.export_dir]
    srcs += [SourceInput("third_party_archive", Path(p)) for p in a.supplemental_archive]
    inv = FullProjectImporter().run(srcs, source_url=a.url, source_id=a.source_id)
    Path(a.out).write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"import_status": inv["import_status"],
                      "coverage": {k: v["state"] for k, v in inv["coverage"].items()},
                      "errors": inv["errors"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
