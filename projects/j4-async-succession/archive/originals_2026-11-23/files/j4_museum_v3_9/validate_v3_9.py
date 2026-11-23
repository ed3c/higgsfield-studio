#!/usr/bin/env python3
import csv,hashlib,json,sys
from pathlib import Path
p=Path(__file__).resolve().parent
reg=json.loads((p/'j4_sonic_object_registry_v3_9.json').read_text())
tr=json.loads((p/'j4_recall_trials_v3_9.json').read_text())
shots=json.loads((p/'baseline'/'j4_shots_v2_9.json').read_text())['shots']
sound=json.loads((p/'baseline'/'j4_sound_ir_v2_8.json').read_text())
assert len(shots)==25 and sum(s['duration_ms'] for s in shots)==90000
assert all(shots[i]['end_ms']==shots[i+1]['start_ms'] for i in range(24))
assert reg['immutable_events']=={'sine_start_ms':500,'local_pitched_tail_cut_ms':38600,'six_family_forced_stop_ms':63700,'new_market_memory_ms':84000,'sine_only_ms':87000,'end_ms':90000}
assert len(sound['phase_families'])==6 and all(f['forced_stop_ms']==63700 for f in sound['phase_families'])
assert len(reg['families'])==7 and len(tr['trials'])==3
ids={f['id'] for f in reg['families']}; aset={a['asset_id'] for a in json.loads((p/'baseline'/'j4_object_registry_v3_2.json').read_text())['assets']}
assert all(f['asset_id'] in aset for f in reg['families'] if f['asset_id'])
sl={s['id']:s for s in shots}
rows=list(csv.DictReader((p/'j4_sound_object_cues_v3_9.csv').open(encoding='utf-8-sig')))
assert len(rows)==reg['event_count']
assert len({r['event_id'] for r in rows})==len(rows)
for r in rows:
 a,b=int(r['global_start_ms']),int(r['global_end_ms'])
 assert a<=b and sl[r['shot_id']]['start_ms']<=a<=b<=sl[r['shot_id']]['end_ms']
 assert int(r['audio_start_sample_48k'])==a*48
 assert int(r['audio_end_sample_48k'])==b*48
 assert r['family_id'] in ids
 assert r['media_status']=='NOT_RENDERED' and r['creative_gate']=='PENDING'
assert next(r for r in rows if r['event_id']=='GLOBAL_18')['global_start_ms']=='63700'
assert next(r for r in rows if r['event_id']=='SINE_ONLY_25')['global_start_ms']=='87000'
assert len({x['id'] for x in tr['trials']})==3
for name,sha in reg['baseline_sha256'].items():
 assert hashlib.sha256((p/'baseline'/name).read_bytes()).hexdigest()==sha,(name,'hash mismatch')
assert reg['status'].startswith('CANDIDATE_') and tr['stimulus_status']=='BLOCKED_NO_REAL_MEDIA'
print(f'PASS: 25 shots / 90000 ms / {len(reg["families"])} sonic families / {len(rows)} cue events / 3 preregistered trials / immutable six-phase stop @63700 / baseline SHA256 unchanged / NO_MEDIA')
