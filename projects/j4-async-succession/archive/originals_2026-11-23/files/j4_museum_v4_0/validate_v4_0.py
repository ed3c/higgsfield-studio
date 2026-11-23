#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,csv,sys,collections
R=Path(__file__).resolve().parent
spec=json.loads((R/'j4_cross_modal_ir_v4_0.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f,h in spec['baseline_sha256'].items():
 assert sha(R/'baseline'/f)==h, f'baseline hash mismatch: {f}'
shots=json.loads((R/'baseline/j4_shots_v2_9.json').read_text())['shots']
sound=json.loads((R/'baseline/j4_sound_ir_v2_8.json').read_text())
assert len(shots)==25 and sum(s['duration_ms'] for s in shots)==90000
cursor=0
for s in shots:
 assert s['start_ms']==cursor and s['end_ms']-s['start_ms']==s['duration_ms']
 assert s['start_ms']*30%1000==0 and s['end_ms']*30%1000==0
 cursor=s['end_ms']
assert cursor==90000 and sound['sample_rate_hz']==48000
assert len(sound['phase_families'])==6 and all(x['forced_stop_ms']==63700 for x in sound['phase_families'])
assert len(spec['arcs'])==3 and len(spec['conditions'])==4
assert {(x['visual'],x['audio']) for x in spec['conditions']}=={(0,0),(1,0),(0,1),(1,1)}
rows=list(csv.DictReader(open(R/'j4_factorial_conditions_v4_0.csv',encoding='utf-8-sig')))
assert len(rows)==12 and all(x['review_state']=='NOT_RUN' for x in rows)
media=list(csv.DictReader(open(R/'j4_stimulus_manifest_v4_0.csv',encoding='utf-8-sig')))
assert len(media)==15 and all(x['material_status']=='MISSING_NOT_RUN' for x in media)
for x in spec['arcs']:
 assert x['origin'] in {s['id'] for s in shots} and x['reveal'] in {s['id'] for s in shots}
alloc=list(csv.DictReader(open(R/'j4_pilot_allocation_v4_0.csv',encoding='utf-8-sig')))
assert len(alloc)==32 and collections.Counter(x['assigned_condition'] for x in alloc)=={x['id']:8 for x in spec['conditions']}
assert all(x['status']=='UNASSIGNED_NO_HUMAN' for x in alloc)
assert spec['immutable_timeline']=={'sine_start_ms':500,'local_S10_cut_ms':38600,'S18_six_phase_stop_ms':63700,'S24_new_market_ms':84000,'S25_sine_only_ms':87000,'end_ms':90000}
print('PASS_STATIC_ONLY: 25 shots / 90,000ms / 6 phases / 3 arcs x 4 conditions / 15 missing media / 32 unassigned slots')
print('NOT_RUN: real media, rights clearance, loudness comparison, human studies, artistic QA')
