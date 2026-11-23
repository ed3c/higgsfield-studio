#!/usr/bin/env python3
"""Fail-closed media preflight. Tests don't establish copyright or psychological validity.
Run only on locally cleared stimulus files. No generation or network requests.
"""
from pathlib import Path
import csv,hashlib,json,subprocess,sys,math
P=Path(__file__).resolve().parent

def hashf(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def ffprobe(p):
 r=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,avg_frame_rate,nb_frames,duration','-of','json',str(p)],capture_output=True,text=True)
 if r.returncode:raise ValueError(r.stderr[:400])
 s=json.loads(r.stdout)['streams'][0];n,d=(int(v) for v in s['avg_frame_rate'].split('/'))
 s['fps']=n/d
 return s

def check_pair(main,ctrl,arc):
 import cv2,numpy as np
 m=cv2.VideoCapture(str(main));c=cv2.VideoCapture(str(ctrl));
 x,y,w,h=arc['manipulation']['target_roi_norm_xywh']; start,end=arc['manipulation']['frame_range_half_open']
 n=0; outside_delta=[]; target_delta=[];luma_deltas=[]
 while True:
  ok1,a=m.read();ok2,b=c.read()
  if not ok1 and not ok2:break
  if ok1!=ok2:raise ValueError('B frames mismatch')
  H,W=a.shape[:2];mask=np.ones((H,W),dtype=bool)
  # registered target mask, with narrow 2% buffer for compression falloff
  pad=.02
  x1=max(0,int((x-pad)*W));y1=max(0,int((y-pad)*H));x2=min(W,int((x+w+pad)*W));y2=min(H,int((y+h+pad)*H))
  if start<=n<end: mask[y1:y2,x1:x2]=False
  delta=np.abs(a.astype(np.float32)-b.astype(np.float32)).mean(axis=2)/255.0
  outside_delta.append(float(delta[mask].mean()))
  target_delta.append(float(delta[~mask].mean()) if (~mask).any() else 0.0)
  # comparable exposure outside target region; whole-frame brightness may legitimately differ in authority experiment
  luma_deltas.append(float(abs(a[mask].mean()-b[mask].mean())/255))
  n+=1
 m.release();c.release()
 if n==0:raise ValueError('no video frames')
 # Tolerances are candidate engineering guards; must be manually confirmed for codec type.
 return {'frames_compared':n,'mean_normalized_difference_outside_mask':sum(outside_delta)/n,'mean_normalized_difference_within_target':sum(target_delta)/n,'mean_luma_shift_outside_mask':sum(luma_deltas)/n,
 'machine_guard_outside_roi': 'PASS' if sum(outside_delta)/n<=.015 else 'NEEDS_REVIEW',
 'machine_guard_luma':'PASS' if sum(luma_deltas)/n<=.015 else 'NEEDS_REVIEW',
 'warning':'PASS is not human salience or artistic approval; moving light pools may fail confound review despite low pixel difference.'}

def main():
 with (P/'j4_stimulus_manifest_v3_6.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 prereg=json.loads((P/'j4_g2a_preregistration_v3_6.json').read_text())
 paths={z['stimulus_id']:P/z['media_relative_path'] for z in rows}
 missing=[str(p.relative_to(P)) for p in paths.values() if not p.is_file()]
 if missing:
  print('BLOCKED_NO_REAL_MEDIA: missing',len(missing),'of',len(paths),'expected clips. No video quality conclusion.')
  for p in missing: print(' -',p)
  return 2
 checks=[]
 for row in rows:
  p=paths[row['stimulus_id']];s=ffprobe(p);valid=(s['width']==int(row['width_expected']) and s['height']==int(row['height_expected']) and abs(s['fps']-float(row['fps_expected']))<.02)
  vframes=s.get('nb_frames');n=int(vframes) if vframes not in ('N/A',None) else None
  if n is None:
   import cv2
   cap=cv2.VideoCapture(str(p)); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.release()
  valid=valid and (n==int(row['frames_expected']))
  streamcheck=subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',str(p)],capture_output=True,text=True)
  silent=(streamcheck.returncode==0 and not streamcheck.stdout.strip())
  valid=valid and silent
  # picture-only pilot requires no audible guidance; videos may contain audio tracks but should be stripped before use
  checks.append({'stimulus':row['stimulus_id'],'path':row['media_relative_path'],'hash':hashf(p),'resolution_fps_frames_no_audio':'PASS' if valid else 'FAIL','frames_observed':n,'frames_expected':int(row['frames_expected'])})
 for arc in prereg['arcs']:
  i=arc['id'];checks.append({'arc':i,'B_pixel_control_comparison':check_pair(paths[f'{i}_B_main'],paths[f'{i}_B_control'],arc)})
 print(json.dumps({'status':'MEDIA_PREFLIGHT_COMPLETED_NOT_HUMAN_SIGNOFF','checks':checks},ensure_ascii=False,indent=2))
 if any(x.get('resolution_fps_frames_no_audio')=='FAIL' for x in checks):return 3
 if any('B_pixel_control_comparison' in x and (x['B_pixel_control_comparison']['machine_guard_outside_roi']!='PASS' or x['B_pixel_control_comparison']['machine_guard_luma']!='PASS') for x in checks):return 3
 return 0
if __name__=='__main__':sys.exit(main())
