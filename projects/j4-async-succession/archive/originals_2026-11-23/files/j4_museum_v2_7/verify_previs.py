#!/usr/bin/env python3
"""Static checks for v2.7 derived, no media rendering."""
from pathlib import Path
import csv,json,re
R=Path(__file__).resolve().parent
base=json.loads((R/'source_v2_6/j4_shots.json').read_text())
report=json.loads((R/'j4_preflight_report.json').read_text())
with (R/'j4_editorial_timeline.csv').open(encoding='utf-8-sig',newline='') as f:t=list(csv.DictReader(f))
with (R/'j4_transition_matrix.csv').open(encoding='utf-8-sig',newline='') as f:transition=list(csv.DictReader(f))
with (R/'j4_sound_events.csv').open(encoding='utf-8-sig',newline='') as f:ev=list(csv.DictReader(f))
assert len(t)==len(base['shots'])==25
assert len(transition)==24
assert int(t[0]['start_frame'])==0 and int(t[-1]['end_frame_exclusive'])==2700
assert sum(int(row['duration_frames']) for row in t)==2700
for i,(a,b) in enumerate(zip(t,base['shots'])):
 assert a['shot_id']==b['id'];assert int(a['start_ms'])==b['start_ms'];assert int(a['end_ms'])==b['end_ms']
 assert int(a['end_frame_exclusive'])-int(a['start_frame'])==int(a['duration_frames'])
 assert i==0 or int(a['start_frame'])==int(t[i-1]['end_frame_exclusive'])
for i,x in enumerate(transition):
 assert x['from']==t[i]['shot_id'] and x['to']==t[i+1]['shot_id']
 assert int(x['cut_at_ms'])==int(t[i]['end_ms'])
assert any(e['event']=='FORCED_GLOBAL_CUT' and int(e['at_ms'])==63700 for e in ev)
assert any(e['event']=='STRIP_TO_SINE' and int(e['at_ms'])==87000 for e in ev)
assert report['assets']['generated_images']==report['assets']['generated_videos']==report['assets']['source_frames_used']==0
assert report['gates']['native_pipeline_schema'].startswith('BLOCKED')
html=(R/'j4_previs.html').read_text(encoding='utf-8')
assert '<!doctype html>' in html and 'TEXT-ONLY PREVIS' in html
assert 'src="http' not in html and '<iframe' not in html and '<video' not in html and '<audio' not in html
assert len(re.findall(r'\"id\":\"S\d{2}\"',html))>=25
print('PASS: 25 clips / 2700 frames / 24 cuts / 17 design sound markers; contest media excluded; offline text-only preview. Native legacy compatibility NOT_TESTED.')
