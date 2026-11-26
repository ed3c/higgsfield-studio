import unittest
from studio.reverse.v2r3_score import score


def fixture(dctl=True):
    key = {"claims": [{"review_id": "J01", "original_id": None, "class": "MEASURED", "decoy": True},
                      {"review_id": "J02", "original_id": "M1", "class": "MEASURED", "decoy": False},
                      {"review_id": "J03", "original_id": "I1", "class": "INFERRED", "decoy": False}],
           "A1_timestamps": [{"sample": f"Q{i:02d}", "author_role": "SPEAKER_WITH_MIC" if i < 5 else None} for i in range(12)],
           "A5_author_sequence_starts": [100.0, 200.0],
           "author_boundaries": [{"t": 10.0, "kind": "cut"}, {"t": 21.0, "kind": "black_edge"}] + [{"t": 50.0 + i, "kind": "cut"} for i in range(5)]
                                + [{"t": 300.0 + i, "kind": "cut"} for i in range(5)],
           "author_dissolves": [{"start": 400.0 + 10 * i, "end": 401.0 + 10 * i} for i in range(5)],
           "dissolve_controls_pass": dctl,
           "A2_windows": [{"window": "Z01", "stratum": "SEG2_CUT_V1", "target": 10.0}, {"window": "Z02", "stratum": "RANDOM", "target": None}]
                         + [{"window": f"Z1{i}", "stratum": "SEG2_CUT_NEW", "target": 300.0 + i} for i in range(5)]
                         + [{"window": f"Z2{i}", "stratum": "SEG2_DISSOLVE", "target": None, "target_span": {"start": 400.0 + 10 * i, "end": 401.0 + 10 * i}} for i in range(5)],
           "A3_spans": [{"span": "V01", "seg2_boundaries_inside": [{"t": 50.0 + i} for i in range(5)]}],
           "A4_camera": [{"cam": f"N{i:02d}", "author_label": "STATIC" if i < 5 else "PAN_OR_TRACK_H"} for i in range(12)]}
    A = {"A1_timestamps": [{"sample": f"Q{i:02d}", "answer": {"people_role": "SPEAKER_WITH_MIC" if i < 5 else "NO_PEOPLE"}} for i in range(12)],
         "A2_windows": [{"window": "Z01", "answer": {"transitions": [{"t_seconds": 10.1, "type": "HARD_CUT"}]}},
                        {"window": "Z02", "answer": {"transitions": [{"t_seconds": 21.2, "type": "CUT_TO_BLACK"}]}}]
                       + [{"window": f"Z1{i}", "answer": {"transitions": [{"t_seconds": 300.2 + i, "type": "HARD_CUT"}]}} for i in range(5)]
                       + [{"window": f"Z2{i}", "answer": {"transitions": [{"t_seconds": 400.5 + 10 * i, "type": "DISSOLVE"}]}} for i in range(5)],
         "A3_spans": [{"span": "V01", "answer": {"transitions": [{"t_seconds": 50.0 + i, "type": "HARD_CUT"} for i in range(5)]}}],
         "A4_camera": [{"cam": f"N{i:02d}", "answer": {"movement": "STATIC" if i < 5 else "PAN_OR_TRACK_H"}} for i in range(12)],
         "A5_sequences": {"sequence_start_seconds": [101, 205]}}
    B = {"claims": [{"review_id": "J01", "verdict": "NOT_SUPPORTED"}, {"review_id": "J02", "verdict": "SUPPORTED"},
                    {"review_id": "J03", "verdict": "PARTIALLY_SUPPORTED"}]}
    return A, B, key


class V2R3ScoreTests(unittest.TestCase):
    def test_pass_when_dissolve_controls_pass(self):
        A, B, k = fixture()
        r = score(A, B, k, [])
        self.assertEqual(r["R4"]["R4_new"], "PASS")
        self.assertEqual(r["R7"]["status"], "PASS")
        self.assertEqual(r["V2_verdict"], "PASS (agent review)")

    def test_failed_dissolve_controls_force_r7_inconclusive(self):
        A, B, k = fixture(dctl=False)
        r = score(A, B, k, [])
        self.assertEqual(r["R7"]["status"], "INCONCLUSIVE")
        self.assertEqual(r["uncapped_gate_verdict"], "INCONCLUSIVE")

    def test_new_cut_miss_fails(self):
        A, B, k = fixture()
        for w in A["A2_windows"]:
            if w["window"].startswith("Z1"):
                w["answer"] = {"transitions": []}
        r = score(A, B, k, [])
        self.assertEqual(r["R4"]["R4_new"], "FAIL")
        self.assertEqual(r["uncapped_gate_verdict"], "FAIL")

    def test_identity_breach_caps_and_reports_uncapped(self):
        A, B, k = fixture()
        r = score(A, B, k, ["F-12 same identity"])
        self.assertEqual(r["uncapped_gate_verdict"], "PASS")
        self.assertTrue(r["V2_verdict"].startswith("INCONCLUSIVE"))

    def test_decoy_miss_invalid(self):
        A, B, k = fixture(); B["claims"][0]["verdict"] = "SUPPORTED"
        self.assertTrue(score(A, B, k, [])["V2_verdict"].startswith("INVALID_REVIEW"))


if __name__ == "__main__":
    unittest.main()
