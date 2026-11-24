"""Headless S13 chat-to-Higgsfield production bridge.

No network, generation, upload, credit spending or inferred image understanding.
The chat operator performs external calls; this module checks their evidence.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from .art_contracts import compile_shot, load_contract
from .evidence_gate import EvidenceGateError, _magic_matches, _resolve_asset, file_sha256


SPEC = Path("projects/j4-async-succession/contracts/s13_chat_loop_v1.json")
STAGES = ("artwork", "shot", "fusion")
STATE = ("NOT_RUN", "EVIDENCE_INCOMPLETE", "QC_FAIL", "QC_PASS")


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise EvidenceGateError(message)


def compile_plan(repo: Path, catalog_model: dict) -> dict:
    """Compile S13 against existing pinned G2 compiler, never authorize rendering."""
    contract = load_contract(repo)
    shot = compile_shot(contract, "S13")
    spec = json.loads((repo / SPEC).read_text(encoding="utf-8"))
    require(spec.get("schema") == "studio.s13-chat-loop-spec.v1", "unsupported S13 chat spec")
    require(spec.get("shot_id") == "S13", "cross-shot spec")
    require(catalog_model.get("output_type") == "image", "model is not an image generator")
    require("9:16" in catalog_model.get("aspect_ratios", []), "model cannot render S13 9:16")
    model_id = catalog_model.get("id")
    require(isinstance(model_id, str) and model_id, "model id missing")
    artwork = spec["artwork_prompt"].strip()
    require(len(artwork) >= 80 and spec.get("artwork_source_urls"), "artwork method/source missing")
    prompts = {
        "artwork": artwork,
        "shot": shot["prompt"],
        "fusion": (
            "J4 S13 ORIGINAL COMPOSITION. The artwork material mechanism and the "
            "narrative shot must BOTH be legible in one physically plausible image. "
            "Do not copy the referenced artwork or reproduce an installation.\n"
            "ARTWORK METHOD (material and altered function, not a copied form):\n"
            + artwork + "\nSHOT CAUSAL CONTRACT (higher priority for objects and place):\n"
            + shot["prompt"]
        ),
    }
    branches = {
        name: {
            "prompt": prompt,
            "prompt_sha256": sha256(prompt.encode("utf-8")).hexdigest(),
            "depends_on": [] if name != "fusion" else ["artwork", "shot"],
            "state": "NOT_RUN",
            "result": None,
            "reviews": [],
        }
        for name, prompt in prompts.items()
    }
    plan = {
        "schema": "studio.s13-chat-loop.v1",
        "project": "j4-async-succession",
        "shot_id": "S13",
        "source_contract_sha256": contract["contract_sha256"],
        "compiled_shot_payload_sha256": shot["payload_sha256"],
        "artwork_sources": spec["artwork_source_urls"],
        "model": {"id": model_id, "aspect_ratio": "9:16",
                  "capability_sha256": digest(catalog_model)},
        "surface_policy": "HIGGSFIELD_CHAT_ZERO_CREDITS_ONLY",
        "submissions_authorized": False,
        "branches": branches,
        "repairs": {},
        "owner_approval": None,
        "golden": False,
        "recipe_reusable": False,
    }
    plan["plan_sha256"] = digest({k: v for k, v in plan.items() if k != "plan_sha256"})
    return plan


def _criteria(repo: Path, manifest: dict, stage: str):
    require(stage in STAGES, "unknown stage")
    registry = load_contract(repo)
    p = next(x for x in registry["contract"]["shots"] if x["shot_id"] == "S13")
    shot = {c["id"]: c["polarity"] for c in p["checks"] if c["modality"] == "still"}
    spec = json.loads((repo / SPEC).read_text(encoding="utf-8"))
    artwork = {item: "must_exist" for item in spec["artwork_checks"]}
    fusion = {item: "must_exist" for item in spec["fusion_checks"]}
    return artwork if stage == "artwork" else shot if stage == "shot" else (shot | fusion)


def quote_allows_zero_credits(quote: dict, *, model_id: str, surface: str) -> bool:
    """A capability flag or a website screenshot is never a live chat entitlement."""
    if surface != "higgsfield_chat" or quote.get("error") or quote.get("unlim_choice"):
        return False
    cost = quote.get("cost")
    return (quote.get("model") == model_id and
            isinstance(cost, dict) and type(cost.get("credits")) in (int, float) and
            cost["credits"] == 0 and
            quote.get("unlimited_applied") is True and
            isinstance(quote.get("quote_ref"), str) and bool(quote["quote_ref"]))


def record_image(repo: Path, plan: dict, stage: str, evidence: dict, media_root: Path) -> dict:
    """Bind a completed real output to exact sent text and fresh zero-credit evidence.

    This returns a new manifest; the previous one remains immutable.
    """
    require(stage in STAGES, "unknown stage")
    result = deepcopy(plan)
    node = result["branches"][stage]
    require(node["state"] == "NOT_RUN", "branch cannot be overwritten")
    if stage == "fusion":
        require(all(result["branches"][p]["state"] == "QC_PASS"
                    for p in node["depends_on"]), "fusion requires both parent QC PASS")
    require(evidence.get("surface") == "higgsfield_chat", "wrong generation surface")
    require(quote_allows_zero_credits(evidence.get("quote", {}),
                                     model_id=result["model"]["id"],
                                     surface=evidence.get("surface", "")), "zero-credit proof missing")
    require(evidence.get("status") == "completed", "not a completed job")
    require(evidence.get("sent_prompt") == node["prompt"], "sent prompt drift")
    require(evidence.get("aspect_ratio") == "9:16", "aspect ratio drift")
    require(evidence.get("model") == result["model"]["id"], "model drift")
    require(isinstance(evidence.get("job_id"), str) and evidence["job_id"], "job ID missing")
    require(evidence.get("charged_credits") == 0 and
            type(evidence.get("charged_credits")) in (int, float), "credit delta unknown/nonzero")
    relative = evidence.get("media_path")
    file = _resolve_asset(media_root, relative)
    require(_magic_matches(file, "still"), "invalid still media signature")
    actual_sha = file_sha256(file)
    require(actual_sha == evidence.get("media_sha256"), "output image bytes/hash mismatch")
    node["result"] = {
        "job_id": evidence["job_id"], "media_path": relative, "media_sha256": actual_sha,
        "sent_prompt_sha256": node["prompt_sha256"],
        "quote_ref": evidence["quote"]["quote_ref"], "charged_credits": 0,
        "surface": evidence["surface"], "state": "EVIDENCE_BOUND_NOT_QC",
    }
    node["state"] = "EVIDENCE_INCOMPLETE"
    return result


def evaluate_human_qc(repo: Path, plan: dict, stage: str,
                      reviews: list[dict], producer_id: str) -> dict:
    """Human attestations are checked mechanically, not authenticated or inferred."""
    require(stage in STAGES, "unknown stage")
    result = deepcopy(plan)
    node = result["branches"][stage]
    require(node["state"] == "EVIDENCE_INCOMPLETE", "no unreviewed image evidence")
    require(isinstance(producer_id, str) and producer_id.strip(), "producer missing")
    require(isinstance(reviews, list) and len(reviews) == 2, "two independent reviews required")
    ids = [r.get("reviewer_id") if isinstance(r, dict) else None for r in reviews]
    require(all(isinstance(x, str) and x.strip() for x in ids) and
            len({x.strip().casefold() for x in ids + [producer_id]}) == 3,
            "reviewers must be distinct from producer")
    expected = _criteria(repo, result, stage)
    media_sha = node["result"]["media_sha256"]
    prompt_sha = node["prompt_sha256"]
    failed = []
    for review in reviews:
        require(review.get("kind") == "human" and
                review.get("media_sha256") == media_sha and
                review.get("prompt_sha256") == prompt_sha, "wrong reviewer binding")
        obs = review.get("observations")
        require(isinstance(obs, dict) and set(obs) == set(expected), "P0 checklist incomplete")
        for key, polarity in expected.items():
            value = obs[key]
            require(isinstance(value, dict) and type(value.get("observed")) is bool and
                    value.get("media_sha256") == media_sha and
                    isinstance(value.get("evidence_note"), str) and
                    value["evidence_note"].strip() and
                    (value.get("full_frame") is True or
                     (isinstance(value.get("roi_norm"), list) and
                      len(value["roi_norm"]) == 4 and
                      all(type(x) in (int, float) and 0 <= x <= 1
                          for x in value["roi_norm"]))),
                    "invalid observation evidence: " + key)
            if value["observed"] != (polarity == "must_exist"):
                failed.append(key)
    node["reviews"] = deepcopy(reviews)
    node["state"] = "QC_FAIL" if failed else "QC_PASS"
    node["failure_ids"] = sorted(set(failed))
    return result


def dry_run_shot_change(plan: dict, changed_shot_prompt: str) -> dict:
    """Q15 fault injection. Does not mutate versions, call model, or spend credits."""
    require(isinstance(changed_shot_prompt, str) and changed_shot_prompt.strip(), "empty shot delta")
    old = plan["branches"]["shot"]["prompt_sha256"]
    new = sha256(changed_shot_prompt.encode()).hexdigest()
    changed = old != new
    return {
        "mode": "DRY_RUN",
        "changed": changed,
        "invalidated": ["shot", "fusion"] if changed else [],
        "reused": ["artwork"],
        "old_shot_sha256": old,
        "new_shot_sha256": new,
        "provider_calls": 0,
    }


def propose_repair(plan: dict, stage: str, root_cause_id: str, evidence_ref: str) -> dict:
    """One causal correction per exact root cause; no hidden retry or new prompt."""
    require(stage in STAGES, "unknown stage")
    require(plan["branches"][stage]["state"] == "QC_FAIL", "repair requires QC failure")
    require(isinstance(root_cause_id, str) and root_cause_id.strip() and
            isinstance(evidence_ref, str) and evidence_ref.strip(), "causal evidence missing")
    result = deepcopy(plan)
    key = stage + ":" + root_cause_id
    require(key not in result["repairs"], "root cause already repaired once: stop")
    result["repairs"][key] = {"attempts": 1, "evidence_ref": evidence_ref,
                              "state": "PROPOSED_NOT_EXECUTED"}
    return result


def approve_golden(plan: dict, owner_id: str) -> dict:
    require(all(plan["branches"][stage]["state"] == "QC_PASS" for stage in STAGES),
            "cannot publish without three independent QC PASS branches")
    require(isinstance(owner_id, str) and owner_id.strip(), "owner approval missing")
    result = deepcopy(plan)
    result["owner_approval"] = {"owner_id": owner_id,
                                 "fusion_media_sha256": result["branches"]["fusion"]["result"]["media_sha256"]}
    result["golden"] = True
    result["recipe_reusable"] = False  # A second independent verified success is required.
    return result
