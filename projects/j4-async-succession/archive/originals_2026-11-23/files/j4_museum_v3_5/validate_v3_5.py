#!/usr/bin/env python3
"""Design-only structural check; does not approve images, rights or generation."""
import json,csv,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'j4_g2a_previs_lock_v3_5.json').read_text(encoding='utf-8'))
assert D['film']=={'shots':25,'duration_ms':90000,'frame_rate':30,'frames':2700,'s10_local_tail_cut_ms':38600,'s18_global_cycle_cut_ms':63700}
assert D['governance']['paid_generation']=='BLOCKED' and D['experiment']['status']=='NOT_RUN'
assert len(D['arcs'])==3
expect={'G2A_COAT':('S10','S21'),'G2A_PAPER':('S11','S22'),'G2A_AUTHORITY':('S18','S19')}
for a in D['arcs']:
 assert (a['a'],a['b'])==expect[a['id']]
 assert a['trial_status']=='NO_MEDIA_NOT_RUN'
 assert len(a['source_art'])==2
 assert len(a['states'])==2
 for s in (a['a'],a['b']):
  beats=sorted([x for x in a['beats'] if x['shot']==s],key=lambda x:x['local_start_frame'])
  assert beats[0]['local_start_frame']==0
  assert beats[-1]['local_end_frame']==a['timing'][s]['duration_ms']*30//1000
  assert all(beats[i]['local_end_frame']==beats[i+1]['local_start_frame'] for i in range(len(beats)-1))
 for ref in a['source_art']:
  assert ref['url'].startswith('https://') and ref['artist'] and ref['work']
A={x['id']:x for x in D['arcs']}
assert A['G2A_COAT']['states'][0]['identity']=='B' and A['G2A_COAT']['states'][1]['identity']=='A'
assert not A['G2A_COAT']['states'][0]['repair'] and A['G2A_COAT']['states'][1]['repair']
assert A['G2A_PAPER']['states'][0]['same_physical_as_S22'] is False
assert A['G2A_AUTHORITY']['states'][0]['x_centres']==A['G2A_AUTHORITY']['states'][1]['x_centres_lit']
assert A['G2A_AUTHORITY']['timing']['S18']['duration_ms']==1300
for f in ['j4_g2a_previs_board_v3_5.html','DIRECTOR_OBJECT_STATE_LOCK_v3_5.md','DIRECTOR_PROMPT_DELTAS_v3_5.md']:
 assert (R/f).stat().st_size>1000
print('PASS: 3 arcs, 6 sourced shot refs, 30fps beat coverage, 90s unchanged, all media NOT_RUN, paid generation BLOCKED')
