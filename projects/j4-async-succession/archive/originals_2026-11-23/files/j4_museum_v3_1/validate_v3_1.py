from pathlib import Path
import json,csv,hashlib
P=Path(__file__).resolve().parent
base=P/'baseline_j4_visual_consistency_ir_v3_0.json'
shot=P/'baseline_j4_shots_v2_9.json'
man=json.loads((P/'j4_g1_manifest_v3_1.json').read_text())
a=json.loads(base.read_text());b=json.loads((P/'j4_g1_layout_candidate_v3_1.json').read_text());timeline=json.loads(shot.read_text())
assert hashlib.sha256(base.read_bytes()).hexdigest()==man['source_sha256']['v3.0_visual_consistency_ir']
assert hashlib.sha256(shot.read_bytes()).hexdigest()==man['source_sha256']['v2.9_shot_ir']
assert len(timeline['shots'])==25 and sum(x['duration_ms'] for x in timeline['shots'])==90000
assert timeline['shots'][0]['start_ms']==0 and timeline['shots'][-1]['end_ms']==90000
assert all(timeline['shots'][i]['end_ms']==timeline['shots'][i+1]['start_ms'] for i in range(24))
assert len(a['vertical_9_16'])==len(b['vertical_9_16'])==10
assert len(a['horizontal_16_9'])==len(b['horizontal_16_9'])==4
assert len(b['continuity_tests'])==14
assert man['status']=='DESIGN_CANDIDATE_NOT_APPROVED' and man['rendered_assets']==man['spent_credits']==0
assert b['metadata']['no_media_generated'] and 'BLOCKED' in b['metadata']['paid_gate']
for rec in b['vertical_9_16']+b['horizontal_16_9']:
 assert rec['render_review_state']=='NOT_RUN_NO_MEDIA'
 for z in rec['zones']:
  x,y,w,h=z['bbox']
  assert 0<=x<1 and 0<=y<1 and w>0 and h>0 and x+w<=1 and y+h<=1,(rec['shot_id'],z)
for e in b['continuity_tests']:
 assert e['design_review_state']=='NOT_RUN' and e['render_review_state']=='NOT_RUN_NO_MEDIA'
V={s['shot_id']:s for s in b['vertical_9_16']}
assert len(V)==10
assert next(x for x in V['S11']['zones'] if x['name']=='paper_house_hint')['priority']==2
assert (next(x for x in V['S22']['zones'] if x['name']=='fragile_bridge')['bbox'][2] > .23)
assert (next(x for x in V['S24']['zones'] if x['name']=='coat_A')['bbox'][2] > .36)
for fn,count in [('j4_g1_review_matrix.csv',40),('j4_g1_continuity_review.csv',14)]:
 with (P/fn).open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
 assert len(r)==count
 assert all(x.get('status','NOT_RUN')=='NOT_RUN' if 'status' in x else x.get('evidence_state')=='NOT_RUN_NO_MEDIA' for x in r)
with (P/'j4_g1_30fps_action_beats.csv').open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
for sid in V:
 arr=[x for x in r if x['shot_id']==sid]
 assert arr and int(arr[0]['local_frame_in'])==0
 assert int(arr[-1]['local_frame_out_exclusive'])==next(x for x in timeline['shots'] if x['id']==sid)['duration_ms']*30//1000
 assert all(int(arr[i]['local_frame_out_exclusive'])==int(arr[i+1]['local_frame_in']) for i in range(len(arr)-1))
print('PASS: immutable provenance, 25-shot/90s timeline, 10 vertical candidates + 4 independent horizontal baselines, 14 NOT_RUN relations, 40 NOT_RUN criteria, frame beats, zero media/spend')
