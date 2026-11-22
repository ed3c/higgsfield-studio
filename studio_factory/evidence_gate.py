"""G2 evidence-bound candidate intake and two-reviewer still-frame oracle.

Offline control plane: no generation, network, upload or image understanding.
It enforces evidence-chain integrity, not artistic accuracy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

from .art_contracts import ArtContractError, compile_shot, load_contract

SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
STILL_TYPES = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_TYPES = {".mp4", ".mov", ".webm"}


class EvidenceGateError(ValueError):
    """Invalid content, origin, or claimed evidence."""


def _require_str(obj: dict, key: str) -> str:
    val = obj.get(key)
    if not isinstance(val, str) or not val.strip() or len(val) > 4096:
        raise EvidenceGateError(f"{key} must be a non-empty string")
    return val


def _require_hash(val: Any, label: str) -> str:
    if not isinstance(val, str) or not SHA256_RE.fullmatch(val):
        raise EvidenceGateError(f"invalid SHA-256: {label}")
    return val


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest()


def _resolve_asset(asset_root: Path, relative: str) -> Path:
    root = asset_root.resolve(strict=True)
    if (not isinstance(relative, str) or not relative or
            Path(relative).is_absolute() or "\\" in relative or
            ".." in Path(relative).parts):
        raise EvidenceGateError("media reference must be a safe asset-root-relative path")
    path = (root / relative).resolve(strict=False)
    if not path.is_relative_to(root):
        raise EvidenceGateError("asset escaped authorized root")
    if not path.is_file():
        raise EvidenceGateError(f"missing media file: {relative}")
    if path.stat().st_size <= 0:
        raise EvidenceGateError("empty media file")
    return path


def _magic_matches(path: Path, media_type: str) -> bool:
    # Deliberately weak MIME check. It does not prove valid media decoding.
    with path.open("rb") as f:
        beginning = f.read(32)
    ext = path.suffix.lower()
    if media_type == "still":
        return (
            (ext == ".png" and beginning.startswith(b"\x89PNG\r\n\x1a\n"))
            or (ext in {".jpg", ".jpeg"} and beginning.startswith(b"\xff\xd8\xff"))
            or (ext == ".webp" and beginning.startswith(b"RIFF")
                and beginning[8:12] == b"WEBP"))
    return ((ext in {".mp4", ".mov"} and beginning[4:8] == b"ftyp")
            or (ext == ".webm" and beginning.startswith(b"\x1a\x45\xdf\xa3")))


def verify_receipt(registry: dict, asset_root: Path, receipt: dict) -> dict:
    if not isinstance(receipt, dict) or receipt.get("schema") != "studio.generation-receipt.v2":
        raise EvidenceGateError("unsupported generation receipt schema")
    compiled = compile_shot(registry, _require_str(receipt, "shot_id"))
    candidate = _require_str(receipt, "candidate_id")
    producer = _require_str(receipt, "producer")
    if receipt.get("project") != registry["contract"]["project"]:
        raise EvidenceGateError("project mismatch")
    for key in ("model", "model_version", "provider", "provider_run_id",
                "generated_at"):
        _require_str(receipt, key)
    if ("seed" not in receipt or
            (receipt["seed"] is not None and
             (isinstance(receipt["seed"], bool) or not isinstance(receipt["seed"], (str,int))))):
        raise EvidenceGateError("seed must be explicit (null if unavailable)")
    if receipt.get("settings") is None or not isinstance(receipt["settings"], dict):
        raise EvidenceGateError("settings object required")
    if receipt["settings"].get("aspect_ratio") != "9:16":
        raise EvidenceGateError("J4 aspect ratio must be 9:16")
    cost = receipt.get("credits")
    if not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0 or not math.isfinite(cost):
        raise EvidenceGateError("nonnegative numeric credit value required")
    if receipt.get("sent_prompt") != compiled["prompt"]:
        raise EvidenceGateError("exact SENT prompt differs from compiled prompt")
    if receipt.get("sent_negative_prompt") != compiled["global_negative_prompt"]:
        raise EvidenceGateError("sent negative differs from canonical negative")
    if receipt.get("compiled_payload_sha256") != compiled["payload_sha256"]:
        raise EvidenceGateError("compiled payload revision mismatch")
    if receipt.get("generation_gate_at_time") != "EXTERNALLY_APPROVED":
        raise EvidenceGateError("no explicit external generation authorization receipt")
    authorization = receipt.get("authorization_evidence")
    if not isinstance(authorization, dict) or any(not authorization.get(k) for k in
         ("owner", "director_estimate", "account_balance", "rights")):
        raise EvidenceGateError("missing 4 independent generation authorization records")
    if not isinstance(receipt.get("reference_assets"), list):
        raise EvidenceGateError("explicit reference_assets array required (may be empty)")
    for entry in receipt["reference_assets"]:
        if not isinstance(entry, dict):
            raise EvidenceGateError("invalid reference entry")
        ref_path = _resolve_asset(asset_root, _require_str(entry, "relative_path"))
        digest = _require_hash(entry.get("sha256"), "reference asset")
        if file_sha256(ref_path) != digest:
            raise EvidenceGateError("reference asset SHA-256 mismatch")
    media = receipt.get("output")
    if not isinstance(media, dict):
        raise EvidenceGateError("output descriptor missing")
    kind = media.get("media_type")
    if kind not in ("still", "video"):
        raise EvidenceGateError("media_type must be still or video")
    path = _resolve_asset(asset_root, _require_str(media, "relative_path"))
    if path.suffix.lower() not in (STILL_TYPES if kind == "still" else VIDEO_TYPES):
        raise EvidenceGateError("media extension incompatible with type")
    if not _magic_matches(path, kind):
        raise EvidenceGateError("media signature mismatch")
    digest = _require_hash(media.get("sha256"), "output")
    if file_sha256(path) != digest:
        raise EvidenceGateError("output SHA-256 mismatch")
    return {
        "candidate_id": candidate, "shot_id": compiled["shot_id"],
        "producer": producer, "media_type": kind,
        "media_sha256": digest, "relative_path": media["relative_path"],
        "compiled_payload_sha256": compiled["payload_sha256"],
        "provider_receipt_present": True,
        "rights_authorization_attested_not_authenticated": True,
        "decoded_media_qa": "NOT_RUN",
        "approved_for_new_generation": False,
    }


def _observation(review: dict, cid: str, expected_digest: str,
                 media_type: str, reviewer: str, polarity: str) -> tuple[str, str]:
    item = review.get("observations", {}).get(cid)
    if not isinstance(item, dict) or type(item.get("observed")) is not bool:
        return "MISSING", f"{cid}: no observed boolean"
    if item.get("media_sha256") != expected_digest:
        return "INVALID", f"{cid}: review media digest differs"
    note = item.get("evidence_note")
    if not isinstance(note, str) or not note.strip() or len(note) > 2000:
        return "INVALID", f"{cid}: evidence note missing"
    if item.get("full_frame") is not True:
        roi = item.get("roi_norm")
        if not isinstance(roi, list) or len(roi) != 4:
            return "INVALID", f"{cid}: normalized [x,y,w,h] ROI missing"
        if any(not isinstance(v, (float,int)) or isinstance(v, bool)
               or not math.isfinite(v) for v in roi):
            return "INVALID", f"{cid}: ROI must be finite numeric"
        x, y, w, h = roi
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > 1 or y + h > 1:
            return "INVALID", f"{cid}: ROI outside frame"
    # A still with a time marker other than 0 is not evidence of motion.
    if media_type == "still" and item.get("frame_at_ms", 0) != 0:
        return "INVALID", f"{cid}: static still cannot prove time"
    if media_type == "video":
        stamp = item.get("frame_at_ms")
        if not isinstance(stamp, int) or isinstance(stamp, bool) or stamp < 0:
            return "INVALID", f"{cid}: video needs a nonnegative timestamp"
    return ("PASS_OBSERVED" if item["observed"] == (polarity == "must_exist")
            else "FAIL_OBSERVED"), ""


def review_candidate(registry: dict, asset_root: Path,
                     receipt: dict, reviews: list[dict]) -> dict:
    """Accept at most evidence-bound *static* review, never art/rights approval.

    Fail-closed with exact binary hashes, source-pinned sent prompt, two different
    independently attested reviewer IDs. A still cannot prove optical motion or
    sound. Video needs separate decoded temporal/sound/cross-shot verification.
    """
    errors = []
    try:
        bound = verify_receipt(registry, asset_root, receipt)
    except (ArtContractError, EvidenceGateError, OSError) as exc:
        return {"state":"BLOCKED_INVALID_RECEIPT", "errors":[str(exc)],
                "ready_for_generation":False, "director_approval":"NOT_RUN"}
    sid=bound["shot_id"]
    prof=next(p for p in registry["contract"]["shots"] if p["shot_id"]==sid)
    static=[c for c in prof["checks"] if c["modality"]=="still"]
    pending=[c["id"] for c in prof["checks"] if c["modality"]!="still"]
    if not isinstance(reviews,list) or len(reviews)!=2:
        return {"state":"BLOCKED_INDEPENDENT_REVIEW", "errors":["exactly two independent review files required"],
                "candidate_id":bound["candidate_id"],"media_sha256":bound["media_sha256"],
                "pending_temporal":pending,"ready_for_generation":False,"director_approval":"NOT_RUN"}
    ids=[]
    values={}
    for review in reviews:
        if not isinstance(review, dict) or review.get("schema")!="studio.g2-review.v2":
            errors.append("unsupported reviewer format");continue
        reviewer=review.get("reviewer_id")
        if not isinstance(reviewer,str) or not reviewer.strip():
            errors.append("reviewer identity missing");continue
        ids.append(reviewer)
        observations=review.get("observations")
        if not isinstance(observations,dict):
            errors.append(f"{reviewer}: observations must be a map")
            continue
        allowed={c["id"] for c in static}
        extras=set(observations) - allowed
        if extras:
            errors.append(f"{reviewer}: unknown or non-still check IDs: {sorted(extras)}")
        for field,expected in (
          ("candidate_id",bound["candidate_id"]),
          ("shot_id",sid),
          ("media_sha256",bound["media_sha256"]),
          ("compiled_payload_sha256",bound["compiled_payload_sha256"])):
            if review.get(field)!=expected:
                errors.append(f"{reviewer}: {field} mismatch")
        observed={}
        for item in static:
            status,reason=_observation(review,item["id"],bound["media_sha256"],
                                       bound["media_type"],reviewer,item["polarity"])
            observed[item["id"]]=status
            if reason:errors.append(f"{reviewer}: {reason}")
        values[reviewer]=observed
    if len(ids)!=2 or len(set(ids))!=2 or bound["producer"] in ids:
        errors.append("two unique reviewers distinct from producer required")
    if errors:
        return {"state":"BLOCKED_EVIDENCE_INVALID","errors":errors,
                "candidate_id":bound["candidate_id"],"media_sha256":bound["media_sha256"],
                "pending_temporal":pending,"ready_for_generation":False,
                "director_approval":"NOT_RUN"}
    rejected=[];disputed=[];passed=[]
    for check in static:
        cid=check["id"];states={values[k][cid] for k in ids}
        if states=={"PASS_OBSERVED"}:passed.append(cid)
        elif states=={"FAIL_OBSERVED"}:rejected.append(cid)
        else:disputed.append(cid)
    if rejected:state="STATIC_REJECTED_BY_TWO_REVIEWERS"
    elif disputed:state="STATIC_DISPUTED_NEEDS_ADJUDICATION"
    else:state="STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN"
    return {
        "schema":"studio.g2-evidence-evaluation.v2",
        "candidate_id":bound["candidate_id"],"shot_id":sid,
        "media_sha256":bound["media_sha256"],
        "compiled_payload_sha256":bound["compiled_payload_sha256"],
        "state":state,"observed_not_machine_detected":True,
        "reviewers_attested_not_authenticated":ids,
        "passed_static_check_ids":passed,"rejected_static_check_ids":rejected,
        "disputed_static_check_ids":disputed,
        "pending_temporal":pending,"decoded_media_qa":"NOT_RUN",
        "originality_rights_review":"NOT_RUN","director_approval":"NOT_RUN",
        "paid_generation_gate":"BLOCKED","ready_for_generation":False,
    }


def main(argv=None):
    parser=argparse.ArgumentParser(prog="python -m studio_factory.evidence_gate")
    parser.add_argument("--repo",type=Path,default=Path.cwd())
    parser.add_argument("--assets",type=Path,required=True)
    parser.add_argument("--receipt",type=Path,required=True)
    parser.add_argument("--review",type=Path,action="append",default=[])
    parser.add_argument("--output",type=Path)
    args=parser.parse_args(argv)
    registry=load_contract(args.repo)
    receipt=json.loads(args.receipt.read_text(encoding="utf-8"))
    reviews=[json.loads(p.read_text(encoding="utf-8")) for p in args.review]
    result=review_candidate(registry,args.assets,receipt,reviews)
    output=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf-8")
    print(output,end="")
    return 0 if result["state"]=="STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN" else 2


if __name__=="__main__":
    raise SystemExit(main())
