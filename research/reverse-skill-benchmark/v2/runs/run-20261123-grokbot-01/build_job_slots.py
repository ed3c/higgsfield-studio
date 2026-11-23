#!/usr/bin/env python3
"""Emit the 30 v2 job slots (18 P1 + 12 P2) exactly as manifest_v2.json defines the matrix.
Prompts are NOT invented: every slot stays prompt=null until P0 prompt lock produces raw/normalized
prompts from the pinned Skills. Writes job_slots.json next to this file, and (if given) a copy elsewhere."""
import json, random, sys, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2 = HERE.parents[1]
m = json.loads((V2 / "manifest_v2.json").read_text(encoding="utf-8"))
pins = {s["id"]: s["head_sha"] for s in json.loads((HERE / "skill_pins.json").read_text())["skills"]}
RUN = "run-20261123-grokbot-01"
SEED = 20261123  # recorded so the within-case submission order is reproducible
rng = random.Random(SEED)
pm = m["primary_model"]
common = {
    "surface": "higgsfield.ai website, ordinary image generation page (NOT MCP/CLI/API/Canvas/Marketing Studio/Supercomputer/Presets)",
    "model_display_name": "GPT Image 2.6 (not Flare); PR #5 observed UI variant 'GPT Image 2.6 Sunburst' — record exact variant at submit",
    "model_locked": False,
    "aspect_ratio": pm["aspect_ratio"], "resolution": pm["resolution"],
    "quality": "Medium (PR #5 observation) or whatever live 0-credit tier the site shows; must be identical for all 30",
    "output_format": "PNG", "images_per_submit": 1,
    "unlimited_toggle_required": True, "required_cost_indicator": "Unlimited / 0 Credits on the fully populated form",
    "reference_image_upload": "FORBIDDEN (spec §1/§5: no image-to-image; source stills go only to the reverse Skill, never to Higgsfield)",
    "media_upload_agreement_dialog_expected": False,
    "stop_if": ["toggle off or missing", "any numeric credit price shown", "Media upload agreement / credits dialog", "balance changes after render"],
    "submit_serially": True,
}
jobs, order = [], 0
def case_ids(): return [c["id"] for c in m["reference_cases"]]
for ph in m["phases"]:
    for case in case_ids():
        cands = list(ph["candidates"])
        reps = [(s, r) for s in cands for r in range(1, ph["replicates"] + 1)]
        rng.shuffle(reps)
        for s, r in reps:
            order += 1
            known = s in pins
            jid = f"{ph['id']}-{case}-{s if known else 'B'}-r{r}"
            jobs.append({
                **common, "job_id": jid, "run_id": RUN, "phase": ph["id"], "task": ph["task"],
                "case_id": case, "case_class": next(c["class"] for c in m["reference_cases"] if c["id"] == case),
                "skill_id": s, "skill_commit": pins.get(s), "replicate": r, "submit_order": order,
                "prompt": None, "prompt_sha256": None,
                "prompt_source_path": f"research/reverse-skill-benchmark/v2/prompts/{ph['task']}/{case}/{s}/normalized_prompt.txt" if known else None,
                "p2_replacement_subject": None if ph["id"] == "P1" else f"p2_subjects_PROPOSED.json#cases.{case} (NOT LOCKED)",
                "reverse_skill_input_reference": f"artifacts/reverse-benchmark-v2/{RUN}/refs/{case}.png (MISSING_SOURCE MS-004)",
                "expected_output_filename": f"artifacts/reverse-benchmark-v2/{RUN}/output/{jid}.png",
                "blind_image_id": "assigned privately at eval time (B0001..B0030); mapping sealed",
                "status": "BLOCKED_SOURCE" if ph["id"] == "P1" else "BLOCKED_ON_P1_SCORES",
                "blocked_by": ["MS-004 no C01-C03 stills", "P0 prompt lock NOT_RUN", "G1 live recheck NOT_RUN"] + ([] if ph["id"] == "P1" else ["P1 blind scores", "candidate B undecided", "MS-008 subjects not locked"]),
            })
assert sum(j["phase"] == "P1" for j in jobs) == 18 and sum(j["phase"] == "P2" for j in jobs) == 12
assert all(j["prompt"] is None for j in jobs)
out = {"run_id": RUN, "generated_from": {"manifest_v2.json_sha256": hashlib.sha256((V2 / "manifest_v2.json").read_bytes()).hexdigest(), "shuffle_seed": SEED},
       "counts": {"P1": 18, "P2": 12, "total": 30, "ready_to_submit": 0}, "jobs": jobs}
txt = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
(HERE / "job_slots.json").write_text(txt, encoding="utf-8")
for extra in sys.argv[1:]:
    Path(extra).parent.mkdir(parents=True, exist_ok=True); Path(extra).write_text(txt, encoding="utf-8")
print("30 slots written; ready_to_submit=0")
