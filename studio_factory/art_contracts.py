"""Fail-closed J4 art mechanism compiler and observation oracle.

A compiler for exact source-locked instructions, NOT a model client.
The oracle judges explicit review observations. It NEVER claims to interpret pixels
or to verify aesthetic effect without an independent human and actual media.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_CONTRACT = Path("projects/j4-async-succession/contracts/art_mechanism_v4_1.json")
SHOT_IDS = ("S02", "S04", "S06", "S11", "S13", "S14")
MODALITIES = frozenset(("still", "temporal", "cross_shot", "audio_temporal"))
POLARITIES = frozenset(("must_exist", "must_not_exist"))
HEX_SHA = re.compile(r"[0-9a-f]{64}\Z")


class ArtContractError(ValueError):
    pass


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _read(root: Path, relative: str) -> tuple[Path, bytes]:
    if relative.startswith("/") or "\\" in relative:
        raise ArtContractError("source path must be repository-relative")
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():
        raise ArtContractError(f"missing/unsafe source: {relative}")
    return p, p.read_bytes()


def _git_blob_sha1(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()


def load_contract(repo_root: Path, relative: Path = DEFAULT_CONTRACT) -> dict:
    root = repo_root.resolve()
    _, content = _read(root, str(relative))
    contract = json.loads(content)
    if contract.get("schema") != "j4.art-mechanism.v1":
        raise ArtContractError("unexpected contract schema")
    if contract.get("generation_gate") != "BLOCKED":
        raise ArtContractError("cannot relax generation gate in compiler")
    if contract.get("project") != "j4-async-succession":
        raise ArtContractError("project identity mismatch")
    if tuple(contract.get("scope", {}).get("shots", [])) != SHOT_IDS:
        raise ArtContractError("six-shot frozen pilot order changed")
    if len(contract.get("source_locks", [])) != 2:
        raise ArtContractError("expected exactly two historical source locks")
    source_data = {}
    for lock in contract["source_locks"]:
        path, raw = _read(root, lock["path"])
        digest = _git_blob_sha1(raw)
        if digest != lock["git_blob_sha1"]:
            raise ArtContractError(f"source lock changed: {lock['role']} {path} "
                                   f"expected {lock['git_blob_sha1']}, got {digest}")
        loaded = json.loads(raw)
        if lock.get("embedded_filename"):
            entries = [f for f in loaded.get("files", [])
                       if f.get("filename") == lock["embedded_filename"]]
            if len(entries) != 1:
                raise ArtContractError(f"embedded source missing/ambiguous: {lock['embedded_filename']}")
            loaded = json.loads(entries[0]["content"])
        source_data[lock["role"]] = loaded
    shots_source = source_data["canonical_shot_ir"]
    if len(shots_source.get("shots", [])) != 25 or shots_source.get("duration_ms") != 90000:
        raise ArtContractError("canonical 25-shot/90s lock broken")
    canonical = {s["id"]: s for s in shots_source["shots"]}
    optical = {s["shot_id"]: s for s in source_data["optical_art_reference"]["shots"]}
    profiles = contract.get("shots", [])
    if len(profiles) != len(SHOT_IDS) or tuple(s.get("shot_id") for s in profiles) != SHOT_IDS:
        raise ArtContractError("contract lost or duplicated a six-shot profile")
    all_ids = set()
    for s in profiles:
        sid = s["shot_id"]
        base = canonical[sid]
        art = optical[sid]
        if s["optical_method"] != art["illusion_id"]:
            raise ArtContractError(f"{sid}: v3.3 illusion reference mismatch")
        if not base["art_reference"]["do_not_copy"] or art["effect_status"] != "DESIGN_ONLY":
            raise ArtContractError(f"{sid}: source rights/status changed")
        for field in ("primary_action", "artistic_question", "scene_graph",
                      "camera", "time_logic", "negative_constraints", "checks", "references"):
            if not s.get(field):
                raise ArtContractError(f"{sid}: missing executable {field}")
        for check in s["checks"]:
            cid = check.get("id", "")
            if cid in all_ids or not cid.startswith(sid + "."):
                raise ArtContractError(f"duplicate/foreign check ID: {cid}")
            all_ids.add(cid)
            if (check.get("polarity") not in POLARITIES
                    or check.get("modality") not in MODALITIES
                    or check.get("severity") != "P0"
                    or not check.get("criterion")):
                raise ArtContractError(f"invalid check contract: {cid}")
        if not any(c["modality"] == "still" for c in s["checks"]):
            raise ArtContractError(f"{sid}: no keyframe acceptance")
        if not any(c["modality"] != "still" for c in s["checks"]):
            raise ArtContractError(f"{sid}: no time/cross-shot proof")
    return {"contract": contract, "canonical": canonical,
            "optical": optical, "contract_sha256": hashlib.sha256(content).hexdigest(),
            "checks_total": len(all_ids)}


def compile_shot(registry: dict, shot_id: str) -> dict:
    if shot_id not in SHOT_IDS:
        raise ArtContractError(f"shot outside G2 pilot: {shot_id}")
    p = next(x for x in registry["contract"]["shots"] if x["shot_id"] == shot_id)
    base = registry["canonical"][shot_id]
    optical = registry["optical"][shot_id]
    # Observe -> arrange -> prevent. Never give a model the art reference image or
    # the artist's name as shorthand for copying a recognisable installation.
    priority = "\n".join([
        f"J4 ORIGINAL FICTIONAL SCENE / SHOT {shot_id} / HIGH PRIORITY",
        "HIGHEST PRIORITY: obey the causal action, spatial arrangement and physical evidence below.",
        "PRIMARY ACTION: " + p["primary_action"],
        "PHYSICAL SCENE GRAPH:",
        *[f"  {i+1}. {node}" for i, node in enumerate(p["scene_graph"])],
        "CAMERA: " + p["camera"],
        "TIME / MECHANISM: " + p["time_logic"],
        "FORBIDDEN:",
        *[f"  - {x}" for x in p["negative_constraints"]],
        "The shot must be an independently plausible original physical scene.",
        "Styling or beauty cannot substitute for action, evidence, material physics or object identity.",
        "BASE SCENE GUIDANCE (lower priority than the specific G2 contract): " + base["image_prompt"],
        "GLOBAL VISUAL SAFETY: " + registry["canonical"]["S02"].get("global_negative_prompt_ref", "GLOBAL_NEGATIVE_V2_6")
    ])
    envelope = {
        "schema": "studio.art-prompt-compiled.v1",
        "project": registry["contract"]["project"],
        "shot_id": shot_id,
        "source_contract_sha256": registry["contract_sha256"],
        "canonical_source_git_blob": registry["contract"]["source_locks"][0]["git_blob_sha1"],
        "art_reference_git_blob": registry["contract"]["source_locks"][1]["git_blob_sha1"],
        "optical_mechanism_id": p["optical_method"],
        "exact_art_historical_source_url": optical["source_url"],
        "art_reference_policy": "METHOD_ONLY_DO_NOT_GENERATE_FROM_REFERENCE_IMAGE",
        "duration_ms": base["duration_ms"],
        "prompt": priority,
        "negative_constraints": p["negative_constraints"],
        "image_lock": registry["canonical"]["S02"].get("global_image_lock_ref", "MASTER_IMAGE_V2_6"),
        "required_check_ids": [c["id"] for c in p["checks"]],
        "evidence_oracle": "independent human observations + actual media SHA-256 + director signoff",
        "state": "COMPILED_NOT_SUBMITTED",
        "generation_gate": "BLOCKED",
        "provider_call": "NONE",
        "media_created": False
    }
    envelope["payload_sha256"] = _digest(envelope)
    return envelope


def judge_observations(registry: dict, candidate: dict) -> dict:
    """Judge reported facts, not pixels. Never returns APPROVED or PASS.

    An independent reviewer must observe actual media and provide evidence before
    READY_FOR_DIRECTOR_REVIEW. A negative observation is recorded as a reviewer
    rejection even when attachment digest was not yet supplied.
    """
    sid = candidate.get("shot_id")
    if sid not in SHOT_IDS:
        raise ArtContractError("candidate shot outside pilot")
    profile = next(s for s in registry["contract"]["shots"] if s["shot_id"] == sid)
    producer = str(candidate.get("producer", "")).strip()
    reviewer = str(candidate.get("reviewer", "")).strip()
    if not producer or not reviewer or producer == reviewer:
        return {"shot_id": sid, "state": "BLOCKED", "reason": "independent producer/reviewer identity missing or equal",
                "failures": [], "unverified": [c["id"] for c in profile["checks"]]}
    media_type = candidate.get("media_type")
    if media_type not in ("still", "video"):
        raise ArtContractError("media_type must be still or video")
    observations = candidate.get("observations", {})
    if not isinstance(observations, dict):
        raise ArtContractError("observations must be object keyed by exact check IDs")
    checks = {c["id"]: c for c in profile["checks"]}
    if set(observations) - set(checks):
        raise ArtContractError("unknown check ID(s): " + ",".join(sorted(set(observations)-set(checks))))
    failures, pending, supported = [], [], []
    for c in profile["checks"]:
        cid = c["id"]
        observation = observations.get(cid)
        if not isinstance(observation, dict) or type(observation.get("observed")) is not bool:
            pending.append({"check_id": cid, "reason": "no boolean independent observation"})
            continue
        if media_type == "still" and c["modality"] != "still":
            pending.append({"check_id": cid, "reason": "requires video/audio or cross-shot evidence, not a still"})
            continue
        should_exist = c["polarity"] == "must_exist"
        meets = observation["observed"] == should_exist
        record = {"check_id": cid, "criterion": c["criterion"],
                  "observation": observation["observed"],
                  "evidence": observation.get("evidence_uri", ""),
                  "reviewer": reviewer}
        if meets:
            supported.append(record)
            if not observation.get("evidence_uri"):
                pending.append({"check_id":cid, "reason":"positive statement lacks evidence pointer"})
        else:
            failures.append(record)
    media_path = candidate.get("media_path")
    media_digest = candidate.get("media_sha256")
    media_verified = False
    if media_path:
        path = Path(media_path)
        if not path.is_file():
            pending.append({"check_id": "MEDIA", "reason": "media path missing"})
        elif not isinstance(media_digest, str) or not HEX_SHA.fullmatch(media_digest):
            pending.append({"check_id": "MEDIA", "reason": "valid media SHA-256 required"})
        else:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != media_digest:
                failures.append({"check_id": "MEDIA", "criterion": "media hash match",
                                 "observation": False, "actual": actual})
            else:
                media_verified = True
    else:
        pending.append({"check_id": "MEDIA", "reason": "no media bytes available for verification"})
    if failures:
        state = "REJECTED_BY_OBSERVATION"
    elif pending or not media_verified:
        state = "BLOCKED_INCOMPLETE_EVIDENCE"
    else:
        state = "READY_FOR_DIRECTOR_REVIEW"  # not an artistic PASS
    return {
        "schema":"studio.art-qc-review.v1",
        "shot_id":sid,"candidate_id":candidate.get("candidate_id", "unnamed"),
        "contract_sha256":registry["contract_sha256"],
        "state":state,"media_sha256_verified":media_verified,
        "reviewer_identity_attested_not_authenticated":reviewer,
        "source_of_observations":"human_report_only_no_automatic_pixel_semantics",
        "failures":failures,"unverified":pending,"supported":supported,
        "rights_gate":"NOT_RUN","director_gate":"NOT_RUN",
        "paid_generation_gate":"BLOCKED",
    }


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m studio_factory.art_contracts")
    p.add_argument("--repo",type=Path,default=Path.cwd())
    sub = p.add_subparsers(dest="action",required=True)
    sub.add_parser("validate")
    c = sub.add_parser("compile");c.add_argument("shot",choices=SHOT_IDS);c.add_argument("--output",type=Path)
    j = sub.add_parser("judge");j.add_argument("candidate",type=Path);j.add_argument("--output",type=Path)
    args = p.parse_args(argv)
    try:
        registry = load_contract(args.repo)
        if args.action == "validate":
            result={"result":"CONTRACT_VALID", "profiles":len(SHOT_IDS),
                    "checks":registry["checks_total"],
                    "generation_gate":"BLOCKED","contract_sha256":registry["contract_sha256"]}
        elif args.action == "compile":
            result=compile_shot(registry,args.shot)
        else:
            result=judge_observations(registry,json.loads(args.candidate.read_text(encoding="utf-8")))
        printed=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
        output=getattr(args,"output",None)
        if output:
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_text(printed,encoding="utf-8")
        print(printed,end="")
        if args.action=="judge" and result["state"]!="READY_FOR_DIRECTOR_REVIEW":
            return 2
        return 0
    except (ArtContractError,ValueError,KeyError,FileNotFoundError) as e:
        p.exit(2,f"BLOCKED: {e}\n")


if __name__=="__main__":
    raise SystemExit(main())
