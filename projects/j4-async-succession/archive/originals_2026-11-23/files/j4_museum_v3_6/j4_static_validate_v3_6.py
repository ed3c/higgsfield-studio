#!/usr/bin/env python3
"""Static preflight for J4 v3.6. Never writes canonical project sources."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,math
P=Path(__file__).resolve().parent

def load_json(f):return json.loads((P/f).read_text(encoding='utf-8'))
def rows(f):
 with (P/f).open(newline='',encoding='utf-8-sig') as h:return list(csv.DictReader(h))
def hashf(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def req(b,msg):
 if not b: raise AssertionError(msg)

def run():
 x=load_json('j4_g2a_preregistration_v3_6.json'); parent=P/x['source']['path']
 req(parent.exists(),'parent missing')
 req(hashf(parent)==x['source']['sha256'],'parent modified')
 req(x['film']['shots']==25 and x['film']['duration_ms']==90000 and x['film']['frames']==2700,'film changed')
 req(x['film']['s18_global_cycle_cut_ms']==63700,'S18 changed')
 req(len(x['arcs'])==3,'wrong arcs')
 manifest=rows('j4_stimulus_manifest_v3_6.csv')
 req(len(manifest)==9,'expected 9 unique stimulus slots')
 qs=rows('j4_blind_questions_v3_6.csv');req(len(qs)==6,'expected six neutral questions')
 audit=rows('j4_confound_audit_v3_6.csv');req(len(audit)==54,'expected 54 pending confound rows')
 req(all(z['status']=='NOT_RUN' and not z['evidence_path'] for z in audit),'audit prematurely marked complete')
 slots=rows('j4_allocation_slots_v3_6.csv');req(len(slots)==36,'36 planned slots')
 groups=Counter(z['condition'] for z in slots);req(groups=={'main':18,'control':18},'unbalanced arm slots')
 counts=Counter((z['condition'],z['order_1'],z['order_2'],z['order_3']) for z in slots)
 req(len(counts)==12 and set(counts.values())=={3},'order permutations imbalance')
 req(all(z['allocation_status']=='UNASSIGNED' and not z['participant_code'] for z in slots),'not anonymous unassigned slots')
 for a in x['arcs']:
  id=a['id']; aa=[z for z in manifest if z['arc_id']==id]
  req(len(aa)==3 and {(z['role'],z['condition']) for z in aa}=={('A','shared'),('B','main'),('B','control')},'bad stimulus slots '+id)
  bmain=next(z for z in aa if z['condition']=='main');bctrl=next(z for z in aa if z['condition']=='control')
  req(bmain['frames_expected']==bctrl['frames_expected'] and bmain['duration_ms']==bctrl['duration_ms'], 'B timing mismatch '+id)
  req(all(z['status']=='MISSING_MEDIA' and not z['sha256_actual'] for z in aa),'unverified media '+id)
  fx=a['manipulation']['frame_range_half_open'];req(int(fx[1])<=int(bmain['frames_expected']),'ROI frame range overflow '+id)
  rr=a['manipulation']['target_roi_norm_xywh'];req(len(rr)==4 and 0<=rr[0]<=1 and 0<=rr[1]<=1 and rr[2]>0 and rr[3]>0 and rr[0]+rr[2]<=1 and rr[1]+rr[3]<=1,'bad ROI '+id)
  req(len(a['source_art'])==2 and all(z['url'].startswith('https://') for z in a['source_art']),'source refs missing '+id)
 req(x['gates']['Higgsfield_paid_generation']=='BLOCKED' and x['scope_guard']['results_recorded']==0,'permission/result mismatch')
 print('PASS_STATIC: 25 shots/90s/2700 frames; 3 arcs; 9 media slots missing; 54 audit checks NOT_RUN; 36 unassigned balanced slots; generation BLOCKED')
if __name__=='__main__':run()
