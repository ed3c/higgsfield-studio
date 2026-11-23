from pathlib import Path
import json,csv,hashlib,zipfile,copy,html,datetime
root=Path('/mnt/data'); src=root/'j4_museum_v3_0'; out=root/'j4_museum_v3_1';out.mkdir(exist_ok=True)
source_json=src/'j4_visual_consistency_ir_v3_0.json'; baseline_shots=src/'baseline_j4_shots_v2_9.json'
base=json.loads(source_json.read_text(encoding='utf-8'))
shots=json.loads(baseline_shots.read_text(encoding='utf-8'))['shots']; S={s['id']:s for s in shots}
vert=base['vertical_9_16']; horiz=base['horizontal_16_9']

# Only proposed changes to zone design, no source mutation, no media review or approval.
changes={
 'S11': {
   'paper_house_hint':{'bbox':[0.52,0.63,0.19,0.12],'priority':2},
 },
 'S21':{
   'single_brass_key':{'bbox':[0.44,0.47,0.16,0.12]},
 },
 'S22':{
   'real_city_window':{'bbox':[0.10,0.09,0.82,0.25]},
   'salaryman':{'bbox':[0.07,0.42,0.31,0.45]},
   'fragile_bridge':{'bbox':[0.41,0.68,0.27,0.13]},
   'empty_paper_house':{'bbox':[0.70,0.46,0.18,0.19]},
   'local_compute':{'bbox':[0.84,0.36,0.09,0.07]}
 },
 'S24':{
   'coat_A':{'bbox':[0.31,0.35,0.40,0.34]},
   'bird_entry':{'bbox':[0.54,0.25,0.15,0.13]},
 }
}
reasons={
'S02':('保留交換碗的手部接觸，避免夜市被讀成旅遊風景','維持碗交接與水面反射同框；一開始就有人的動作'),
'S03':('保留創辦人相對巨大光學薄膜的小尺度，建立不對等關係','不改幾何；嚴格排除四方形懸浮水箱與原素材鏡位'),
'S04':('金屬光鳥必須與行李箱共同被辨識，但不形成徽記','細線光鳥維持小尺度；片頭不使用完整鳥徽輪廓'),
'S11':('紙屋應是跨鏡伏筆，不應與自動化產線爭奪主焦點','紙屋 priority 1→2；空凳與機器仍是第一視覺層'),
'S12':('線的外接矩形面積不等於線本身粗細與可讀性','保留區域；要求紅線可沿實體導線環被追蹤至兩端'),
'S13':('晶圓小但不需主導畫面；應由反光而非放大呈現','維持技師／鋼琴為焦點；晶圓僅做工藝線索'),
'S21':('鑰匙 1.4% 區域過小，恐與雙手重疊難辨','鑰匙辨識區微幅提高；雙手先後接觸須明確'),
'S22':('紙橋、空屋各僅約 2–3% 視覺面積，三秒內負荷較高','略增紙橋與空屋區域、減少城市窗比重；不加第二動作'),
'S23':('用同一場景、換服裝、延遲反射表達人物的時間位移','不改區域；光學遲延後製處理，不生成超自然人體複本'),
'S24':('鳥要小但降落路徑清楚，外套「空」是首影格核心','外套增大，鳥靠近肩部；雨自 0 秒已存在')
}
checks={
'S02':['首秒看出人與人交換食物，不只是觀光夜市','普通夜市燈泡有可見物理光源','水紋可與 S03 的光學反射剪接'],
'S03':['一眼看出背影人物與開放式薄膜的尺度差','結構不能是方形懸浮水箱','水滴與反射的延時有後製設計，不宣稱光速變慢'],
'S04':['細金屬造物與行李箱都在首影格','光鳥不可長成電影鳥徽','鎢絲反射能接到 S24 的原創道具'],
'S11':['觀眾先注意機器與空凳','紙屋是第二層伏筆','人類勞動不被刻畫成沒有價值'],
'S12':['紅線可追到電話聽筒與遠端方向','紅線不是魔法蛛網','兩張桌子都無人但存在拉力'],
'S13':['第一影格有舊鋼琴、技師與臨海測試廳','晶圓反光可被看見但非畫面中心','畫面不複製真實受災鋼琴或裝置藝術'],
'S21':['鑰匙僅一把且不被手指遮斷','外套 A 已掛在椅上，不能瞬間移動','布料與手掌自然接觸'],
'S22':['0 秒有人、紙橋、紙屋同時存在','唯一動作是一根指頭扶住橋','空屋沒有居民；遠端本地 AI 不搶焦點'],
'S23':['同一人物與光學建築可辨認','人物已脫下主線外套','反射滯後不形成超自然分身'],
'S24':['0 秒外套已舉起且明顯是空的','雨在第一影格已出現','光鳥降落軌跡獨立可辨，不變成徽章'],
}
brief={
'S02':'生活先於技術：碗從一隻手到另一隻手',
'S03':'集中之光：人物在開放式薄膜前渺小',
'S04':'脆弱離開：細線造物從日常光源脫離',
'S11':'自動化仍運轉：空凳與紙屋留下人的痕跡',
'S12':'缺席的談判：紅線在兩張無人桌間受力',
'S13':'技術失準：技師與受潮琴鍵同處測試廳',
'S21':'制度交接：唯一鑰匙完成一次轉移',
'S22':'勞動的孤獨：一根手指維持紙做的橋',
'S23':'回憶的延遲：人物移動，反射稍後才追上',
'S24':'共同承接：人群已舉起空衣，光鳥才降落',
}
# build proposed IR
new=copy.deepcopy(base)
new['metadata']=dict(new['metadata'])
new['metadata']['version']='v3.1-G1-DESIGN-CANDIDATE'
new['metadata']['status']='G1_LAYOUT_CANDIDATE_ONLY_NOT_HUMAN_SIGNED_NOT_RENDERED'
new['metadata']['parent_v3_0_sha256']=hashlib.sha256(source_json.read_bytes()).hexdigest()
new['metadata']['scope']='10 vertical proposals; 4 source-authored horizontal compositions unchanged; 14 continuity records intact'
new['metadata']['approval_scope']='G1 layout only, never authorizes image/video/audio generation'
new['metadata']['no_media_generated']=True
new['metadata']['paid_gate']='BLOCKED; Neon approval + Director estimate posted + 9000 headroom + rights checks'
for rec in new['vertical_9_16']:
 sid=rec['shot_id']
 rec['design_state']='G1_PROPOSED_NOT_APPROVED'
 rec['render_review_state']='NOT_RUN_NO_MEDIA'
 rec['g1_intent_zh']=brief[sid]
 rec['g1_risk_zh']=reasons[sid][0]
 rec['g1_proposal_zh']=reasons[sid][1]
 rec['g1_blind_questions_zh']=checks[sid]
 for z in rec['zones']:
  d=changes.get(sid,{}).get(z['name'])
  if d:z.update(d)
for rec in new['horizontal_16_9']:
 rec['design_state']='UNCHANGED_FROM_V3_0_SEPARATELY_AUTHORED'
 rec['render_review_state']='NOT_RUN_NO_MEDIA'
for e in new['continuity_tests']:
 e['design_review_state']='NOT_RUN'
 e['render_review_state']='NOT_RUN_NO_MEDIA'
(out/'j4_g1_layout_candidate_v3_1.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# compare each shot and highlight differences
byold={x['shot_id']:x for x in vert};bynew={x['shot_id']:x for x in new['vertical_9_16']}
attention=[]
for sid in [x['shot_id'] for x in vert]:
 b=byold[sid];n=bynew[sid]
 bmap={z['name']:z for z in b['zones']}
 for z in n['zones']:
  oz=bmap[z['name']];old_pct=round(oz['bbox'][2]*oz['bbox'][3]*100,2);new_pct=round(z['bbox'][2]*z['bbox'][3]*100,2)
  attention.append({'shot_id':sid,'zone':z['name'],'prior_area_pct':old_pct,'candidate_area_pct':new_pct,'prior_priority':oz['priority'],'candidate_priority':z['priority'],'required_first_frame':z['required_first_frame'],'changed':str(z['bbox']!=oz['bbox'] or z['priority']!=oz['priority']),'note':reasons[sid][1] if z['bbox']!=oz['bbox'] or z['priority']!=oz['priority'] else '未修改；維持 v3.0 位置'})
with (out/'j4_g1_attention_audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(attention[0]));w.writeheader();w.writerows(attention)

# 10x4 human review criteria; intentionally NOT_RUN
rows=[]
for sid in [x['shot_id'] for x in vert]:
 s=S[sid]
 for i,(name,question) in enumerate([
  ('first_frame_500ms',checks[sid][0]),('single_action_at_1x',checks[sid][1]),('physical_and_ip_distance',checks[sid][2]),('transition_coherence',f"以 1× 正常速度連續播放前後鏡，能否辨識 {s['in_transition']} → {s['out_transition']}，且不靠字幕解說？")
 ],1):
  rows.append({'check_id':f'V31-{sid}-G1-{i:02d}','shot_id':sid,'start_ms':s['start_ms'],'end_ms':s['end_ms'],'dimension':name,'question':question,'status':'NOT_RUN','reviewer':'','evidence_uri':'','notes':'','scope':'G1 composition only; never generation approval'})
with (out/'j4_g1_review_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# shot-specific timing updates; use frames to prevent half-frame. Keep original structure.
timing={
'S02':[(0,30,'建立夜市的「人際交換」'),(30,90,'碗由一人傳到另一人'),(90,120,'水反射接 S03')],
'S03':[(0,45,'背影人物與非盒狀薄膜成立'),(45,105,'一滴水沿薄膜移動'),(105,150,'地面冷光稍晚回應')],
'S04':[(0,33,'行李箱與鎢絲小物共存'),(33,96,'光鳥受微風抬起'),(96,120,'離框留下暖反射')],
'S11':[(0,30,'機械與空凳讀得見'),(30,90,'水滴落下，產線繼續'),(90,120,'紙屋伏筆仍是次焦點')],
'S12':[(0,24,'紅線連接兩張空桌'),(24,72,'聽筒被拉動數毫米'),(72,90,'線仍有殘留振動')],
'S13':[(0,36,'鋼琴與技師、晶圓存在'),(36,96,'按鍵未正常回彈'),(96,120,'機械泛音留下')],
'S21':[(0,24,'雙手與唯一鑰匙都被看見'),(24,78,'鑰匙完整換手'),(78,120,'視線轉往已掛在椅上的外套')],
'S22':[(0,18,'紙地景、橋、空屋首影格已建立'),(18,51,'只有一指扶紙橋'),(51,75,'紙橋穩住'),(75,90,'空屋仍無人、聲音接 S23')],
'S23':[(0,30,'同一空間與不穿外套人物'),(30,93,'一步向前，反射稍晚跟上'),(93,135,'兩個遠景物件退出'),],
'S24':[(0,24,'空外套已舉起，雨已在下'),(24,60,'唯一主動作：光鳥降落'),(60,90,'共同承接的手保持不對拍')],
}
frame_rows=[]
for sid,items in timing.items():
 for f0,f1,claim in items:
  frame_rows.append({'shot_id':sid,'shot_global_start_frame':S[sid]['start_ms']*30//1000,'local_frame_in':f0,'local_frame_out_exclusive':f1,'global_frame_in':S[sid]['start_ms']*30//1000+f0,'global_frame_out_exclusive':S[sid]['start_ms']*30//1000+f1,'purpose_zh':claim,'status':'PROPOSED_NOT_RENDERED'})
with (out/'j4_g1_30fps_action_beats.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(frame_rows[0]));w.writeheader();w.writerows(frame_rows)

# maintain 14 edges with plain audit status, no false approvals
edges=[]
for e in base['continuity_tests']:
 edges.append({'id':e['id'],'kind':e['kind'],'from':e['from'],'to':e['to'],'mechanism':e['mechanism'],'intent':e['visual_claim'],'evidence_state':'NOT_RUN_NO_MEDIA','g1_note':'先確認示意線框中「接力元素」的空間位置，真實影格接入後再檢查','reviewer':'','evidence_uri':''})
with (out/'j4_g1_continuity_review.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(edges[0]));w.writeheader();w.writerows(edges)

# versioned source snapshots so standalone archive verifies by hash
for name,path in [('baseline_j4_visual_consistency_ir_v3_0.json',source_json),('baseline_j4_shots_v2_9.json',baseline_shots)]:
 (out/name).write_bytes(path.read_bytes())

manifest={
 'version':'3.1','scope':'G1 Director Composition PRE-FLIGHT ONLY',
 'source_sha256':{'v3.0_visual_consistency_ir':hashlib.sha256(source_json.read_bytes()).hexdigest(),'v2.9_shot_ir':hashlib.sha256(baseline_shots.read_bytes()).hexdigest()},
 'total_shots':25,'source_reviewed_shots':10,'source_continuity_edges':14,'changed_shots':sorted(changes),'review_checks':len(rows),'status':'DESIGN_CANDIDATE_NOT_APPROVED','rendered_assets':0,'spent_credits':0,'legacy_pipeline':'NOT_TESTED','rights_review':'NOT_RUN',
}
(out/'j4_g1_manifest_v3_1.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# director doc
sections=['''# J4 v3.1 — G1 Director Composition Preflight

**狀態：DESIGN CANDIDATE / G1 HUMAN REVIEW NOT_RUN / NO MEDIA GENERATED / PAID GENERATION BLOCKED。**

## 範圍與承繼

- 來源：v3.0 Visual Consistency IR、v2.9 Canonical Shot IR；原始檔維持不變。
- 25 鏡、90.000 秒、30fps / 2700 影格，不改時碼。
- 審核 3 條場景鏈中的 10 鏡、7 個相鄰轉場及 7 個跨鏡資產檢查。
- 10 個 9:16 線框；四張 16:9 獨立構圖維持 v3.0 版本，沒有擅自宣告已通過。
- 輸出 40 項 G1 人工審核條件，**全部 NOT_RUN**。

## G1 判斷規則

1. **首影格 0.5 秒：** 單獨呈現第一張畫面、不顯示標題、字幕或 Prompt。受試者能說出故事主體，不能靠場景名稱猜。
2. **原鏡長、1× 無聲：** 優先檢查一個主要動作，不因輔助動作而失去焦點。
3. **相鄰鏡頭連看：** 前鏡提供的材料、光線、聲音或手勢，能在下一鏡找到可辨認的結果。
4. **來源距離：** 人物、裝置、藝術參考與原始照片不能在幾何、鏡位及具有辨識度的造型上高度近似。
5. **人工評分** 必須標明審核者、實際素材以及可重現的證據，不能用本版線框代替真實影格審核。

## 本輪提出的構圖 Delta
''']
for sid in [x['shot_id'] for x in vert]:
 sections.append(f'\n### {sid} — {S[sid]["title_en"]}\n\n**敘事判準：**{brief[sid]}。\n\n**風險：**{reasons[sid][0]}。\n\n**建議：**{reasons[sid][1]}。\n\n**盲測問題：**'+ '；'.join(checks[sid])+'。\n')
sections.append('''
## 關鍵例外與法務/製作閘口

- S11 紙屋降為次焦點，不代表移除 S11→S22 的紙摺語法伏筆。
- S22 紙屋與紙橋的面積是 **bounding-box 面積**，不是觀眾感知尺寸、實際物體畫素或辨識率；G1 仍需要真實影格。
- S24 微小光鳥維持原創非徽章形式，外套 A 與 S21 的同一資產鎖；**不是現實人物復職的紀錄**。
- S03 只使用原始水箱的抽象方法（水光、凝結、空間性）；拒絕原物的四方形玻璃箱、吊線鏡位、白色噴霧主體。
- S13 原始當代藝術作品僅提供時間/自然/樂器受損的思考方式，不重製已知受災物件。
- 沒有真實圖像、動作、聲音生成。影像與版權、比賽合規都 NOT_RUN。
- 90 秒預告本身仍未達原規劃 3–7 分鐘的正式投稿片長要求。
- **任何付費／生成前：Neon 明確 GO → Director 在「AI Video Production Service」發估點 → 確認 9,000 月額度可用 → 權利/比賽審查。**
- `pipeline/build_animatic.py` 未取得，legacy schema 相容性 NOT_TESTED。

## 下一個合法動作

導演先對 10 個建議構圖進行 G1 人工簽核（可拒絕/回修），再準備獨立的零生成素材 G2 原創距離比較與 G3 真實 keyframe 一致性驗收。**不得把簽核 G1 當成批准生成。**
''')
(out/'DIRECTOR_G1_ADDENDUM_v3_1.md').write_text('\n'.join(sections),encoding='utf-8')

# HTML review tool: static schematics only. all review decisions local and exportable.
minimal_data={
 'shots':[
  {'id':s['shot_id'],'title':S[s['shot_id']]['title_en'],'title_zh':S[s['shot_id']]['title_zh'],'start_ms':s['start_ms'],'end_ms':s['end_ms'],'first_frame':s['first_frame_read'],'risk':reasons[s['shot_id']][0],'proposal':reasons[s['shot_id']][1], 'blind':checks[s['shot_id']], 'orig':s['zones'], 'candidate':bynew[s['shot_id']]['zones'],'horizontal': next((h['zones'] for h in horiz if h['shot_id']==s['shot_id']),None),'beats':[r for r in frame_rows if r['shot_id']==s['shot_id']]}
  for s in vert
 ],
 'meta':{'version':'v3.1','review':'G1 DESIGN PROPOSAL, NOT RUN WITH ACTUAL MEDIA','source':'v3.0'}
}
payload=json.dumps(minimal_data,ensure_ascii=False).replace('</','<\\/')
css='''
:root{color-scheme:dark;--bg:#0c1015;--panel:#151c24;--panel2:#1e2833;--ink:#f0ede4;--muted:#aab8bd;--line:#354655;--warm:#dcc49f;--cold:#92b7c4;--alert:#e4b589}*{box-sizing:border-box}body{font-family:ui-sans-serif,system-ui,-apple-system,"Noto Sans TC",sans-serif;margin:0;background:var(--bg);color:var(--ink)}header{padding:28px max(20px,calc((100vw - 1320px)/2));border-bottom:1px solid var(--line);background:linear-gradient(120deg,#101a24,#0c1015)}h1{margin:2px 0 8px;font-weight:590;font-size:clamp(25px,3vw,38px);letter-spacing:-.03em}header p{max-width:900px;color:var(--muted);line-height:1.7;margin:6px 0}main{max-width:1340px;margin:auto;padding:20px;display:grid;gap:18px}.notice{padding:13px 16px;background:#25262a;border-left:3px solid var(--warm);color:#e2d3b9;border-radius:4px}.topbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;padding:14px;background:var(--panel);border:1px solid var(--line);border-radius:10px}select,button,textarea,input{background:#202b34;border:1px solid #526372;border-radius:7px;color:var(--ink);font:inherit;padding:8px 10px}button{cursor:pointer}button:hover{background:#2d3943}select{max-width:100%}.meta{font-size:13px;color:var(--muted)}.flex{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.boards{display:grid;grid-template-columns:1fr 1fr;gap:14px}.board{border:1px solid var(--line);border-radius:11px;background:var(--panel);padding:12px;display:grid;gap:12px}.board h2{font-size:15px;margin:0;line-height:1.5}.plotwrap{display:grid;place-items:center;min-height:430px;background:#0a0e13;border:1px solid #2e3944;border-radius:8px;padding:12px}.plotwrap svg{height:min(62vh,570px);max-width:100%;width:auto;display:block}.legend{display:grid;gap:4px;font-size:12px;color:#b8c3ca}.legend-line{display:flex;gap:8px;align-items:baseline}.legend-index{font-weight:700;color:#f9e2bb;min-width:20px}.details{display:grid;grid-template-columns:1fr 1fr;gap:14px}.panel{border:1px solid var(--line);border-radius:10px;background:var(--panel);padding:18px}.panel h3{margin:0 0 10px;font-size:16px}.panel p{line-height:1.65}.panel li{line-height:1.65;margin-bottom:7px}.steps{display:grid;gap:8px}.step{display:grid;grid-template-columns:68px 1fr;gap:10px;align-items:start;padding:8px;border-bottom:1px solid #273441}.step em{font-style:normal;color:#dbc4a3;font-size:12px}.review{display:grid;gap:10px}.review textarea{width:100%;min-height:85px;resize:vertical}footer{padding:18px 24px;margin-top:28px;color:#8a9ba4;border-top:1px solid #34404d;font-size:13px}@media(max-width:900px){.boards,.details{grid-template-columns:1fr}.plotwrap svg{height:min(48vh,500px)}header{padding:22px}}
'''
script='''
const D = __PAYLOAD__;
const $=s=>document.querySelector(s); const choose=$('#shot');
const draft={};
for(const s of D.shots){let o=document.createElement('option');o.value=s.id;o.textContent=s.id+'｜'+s.title_zh;choose.appendChild(o);draft[s.id]={status:'NOT_RUN',reviewer:'',notes:''};}
function makeSVG(zones,aspect){
 let W=aspect==='9:16'?900:1600,H=aspect==='9:16'?1600:900;
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('role','img');svg.setAttribute('aria-label','原創導演線框，非實際生成畫面');
 const elem=(tag,attrs)=>{let e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(let [k,v] of Object.entries(attrs))e.setAttribute(k,v);svg.appendChild(e);return e};
 elem('rect',{x:0,y:0,width:W,height:H,fill:'#0d131a'});
 for(let i=1;i<4;i++){elem('line',{x1:W*i/4,y1:0,x2:W*i/4,y2:H,stroke:'#24323d','stroke-width':2,'stroke-dasharray':'4 12'});elem('line',{x1:0,y1:H*i/4,x2:W,y2:H*i/4,stroke:'#24323d','stroke-width':2,'stroke-dasharray':'4 12'});}
 zones.forEach((z,i)=>{let [x,y,w,h]=z.bbox;let color=z.priority===1?'#d8b68a':z.priority===2?'#86b7c4':'#728b9f';let rect=elem('rect',{x:x*W,y:y*H,width:w*W,height:h*H,fill:color,'fill-opacity':z.priority===1?0.17:0.10,stroke:color,'stroke-width':z.priority===1?4:2,rx:4});let text=elem('text',{x:x*W+10,y:y*H+32,fill:'#ffffff','font-size':Math.max(19,Math.min(28,w*W*.24)),'font-weight':700});text.textContent=String(i+1);});
 return svg;
}
function legend(el,zones){el.replaceChildren(...zones.map((z,i)=>{let r=document.createElement('div');r.className='legend-line';let a=document.createElement('span');a.className='legend-index';a.textContent=(i+1)+'.';let b=document.createElement('span');b.textContent=z.name+' · P'+z.priority+(z.required_first_frame?' · 首影格':' · 次要');r.append(a,b);return r;}));}
function show(){
 let s=D.shots.find(x=>x.id===choose.value)||D.shots[0];let aspect=$('#aspect').value;
 $('#shotTitle').textContent=s.id+'｜'+s.title_zh+' · '+s.title;
 $('#frameTime').textContent=`${(s.start_ms/1000).toFixed(1)}–${(s.end_ms/1000).toFixed(1)}s · ${((s.end_ms-s.start_ms)*30/1000).toFixed(0)} frames`;
 $('#story').textContent=s.first_frame;$('#risk').textContent=s.risk;$('#proposal').textContent=s.proposal;
 let z0=aspect==='9:16'?s.orig:s.horizontal;
 let z1=aspect==='9:16'?s.candidate:s.horizontal;
 $('#beforeWrap').replaceChildren(z0?makeSVG(z0,aspect):document.createTextNode('v3.0 尚無此鏡獨立 16:9 構圖；禁止以 9:16 裁切假冒。'));
 $('#afterWrap').replaceChildren(z1?makeSVG(z1,aspect):document.createTextNode('v3.1 未建立此鏡 16:9 設計，保持 NOT_RUN。'));
 legend($('#beforeLegend'),z0||[]);legend($('#afterLegend'),z1||[]);
 $('#changes').textContent=aspect==='9:16'?s.proposal:'橫式版本沿用 v3.0 既有獨立設計，這一輪沒有提出橫式修改。';
 $('#blind').replaceChildren(...s.blind.map(v=>{let li=document.createElement('li');li.textContent=v;return li;}));
 $('#beats').replaceChildren(...s.beats.map(b=>{let r=document.createElement('div');r.className='step';let t=document.createElement('em');t.textContent=`${(b.local_frame_in/30).toFixed(1)}–${(b.local_frame_out_exclusive/30).toFixed(1)}s`;let v=document.createElement('span');v.textContent=b.purpose_zh;r.append(t,v);return r;}));
 let f=draft[s.id];$('#status').value=f.status;$('#reviewer').value=f.reviewer;$('#notes').value=f.notes;
}
function save(){let s=choose.value;draft[s]={status:$('#status').value,reviewer:$('#reviewer').value,notes:$('#notes').value};$('#msg').textContent='此頁僅暫存 G1 人工記錄；請匯出 JSON 留存。';}
choose.addEventListener('change',show);$('#aspect').addEventListener('change',show);
for(let a of ['status','reviewer','notes'])$('#'+a).addEventListener('change',save);
$('#export').addEventListener('click',()=>{save();let result={project:'J4',version:'v3.1',scope:'G1 human composition review ONLY, NOT permission for generation',review:Object.entries(draft).map(([shot_id,r])=>({shot_id,...r}))};let blob=new Blob([JSON.stringify(result,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='j4_g1_director_review_export.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),500);});
show();
'''.replace('__PAYLOAD__',payload)
page=f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>J4 v3.1 G1 Director Composition Review</title><style>{css}</style></head>
<body><header><div class="meta">J4 / ASYNC: SUCCESSION · Museum Cinema v3.1</div><h1>G1 導演構圖預審</h1><p>比較 v3.0 線框與 v3.1 的十鏡建議配置。這是 <b>資料層線框</b>，不是真實影格或藝術驗收；所有正式媒體審核仍然 NOT_RUN。</p></header>
<main><div class="notice">DESIGN ONLY · NO MEDIA GENERATED · HUMAN G1 NOT_RUN · 生成授權仍 BLOCKED</div>
<div class="topbar"><label>鏡頭 <select id="shot"></select></label><label>構圖比例 <select id="aspect"><option value="9:16">9:16 直式</option><option value="16:9">16:9 獨立橫式（僅四鏡）</option></select></label><strong id="shotTitle"></strong><span class="meta" id="frameTime"></span></div>
<section class="boards"><div class="board"><h2>v3.0 基準線框</h2><div class="plotwrap" id="beforeWrap"></div><div class="legend" id="beforeLegend"></div></div><div class="board"><h2>v3.1 建議構圖（未核准）</h2><div class="plotwrap" id="afterWrap"></div><div class="legend" id="afterLegend"></div></div></section>
<section class="details"><div class="panel"><h3>第一影格應說出的故事</h3><p id="story"></p><h3>現有風險</h3><p id="risk"></p><h3>構圖修訂</h3><p id="proposal"></p><p class="meta" id="changes"></p></div><div class="panel"><h3>30fps 內部動作節拍</h3><div class="steps" id="beats"></div><h3>無字幕盲測問題</h3><ol id="blind"></ol></div></section>
<section class="panel"><h3>導演人工 G1 記錄（不等於准許生成）</h3><div class="review"><div class="flex"><label>構圖狀態 <select id="status"><option value="NOT_RUN">NOT_RUN（預設）</option><option value="G1_ACCEPTED_BY_REVIEWER">G1 人工接受構圖</option><option value="G1_REVISION_REQUIRED">G1 需要修訂</option><option value="G1_REJECTED">G1 拒絕</option></select></label><label>審核者 <input id="reviewer" placeholder="人工填寫" aria-label="審核者"></label></div><label>依據與修訂備註<textarea id="notes" placeholder="觀看時間、實際影格來源、需要調整的區域……"></textarea></label><div class="flex"><button id="export">匯出本次審核 JSON</button><span class="meta" id="msg">此審核頁不會自動核准生成。</span></div></div></section>
</main><footer>v3.1 是無媒體的原創線框比較。所有藝術、權利、競賽及影片生成相關閘口保持未通過。原 repository 未變更。</footer>
<script>{script}</script></body></html>'''
(out/'j4_g1_review_board_v3_1.html').write_text(page,encoding='utf-8')

readme='''# J4 v3.1 G1 Composition Preflight

**No generated images, videos or music. Zero Higgsfield spend. No repository writes.**

這一輪承接 v3.0 Visual Consistency Gate，對 10 鏡做構圖線框的**靜態診斷與建議修改**。G1 導演人工簽核、實際影格可讀性、IP 比較、權利與比賽合規均維持 NOT_RUN。

## Files
- `j4_g1_review_board_v3_1.html`: 10-shot baseline/candidate wireframe comparison with 9:16 and four unchanged independently-authored 16:9 boards; exports human review to JSON, does not authorize generation.
- `j4_g1_layout_candidate_v3_1.json`: proposed delta over v3.0; baseline source unmodified.
- `j4_g1_attention_audit.csv`: bounding-box area percentages, **not actual recognizability measurements**.
- `j4_g1_30fps_action_beats.csv`: key intervals in 30fps frames; timecodes unchanged.
- `j4_g1_review_matrix.csv`: 40 questions, all NOT_RUN.
- `j4_g1_continuity_review.csv`: 14 adjacent/cross-shot relations, all NOT_RUN.
- `DIRECTOR_G1_ADDENDUM_v3_1.md`: creative judgments and next steps.
- `validate_v3_1.py`: verifies provenance hashes, 25 shot timing, proposals, 14 relations, and NOT_RUN statuses.

## Key proposed changes
- S11 paper-house priority P1 → P2 (easter egg rather than dominant focus).
- S21 brass-key zone 1.43% → 1.92% of 9:16 frame bounding box.
- S22 paper-bridge 2.53% → 3.51%, empty house 2.88% → 3.42%, fewer upper-window distractions.
- S24 main coat 10.80% → 13.60%, wire bird stays small and its movement alone defines the shot.

### Limitation
Percentages are zone bbox dimensions, not pixel segmentation or experimental viewer-recognition rates. Do not mark G1 PASS until a human reviews actual frames at intended duration. No old pipeline compatibility test was possible; `pipeline/build_animatic.py` has not been supplied.

## Governance
Neon explicit approval -> Director estimate in AI Video Production Service -> current month 9000-credit headroom -> rights/contest screening -> then permitted generation. This G1 bundle is not any such approval.
'''
(out/'README_v3_1.md').write_text(readme,encoding='utf-8')

validator='''from pathlib import Path
import json,csv,hashlib
P=Path(__file__).resolve().parent
base=P/'baseline_j4_visual_consistency_ir_v3_0.json'
shot=P/'baseline_j4_shots_v2_9.json'
man=json.loads((P/'j4_g1_manifest_v3_1.json').read_text())
a=json.loads(base.read_text());b=json.loads((P/'j4_g1_layout_candidate_v3_1.json').read_text());timeline=json.loads(shot.read_text())
assert hashlib.sha256(base.read_bytes()).hexdigest()==man['source_sha256']['v3.0_visual_consistency_ir']
assert hashlib.sha256(shot.read_bytes()).hexdigest()==man['source_sha256']['v2.9_shot_ir']
assert len(timeline['shots'])==25 and sum(x['duration_ms'] for x in timeline['shots'])==90000
assert timeline['shots'][0]['start_ms']==0 and timeline['shots'][-1]['end_ms']==90000
assert all(timeline['shots'][i]['end_ms']==timeline['shots'][i+1]['start_ms'] for i in range(24))
assert len(a['vertical_9_16'])==len(b['vertical_9_16'])==10
assert len(a['horizontal_16_9'])==len(b['horizontal_16_9'])==4
assert len(b['continuity_tests'])==14
assert man['status']=='DESIGN_CANDIDATE_NOT_APPROVED' and man['rendered_assets']==man['spent_credits']==0
assert b['metadata']['no_media_generated'] and 'BLOCKED' in b['metadata']['paid_gate']
for rec in b['vertical_9_16']+b['horizontal_16_9']:
 assert rec['render_review_state']=='NOT_RUN_NO_MEDIA'
 for z in rec['zones']:
  x,y,w,h=z['bbox']
  assert 0<=x<1 and 0<=y<1 and w>0 and h>0 and x+w<=1 and y+h<=1,(rec['shot_id'],z)
for e in b['continuity_tests']:
 assert e['design_review_state']=='NOT_RUN' and e['render_review_state']=='NOT_RUN_NO_MEDIA'
V={s['shot_id']:s for s in b['vertical_9_16']}
assert len(V)==10
assert next(x for x in V['S11']['zones'] if x['name']=='paper_house_hint')['priority']==2
assert (next(x for x in V['S22']['zones'] if x['name']=='fragile_bridge')['bbox'][2] > .23)
assert (next(x for x in V['S24']['zones'] if x['name']=='coat_A')['bbox'][2] > .36)
for fn,count in [('j4_g1_review_matrix.csv',40),('j4_g1_continuity_review.csv',14)]:
 with (P/fn).open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
 assert len(r)==count
 assert all(x.get('status','NOT_RUN')=='NOT_RUN' if 'status' in x else x.get('evidence_state')=='NOT_RUN_NO_MEDIA' for x in r)
with (P/'j4_g1_30fps_action_beats.csv').open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
for sid in V:
 arr=[x for x in r if x['shot_id']==sid]
 assert arr and int(arr[0]['local_frame_in'])==0
 assert int(arr[-1]['local_frame_out_exclusive'])==next(x for x in timeline['shots'] if x['id']==sid)['duration_ms']*30//1000
 assert all(int(arr[i]['local_frame_out_exclusive'])==int(arr[i+1]['local_frame_in']) for i in range(len(arr)-1))
print('PASS: immutable provenance, 25-shot/90s timeline, 10 vertical candidates + 4 independent horizontal baselines, 14 NOT_RUN relations, 40 NOT_RUN criteria, frame beats, zero media/spend')
'''
(out/'validate_v3_1.py').write_text(validator,encoding='utf-8')

# ZIP with portable review and baseline sources
zipfile_path=root/'j4_museum_v3_1_bundle.zip'
with zipfile.ZipFile(zipfile_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(out.iterdir()):
  if f.is_file():z.write(f,arcname=f'j4_museum_v3_1/{f.name}')
print('Output:',out,' files:',len(list(out.iterdir())),' zip:',zipfile_path.stat().st_size)
