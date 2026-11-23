from pathlib import Path
import json,csv
root=Path(__file__).resolve().parent
m=json.loads((root/'j4_g2a_trial_manifest_v3_4.json').read_text())
assert len(m['trials'])==3
assert m['media_status']=='ALL_MEDIA_MISSING' and m['review_state']=='NOT_RUN'
assert [(t['a'],t['b']) for t in m['trials']]==[('S10','S21'),('S11','S22'),('S18','S19')]
assert [(t['a_media']['duration_ms'],t['b_media']['duration_ms']) for t in m['trials']]==[(3500,4000),(4000,3000),(1300,4000)]
assert all(t['a_media']['status']==t['b_media']['status']=='MISSING_REAL_STIMULUS' for t in m['trials'])
assert all(t['review_state']=='NOT_RUN' for t in m['trials'])
with open(root/'j4_g2a_art_crosswalk.csv',encoding='utf-8-sig') as f:
 rows=list(csv.DictReader(f))
assert len(rows)==6 and all(r['reference_url'].startswith('https://') for r in rows)
assert len(json.loads((root/'g2a_observation_schema.json').read_text())['properties'])>=4
h=(root/'j4_g2a_viewer_lab_v3_4.html').read_text()
assert 'LOCAL_USER_SELECTED_MEDIA' in h and 'NOT_RUN' in h and 'URL.createObjectURL' in h
print('PASS v3.4: 3 arcs / 6 shot references / correct durations / media missing / no fabricated viewer results')
