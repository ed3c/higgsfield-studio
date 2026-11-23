from __future__ import annotations
import json,csv,os,hashlib,html,zipfile,datetime
from pathlib import Path
from copy import deepcopy
import shutil

ROOT=Path('/mnt/data')
SRC=ROOT/'j4_museum_v2_9'; OUT=ROOT/'j4_museum_v3_0';OUT.mkdir(exist_ok=True)
shots_base=json.loads((SRC/'j4_shots_v2_9.json').read_text())
sound_base=json.loads((SRC/'baseline_j4_sound_ir_v2_8.json').read_text())
comp_base=json.loads((SRC/'j4_keyframe_composition_v2_9.json').read_text())
shutil.copy2(SRC/'j4_shots_v2_9.json',OUT/'baseline_j4_shots_v2_9.json')
shutil.copy2(SRC/'j4_keyframe_composition_v2_9.json',OUT/'baseline_j4_keyframe_composition_v2_9.json')
S={s['id']:s for s in shots_base['shots']}
orig_boards={b['shot_id']:b for b in comp_base['boards']}

def Z(name,bbox,priority=2,first=True,role=''):
    return {'name':name,'bbox':bbox,'priority':priority,'required_first_frame':first,'role':role}

def B(id,brief,action,zones,lens,cam,light,read_test,forbid):
    s=S[id]
    return {'shot_id':id,'title':s['title_en'],'start_ms':s['start_ms'],'end_ms':s['end_ms'],
            'first_frame_read':brief,'single_action':action,'lens':lens,'camera':cam,'light_logic':light,
            'blind_test':read_test,'forbidden_similarity':forbid,'zones':zones,'design_state':'DESIGN_ONLY',
            'render_review_state':'NOT_RUN_NO_RENDER'}

vboards={
'S02':B('S02','夜市裡的人正在共享一盞普通的光','人把碗傳給另一人，水反射留給 S03',[
 Z('market_lamps',[.08,.13,.82,.22],2,True,'uneven practical tungsten'),
 Z('vendor',[.10,.40,.35,.37],1,True,'working adult at stall'),
 Z('bowl_exchange',[.41,.58,.34,.14],1,True,'human hand-to-hand connection'),
 Z('ordinary_market',[.53,.39,.41,.43],2,True,'intimate life, not spectacle'),
 Z('wet_reflection',[.24,.82,.50,.11],2,True,'thin warm reflection to S03')],
 '24mm','human eye height, gentle forward drift','bulb and wet steel each have local source','無聲第一秒：能辨識有人在交換食物，非旅遊景點照片',
 'no copied tank silhouette; no overfilled neon night market'),
'S03':None,
'S04':B('S04','舊行李箱旁一件極細、微亮的金屬造物','細線光鳥離開框外，非神奇變形',[
 Z('practical_bulb',[.30,.15,.39,.29],2,True,'real source of warm emission'),
 Z('small_wire_bird',[.58,.38,.19,.16],1,True,'unique irregular nonemblem wire bird'),
 Z('closed_suitcase',[.07,.62,.53,.23],1,True,'aged ordinary suitcase'),
 Z('warm_glint',[.28,.68,.23,.08],2,True,'visual trace of S03')],
 '85mm macro','locked close','filament glows weakly; no magic aura','首影格能辨識金屬小物與行李箱、不是某電影鳥徽',
 'no recognizable game or film bird insignia; no detailed wings'),
'S11':B('S11','機器照常工作，旁邊仍留著人類的紙屋','凝結水滴落下，最後視線才注意到紙屋',[
 Z('automated_line',[.09,.14,.82,.46],1,True,'credible robotic production'),
 Z('empty_stools',[.11,.63,.79,.24],1,True,'human absence without catastrophe'),
 Z('paper_house_hint',[.51,.62,.19,.12],1,True,'small imperfect roof echo of S22'),
 Z('condensation',[.74,.31,.11,.14],3,False,'one environmental droplet')],
 '24mm','low human-height wide','cold industrial practicals, restrained signal LEDs','能看出空凳、人造紙屋與機器共存，不是工廠毀滅',
 'no alarm lighting, no abandoned battlefield'),
'S12':B('S12','兩個無人桌位間只有一條受力的紅色線','電話線牽動聽筒數毫米，最後留下振動',[
 Z('near_table',[.07,.66,.53,.20],2,True,'dark worn wood'),
 Z('far_table',[.59,.35,.29,.14],2,True,'distant unoccupied position'),
 Z('red_phone_cord',[.27,.46,.59,.20],1,True,'single physically routed cord'),
 Z('receiver',[.17,.61,.20,.09],1,True,'muted red handset'),
 Z('negative_space',[.30,.19,.36,.26],2,True,'empty room with no human')],
 '50mm','locked architectural perspective','real high window makes faint cable shadow','不靠文字就能感到兩端的空缺、看到一條線的張力',
 'no red spiderweb boats; no diplomatic news scene'),
'S13':None,
'S21':B('S21','兩隻不同衣袖的手交接同一把黃銅鑰匙','鑰匙移交；焦點後移至已掛好的外套 A',[
 Z('founder_hand_shirt',[.10,.42,.38,.21],1,True,'plain dark SHIRT sleeve, no coat'),
 Z('steward_hand',[.54,.41,.34,.22],1,True,'fictional frost-white sleeve'),
 Z('single_brass_key',[.45,.48,.13,.11],1,True,'single key with coherent contact'),
 Z('chair_with_coat_A',[.38,.09,.30,.28],2,True,'coat A already on chair at frame 0')],
 '85mm','static tactile close; tiny rack focus','two separate practical shafts, no glowing key','鑰匙在兩隻手中只有一把，外套從第一影格已掛在後方',
 'no real CEO likeness; coat cannot teleport; no two clocks'),
'S22':None,
'S23':B('S23','不穿外套的同一背影人物，面對休眠的光學空間','前進一步，光學倒影以剪輯效果稍後跟上',[
 Z('optical_membranes_dormant',[.13,.18,.75,.39],1,True,'S03 structure, low illumination'),
 Z('founder_shirt_back',[.40,.56,.19,.34],1,True,'same fictional founder, no coat'),
 Z('delayed_floor_reflection',[.29,.80,.41,.10],2,True,'editorial temporal delay not light-speed phenomenon'),
 Z('piano_worker_distant',[.06,.61,.16,.14],3,True,'distant piano dolly'),
 Z('opera_coat_distant',[.79,.60,.14,.16],3,True,'garment rack, no national allegory')],
 '35mm','locked, human figure in lower third','one local source, optical surface near dormant','與 S03 同一間光學廳、服裝狀態已改，反射可剪輯控制',
 'no copying Bill Viola pool shot; no sudden supernatural double'),
'S24':None}
for sid in ('S03','S13','S22','S24'):
    b=orig_boards[sid]
    vboards[sid]={'shot_id':sid,'title':S[sid]['title_en'],'start_ms':S[sid]['start_ms'],'end_ms':S[sid]['end_ms'],
     'first_frame_read':b['frame_0_takeaway'],'single_action':b['dominant_action'],'lens':b['lens'],
     'camera':b['camera'],'light_logic':b['light'],'blind_test':b['frame_0_takeaway'],
     'forbidden_similarity':'; '.join(b['forbidden_similarity']),
     'zones':[{'name':z['name'],'bbox':z['bbox'],'priority':z['priority'],
               'required_first_frame':z['required_at_first_frame'],'role':z['role']} for z in b['zones']],
     'design_state':'DESIGN_ONLY','render_review_state':'NOT_RUN_NO_RENDER'}

hboards={
'S03':{'idea':'16:9 獨立構圖：創造者置於寬廣地坪的中央下方，薄膜向兩側擴張；不是 9:16 裁切',
 'zones':[Z('wide_optical_membranes',[.21,.13,.64,.48],1,True,'open arc, horizontal negative gaps'),Z('fictional_founder',[.44,.59,.12,.33],1,True,'small founder lower third'), Z('floor_reflection',[.30,.76,.47,.13],2,True,'local cold floor trace'),Z('warm_trace',[.55,.69,.11,.05],3,False,'warm motive')]},
'S13':{'idea':'16:9 獨立構圖：窗景留出海岸風，舊鋼琴與技師兩端互望，晶圓反射連接',
 'zones':[Z('sea_window',[.07,.07,.85,.37],2,True,'distant sea'),Z('weathered_piano',[.18,.44,.34,.48],1,True,'old upright'),Z('technician',[.62,.31,.20,.60],1,True,'fictional lithographer'),Z('wafer',[.56,.54,.11,.13],2,True,'one wafer')]},
'S22':{'idea':'16:9 獨立構圖：紙世界由中景擴到右方，孤獨人置左，遠方空房有足夠尺度可辨識',
 'zones':[Z('city_window',[.08,.05,.84,.25],3,True,'real dark city'),Z('salaryman',[.12,.29,.26,.62],1,True,'human labor left'),Z('paper_geography',[.34,.54,.53,.37],1,True,'paper terrain rich but legible'),Z('fragile_bridge',[.50,.65,.16,.12],1,True,'one focal bridge'),Z('empty_paper_house',[.73,.43,.10,.16],1,True,'distinct empty destination'),Z('local_compute',[.89,.32,.07,.11],3,False,'unobtrusive hardware')]},
'S24':{'idea':'16:9 獨立構圖：夜市水平層次而非新聞台團體合照，外套居中，光鳥極小；雨從頭就存在',
 'zones':[Z('market_bulbs',[.06,.10,.86,.22],2,True,'asymmetric practical lamps'),Z('coat_A',[.40,.29,.23,.37],1,True,'the original empty coat A'),Z('supporting_hands',[.29,.58,.44,.22],2,True,'different timings'),Z('bird_entry',[.54,.20,.09,.13],1,False,'small thin wire bird'),Z('market_ensemble',[.05,.64,.90,.26],2,True,'human market life'),Z('wet_pavement',[.07,.90,.84,.08],3,True,'natural reflections')]}
}

GROUPS=[
 {'id':'origin','name':'光的起源','shots':['S02','S03','S04'],'claim':'讓同一條暖色光學線索由生活 → 光學薄膜 → 細金屬絲轉換；不複製原始水箱構圖'},
 {'id':'system','name':'制度的振動','shots':['S11','S12','S13'],'claim':'生產線振動 → 電話線受力 → 失準琴弦；紙屋在 S11 只作伏筆'},
 {'id':'inheritance','name':'繼承與回返','shots':['S21','S22','S23','S24'],'claim':'鑰匙交接 → 指尖扶紙橋 → 人與反射分離 → 人群接住空外套與光鳥'}]

# Exact user-provided source; retain v2.7 reviewed transition wording.
with open(ROOT/'j4_museum_v2_7/j4_transition_matrix.csv',encoding='utf-8-sig') as f:
 rows={(r['from'],r['to']):r for r in csv.DictReader(f)}
edges=[]
for g in GROUPS:
 for a,b in zip(g['shots'],g['shots'][1:]):
  r=rows[(a,b)]
  edges.append({'id':f'{a}_{b}','kind':'adjacent','from':a,'to':b,'at_ms':int(r['cut_at_ms']),
    'at_frame':int(r['cut_at_frame']),'visual_claim':r['outgoing_intent'],'audio_claim':r['incoming_intent'],
    'mechanism':r['planned_mechanism'],'design_review_state':'NOT_RUN','render_review_state':'NOT_RUN_NO_MEDIA',
    'reviewer':'','evidence_uri':'','notes':''})
locks=[
 ('S02','S24','market_environment','ordinary warm practicals, wet pavement, human-scale market; no identical camera position'),
 ('S03','S17','optical_membranes','same architecture, membranes sparse to dense; same fictional founder in coat A'),
 ('S17','S23','optical_membranes','same architecture, dense to near-dormant; founder without coat A'),
 ('S04','S24','filament_bird_v1','same asymmetrical bird with one filament and three tiny wire joins'),
 ('S11','S22','paper_house_v1','same paper folding grammar; NOT same transported physical house'),
 ('S13','S23','untuned_piano','aged upright returns as distant theme on dolly, never a copied disaster instrument'),
 ('S21','S24','founder_coat_A','coat with small LEFT hem repair raised in S24; no archive coat B')]
for a,b,aid,claim in locks:
 edges.append({'id':f'{a}_{b}_{aid}','kind':'nonadjacent_asset','from':a,'to':b,'at_ms':None,'at_frame':None,
 'visual_claim':claim,'audio_claim':'Track only if the particular shot sound cue calls for it. No phase reset.',
 'mechanism':f'ASSET_LOCK:{aid}','design_review_state':'NOT_RUN','render_review_state':'NOT_RUN_NO_MEDIA',
 'reviewer':'','evidence_uri':'','notes':''})

# Four independent horizontal concepts are NOT derivatives of the vertical boxes.
meta={'version':'v3.0','project':'J4 ASYNC: SUCCESSION','status':'DESIGN_ONLY_NOT_GENERATED_NOT_APPROVED',
 'source_package':'j4_museum_v2_9','source_shots_sha256':hashlib.sha256((SRC/'j4_shots_v2_9.json').read_bytes()).hexdigest(),
 'source_composition_sha256':hashlib.sha256((SRC/'j4_keyframe_composition_v2_9.json').read_bytes()).hexdigest(),
 'timeline':{'shots':25,'duration_ms':90000,'fps':30,'frames':2700},
 'scope':{'linked_shots':10,'adjacent_edges':7,'nonadjacent_asset_checks':7,'vertical_wireframes':10,'horizontal_independently_authored':4},
 'no_media_generated':True,'no_external_service_calls':True,'rights_state':'NOT_REVIEWED',
 'paid_gate':'BLOCKED until Neon explicit approval, Director estimate posted, 9000 headroom and rights check',
 'notes':['Wireframes are DESIGN intent, not screenshots or approved visual outputs',
          '16:9 boards are independently art-directed, not crop validations',
          'Keep original source imagery unembedded; source usage is abstract, not a shot plate',
          'S18 global six-loop cut at 63.700s unchanged; local S10 cue at 38.600s unchanged']}
artifact={'metadata':meta,'groups':GROUPS,'vertical_9_16':list(vboards.values()),
 'horizontal_16_9':[{**{'shot_id':id},**data,'design_state':'DESIGN_ONLY','render_review_state':'NOT_RUN_NO_RENDER'} for id,data in hboards.items()],
 'continuity_tests':edges}
(OUT/'j4_visual_consistency_ir_v3_0.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')

with open(OUT/'j4_transition_acceptance_v3_0.csv','w',newline='',encoding='utf-8-sig') as f:
 field=['id','kind','from','to','at_ms','at_frame','visual_claim','audio_claim','mechanism','design_review_state','render_review_state','reviewer','evidence_uri','notes']
 wr=csv.DictWriter(f,fieldnames=field);wr.writeheader();wr.writerows(edges)

# Independent G1/G2/G3 review questions, statuses deliberately not passed.
checks=[]
def C(shot,gate,criterion):
 checks.append({'check_id':f'V3-{shot}-{gate}-{len(checks)+1:02d}','shot_id':shot,'gate':gate,
                'criterion':criterion,'status':'NOT_RUN','reviewer':'','evidence_uri':'','notes':''})
for sid,b in vboards.items():
 C(sid,'G1_FIRST_FRAME',b['blind_test'])
 C(sid,'G2_REFERENCE_DISTANCE',b['forbidden_similarity'])
 C(sid,'G3_MATERIAL',b['light_logic'])
 C(sid,'G4_MOTION','One dominant action only: '+b['single_action'])
 C(sid,'G5_MEDIA_REALITY','Do not mark PASS before inspecting actual generated/licensed footage.')
for sid in hboards:
 C(sid,'G1_16_9_INDEPENDENCE','Review independent wide framing, not a crop of 9:16. '+hboards[sid]['idea'])
for e in edges:
 C(e['from']+'-'+e['to'],'G3_TRANSITION',e['visual_claim'])
with open(OUT/'j4_visual_acceptance_v3_0.csv','w',newline='',encoding='utf-8-sig') as f:
 wr=csv.DictWriter(f,fieldnames=['check_id','shot_id','gate','criterion','status','reviewer','evidence_uri','notes']);wr.writeheader();wr.writerows(checks)

# Human-readable director addendum, not overwriting existing prompts.
md=['# J4 v3.0 — Visual Consistency Gate / Director Addendum','',
    '**狀態：DESIGN_ONLY / NOT_GENERATED / NOT_APPROVED。** 此文件增量補充 v2.9，**不覆寫** 25 鏡 Image/Motion/Sound Prompt。',
    '', '## 範圍與不變條件','',
    '- 25 鏡，90,000ms，30 fps，2,700 frames；音訊與付費 Gate 沿用 v2.9。',
    '- 三段核心場景鏈：S02–S04 / S11–S13 / S21–S24，共 10 鏡及 7 條相鄰轉場。',
    '- 另設 7 條跨鏡資產一致性稽核，包含外套 A、光鳥、紙屋與鋼琴。',
    '- 9:16 全部 10 鏡建立構圖，16:9 獨立規劃 S03、S13、S22、S24；未驗收真實生成影像。',
    '- 原始水箱與上市影片照片僅作抽象視覺參考；此包不嵌入原照片或真人影片。',
    '', '## 三組轉場的設計目標', '']
for g in GROUPS:
 md.extend([f"### {g['name']} — {' → '.join(g['shots'])}",g['claim'],''])
 for sid in g['shots']:
  b=vboards[sid]
  md.extend([f'**{sid} {b["title"]}**','',
    f'- 第一影格：{b["first_frame_read"]}',
    f'- 主動作：{b["single_action"]}',
    f'- 鏡頭：{b["lens"]} / {b["camera"]}',
    f'- 光線因果：{b["light_logic"]}',
    f'- 獨立盲測問題：{b["blind_test"]}',
    f'- 避免相似性：{b["forbidden_similarity"]}',
    '- 生成／導演狀態：NOT_RUN / 待審核',''])
md+=['## 16:9 獨立構圖（非自動裁切）','']
for sid,board in hboards.items(): md.extend([f'- **{sid}**：{board["idea"]}'])
md+=['','## 人工盲測與證據 Gate','',
 '1. **G0 結構**：JSON schema、時碼、道具一致性、坐標界限；機械 PASS 僅限此層。',
 '2. **G1 導演線框**：導演審核 9:16 與 16:9 的焦點、負空間、比例，結果需由人簽。',
 '3. **G2 原創距離**：以原始素材與藝術對標比較物件幾何、鏡位、敘事功能；禁止照搬。',
 '4. **G3 資產/轉場**：照片或正式 keyframe 產生後，比對 7 個直接轉場與 7 個跨鏡鎖。',
 '5. **G4 1× 盲測**：觀眾在原鏡長、無字幕、無旁白下說出首影格訊息；真實影片未產生前 NOT_RUN。',
 '6. **G5 音訊/光敏/版權**：聲音原創性、敏感閃爍、實際權利、賽規，均需實物證據。',
 '7. **G6 授權**：Neon 明確 GO → Director 在 AI Video Production Service 發估點 → 當月 9000 點餘裕 → 正式生成。',
 '', '## 未解決阻擋','',
 '- Legacy `pipeline/build_animatic.py` 與 repo `shots.json` 尚未取得：相容性 NOT_TESTED。',
 '- 本包只有線框與構圖設計，不含新圖片、影片、音樂或真實影格。',
 '- 90 秒預告不自動符合原文件記載 3–7 分鐘的競賽影片長度。',
 '- 獨立 16:9 構圖不代表 16:9 已完成影像審核。',
 '- `NOT_RUN` 不得自動升級為 PASS。',
]
(OUT/'DIRECTOR_ADDENDUM_v3_0.md').write_text('\n'.join(md)+'\n')

# Browser-openable interactive schematic board. No user images or generated images used.
json_for_html=json.dumps(artifact,ensure_ascii=False).replace('</','<\\/')
ht=r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>J4 · v3.0 Visual Consistency Gate</title>
<style>
:root{--bg:#0d1015;--surface:#171d24;--surface2:#212833;--line:#374353;--text:#eef3f4;--muted:#a0aebd;--accent:#d6b782;--green:#a8c4b9}
*{box-sizing:border-box} body{background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,'Noto Sans TC',sans-serif;margin:0}
header{padding:22px max(20px,calc((100vw - 1250px)/2));border-bottom:1px solid var(--line)}
h1{margin:0;font-weight:580;font-size:24px;letter-spacing:.01em}header p{color:var(--muted);margin:6px 0 0;font-size:13px}
main{max-width:1280px;margin:auto;padding:22px;display:grid;grid-template-columns:245px minmax(0,1fr);gap:22px}
nav,.panel{background:var(--surface);border:1px solid var(--line);border-radius:15px;padding:17px}
nav{align-self:start;position:sticky;top:16px}h2{font-size:15px;font-weight:650;margin:0 0 12px}h3{font-size:13px;font-weight:650;margin:16px 0 6px;color:var(--accent)}
.group{display:block;margin-bottom:8px;width:100%;text-align:left;background:transparent;border:1px solid var(--line);border-radius:9px;padding:10px;color:var(--text);cursor:pointer}
.group.active{background:var(--surface2);border-color:var(--accent)}.group span{color:var(--muted);display:block;font-size:11px}
.shotbuttons{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}.shotbtn{background:transparent;color:var(--muted);border:1px solid var(--line);padding:7px 10px;border-radius:7px;cursor:pointer}.shotbtn.active{border-color:var(--accent);color:var(--text)}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}.pill{display:inline-block;border:1px solid var(--line);border-radius:7px;padding:4px 9px;color:var(--muted);font-size:12px}
.switch button,.export{background:var(--surface2);color:var(--text);border:1px solid var(--line);border-radius:7px;padding:8px 12px;cursor:pointer}.switch button.active{border-color:var(--accent)}.switch button:disabled{opacity:.3;cursor:not-allowed}
.content{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:20px;margin-top:16px}
.drawpane{background:#111923;border-radius:12px;padding:16px;min-width:0;display:flex;justify-content:center;align-items:center}
#view{width:100%;max-width:520px;max-height:590px;display:block} .side p{margin:4px 0 12px;color:var(--muted)}
.zone{fill:#d6b78222;stroke:#e5c894;stroke-width:2}.zone.secondary{fill:#739cab23;stroke:#95b3bd}.zone.minor{fill:#ffffff12;stroke:#c2cbd3;stroke-dasharray:5 5}
.zone-label{fill:#fffaf0;font-size:16px;paint-order:stroke;stroke:#101820;stroke-width:4px}.canvas{fill:#121a23;stroke:#5c6b78;stroke-width:3px}.gridline{stroke:#3d4a57;stroke-dasharray:3 7;opacity:.35}
.notes{padding:13px;border:1px solid var(--line);border-radius:10px;background:#111720;font-size:12px;line-height:1.65}
.small{font-size:12px;color:var(--muted)}.warn{color:#dbc5a8}.links{border-top:1px solid var(--line);margin-top:18px;padding-top:15px}li{margin:7px 0}
footer{max-width:1280px;margin:auto;padding:0 22px 22px;color:var(--muted);font-size:12px}
@media(max-width:900px){main{grid-template-columns:1fr}nav{position:static}.content{grid-template-columns:1fr}.side{display:grid;grid-template-columns:1fr 1fr;gap:14px}.side>*{min-width:0}}
@media(max-width:580px){.side{display:block}h1{font-size:19px}}
</style></head><body>
<header><h1>J4 / Visual Consistency Gate <span class="pill">v3.0 · DESIGN ONLY</span></h1><p>9:16 十鏡連續性線框 · 四鏡獨立 16:9 · 七條相鄰轉場與七條跨鏡資產鎖｜非生成影格，未通過影像審核</p></header>
<main><nav><h2>場景鏈</h2><div id="groups"></div><h3>鏡頭</h3><div class="shotbuttons" id="shotbuttons"></div><p class="small" id="gclaim"></p><div class="links"><h3>證據狀態</h3><p class="small">靜態構圖：DESIGN_ONLY<br>生成影像：NOT_RUN<br>導演盲測：NOT_RUN<br>授權 Gate：BLOCKED</p></div></nav>
<section class="panel"><div class="topbar"><div><h2 style="font-size:18px;margin:0" id="title"></h2><div class="small" id="time"></div></div><div class="switch"><button id="vertical" class="active" onclick="setAspect('9:16')">9:16 直式</button> <button id="horizontal" onclick="setAspect('16:9')">16:9 獨立構圖</button></div></div>
<div class="content"><div class="drawpane"><svg id="view" role="img" aria-label="原創線框構圖，不是真實影像" xmlns="http://www.w3.org/2000/svg"></svg></div><div class="side"><div><h3>第一影格的訊息</h3><p id="first"></p><h3>主動作</h3><p id="action"></p><h3>鏡頭與光線</h3><p id="camera"></p></div><div><h3>人工盲測</h3><p id="blind"></p><h3>避免照搬</h3><p id="forbidden"></p><div class="notes">此圖只是故事空間與物件視覺權重的設計目標。線框沒有通過 AI 影像生成、版權、原創性或光敏安全驗收。</div></div></div>
<div class="links"><h3>場景轉場／遠距資產關聯</h3><ul id="links"></ul></div></section></main><footer>來源：v2.9 Canonical Shot IR／Composition Gate，及 v2.7 Transition Matrix。任何正式媒體仍需 Neon GO、Director 發估點、每月 9,000 點檢查。</footer>
<script id="data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.getElementById('data').textContent);
let group='origin', shot='S02', aspect='9:16';
const V=Object.fromEntries(data.vertical_9_16.map(b=>[b.shot_id,b]));
const H=Object.fromEntries(data.horizontal_16_9.map(b=>[b.shot_id,b]));
const $=id=>document.getElementById(id);
function setGroup(g){group=g;shot=data.groups.find(x=>x.id===g).shots[0];aspect='9:16';draw()}
function setShot(s){shot=s;aspect='9:16';draw()}
function setAspect(x){if(x==='16:9'&&!H[shot])return;aspect=x;draw()}
function safe(t){return String(t??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function ms(t){let m=Math.floor(t/60000),s=((t%60000)/1000).toFixed(1).padStart(4,'0');return `${m}:${s}`}
function svgText(x,y,t){let txt=safe(t.length>20?t.slice(0,18)+'…':t);return `<text x="${x}" y="${y}" class="zone-label">${txt}</text>`}
function draw(){
 $('groups').innerHTML=data.groups.map(g=>`<button class="group ${group===g.id?'active':''}" onclick="setGroup('${g.id}')">${safe(g.name)}<span>${g.shots.join(' → ')}</span></button>`).join('');
 let g=data.groups.find(x=>x.id===group);$('gclaim').textContent=g.claim;
 $('shotbuttons').innerHTML=g.shots.map(s=>`<button class="shotbtn ${shot===s?'active':''}" onclick="setShot('${s}')">${s}</button>`).join('');
 $('vertical').classList.toggle('active',aspect==='9:16');$('horizontal').classList.toggle('active',aspect==='16:9');$('horizontal').disabled=!H[shot];
 let b=V[shot],h=H[shot],board=aspect==='9:16'?b:h;let W=aspect==='9:16'?360:640,HH=aspect==='9:16'?640:360;
 $('title').textContent=`${shot} · ${b.title}`; $('time').textContent=`${ms(b.start_ms)}–${ms(b.end_ms)} ｜ ${aspect}｜ ${aspect==='16:9'?'獨立編排':'既有直式規格擴展'}`;
 $('first').textContent=aspect==='16:9'?h.idea:b.first_frame_read;
 $('action').textContent=b.single_action;
 $('camera').textContent=`${b.lens} · ${b.camera}。${b.light_logic}`;
 $('blind').textContent=b.blind_test;
 $('forbidden').textContent=b.forbidden_similarity;
 let s=`<rect class="canvas" x="1.5" y="1.5" width="${W-3}" height="${HH-3}" rx="8"/>`;
 for(let i=1;i<3;i++){s+=`<line class="gridline" x1="${W*i/3}" y1="0" x2="${W*i/3}" y2="${HH}"/><line class="gridline" x1="0" y1="${HH*i/3}" x2="${W}" y2="${HH*i/3}"/>`}
 for(let z of board.zones){let [x,y,w,h]=z.bbox;let px=x*W,py=y*HH,pw=w*W,ph=h*HH; let cls=z.priority===1?'zone':z.priority===2?'zone secondary':'zone minor';s+=`<rect class="${cls}" x="${px}" y="${py}" width="${pw}" height="${ph}" rx="6"/>`;s+=svgText(px+5,Math.max(py+19,22),z.name);}
 let view=$('view');view.setAttribute('viewBox',`0 0 ${W} ${HH}`);view.innerHTML=s;
 let links=data.continuity_tests.filter(t=>t.from===shot||t.to===shot);$('links').innerHTML=links.map(x=>`<li><b>${safe(x.from)} → ${safe(x.to)}</b> <span class="small">(${safe(x.kind)})</span><div class="small">${safe(x.visual_claim)}</div></li>`).join('')||'<li>此鏡無本輪新增的直接關聯</li>';
}
draw();
</script></body></html>'''
(OUT/'j4_visual_review_board_v3_0.html').write_text(ht.replace('__DATA__',json_for_html))

# Explicit validator for this contract only.
validator=r'''from pathlib import Path
import json,csv,hashlib
P=Path(__file__).parent; SRC=P
j=json.loads((P/'j4_visual_consistency_ir_v3_0.json').read_text())
base=json.loads((SRC/'baseline_j4_shots_v2_9.json').read_text())
assert j['metadata']['source_shots_sha256']==hashlib.sha256((SRC/'baseline_j4_shots_v2_9.json').read_bytes()).hexdigest()
assert j['metadata']['source_composition_sha256']==hashlib.sha256((SRC/'baseline_j4_keyframe_composition_v2_9.json').read_bytes()).hexdigest()
S={s['id']:s for s in base['shots']}
assert len(S)==25 and base['duration_ms']==90000
assert sum(s['duration_ms'] for s in S.values())==90000
assert all(s['start_ms']%100==s['end_ms']%100==0 for s in S.values())
assert [s['start_ms'] for s in base['shots']]==[0]+[s['end_ms'] for s in base['shots']][:-1]
assert base['shots'][-1]['end_ms']==90000
assert j['metadata']['no_media_generated'] and j['metadata']['paid_gate'].startswith('BLOCKED')
assert len(j['vertical_9_16'])==10 and len(j['horizontal_16_9'])==4
assert len(j['continuity_tests'])==14
V={b['shot_id']:b for b in j['vertical_9_16']};H={b['shot_id']:b for b in j['horizontal_16_9']}
assert set(H)=={'S03','S13','S22','S24'}
assert set(V)==set(sum([g['shots'] for g in j['groups']],[]))
for b in list(V.values())+list(H.values()):
 assert b['render_review_state']=='NOT_RUN_NO_RENDER'
 assert b['zones']
 for z in b['zones']:
  x,y,w,h=z['bbox'];assert 0<=x<1 and 0<=y<1 and w>0 and h>0 and x+w<=1.0000001 and y+h<=1.0000001,(b['shot_id'],z)
for e in j['continuity_tests']:
 assert e['from'] in S and e['to'] in S and e['design_review_state']=='NOT_RUN' and e['render_review_state']=='NOT_RUN_NO_MEDIA'
 if e['kind']=='adjacent':
  assert S[e['from']]['end_ms']==S[e['to']]['start_ms']==e['at_ms']
  assert e['at_frame']==e['at_ms']*30//1000
with open(P/'j4_visual_acceptance_v3_0.csv',encoding='utf-8-sig') as f:
 checks=list(csv.DictReader(f))
assert checks and all(c['status']=='NOT_RUN' for c in checks)
assert len([e for e in j['continuity_tests'] if e['kind']=='adjacent'])==7
assert len([e for e in j['continuity_tests'] if e['kind']=='nonadjacent_asset'])==7
print('PASS: baseline hash, 25 shot/90s, 10 vertical + 4 independently authored horizontal designs, 14 continuity checks,',len(checks),'unreviewed criteria, NO media generation')
'''
(OUT/'validate_v3_0.py').write_text(validator)
readme=f'''# J4 v3.0 — Visual Consistency Gate\n\n**DESIGN_ONLY / NOT_GENERATED / NOT_APPROVED.**\n\n## Scope\n- 25 shots, 90.000 seconds, 30 fps unchanged. Canonical `j4_shots_v2_9.json` is read-only.\n- 3 story chains, 10 adjacent reviewed shots, 7 immediate transitions and 7 long-range asset checks.\n- 10 original 9:16 schematic compositions; 4 separately authored 16:9 designs (S03/S13/S22/S24), not crops.\n- 14 transition records with all real-media evidence NOT_RUN; {len(checks)} additional review criteria all NOT_RUN.\n- Baseline snapshots are bundled so `validate_v3_0.py` runs standalone after extraction; these are read-only provenance copies, not new canonical files.\n- New files: `j4_visual_consistency_ir_v3_0.json`, `j4_transition_acceptance_v3_0.csv`, `j4_visual_acceptance_v3_0.csv`, `DIRECTOR_ADDENDUM_v3_0.md`, `j4_visual_review_board_v3_0.html`, `validate_v3_0.py`.\n\n## Gates\nNo image, video, audio, or model inference was generated in this phase. Do not portray schematic or source-media inspection as human artistic PASS. Paid generation requires Neon GO, Director estimation in AI Video Production Service, current-month 9000-credit headroom, and rights/contest review.\n\n## Legacy compatibility\n`pipeline/build_animatic.py` and canonical repo source have not been provided; Legacy Adapter = NOT_TESTED. This v3.0 package is a non-destructive addendum, not a repo update.\n\n## Art direction safeguards\n- Never reuse user-source square glass tank geometry, real IPO-stage layout, real people, recognizable game scenes, or protected artist-specific installation design.\n- S21 coat A is on chair already at first frame; its sleeve is never on the hand handing over the key.\n- S22 first-frame paper house and bridge must both be legible; 3-second action is one finger steadying the bridge.\n- S24 coat held from frame 0, rain already falling, only bird settles.\n- S18 remains a single accessibility-conscious low-brightness appearance with original global sound cut at 63.700s.\n\n## Mechanical verification\nRun `python validate_v3_0.py`. It validates file hashes, 90-second continuous baseline, independent compositions, zone geometry, 7 + 7 continuity tests and NOT_RUN media states; it does not certify final film quality.\n'''
(OUT/'README_v3_0.md').write_text(readme)

# Create archive after all files exist.
archive=ROOT/'j4_museum_v3_0_bundle.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file():z.write(p,arcname=f'j4_museum_v3_0/{p.name}')
print('CREATED',archive,'files',len(list(OUT.iterdir())),'acceptance',len(checks))
