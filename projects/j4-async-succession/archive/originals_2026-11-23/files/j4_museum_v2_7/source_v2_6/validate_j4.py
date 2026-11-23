#!/usr/bin/env python3
"""Offline structural verification for J4 v2.6. Never triggers media generation."""
from pathlib import Path
import json,csv,sys
R=Path(__file__).resolve().parent
shot=json.loads((R/'j4_shots.json').read_text(encoding='utf8'))
sound=json.loads((R/'j4_sound_ir.json').read_text(encoding='utf8'))
budget=json.loads((R/'j4_budget_audit.json').read_text(encoding='utf8'))
a=shot['shots'];assert len(a)==25 and shot['duration_ms']==90000
assert all(s['id']==f'S{i+1:02}' for i,s in enumerate(a))
assert a[0]['start_ms']==0 and a[-1]['end_ms']==90000
for i,s in enumerate(a):
 assert s['start_ms']<s['end_ms'] and s['end_ms']-s['start_ms']==s['duration_ms']
 assert i==0 or s['start_ms']==a[i-1]['end_ms']
 for field in ['image_prompt','motion_prompt','sound_prompt','art_reference','in_transition','out_transition','contest_override','generation_recipe']:
  assert s[field],(s['id'],field)
 assert 'artist' in s['art_reference'] and 'work' in s['art_reference']
 if s['generation_mode']=='editorial':assert not s['generation_recipe']['billable_generation']
 else:assert s['generation_recipe']['minimum_billable_ms']==5000
assert sum(s['duration_ms'] for s in a)==90000
assert [s['id'] for s in a if s['generation_mode']=='editorial']==['S01','S18','S25']
assert len(sound['phase_families'])==6
assert {p['period_ms'] for p in sound['phase_families']}=={5000,7000,11000,13000,17000,19000}
assert all(p['forced_stop_ms']==63700 for p in sound['phase_families'])
assert any(x['kind']=='forced_global_cut' and x['at_ms']==63700 and x['preserve']==['STEM_01'] for x in sound['events'])
assert any(x['kind']=='strip_to_sine' and x['at_ms']==87000 for x in sound['events'])
assert len(sound['shot_sound_cues'])==25
assert len({s['art_reference']['work'] for s in a})==25
for i in [3,17,21,24]: assert 'founder_coat_A' in a[i-1]['props']
assert 'archive_coat_B' in a[9]['props']
assert 'SHIRT sleeve' in a[20]['image_prompt']
assert 'Shenzhen' in a[18]['image_prompt'] and 'fictional' in a[18]['contest_override']
assert budget['v2_6_S18_editorial']['contest_22_cinema_round_up']==1905
with (R/'j4_qc_matrix.csv').open(encoding='utf-8-sig',newline='') as f:
 checks=list(csv.DictReader(f))
assert checks[0]['status']=='PASS_STATIC'
assert all(r['status']=='NOT_RUN' for r in checks[1:])
print('PASS: 25 contiguous shots, 90.000s; 3 editorial shots; 25 reference methods; 6 phase-families; S18 sound cut; key prop IDs; budget scenarios; QC statuses.')
