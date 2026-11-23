"""Replay the captured J4 S13 diagnostic run without authorizing production."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from .art_contracts import ArtContractError, compile_shot, load_contract
from .evidence_gate import EvidenceGateError, _magic_matches, _observation, _resolve_asset, file_sha256


CONTRACT = Path("projects/j4-async-succession/contracts/s13_eval_v1.json")
AB = ("A1", "B1", "A2", "B2")
TAKE_PROMPTS = {
    "A1": "A", "B1": "B", "A2": "A", "B2": "B",
    "B3": "B3", "ART": "ART", "C1": "C1",
}


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition, reason):
    if not condition:
        raise EvidenceGateError(reason)


def _fingerprinted_files(root, run):
    files = {
        path: _resolve_asset(root, path)
        for take in run["takes"].values()
        for path in (take["prompt"], take["original"])
    }
    _require(files.keys() == run["sha256"].keys(), "incomplete run file inventory")
    prompts = {}
    for relative, path in files.items():
        if relative.startswith("prompts/"):
            content = path.read_bytes()
            digest = sha256(content).hexdigest()
            prompts[relative] = content.decode("utf-8")
        else:
            digest = file_sha256(path)
        _require(digest == run["sha256"][relative], f"SHA-256 mismatch: {relative}")
    return prompts


def _gate(status, reason):
    return {"status": status, "reason": reason}


def _review_panel(take, criteria, run, attestations):
    panels = attestations.get("reviews", {})
    if not isinstance(panels, dict):
        return _gate("FAIL", "Review panels must be keyed by exact take")
    panel = panels.get(take, [])
    if not panel:
        return _gate("NOT_RUN", "Two independent human reviews are pending")
    if not isinstance(panel, list) or len(panel) != 2:
        return _gate("INCONCLUSIVE", "Exactly two reviews are required")
    producer = attestations.get("producer_id")
    if any(not isinstance(review, dict) for review in panel):
        return _gate("FAIL", "Malformed review")
    reviewer_ids = [review.get("reviewer_id") for review in panel]
    if (not isinstance(producer, str) or not producer.strip() or
            any(not isinstance(value, str) or not value.strip() for value in reviewer_ids) or
            len({value.strip().casefold() for value in reviewer_ids + [producer]}) != 3):
        return _gate("FAIL", "Human reviewers must be distinct from one another and the producer")

    item = run["takes"][take]
    media_sha = run["sha256"][item["original"]]
    prompt_sha = run["sha256"][item["prompt"]]
    outcomes = []
    for reviewer, review in zip(reviewer_ids, panel, strict=True):
        if (review.get("kind"), review.get("media_sha256"), review.get("prompt_sha256")) != (
            "human", media_sha, prompt_sha
        ):
            return _gate("FAIL", "Review is not human attestation for the exact image and prompt")
        observations = review.get("observations")
        if not isinstance(observations, dict) or not observations.keys() <= criteria.keys():
            return _gate("FAIL", "Invalid or non-static observation")
        for check_id, polarity in criteria.items():
            status, reason = _observation(review, check_id, media_sha, "still", reviewer, polarity)
            if status in {"INVALID", "MISSING"}:
                return _gate("INCONCLUSIVE" if status == "MISSING" else "FAIL", reason)
            outcomes.append(status)
    if "FAIL_OBSERVED" in outcomes:
        return _gate("FAIL", "At least one reviewer reported a hard failure; hold for adjudication")
    return _gate("PASS", "Both independent human attestations cover the exact static criteria")


def _apply_attestations(result, root, contract, run, shot_checks, attestations):
    gates = result["gates"]
    if not isinstance(attestations, dict) or attestations.get("run_sha256") != contract["run_sha256"]:
        gates["E02"] = _gate("FAIL", "Attestations belong to a different run manifest")
        return

    sources = attestations.get("artwork_sources")
    if not sources:
        return
    try:
        _require(isinstance(sources, list) and len(sources) == len(contract["artwork_source_urls"]),
                 "Every artwork in the pinned source register needs direct image evidence")
        _require({item["source_url"] for item in sources} == set(contract["artwork_source_urls"]),
                 "Artwork sources differ from the pinned source register")
        for rights in sources:
            _require(rights["reviewer_id"].strip() and rights["rights_evidence_ref"].strip(),
                     "Artwork provenance and rights attestation are required")
            _require(rights["scope"] == "PRIVATE_REVIEW", "Private-review rights scope is required")
            artwork_image = _resolve_asset(root, rights["image"])
            _require(_magic_matches(artwork_image, "still"), "Direct artwork evidence must be an image")
            _require(file_sha256(artwork_image) == rights["image_sha256"],
                     "Direct artwork image bytes differ from the rights attestation")
    except (EvidenceGateError, KeyError, TypeError, AttributeError, OSError) as exc:
        gates["E02"] = _gate("FAIL", str(exc))
        return
    gates["E02"] = _gate("PASS", "Direct artwork bytes and private-review rights attestations recorded")
    art_checks = dict.fromkeys(contract["visible_criteria"]["artwork"], "must_exist")
    fusion_checks = shot_checks | dict.fromkeys(contract["visible_criteria"]["fusion"], "must_exist")
    gates["E06"] = _review_panel("ART", art_checks, run, attestations)
    gates["E07"] = _review_panel("B3", shot_checks, run, attestations)
    if {gates["E06"]["status"], gates["E07"]["status"]} != {"PASS"}:
        return
    gates["E08"] = _review_panel("C1", fusion_checks, run, attestations)
    if gates["E08"]["status"] != "PASS":
        return

    approval = attestations.get("owner_approval")
    if not approval:
        return
    freeze = {
        "take": "C1",
        "run_sha256": contract["run_sha256"],
        "media_sha256": run["sha256"]["originals/C1.png"],
        "prompt_sha256": run["sha256"]["prompts/C1.txt"],
    }
    owner = approval.get("owner_id") if isinstance(approval, dict) else None
    if (not isinstance(owner, str) or not owner.strip() or
            owner.strip().casefold() == attestations["producer_id"].strip().casefold() or
            approval.get("decision") != "APPROVE_STATIC_FREEZE" or
            any(approval.get(key) != value for key, value in freeze.items())):
        gates["E09"] = _gate("FAIL", "Owner approval failed to bind to the exact static candidate")
        return
    freeze["attestations_sha256"] = sha256(
        json.dumps(attestations, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    result["frozen_take"] = freeze
    result["state"] = "STATIC_FROZEN_RECIPE_PENDING"
    gates["E09"] = _gate("PASS", "Owner attested to the specific static candidate")


def evaluate(repo, evidence, attestations=None):
    """Return mechanical replay and explicit gaps for the human oracles."""
    gates = {
        "E01": _gate("NOT_RUN", "Pinned source and exact compiler output"),
        "E02": _gate("NOT_RUN", "Direct artwork image and rights attestation"),
        "E03": _gate("NOT_RUN", "Historical A/B reconciliation"),
        "E04": _gate("NOT_RUN", "Official website cost readback"),
        "E05": _gate("NOT_RUN", "Original media and sent prompt integrity"),
        "E06": _gate("NOT_RUN", "Independent artwork-only QC"),
        "E07": _gate("NOT_RUN", "Independent shot-only QC"),
        "E08": _gate("NOT_RUN", "Fusion lineage and independent fusion QC"),
        "E09": _gate("NOT_RUN", "Human approval and frozen take"),
        "E10": _gate("NOT_RUN", "Second independent success and recipe regression"),
        "E11": _gate("PASS", "Vision output is triage only; evaluator cannot promote from it"),
    }
    result = {
        "schema": "studio.s13-eval-report.v1",
        "shot": "S13",
        "state": "BLOCKED",
        "gates": gates,
        "vision_judge": {"mode": "TRIAGE_ONLY", "run": "NOT_RUN"},
        "formal_g2": "NOT_RUN",
        "audio_temporal": "NOT_RUN",
        "frozen_take": None,
        "recipe_reusable": False,
        "approved_for_generation": False,
        "approved_for_publication": False,
    }
    active = "E01"
    try:
        contract = _read_json(repo / CONTRACT)
        manifest = _resolve_asset(evidence, "run.json")
        manifest_bytes = manifest.read_bytes()
        _require(sha256(manifest_bytes).hexdigest() == contract["run_sha256"], "unpinned run manifest")
        run = json.loads(manifest_bytes)
        registry = load_contract(repo)
        compiled = compile_shot(registry, "S13")
        _require((run["project"], run["shot"]) == (compiled["project"], compiled["shot_id"]),
                 "run belongs to another project or shot")
        _require(run["compiler_payload_sha256"] == compiled["payload_sha256"],
                 "compiler source revision changed")
        gates[active] = _gate("PASS", "Pinned run manifest and S13 compiler payload match")

        active = "E03"
        takes = run["takes"]
        _require(takes.keys() == TAKE_PROMPTS.keys(), "missing or unexpected S13 take")
        _require(all(takes[t]["original"] == f"originals/{t}.png"
                     and takes[t]["prompt"] == f"prompts/{prompt}.txt"
                     for t, prompt in TAKE_PROMPTS.items()), "take has wrong role or evidence file")
        _require(len({run["sha256"][takes[t]["original"]] for t in AB}) == len(AB),
                 "A/B repeats share identical media")
        gates[active] = _gate("PASS",
            "Matched four controlled diagnostic takes; original six-panel cause remains UNKNOWN")

        active = "E04"
        settings = run["settings"]
        _require((settings["provider"], settings["mode"]) == ("Higgsfield web", "Unlimited"),
                 "missing official website Unlimited evidence")
        _require(run["credits_before"] == run["credits_after"], "nonzero credit delta")
        _require(run["unlimited_counter_after"] - run["unlimited_counter_before"] == len(takes),
                 "Unlimited counter does not reconcile to take count")
        gates[active] = _gate("PASS", "Historical batch readback reconciles seven takes and zero credits")
        result["live_generation_preflight"] = "NOT_RUN"

        active = "E05"
        prompts = _fingerprinted_files(evidence, run)
        _require(prompts["prompts/B.txt"] == compiled["prompt"],
                 "B sent text differs from the pinned compiler")
        gates[active] = _gate("PASS", "Seven original files and five exact prompt texts match their hashes")

        active = "E08"
        delta = run["prompt_delta"]
        baseline = compiled["prompt"]
        repair = prompts["prompts/B3.txt"]
        _require(baseline.count(delta["old"]) == 1 and
                 baseline.replace(delta["old"], delta["replacement"]) == repair,
                 "B3 is not one localized change to B")
        _require(takes["B3"]["inputs"] == ["B1", "B2"] and
                 takes["ART"]["inputs"] == [] and takes["C1"]["inputs"] == ["B3", "ART"],
                 "invalid repair, independent artwork, or fusion lineage")
        _require(repair.count(delta["pivot"]) == 1 and
                 repair.replace(delta["pivot"], delta["pivot"] + "\n" + delta["addition"]) ==
                 prompts["prompts/C1.txt"],
                 "C1 adds more than the recorded artwork method")
        gates[active] = _gate("NOT_RUN", "Fusion prompt lineage PASS; independent fusion QC pending")
        profile = next(shot for shot in registry["contract"]["shots"] if shot["shot_id"] == "S13")
        shot_checks = {
            check["id"]: check["polarity"] for check in profile["checks"] if check["modality"] == "still"
        }
        _require(list(shot_checks) == contract["visible_criteria"]["shot"],
                 "S13 static criteria differ from the versioned review contract")
        result["diagnostic_replay"] = "PASS"
        result["state"] = "DIAGNOSTIC_VERIFIED_FORMAL_HOLD"
        result["review_criteria"] = {
            "ART": contract["visible_criteria"]["artwork"],
            "B3": shot_checks,
            "C1_additional": contract["visible_criteria"]["fusion"],
        }
    except (ArtContractError, EvidenceGateError, OSError, ValueError, KeyError, TypeError) as exc:
        status = "INCONCLUSIVE" if isinstance(exc, OSError) or str(exc).startswith("missing media file:") else "FAIL"
        gates[active] = _gate(status, str(exc))
        result["diagnostic_replay"] = status
        return result
    if attestations is not None:
        _apply_attestations(result, evidence, contract, run, shot_checks, attestations)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--evidence", type=Path, required=True, help="Extracted private S13 evidence")
    parser.add_argument("--attestations", type=Path, help="Private owner and independent human records")
    args = parser.parse_args(argv)
    try:
        attestations = _read_json(args.attestations) if args.attestations else None
    except (OSError, ValueError) as exc:
        parser.error(f"cannot read private attestations: {exc}")
    result = evaluate(args.repo, args.evidence, attestations)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["diagnostic_replay"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
