#!/usr/bin/env python3
"""Non-mutating diagnostic for a proposed sonic-object treatment swap."""
import argparse,json,pathlib
p=pathlib.Path(__file__).resolve().parent
r=json.loads((p/'j4_sonic_object_registry_v3_9.json').read_text())
t=json.loads((p/'j4_recall_trials_v3_9.json').read_text())
a=argparse.ArgumentParser(description='J4 Sonic Object Swap DRY-RUN — no rendering or source edits')
a.add_argument('--family',required=True,choices=[x['id'] for x in r['families']]);a.add_argument('--variant',choices=['target','control'],default='target')
args=a.parse_args();f=next(x for x in r['families'] if x['id']==args.family)
trials=[x['id'] for x in t['trials'] if any(s in x['origin']+';'+x['reveal'] for s in f['source']+f['recall'])]
print(json.dumps({'mode':'DRY_RUN_ONLY','family_id':f['id'],'asset_id':f['asset_id'],'identity_class':f['kind'],
 'affected_shots':sorted(set(f['source']+f['recall'])),'variant':args.variant,
 'instruction':f['test_var'] if args.variant=='target' else f['negative'],
 'MUST_PRESERVE':f['invariant'],'impacted_candidate_trials':trials,
 'status':'NOT_RENDERED_NOT_APPROVED'},ensure_ascii=False,indent=2))
