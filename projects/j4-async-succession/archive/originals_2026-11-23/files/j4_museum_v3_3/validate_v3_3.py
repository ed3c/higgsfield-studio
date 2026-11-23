from pathlib import Path
import json,csv,hashlib
p=Path(__file__).parent
a=json.loads((p/'j4_illusion_ir_v3_3.json').read_text())
r=a['shots']; assert len(r)==25 and [x['shot_id'] for x in r]==[f'S{i:02d}' for i in range(1,26)]
assert all(x['source_url'].startswith('https://') and x['reference_work'] and x['source_mechanism'] and x['prompt_delta_en'] for x in r)
assert all(x['effect_status']=='DESIGN_ONLY' and x['viewer_test']=='NOT_RUN' and x['rights_review']=='NOT_RUN' for x in r)
assert {x['category'] for x in r}=={'PERCEPTUAL','TEMPORAL_AUDIOVISUAL','NARRATIVE_RECONTEXT'}
b=json.loads((p/'j4_46asset_illusion_dependencies_v3_3.json').read_text())['assets']; assert len(b)==46 and all(x['art_illusion_dependencies'] for x in b)
c=json.loads((p/'j4_10memory_arc_evidence_v3_3.json').read_text())['arcs']; assert len(c)==10 and all(x['illusion_references'] for x in c)
with (p/'j4_g2_art_illusion_qc_v3_3.csv').open(encoding='utf-8-sig') as f:rr=list(csv.DictReader(f));assert len(rr)==125 and all(x['status']=='NOT_RUN' for x in rr)
meta=a['metadata']; assert meta['generation_gate']=='BLOCKED' and meta['constraints']['total_ms']==90000 and meta['constraints']['s18_cut_ms']==63700
print('PASS: 25/25 artwork mappings; 46/46 asset links; 10/10 arcs; 125/125 NOT_RUN; 90s unchanged; generation blocked')
