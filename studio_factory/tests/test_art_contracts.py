"""G2 Art Mechanism regression: six rejected images must never be called PASS."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from studio_factory.art_contracts import (
    ArtContractError, SHOT_IDS, compile_shot, judge_observations, load_contract
)

ROOT = Path(__file__).resolve().parents[2]
REPORT = (ROOT / "projects/j4-async-succession/qc/"
          "six_panel_observations_v4_1.json")


class ArtRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_contract(ROOT)
        cls.cases = json.loads(REPORT.read_text(encoding="utf-8"))["cases"]

    def test_six_source_locked_contracts_have_explicit_p0s(self):
        self.assertEqual(len(SHOT_IDS), 6)
        self.assertEqual(self.registry["checks_total"], 33)
        self.assertEqual(self.registry["contract"]["generation_gate"], "BLOCKED")
        self.assertEqual({x["shot_id"] for x in self.registry["contract"]["shots"]}, set(SHOT_IDS))
        self.assertEqual({x["shot_id"] for x in self.cases}, set(SHOT_IDS))
        for p in self.registry["contract"]["shots"]:
            self.assertGreater(len(p["scene_graph"]), 2)
            self.assertTrue(all(c["severity"] == "P0" for c in p["checks"]))
            self.assertTrue(any(c["modality"] == "still" for c in p["checks"]))
            self.assertTrue(any(c["modality"] != "still" for c in p["checks"]))
            self.assertTrue(len(p["references"]) >= 2)

    def test_compiler_pins_scene_and_never_calls_provider(self):
        for shot_id in SHOT_IDS:
            payload = compile_shot(self.registry, shot_id)
            self.assertEqual(payload["generation_gate"], "BLOCKED")
            self.assertFalse(payload["media_created"])
            self.assertEqual(payload["provider_call"], "NONE")
            self.assertIn("HIGHEST PRIORITY", payload["prompt"])
            self.assertIn("PRIMARY ACTION:", payload["prompt"])
            self.assertIn("FORBIDDEN:", payload["prompt"])
            self.assertIn(self.registry["canonical"][shot_id]["image_prompt"], payload["prompt"])
            self.assertIn(self.registry["master"]["master_image_lock"], payload["prompt"])
            self.assertIn(self.registry["master"]["global_negative_prompt"], payload["prompt"])
            for key, source in (("source_motion_prompt", "motion_prompt"),
                                ("source_sound_prompt", "sound_prompt"),
                                ("in_transition", "in_transition"),
                                ("out_transition", "out_transition")):
                self.assertEqual(payload[key], self.registry["canonical"][shot_id][source])
            self.assertEqual(payload["props"], self.registry["canonical"][shot_id]["props"])
            self.assertEqual(payload["characters"], self.registry["canonical"][shot_id]["characters"])
            self.assertEqual(payload, compile_shot(self.registry, shot_id))
            self.assertEqual(len(payload["payload_sha256"]), 64)

    def test_reject_all_six_failed_user_supplied_cues(self):
        actual_failures = set()
        for case in self.cases:
            report = judge_observations(self.registry, case)
            self.assertEqual(report["state"], "REJECTED_BY_OBSERVATION", case["shot_id"])
            self.assertFalse(report["media_sha256_verified"])
            self.assertEqual(report["director_gate"], "NOT_RUN")
            self.assertEqual(report["rights_gate"], "NOT_RUN")
            self.assertEqual(report["paid_generation_gate"], "BLOCKED")
            self.assertGreater(len(report["failures"]), 0)
            self.assertTrue(report["unverified"])
            actual_failures.update(c["check_id"] for c in report["failures"])
        self.assertTrue({"S02.BOWL_TRANSFER", "S04.ORNATE_FULL_BIRD",
                         "S06.SPLIT_COMPOSITION", "S11.PAPER_HOUSE",
                         "S13.OUTDOOR_BEACH_PIANO", "S14.EMPTY_AUDITORIUM"}
                        <= actual_failures)

    def test_no_self_review_and_no_fake_pass_from_positive_claims(self):
        case = dict(self.cases[0])
        case["reviewer"] = case["producer"]
        self.assertEqual(judge_observations(self.registry, case)["state"], "BLOCKED")
        p = next(s for s in self.registry["contract"]["shots"] if s["shot_id"] == "S02")
        case["reviewer"] = "independent_human_1"
        case["observations"] = {c["id"]: {
            "observed": c["polarity"] == "must_exist",
            "evidence_uri": "review-evidence-not-yet-hashed"
        } for c in p["checks"]}
        report = judge_observations(self.registry, case)
        self.assertEqual(report["state"], "BLOCKED_INCOMPLETE_EVIDENCE")
        self.assertEqual(report["director_gate"], "NOT_RUN")

    def test_unknown_id_must_not_be_ignored(self):
        case = dict(self.cases[0])
        case["observations"] = dict(case["observations"])
        case["observations"]["S09.MADE_UP"] = {"observed": True}
        with self.assertRaisesRegex(ArtContractError, "unknown check ID"):
            judge_observations(self.registry, case)

    def test_source_hash_is_an_exact_git_blob_lock(self):
        original = (ROOT / self.registry["contract"]["source_locks"][0]["path"]).read_bytes()
        expected = self.registry["contract"]["source_locks"][0]["git_blob_sha1"]
        actual = hashlib.sha1(
            b"blob " + str(len(original)).encode() + b"\x00" + original
        ).hexdigest()
        self.assertEqual(expected, actual)
        self.assertNotEqual(hashlib.sha1(
            b"blob " + str(len(original) + 1).encode() + b"\x00"
            + original + b"\n").hexdigest(), expected)

    def test_local_review_site_exposes_six_art_cases_with_blocked_pass(self):
        import threading
        import urllib.error
        import urllib.request
        from http.server import ThreadingHTTPServer
        from studio_factory.review_web import Catalog, Handler
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = Catalog(root / "assets", ROOT, root / "reviews.sqlite3")
            art = [entry for entry in catalog.entries.values() if entry["group"] == "art"]
            self.assertEqual(len(art), 6)
            run = catalog.run_test("art_contract")
            self.assertEqual(run["state"], "PASS_STATIC")
            self.assertEqual(run["expected_rejected_reports"], 6)
            self.assertEqual(run["visual_media_verified"], 0)
            self.assertTrue(all(a["meta"]["report"]["state"] == "REJECTED_BY_OBSERVATION"
                                for a in art))
            server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            server.app = catalog
            server.csrf = "test-csrf"
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}/api/review"
                payload = {"item_id": art[0]["id"], "decision": "PASS",
                           "note": "attempt to bypass independent QC",
                           "reviewer": "fixture", "evidence": ""}
                request = urllib.request.Request(url,
                    data=json.dumps(payload).encode("utf-8"), method="POST",
                    headers={"Content-Type": "application/json",
                             "X-Review-CSRF": server.csrf})
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(request, timeout=5)
                self.assertEqual(error.exception.code, 400)
                self.assertEqual(catalog.store.get_all(), {})
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)

    def test_static_still_cannot_prove_temporal_optical_success(self):
        case = dict(self.cases[1])
        case["observations"] = {}
        p = next(s for s in self.registry["contract"]["shots"] if s["shot_id"] == "S04")
        case["observations"] = {c["id"]: {"observed": c["polarity"] == "must_exist",
                                                  "evidence_uri": "placeholder"}
                                for c in p["checks"]}
        report = judge_observations(self.registry, case)
        self.assertEqual(report["state"], "BLOCKED_INCOMPLETE_EVIDENCE")
        self.assertTrue(any("still" in x["reason"] for x in report["unverified"]))


if __name__ == "__main__":
    unittest.main()
