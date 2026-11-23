#!/usr/bin/env python3
import argparse,csv,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser(description='QA expected 15 video stimuli; missing media BLOCKS promotion')
p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
p.add_argument('--json-out',type=Path)
a=p.parse_args();root=a.root;manifest=Path(__file__).resolve().parent/'j4_stimulus_manifest_v4_0.csv'
rows=list(csv.DictReader(open(manifest,encoding='utf-8-sig')))
result={'gate':'BLOCKED','items':[],'note':'Structural media QA only. Exposure/audio-content/rights equality require manual evidence.'}
for r in rows:
 item={'media_id':r['media_id'],'path':str(root/r['expected_file']),'checks':{}}
 f=root/r['expected_file']
 if not f.is_file():item['status']='MISSING';result['items'].append(item);continue
 try:
  ff=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)],text=True))
  vs=[s for s in ff.get('streams',[]) if s.get('codec_type')=='video']; au=[s for s in ff.get('streams',[]) if s.get('codec_type')=='audio']
  if not vs or not au:raise ValueError('Both video and audio streams required')
  fps=vs[0].get('avg_frame_rate') or vs[0].get('r_frame_rate')
  num,den=map(int,fps.split('/'))
  dur=float(ff['format']['duration'])*1000
  item['checks']={'fps':num/den,'duration_ms':dur,'width':vs[0].get('width'),'height':vs[0].get('height'),'sample_rate':int(au[0].get('sample_rate',0)),'channels':au[0].get('channels')}
  ok=abs(num/den-30)<0.001 and abs(dur-int(r['duration_ms']))<=1000/30+10 and int(au[0].get('sample_rate',0))==48000
  item['status']='STRUCTURE_PASS_NEEDS_MANUAL_MIX_RIGHTS' if ok else 'STRUCTURE_FAIL'
 except Exception as e:item['status']='ERROR';item['error']=str(e)
 result['items'].append(item)
counts={x:sum(i['status']==x for i in result['items']) for x in {i['status'] for i in result['items']}}
result['counts']=counts
if all(i['status']=='STRUCTURE_PASS_NEEDS_MANUAL_MIX_RIGHTS' for i in result['items']):result['gate']='STRUCTURE_PASS_MANUAL_GATES_NOT_RUN'
if a.json_out:a.json_out.write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps({'gate':result['gate'],'counts':counts,'expected':len(rows)},ensure_ascii=False))
sys.exit(0 if result['gate']=='STRUCTURE_PASS_MANUAL_GATES_NOT_RUN' else 2)
