from pathlib import Path
import json,csv,hashlib,sys
DIR=Path(__file__).resolve().parent
base=DIR
B=json.loads((DIR/'j4_keyframe_composition_v2_9.json').read_text())
X=json.loads((DIR/'j4_shots_v2_9.json').read_text())
baseX=json.loads((base/'baseline_j4_shots_v2_8.json').read_text())
baseS=base/'baseline_j4_sound_ir_v2_8.json'
assert hashlib.sha256((base/'baseline_j4_shots_v2_8.json').read_bytes()).hexdigest()==B['metadata']['baseline_shots_sha256']
assert hashlib.sha256(baseS.read_bytes()).hexdigest()==B['metadata']['baseline_sound_sha256']
assert len(X['shots'])==len(baseX['shots'])==25
assert X['duration_ms']==90000
assert [(s['id'],s['start_ms'],s['end_ms']) for s in X['shots']]==[(s['id'],s['start_ms'],s['end_ms']) for s in baseX['shots']]
assert X['shots'][-1]['end_ms']==90000 and X['shots'][17]['start_ms']==63700
assert all(s['image_prompt']==b['image_prompt'] and s['motion_prompt']==b['motion_prompt'] and s['sound_prompt']==b['sound_prompt'] for s,b in zip(X['shots'],baseX['shots']))
assert all(s['review_state']==b['review_state'] for s,b in zip(X['shots'],baseX['shots']))
assert len(B['boards'])==4 and {b['shot_id'] for b in B['boards']}==set(B['metadata']['focus_shots'])
for board in B['boards']:
 sh=next(s for s in X['shots'] if s['id']==board['shot_id'])
 assert board['time_ms']==[sh['start_ms'],sh['end_ms']]
 assert len(board['zones'])>=4
 assert any(z['priority']==1 and z['required_at_first_frame'] for z in board['zones'])
 for z in board['zones']:
  x,y,w,h=z['bbox']
  assert 0<=x<=1 and 0<=y<=1 and w>0 and h>0 and x+w<=1.000001 and y+h<=1.000001,(board['shot_id'],z)
  if z['min_width_px_on_1080'] is not None:assert w*1080>=z['min_width_px_on_1080'],(board['shot_id'],z['name'])
 for z in board['negative_space']:
  x,y,w,h=z['bbox'];assert x+w<=1.000001 and y+h<=1.000001
assert X['governance']['v2_9_generation_allowed'] is False
assert 'no_paid_generation_without' in X['governance']
with (DIR/'j4_composition_acceptance.csv').open() as f:
 checks=list(csv.DictReader(f))
assert len(checks)>=40 and all(r['status']=='NOT_RUN_NO_RENDER' and not r['reviewer'] for r in checks)
with (DIR/'j4_asset_lock_registry.csv').open() as f:
 assets=list(csv.DictReader(f))
assert len(assets)>=10 and all(r['status']=='DESIGN_ONLY' for r in assets)
print(f'PASS: 25 shots / 90000 ms unchanged; 4 boards; {len(checks)} unscored acceptance checks; {len(assets)} asset locks; no generation approval')
