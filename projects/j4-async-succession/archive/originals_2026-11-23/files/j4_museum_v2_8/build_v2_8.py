#!/usr/bin/env python3
"""Create versioned zero-generative J4 v2.8 acceptance review from mounted v2.6/2.7 sources."""
from pathlib import Path
import json,csv,copy,html,datetime,shutil,zipfile,hashlib
ROOT=Path('/mnt/data')
V26=ROOT/'j4_museum_v2_6'; V27=ROOT/'j4_museum_v2_7'; OUT=ROOT/'j4_museum_v2_8'
OUT.mkdir(exist_ok=True)
read_json=lambda p:json.loads(p.read_text(encoding='utf-8'))
write_json=lambda name,obj:(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
base=read_json(V26/'j4_shots.json'); sound=read_json(V26/'j4_sound_ir.json')
rev=copy.deepcopy(base); snd=copy.deepcopy(sound)
rev['version']='v2.8-zero-credit-previs-candidate'
rev['status']='EDITORIAL_REVIEW_ONLY; NO_IMAGERY_AUDIO_GENERATED; NO_MEDIA_APPROVAL'
rev['governance']['production_state']='GATED_NO_GENERATIVE_MEDIA'
rev['governance']['v2_8_scope']='Only S10/S18/S22/S24 motion/sound design changed; no creative render and no base v2.6 overwrite'
changes={
'S10':{
'motion_prompt': '0.0–0.9 still with mesh open; 0.9–1.8 gloved hand begins sliding door; 1.8–2.7 mesh shadow crosses archived coat; 2.7–3.1 door continues closing; at local 3.1s (absolute 38.600s) metal latch makes restrained contact, the incomplete local piano-like tail is cut; 3.1–3.5 one sleeve shifts slightly in displaced air and settles. No ghost effect. The mesh-metal contact decay bridges to S11, independently of the interrupted piano-like tail.',
'sound_prompt': 'Preserve six independent global ambience phase families. The S10-only deliberately interrupted short piano-like residual tone continues until absolute 38.600s, precisely when the mesh door latch contacts. Cut only this residual pitched tail; the same moment creates a fresh metal contact whose natural decay continues into S11 actuator sound. Global sine stays phase-continuous. Do not execute a global sound interruption here.'},
'S18':{
'motion_prompt': 'ACCESSIBLE EDITORIAL DEFAULT. 0.00–0.35 absolute black; 0.35–0.70 one soft low-luminance reveal of three abstract non-strobing light volumes; 0.70–1.00 low-luminance dissolve into black; 1.00–1.30 black hold; at exact absolute 65.000s hard cut to S19. No repeated flash, sudden bright white or high-frequency modulation. Use safe luminance and exposure testing on final mastered media.',
'sound_prompt':'At exactly absolute 63.700s, interrupt all six phase-family ambiences and secondary pitched textures with anti-click envelopes; never reset or phase-align them. Continuous original sine retains phase. Do not attach impacts to the single soft reveal. At 65.000s introduce a new low-level S19 broadcast-electronics ambience. Visual accessibility not certified until mastered playback.'},
'S22':{
'motion_prompt': '3.0s LEGIBILITY-FIRST. FIRST FRAME must already show one fictional salaryman, complete physical paper coastline, paper bridge in foreground and distant unoccupied warm-lit paper house all in one clear composition. 0.0–0.6 hold to read world; 0.6–1.7 ONE PRIMARY ACTION: a single fingertip gently steadies a fragile bridge moved by ventilation; 1.7–2.5 the paper bridge holds, the hand stops; 2.5–3.0 silent held composition with distant warm house still empty. No new document stamping, parcel placement, bridge building or second reveal. Paper and character physically continuous.',
'sound_prompt':'S21 brass-contact tail transitions into paper friction. Ventilation moves the bridge; the only focal Foley is fingertip-on-folded-paper contact around local 0.6–1.7. One very low original felt-muted piano tone enters off the physical hand gesture after local 1.7; distant stationary compute harmonic is secondary. Carry residual paper friction to S23. No added secondary heroic cue.'},
'S24':{
'motion_prompt': '3.0s LEGIBILITY-FIRST. FIRST FRAME already shows fictional ordinary night-market ensemble holding the EMPTY founder coat A aloft, with rain already softly falling and warm bulbs lit; the original filament bird v1 is approaching from just above frame. 0.0–0.8 hold coat nearly still and let audience register place and absence; 0.8–2.0 ONE PRIMARY ACTION: the tiny bird settles once onto coat shoulder with physically modest movement; 2.0–3.0 hold its delicate light, while fingers and rain have only incidental motion. No new coat-lift, rain onset, synchronized lights, cheering or camera crane. Hard cut to S25 at 87.000s.',
'sound_prompt':'At 84.000s introduce NEW short market-memory ambience and light rain, not the old seven-second phase family; include restrained fabric and breathing. The bird landing has only a delicate material/electrical sound, no theme victory. Original motif may appear as unresolved fragments. At 87.000s strip all new environmental and motif layers, leaving the phase-continuous sine unchanged in S25.'}
}
for s in rev['shots']:
 if s['id'] in changes:
  s.update(changes[s['id']]);s['review_state']='V2_8_TEXT_DESIGN_REVISED_NOT_VIEWED'
  if s['id']=='S24':
   s['image_prompt']=s['image_prompt'].replace('gently raise the SAME plain charcoal founder work coat A, while the unique irregular small incandescent filament bird from S04 rests on its shoulder', 'already hold the SAME plain charcoal founder work coat A fully aloft; the unique irregular small incandescent filament bird from S04 hovers just above the shoulder and is about to land')
snd['version']='J4-SOUND-IR-v2.8-proposed'
snd['source_note']='Non-rendered v2.8 amendment; sound timing candidates require Sound Owner review and measured mix test.'
for e in snd['events']:
 if e['kind']=='deliberate_exception':
  assert e['at_ms']==35500
  e['at_ms']=38600
  e['detail']='S10: precisely at door latch (S10 local 3.1s); interrupt ONLY a local unfinished piano-like tail, not phase families; new metal contact rings into S11'
for c in snd['shot_sound_cues']:
 if c['shot_id'] in changes:c['sound_prompt']=changes[c['shot_id']]['sound_prompt']
write_json('j4_shots_v2_8.json',rev)
write_json('j4_sound_ir_v2_8.json',snd)
# Mapping from actual 25-shot source, human-authored concise single-frame inference and action hierarchy.
reviews = {
'S01':('黑畫面已先讓觀眾聽見一個尚未顯影的世界','維持純黑；不加入任何額外物件','唯一音訊動作：正弦波自 0.5s 出現','沒有可見影格；片頭字卡需剪輯驗收'),
'S02':('普通人分享食物與光，建立日常社群','第一影格含攤販、共享食物動線、暖燈','交碗是主要動作；蒸氣只作環境','避免夜市成為旅遊奇觀或高亮霓虹'),
'S03':('創造者在自己無法完全控制的光學現象前停下','人物背影與非水箱式光學薄膜同框','水滴造成稍晚的光學反射','不可重製原始水箱、已知藝術裝置'),
'S04':('脆弱的鎢絲光鳥離開日常起點','原創鳥與舊箱、燈具先同框','唯一動作：光鳥極小幅離開畫面','S24 使用同一鳥形；不可像既有徽記'),
'S05':('維護生活的工作有真實價值','手、碗、水槽及已洗淨物件皆可辨識','完成一次洗碗並放好','不得與 S22 制度性低效率等同'),
'S06':('分散分享與集中控制的兩種光系統並存','共享工作台在前、封閉裝置在後','一盞燈由他人接手後亮起','不能做簡單善惡對照或左右資訊圖'),
'S07':('運算基礎設施產生可觀察的人工氣候','空曠環境、設施與冷卻氣流同場','自然與人工氣流不同方向','避免宗教灌木、巴別塔、能源魔法'),
'S08':('人們互相模仿掌聲，共識逐漸形成','空展示台與不同聲學隔間中的人同框','鼓掌傳染；一人晚加入','不復刻 IPO 舞台及新聞素材'),
'S09':('一個人試圖發聲，卻可能被環境遮蔽','紅大衣人物與自製風扇擴音器可辨識','抬起裝置並嘗試說話','不對應任何真實活動領袖或口號'),
'S10':('機構保存衣物，卻無法保存人的意志','空舊衣、普通眼鏡和開啟的網格門可辨識','網格門於局部3.1秒閉合','Coat B 是檔案副本，非 S21/S24 Coat A'),
'S11':('機器繼續生產，而人類生活留下痕跡','機械臂、空凳及小紙屋先可辨識','機械循環；紙屋只在末段被注意','紙屋引到 S22；不表現工人無價值'),
'S12':('不在場的關係仍透過細線施力','兩張空桌與單一電話線完整看得見','張力引起極小移動','不建構紅線森林、不影射真實性別族群'),
'S13':('失去音準的技術器物仍保存精湛手藝','工匠、晶圓、受潮鋼琴同框','按下一鍵但不能正常發聲','不得重現真實災難受損鋼琴裝置'),
'S14':('文明對空舞台鼓掌，形成自我回音','空舞台與稀疏觀眾席同框','掌聲由不同方位發生','不復刻飢餓遊戲都城服飾或建築'),
'S15':('兩位織者用不同節奏照護未完成的未來','兩織者、不同材質、空搖籃同框','兩種梭子動作不對拍','不得偏袒單一族群生育論述'),
'S16':('機器效率與人的協調等待不是同一件事','平行通道、物流機器、人類同行者同框','機器移動，人類相互等待','不畫出真實邊境政治宣傳'),
'S17':('人面對超出直接感知能力的複雜系統','同一虛構人物與已變化的光學薄膜同框','張手、反射不同步，運動極少','音訊密度高但人保持克制'),
'S18':('不同系統在同一瞬間被外力中斷','黑暗中三個抽象低亮度光形位置明確','一次緩慢亮起後消失','不可頻閃；需實際光敏感審核'),
'S19':('尚未開始的新聞演播室已安排座位權力','虛構螢幕、五椅和三處亮光同框','微弱影像延遲，不移椅','不得偽裝真實深圳峰會新聞'),
'S20':('同一段記憶透過兩種媒材保留不同痕跡','紙、玻璃、兩隻手構圖成立','反射與印痕緩慢錯位','避免真實族群宗教檔案刻板化'),
'S21':('一把鑰匙易手，權力交接但時間不會同步','兩手、黃銅鑰匙、掛著 Coat A 的椅子同框','單次交接與手撤回','鑰匙/手部物理接觸及 Coat A 必須連續'),
'S22':('人極精巧地維持紙造世界，卻沒有人住在其中','第一影格：上班族、紙橋、紙海岸、空屋同框','唯一主動作：一指穩住紙橋','3秒仍可能過載；需1x實際畫面盲測'),
'S23':('創造者的身體已移動，反射卻稍晚抵達','同一主角無外套，遠方離開物件可見','一步後反射延遲','不可複製 Bill Viola 水池或真人原片'),
'S24':('普通人不對拍地共同保存創造者的象徵','第一影格外套已舉起、雨已落、鳥將進畫','唯一主動作：光鳥落在肩上','Coat A / Bird v1 正確；禁同期慶祝與口號'),
'S25':('影像停止，原本的聲音仍繼續','全黑加簡潔片名字卡','剪輯時片名淡入淡出','不得錯誤音檔截斷產生爆音')
}
assert len(reviews)==25
# Scores/status are deliberately unfilled: no rendered media to objectively judge.
axes=['narrative','first_frame','motion_hierarchy','sound_timing','transition','physical_ip']
rows=[]
for s in rev['shots']:
 sid=s['id']; target, first, motion, concern=reviews[sid]
 row={'shot_id':sid,'start_ms':s['start_ms'],'end_ms':s['end_ms'],'duration_ms':s['duration_ms'],
      'title_zh':s['title_zh'],'title_en':s['title_en'],'art_reference':s['art_reference']['artist']+' — '+s['art_reference']['work'],
      'viewer_takeaway_1x':target,'first_frame_acceptance':first,'dominant_motion_acceptance':motion,
      'audio_acceptance':s['sound_prompt'],'incoming_transition':s['in_transition'],'outgoing_transition':s['out_transition'],
      'specific_risk':concern, 'screen_media_available':'NO', 'rubric_version':'RUBRIC_V2_8'}
 for a in axes:
  row['score_'+a]=''
  row['status_'+a]='NOT_RUN'
 row['overall_status']='NOT_RUN';row['reviewer']='';row['evidence_path']='';row['review_notes']=''
 rows.append(row)
with (OUT/'j4_acceptance_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
write_json('j4_acceptance_matrix.json',{'version':'v2.8','review_state':'NOT_RUN_NO_RENDERED_MEDIA','rubric':{'dimensions':axes,'scoring':'0-10 per axis, require each >=7 and mean >=8; review statuses must reflect actual inspected media; no auto-pass on text','human_required':True,'cannot_evaluate_now':['creative image legibility','actual sound spatial accuracy','IP likeness','photosensitivity','true peak / LUFS','cross-shot visual matching']},'shots':rows})
# action log for resolved-as-proposal, not completed media QC
proposals=[]
for sid in ['S10','S18','S22','S24']:
 original=next(x for x in base['shots'] if x['id']==sid); proposed=next(x for x in rev['shots'] if x['id']==sid)
 proposals.append({'shot_id':sid,'state':'TEXT_PATCH_PROPOSED','approval_required':'DIRECTOR_REVIEW',
   'old_image_prompt':original['image_prompt'],'new_image_prompt':proposed['image_prompt'],
   'old_motion_prompt':original['motion_prompt'],'new_motion_prompt':proposed['motion_prompt'],
   'old_sound_prompt':original['sound_prompt'],'new_sound_prompt':proposed['sound_prompt']})
write_json('j4_revision_deltas.json',{'baseline':'v2.6 canonical JSON','changed':['S10','S18','S22','S24'],'no_render':True,'deltas':proposals})
# Detailed acceptance & gates
notes='''# J4 v2.8 — Previs Acceptance Protocol

**State: DESIGN_PATCHED / CREATIVE_QC_NOT_RUN / GENERATION_BLOCKED**  
Canonical baseline: v2.6 sources actually mounted in `/mnt/data/j4_museum_v2_6/`; editorial notes from v2.7. The derived v2.8 files do **not** mutate the user's original repository or previous package.

## 1. Scope

- Freeze the **25 shots / 90,000 ms / 30 fps / 2,700 frames** with 24 transitions.
- Motion and sound design patches for **S10, S18, S22, S24**, plus a matching **S24 image-prompt consistency fix** (bird approaching, coat already raised). Artistic content and documentary constraints for remaining shots preserved.
- A `REVIEW_SLATE_ONLY` exercise can test time allocation and intended narrative priority; **it cannot certify real-time image comprehension, sound mixing, similarity or copyright**.
- All scores blank and status `NOT_RUN`; never fill scores based solely on prose.

## 2. Human review dimensions (0–10)

| Dimension | Observe in final rendered candidate | Pass |
|---|---|---|
| narrative | First-time viewer can explain central meaning without subtitles | >=7 |
| first_frame | Needed place, props, and character are recognizable before action | >=7 |
| motion_hierarchy | One dominant action; secondary motion does not compete | >=7 |
| sound_timing | Original ambience/resonances coherent, spatial, phase-continuous | >=7 |
| transition | Outgoing visual and acoustic cues genuinely match next take | >=7 |
| physical_ip | Plausible materials/hands, no identifiable third-party art/real persons | >=7 |

**Creative gate:** average of six dimensions >=8; no dimension <7; evidence (take ID or video path) plus human reviewer and notes required. IP, consent, rights and contest are independent hard gates; a numeric pass does not substitute for them.

### Normal-speed blind review

1. Show each candidate shot at **1× speed**, with no explanation or written overlays. Ask an unfamiliar viewer: “What happened, and what did you notice first?”
2. Record literal answer and whether it matches `viewer_takeaway_1x`. A second playback may test details, but mark first-pass comprehension separately.
3. Show adjoining A→B cuts at 1× to test material/sound continuity. Do not infer transitions from text slates alone.
4. Test spatial and psychoacoustic effects with actual mix in stereo and headphones; check loudness and true peak with measured files.
5. Ensure no distinctive artwork image/audio is replicated; contest compliance needs current official rules and separate independent review.

## 3. Four proposed non-render changes

**S10**: Door latch designated **38.600s** (S10 local 3.1s). Cut only one residual piano-like tail then; preserve independent phase families and preserve a *new* metallic door contact to bridge into S11. v2.7 issue REV-04 gets a text-level proposal, NOT a creative pass.

**S18**: Accessibility-first single **soft non-strobe** reveal inside 63.700–65.000s. Original six phase families still stop exactly at **63.700s**, sine continues. Final mastered luminance and accessibility remain NOT_RUN.

**S22**: Salaryman, paper coast, bridge and empty lit house must be visible in FIRST FRAME. The sole dominant gesture is one finger steadying the bridge. Maintain 3.0s; real 1× comprehension NOT_RUN.

**S24**: Coat already raised and light rain already falling in FIRST FRAME; image prompt now says bird is approaching rather than already perched. The sole dominant gesture is bird landing on coat shoulder. Coat A and Bird v1 must match earlier shots. Maintain 3.0s; real 1× comprehension NOT_RUN.

## 4. Hard blockers retained

| Gate | Status | Exit condition |
|---|---|---|
| Original pipeline schema compatibility | BLOCKED | Obtain original `pipeline/build_animatic.py` and examples; read-only adapter test |
| 90s official contest entry | BLOCKED | Feature-length 3–7min version, independently reconfirm contest rules |
| Protected IP / real-person likeness / publication rights | NOT_RUN | Rights review on final imagery, voices, sources and claims |
| Mastering and photosensitivity QC | NOT_RUN | Inspect actual final renders and audio; measure standards |
| Higgsfield creation approval | BLOCKED | Neon explicit GO + Director estimate posted to AI Video Production Service + current month available budget verified |

## 5. Deliverables

- `j4_shots_v2_8.json`: versioned derived Shot IR (unrendered)
- `j4_sound_ir_v2_8.json`: corresponding versioned Sound IR
- `j4_revision_deltas.json`: before/after text record of four patches, including S24's image/motion consistency correction
- `j4_acceptance_matrix.csv/json`: 25-shot, six-axis unscored human review matrix
- `j4_review_v2_8.html`: interactive text-slate review and browser-local score entry; no external network
- `j4_previs_v2_7.html`: original v2.7 text animatic retained for reference
- `validate_v2_8.py`: checks 25/90s/30fps/changed-shots-only/critical events/default statuses

**Nothing in this package is a generated image, video or original sound master.**
'''
(OUT/'README_v2_8.md').write_text(notes,encoding='utf-8')
shutil.copy2(V27/'j4_previs.html',OUT/'j4_previs_v2_7.html')
# HTML with interactive timing preview and editable ratings exported client-side.
summary=[{'id':x['shot_id'],'start':x['start_ms'],'end':x['end_ms'],'title':x['title_zh'], 'eng':x['title_en'], 'takeaway':x['viewer_takeaway_1x'],'first':x['first_frame_acceptance'],'motion':x['dominant_motion_acceptance'],'audio':x['audio_acceptance'],'risk':x['specific_risk'],'art':x['art_reference'],'incoming':x['incoming_transition'],'outgoing':x['outgoing_transition']} for x in rows]
js_data=json.dumps(summary,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e')
page=r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>J4 v2.8 | Previs Acceptance</title>
<style>
:root{--bg:#101318;--panel:#1c2026;--panel2:#252a30;--line:#343a41;--text:#e9e9e7;--muted:#a5a9ad;--amber:#ddbd89;--red:#e8a9a9;--green:#9bcaad}
*{box-sizing:border-box}body{background:var(--bg);color:var(--text);font:15px/1.55 system-ui,-apple-system,'Noto Sans TC',sans-serif;margin:0}
a{color:var(--amber)}header{padding:25px 30px;border-bottom:1px solid var(--line);display:flex;align-items:end;gap:20px;justify-content:space-between;flex-wrap:wrap}
h1{font-size:24px;font-weight:560;margin:0}h2{font-size:16px;font-weight:600;margin:0 0 9px}p{margin:6px 0;color:var(--muted)}.eyebrow{font-size:11px;letter-spacing:.13em;color:var(--amber);text-transform:uppercase}
main{padding:20px 25px;max-width:1450px;margin:auto}.notice{border-left:3px solid var(--amber);background:var(--panel);padding:14px 18px;color:var(--text);margin:0 0 18px}
.layout{display:grid;grid-template-columns: minmax(290px, 390px) 1fr;gap:16px}.card{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:17px}
.screen{background:#050608;aspect-ratio:9/11;max-height:450px;display:flex;justify-content:center;align-items:center;text-align:center;flex-direction:column;padding:28px;margin-top:12px;border:1px solid #373737;position:relative}
.screen .kid{color:#777;letter-spacing:.2em;font-size:10px}.screen .large{font-size:36px;font-weight:400;color:var(--amber)}.screen .story{font-size:17px;color:#fff;max-width:420px;margin-top:13px}.screen .foot{position:absolute;bottom:15px;color:#999;font-size:11px}
.controls{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:12px}button,select,input[type=number],textarea{background:var(--panel2);color:var(--text);border:1px solid #50565c;border-radius:6px;padding:7px 9px;font:inherit}button{cursor:pointer}button:hover{border-color:var(--amber)}button.primary{border-color:var(--amber);color:var(--amber)}input[type=range]{width:100%;accent-color:var(--amber)}
.slist{max-height:290px;overflow:auto;margin-top:10px}.item{padding:9px;border-bottom:1px solid var(--line);cursor:pointer;display:flex;justify-content:space-between;gap:8px}.item.active{background:#343230;border-left:2px solid var(--amber)}.item small{color:var(--muted)}.item:hover{background:#292b2f}
.meta{display:grid;grid-template-columns:1fr 1fr;gap:9px}.meta>div{background:var(--panel2);padding:10px;border-radius:7px}.meta small{color:var(--muted);display:block}.meta span{font-size:14px}
.glist{display:grid;grid-template-columns: repeat(2,minmax(150px,1fr));gap:8px;margin-top:12px}.grade{background:var(--panel2);padding:11px;border-radius:8px}.grade label{display:block;font-size:12px;color:var(--muted)}.grade select{width:100%;margin-top:5px}
.details{display:grid;gap:9px;margin:14px 0}.details .detail{border-bottom:1px solid var(--line);padding-bottom:8px}.details strong{display:block;color:var(--amber);font-size:12px}.details span{color:var(--text)}
.badge{font-size:11px;border:1px solid #6f6c66;border-radius:40px;padding:3px 9px;color:var(--amber)}.warn{color:var(--red)}.status{color:var(--muted);font-size:12px}.info{color:var(--green)}textarea{width:100%;min-height:65px;resize:vertical}.footer{margin:24px 0;color:var(--muted);font-size:12px}
@media(max-width:920px){.layout{grid-template-columns:1fr}.screen{aspect-ratio:16/9;max-height:300px}.glist{grid-template-columns:1fr 1fr}}@media(max-width:480px){header,main{padding:16px}.glist{grid-template-columns:1fr}.screen .large{font-size:28px}}
</style></head><body>
<header><div><div class="eyebrow">ASYNC: SUCCESSION / MUSEUM CINEMA</div><h1>v2.8 · Previs Acceptance</h1><p>90 秒純文字節拍預演與人工驗收記錄</p></div><div class="badge">TEXT ONLY · NO CREATIVE MEDIA · GATE BLOCKED</div></header>
<main><div class="notice"><b>審核界線：</b>這是閱讀節奏和導演記錄工具，不是影片。不能從文字畫面給出真實視覺／聲音通過分數。尚未有生成畫面，全部評分預設 <code>NOT_RUN</code>。任何通過紀錄需在看到實際 take 後才填寫。</div>
<div class="layout"><section><div class="card"><div class="eyebrow" id="clock">00:00.000 / 01:30.000</div><div class="screen"><div class="kid" id="shotnum">S01</div><div class="large" id="shotTitle">第一束光之前</div><div class="story" id="shotStory">聲音先於畫面</div><div class="foot">STORY SLATE — NOT GENERATED VIDEO</div></div>
<div class="controls"><button class="primary" id="play">播放 1×</button><button id="prev">上一鏡</button><button id="next">下一鏡</button><select id="speed" title="播放倍速"><option value="1">1×</option><option value="2">2×</option><option value="4">4×</option></select></div><input id="seek" type="range" min="0" max="90000" value="0" step="10" aria-label="時間軸"/>
<div class="status" id="timelineState">未播放</div></div><div class="card" style="margin-top:16px"><h2>25 鏡</h2><div class="slist" id="shotList"></div></div></section>
<section><div class="card"><div style="display:flex;align-items:center;justify-content:space-between;gap:12px"><h2 id="reviewTitle">S01 — 第一束光之前</h2><span class="badge" id="duration">3.0s</span></div>
<div class="meta"><div><small>藝術參考（方法，非授權）</small><span id="art"></span></div><div><small>審核狀態</small><span id="overall">NOT_RUN</span></div></div>
<div class="details"><div class="detail"><strong>觀眾第一次觀看要理解</strong><span id="takeaway"></span></div><div class="detail"><strong>第一影格必須成立</strong><span id="first"></span></div><div class="detail"><strong>主要動作</strong><span id="motion"></span></div><div class="detail"><strong>聲音設計</strong><span id="audio"></span></div><div class="detail"><strong>入鏡轉場</strong><span id="incoming"></span></div><div class="detail"><strong>出鏡轉場</strong><span id="outgoing"></span></div><div class="detail"><strong>特定風險</strong><span id="risk" class="warn"></span></div></div>
<h2>人工驗收（只在檢視真實素材後填寫）</h2><p style="font-size:12px">六維各 0–10 分；每項≥7、平均≥8，另需獨立權利／授權 Gate。未實際檢視請保持空白。</p>
<div id="grades" class="glist"></div><label for="reviewer" class="eyebrow" style="display:block;margin-top:13px">審核者／實際 Take 證據</label><input id="reviewer" placeholder="Reviewer / Take ID or media path" style="width:100%;margin:6px 0"/>
<label for="notes" class="eyebrow" style="display:block;margin-top:9px">審核註記</label><textarea id="notes" placeholder="真實 1× 播放觀察、盲測答覆、需要修正的細節"></textarea>
<div class="controls"><button class="primary" id="save">儲存當前審核</button><button id="export">匯出全部審核 JSON</button><button id="reset">清除此鏡輸入</button></div><p class="status" id="saveState">狀態保存在本機瀏覽器（若環境允許）；請匯出 JSON 備份。</p>
</div></section></div>
<div class="footer">J4 v2.8 • 25 shots / 2700 frames / 30 fps • S18 phase stop 63.700 s • S10 local tail cut 38.600 s • This review does not call generation services or submit data online.</div>
</main>
<script>
const SHOTS=__DATA__;
const AXES=[['narrative','敘事清楚'],['first_frame','首影格可讀'],['motion_hierarchy','主動作清楚'],['sound_timing','聲音與時間'],['transition','前後鏡串接'],['physical_ip','物理真實與 IP']];
let states={};try{states=JSON.parse(localStorage.getItem('j4_v2_8_review')||'{}')}catch(e){states={}}
let position=0,playing=false,speed=1,raf=null,lastT=null,selected='S01';
const $=x=>document.getElementById(x), seconds=x=>(x/1000).toFixed(2)+'s',tcode=x=>String(Math.floor(x/60000)).padStart(2,'0')+':'+String(Math.floor(x%60000/1000)).padStart(2,'0')+'.'+String(x%1000).padStart(3,'0');
const safe=(s)=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function findshot(ms){return SHOTS.find(s=>ms>=s.start&&ms<s.end)||SHOTS[SHOTS.length-1]}
function rec(id){return states[id]||{scores:{},reviewer:'',notes:''}}
function renderList(){ $('shotList').innerHTML=SHOTS.map(s=>`<div class="item ${s.id===selected?'active':''}" data-id="${s.id}"><span><b>${s.id}</b>　${safe(s.title)}</span><small>${seconds(s.start)}–${seconds(s.end)}　${Object.values(rec(s.id).scores).filter(x=>x!=='').length}/6</small></div>`).join('');for(const el of document.querySelectorAll('.item'))el.onclick=()=>jump(el.dataset.id)}
function renderCurrent(s){
 $('shotnum').textContent=s.id; $('shotTitle').textContent=s.title;$('shotStory').textContent=s.takeaway;$('reviewTitle').textContent=s.id+' — '+s.title;
 $('duration').textContent=seconds(s.end-s.start);$('art').textContent=s.art;
 ['takeaway','first','motion','audio','incoming','outgoing','risk'].forEach(k=>$(k).textContent=s[k]);
 const r=rec(s.id); const sc=r.scores||{};const vals=Object.values(sc).filter(x=>Number.isInteger(x));
 $('overall').textContent=vals.length===6?('人工得分平均 '+(vals.reduce((a,b)=>a+b,0)/6).toFixed(1)+' — '+(vals.every(x=>x>=7)&&(vals.reduce((a,b)=>a+b,0)/6)>=8?'待核對其他 Gate':'需修訂')):'NOT_RUN / '+vals.length+'/6';
 $('grades').innerHTML=AXES.map(([key,lab])=>`<div class="grade"><label for="g_${key}">${lab}</label><select id="g_${key}"><option value="">NOT_RUN</option>${Array.from({length:11},(_,i)=>`<option value="${i}" ${sc[key]===i?'selected':''}>${i}/10</option>`).join('')}</select></div>`).join('');
 $('reviewer').value=r.reviewer||'';$('notes').value=r.notes||'';
}
function refresh(){const s=findshot(position);$('clock').textContent=tcode(position)+' / 01:30.000';$('seek').value=Math.floor(position);if(s.id!==selected){selected=s.id;renderCurrent(s);renderList()}}
function jump(id){const s=SHOTS.find(s=>s.id===id);if(!s)return;position=s.start;selected=id;refresh();renderCurrent(s);renderList()}
function stop(){playing=false;lastT=null;$('play').textContent='播放 1×';if(raf)cancelAnimationFrame(raf);raf=null}
function step(t){if(!playing)return;if(lastT!==null){position+=Math.max(0,t-lastT)*speed}lastT=t;if(position>=90000){position=89999;refresh();stop();return}refresh();raf=requestAnimationFrame(step)}
$('play').onclick=()=>{if(playing){stop()}else{playing=true;lastT=null;$('play').textContent='暫停';raf=requestAnimationFrame(step)}};
$('prev').onclick=()=>{let i=SHOTS.findIndex(s=>s.id===findshot(position).id);jump(SHOTS[Math.max(0,i-1)].id)};
$('next').onclick=()=>{let i=SHOTS.findIndex(s=>s.id===findshot(position).id);jump(SHOTS[Math.min(SHOTS.length-1,i+1)].id)};
$('speed').onchange=e=>{speed=Number(e.target.value)};
$('seek').oninput=e=>{position=Number(e.target.value);refresh()};
$('save').onclick=()=>{const scores={};for(const [key] of AXES){const v=$('g_'+key).value;if(v!=='')scores[key]=Number(v)}const reviewer=$('reviewer').value.trim(),notes=$('notes').value.trim();if(Object.keys(scores).length>0&&!reviewer){alert('如要評分，請填寫審核者及 Take ID／媒體路徑，並確保實際看過素材。');return}states[selected]={scores,reviewer,notes,updated_at:new Date().toISOString()};try{localStorage.setItem('j4_v2_8_review',JSON.stringify(states))}catch(e){}renderCurrent(findshot(position));renderList();$('saveState').textContent='已儲存瀏覽器暫存；請定期匯出 JSON。'};
$('reset').onclick=()=>{delete states[selected];try{localStorage.setItem('j4_v2_8_review',JSON.stringify(states))}catch(e){}renderCurrent(findshot(position));renderList()};
$('export').onclick=()=>{const payload={project:'J4',version:'v2.8',kind:'HUMAN_REVIEW_NOT_AUTOMATED_QC',saved_at:new Date().toISOString(),reviews:states};const a=document.createElement('a');const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.href=url;a.download='j4_v2_8_human_review.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),400)};
renderCurrent(SHOTS[0]);renderList();refresh();
</script></body></html>'''
page=page.replace('__DATA__',js_data)
(OUT/'j4_review_v2_8.html').write_text(page,encoding='utf-8')
# validator authored separately; expected script regenerated without touching originals.
validator='''#!/usr/bin/env python3
from pathlib import Path
import json,csv,hashlib
r=Path(__file__).resolve().parent
src=Path('/mnt/data/j4_museum_v2_6')
a=json.loads((r/'j4_shots_v2_8.json').read_text()); b=json.loads((src/'j4_shots.json').read_text()); snd=json.loads((r/'j4_sound_ir_v2_8.json').read_text());base_snd=json.loads((src/'j4_sound_ir.json').read_text())
shots=a['shots']; orig=b['shots']; assert len(shots)==25
assert a['duration_ms']==90000 and sum(s['duration_ms'] for s in shots)==90000
for i,s in enumerate(shots):
 assert s['id']==f'S{i+1:02}'
 assert s['start_ms']==(shots[i-1]['end_ms'] if i else 0)
 assert s['end_ms']-s['start_ms']==s['duration_ms']
 assert s['start_ms']*30%1000==0 and s['end_ms']*30%1000==0
assert shots[-1]['end_ms']==90000
changed={s['id'] for s,o in zip(shots,orig) if s['motion_prompt']!=o['motion_prompt'] or s['sound_prompt']!=o['sound_prompt']}
assert changed=={'S10','S18','S22','S24'},changed
assert all(s['image_prompt']==o['image_prompt'] for s,o in zip(shots,orig) if s['id']!='S24')
assert shots[23]['image_prompt'] != orig[23]['image_prompt'] and 'about to land' in shots[23]['image_prompt']
assert any(e['kind']=='deliberate_exception' and e['at_ms']==38600 for e in snd['events'])
assert any(e['kind']=='forced_global_cut' and e['at_ms']==63700 for e in snd['events'])
assert not any(e['kind']=='deliberate_exception' and e['at_ms']==35500 for e in snd['events'])
for e in base_snd['phase_families']:
 r1=next(x for x in snd['phase_families'] if x['id']==e['id']); assert r1==e
with (r/'j4_acceptance_matrix.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
assert len(rows)==25 and [r['shot_id'] for r in rows]==[s['id'] for s in shots]
for row in rows:
 assert row['overall_status']=='NOT_RUN'
 assert row['reviewer']=='' and row['evidence_path']==''
 assert all(row['status_'+axis]=='NOT_RUN' and row['score_'+axis]=='' for axis in ['narrative','first_frame','motion_hierarchy','sound_timing','transition','physical_ip'])
assert 'one soft low-luminance reveal' in shots[17]['motion_prompt']
assert 'FIRST FRAME' in shots[21]['motion_prompt'] and 'FIRST FRAME' in shots[23]['motion_prompt']
assert '38.600s' in shots[9]['motion_prompt']
print('PASS: 25 shots, 2700 frames, 90s, 24 cuts, fixed S10 only-local audio, preserved S18 global stop, 4 shot revisions (S24 image consistency included), all 25 human QC NOT_RUN')
'''
(OUT/'validate_v2_8.py').write_text(validator,encoding='utf-8')
print('BUILT',len(rows),'shots','HTML',len(page),'bytes')
