"""Mechanical negative/positive controls; all receipts and PNGs here are synthetic."""
import base64
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest

from studio_factory import chat_loop

REPO = Path(__file__).resolve().parents[2]
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg=="
)


class ChatLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.assets = Path(self.temp.name)
        self.catalog = {"id": "gpt_image_2_6", "output_type": "image",
                        "aspect_ratios": ["1:1", "9:16"], "supports_unlim": True}
        self.plan = chat_loop.compile_plan(REPO, self.catalog)

    def receipt(self, stage, *, cost=0, quote=True):
        item = self.plan["branches"][stage]
        image = self.assets / (stage + ".png")
        image.write_bytes(PNG + stage.encode())
        return {
            "surface": "higgsfield_chat",
            "quote": {"model": "gpt_image_2_6", "cost": {"credits": cost},
                      "unlimited_applied": quote, "quote_ref": "quote:" + stage},
            "status": "completed", "job_id": "synthetic-job-" + stage,
            "sent_prompt": item["prompt"], "aspect_ratio": "9:16",
            "model": "gpt_image_2_6", "charged_credits": cost,
            "media_path": stage + ".png",
            "media_sha256": sha256(image.read_bytes()).hexdigest(),
        }

    def humans(self, plan, stage, *, beach=False):
        node = plan["branches"][stage]
        expected = chat_loop._criteria(REPO, plan, stage)
        return [
            {
                "kind": "human", "reviewer_id": who,
                "media_sha256": node["result"]["media_sha256"],
                "prompt_sha256": node["prompt_sha256"],
                "observations": {
                    key: {
                        "observed": beach if key == "S13.OUTDOOR_BEACH_PIANO"
                                    else polarity == "must_exist",
                        "media_sha256": node["result"]["media_sha256"],
                        "full_frame": True,
                        "evidence_note": "synthetic test case; not an actual visual observation"
                    }
                    for key, polarity in expected.items()
                }
            }
            for who in ("observer-a", "observer-b")
        ]

    def test_compiler_is_source_pinned_and_nonexecuting(self):
        self.assertEqual(self.plan["shot_id"], "S13")
        self.assertFalse(self.plan["submissions_authorized"])
        self.assertIn("S13", self.plan["branches"]["shot"]["prompt"])
        self.assertTrue(self.plan["branches"]["fusion"]["depends_on"])
        self.assertEqual(self.plan["branches"]["artwork"]["state"], "NOT_RUN")

    def test_mismatched_model_and_no_unlimited_rejected(self):
        with self.assertRaisesRegex(ValueError, "model cannot"):
            chat_loop.compile_plan(REPO, {"id":"x","output_type":"image","aspect_ratios":["16:9"]})
        self.assertFalse(chat_loop.quote_allows_zero_credits(
            {"error":"Unlimited generations aren't available on this account"},
            model_id="gpt_image_2_6",surface="higgsfield_chat"))
        self.assertFalse(chat_loop.quote_allows_zero_credits(
            {"model":"gpt_image_2_6","cost":{"credits":1},"unlimited_applied":False,"quote_ref":"q"},
            model_id="gpt_image_2_6",surface="higgsfield_chat"))

    def test_paid_or_unverifiable_quote_must_not_create_image_evidence(self):
        for cost, confirmed in ((1, True), (0, False)):
            with self.subTest(cost=cost, confirmed=confirmed):
                with self.assertRaisesRegex(ValueError, "zero-credit"):
                    chat_loop.record_image(REPO,self.plan,"artwork",
                                           self.receipt("artwork",cost=cost,quote=confirmed),
                                           self.assets)
        self.assertEqual(self.plan["branches"]["artwork"]["state"],"NOT_RUN")

    def test_fusion_requires_both_independently_reviewed_branches(self):
        with self.assertRaisesRegex(ValueError, "parent QC PASS"):
            chat_loop.record_image(REPO,self.plan,"fusion",self.receipt("fusion"),self.assets)

    def test_evidence_review_and_release_path(self):
        plan=self.plan
        for stage in ("artwork","shot","fusion"):
            ev=self.receipt(stage)
            plan=chat_loop.record_image(REPO,plan,stage,ev,self.assets)
            self.assertEqual(plan["branches"][stage]["state"],"EVIDENCE_INCOMPLETE")
            plan=chat_loop.evaluate_human_qc(REPO,plan,stage,self.humans(plan,stage),"producer")
            self.assertEqual(plan["branches"][stage]["state"],"QC_PASS")
        frozen=chat_loop.approve_golden(plan,"final-owner")
        self.assertTrue(frozen["golden"])
        self.assertFalse(frozen["recipe_reusable"])
        self.assertFalse(plan["golden"])
        with self.assertRaisesRegex(ValueError,"overwritten"):
            chat_loop.record_image(REPO,frozen,"artwork",self.receipt("artwork"),self.assets)

    def test_single_reviewer_wrong_identity_and_wrong_prompt_rejected(self):
        plan=chat_loop.record_image(REPO,self.plan,"shot",self.receipt("shot"),self.assets)
        with self.assertRaisesRegex(ValueError,"two independent"):
            chat_loop.evaluate_human_qc(REPO,plan,"shot",self.humans(plan,"shot")[:1],"producer")
        review=self.humans(plan,"shot")
        review[1]["reviewer_id"]="producer"
        with self.assertRaisesRegex(ValueError,"distinct"):
            chat_loop.evaluate_human_qc(REPO,plan,"shot",review,"producer")
        ev=self.receipt("artwork")
        ev["sent_prompt"]="different"
        with self.assertRaisesRegex(ValueError,"drift"):
            chat_loop.record_image(REPO,self.plan,"artwork",ev,self.assets)

    def test_beach_failure_bounded_repair_and_no_fusion(self):
        plan=chat_loop.record_image(REPO,self.plan,"shot",self.receipt("shot"),self.assets)
        plan=chat_loop.evaluate_human_qc(REPO,plan,"shot",self.humans(plan,"shot",beach=True),"producer")
        self.assertEqual(plan["branches"]["shot"]["state"],"QC_FAIL")
        with self.assertRaisesRegex(ValueError,"without three"):
            chat_loop.approve_golden(plan,"owner")
        repaired=chat_loop.propose_repair(plan,"shot","beach-piano","review-evidence-01")
        self.assertEqual(repaired["repairs"]["shot:beach-piano"]["attempts"],1)
        with self.assertRaisesRegex(ValueError,"already repaired"):
            chat_loop.propose_repair(repaired,"shot","beach-piano","review-evidence-02")

    def test_q15_fault_injection_preserves_frozen_artwork(self):
        baseline=self.plan["branches"]["artwork"]["prompt_sha256"]
        dry=chat_loop.dry_run_shot_change(self.plan,self.plan["branches"]["shot"]["prompt"]+"\nlocalized fix")
        self.assertEqual(dry["invalidated"],["shot","fusion"])
        self.assertEqual(dry["reused"],["artwork"])
        self.assertEqual(self.plan["branches"]["artwork"]["prompt_sha256"],baseline)
        self.assertEqual(dry["provider_calls"],0)
        noop=chat_loop.dry_run_shot_change(self.plan,self.plan["branches"]["shot"]["prompt"])
        self.assertEqual(noop["invalidated"],[])


if __name__=="__main__":
    unittest.main()
