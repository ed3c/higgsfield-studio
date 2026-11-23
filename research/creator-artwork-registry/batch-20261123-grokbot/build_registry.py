#!/usr/bin/env python3
"""Deterministically derive batch-20261123-grokbot registry rows from the immutable
research/creators.json plus the named obligations in CREATIVE_RESEARCH_SCOPE.md §1.
Reads only; never writes back to research/*.json. Re-run to reproduce the JSONL files."""
import json, re, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BATCH = "batch-20261123-grokbot"
src_path = REPO / "research" / "creators.json"
raw = src_path.read_bytes()
src_sha = hashlib.sha256(raw).hexdigest()
data = json.loads(raw)
creators = data["creators"]
assert len(creators) == 79, len(creators)

def slug(s):
    s = re.sub(r"[（(].*?[)）]", "", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "unnamed"

# Named obligations from CREATIVE_RESEARCH_SCOPE.md §1 -> historical record index (None = not in the 79)
NAMED = {
    "CR-TUPACABRA": None,
    "CR-ROCOCO": 0, "CR-PURGA": 0,  # one historical record; scope requires distinct studio/person/award roles -> gap G-07
    "CR-AIST": 1, "CR-ZACK": 2, "CR-JOEY": 48, "CR-TSEILY": 38, "CR-ALEKSANDRA": 39,
    "CR-YOAV": 7, "CR-AUTHORS": 72, "CR-TAMBV": 11, "CR-ONEOFONE": 68, "CR-BOXEL": 67,
}
named_by_idx = {}
for k, v in NAMED.items():
    if v is not None:
        named_by_idx.setdefault(v, []).append(k)

rows, sources, seen_src = [], [], {}

def add_source(url, kind, provided_by_user, claim_type, note, creator_ids):
    if url in seen_src:
        s = sources[seen_src[url]]
        for c in creator_ids:
            if c not in s["consumer_ids"]:
                s["consumer_ids"].append(c)
        return s["source_id"]
    sid = f"SRC-{len(sources)+1:04d}"
    seen_src[url] = len(sources)
    sources.append({
        "source_id": sid, "batch_id": BATCH, "source_url": url, "media_kind": kind,
        "provided_by_user": provided_by_user, "capture_timestamp": None,
        "reference_asset_sha256": None, "claim_type": claim_type,
        "analysis_status": "NOT_YET_ANALYZED", "use_scope": "UNKNOWN",
        "rights_status": "UNKNOWN", "external_processing_allowed": "UNKNOWN",
        "consumer_ids": list(creator_ids), "provenance_notes": note,
    })
    return sid

for i, c in enumerate(creators):
    cid = f"HC79-{i:03d}-{slug(c.get('hf_username') or c['name'])}"
    sids = [add_source(u, "web_page", False, "SOURCE_EVIDENCE",
                       "listed in research/creators.json (2026-11-21); not re-fetched in this batch", [cid])
            for u in c.get("sources", [])]
    rows.append({
        "creator_id": cid, "batch_id": BATCH, "historical_index": i,
        "historical_source": f"research/creators.json#creators[{i}]", "historical_source_sha256": src_sha,
        "display_name": c["name"], "hf_username": c.get("hf_username"), "also_hf": c.get("also_hf", []),
        "domain_tags": c.get("domains", []), "category": c.get("category"),
        "historical_confidence": c.get("confidence"), "award_claim": c.get("award"),
        "notable_raw": c.get("notable"), "source_ids": sids,
        "named_obligations": named_by_idx.get(i, []),
        "claim_type": "SOURCE_EVIDENCE" if c.get("confidence") == "verified" else "UNVERIFIED_CLAIM",
        "analysis_status": "NOT_YET_ANALYZED",
        "artwork_extraction_status": "NOT_RUN",
        "rights_status": "UNKNOWN", "use_scope": "UNKNOWN", "external_processing_allowed": "UNKNOWN",
        "provenance_notes": "Copied field-for-field from the historical inventory; no new verification performed in this batch.",
    })

for j, c in enumerate(data.get("lower_confidence_candidates", [])):
    rows.append({
        "creator_id": f"HCLOW-{j:03d}-{slug(c['name'])}", "batch_id": BATCH, "historical_index": None,
        "historical_source": f"research/creators.json#lower_confidence_candidates[{j}]",
        "historical_source_sha256": src_sha, "display_name": c["name"], "hf_username": None,
        "domain_tags": [], "category": "lower_confidence_candidate", "historical_confidence": c.get("reason"),
        "notable_raw": c.get("notable"), "source_ids": [], "named_obligations": [],
        "claim_type": "UNVERIFIED_CLAIM", "analysis_status": "NOT_YET_ANALYZED",
        "artwork_extraction_status": "NOT_RUN", "rights_status": "UNKNOWN", "use_scope": "UNKNOWN",
        "external_processing_allowed": "UNKNOWN",
        "provenance_notes": "Not counted in the 79; preserved so it is not silently dropped.",
    })

# New record required by the scope: @tupacabra is NOT among the 79.
tup = "CR-TUPACABRA"
tup_srcs = [
    add_source("https://x.com/tupacabra", "social_profile", True, "SOURCE_EVIDENCE",
               "User-supplied handle (scope §1). Profile not opened in this batch.", [tup]),
    add_source("https://x.com/tupacabra/status/2121357879341166683", "x_post_video", False, "UNVERIFIED_CLAIM",
               "Post ID cited by secondary pages found via web search 2026-11-23; post/video NOT opened or downloaded in this batch.", [tup]),
    add_source("https://www.youtube.com/watch?v=Xeto4CMwvzA", "video", False, "UNVERIFIED_CLAIM",
               "Search result titled 'NUREMBERG 1561 - Official Trailer'; channel ownership by @tupacabra NOT verified.", [tup]),
    add_source("https://aifilmhistory.org/entry/nuremberg-official-trailer", "secondary_article", False, "UNVERIFIED_CLAIM",
               "Secondary description (Venice AI attribution, ~90 s, earlier 'NUREMBERG - 1561 A.D.' clip). Snippet only.", [tup]),
    add_source("https://sloptvnews.com/nuremberg-ai-concept-trailer-venice-viral/", "secondary_article", False, "UNVERIFIED_CLAIM",
               "Secondary article; metrics and tool attribution are claims, not measured here.", [tup]),
    add_source("https://www.artevolves.com/videos/nuremberg-official-trailer/", "secondary_article", False, "UNVERIFIED_CLAIM",
               "Secondary listing, duration 1:27 claimed.", [tup]),
]
rows.append({
    "creator_id": tup, "batch_id": BATCH, "historical_index": None, "historical_source": None,
    "historical_source_sha256": None, "display_name": "TUPACABRA", "hf_username": None,
    "domain_tags": ["film", "scifi", "shorts", "social-distribution"], "category": "benchmark_seed_case",
    "historical_confidence": None, "award_claim": None,
    "notable_raw": "NUREMBERG - Official Trailer (AI concept trailer). Tool attribution 'Venice AI' and reach metrics are UNVERIFIED_CLAIM from secondary sources.",
    "source_ids": tup_srcs, "named_obligations": [tup], "claim_type": "UNVERIFIED_CLAIM",
    "analysis_status": "NOT_YET_ANALYZED", "artwork_extraction_status": "PARTIAL_NAMED_ONLY",
    "rights_status": "UNKNOWN", "use_scope": "UNKNOWN", "external_processing_allowed": "UNKNOWN",
    "provenance_notes": "New in this batch because the scope names it and it is absent from the 79. Not merged into the historical count.",
})

def cid_of(idx):
    return next(r["creator_id"] for r in rows if r["historical_index"] == idx)

ART = [
    ("AW-NUREMBERG-TRAILER", tup, "NUREMBERG - Official Trailer", "trailer", "UNVERIFIED_CLAIM",
     [tup_srcs[1], tup_srcs[3], tup_srcs[4], tup_srcs[5]], "Primary benchmark seed work. Media NOT inspected."),
    ("AW-NUREMBERG-1561AD", tup, "NUREMBERG - 1561 A.D. / NUREMBERG 1561 (earlier clip, per secondary source)", "short", "UNVERIFIED_CLAIM",
     [tup_srcs[2], tup_srcs[3]], "Link between this video and @tupacabra not verified."),
    ("AW-LISTEN-TO-MEH", cid_of(0), "Listen to Meh", "short_film", "SOURCE_EVIDENCE", [], "Studio/person/award roles must be reconciled (scope CR-PURGA)."),
    ("AW-LOREM-IPSUM", cid_of(0), "Lorem Ipsum (with GUT Mexico City)", "ad", "UNVERIFIED_CLAIM", [], "Award claim from historical notable field."),
    ("AW-FUKUSHIMA", cid_of(1), "Fukushima", "short_film", "SOURCE_EVIDENCE", [], ""),
    ("AW-FIELD-AGENT", cid_of(2), "The Field Agent", "short_film", "NEEDS_VERIFICATION", [], "Scope: verify work/handle linkage."),
    ("AW-SOULLESS", cid_of(7), "Soulless", "short_film", "UNVERIFIED_CLAIM", [], ""),
    ("AW-GIRLS-DEMONS", cid_of(11), "GIRLS / DEMONS", "music_video", "UNVERIFIED_CLAIM", [], ""),
    ("AW-JOEY-PIPELINE", cid_of(48), "Story Bible / Castkit / Scenecraft / Shotcaller / Motiondojo skill pipeline", "method_skill_pack", "UNVERIFIED_CLAIM", [], "TinyURL-hosted pack not archived; see gap G-10."),
]
arts = []
for aid, cid, title, kind, ct, sids, note in ART:
    row = next(r for r in rows if r["creator_id"] == cid)
    arts.append({
        "artwork_id": aid, "batch_id": BATCH, "creator_id": cid, "title": title, "media_kind": kind,
        "source_ids": sids or row["source_ids"], "original_work_link": None, "reference_asset_sha256": None,
        "domain_tags": row["domain_tags"], "claim_type": ct, "confidence": "low" if ct != "SOURCE_EVIDENCE" else "medium",
        "analysis_status": "NOT_YET_ANALYZED", "use_scope": "UNKNOWN", "rights_status": "UNKNOWN",
        "external_processing_allowed": "UNKNOWN", "consumer_ids": ["Creator Intelligence", "Art Direction", "Cinematography / Motion"],
        "provenance_notes": note,
    })

for name, data_ in (("creators.jsonl", rows), ("artworks.jsonl", arts), ("sources.jsonl", sources)):
    (HERE / name).write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in data_), encoding="utf-8")

hist = [r for r in rows if r["historical_index"] is not None]
assert len(hist) == 79 and sorted(r["historical_index"] for r in hist) == list(range(79))
print(f"creators.jsonl: {len(rows)} rows (79 historical + {len(rows)-79-1} lower-confidence + 1 new CR-TUPACABRA)")
print(f"artworks.jsonl: {len(arts)} rows; sources.jsonl: {len(sources)} rows; creators.json sha256 {src_sha}")
