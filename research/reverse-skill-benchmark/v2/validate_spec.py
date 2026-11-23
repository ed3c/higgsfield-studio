#!/usr/bin/env python3
"""Zero-dependency schema coherence validator; does NOT certify a completed benchmark."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
m = json.loads((root / "manifest_v2.json").read_text(encoding="utf-8"))
assert m["schema_version"] == "2.0"
assert len(m["reference_cases"]) == 3
assert m["cost_policy"]["max_additional_higgsfield_credits"] == 0
assert sum(p["expected_images"] for p in m["phases"]) == 30
assert all(p["expected_images"] == p["cases"] * len(p["candidates"]) * p["replicates"] for p in m["phases"])
assert m["reviewers_per_image"] == 2
assert all(abs(sum(w.values()) - 1.0) < 1e-9 for w in m["scoring"].values() if isinstance(w, dict))
assert m["execution_surface"].startswith("higgsfield.ai website")
assert m["results"]["actual_images"] == sum(p["completed_images"] for p in m["phases"])
assert m["results"]["actual_images"] <= m["expected_core_images"]
if m["results"]["actual_images"] == 0:
    assert m["results"]["P1_winner"] is None and m["results"]["P2_winner_among_compared"] is None
    assert m["state"] != "COMPLETE"
print("SPEC LINT PASS: matrix, score weights, zero-credit gate and NOT_RUN semantics coherent.")
print("EXECUTION STATUS:", m["state"], "— no images or scores produced by this spec pack.")
