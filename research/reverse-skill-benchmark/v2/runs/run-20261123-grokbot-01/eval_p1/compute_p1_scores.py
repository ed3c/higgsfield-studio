#!/usr/bin/env python3
"""Spec §7 aggregation. Usage: compute_p1_scores.py ratings_R1.csv ratings_R2.csv KEY.json > result.json
KEY is the sealed blind_key.json; run only AFTER both sheets are locked (hash them first)."""
import csv,json,sys,statistics as st
W={"composition":.25,"perspective":.20,"lighting":.15,"palette":.10,"material":.15,"artifact_control":.15}
r1,r2,keyf=sys.argv[1:4]
key={k['blind_id']:k for k in json.load(open(keyf))['map']}
def load(f):
    d={}
    for row in csv.DictReader(open(f)):
        d.setdefault(row['blind_image_id'],{})[row['criterion']]=(float(row['score_0_to_5']),row['hard_fail'].strip().lower()=='yes')
    return d
R={'R1':load(r1),'R2':load(r2)}
img={}; adj=[]
for b in key:
    per={}
    for r in R:
        sc=R[r][b]; assert set(sc)==set(W),(r,b)
        per[r]=sum(W[c]*sc[c][0] for c in W)
        for c in W:
            if r=='R1' and abs(R['R1'][b][c][0]-R['R2'][b][c][0])>2: adj.append({"blind_id":b,"criterion":c,"R1":R['R1'][b][c][0],"R2":R['R2'][b][c][0]})
    hf=any(v[1] for r in R for v in R[r][b].values())
    img[b]={**{k:key[b][k] for k in('case_id','skill_id','replicate')},"R1":round(per['R1'],3),"R2":round(per['R2'],3),"mean":round((per['R1']+per['R2'])/2,3),"hard_fail_any":hf}
skills=sorted({v['skill_id'] for v in img.values()}); cases=sorted({v['case_id'] for v in img.values()})
table={}
for s in skills:
    pc={c:st.mean([v['mean'] for v in img.values() if v['skill_id']==s and v['case_id']==c]) for c in cases}
    n={c:sum(1 for v in img.values() if v['skill_id']==s and v['case_id']==c) for c in cases}
    table[s]={"per_case":{c:round(pc[c],3) for c in cases},"replicates_per_case":n,"mean_over_cases":round(st.mean(pc.values()),3),
      "range_over_cases":round(max(pc.values())-min(pc.values()),3),"hard_fail_count":sum(1 for v in img.values() if v['skill_id']==s and v['hard_fail_any'])}
non=sorted([s for s in skills if s!='caph'],key=lambda s:-table[s]['mean_over_cases'])
gap=table[non[0]]['mean_over_cases']-table[non[1]]['mean_over_cases'] if len(non)>1 else None
cases_won=sum(1 for c in cases if table[non[0]]['per_case'][c]>table[non[1]]['per_case'][c])
decision={"candidate_B":non[0] if gap is not None and gap>=0.25 and cases_won>=2 else "INCONCLUSIVE",
  "rule":"leading non-Caph needs mean gap >=0.25 and to lead in >=2 of 3 cases; else INCONCLUSIVE","gap":round(gap,3) if gap is not None else None,"cases_led":cases_won,"status":"PROVISIONAL (GAP-P1-01: C03/unimage single replicate)"}
json.dump({"per_image":img,"per_skill":table,"adjudication_required":adj,"p2_candidate_B":decision},sys.stdout,indent=1)
