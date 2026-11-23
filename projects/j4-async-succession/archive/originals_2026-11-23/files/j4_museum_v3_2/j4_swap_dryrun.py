#!/usr/bin/env python3
"""J4 v3.2: propose an object variant; never call an image/model service."""
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--asset',required=True)
p.add_argument('--variant',required=True,choices=['A','B'])
p.add_argument('--out',default=None)
a=p.parse_args()
db=json.loads((HERE/'j4_object_registry_v3_2.json').read_text())
item=next((v for v in db['assets'] if v['asset_id']==a.asset),None)
if item is None: p.error('Unknown asset ID')
choice=next(v for v in item['swap_variants'] if v['id']==a.variant)
proposal={'mode':'DRY_RUN_ONLY','status':'NOT_APPROVED','paid_generation':'BLOCKED',
 'asset_id':a.asset,'variant':a.variant,'description':choice['description'],
 'required_invariant':item['invariant'],'identity_class':item['identity_class'],
 'affected_shots':[v['shot'] for v in item['occurrences']],
 'camera_and_sound_review':'REQUIRED','human_G1_G2_G3_G4':'NOT_RUN',
 'new_prompt_suffix':'Original prop treatment: '+choice['description']+'. Preserve: '+item['invariant']+'. Do not copy source imagery.',
 'note':'Append only during local editorial review; never overwrite baseline Shot IR.'}
result=json.dumps(proposal,ensure_ascii=False,indent=2)+'\n'
if a.out: Path(a.out).write_text(result)
else:print(result)
