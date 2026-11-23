from pathlib import Path
import json,csv,hashlib
root=Path(__file__).resolve().parent
d=json.loads((root/'j4_sound_dramaturgy_overlay_v3_7.json').read_text())
shots=json.loads((root/'baseline/j4_shots_v2_9.json').read_text())['shots']
sound=json.loads((root/'baseline/j4_sound_ir_v2_8.json').read_text())
assert len(shots)==25==len(d['shots'])
assert [s['id'] for s in shots]==[s['shot_id'] for s in d['shots']]
assert shots[0]['start_ms']==0 and shots[-1]['end_ms']==90000
assert all(x['end_ms']==y['start_ms'] for x,y in zip(shots,shots[1:]))
assert all(s['start_ms']==m['start_ms'] and s['end_ms']==m['end_ms'] for s,m in zip(shots,d['shots']))
assert all(p['forced_stop_ms']==63700 for p in sound['phase_families']) and len(sound['phase_families'])==6
assert [p['period_ms'] for p in sound['phase_families']]==[7000,11000,5000,13000,19000,17000]
assert d['fixed_timeline']['global_stop_ms']==63700 and d['fixed_timeline']['local_s10_event_ms']==38600
assert len(set(s['shot_id'] for s in d['shots']))==25
assert all(s['human_audio_qc']=='NOT_RUN' and s['generation_action']=='NONE' for s in d['shots'])
assert d['gates']['higgsfield_authorization']=='BLOCKED'
for path,key in [('j4_shots_v2_9.json','shot_ir_sha256'),('j4_sound_ir_v2_8.json','sound_ir_sha256')]:
 p=root/'baseline'/path
 assert hashlib.sha256(p.read_bytes()).hexdigest()==d['baseline'][key]
with (root/'j4_sonic_recall_arcs_v3_7.csv').open() as f:
 assert len(list(csv.DictReader(f)))==8
print('PASS: 25 shots, 90s, 6 phases, 8 sonic arcs, no generation, original baseline checksum.')
