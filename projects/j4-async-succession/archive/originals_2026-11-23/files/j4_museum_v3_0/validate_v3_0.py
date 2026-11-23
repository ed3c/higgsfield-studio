from pathlib import Path
import json,csv,hashlib
P=Path(__file__).parent; SRC=P
j=json.loads((P/'j4_visual_consistency_ir_v3_0.json').read_text())
base=json.loads((SRC/'baseline_j4_shots_v2_9.json').read_text())
assert j['metadata']['source_shots_sha256']==hashlib.sha256((SRC/'baseline_j4_shots_v2_9.json').read_bytes()).hexdigest()
assert j['metadata']['source_composition_sha256']==hashlib.sha256((SRC/'baseline_j4_keyframe_composition_v2_9.json').read_bytes()).hexdigest()
S={s['id']:s for s in base['shots']}
assert len(S)==25 and base['duration_ms']==90000
assert sum(s['duration_ms'] for s in S.values())==90000
assert all(s['start_ms']%100==s['end_ms']%100==0 for s in S.values())
assert [s['start_ms'] for s in base['shots']]==[0]+[s['end_ms'] for s in base['shots']][:-1]
assert base['shots'][-1]['end_ms']==90000
assert j['metadata']['no_media_generated'] and j['metadata']['paid_gate'].startswith('BLOCKED')
assert len(j['vertical_9_16'])==10 and len(j['horizontal_16_9'])==4
assert len(j['continuity_tests'])==14
V={b['shot_id']:b for b in j['vertical_9_16']};H={b['shot_id']:b for b in j['horizontal_16_9']}
assert set(H)=={'S03','S13','S22','S24'}
assert set(V)==set(sum([g['shots'] for g in j['groups']],[]))
for b in list(V.values())+list(H.values()):
 assert b['render_review_state']=='NOT_RUN_NO_RENDER'
 assert b['zones']
 for z in b['zones']:
  x,y,w,h=z['bbox'];assert 0<=x<1 and 0<=y<1 and w>0 and h>0 and x+w<=1.0000001 and y+h<=1.0000001,(b['shot_id'],z)
for e in j['continuity_tests']:
 assert e['from'] in S and e['to'] in S and e['design_review_state']=='NOT_RUN' and e['render_review_state']=='NOT_RUN_NO_MEDIA'
 if e['kind']=='adjacent':
  assert S[e['from']]['end_ms']==S[e['to']]['start_ms']==e['at_ms']
  assert e['at_frame']==e['at_ms']*30//1000
with open(P/'j4_visual_acceptance_v3_0.csv',encoding='utf-8-sig') as f:
 checks=list(csv.DictReader(f))
assert checks and all(c['status']=='NOT_RUN' for c in checks)
assert len([e for e in j['continuity_tests'] if e['kind']=='adjacent'])==7
assert len([e for e in j['continuity_tests'] if e['kind']=='nonadjacent_asset'])==7
print('PASS: baseline hash, 25 shot/90s, 10 vertical + 4 independently authored horizontal designs, 14 continuity checks,',len(checks),'unreviewed criteria, NO media generation')
