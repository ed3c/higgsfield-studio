#!/usr/bin/env python3
"""Structural check only. Does not certify actual audio, creative quality, or rights."""
import sys, json, hashlib, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
m=json.loads((ROOT/'j4_g2b_trial_manifest_v3_8.json').read_text())
b=ROOT/'baseline'
for fn, digest in m['baseline_sha256'].items():
 p=b/fn
 assert p.exists(),f'MISSING BASELINE: {fn}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,f'BASELINE MODIFIED: {fn}'
s=json.loads((b/'j4_shots_v2_9.json').read_text())
a=json.loads((b/'j4_sound_ir_v2_8.json').read_text())
o=json.loads((b/'j4_sound_dramaturgy_overlay_v3_7.json').read_text())
shots=s['shots']; assert len(shots)==25
start=0
for i,sh in enumerate(shots):
 assert sh['id']==f'S{i+1:02d}'
 assert sh['start_ms']==start, (sh['id'],start,sh['start_ms'])
 assert sh['duration_ms']==sh['end_ms']-sh['start_ms']
 start=sh['end_ms']
assert start==90000 and s['duration_ms']==90000
assert a['duration_ms']==90000 and a['sample_rate_hz']==48000
assert len(a['stems'])==5 and len(a['phase_families'])==6
assert [f['period_ms'] for f in a['phase_families']]==[7000,11000,5000,13000,19000,17000]
assert all(f['forced_stop_ms']==63700 for f in a['phase_families'])
events=a['events']
assert any(e['kind']=='forced_global_cut' and e['at_ms']==63700 and e.get('preserve')==['STEM_01'] for e in events)
assert any(e['kind']=='deliberate_exception' and e['at_ms']==38600 for e in events)
assert any(e['kind']=='strip_to_sine' and e['at_ms']==87000 for e in events)
assert m['hard_constraints']['sine_start_ms']==500
assert len(o['shots'])==25 and len(m['trials'])==4 and len(m['media_slots'])==8
for key,trial in m['trials'].items():
 assert trial['result']=='NOT_RUN' and trial['rights_review']=='NOT_RUN'
 assert all(sh in [x['id'] for x in shots] for sh in trial['shots'])
 assert trial['length_ms']>0
 if len(trial['window_ms'])==2:
  st,en=trial['window_ms'];assert en-st==trial['length_ms']
 else:
  st1,en1,st2,en2=trial['window_ms'];assert (en1-st1)+(en2-st2)+500==trial['length_ms']
 assert len([x for x in m['media_slots'] if x['trial']==key])==2
assert m['human_gate']=='NOT_RUN' and 'NO_HIGGSFIELD' in m['hard_constraints']['authorization']
print('PASS_STATIC_DATA: 25 shots / 90s / 2700 frames / 48kHz / 5 stems / 6 phase families / 4 trials / 8 blank media slots')
print('NOT_RUN: media QA, sound listening, participant scoring, human rights review')
