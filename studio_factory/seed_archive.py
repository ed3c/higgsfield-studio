"""Idempotent offline import of J4's Git text archives into the reusable registry."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from .core import Factory

def classify(name):
    text=name.lower()
    for token,domain in [
      ("sonic","sound"),("sound","sound"),("prompt","prompt"),
      ("shots","shot"),("shotlist","shot"),("timeline","shot"),
      ("illusion","optical"),("optic","optical"),("character","character"),
      ("prop","asset"),("asset","asset"),("art_","art_direction"),
      ("source","research"),("budget","budget"),("qc","qc"),
      ("test","qc"),("trial","experiment"),("stimulus","experiment"),
      ("review","experiment")
    ]:
        if token in text:return domain
    return "provenance"

def sources(project_dir):
    for path in sorted((project_dir/"archive"/"v2_6").glob("*")):
        if path.is_file() and path.suffix in {".md",".csv",".json",".html",".py"}:
            yield "v2_6",path.name,path.read_text(encoding="utf-8"),path.as_posix()
    for folder in sorted((project_dir/"archive").glob("v*")):
        if folder.name=="v2_6":continue
        blob=folder/"conversation_text_archive.json"
        if not blob.is_file():continue
        record=json.loads(blob.read_text(encoding="utf-8"))
        for f in record["files"]:
            yield folder.name,f["filename"],f["content"],blob.as_posix()+"#"+f["filename"]

def seed(factory,project_dir,slug="j4-async-succession"):
    if not factory.db.execute("SELECT 1 FROM projects WHERE slug=?", (slug,)).fetchone():
        factory.create_project(slug)
    created=skipped=0
    for version,name,content,uri in sources(Path(project_dir)):
        domain=classify(name)
        key=re.sub(r"[^A-Za-z0-9._-]","-",version+"--"+name)[:128]
        meta={"source_version":version,"filename":name,
              "content_sha256":hashlib.sha256(content.encode("utf-8")).hexdigest(),
              "status":"SOURCE_ARCHIVED_NOT_QC_APPROVED"}
        row=factory.db.execute(
          "SELECT id,payload,uri FROM artifacts WHERE namespace=? AND domain=? AND asset_key=? ORDER BY revision DESC LIMIT 1",
          (f"projects/{slug}",domain,key)).fetchone()
        if row and json.loads(row["payload"])==meta and row["uri"]==uri:
            skipped+=1;continue
        factory.publish(namespace=f"projects/{slug}",domain=domain,key=key,
                        uri=uri,payload=meta,expected_previous=row["id"] if row else None)
        created+=1
    return {"created":created,"unchanged":skipped,"project":slug}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("project_directory",type=Path)
    p.add_argument("--db",default=".factory/registry.sqlite3")
    a=p.parse_args();factory=Factory(a.db)
    try:print(json.dumps(seed(factory,a.project_directory),indent=2))
    finally:factory.close()
