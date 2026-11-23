"""SQLite-backed immutable artifact registry and domain-manager handoffs.

Design constraints:
- Shared knowledge is reusable; project decisions and approvals are scoped.
- Producer alone may publish revisions. Consumer explicitly acknowledges handoffs.
- References are hashes + URIs, not copied media. No source is overwritten.
- The system cannot spend credits or call image/video generation providers.
"""
from __future__ import annotations
import hashlib
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MANAGER_DOMAINS = (
    "portfolio", "research", "story", "art_direction", "character",
    "asset", "prompt", "shot", "optical", "sound", "generation",
    "budget", "rights", "qc", "delivery", "provenance", "experiment",
)
HANDOFFS = {
    "portfolio": {"research", "story", "budget", "rights"},
    "research": {"story", "art_direction", "rights", "provenance"},
    "story": {"art_direction", "character", "shot", "sound"},
    "art_direction": {"character", "asset", "prompt", "optical", "shot"},
    "character": {"asset", "prompt", "shot", "qc"},
    "asset": {"prompt", "shot", "optical", "sound", "qc", "provenance"},
    "prompt": {"shot", "sound", "generation", "qc"},
    "shot": {"optical", "sound", "generation", "qc", "delivery"},
    "optical": {"shot", "qc", "experiment"},
    "sound": {"qc", "delivery", "experiment"},
    "generation": {"qc", "budget", "provenance"},
    "budget": {"generation", "qc", "provenance"},
    "rights": {"generation", "qc", "delivery", "provenance"},
    "qc": {"generation", "delivery", "experiment"},
    "delivery": {"provenance", "portfolio"},
    "provenance": {"research", "rights", "qc", "delivery"},
    "experiment": {"art_direction", "prompt", "qc"},
}
PROJECT_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class FactoryError(ValueError):
    """A refused state transition or evidence mismatch."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


class Factory:
    def __init__(self, database: str | Path):
        self.database = str(database)
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.database)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
          slug TEXT PRIMARY KEY, created_at TEXT NOT NULL,
          budget_limit INTEGER NOT NULL, status TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS artifacts (
          id TEXT PRIMARY KEY, namespace TEXT NOT NULL,
          domain TEXT NOT NULL, asset_key TEXT NOT NULL,
          revision INTEGER NOT NULL, digest TEXT NOT NULL,
          uri TEXT NOT NULL, payload TEXT NOT NULL,
          supersedes TEXT, created_at TEXT NOT NULL,
          UNIQUE(namespace, domain, asset_key, revision)
        );
        CREATE TABLE IF NOT EXISTS links (
          source_id TEXT NOT NULL, target_id TEXT NOT NULL,
          relation TEXT NOT NULL,
          PRIMARY KEY(source_id, target_id, relation),
          FOREIGN KEY(source_id) REFERENCES artifacts(id),
          FOREIGN KEY(target_id) REFERENCES artifacts(id)
        );
        CREATE TABLE IF NOT EXISTS handoffs (
          event_id TEXT PRIMARY KEY, project TEXT NOT NULL,
          producer TEXT NOT NULL, consumer TEXT NOT NULL,
          asset_id TEXT NOT NULL, key TEXT NOT NULL,
          state TEXT NOT NULL, evidence TEXT NOT NULL,
          created_at TEXT NOT NULL, ack_at TEXT,
          UNIQUE(project,key),
          FOREIGN KEY(asset_id) REFERENCES artifacts(id),
          FOREIGN KEY(project) REFERENCES projects(slug)
        );
        CREATE TABLE IF NOT EXISTS gates (
          project TEXT NOT NULL, gate TEXT NOT NULL,
          state TEXT NOT NULL, approver TEXT NOT NULL,
          evidence_uri TEXT NOT NULL, updated_at TEXT NOT NULL,
          PRIMARY KEY(project, gate),
          FOREIGN KEY(project) REFERENCES projects(slug)
        );
        """)

    def close(self):
        self.db.close()

    def create_project(self, slug: str, budget_limit: int = 9000):
        if not PROJECT_RE.fullmatch(slug) or budget_limit <= 0:
            raise FactoryError("invalid project slug or budget")
        with self.db:
            self.db.execute(
                "INSERT INTO projects VALUES(?,?,?,?)",
                (slug, _now(), budget_limit, "planning"))
        return slug

    def publish(self, *, namespace: str, domain: str, key: str,
                uri: str, payload: dict, expected_previous: str | None = None,
                derived_from: tuple[str, ...] = ()) -> str:
        if domain not in MANAGER_DOMAINS or not KEY_RE.fullmatch(key):
            raise FactoryError("unknown manager or invalid key")
        if namespace != "shared":
            if not namespace.startswith("projects/"):
                raise FactoryError("namespace must be shared or projects/<slug>")
            slug = namespace.split("/", 1)[1]
            if self.db.execute("SELECT 1 FROM projects WHERE slug=?", (slug,)).fetchone() is None:
                raise FactoryError("project does not exist")
        elif not payload.get("rights") or not payload.get("source"):
            raise FactoryError("shared knowledge requires rights and source provenance")
        if not isinstance(payload, dict) or not uri:
            raise FactoryError("payload must be an object and uri cannot be empty")
        previous = self.db.execute(
            "SELECT id, revision FROM artifacts WHERE namespace=? AND domain=? AND asset_key=? "
            "ORDER BY revision DESC LIMIT 1", (namespace, domain, key)).fetchone()
        prev_id = previous["id"] if previous else None
        if prev_id != expected_previous:
            raise FactoryError("revision conflict: expected_previous must match latest")
        revision = previous["revision"]+1 if previous else 1
        asset_id = f"{namespace}/{domain}/{key}@{revision}"
        digest = hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()
        with self.db:
            self.db.execute("INSERT INTO artifacts VALUES(?,?,?,?,?,?,?,?,?,?)",
                (asset_id, namespace, domain, key, revision, digest,
                 uri, _json(payload), prev_id, _now()))
            for parent in derived_from:
                if self.db.execute("SELECT 1 FROM artifacts WHERE id=?", (parent,)).fetchone() is None:
                    raise FactoryError(f"unknown parent: {parent}")
                self.db.execute("INSERT INTO links VALUES(?,?,?)",
                    (asset_id, parent, "derived_from"))
        return asset_id

    def get(self, asset_id: str) -> dict:
        row = self.db.execute("SELECT * FROM artifacts WHERE id=?", (asset_id,)).fetchone()
        if not row:
            raise FactoryError(f"unknown artifact: {asset_id}")
        value = dict(row)
        value["payload"] = json.loads(value["payload"])
        return value

    def reference(self, consumer_id: str, source_id: str, relation: str = "uses"):
        if consumer_id == source_id or not KEY_RE.fullmatch(relation):
            raise FactoryError("invalid reference")
        consumer, source = self.get(consumer_id), self.get(source_id)
        if source["namespace"] != "shared" and consumer["namespace"] != source["namespace"]:
            raise FactoryError("cross-project reuse requires promoting the source to shared")
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO links VALUES(?,?,?)",
                            (consumer_id, source_id, relation))

    def handoff(self, *, project: str, producer: str, consumer: str,
                asset_id: str, key: str, evidence: dict) -> str:
        if consumer not in HANDOFFS.get(producer, set()):
            raise FactoryError("handoff forbidden by domain contract")
        if not KEY_RE.fullmatch(key) or not evidence:
            raise FactoryError("handoff requires stable key and evidence")
        artifact = self.get(asset_id)
        if artifact["domain"] != producer:
            raise FactoryError("only artifact owner can hand off")
        if artifact["namespace"] not in ("shared", f"projects/{project}"):
            raise FactoryError("artifact belongs to another project")
        if self.db.execute("SELECT 1 FROM projects WHERE slug=?", (project,)).fetchone() is None:
            raise FactoryError("unknown project")
        old = self.db.execute(
            "SELECT * FROM handoffs WHERE project=? AND key=?", (project,key)).fetchone()
        if old:
            if (old["producer"], old["consumer"], old["asset_id"], old["evidence"]) != (
               producer, consumer, asset_id, _json(evidence)):
                raise FactoryError("idempotency key reused with different handoff")
            return old["event_id"]
        event_id = f"evt-{uuid.uuid4().hex}"
        with self.db:
            self.db.execute("INSERT INTO handoffs VALUES(?,?,?,?,?,?,?,?,?,?)",
                (event_id, project, producer, consumer, asset_id,
                 key, "PENDING", _json(evidence), _now(), None))
        return event_id

    def acknowledge(self, event_id: str, consumer: str):
        with self.db:
            row = self.db.execute("SELECT * FROM handoffs WHERE event_id=?",
                                  (event_id,)).fetchone()
            if not row or row["consumer"] != consumer:
                raise FactoryError("only intended consumer may ACK")
            if row["state"] == "ACK":
                return
            self.db.execute("UPDATE handoffs SET state='ACK',ack_at=? WHERE event_id=?",
                            (_now(),event_id))

    def set_gate(self, *, project: str, gate: str, state: str,
                 approver: str, evidence_uri: str):
        if state not in {"APPROVED", "BLOCKED", "NOT_RUN"}:
            raise FactoryError("invalid gate status")
        if state == "APPROVED" and (not approver or not evidence_uri):
            raise FactoryError("approval requires named approver and evidence")
        if self.db.execute("SELECT 1 FROM projects WHERE slug=?", (project,)).fetchone() is None:
            raise FactoryError("unknown project")
        with self.db:
            self.db.execute("INSERT INTO gates VALUES(?,?,?,?,?,?) "
                "ON CONFLICT(project,gate) DO UPDATE SET state=excluded.state,"
                "approver=excluded.approver,evidence_uri=excluded.evidence_uri,"
                "updated_at=excluded.updated_at",
                (project,gate,state,approver,evidence_uri,_now()))

    def require_generation_gate(self, project: str, estimated_credits: int,
                                spent_credits: int, authorized_actor: str):
        """Read-only guard, not an approval UI or generation trigger."""
        row=self.db.execute("SELECT budget_limit FROM projects WHERE slug=?",
                            (project,)).fetchone()
        if row is None or estimated_credits<0 or spent_credits<0:
            raise FactoryError("invalid project or credits")
        if estimated_credits+spent_credits>row["budget_limit"]:
            raise FactoryError("monthly budget cap exceeded")
        for gate in ("owner_approval","director_estimate_posted",
                     "live_balance_checked","rights_review"):
            g=self.db.execute("SELECT * FROM gates WHERE project=? AND gate=?",
                              (project,gate)).fetchone()
            if not g or g["state"]!="APPROVED" or not g["evidence_uri"]:
                raise FactoryError(f"generation BLOCKED: {gate}")
        if not authorized_actor:
            raise FactoryError("explicit authorized actor required")
        return "ELIGIBLE_FOR_SEPARATE_HUMAN_EXECUTION"

    def export_manifest(self, project: str) -> dict:
        rows=self.db.execute(
          "SELECT * FROM artifacts WHERE namespace IN (?, 'shared') ORDER BY namespace,domain,asset_key,revision",
          (f"projects/{project}",)).fetchall()
        if self.db.execute("SELECT 1 FROM projects WHERE slug=?", (project,)).fetchone() is None:
            raise FactoryError("unknown project")
        return {"project":project,"exported_at":_now(),"artifacts":[
             {**dict(r),"payload":json.loads(r["payload"])} for r in rows],
             "links":[dict(r) for r in self.db.execute("SELECT l.* FROM links l JOIN artifacts a ON a.id=l.source_id WHERE a.namespace=?", (f"projects/{project}",))],
             "handoffs":[dict(r) for r in self.db.execute(
                 "SELECT * FROM handoffs WHERE project=?", (project,))],
             "gates":[dict(r) for r in self.db.execute(
                 "SELECT * FROM gates WHERE project=?", (project,))]}
