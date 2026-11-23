from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from studio_factory import s13_eval
from studio_factory.art_contracts import DEFAULT_CONTRACT, compile_shot, load_contract


ROOT = Path(__file__).resolve().parents[2]


class S13EvalTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.repo = self.root / "repo"
        self.evidence = self.root / "evidence"
        registry = load_contract(ROOT)
        compiled = compile_shot(registry, "S13")
        self.contract = json.loads((ROOT / s13_eval.CONTRACT).read_text())
        for lock in registry["contract"]["source_locks"]:
            relative = lock["path"]
            self.write(self.repo / relative, (ROOT / relative).read_bytes())
        self.write(self.repo / DEFAULT_CONTRACT, (ROOT / DEFAULT_CONTRACT).read_bytes())
        self.checks = {
            check["id"]: check["polarity"]
            for shot in registry["contract"]["shots"] if shot["shot_id"] == "S13"
            for check in shot["checks"] if check["modality"] == "still"
        }
        old = "reflected wafer contour momentarily resembles notation."
        pivot = "The shot must be an independently plausible original physical scene."
        delta = {"old": old, "replacement": "one narrow arc", "pivot": pivot, "addition": "Method"}
        repair = compiled["prompt"].replace(old, delta["replacement"])
        prompts = {"A": "Control", "B": compiled["prompt"], "B3": repair, "ART": "Mechanism",
                   "C1": repair.replace(pivot, pivot + "\n" + delta["addition"])}
        takes = {}
        hashes = {}
        for take, label in s13_eval.TAKE_PROMPTS.items():
            original = f"originals/{take}.png"
            prompt = f"prompts/{label}.txt"
            takes[take] = {"original": original, "prompt": prompt, "inputs": []}
            hashes[original] = self.write(self.evidence / original, take.encode())
            hashes[prompt] = self.write(self.evidence / prompt, prompts[label].encode())
        takes["B3"]["inputs"] = ["B1", "B2"]
        takes["C1"]["inputs"] = ["B3", "ART"]
        self.run = {
            "shot": "S13", "project": compiled["project"], "sha256": hashes,
            "compiler_payload_sha256": compiled["payload_sha256"],
            "settings": {"provider": "Higgsfield web", "mode": "Unlimited"},
            "credits_before": 1, "credits_after": 1,
            "unlimited_counter_before": 0, "unlimited_counter_after": 7,
            "takes": takes, "prompt_delta": delta,
        }
        self.persist_manifest()

    @staticmethod
    def write(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return sha256(data).hexdigest()

    def persist_manifest(self):
        self.contract["run_sha256"] = self.write(
            self.evidence / "run.json", json.dumps(self.run).encode())
        self.write(self.repo / s13_eval.CONTRACT, json.dumps(self.contract).encode())

    def evaluate(self, attestations=None):
        return s13_eval.evaluate(self.repo, self.evidence, attestations)

    def approvals(self):
        def panel(take, criteria):
            item = self.run["takes"][take]
            media = self.run["sha256"][item["original"]]
            prompt = self.run["sha256"][item["prompt"]]
            return [{
                "kind": "human", "reviewer_id": identity, "media_sha256": media,
                "prompt_sha256": prompt,
                "observations": {
                    key: {"observed": value == "must_exist", "media_sha256": media,
                          "full_frame": True, "evidence_note": "synthetic contract test"}
                    for key, value in criteria.items()
                },
            } for identity in ("observer-a", "observer-b")]

        art = dict.fromkeys(self.contract["visible_criteria"]["artwork"], "must_exist")
        fusion = self.checks | dict.fromkeys(self.contract["visible_criteria"]["fusion"], "must_exist")
        return {
            "run_sha256": self.contract["run_sha256"], "producer_id": "producer",
            "artwork_sources": [
                {"reviewer_id": "rights-owner", "rights_evidence_ref": "fixture",
                 "source_url": url, "scope": "PRIVATE_REVIEW", "image": f"source-{number}.png",
                 "image_sha256": self.write(self.evidence / f"source-{number}.png",
                                            b"\x89PNG\r\n\x1a\n" + bytes([number]))}
                for number, url in enumerate(self.contract["artwork_source_urls"])
            ],
            "reviews": {"ART": panel("ART", art), "B3": panel("B3", self.checks),
                        "C1": panel("C1", fusion)},
            "owner_approval": {
                "owner_id": "owner", "decision": "APPROVE_STATIC_FREEZE", "take": "C1",
                "run_sha256": self.contract["run_sha256"],
                "media_sha256": self.run["sha256"]["originals/C1.png"],
                "prompt_sha256": self.run["sha256"]["prompts/C1.txt"],
            },
        }

    def test_mechanical_success_never_promotes_without_attestations(self):
        result = self.evaluate()
        self.assertEqual(result["state"], "DIAGNOSTIC_VERIFIED_FORMAL_HOLD")
        self.assertEqual(result["gates"]["E05"]["status"], "PASS")
        self.assertEqual(result["gates"]["E08"]["status"], "NOT_RUN")
        self.assertIsNone(result["frozen_take"])
        self.assertEqual(result["vision_judge"], {"mode": "TRIAGE_ONLY", "run": "NOT_RUN"})

    def test_unpinned_manifest_and_missing_bytes(self):
        manifest = self.evidence / "run.json"
        self.write(manifest, manifest.read_bytes() + b" ")
        self.assertEqual(self.evaluate()["gates"]["E01"]["status"], "FAIL")
        self.persist_manifest()
        (self.evidence / "originals/A1.png").unlink()
        self.assertEqual(self.evaluate()["gates"]["E05"]["status"], "INCONCLUSIVE")

    def test_changed_bytes_and_nonzero_cost(self):
        self.write(self.evidence / "originals/C1.png", b"changed")
        self.assertEqual(self.evaluate()["gates"]["E05"]["status"], "FAIL")
        self.run["credits_after"] = 0
        self.persist_manifest()
        self.assertEqual(self.evaluate()["gates"]["E04"]["status"], "FAIL")

    def test_mixed_control_and_unapproved_fusion_dependency(self):
        self.run["takes"]["A1"]["prompt"] = "prompts/B.txt"
        self.persist_manifest()
        self.assertEqual(self.evaluate()["gates"]["E03"]["status"], "FAIL")
        self.run["takes"]["A1"]["prompt"] = "prompts/A.txt"
        self.run["takes"]["C1"]["inputs"] = ["B3"]
        self.persist_manifest()
        self.assertEqual(self.evaluate()["gates"]["E08"]["status"], "FAIL")

    def test_current_artwork_bytes_and_rights_precede_human_review(self):
        attested = self.approvals()
        attested["artwork_sources"][0]["scope"] = "PUBLICATION"
        result = self.evaluate(attested)
        self.assertEqual(result["gates"]["E02"]["status"], "FAIL")
        self.assertEqual(result["gates"]["E06"]["status"], "NOT_RUN")

    def test_vision_and_same_reviewer_cannot_unlock_merge(self):
        attested = self.approvals()
        attested["reviews"]["ART"][0]["kind"] = "vision"
        result = self.evaluate(attested)
        self.assertEqual(result["gates"]["E06"]["status"], "FAIL")
        self.assertEqual(result["gates"]["E08"]["status"], "NOT_RUN")
        attested = self.approvals()
        attested["reviews"]["B3"][0]["reviewer_id"] = " observer-b "
        self.assertEqual(self.evaluate(attested)["gates"]["E07"]["status"], "FAIL")

    def test_hard_failure_and_mismatched_owner_digest_block_freeze(self):
        attested = self.approvals()
        attested["reviews"]["C1"][0]["observations"]["S13.OUTDOOR_BEACH_PIANO"]["observed"] = True
        result = self.evaluate(attested)
        self.assertEqual(result["gates"]["E08"]["status"], "FAIL")
        self.assertIsNone(result["frozen_take"])
        attested = self.approvals()
        attested["owner_approval"]["media_sha256"] = self.run["sha256"]["originals/B3.png"]
        self.assertEqual(self.evaluate(attested)["gates"]["E09"]["status"], "FAIL")

    def test_exact_approval_yields_static_freeze_only(self):
        approval = self.approvals()
        result = self.evaluate(deepcopy(approval))
        self.assertEqual(result["state"], "STATIC_FROZEN_RECIPE_PENDING")
        self.assertEqual(result["frozen_take"]["media_sha256"], self.run["sha256"]["originals/C1.png"])
        self.assertEqual(result["gates"]["E10"]["status"], "NOT_RUN")
        self.assertFalse(result["recipe_reusable"])
        self.assertFalse(result["approved_for_publication"])
        self.assertEqual(result["audio_temporal"], "NOT_RUN")
