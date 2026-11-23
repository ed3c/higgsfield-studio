import json,csv,hashlib,zipfile,html,re,os
from pathlib import Path
from datetime import datetime
ROOT=Path('/mnt/data'); OUT=ROOT/'j4_museum_v3_4'; OUT.mkdir(exist_ok=True)
source_shots=json.loads((ROOT/'j4_museum_v2_9/j4_shots_v2_9.json').read_text())['shots']
byid={s['id']:s for s in source_shots}
art=json.loads((ROOT/'j4_museum_v3_3/j4_illusion_ir_v3_3.json').read_text())['shots']
artby={s['shot_id']:s for s in art}
arcby={a['arc_id']:a for a in json.loads((ROOT/'j4_museum_v3_3/j4_10memory_arc_evidence_v3_3.json').read_text())['arcs']}
assetby={a['asset_id']:a for a in json.loads((ROOT/'j4_museum_v3_2/j4_object_registry_v3_2.json').read_text())['assets']}
TRIALS=[
 dict(id='G2A_COAT',arc_id='ARC_COAT_FALSE',title='外套身分錯視',a='S10',b='S21',extra=[],mechanism='SHADOW_FIGURE_GROUND + FALSE_CONTINUITY_REVEAL',prior='觀眾可能把 S10 的檔案外套 B 誤認為創辦人的外套 A。',reveal='S21 的外套 A 左下襬有修補，S10 的 B 沒有；兩件衣服不是同一件。',anchor='左下襬修補（A 有、B 無），而非顏色或演員外貌',control='S21 的修補被刻意遮擋；若仍大量回報「兩件不同」需警惕提問誘導。',guard='禁止使用真人肖像、知名皮衣外觀或與受害者檔案藝術相似的陳列形式。',opening='請用一句話描述鏡頭中看到了什麼；這件物品可能屬於誰？',second='再看前一鏡後，你認為兩件衣服的關係是什麼？請指出畫面中的可見證據。'),
 dict(id='G2A_PAPER',arc_id='ARC_PAPER',title='紙屋尺度與意義重釋',a='S11',b='S22',extra=['S15','S20'],mechanism='SCALE_AND_ATTENTION_SHIFT + SHARED_FABRICATION_GRAMMAR',prior='S11 紙屋像工人休息時留下的小手作。',reveal='S22 顯示類似摺法如何構成無人居住的整座紙海岸；它們是不同物件，共享製造語法。',anchor='不規則屋頂摺線 + 單一非矩形窗戶；S11/S22 絕非同一實體',control='S22 使用不相容的屋頂摺法及窗形；若仍認作相同摺紙語法，說明線索可能太泛化。',guard='紙景不能幻化成實景，不能複製遊戲專屬地景、物流裝備及角色。',opening='注意到哪個物件？它在這個工廠中可能意味著什麼？',second='重新觀看後，S11 的小物件對你有何不同意義？哪項物理製作細節支持這個聯想？'),
 dict(id='G2A_AUTHORITY',arc_id='ARC_AUTHORITY',title='權力光形的事後辨識',a='S18',b='S19',extra=['S21'],mechanism='RETROSPECTIVE_SHAPE_MATCH + ILLUMINATED_HIERARCHY',prior='S18 的三個光形只是尚不具體意義的訊號。',reveal='S19 的三處主位照明與 S18 三個抽象光形有一致的相對位置，另兩席黯淡。',anchor='三個主要光位的橫向排序、相對距離與高度；不可依靠真實國家配色',control='S19 主要照明位置重新排列；若仍認出一一對應，可能只是「三個」的泛化聯想。',guard='S18 無高頻閃光；S19 是明顯虛構新聞台，禁止誤認真實峰會畫面。',opening='這段極短畫面出現了哪些形狀？你能確定它們是什麼嗎？',second='觀看下一鏡後，先前光形有沒有獲得新的意義？兩鏡間有哪些具體空間對應？')
]
for t in TRIALS:
 for key in ['a','b']:
  s=byid[t[key]]; ar=artby[t[key]]
  t[key+'_media']={'shot_id':t[key],'duration_ms':s['duration_ms'],'start_ms':s['start_ms'],'end_ms':s['end_ms'],'status':'MISSING_REAL_STIMULUS','art_reference':{'artist':ar['reference_artist'],'work':ar['reference_work'],'url':ar['source_url']},'image_prompt':s['image_prompt'],'motion_prompt':s['motion_prompt']}
 t['source_arc']=t['arc_id']; t['review_state']='NOT_RUN'
 t['anchor_assets']=arcby[t['arc_id']]['asset_ids']
 t['source_narrative_class']=arcby[t['arc_id']]['narrative_class']
 t['allowed_variants']={name:[v['id'] for v in assetby[name]['swap_variants']] for name in t['anchor_assets'] if name in assetby}
manifest={'project':'J4 ASYNC: SUCCESSION','version':'3.4','phase':'G2-A','source_versions':['v3.2','v3.3','v2.9'],'experiment_kind':'human_double_viewing_visual_memory','do_not_confuse':'text-only rehearsal is not an optical perception result','total_shots':25,'film_duration_ms':90000,'frame_rate':30,'trial_count':3,'media_status':'ALL_MEDIA_MISSING','paid_generation':'BLOCKED','review_state':'NOT_RUN','constraints':['no Higgsfield generation','no paid image/video generation','no existing artwork reproduction','no real-person contest plates','participant responses must not be treated as measured without real stimuli'],'trials':TRIALS,'protocol':{'sequence':['A_without_context','free_first_read','B_reveal','A_second_viewing','free_second_read','confidence','export'], 'presentation_rule':'A and B must be actual approved generated/edited individual shot clips or stills; show at source duration; with missing media no result is scorable.','counterbalance':'Participant order assigned modulo six predefined permutations; do not use fixed order across viewers.','no_spoilers':'Do not show source artwork, cue description or director intended reveal to participant until submission.'}}
(OUT/'j4_g2a_trial_manifest_v3_4.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

# Creative methods tied to art, source basis precisely from v3.3
rows=[]
for t in TRIALS:
 for sh,role in [(t['a'],'A_first'),(t['b'],'B_reveal')]:
  a=artby[sh]
  rows.append({'trial_id':t['id'],'shot_id':sh,'role':role,'illusion_category':a['category'],'mechanism':a['illusion_id'],'artist':a['reference_artist'],'reference_work':a['reference_work'],'reference_url':a['source_url'],'method_transfer':a['j4_original_transformation'],'not_to_copy':a['do_not_copy'],'source_status':a['source_status'],'viewer_status':'NOT_RUN'})
with open(OUT/'j4_g2a_art_crosswalk.csv','w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()));writer.writeheader();writer.writerows(rows)

# Asset invariants: preserve dependencies
inv=[]
for t in TRIALS:
 for aid in t['anchor_assets']:
  x=assetby.get(aid)
  if not x: continue
  inv.append({'trial':t['id'],'asset_id':aid,'identity_policy':x['physical_identity_policy'],'invariant':x['invariant'],'occurrences':','.join(o['shot'] for o in x['occurrences']),'variant_options':' / '.join(v['id']+': '+v['description'] for v in x['swap_variants']),'status':'NOT_RUN'})
with open(OUT/'j4_g2a_asset_invariants.csv','w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=list(inv[0].keys()));writer.writeheader();writer.writerows(inv)

protocol='''# J4 G2-A｜三條跨鏡記憶回響：雙次觀看實驗協定 v3.4

## 範圍與證據層級

本文件以 v3.2 Object Registry、v3.3 10 memory arcs、v2.9 Shot IR 為基準；原件只讀。這是**研究與執行規格**，不等於觀眾測試已執行。三組 A/B 片段目前尚未提供可測試的影像，`NOT_RUN` 不得改為 PASS。

只研究三條 P0 鏈：`ARC_COAT_FALSE`（S10→S21）、`ARC_PAPER`（S11→S22）、`ARC_AUTHORITY`（S18→S19；S21 為後續第三層揭示，不併入第一輪 A/B 曝光）。

## 不同層次的觀眾問題

- **第一次解讀**：只播放 A，不公開藝術家來源與導演意圖。自由描述「看見什麼／可能意味什麼」，並填 1–5 的把握度。
- **揭示**：播放 B，維持同一縱橫比、同一觀看條件；不顯示導演設計答案。
- **第二次解讀**：再次播放 A，再問是否改變理解、可見物件線索與把握度。允許「沒有改變」或「不確定」。
- **佐證**：若提出物件身分、摺紙語法或空間排序的推論，須指向具體可見線索，而非單純從故事猜測。

## 曝光長度

| Pair | A | B | 重點 |
|---|---|---|---|
| Coat | S10 3.5s | S21 4.0s | 左下襬修補：A 有、B 無 |
| Paper | S11 4.0s | S22 3.0s | 相同摺紙語法，不同實體 |
| Authority | S18 1.3s | S19 4.0s | 三個光形的相對配置呼應三個照明席位 |

A 再看需與 A 首看相同版次。不可先展示參考藝術品、物件 ID 或其他提示。原始 9:16 版優先；橫式版另開實驗，不混合數據。手機測試應記錄裝置尺寸與音量條件。

## 對照組與反事實

建立**僅供測試**的負對照，不修改 Canonical Film：
- Coat：在 B 隱藏修補痕；如果受試者仍精準聲稱識別，可能是引導或猜測。
- Paper：B 改用不相容的屋頂折線／窗形；觀察是否仍說出相同摺紙語法。
- Authority：B 重新排列三個主燈位；觀察是否仍宣稱有精確對應。

單次試驗不要把同一位受試者的正確版和對照版混播，避免互相污染。正式量化前，先以 5–8 位觀眾做可行性 pilot；條件分配與評分準則預先固定。

## 事前制定的人工編碼規則

單組結果不由 AI 自動決定。由不知條件的兩位審核者分別評估：

- `anchor_evidence_score`（0–2）：0 無可見依據；1 提到大方向；2 指出具體物理線索。
- `semantic_revision_score`（0–2）：0 沒改變／無效猜測；1 改變但證據薄弱；2 改變且能説明理由。
- `unfounded_claim`（0/1）：是否對沒有呈現的身分、國家或政治事件做確定判斷。
- `readability`（1–5）：一鏡能否被看懂，不代表理論上正確。

任何正式通過門檻都要先在 preregistration 中固定，不能測完才按結果調整。以下只是候選 pilot 標準：至少 5 位觀眾；實驗組中至少 70% 能提出具體 anchor，至少 50% 有有理由的語義改讀，對照組的 anchor 比率必須低於實驗組；小樣本只供設計調整，不宣稱統計顯著。

## 決策條件

`BLOCKED`: 缺少影像、來源權利或授權；`READY_FOR_PILOT`: 來源影像、剪輯時長、盲測文字與授權完成；`NOT_RUN`: 試驗尚未執行；`NEEDS_REVISION`: 視覺線索不可見、觀眾無法重釋、或對照組也得到同樣結果；`PASS_FOR_DIRECTOR_REVIEW`: pilot 有可重現質性回響，且專案權利審查可接受。以上都不是 Higgsfield 付費生成批准。

## 藝術來源與原創距離

S10 Tim Noble × Sue Webster；S21 Michelangelo Pistoletto；S11 Liliana Porter；S22 Thomas Demand；S18 Jim Campbell；S19 James Turrell。參考只做方法研究，禁止複製既有作品的裝置排列、可辨識構圖、圖形、影像、音訊。詳見 `j4_g2a_art_crosswalk.csv`，來源 URL 取自 v3.3；本次未重新線上複核各網站。

## 導演 G2-A 簽核

本階段全部保留 `NOT_RUN`。無實驗刺激即無實驗結論。生成前仍需 Neon 明確同意、Director 於指定聊天室貼出估點、核實 9,000 點月額度及各種權利限制。
'''
(OUT/'G2A_DOUBLE_VIEW_PROTOCOL.md').write_text(protocol)

schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'J4 G2A Human Viewer Result','type':'object','required':['schema_version','mode','participant_id','trials'], 'properties':{'schema_version':{'const':'3.4'},'mode':{'enum':['REHEARSAL_ONLY','HUMAN_VIEWER_WITH_MEDIA']},'participant_id':{'type':'string'},'session_started':{'type':['string','null']},'trials':{'type':'array','minItems':0,'maxItems':3,'items':{'type':'object','required':['trial_id','first_read','second_read','anchor_evidence','media_present'], 'properties':{'trial_id':{'enum':[t['id'] for t in TRIALS]},'media_present':{'type':'boolean'},'first_read':{'type':'string'},'second_read':{'type':'string'},'anchor_evidence':{'type':'string'},'confidence_before':{'type':'integer','minimum':1,'maximum':5},'confidence_after':{'type':'integer','minimum':1,'maximum':5},'status':{'enum':['NOT_RUN','HUMAN_SUBMITTED','REHEARSAL_ONLY']}}}}}}
(OUT/'g2a_observation_schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2))

readme='''# J4 Museum v3.4 · G2-A Memory Recall Pilot Package

這是 **pilot/test harness**，不是完成的觀眾研究；無可測試媒體時 `NOT_RUN`。

- `j4_g2a_trial_manifest_v3_4.json`：三組來源對齊的實驗設計（S10→S21、S11→S22、S18→S19）。
- `G2A_DOUBLE_VIEW_PROTOCOL.md`：雙次觀看、對照組、預先定義編碼與導演 Gate。
- `j4_g2a_art_crosswalk.csv`：6 鏡錯視方法對應當代藝術作品與來源。
- `j4_g2a_asset_invariants.csv`：跨鏡物件替換約束。
- `g2a_observation_schema.json`：觀眾匿名回應的匯出 schema。
- `j4_g2a_viewer_lab_v3_4.html`：無外部網路依賴的本機觀眾流程。可載入持權利的個別鏡頭檔案，未載入時僅可預演流程、不能記錄成正式結果。
- `validate_g2a_v3_4.py`：來源一致性與資料結構驗證。

### 重要限制

所有影片／靜幀皆需另行取得合法權利與生成許可；本包沒有生成圖片或影片。手繪示意、文字 Prompt、藝術來源截圖都不應被誤用為正式觀眾錯視實驗的刺激材料。

沒有人已實際觀看 A/B 組，沒有實測觀眾結果；任何百分比或分數只是事前規劃。所有原始 v2.9/v3.2/v3.3 工程檔保持只讀。
'''
(OUT/'README_v3_4.md').write_text(readme)

# The interactive lab intentionally only runs human test if actual per-shot media provided.
jsdata=json.dumps([{'id':t['id'],'title':t['title'],'a':t['a'],'b':t['b'],'durA':t['a_media']['duration_ms']/1000,'durB':t['b_media']['duration_ms']/1000,'firstQ':t['opening'],'secondQ':t['second']} for t in TRIALS],ensure_ascii=False)
page=r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>J4 G2-A｜記憶回響雙次觀看實驗</title><style>
:root{font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC",Arial,sans-serif;color:#e4e4e7;background:#101114}body{margin:0}main{max-width:1000px;margin:auto;padding:22px 16px 80px}header{border-bottom:1px solid #34353d;padding-bottom:18px;margin-bottom:20px}.eyebrow{color:#a3a3aa;font-size:12px;letter-spacing:1px}.title{font-size:28px;margin:8px 0}.sub{color:#b7b8c0;line-height:1.7}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(265px,1fr));gap:12px}.panel{border:1px solid #353740;border-radius:14px;padding:16px;background:#17191f}.panel h2{margin:0 0 6px;font-size:17px}label{display:block;font-size:13px;color:#ccc;margin:10px 0 5px}input,textarea,select,button{font:inherit}input[type=file]{width:100%;font-size:12px}input[type=text],textarea,select{box-sizing:border-box;width:100%;background:#0c0e12;color:#eee;border:1px solid #444650;border-radius:7px;padding:10px}textarea{min-height:86px;resize:vertical}button{padding:10px 15px;border-radius:9px;background:#d3d5df;color:#111217;border:0;cursor:pointer}button:disabled{opacity:.35;cursor:not-allowed}.secondary{background:#2f323a;color:#e9e9ee}.notice{background:#242027;border:1px solid #6b5362;border-radius:10px;padding:12px;font-size:13px;color:#f1dee3}.tag{display:inline-block;padding:3px 8px;border:1px solid #666;border-radius:100px;color:#ddd;font-size:12px}.muted{color:#aaa;font-size:13px}.stage{margin-top:22px}.hidden{display:none}#screen{height:min(60vw,480px);min-height:275px;background:#000;border:1px solid #444;display:flex;align-items:center;justify-content:center;margin:12px auto;position:relative;overflow:hidden}#screen video,#screen img{height:100%;max-width:100%;object-fit:contain}#screen .screen-caption{position:absolute;bottom:8px;left:8px;font-size:11px;color:#ccc;background:#222a;padding:4px 6px}#screen .empty{color:#747580;padding:20px;text-align:center}.row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:12px 0}.question{font-weight:600;line-height:1.5;margin-top:13px}.timer{font-variant-numeric:tabular-nums;color:#c4ccde}.ok{color:#a5e3b0}.bad{color:#ffb6b6}code{font-size:12px}footer{font-size:12px;color:#999;margin-top:30px;border-top:1px solid #333;padding-top:15px}
</style></head><body><main><header><div class="eyebrow">J4 · G2-A · v3.4 · HUMAN VIEWER LAB</div><h1 class="title">記憶回響雙次觀看測試</h1><div class="sub">先看鏡頭 A，留下第一印象；再看鏡頭 B，最後回看 A，描述意義是否改變。本工具僅本機處理你選擇的媒體，不會上傳影片或回覆。</div></header><div class="notice" id="status">目前沒有正式測試影像。未放入每組 A/B 真正的鏡頭剪輯前，狀態為 NOT_RUN；不能用空白頁或文字示意宣稱觀眾通過錯視測試。</div><section id="setup"><h2>準備三組鏡頭素材</h2><p class="muted">應使用獨立剪好的單鏡片段（9:16）。靜態定格可用，但屬「首影格可讀性測試」，不等同動態錯視驗證。影音需具備使用權。不要先向觀眾透露藝術家對標或物件的設計答案。</p><div class="grid" id="uploads"></div><div class="row"><label>匿名參與代碼 <input id="participant" type="text" value="PILOT-001" autocomplete="off" style="width:180px"></label><label>條件 <select id="condition"><option value="CANONICAL">原版主張</option><option value="CONTROL">反事實對照（需另外提供對照版 B）</option></select></label><label>測試模式 <select id="mode"><option value="HUMAN_VIEWER_WITH_MEDIA">正式媒體觀看</option><option value="REHEARSAL_ONLY">流程排練，不計入結果</option></select></label></div><div class="row"><button id="start">開始流程</button><span class="muted" id="ready">尚未就緒</span></div></section><section id="trial" class="stage hidden"><div class="row"><span class="tag" id="trial-number"></span><span class="tag" id="step-name"></span><span class="timer" id="duration-label"></span></div><h2 id="trial-title">—</h2><div class="muted" id="instruction"></div><div id="screen"><div class="empty">等待播放</div></div><div class="row"><button id="play" class="secondary">播放此鏡頭</button><button id="next" disabled>下一步</button><span class="timer" id="clock"></span></div><div id="survey" class="hidden"><div id="question" class="question"></div><textarea id="answer" placeholder="請寫下你實際看到的細節與解讀；可以回答不知道或沒有改變。"></textarea><label>解讀把握度（1–5） <select id="confidence"><option value="1">1 — 很不確定</option><option value="2">2</option><option value="3" selected>3</option><option value="4">4</option><option value="5">5 — 非常確定</option></select></label><div id="anchor-wrap" class="hidden"><label>支持你第二次解讀的**具體可見線索**</label><textarea id="anchor" placeholder="例如某一處修補、摺痕、相對位置；未看到請寫未看到。"></textarea></div></div></section><section id="finished" class="stage hidden"><h2>流程完成</h2><p class="muted" id="finished-note"></p><button id="export">下載匿名 JSON 回答</button><button class="secondary" onclick="location.reload()">新場次</button><p class="muted">回答僅供人工雙盲評分。工具不會自動宣布效果 PASS，亦不代替導演或權利審核。</p></section><footer>原始鏡頭的全部藝術來源與不變約束請查閱 ZIP 中的 `j4_g2a_art_crosswalk.csv` 和 `G2A_DOUBLE_VIEW_PROTOCOL.md`。媒體由使用者明確選取，不使用任何外部 API、伺服器或付費生成服務。</footer></main><script>
const T=__TRIALS__;
const $=id=>document.getElementById(id), data={}, results=[], fileUrls=[];
const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
function hash(s){let x=0;for(let c of s)x=(x*31+c.charCodeAt(0))>>>0;return x}
for(const t of T){let el=document.createElement('div');el.className='panel';el.innerHTML=`<h2>${t.title}</h2><div class="muted">${t.a}：${t.durA}s / ${t.b}：${t.durB}s</div><label>A 第一鏡<input type="file" accept="video/*,image/*" data-key="${t.id}_A"></label><label>B 揭示鏡<input type="file" accept="video/*,image/*" data-key="${t.id}_B"></label><div class="muted" id="${t.id}_hint">兩段媒體未載入</div>`;$('uploads').appendChild(el)}
document.querySelectorAll('input[type=file]').forEach(x=>x.addEventListener('change',e=>{const f=e.target.files?.[0];if(f) data[x.dataset.key]=f;updateReady()}));
function updateReady(){const count=T.reduce((n,t)=>n+(data[t.id+'_A']?1:0)+(data[t.id+'_B']?1:0),0);$('ready').textContent=`已載入 ${count}/6 媒體；正式測試需完整六段`;for(const t of T){const n=(data[t.id+'_A']?1:0)+(data[t.id+'_B']?1:0);$(t.id+'_hint').textContent=`${n}/2 媒體就緒`}}
let order=[],pos=0,phase=0,condition='',mode='',firstTime=null,currentTimer=null,playcount=0;
const PHASES=['A_PRE','FIRST_FORM','B_REVEAL','A_REPLAY','SECOND_FORM'];
function fileFor(shot,role){return data[shot.id+'_'+role]}
function clearScreen(){if(currentTimer){clearTimeout(currentTimer);currentTimer=null}let old=$('screen').querySelector('video');if(old) old.pause();$('screen').innerHTML='<div class="empty">按播放顯示素材</div>'; $('clock').textContent=''}
function stage(){const t=order[pos],s=PHASES[phase];$('trial-number').textContent=`第 ${pos+1}/3 組`; $('step-name').textContent={A_PRE:'首次觀看 A',FIRST_FORM:'第一印象',B_REVEAL:'觀看 B',A_REPLAY:'重看 A',SECOND_FORM:'第二次解讀'}[s];$('trial-title').textContent='片段閱讀'; $('duration-label').textContent=['A_PRE','A_REPLAY'].includes(s)?`${t.a} · ${t.durA} 秒`:(s==='B_REVEAL'?`${t.b} · ${t.durB} 秒`:'');$('survey').classList.toggle('hidden',!s.endsWith('FORM'));$('play').classList.toggle('hidden',s.endsWith('FORM'));$('next').disabled=true;clearScreen();$('answer').value='';$('anchor').value='';$('confidence').value='3';$('anchor-wrap').classList.toggle('hidden',s!=='SECOND_FORM');$('question').textContent=s==='FIRST_FORM'?t.firstQ:(s==='SECOND_FORM'?t.secondQ:'');$('instruction').textContent=s.endsWith('FORM')?'請獨立填寫。不要討論、不查來源。':'按播放後，素材會按照鏡頭時長顯示；看完才可進入下一步。';if(s.endsWith('FORM')){$('next').disabled=false;$('screen').innerHTML='<div class="empty">已結束本輪觀看；請寫下印象。</div>'}}
function next(){const t=order[pos],s=PHASES[phase];const r=results[pos]??{trial_id:t.id,media_present:!!(data[t.id+'_A']&&data[t.id+'_B']),status:mode==='REHEARSAL_ONLY'?'REHEARSAL_ONLY':'NOT_RUN'};if(s==='FIRST_FORM'){r.first_read=$('answer').value.trim();r.confidence_before=+$('confidence').value;if(!r.first_read){alert('請填第一印象；若無法判讀可填「不知道」。');return}}if(s==='SECOND_FORM'){r.second_read=$('answer').value.trim();r.anchor_evidence=$('anchor').value.trim();r.confidence_after=+$('confidence').value;if(!r.second_read||!r.anchor_evidence){alert('請填第二次解讀與可見線索；未看到可填「未看到」。');return}r.status=mode==='REHEARSAL_ONLY'?'REHEARSAL_ONLY':'HUMAN_SUBMITTED';results[pos]=r}phase++;if(phase>=PHASES.length){phase=0;pos++}if(pos>=order.length){$('trial').classList.add('hidden');$('finished').classList.remove('hidden');$('finished-note').textContent=mode==='REHEARSAL_ONLY'?'這是流程排練，沒有正式觀眾效果驗證。':'已完成觀眾資料紀錄；仍需盲評者審核與 G2-A 授權決定。';return}stage()}
$('next').onclick=next;
$('start').onclick=()=>{mode=$('mode').value;condition=$('condition').value;const full=T.every(t=>data[t.id+'_A']&&data[t.id+'_B']);if(!full){alert('此實驗必須載入三組 A/B 共六段真實素材。未載入媒體不可執行，避免製造假的觀眾結果。');return}if(condition==='CONTROL'&&!confirm('對照組應提供刻意改變關鍵線索的 B 版影片；確認你已使用對照素材？'))return;order=perms[hash($('participant').value)%6].map(i=>T[i]);$('setup').classList.add('hidden');$('trial').classList.remove('hidden');pos=0;phase=0;stage()};
$('play').onclick=async()=>{const t=order[pos],p=PHASES[phase];const role=p==='B_REVEAL'?'B':'A',f=fileFor(t,role),dur=(role==='A'?t.durA:t.durB);if(!f)return;clearScreen();const url=URL.createObjectURL(f);fileUrls.push(url);let m;if(f.type.startsWith('image/')){m=document.createElement('img');m.src=url;m.alt='已載入的實驗影格'}else{m=document.createElement('video');m.src=url;m.playsInline=true;m.muted=false;m.controls=false;m.preload='auto';m.onended=()=>{};} $('screen').innerHTML='';$('screen').appendChild(m);$('next').disabled=true;$('play').disabled=true;$('clock').textContent=`觀看 ${dur.toFixed(1)} 秒`;
try{if(m.tagName==='VIDEO'){m.currentTime=0;await m.play()}}catch(e){$('clock').textContent='播放器遭瀏覽器限制，請再點播放';$('play').disabled=false;return}
currentTimer=setTimeout(()=>{if(m.tagName==='VIDEO')m.pause();$('screen').innerHTML='<div class="empty">片段播放結束</div>';$('play').disabled=false;$('next').disabled=false;$('clock').textContent='可進入下一步'},Math.round(dur*1000))};
$('export').onclick=()=>{const r={schema_version:'3.4',mode,participant_id:$('participant').value.trim(),condition,trial_order:order.map(t=>t.id),source:'LOCAL_USER_SELECTED_MEDIA',observer_scores:'NOT_RUN',director_gate:'NOT_RUN',trials:results};let blob=new Blob([JSON.stringify(r,null,2)],{type:'application/json'});let u=URL.createObjectURL(blob);let a=document.createElement('a');a.href=u;a.download='j4_g2a_'+(r.participant_id.replace(/[^a-zA-Z0-9_-]/g,'_')||'anonymous')+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)};
</script></body></html>'''
(OUT/'j4_g2a_viewer_lab_v3_4.html').write_text(page.replace('__TRIALS__',jsdata))

validation='''from pathlib import Path
import json,csv
root=Path(__file__).resolve().parent
m=json.loads((root/'j4_g2a_trial_manifest_v3_4.json').read_text())
assert len(m['trials'])==3
assert m['media_status']=='ALL_MEDIA_MISSING' and m['review_state']=='NOT_RUN'
assert [(t['a'],t['b']) for t in m['trials']]==[('S10','S21'),('S11','S22'),('S18','S19')]
assert [(t['a_media']['duration_ms'],t['b_media']['duration_ms']) for t in m['trials']]==[(3500,4000),(4000,3000),(1300,4000)]
assert all(t['a_media']['status']==t['b_media']['status']=='MISSING_REAL_STIMULUS' for t in m['trials'])
assert all(t['review_state']=='NOT_RUN' for t in m['trials'])
with open(root/'j4_g2a_art_crosswalk.csv',encoding='utf-8-sig') as f:
 rows=list(csv.DictReader(f))
assert len(rows)==6 and all(r['reference_url'].startswith('https://') for r in rows)
assert len(json.loads((root/'g2a_observation_schema.json').read_text())['properties'])>=4
h=(root/'j4_g2a_viewer_lab_v3_4.html').read_text()
assert 'LOCAL_USER_SELECTED_MEDIA' in h and 'NOT_RUN' in h and 'URL.createObjectURL' in h
print('PASS v3.4: 3 arcs / 6 shot references / correct durations / media missing / no fabricated viewer results')
'''
(OUT/'validate_g2a_v3_4.py').write_text(validation)

# hashes and manifest
files=sorted(p for p in OUT.iterdir() if p.is_file())
(OUT/'ARTIFACT_MANIFEST_SHA256.json').write_text(json.dumps({'package':'j4_museum_v3_4','created_utc':'2026-11-22T04:00:00Z (project date label, not actual filesystem time)','files':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]},ensure_ascii=False,indent=2))
with zipfile.ZipFile(ROOT/'j4_museum_v3_4_bundle.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file():z.write(p,arcname='j4_museum_v3_4/'+p.name)
print('Created',OUT,'and',ROOT/'j4_museum_v3_4_bundle.zip')
