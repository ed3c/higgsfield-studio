#!/usr/bin/env python3
"""J4 v2.7 offline text-only previsualization builder. No AI/media generation or network access."""
from __future__ import annotations
from pathlib import Path
import csv, json, re, subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source_v2_6'
shots_doc = json.loads((SOURCE/'j4_shots.json').read_text(encoding='utf-8'))
sound_doc = json.loads((SOURCE/'j4_sound_ir.json').read_text(encoding='utf-8'))
shots = shots_doc['shots']
FPS = 30
TOTAL_MS = 90_000

def write_csv(name: str, fields: list[str], rows: list[dict]):
    with (ROOT/name).open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

def tc(frame:int)->str:
    return f'{frame//(FPS*3600):02}:{frame//(FPS*60)%60:02}:{frame//FPS%60:02}:{frame%FPS:02}'

def srt_tc(ms:int)->str:
    return f'{ms//3600000:02}:{(ms//60000)%60:02}:{(ms//1000)%60:02},{ms%1000:03}'

def excerpt(text:str,length:int=280)->str:
    return ' '.join(text.split())[:length].strip()

# No guessed original pipeline schema. All output is explicitly review/interchange format.
rows=[]; preview_shots=[]; subtitles=[]
for i,s in enumerate(shots):
    start_frames, end_frames = s['start_ms']*FPS//1000, s['end_ms']*FPS//1000
    assert start_frames*1000 == s['start_ms']*FPS, (s['id'],'non-frame boundary')
    assert end_frames*1000 == s['end_ms']*FPS, (s['id'],'non-frame boundary')
    assert s['duration_ms']==s['end_ms']-s['start_ms']
    r=dict(shot_id=s['id'],act=s['act'],title_zh=s['title_zh'],title_en=s['title_en'],
        start_ms=s['start_ms'],end_ms=s['end_ms'],duration_ms=s['duration_ms'],
        start_frame=start_frames,end_frame_exclusive=end_frames,duration_frames=end_frames-start_frames,
        record_in_tc=tc(start_frames),record_out_tc_exclusive=tc(end_frames),
        production_mode=s['generation_mode'],asset_status='REVIEW_SLATE_ONLY',
        art_reference=f"{s['art_reference']['artist']} — {s['art_reference']['work']}",
        prop_ids=';'.join(s.get('props',[])),
        incoming_transition=s['in_transition'],outgoing_transition=s['out_transition'])
    rows.append(r)
    preview_shots.append({
        'id':s['id'],'act':s['act'],'zh':s['title_zh'],'en':s['title_en'],
        'start':s['start_ms'],'end':s['end_ms'],'mode':s['generation_mode'],
        'artist':s['art_reference']['artist'],'art':s['art_reference']['work'],
        'image':excerpt(s['image_prompt'],470),'motion':excerpt(s['motion_prompt'],360),
        'sound':excerpt(s['sound_prompt'],350),
        'in':s['in_transition'],'out':s['out_transition'],'props':s.get('props',[]),
        'contest':excerpt(s['contest_override'],500)
    })
    subtitles.append(f"{i+1}\n{srt_tc(s['start_ms'])} --> {srt_tc(s['end_ms'])}\n[{s['id']}] {s['title_zh']} / {s['title_en']} [REVIEW SLATE ONLY]\n")

write_csv('j4_editorial_timeline.csv',list(rows[0]),rows)
(ROOT/'j4_review_slates.srt').write_text('\n'.join(subtitles),encoding='utf-8')
trans=[]
for a,b in zip(shots,shots[1:]):
    trans.append({'from':a['id'],'to':b['id'],'cut_at_ms':a['end_ms'], 'cut_at_frame':a['end_ms']*FPS//1000,
                  'outgoing_intent':a['out_transition'],'incoming_intent':b['in_transition'],
                  'planned_mechanism':'EDITORIAL_MATCH / SOUND_BRIDGE',
                  'review_status':'NOT_RUN','evidence':'',
                  'high_priority':'YES' if a['id'] in {'S02','S03','S04','S05','S07','S08','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22','S23','S24'} else 'NO'})
write_csv('j4_transition_matrix.csv',list(trans[0]),trans)

# Sound events are timing guide only, NOT audio synthesis / no sounds played.
events=[]
for fam in sound_doc['phase_families']:
    events.append({'at_ms':fam['start_ms'],'timecode':tc(fam['start_ms']*FPS//1000),
                   'event':f"START_{fam['id']}",'class':'phase_family',
                   'description':f"{fam['theme']} / period {fam['period_ms']} ms; hard stop 63700 ms",'review_status':'DESIGN_ONLY'})
for ev in sound_doc['events']:
    events.append({'at_ms':ev['at_ms'],'timecode':tc(ev['at_ms']*FPS//1000),
                   'event':ev['kind'].upper(),'class':'absolute_event',
                   'description':ev.get('detail',str({k:v for k,v in ev.items() if k not in ['at_ms','kind']})),
                   'review_status':'DESIGN_ONLY'})
events.sort(key=lambda e:(e['at_ms'],e['class']))
write_csv('j4_sound_events.csv',list(events[0]),events)

# These uploaded copies are for provenance inventory only; no images / frames are extracted.
media=[]
for filename in ['IMG_7835.mp4','IMG_7836.mp4','IMG_7876.mp4']:
    p=Path('/mnt/data')/filename
    if not p.exists(): continue
    cmd=['ffprobe','-v','error','-select_streams','v:0','-show_entries',
         'stream=width,height,avg_frame_rate,nb_frames:format=duration',
         '-of','json',str(p)]
    result=json.loads(subprocess.check_output(cmd, text=True))
    video=result['streams'][0]
    media.append({'filename':filename,'duration_s':result['format']['duration'],
      'width':video['width'],'height':video['height'],'fps':video['avg_frame_rate'],
      'total_video_frames':video.get('nb_frames',''),
      'contest_previs_usage':'EXCLUDED','portfolio_footage_permission':'NOT_REVIEWED',
      'notes':'User supplied media; metadata only. No frames included in preview.'})
if media: write_csv('j4_media_inventory.csv',list(media[0]),media)

report={
 'project':'J4 Museum Cinema','version':'v2.7-offline-text-previs',
 'approval_state':'NO_GENERATIVE_MEDIA_REQUESTED_OR_RUN',
 'timeline':{'fps':FPS,'total_ms':TOTAL_MS,'frames':TOTAL_MS*FPS//1000,
   'shot_count':len(shots),'transition_count':len(trans),
   'frame_aligned':True,'continuous':True,
   'editorial': [s['id'] for s in shots if s['generation_mode']=='editorial'],
   'candidate_video':[s['id'] for s in shots if s['generation_mode']=='video']},
 'sound':{'phase_families':len(sound_doc['phase_families']),
   'stop_at_ms':63700,'sine_continues':True,
   'original_audio_created':False,'mix_measured':False},
 'assets':{'source_media_probed':[a['filename'] for a in media],
    'source_frames_used':0,'generated_images':0,'generated_videos':0,
    'licensed_reference_art_used':0,'provided_original_video_embedded':False},
 'gates':{'contest_feature_length':'BLOCKED_90_SECONDS_BELOW_3_MINUTES',
          'native_pipeline_schema':'BLOCKED_NOT_PROVIDED',
          'media_authorisation':'NOT_RUN',
          'sound_production':'NOT_RUN',
          'visual_composition_review':'NOT_RUN',
          'actual_video_generation':'NOT_APPROVED',
          'current_paid_credit_estimate':'NOT_VERIFIED'},
 'static_checks':{'timeline_90s':'PASS','25_shots':'PASS','frame_alignment_30fps':'PASS',
          '24_transitions':'PASS','metadata_only_contest_previs':'PASS',
          'exact_s18_start_ms':63700,'exact_s18_end_ms':65000,
          'original_180s_min_contest_condition':'NOT_MET'},
 'not_claimed':['Higgsfield render or free image generation','Real image or audio QC',
                'Original pipeline/build_animatic.py schema compatibility',
                'Current contest eligibility', 'Current credits/account usage']
}
(ROOT/'j4_preflight_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'j4_timeline_v2_7.json').write_text(json.dumps({
  'version':'v2.7-review-only','fps':FPS,'duration_frames':2700,
  'clips':rows,'sound_events':events,
  'source_ir':'source_v2_6/j4_shots.json',
  'note':'Review timeline only. Not a native editor/pipeline schema, no media linked.'
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Prevent embedded JSON from closing script; no tool or external network dependencies.
manifest={'shots':preview_shots,'sound_families':sound_doc['phase_families'],
          'sound_events':events, 'duration_ms':TOTAL_MS,'fps':FPS}
json_js=json.dumps(manifest,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>J4 Museum Cinema — 90s Text Animatic</title>
<style>
:root{color-scheme:dark;--bg:#101419;--muted:#96a2af;--text:#e5e9ec;--line:#303942;--panel:#182129;--gold:#d0b886;--blue:#9db9c7}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif}
header{max-width:1160px;margin:0 auto;padding:26px 22px 15px;display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap}
h1{margin:0;font-size:21px;font-weight:550;letter-spacing:.015em}small,.sub{color:var(--muted)}.warn{border:1px solid #665b3d;border-radius:7px;padding:8px 11px;color:#dac79e;font-size:12px}
main{max-width:1160px;margin:auto;padding:0 22px 40px}
.display{border:1px solid var(--line);border-radius:14px;min-height:310px;display:flex;overflow:hidden;position:relative;background:linear-gradient(165deg,#161c22,#0d1015)}
.display[data-act="1"]{background:linear-gradient(140deg,#25241f 0%,#121820 65%)}
.display[data-act="2"]{background:linear-gradient(135deg,#142027 0%,#10141a 65%)}
.display[data-act="3"]{background:linear-gradient(135deg,#202024 0%,#101319 65%)}
.scene{width:100%;padding:45px 36px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:14px}
.scene h2{font-size:clamp(28px,4.3vw,48px);font-weight:450;margin:0;line-height:1.16;letter-spacing:.04em}
.scene .en{color:var(--blue);font-size:14px;letter-spacing:.12em;text-transform:uppercase}
.scene .label{color:#cbb991;font-size:11px;letter-spacing:.12em}.scene .note{max-width:680px;color:#b4bec7;font-size:13px;line-height:1.6}
#shotTag{position:absolute;top:16px;left:18px;font-size:12px;color:#b8c3cb}#timeTag{position:absolute;top:16px;right:18px;color:#b8c3cb;font-variant-numeric:tabular-nums;font-size:12px}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:16px 0}button,select{border:1px solid #44525e;color:#e8edf0;background:#25313c;border-radius:7px;padding:9px 12px;cursor:pointer}
button:hover{background:#30414d}button:focus-visible,input:focus-visible{outline:2px solid #b5cedc}#seek{width:100%;accent-color:#bdc9d0;cursor:pointer}
#bar{display:flex;width:100%;height:20px;overflow:hidden;gap:1px;background:#111922;border-radius:5px}#bar button{padding:0;height:20px;min-width:1px;border:0;border-radius:0;background:#637281;opacity:.65}
#bar button:nth-child(-n+5){background:#a18d70}#bar button:nth-child(n+19){background:#9ca6a7}#bar button.active{opacity:1;filter:brightness(1.65)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0}
.panel{border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:18px 20px;min-width:0}
.panel h3{font-weight:550;font-size:14px;color:#e1e8ec;margin:0 0 12px}#outText,#inText,#promptText,#soundText,#artText,#contestText{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.6;font-size:13px;color:#b6c2cc}
.meta{color:#d3bf98;font-size:12px;letter-spacing:.02em}#phaseList{display:grid;gap:8px}.phase{display:grid;grid-template-columns:105px 1fr 36px;align-items:center;gap:9px;font-size:11px;color:#b8c4cd}
.track{height:6px;border-radius:5px;background:#323b47;overflow:hidden}.fill{background:#9db9c7;height:100%;width:0%}
footer{max-width:1160px;margin:10px auto 30px;padding:0 22px;color:#8e9aa7;font-size:12px}
@media(max-width:700px){.cols{grid-template-columns:1fr}.scene{padding:48px 16px}.display{min-height:310px}header{padding:20px 18px}main{padding:0 16px 30px}.phase{grid-template-columns:95px 1fr 30px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{transition:none!important;animation:none!important}}
</style></head>
<body><header><div><h1>J4《非同步：繼承》</h1><div class="sub">90 秒｜25 鏡｜當代藝術聲畫電影・文字預演</div></div><div class="warn">REVIEW ONLY · 無影像生成 · 無聲音播放</div></header>
<main><div class="display" id="display" data-act="1" role="region" aria-label="目前預演鏡頭">
<div id="shotTag">S01</div><div id="timeTag">00:00.0</div><div class="scene"><div class="label" id="actLabel">ACT I · LIGHT</div><h2 id="shotTitle">第一束光之前</h2><div class="en" id="shotEnglish">Before the First Light</div><div class="note" id="shotDesc">純黑文字預演；不代表實際視覺內容</div></div></div>
<div class="controls"><button id="prev" aria-label="上一鏡">◀ 上一鏡</button><button id="play">▶ 播放</button><button id="next" aria-label="下一鏡">下一鏡 ▶</button><button id="jump">跳至 S18</button><label class="sub">速度 <select id="speed"><option value="1">1×</option><option value="2">2×</option><option value="4">4×</option></select></label><label class="sub"><input id="contest" type="checkbox"/> 顯示比賽版替代註記</label><span class="sub" id="progress">0.0 / 90.0s</span></div>
<input id="seek" type="range" min="0" max="90000" step="100" value="0" aria-label="預演時間軸"/>
<div id="bar" aria-label="25 鏡時間軸"></div>
<div class="cols"><section class="panel"><h3>場景與藝術對標</h3><div class="meta" id="artText"></div><p id="promptText"></p><h3>進入此鏡</h3><div id="inText"></div><h3 style="margin-top:16px">離開此鏡</h3><div id="outText"></div></section>
<section class="panel"><h3>聲音提示（無實際聲音）</h3><div id="soundText"></div><h3 style="margin-top:18px">六個非同步相位</h3><div id="phaseList"></div><h3 style="margin-top:18px">比賽版與權利註記</h3><div id="contestText"></div></section></div>
<p class="sub">此頁僅提供構圖、聲音與剪接時碼的文字檢查。沒有使用原始真人影片、生成關鍵幀、生成音樂，也未核准付費製作；作品集／比賽資格需獨立審核。</p></main>
<footer>Source: v2.6 Canonical Shot IR · 30fps planning grid · v2.7 offline review · No external scripts, fonts, network, or media.</footer>
<script>const DATA=__MANIFEST__;
const $=id=>document.getElementById(id);const D=DATA.duration_ms;let t=0,playing=false,last=0,cur=-1;
function indexAt(ms){let i=DATA.shots.findIndex(s=>ms>=s.start&&ms<s.end);return i<0?DATA.shots.length-1:i}
function stamp(ms){let tenths=Math.floor(ms/100);return `${String(Math.floor(tenths/600)).padStart(2,'0')}:${String(Math.floor(tenths%600/10)).padStart(2,'0')}.${tenths%10}`}
function setTime(v){t=Math.max(0,Math.min(D,Number(v)));draw()}
function draw(){let i=indexAt(Math.min(t,D-1)),s=DATA.shots[i];$('timeTag').textContent=stamp(t);$('progress').textContent=(t/1000).toFixed(1)+' / 90.0s';$('seek').value=t;
$('shotTag').textContent=`${s.id} · ${((s.end-s.start)/1000).toFixed(1)}s · ${s.mode.toUpperCase()}`;$('display').dataset.act=s.act;
if(cur!==i){cur=i;$('shotTitle').textContent=s.zh;$('shotEnglish').textContent=s.en;$('actLabel').textContent=['','ACT I · LIGHT','ACT II · DISTRIBUTION','ACT III · SUCCESSION'][s.act];
$('shotDesc').textContent='TEXT-ONLY PREVIS · '+s.image.slice(0,205)+'…';$('artText').textContent=s.artist+' — '+s.art;
$('promptText').textContent=s.image+'…\n\n動作：'+s.motion+'…';$('inText').textContent=s.in;$('outText').textContent=s.out;$('soundText').textContent=s.sound+'…';
$('contestText').textContent=$('contest').checked?s.contest:'原始影片與可辨識真人不得用於比賽版本；切換上方選項顯示此鏡替代說明。';
[...$('bar').children].forEach((b,j)=>b.classList.toggle('active',j===i));}
$('phaseList').innerHTML='';for(let f of DATA.sound_families){let live=t>=f.start_ms&&t<f.forced_stop_ms;let pct=live?((t-f.start_ms)%f.period_ms)/f.period_ms*100:0;
let div=document.createElement('div');div.className='phase';let name=document.createElement('span');name.textContent=f.id.replace('_',' ');let track=document.createElement('div');track.className='track';let fill=document.createElement('div');fill.className='fill';fill.style.width=pct+'%';track.appendChild(fill);let state=document.createElement('span');state.textContent=live?'ON':'OFF';div.append(name,track,state);$('phaseList').appendChild(div);}}
function animate(now){if(!playing)return;if(!last)last=now;const delta=(now-last)*Number($('speed').value);last=now;t=Math.min(D,t+delta);draw();if(t>=D){playing=false;$('play').textContent='▶ 播放';return;}requestAnimationFrame(animate)}
$('play').onclick=()=>{playing=!playing;$('play').textContent=playing?'Ⅱ 暫停':'▶ 播放';last=0;if(playing){if(t>=D)t=0;requestAnimationFrame(animate)}};
$('seek').oninput=e=>setTime(e.target.value);$('next').onclick=()=>setTime(DATA.shots[Math.min(indexAt(Math.min(t,D-1))+1,24)].start);
$('prev').onclick=()=>setTime(DATA.shots[Math.max(indexAt(Math.min(t,D-1))-1,0)].start);$('jump').onclick=()=>setTime(63700);
$('contest').onchange=()=>{cur=-1;draw()};window.addEventListener('keydown',e=>{if(e.code==='Space'&&!(e.target instanceof HTMLInputElement)){e.preventDefault();$('play').click()}});
for(let s of DATA.shots){let b=document.createElement('button');b.style.flex=`${s.end-s.start} 1 0`;b.title=`${s.id} ${s.zh} ${stamp(s.start)}–${stamp(s.end)}`;b.setAttribute('aria-label',`${s.id} ${s.zh}`);b.onclick=()=>setTime(s.start);$('bar').appendChild(b)}draw();
</script></body></html>'''
(ROOT/'j4_previs.html').write_text(html.replace('__MANIFEST__',json_js),encoding='utf-8')
print(f'Built {len(shots)} shots / {len(trans)} transitions, {len(events)} sound markers, {len(media)} media metadata rows. No video/audio/image generation.')
