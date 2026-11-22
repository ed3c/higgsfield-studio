"""Evidence-bound candidate regression: binary, provenance, two independent reviews.

Fixture creates a valid 1x1 PNG with stdlib; it does NOT simulate real artistic
recognition, rights approval, model generation or external provider usage.
"""
from __future__ import annotations
import hashlib
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from studio_factory.art_contracts import compile_shot, load_contract
from studio_factory.evidence_gate import review_candidate, verify_receipt, EvidenceGateError

ROOT=Path(__file__).resolve().parents[2]


def pixel_png():
    def chunk(name, body):
        return (struct.pack(">I", len(body)) + name + body
                + struct.pack(">I", zlib.crc32(name + body)))
    raw=b"\x00\x20\x40\x60\xff"   # one RGBA pixel + PNG filter byte
    return (b"\x89PNG\r\n\x1a\n"
            +chunk(b"IHDR",struct.pack(">IIBBBBB",1,1,8,6,0,0,0))
            +chunk(b"IDAT",zlib.compress(raw))
            +chunk(b"IEND",b""))


class EvidenceGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=load_contract(ROOT)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.asset=self.root/"extra"/"candidates"/"S14-001.png"
        self.asset.parent.mkdir(parents=True)
        self.asset.write_bytes(pixel_png())
        self.digest=hashlib.sha256(self.asset.read_bytes()).hexdigest()
        self.compiled=compile_shot(self.registry,"S14")
        self.receipt={
            "schema":"studio.generation-receipt.v2",
            "project":"j4-async-succession",
            "candidate_id":"S14-001","shot_id":"S14",
            "producer":"operator-A",
            "provider":"local-fixture", "provider_run_id":"fixture-001",
            "model":"fixture-only","model_version":"0",
            "generated_at":"2026-11-23T00:00:00+00:00","seed":0,
            "settings":{"aspect_ratio":"9:16"},
            "credits":0,
            "sent_prompt":self.compiled["prompt"],
            "sent_negative_prompt":self.compiled["global_negative_prompt"],
            "compiled_payload_sha256":self.compiled["payload_sha256"],
            "generation_gate_at_time":"EXTERNALLY_APPROVED",
            "authorization_evidence":{
                "owner":"fixture://owner", "director_estimate":"fixture://estimate",
                "account_balance":"fixture://balance","rights":"fixture://rights"},
            "reference_assets":[],
            "output":{"relative_path":"extra/candidates/S14-001.png",
                      "media_type":"still","sha256":self.digest}
        }
        p=next(s for s in self.registry["contract"]["shots"] if s["shot_id"]=="S14")
        self.static=[c for c in p["checks"] if c["modality"]=="still"]

    def tearDown(self):
        self.temp.cleanup()

    def review(self,who,changes=None):
        states={c["id"]:c["polarity"]=="must_exist" for c in self.static}
        if changes:states.update(changes)
        obs={cid:{"observed":flag,"media_sha256":self.digest,"full_frame":True,
                  "frame_at_ms":0,"evidence_note":"fixture simulated reviewer observation"}
             for cid,flag in states.items()}
        return {"schema":"studio.g2-review.v2",
                "reviewer_id":who,"candidate_id":self.receipt["candidate_id"],
                "shot_id":"S14","media_sha256":self.digest,
                "compiled_payload_sha256":self.compiled["payload_sha256"],
                "observations":obs}

    def test_integrity_and_non_promotion_even_if_all_claim_positive(self):
        receipt=verify_receipt(self.registry,self.root,self.receipt)
        self.assertTrue(receipt["provider_receipt_present"])
        self.assertEqual(receipt["decoded_media_qa"],"NOT_RUN")
        a,b=self.review("reviewer-A"),self.review("reviewer-B")
        report=review_candidate(self.registry,self.root,self.receipt,[a,b])
        self.assertEqual(report["state"],"STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN")
        self.assertFalse(report["ready_for_generation"])
        self.assertEqual(report["director_approval"],"NOT_RUN")
        self.assertTrue(report["pending_temporal"])
        self.assertTrue(report["observed_not_machine_detected"])
        self.assertEqual(report["passed_static_check_ids"],
                         [x["id"] for x in self.static])

    def test_both_reviewers_reject_missing_audience(self):
        changes={"S14.AUDIENCE_PRESENT":False,"S14.EMPTY_AUDITORIUM":True}
        out=review_candidate(self.registry,self.root,self.receipt,
                            [self.review("A",changes),self.review("B",changes)])
        self.assertEqual(out["state"],"STATIC_REJECTED_BY_TWO_REVIEWERS")
        self.assertIn("S14.AUDIENCE_PRESENT",out["rejected_static_check_ids"])

    def test_disagreement_is_never_approved(self):
        out=review_candidate(self.registry,self.root,self.receipt,
                            [self.review("A"),self.review("B",{"S14.HERO_COSTUME":True})])
        self.assertEqual(out["state"],"STATIC_DISPUTED_NEEDS_ADJUDICATION")
        self.assertIn("S14.HERO_COSTUME",out["disputed_static_check_ids"])

    def test_missing_or_forged_receipt_is_blocked(self):
        for field,invalid in [
            ("sent_prompt","nice picture"),
            ("compiled_payload_sha256","0"*64),
            ("generation_gate_at_time","BLOCKED"),
            ("authorization_evidence",{}),
            ("reference_assets",None)]:
            data={**self.receipt,field:invalid}
            report=review_candidate(self.registry,self.root,data,
                                    [self.review("A"),self.review("B")])
            self.assertEqual(report["state"],"BLOCKED_INVALID_RECEIPT",field)
        data=json.loads(json.dumps(self.receipt))
        data["output"]["sha256"]="f"*64
        self.assertEqual(review_candidate(self.registry,self.root,data,
                [self.review("A"),self.review("B")])["state"],"BLOCKED_INVALID_RECEIPT")

    def test_asset_reference_cannot_escape_root(self):
        for uri in ["../outside.png","/etc/passwd","../../secret","extra/../outside.png"]:
            data=json.loads(json.dumps(self.receipt))
            data["output"]["relative_path"]=uri
            self.assertEqual(review_candidate(self.registry,self.root,data,
                [self.review("A"),self.review("B")])["state"],"BLOCKED_INVALID_RECEIPT")

    def test_review_witness_cannot_be_reused_for_other_media(self):
        good=self.review("A")
        forged=self.review("B")
        forged["observations"]["S14.AUDIENCE_PRESENT"]["media_sha256"]="a"*64
        out=review_candidate(self.registry,self.root,self.receipt,[good,forged])
        self.assertEqual(out["state"],"BLOCKED_EVIDENCE_INVALID")
        self.assertTrue(any("digest differs" in s for s in out["errors"]))

    def test_no_single_or_self_review(self):
        one=self.review("A")
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,[one])["state"],
                         "BLOCKED_INDEPENDENT_REVIEW")
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [one,one])["state"],"BLOCKED_EVIDENCE_INVALID")
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [one,self.review("operator-A")])["state"],"BLOCKED_EVIDENCE_INVALID")

    def test_invalid_or_omitted_frame_evidence(self):
        a,b=self.review("A"),self.review("B")
        a["observations"]["S14.AUDIENCE_PRESENT"]["full_frame"]=False
        a["observations"]["S14.AUDIENCE_PRESENT"]["roi_norm"]=[0.9,0.9,0.2,0.2]
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [a,b])["state"],"BLOCKED_EVIDENCE_INVALID")
        a,b=self.review("A"),self.review("B")
        del a["observations"]["S14.AUDIENCE_PRESENT"]
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [a,b])["state"],"BLOCKED_EVIDENCE_INVALID")
        a,b=self.review("A"),self.review("B")
        a["observations"]["S14.AUDIENCE_PRESENT"]["frame_at_ms"]=999
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [a,b])["state"],"BLOCKED_EVIDENCE_INVALID")

    def test_local_review_catalog_surfaces_bound_candidate_and_denies_pass(self):
        import threading
        import urllib.error
        import urllib.request
        from http.server import ThreadingHTTPServer
        from studio_factory.review_web import Catalog, Handler
        receipts_dir = self.root / "extra" / "g2_receipts"
        review_dir = self.root / "extra" / "g2_reviews" / "S14-001"
        receipts_dir.mkdir(parents=True)
        review_dir.mkdir(parents=True)
        (receipts_dir / "S14-001.json").write_text(
            json.dumps(self.receipt), encoding="utf-8")
        for name, review in (("a", self.review("Reviewer-A")),
                             ("b", self.review("Reviewer-B"))):
            (review_dir / (name + ".json")).write_text(
                json.dumps(review), encoding="utf-8")
        from pathlib import Path
        catalog = Catalog(self.root, ROOT, self.root / "review.sqlite3")
        try:
            candidates = [c for c in catalog.entries.values()
                          if c["group"] == "candidate"]
            self.assertEqual(len(candidates), 1)
            item = candidates[0]
            self.assertEqual(item["meta"]["report"]["state"],
                             "STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN")
            self.assertIsNotNone(item["meta"]["media_resource_id"])
            self.assertIsNotNone(item["meta"]["receipt_resource_id"])
            self.assertEqual(item["meta"]["generation_gate"], "BLOCKED")
            server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            server.app = catalog
            server.csrf = "only-test"
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                uri = f"http://127.0.0.1:{server.server_port}/api/review"
                body = {"item_id": item["id"], "decision":"PASS",
                        "note":"attempted gate bypass", "reviewer":"test", "evidence":""}
                request = urllib.request.Request(
                    uri, data=json.dumps(body).encode(), method="POST",
                    headers={"X-Review-CSRF": "only-test",
                             "Content-Type":"application/json"})
                with self.assertRaises(urllib.error.HTTPError) as err:
                    urllib.request.urlopen(request,timeout=5)
                self.assertEqual(err.exception.code,400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
        finally:
            catalog.store.connection.close()

    def test_unknown_observation_or_wrong_type_is_rejected(self):
        a,b=self.review("A"),self.review("B")
        a["observations"]["S14.UNDEFINED_RULE"]={"observed":True}
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [a,b])["state"],"BLOCKED_EVIDENCE_INVALID")
        a,b=self.review("A"),self.review("B")
        a["observations"]=["not","a","map"]
        self.assertEqual(review_candidate(self.registry,self.root,self.receipt,
                         [a,b])["state"],"BLOCKED_EVIDENCE_INVALID")

    def test_boolean_seed_is_not_provenance(self):
        data=json.loads(json.dumps(self.receipt))
        data["seed"]=True
        self.assertEqual(review_candidate(self.registry,self.root,data,
                         [self.review("A"),self.review("B")])["state"],"BLOCKED_INVALID_RECEIPT")

    def test_reference_hash_must_match(self):
        reference=self.root/"reference.png";reference.write_bytes(pixel_png())
        data=json.loads(json.dumps(self.receipt))
        data["reference_assets"]=[{"relative_path":"reference.png","sha256":"0"*64}]
        self.assertEqual(review_candidate(self.registry,self.root,data,
                         [self.review("A"),self.review("B")])["state"],"BLOCKED_INVALID_RECEIPT")

    def test_false_video_extension_not_enough(self):
        fake=self.root/"extra"/"candidate.mp4";fake.write_bytes(b"not an MP4")
        data=json.loads(json.dumps(self.receipt))
        data["output"]={"relative_path":"extra/candidate.mp4","media_type":"video",
                        "sha256":hashlib.sha256(fake.read_bytes()).hexdigest()}
        self.assertEqual(review_candidate(self.registry,self.root,data,
                         [self.review("A"),self.review("B")])["state"],"BLOCKED_INVALID_RECEIPT")


if __name__=="__main__":
    unittest.main()
