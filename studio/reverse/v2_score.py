"""Score an S1 V2 agent review against the sealed Reference Oracle key (pre-registered RUBRIC.md).

Run AFTER the reviewer has delivered stage_A_answers.json and stage_B_answers.json.
Outcome label is always 'agent review' (not a human Oracle; cf. GAP-EVAL-01).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SUP = {"SUPPORTED", "PARTIALLY_SUPPORTED"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--key", type=Path, required=True)
    ap.add_argument("--pack", type=Path, required=True, help="private v1 pack (for author labels)")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    A = json.load(open(a.package / "answers/stage_A_answers.json"))
    B = json.load(open(a.package / "answers/stage_B_answers.json"))
    ck = json.load(open(a.key / "claims_key.json"))
    sk = json.load(open(a.key / "strata_key.json"))
    obs = json.load(open(a.pack / "observations.agent.json"))
    segs = json.load(open(a.pack / "shots/segments.json"))["segments"]
    verdict = {c["review_id"]: c for c in B["claims"]}
    res = {"label": "agent review (not a human Oracle; cf. GAP-EVAL-01)", "rubric": "RUBRIC.md v1 (pre-registered)"}
    # R1 decoys
    dec = [m for m in ck["mapping"] if m["decoy"]]
    rej = [m["review_id"] for m in dec if verdict.get(m["review_id"], {}).get("verdict") == "NOT_SUPPORTED"]
    res["R1_decoys"] = {"rejected": len(rej), "of": len(dec), "status": "VALID" if len(rej) == len(dec) else "INVALID_REVIEW"}
    # R2 claim support
    real = [m for m in ck["mapping"] if not m["decoy"]]
    inf = [m for m in real if m["class"] == "INFERRED"]
    mea = [m for m in real if m["class"] == "MEASURED"]
    inf_sup = sum(verdict.get(m["review_id"], {}).get("verdict") in SUP for m in inf)
    inf_ns = [m["original_id"] for m in inf if verdict.get(m["review_id"], {}).get("verdict") == "NOT_SUPPORTED"]
    mea_sup = sum(verdict.get(m["review_id"], {}).get("verdict") == "SUPPORTED" for m in mea)
    r2 = inf_sup >= 0.75 * len(inf) and mea_sup >= 0.90 * len(mea)
    res["R2_claims"] = {"inferred_supported_or_partial": f"{inf_sup}/{len(inf)}", "inferred_not_supported": inf_ns,
                        "measured_supported": f"{mea_sup}/{len(mea)}", "status": "PASS" if r2 else "FAIL",
                        "per_claim": [{"original_id": m["original_id"], "verdict": verdict.get(m["review_id"], {}).get("verdict")} for m in real]}
    # R3 blind agreement (roles) + sequence boundaries
    role_map = {"interviewee_A_white_wall_title_lettering": "SEATED_INTERVIEW_SINGLE", "speaker_B_with_microphone_white_wall": "SPEAKER_WITH_MIC",
                "speaker_C_seated_with_microphone": "SPEAKER_WITH_MIC"}
    author_role = {i: role_map[r] for r, ids in obs["role_shots"].items() for i in ids}
    agree = n = 0
    for s in A["segments"]:
        rv = s["answer"].get("people_role")
        if rv in (None, "", "CANNOT_DETERMINE"):
            continue
        au = author_role.get(s["segment_id"])
        is_int_rev = rv in ("SEATED_INTERVIEW_SINGLE", "SPEAKER_WITH_MIC")
        is_int_au = au is not None
        n += 1
        agree += (is_int_rev == is_int_au) and (not is_int_au or rv == au)
    role_ok = n > 0 and agree / n >= 0.80
    idx = {s["id"]: i for i, s in enumerate(segs)}
    au_b = sorted({idx[next(x["id"] for x in segs if x["start"] >= q["start"] - 1e-6)] for q in obs["sequences"]})
    rv_b = sorted({idx[i] for i in A["sequences"]["sequence_start_segment_ids"] if i in idx})
    tp = sum(any(abs(r - b) <= 1 for b in au_b) for r in rv_b)
    prec = tp / len(rv_b) if rv_b else 0
    rec = sum(any(abs(r - b) <= 1 for r in rv_b) for b in au_b) / len(au_b) if au_b else 0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0
    res["R3_blind_agreement"] = {"role_agreement": f"{agree}/{n}", "sequence_boundary_f1_pm1": round(f1, 3),
                                 "status": "PASS" if role_ok and f1 >= 0.60 else ("INCONCLUSIVE" if n < 10 else "FAIL")}
    # R4 cut recall in random windows + boundary-window precision
    ans = {s["window"]: s["answer"] for s in A["strips"]}
    hard_rev = found_by_v1 = 0
    bw_ok = bw_n = 0
    for k in sk["strips"]:
        an = ans.get(k["window"], {})
        hc = an.get("transition_present") == "YES" and an.get("type") in ("HARD_CUT",)
        if k["stratum"] == "RANDOM" and hc:
            hard_rev += 1
            found_by_v1 += bool(k["v1_boundaries_inside"])
        if k["stratum"] == "V1_HARD_CUT":
            bw_n += 1
            bw_ok += hc
    rec4 = found_by_v1 / hard_rev if hard_rev else None
    res["R4_cuts"] = {"random_window_hard_cuts_seen_by_reviewer": hard_rev, "of_which_v1_has_boundary": found_by_v1,
                      "recall": rec4, "hard_cut_window_confirmed": f"{bw_ok}/{bw_n}",
                      "status": "INCONCLUSIVE" if hard_rev < 5 else ("PASS" if rec4 >= 0.80 and bw_ok >= 0.9 * bw_n else "FAIL")}
    # R5 forbidden inference
    forb = [c["review_id"] for c in B["claims"] if c.get("forbidden_inference") not in (None, "", "NONE")]
    forb_real = [m["original_id"] for m in real if m["review_id"] in forb]
    res["R5_forbidden"] = {"flagged_real_claims": forb_real, "status": "PASS" if not forb_real else "FAIL"}
    if res["R1_decoys"]["status"] != "VALID":
        v = "INVALID_REVIEW"
    elif any(res[k]["status"] == "FAIL" for k in ("R2_claims", "R3_blind_agreement", "R4_cuts", "R5_forbidden")):
        v = "FAIL"
    elif any(res[k]["status"] == "INCONCLUSIVE" for k in ("R3_blind_agreement", "R4_cuts")):
        v = "INCONCLUSIVE"
    else:
        v = "PASS"
    res["V2_verdict"] = f"{v} (agent review)"
    a.out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(res["V2_verdict"])


if __name__ == "__main__":
    main()
