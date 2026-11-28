"""Score the S1 V2 round-3 agent review (RUBRIC_V2R4.md). Run only after both stages are delivered.

The key is decrypted to memory (passphrase from env V2R4_KEY_PASS) and verified against the published plaintext SHA-256.
Outcome label is always 'agent review'.
"""
from __future__ import annotations

import argparse, hashlib, json, os, subprocess
from pathlib import Path

OPENSSL = ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "600000", "-salt", "-md", "sha256", "-d", "-pass", "env:V2R4_KEY_PASS"]
CUT = {"HARD_CUT", "CUT_TO_BLACK", "CUT_FROM_BLACK"}
SOFT = {"DISSOLVE", "FADE_TO_BLACK", "FADE_FROM_BLACK"}
SUP = {"SUPPORTED", "PARTIALLY_SUPPORTED"}
TOL = 0.5


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def events(ans):
    out = []
    for t in (ans or {}).get("transitions") or []:
        v = num(t.get("t_seconds"))
        if v is not None and t.get("type") not in (None, "", "CANNOT_DETERMINE"):
            out.append((v, t["type"]))
    return out


def score(A, B, key, breaches):
    res = {"label": "agent review (not a human Oracle; cf. GAP-EVAL-01)", "rubric": "RUBRIC_V2R4.md"}
    ver = {c["review_id"]: c for c in B["claims"]}
    ck = key["claims"]
    dec = [m for m in ck if m["decoy"]]
    rej = sum(ver.get(m["review_id"], {}).get("verdict") == "NOT_SUPPORTED" for m in dec)
    res["R1"] = {"decoys_rejected": f"{rej}/{len(dec)}", "status": "VALID" if rej == len(dec) else "INVALID_REVIEW"}
    real = [m for m in ck if not m["decoy"]]
    inf = [m for m in real if m["class"] == "INFERRED"]
    mea = [m for m in real if m["class"] == "MEASURED"]
    inf_ok = sum(ver.get(m["review_id"], {}).get("verdict") in SUP for m in inf)
    mea_ok = sum(ver.get(m["review_id"], {}).get("verdict") == "SUPPORTED" for m in mea)
    short = [m for m in mea if ver.get(m["review_id"], {}).get("verdict") != "SUPPORTED"]
    only_missing = short and all(ver.get(m["review_id"], {}).get("verdict") == "CANNOT_DETERMINE" and
                                 "EVIDENCE_MISSING_FROM_PACKAGE" in str(ver[m["review_id"]].get("cannot_determine_reason")) for m in short)
    r2i = inf_ok >= 0.75 * len(inf)
    r2m = "PASS" if mea_ok >= 0.90 * len(mea) else ("INCONCLUSIVE" if only_missing else "FAIL")
    res["R2"] = {"inferred": f"{inf_ok}/{len(inf)}", "R2_inf": "PASS" if r2i else "FAIL", "measured": f"{mea_ok}/{len(mea)}", "R2_mea": r2m,
                 "per_claim": [{"review_id": m["review_id"], "original_id": m["original_id"], "class": m["class"],
                                "verdict": ver.get(m["review_id"], {}).get("verdict")} for m in real],
                 "status": "FAIL" if (not r2i or r2m == "FAIL") else ("INCONCLUSIVE" if r2m == "INCONCLUSIVE" else "PASS")}
    # R3
    ans1 = {s["sample"]: s["answer"] for s in A["A1_timestamps"]}
    agree = n = 0
    for k in key["A1_timestamps"]:
        rv = ans1.get(k["sample"], {}).get("people_role")
        if rv in (None, "", "CANNOT_DETERMINE") or "|" in str(rv):
            continue
        au = k["author_role"]
        is_rev = rv in ("SEATED_INTERVIEW_SINGLE", "SPEAKER_WITH_MIC")
        n += 1
        agree += (is_rev == (au is not None)) and (au is None or rv == au)
    seq_au = key["A5_author_sequence_starts"]
    seq_rv = [v for v in (num(x) for x in A["A5_sequences"].get("sequence_start_seconds") or []) if v is not None and v > 0]
    tp_r = sum(any(abs(r - b) <= 10 for b in seq_au) for r in seq_rv)
    tp_a = sum(any(abs(r - b) <= 10 for r in seq_rv) for b in seq_au)
    p = tp_r / len(seq_rv) if seq_rv else 0
    r = tp_a / len(seq_au) if seq_au else 0
    f1 = 2 * p * r / (p + r) if p + r else 0
    role_st = "INCONCLUSIVE" if n < 10 else ("PASS" if agree / n >= 0.80 else "FAIL")
    seq_st = "PASS" if f1 >= 0.60 else "FAIL"
    res["R3"] = {"role_agreement": f"{agree}/{n}", "R3_role": role_st, "seq_f1_10s": round(f1, 3), "R3_seq": seq_st,
                 "status": "FAIL" if "FAIL" in (role_st, seq_st) else ("INCONCLUSIVE" if role_st == "INCONCLUSIVE" else "PASS")}
    # R4 / R7 / R8 (reference = segmentation v3)
    allb = [b["t"] for b in key["author_boundaries"]]
    dss = key["author_dissolves"]
    in_ds = lambda t: any(d["start"] - TOL <= t <= d["end"] + TOL for d in dss)
    ans2 = {w["window"]: w["answer"] for w in A["A2_windows"]}
    ans3 = {s["span"]: s["answer"] for s in A["A3_spans"]}
    prec_ok = prec_n = new_ok = new_n = 0
    rec_ev = rec_hit = 0
    soft_ev = soft_hit = 0
    r7_ok = r7_n = 0
    dark_ok = dark_n = r8_ok = r8_n = 0
    def rec(ev):
        nonlocal rec_ev, rec_hit, soft_ev, soft_hit
        for t, ty in ev:
            if ty in CUT:
                rec_ev += 1
                rec_hit += any(abs(t - b) <= TOL for b in allb) or in_ds(t)
            elif ty in SOFT:
                soft_ev += 1
                soft_hit += in_ds(t)
    for w in key["A2_windows"]:
        ev = events(ans2.get(w["window"]))
        if w["stratum"] in ("SEG3_CUT_V1", "SEG3_CUT_NEW"):
            hit = any(ty in CUT and abs(t - w["target"]) <= TOL for t, ty in ev)
            prec_n += 1; prec_ok += hit
            if w["stratum"] == "SEG3_CUT_NEW":
                new_n += 1; new_ok += hit
        if w["stratum"] == "SEG3_DISSOLVE":
            d = w["target_span"]
            r7_n += 1
            r7_ok += any(ty in SOFT and d["start"] - TOL <= t <= d["end"] + TOL for t, ty in ev)
        if w["stratum"] == "SEG3_DARK_NEW":
            dark_n += 1; dark_ok += any(ty in CUT and abs(t - w["target"]) <= TOL for t, ty in ev)
        if w["stratum"] == "SEG3_LIGHT":
            r8_n += 1; r8_ok += not any(ty in CUT and abs(t - w["target"]) <= TOL for t, ty in ev)
        if w["stratum"] == "RANDOM":
            rec(ev)
    a3_author_matched = a3_author_n = 0
    for s in key["A3_spans"]:
        ev = events(ans3.get(s["span"]))
        rec(ev)
        for b in s["seg3_boundaries_inside"]:
            a3_author_n += 1
            a3_author_matched += any(abs(t - b["t"]) <= TOL for t, _ in ev)
    p_st = "PASS" if prec_n and prec_ok >= 0.90 * prec_n else "FAIL"
    n_st = "INCONCLUSIVE" if new_n < 5 else ("PASS" if new_ok >= 0.80 * new_n else "FAIL")
    r_st = "INCONCLUSIVE" if rec_ev < 5 else ("PASS" if rec_hit >= 0.80 * rec_ev else "FAIL")
    d_st = "INCONCLUSIVE" if dark_n < 5 else ("PASS" if dark_ok >= 0.80 * dark_n else "FAIL")
    sts = (p_st, n_st, d_st, r_st)
    res["R4"] = {"seg3_cut_windows_confirmed": f"{prec_ok}/{prec_n}", "R4_prec": p_st, "new_cut_windows_confirmed": f"{new_ok}/{new_n}", "R4_new": n_st,
                 "dark_cut_windows_confirmed": f"{dark_ok}/{dark_n}", "R4_dark": d_st,
                 "reviewer_cut_events_matched": f"{rec_hit}/{rec_ev}", "R4_rec": r_st,
                 "info_reviewer_soft_events_matched_by_seg3_dissolves": f"{soft_hit}/{soft_ev}",
                 "info_seg3_boundaries_in_A3_matched_by_reviewer": f"{a3_author_matched}/{a3_author_n}",
                 "status": "FAIL" if "FAIL" in sts else ("INCONCLUSIVE" if "INCONCLUSIVE" in sts else "PASS")}
    if not key.get("dissolve_controls_pass", False):
        r7 = "INCONCLUSIVE"
    else:
        r7 = "INCONCLUSIVE" if r7_n < 5 else ("PASS" if r7_ok >= 0.70 * r7_n else "FAIL")
    res["R7"] = {"dissolve_windows_confirmed": f"{r7_ok}/{r7_n}", "dissolve_controls_pass": key.get("dissolve_controls_pass"), "status": r7}
    r8 = "INCONCLUSIVE" if r8_n < 5 else ("PASS" if r8_ok >= 0.80 * r8_n else "FAIL")
    res["R8"] = {"light_change_windows_without_reviewer_cut": f"{r8_ok}/{r8_n}", "status": r8}
    forb = [m["original_id"] for m in real if ver.get(m["review_id"], {}).get("forbidden_inference") not in (None, "", "NONE")]
    res["R5"] = {"flagged_real_claims": forb, "status": "PASS" if not forb else "FAIL"}
    ans4 = {c["cam"]: c["answer"] for c in A["A4_camera"]}
    agree6 = n6 = type_ag = both_mv = 0
    fam = {"ZOOM_OR_PUSH_IN": "ZOOM_OR_DOLLY_IN", "ZOOM_OR_PULL_OUT": "ZOOM_OR_DOLLY_OUT"}
    for c in key["A4_camera"]:
        rv = ans4.get(c["cam"], {}).get("movement")
        if rv in (None, "", "CANNOT_DETERMINE") or "|" in str(rv):
            continue
        n6 += 1
        au_mv, rv_mv = c["author_label"] != "STATIC", rv != "STATIC"
        agree6 += au_mv == rv_mv
        if au_mv and rv_mv:
            both_mv += 1
            type_ag += fam.get(c["author_label"], c["author_label"]) == rv
    r6 = "INCONCLUSIVE" if n6 < 10 else ("PASS" if agree6 >= 0.70 * n6 else "FAIL")
    res["R6"] = {"static_vs_moving": f"{agree6}/{n6}", "info_type_agreement": f"{type_ag}/{both_mv}", "status": r6}
    gates = ("R2", "R3", "R4", "R5", "R6", "R7", "R8")
    if res["R1"]["status"] != "VALID":
        v = "INVALID_REVIEW"
    elif any(res[g]["status"] == "FAIL" for g in gates):
        v = "FAIL"
    elif any(res[g]["status"] == "INCONCLUSIVE" for g in gates):
        v = "INCONCLUSIVE"
    else:
        v = "PASS"
    res["uncapped_gate_verdict"] = v
    if breaches and v in ("PASS", "FAIL"):
        v = "INCONCLUSIVE"
    res["protocol_breaches"] = breaches
    res["V2_verdict"] = f"{v} (agent review)"
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--sealed-key", type=Path, required=True)
    ap.add_argument("--expect-plain-sha256", required=True)
    ap.add_argument("--breach", action="append", default=[], help="protocol breach found by the protocol check (repeatable)")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    raw = subprocess.run(OPENSSL, input=a.sealed_key.read_bytes(), capture_output=True, check=True, env=dict(os.environ)).stdout
    if hashlib.sha256(raw).hexdigest() != a.expect_plain_sha256:
        raise SystemExit("oracle key hash mismatch")
    key = json.loads(raw)
    A = json.load(open(a.package / "answers/stage_A_answers.json"))
    B = json.load(open(a.package / "answers/stage_B_answers.json"))
    res = score(A, B, key, a.breach)
    a.out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(res["V2_verdict"])


if __name__ == "__main__":
    main()
