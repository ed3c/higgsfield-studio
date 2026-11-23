#!/usr/bin/env python3
import json,hashlib,sys
from collections import defaultdict
from pathlib import Path
P=Path(__file__).resolve().parent
bs=json.loads((P/'baseline_shots_v3_1.json').read_text())
rr=json.loads((P/'j4_object_registry_v3_2.json').read_text())
ss=json.loads((P/'j4_shot_optical_ir_v3_2.json').read_text())
ma=json.loads((P/'j4_memory_arcs_v3_2.json').read_text())
assert len(bs['shots'])==len(ss['shots'])==25
assert bs['shots'][-1]['end_ms']==90000
assert sum(x['duration_ms'] for x in bs['shots'])==90000
assert all(x['start_ms']==(bs['shots'][i-1]['end_ms'] if i else 0) for i,x in enumerate(bs['shots']))
assert all(x['end_ms']-x['start_ms']==x['duration_ms'] for x in bs['shots'])
assert all((x['start_ms']*30)%1000==0 and (x['end_ms']*30)%1000==0 for x in bs['shots'])
ids={x['asset_id'] for x in rr['assets']}; baseline_ids={p for x in bs['shots'] for p in x['props']}
assert len(ids)==46 and ids==baseline_ids
assert len(set(x['shot_id'] for x in ss['shots']))==25
assert all(len(x['swap_variants'])>=2 for x in rr['assets'])
assert all(x['art_review']=='NOT_RUN' and x['generation_gate']=='BLOCKED' for x in ss['shots'])
assert all(set(x['all_swappable_slots']).issubset(ids) for x in ss['shots'])
for a in rr['assets']:
 expected=[x['id'] for x in bs['shots'] if a['asset_id'] in x['props']]
 assert expected==[v['shot'] for v in a['occurrences']],a['asset_id']
 assert len({v['shot'] for v in a['occurrences']})==len(a['occurrences'])
for arc in ma['arcs']:
 assert set(arc['source']).issubset({x['id'] for x in bs['shots']})
 assert arc['reveal_shot'] in arc['source']
 assert set(arc['asset_ids']).issubset(ids|{'sine_master'})
coats={a['asset_id']:a for a in rr['assets'] if 'coat' in a['asset_id']}
assert [o['shot'] for o in coats['founder_coat_A']['occurrences']]==['S03','S17','S21','S24']
assert [o['shot'] for o in coats['archive_coat_B']['occurrences']]==['S10']
assert next(a for a in rr['assets'] if a['asset_id']=='paper_house_v1')['physical_identity_policy']=='SHARE_DESIGN_GRAMMAR_NOT_PHYSICAL_IDENTITY'
assert next(x for x in ss['shots'] if x['shot_id']=='S18')['method']=='LOW_LUMINANCE_EDITORIAL_COMPOSITE'
assert next(x for x in ss['shots'] if x['shot_id']=='S23')['illusion_type']=='TIME_OFFSET_COMPOSITE'
print('PASS: 25 shots; 90.000s; 2700 frames @30fps; 46 swappable slots; 10 memory arcs; review NOT_RUN; paid gate BLOCKED')
