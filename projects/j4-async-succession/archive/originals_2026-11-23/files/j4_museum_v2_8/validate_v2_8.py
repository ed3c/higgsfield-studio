#!/usr/bin/env python3
from pathlib import Path
import json,csv,hashlib
r=Path(__file__).resolve().parent
src=(r/'source_v2_6') if (r/'source_v2_6'/'j4_shots.json').exists() else Path('/mnt/data/j4_museum_v2_6')
a=json.loads((r/'j4_shots_v2_8.json').read_text()); b=json.loads((src/'j4_shots.json').read_text()); snd=json.loads((r/'j4_sound_ir_v2_8.json').read_text());base_snd=json.loads((src/'j4_sound_ir.json').read_text())
shots=a['shots']; orig=b['shots']; assert len(shots)==25
assert a['duration_ms']==90000 and sum(s['duration_ms'] for s in shots)==90000
for i,s in enumerate(shots):
 assert s['id']==f'S{i+1:02}'
 assert s['start_ms']==(shots[i-1]['end_ms'] if i else 0)
 assert s['end_ms']-s['start_ms']==s['duration_ms']
 assert s['start_ms']*30%1000==0 and s['end_ms']*30%1000==0
assert shots[-1]['end_ms']==90000
changed={s['id'] for s,o in zip(shots,orig) if s['motion_prompt']!=o['motion_prompt'] or s['sound_prompt']!=o['sound_prompt']}
assert changed=={'S10','S18','S22','S24'},changed
assert all(s['image_prompt']==o['image_prompt'] for s,o in zip(shots,orig) if s['id']!='S24')
assert shots[23]['image_prompt'] != orig[23]['image_prompt'] and 'about to land' in shots[23]['image_prompt']
assert any(e['kind']=='deliberate_exception' and e['at_ms']==38600 for e in snd['events'])
assert any(e['kind']=='forced_global_cut' and e['at_ms']==63700 for e in snd['events'])
assert not any(e['kind']=='deliberate_exception' and e['at_ms']==35500 for e in snd['events'])
for e in base_snd['phase_families']:
 r1=next(x for x in snd['phase_families'] if x['id']==e['id']); assert r1==e
with (r/'j4_acceptance_matrix.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
assert len(rows)==25 and [r['shot_id'] for r in rows]==[s['id'] for s in shots]
for row in rows:
 assert row['overall_status']=='NOT_RUN'
 assert row['reviewer']=='' and row['evidence_path']==''
 assert all(row['status_'+axis]=='NOT_RUN' and row['score_'+axis]=='' for axis in ['narrative','first_frame','motion_hierarchy','sound_timing','transition','physical_ip'])
assert 'one soft low-luminance reveal' in shots[17]['motion_prompt']
assert 'FIRST FRAME' in shots[21]['motion_prompt'] and 'FIRST FRAME' in shots[23]['motion_prompt']
assert '38.600s' in shots[9]['motion_prompt']
print('PASS: 25 shots, 2700 frames, 90s, 24 cuts, fixed S10 only-local audio, preserved S18 global stop, 4 shot revisions (S24 image consistency included), all 25 human QC NOT_RUN')
