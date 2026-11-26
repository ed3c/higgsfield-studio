import unittest
from studio.reverse.v2r2_score import score


def fixture():
    key = {"claims": [{"review_id": "K01", "original_id": None, "class": "MEASURED", "decoy": True},
                      {"review_id": "K02", "original_id": "M1", "class": "MEASURED", "decoy": False},
                      {"review_id": "K03", "original_id": "I1", "class": "INFERRED", "decoy": False}],
           "A1_timestamps": [{"sample": f"P{i:02d}", "author_role": "SPEAKER_WITH_MIC" if i < 5 else None} for i in range(12)],
           "A5_author_sequence_starts": [100.0, 200.0],
           "author_boundaries": [{"t": 10.0, "kind": "cut"}, {"t": 21.0, "kind": "black_start"}] + [{"t": 50.0 + i, "kind": "cut"} for i in range(5)],
           "A2_windows": [{"window": "X01", "stratum": "V1_HARD_CUT", "target": 10.0}, {"window": "X02", "stratum": "RANDOM", "target": None}],
           "A3_spans": [{"span": "Y01", "v1_boundaries_inside": [{"t": 50.0 + i} for i in range(5)]}],
           "A4_camera": [{"cam": f"M{i:02d}", "author_label": "STATIC" if i < 5 else "PAN_OR_TRACK_H"} for i in range(12)]}
    A = {"A1_timestamps": [{"sample": f"P{i:02d}", "answer": {"people_role": "SPEAKER_WITH_MIC" if i < 5 else "NO_PEOPLE"}} for i in range(12)],
         "A2_windows": [{"window": "X01", "answer": {"transitions": [{"t_seconds": 10.1, "type": "HARD_CUT"}]}},
                        {"window": "X02", "answer": {"transitions": [{"t_seconds": 21.2, "type": "CUT_TO_BLACK"}]}}],
         "A3_spans": [{"span": "Y01", "answer": {"transitions": [{"t_seconds": 50.0 + i, "type": "HARD_CUT"} for i in range(5)]}}],
         "A4_camera": [{"cam": f"M{i:02d}", "answer": {"movement": "STATIC" if i < 5 else "PAN_OR_TRACK_H"}} for i in range(12)],
         "A5_sequences": {"sequence_start_seconds": [101, 205]}}
    B = {"claims": [{"review_id": "K01", "verdict": "NOT_SUPPORTED"}, {"review_id": "K02", "verdict": "SUPPORTED"},
                    {"review_id": "K03", "verdict": "PARTIALLY_SUPPORTED"}]}
    return A, B, key


class V2R2ScoreTests(unittest.TestCase):
    def test_pass(self):
        A, B, k = fixture()
        self.assertEqual(score(A, B, k, [])["V2_verdict"], "PASS (agent review)")

    def test_decoy_miss_invalid(self):
        A, B, k = fixture(); B["claims"][0]["verdict"] = "SUPPORTED"
        self.assertTrue(score(A, B, k, [])["V2_verdict"].startswith("INVALID_REVIEW"))

    def test_breach_caps(self):
        A, B, k = fixture()
        self.assertTrue(score(A, B, k, ["same identity"])["V2_verdict"].startswith("INCONCLUSIVE"))

    def test_missing_evidence_inconclusive(self):
        A, B, k = fixture(); B["claims"][1] = {"review_id": "K02", "verdict": "CANNOT_DETERMINE", "cannot_determine_reason": "EVIDENCE_MISSING_FROM_PACKAGE"}
        r = score(A, B, k, [])
        self.assertEqual(r["R2"]["R2_mea"], "INCONCLUSIVE")
        self.assertTrue(r["V2_verdict"].startswith("INCONCLUSIVE"))


if __name__ == "__main__":
    unittest.main()
