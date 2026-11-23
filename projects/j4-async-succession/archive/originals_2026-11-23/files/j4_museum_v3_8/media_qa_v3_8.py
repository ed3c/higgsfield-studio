#!/usr/bin/env python3
"""Inspect user-supplied A/B masters; no rendering or generation. Nonzero if missing/invalid."""
import json,sys,pathlib,subprocess,statistics
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'j4_g2b_trial_manifest_v3_8.json').read_text())
missing=[x['id'] for x in m['media_slots'] if not (root/x['path']).is_file()]
if missing:
 print('BLOCKED_NO_REAL_MEDIA: '+', '.join(missing));print('Do not score sound quality or psychological effect from an empty slot.');sys.exit(2)
def run(cmd):
 p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise RuntimeError(p.stderr[-1500:])
 return p.stdout,p.stderr
outputs=[];failed=[]
for x in m['media_slots']:
 p=root/x['path']
 try:
  stdout,_=run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)])
  meta=json.loads(stdout)
  tracks=meta.get('streams',[]);audio=[z for z in tracks if z.get('codec_type')=='audio'];video=[z for z in tracks if z.get('codec_type')=='video']
  if not audio:raise ValueError('audio stream missing')
  sr=int(audio[0].get('sample_rate',0));channels=int(audio[0].get('channels',0))
  dur=float(meta['format']['duration']);target=x['expected_duration_ms']/1000
  if sr!=48000:failed.append(f"{x['id']} sample_rate {sr} !=48000")
  if channels!=2:failed.append(f"{x['id']} channels {channels} !=2")
  if abs(dur-target)>0.034:failed.append(f"{x['id']} duration {dur:.3f} target {target:.3f}")
  if x['type']=='audiovisual' and not video:failed.append(f"{x['id']} needs video for audiovisual object recall")
  if video:
   raw=video[0].get('avg_frame_rate','0/1')
   n,d=map(int,raw.split('/'))
   fps=n/d if d else 0
   if abs(fps-30)>0.01: failed.append(f"{x['id']} frame_rate {fps:.3f} !=30")
  # loudnorm analysis prints source measurements to stderr; does NOT change source file.
  _,stderr=run(['ffmpeg','-nostdin','-hide_banner','-i',str(p),'-vn','-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-'])
  tail=stderr.rfind('{');meas=json.loads(stderr[tail:stderr.find('}',tail)+1]) if tail>=0 else {}
  info={'id':x['id'],'duration_s':round(dur,3),'rate_hz':sr,'channels':channels,'video':bool(video),'input_i_lufs':meas.get('input_i'),'input_tp_dbtp':meas.get('input_tp'),'input_lra':meas.get('input_lra')}
  outputs.append(info)
 except Exception as ex:failed.append(f"{x['id']}: {ex}")
for key in m['trials']:
 items=[z for z in outputs if z['id'] in [key+'_T',key+'_C']]
 if len(items)==2:
  vals=[]
  for row in items:
   try: vals.append(float(row['input_i_lufs']))
   except: vals.append(None)
  if None not in vals and key in ('A','B','D') and abs(vals[0]-vals[1])>1.0:
   failed.append(f'{key} integrated loudness difference {abs(vals[0]-vals[1]):.2f} LUFS > 1.0 LU (review gain confound)')
print(json.dumps({'media_probe_results':outputs,'problems':failed,'status':'NEEDS_REVIEW' if failed else 'TECHNICAL_MEDIA_PROBE_PASS_NOT_ARTISTIC_QC'},ensure_ascii=False,indent=2))
print('Manual check required: semantic clarity, time-dependent masking, spatial location, audio-phase continuity, real-video rights and visual confounds.')
sys.exit(1 if failed else 0)
