from pathlib import Path
import json,csv,hashlib,shutil,zipfile,random,html,textwrap

ROOT=Path('/mnt/data')
SRC=ROOT/'j4_museum_v3_9'
OUT=ROOT/'j4_museum_v4_0'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'baseline').mkdir(exist_ok=True)
for name in ['j4_sonic_object_registry_v3_9.json','j4_recall_trials_v3_9.json']:
 shutil.copy2(SRC/name,OUT/'baseline'/name)
for name in ['j4_shots_v2_9.json','j4_sound_ir_v2_8.json','j4_sound_dramaturgy_overlay_v3_7.json']:
 shutil.copy2(SRC/'baseline'/name,OUT/'baseline'/name)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
shots=json.loads((OUT/'baseline/j4_shots_v2_9.json').read_text())['shots']
shot_index={s['id']:s for s in shots}

arcs=[
 dict(id='R1_BIRD',name='光鳥：相同物件，情感改變',origin='S04',reveal='S24',object_family='BIRD_METAL',
      visual_art='Studio DRIFT — Fragile Future III（精密脆弱材料；僅借用方法）',audio_art='Rafael Lozano-Hemmer — Pulse Room（不同個體時間並存；僅借用方法）',
      baseline='光鳥實體相同，生成時必須保留三處非對稱金屬接點與同一段細線彎曲關係。',
      visual_on='S24 光鳥獨立輪廓與三處不對稱接點可辨認；與 S04 同一實體。',
      visual_off='S24 光鳥仍是同一實體，但以局部遮擋／焦點條件減少接點辨識；維持明暗、大小與動作時碼。',
      audio_on='S24 以新錄的同材質微金屬指紋，保留 S04 的微小不諧泛音比例，起音柔和且空間殘響改變。',
      audio_off='S24 使用不同但原創的微金屬聲，保持起音時點、包絡、聲像與主觀響度相近。',
      first_question='你認為初次鏡頭中小型發光物件的材質與情緒是什麼？',
      reveal_question='這件物品與先前是否有關？你依據什麼可見或可聽證據？',
      avoid='禁止既有電影鳥徽、仿製 Studio DRIFT 的蒲公英 LED 造型、受保護錄音。',
      evidence='相同接點與金屬局部構造；非重新生成的鳥徽；音色變化不能直接充當答案音效。',
      audio_time_ms=85150),
 dict(id='R2_COAT',name='真假外套：相似不等於同一',origin='S10',reveal='S21',object_family='COAT_ARCHIVE|COAT_MAIN',
      visual_art='Tim Noble × Sue Webster — Dirty White Trash (with Gulls)（影子重組；僅借用方法）',audio_art='Doris Salcedo — Atrabilious（日常物件承載缺席；僅借用方法）',
      baseline='檔案外套 B 和主線外套 A 始終是不同物件；A 左下襬修補，B 無此修補。',
      visual_on='S21 末 0.7 秒在椅上的外套 A 左下襬修補能辨認；S10 外套 B 沒有修補。',
      visual_off='A 的修補客觀存在，但受摺疊／遮擋而難以辨認；不得把 B 偽裝成 A 或更改故事事實。',
      audio_on='S10 網門加短粗織布 B；S21 使用較長、不同織法的 A 之布料摩擦；保留可聽材質差異。',
      audio_off='S21 以沒有可區辨織法特徵的中性布料摩擦替換，維持時長與主觀響度，不能偽造相同物件。',
      first_question='你覺得被存放的外套與人的身分有什麼關係？',
      reveal_question='兩鏡的外套是同一件嗎？你看見或聽見什麼可供核對的差異？',
      avoid='不得出現真人名人可識別服飾；不得使用暴力受害者物件造型；不得以音效聲稱兩衣同一實體。',
      evidence='A 的左下襬修補、B 缺失；兩件服裝的實際比例與剪裁差異；聲學不誤導。',
      audio_time_ms=75500),
 dict(id='R3_PAPER',name='紙屋：相同製作語法，不同世界',origin='S11',reveal='S22',object_family='PAPER_FOLD',
      visual_art='Thomas Demand — Office（紙構現實；僅借用方法）',audio_art='Mierle Laderman Ukeles — Washing/Tracks/Maintenance: Inside（維護動作的價值；僅借用方法）',
      baseline='S11 與 S22 是兩個不同紙屋；共享屋頂折線與偏斜窗洞的製作語法。',
      visual_on='S22 在微縮地景呈現與 S11 相同的偏斜屋頂折線及非規則窗形，明確保留兩屋非同一實體。',
      visual_off='S22 以同等複雜但不同的摺折／窗形設計，材料與位置不變；兩物件仍是紙造。',
      audio_on='S22 使用同類紙張纖維的壓折接觸，與 S11 有可辨別的材質族譜，但不是重複相同音檔。',
      audio_off='S22 使用另一種原創紙材的折痕聲，匹配長度、主觀響度與房間位置。',
      first_question='工廠裡的紙屋是什麼？你認為它在場景中代表什麼？',
      reveal_question='這座紙世界是否讓你重新理解先前的小紙屋？請指出摺法或材質證據。',
      avoid='不可複製 Thomas Demand 既有模型；不可直接使用《死亡擱淺》遊戲角色、道具或音效。',
      evidence='跨鏡摺痕、窗形、紙纖維；重要的是技法相同而非同一物體。',
      audio_time_ms=76900),
]
conditions=[
 dict(id='V0A0',visual=0,audio=0,name='雙控制',purpose='不保留特定視覺或聲學記憶線索'),
 dict(id='V1A0',visual=1,audio=0,name='視覺錨點',purpose='估計視覺線索單獨貢獻'),
 dict(id='V0A1',visual=0,audio=1,name='聲學錨點',purpose='估計聲音線索單獨貢獻'),
 dict(id='V1A1',visual=1,audio=1,name='聲畫一致',purpose='檢驗互補或交互作用'),
]
base_files=['j4_shots_v2_9.json','j4_sound_ir_v2_8.json','j4_sound_dramaturgy_overlay_v3_7.json','j4_sonic_object_registry_v3_9.json','j4_recall_trials_v3_9.json']
checksums={n:sha(OUT/'baseline'/n) for n in base_files}

spec={
 'project':'J4 ASYNC: SUCCESSION','version':'v4.0 Cross-Modal Recall Gate','status':'CANDIDATE_DESIGN_ONLY_NO_MEDIA_NO_GENERATION',
 'shot_count':25,'duration_ms':90000,'fps':30,'sample_rate_hz':48000,'baseline_sha256':checksums,
 'immutable_timeline': {'sine_start_ms':500,'local_S10_cut_ms':38600,'S18_six_phase_stop_ms':63700,'S24_new_market_ms':84000,'S25_sine_only_ms':87000,'end_ms':90000},
 'film_governance':'No billable generation before Neon explicit GO, Director point estimate in AI Video Production Service, monthly credit balance, rights approval.',
 'design':{'type':'2x2 between-subjects (revealed visual cue × recalled sonic cue)',
           'origin_same_across_conditions':True,'reveal_only_factorial_changes':True,
           'pilot_target_participants':32,'allocation_per_condition':8,
           'pilot_limit':'formative only, not powered for statistical inference',
           'primary_measure':'binary evidence-grounded reinterpretation scored independently by 2 blinded judges',
           'secondary_measures':['object_relation_accuracy_0to2','evidence_specificity_0to2','emotional_delta_minus2to2','confidence_1to5','response_latency_ms'],
           'analysis':'interaction=(p11-p10)-(p01-p00); exploratory descriptive with uncertainty by participant, no effect claim before real media',
           'participant_flow':['view_origin','open_answer_before','view_reveal','replay_origin','open_answer_after','confidence_and_emotion']},
 'conditions':conditions,'arcs':arcs,
 'external_exploratory':{'id':'E1_SEATS','origin':'S18','reveal':'S19','type':'visual spatial recall only',
                          'rule':'Do not add audio to S18; the original sine is the only surviving sound after 63.700s.',
                          'art':'Jim Campbell — Exploded Views; James Turrell — Afrum I (White)',
                          'status':'NOT_RUN_NO_MEDIA'},
 'critical_constraints':['Preserve 25-shot 90s canon','S18 only original sine after forced stop','S10 local stop is not global','No sound or image sampled from protected art works','No altered object truth','No sham human-study data', 'Actual source/rights logs required'],
 'media_status':'BLOCKED_NO_REAL_MEDIA',
 'trial_status':'NOT_RUN',
}
(OUT/'j4_cross_modal_ir_v4_0.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')

def writecsv(path,fields,rows):
 with open(path,'w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

# 3 fixed origins + 12 reveal assets (no media generated)
media=[]; pairs=[]
for arc in arcs:
 ss=shot_index[arc['origin']]; rr=shot_index[arc['reveal']]
 origin_name=f"media/{arc['id']}_origin.mp4"
 media.append(dict(media_id=f"{arc['id']}_ORIGIN",arc=arc['id'],role='origin',condition='ALL',expected_file=origin_name,
                   shot_id=arc['origin'],duration_ms=ss['duration_ms'],fps=30,audio_rate_hz=48000,material_status='MISSING_NOT_RUN'))
 for cond in conditions:
  rn=f"media/{arc['id']}_{cond['id']}_reveal.mp4"
  media.append(dict(media_id=f"{arc['id']}_{cond['id']}_REVEAL",arc=arc['id'],role='reveal',condition=cond['id'],expected_file=rn,
                   shot_id=arc['reveal'],duration_ms=rr['duration_ms'],fps=30,audio_rate_hz=48000,material_status='MISSING_NOT_RUN'))
  pairs.append(dict(arc=arc['id'],condition=cond['id'],visual=cond['visual'],audio=cond['audio'],origin_file=origin_name,reveal_file=rn,
                    image_rule=arc['visual_on'] if cond['visual'] else arc['visual_off'],
                    audio_rule=arc['audio_on'] if cond['audio'] else arc['audio_off'],review_state='NOT_RUN'))
writecsv(OUT/'j4_stimulus_manifest_v4_0.csv',list(media[0]),media)
writecsv(OUT/'j4_factorial_conditions_v4_0.csv',list(pairs[0]),pairs)

# allocation: one participant gets all arcs in one between-subject condition, counterbalanced arc order.
rng=random.Random(40261122)
orders=[('R1_BIRD','R2_COAT','R3_PAPER'),('R2_COAT','R3_PAPER','R1_BIRD'),('R3_PAPER','R1_BIRD','R2_COAT')]
allocation_pool=[]
for cond in conditions:
 sequence_ids=[0,0,0,1,1,1,2,2]
 rng.shuffle(sequence_ids)
 allocation_pool.extend((cond['id'], idx) for idx in sequence_ids)
rng.shuffle(allocation_pool)
alloc=[]
for i,(cond,seq_index) in enumerate(allocation_pool):
 alloc.append(dict(participant_code=f'P{i+1:03d}',assigned_condition=cond,arc_sequence='>'.join(orders[seq_index]),consent_status='NOT_OBTAINED',status='UNASSIGNED_NO_HUMAN'))
writecsv(OUT/'j4_pilot_allocation_v4_0.csv',list(alloc[0]),alloc)

rubric=[
 {'dimension':'reinterpretation_binary','range':'0/1','decision':'1 only if later viewing changes the interpretation AND participant cites a true specific visual or sonic cue','blind':'YES'},
 {'dimension':'object_relation_accuracy','range':'0..2','decision':'2 accurate physical identity/grammar; 1 uncertain but not fabricated; 0 explicitly wrong','blind':'YES'},
 {'dimension':'evidence_specificity','range':'0..2','decision':'2 observable specific evidence; 1 generic material; 0 unsupported intuition','blind':'YES'},
 {'dimension':'emotional_delta','range':'-2..2','decision':'self-report after vs before emotion; not treated as factual recall accuracy','blind':'NO'},
 {'dimension':'confidence','range':'1..5','decision':'self-report in each stage, no pressure to guess','blind':'NO'},
 {'dimension':'latency_ms','range':'nonnegative','decision':'response delay may reflect interface or device, exploratory only','blind':'NO'},
]
writecsv(OUT/'j4_scoring_rubric_v4_0.csv',list(rubric[0]),rubric)

conf=[]
controls=[
 ('time','origin duration identical; reveal duration identical for each arc'),
 ('image','same camera, framing, color/exposure, actor, props and spatial blocking except target local cue'),
 ('audio','same onset, event length, perceived loudness, broad spectral balance, panning and room response except target fingerprint'),
 ('language','no new subtitles, dialog or readable signs between conditions'),
 ('truth','same story and physical object identity across all four conditions'),
 ('rights','all 15 stimuli require independent original imagery/audio or licensed assets'),
 ('accessibility','confirm caption/mono parity; key meaning recoverable outside intentional cue test'),
 ('reliability','all stimuli coded with hashes, takes, source/license and independent reviews'),
]
for a in arcs:
 for aspect,rule in controls:
  conf.append(dict(arc=a['id'],aspect=aspect,required_control=rule,check_state='NOT_RUN',evidence_file='',reviewer='',notes=''))
writecsv(OUT/'j4_confound_checklist_v4_0.csv',list(conf[0]),conf)

score=[]
for a in arcs:
 score.append(dict(participant_code='',arc=a['id'],condition_code='',origin_response='',after_reveal_response='',replay_response='',evidence_phrase='',
             reinterpretation_rater1='',reinterpretation_rater2='',accuracy_rater1='',accuracy_rater2='',evidence_rater1='',evidence_rater2='',
             emotional_before='',emotional_after='',confidence_before='',confidence_after='',test_state='NOT_RUN'))
writecsv(OUT/'j4_blind_scorecard_v4_0.csv',list(score[0]),score)

methods='''# J4 v4.0｜聲畫聯合導演契約

## 不變基準

- 25 鏡、90,000 ms、30 fps；既有 canonical Shot IR、Sound IR **唯讀**。
- `SINE_GROUND` 自 0.500 秒開始，跨越 63.700 秒 S18 全局中斷，直到 90.000 秒才結束。
- S10 的 38.600 秒為局部音尾中斷，並非六組循環的全局停止。
- S24 的新夜市聲場在 84.000 秒返回，但不重新啟動原來的七秒循環。
- 本階段沒有合法可播放的視聽刺激；所有實驗結果 `NOT_RUN`。

## 實驗方法

一個受試者只分配到 V0A0、V1A0、V0A1 或 V1A1 **其中一種**條件，再以輪換順序觀看三條回響鏈。每條鏈的 origin 片段固定；四個版本只對 reveal 中預先宣告的局部視覺／聽覺記憶線索做差異化。進行 Origin → 原始回答 → Reveal → Origin 重看 → 第二次回答。不得由實驗主持人在問題中直接說出「外套 A/B」、「同一隻光鳥」等答案。

**主要指標**：兩位盲評者是否都看到具體、正確的證據支持重新理解。若兩人不同意，保留雙方原始分數並安排第三位裁決，不得自動改成 PASS。估計聲畫交互作用為 `p11 - p10 - p01 + p00`，只作描述，不在缺乏充分樣本下宣稱顯著。

**測試媒材**：三條固定 origin + 十二個 reveal = 15 個不同邏輯影片檔；不代表需要 15 次付費生成。可用合法原創影像／剪輯局部遮罩與獨立混音生成。A0 仍有聲音；V0 仍有影像。控制版本必須維持真實物件身分。

## 研究對標（只借方法）

- R1 光鳥：Studio DRIFT《Fragile Future III》精密材料脆弱性；Rafael Lozano-Hemmer《Pulse Room》個體節奏並存。
- R2 外套：Tim Noble × Sue Webster《Dirty White Trash (with Gulls)》物件／影像雙讀；Doris Salcedo《Atrabilious》缺席者的物件。
- R3 紙屋：Thomas Demand《Office》紙製現實的尺度；Mierle Laderman Ukeles《Washing/Tracks/Maintenance: Inside》維護行為。
- E1 S18→S19：Jim Campbell《Exploded Views》低解析形態回想；James Turrell《Afrum I (White)》光學立體感。此鏈僅作視覺探索，不加入 2×2 實驗或修改 S18 聲音。

不複製藝術家的錄音、旋律、造型、安裝結構或既有畫面；不使用真人特徵、電影／遊戲受保護角色、新聞台真實識別。

## P0 阻擋條件

`NO_REAL_MEDIA`、`NO_MEDIA_QA`、`NO_RIGHTS_APPROVAL`、`NO_DIRECTOR_SIGNOFF`、`NO_HUMAN_DATA`，任何一項存在，都不得將 G2-GATE 標為通過。

**付費製作閘口**：仍需 Neon 明確批准、Director 先把估點貼到「AI Video Production Service」、查實當月 9,000 點限額與剩餘點數，以及權利審核。嚴禁默認批准。
'''
(OUT/'JOINT_SOUND_VISUAL_DIRECTOR_CONTRACT_v4_0.md').write_text(methods)

delta=['# v4.0｜12 組聲畫聯合刺激設計（只改 Reveal，非生成指令執行）','',
       '每組配合原始 Master Image/Sound Lock 使用。以下是**候選局部 Prompt Delta**；不覆寫 canonical prompts。']
for a in arcs:
 delta.extend(['',f"## {a['id']}｜{a['name']}",f"Origin：{a['origin']}；Reveal：{a['reveal']}",f"**不可變事實：** {a['baseline']}",f"**藝術方法：** {a['visual_art']}；{a['audio_art']}"])
 for c in conditions:
  v=a['visual_on'] if c['visual'] else a['visual_off']
  au=a['audio_on'] if c['audio'] else a['audio_off']
  delta.extend(['',f"### {c['id']}（V={c['visual']}，A={c['audio']}）",'```text',
      f"Visual: {v}",f"Audio: {au}",
      'Keep shot timing, narrative truth, camera path, lighting, subjective loudness and non-target material unchanged.',
      'Use only original or properly licensed visual and sonic sources. Do not quote any known artist recording or distinctive movie/game design.',
      '```'])
(OUT/'PASTE_READY_JOINT_DELTAS_v4_0.md').write_text('\n'.join(delta)+'\n')

readme='''# J4 v4.0 — Cross-Modal Memory Recall Gate

## 交付範圍

正式 Shot IR、Sound IR 與 v3.9 物件聲音 Registry 維持唯讀。本包新增三條 P0 回響鏈的視覺 × 聲音 2×2 因子實驗、15 個預期媒體槽位、32 個未指派 pilot 名額、混淆因子查核、評分表、可離線操作的審核頁面及驗證程式。

- **PASS（僅靜態）**：原始來源 SHA-256、25 鏡 90 秒、三條回響鏈、12 個條件配對、30 fps 時碼與 48 kHz 聲音座標。
- **BLOCKED**：缺少真實可播放、可核對權利的媒體。沒有聲音或影片生成，沒有實際觀眾，不能聲稱通過藝術／聲音或 G2-A/B gate。
- **不包含**：Higgsfield 呼叫、API、MCP、付費點數、原 repository 寫入。

## 核心檔案

- `j4_cross_modal_ir_v4_0.json`: 永續性約束、3 條回響鏈、4 種條件、分配與評分規格
- `j4_factorial_conditions_v4_0.csv`: 12 組視覺／聽覺操控
- `j4_stimulus_manifest_v4_0.csv`: 3 個固定 origin、12 個 reveal，全部 MISSING
- `j4_pilot_allocation_v4_0.csv`: 32 個尚未指派的 pilot 位置，請勿當成已測數據
- `j4_confound_checklist_v4_0.csv`: 24 個必查混淆因素
- `j4_blind_scorecard_v4_0.csv`: 雙盲評分空白模板
- `PASTE_READY_JOINT_DELTAS_v4_0.md`: 候選改動（不寫入正式提示詞）
- `JOINT_SOUND_VISUAL_DIRECTOR_CONTRACT_v4_0.md`: 藝術與實驗合約
- `j4_cross_modal_review_board_v4_0.html`: 本機影片載入／設計審核／排練紀錄匯出
- `media_qa_v4_0.py`: 真實檔案存在後使用 ffprobe 驗證 30 fps、48 kHz、畫面尺寸與長度，未提供媒體就必須 BLOCKED
- `validate_v4_0.py`: 只針對 JSON/CSV 和基準校驗值執行離線靜態測試

## 實際測試順序

1. 製作與授權所有原始素材（仍受 Neon/Director/額度 Gate 約束）。
2. 產出每條鏈的同一支 origin 與四個 reveal，先行人工核對四個版本只在預先規定的局部線索不同。
3. 執行 `python media_qa_v4_0.py --root <包含 media/ 的目錄>`；沒有素材時返回非零狀態。
4. 訪問本機頁面並手動載入兩支影片；只有已載入真正媒體才可以將紀錄標成正式刺激。
5. 依實驗預註冊流程收集觀眾資料，兩人獨立盲評；正式數據需有可追溯 consent 及 media hash。

## 不宣稱的事

- 無實際觀眾記憶改善數據。
- 無音量相等、真峰值、音色等價、實際錯視效果之驗證。
- 網頁 smoke test ≠ 實際影片或受試者測試。
'''
(OUT/'README_v4_0.md').write_text(readme)

# HTML with an embedded, self-contained manifest and no network
client={'arcs':arcs,'conditions':conditions,'pairs':pairs,'immutable':spec['immutable_timeline']}
jsondata=json.dumps(client,ensure_ascii=False).replace('</','<\\/')
html_template=r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/><title>J4 v4.0 — 聲畫聯合實驗</title>
<style>
:root{font-family:system-ui,-apple-system,"Noto Sans TC",sans-serif;color-scheme:dark;background:#11141a;color:#e8ebee}
*{box-sizing:border-box}body{margin:0;padding:20px}main{max-width:1160px;margin:auto}
header{padding:20px 0 22px;border-bottom:1px solid #3a4149}h1{font-size:28px;margin:0 0 10px}h2{font-size:19px;margin:8px 0 12px}h3{font-size:15px;margin:12px 0}
p{line-height:1.65;color:#b6c0c8;margin:6px 0 14px}.muted{color:#a5afb9;font-size:13px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{border:1px solid #424951;border-radius:12px;padding:16px;background:#1b2027;margin:15px 0}
.kpis{display:flex;gap:10px;flex-wrap:wrap}.kpi{border:1px solid #424951;border-radius:8px;padding:9px 12px;font-size:13px}.kpi strong{display:block;font-size:17px;color:white}
button,select,input,textarea{font:inherit;color:#e8ebee;background:#252c35;border:1px solid #59616c;border-radius:7px;padding:8px}
button{cursor:pointer}button:disabled{opacity:.45;cursor:not-allowed}button:hover:enabled{border-color:#b6d1df}
label{display:block;font-size:13px;margin-bottom:6px;color:#c6cfd7}.controls{display:flex;gap:12px;align-items:end;flex-wrap:wrap}.controls>div{flex:1;min-width:180px}
video{display:block;background:#0c0f13;width:100%;max-height:380px;aspect-ratio:9/16;object-fit:contain;border:1px solid #454d56;border-radius:8px}
.stage{display:flex;gap:9px;flex-wrap:wrap;margin:10px 0}.stage button{font-size:13px}.stage .sel{background:#334a5c;border-color:#84b7cf}
textarea{width:100%;min-height:76px;resize:vertical;margin:4px 0 10px}
.danger{border-left:3px solid #d7ac68;padding-left:10px;color:#e6bd82}.box{background:#12171d;border:1px solid #303943;border-radius:8px;padding:12px;line-height:1.7}
code{font-family:ui-monospace,monospace;font-size:12px}a{color:#a4d9f4}.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}small{font-size:11px;color:#a1aeb9}
@media(max-width:740px){body{padding:10px}.grid{grid-template-columns:1fr}h1{font-size:23px}video{max-height:360px}.controls>div{min-width:140px}}
</style></head><body><main>
<header><div class="muted">J4《非同步：繼承》｜v4.0 Cross-Modal Recall Gate</div><h1>聲畫聯合記憶實驗</h1><p>正式影像與聲音尚未提供；本頁預設為設計排練。沒有真實媒體時，所有匯出一律標記為 REHEARSAL_ONLY。</p>
<div class="kpis"><div class="kpi"><strong>3</strong>回響鏈</div><div class="kpi"><strong>4</strong>因子條件</div><div class="kpi"><strong>15</strong>待製作媒體槽</div><div class="kpi"><strong>NOT_RUN</strong>正式聽測</div></div></header>
<section class="card"><h2>1. 導演設定 / 受試者載入</h2><div class="controls"><div><label for="arc">記憶回響</label><select id="arc"></select></div><div><label for="condition">條件（由主持人分配）</label><select id="condition"></select></div><div><label for="participant">匿名受試者代碼</label><input id="participant" placeholder="例如 P001" maxlength="30"/></div></div>
<div class="row"><label><input id="reviewMode" type="checkbox" checked/> 顯示導演備註（正式測試時關閉）</label></div>
<div id="director" class="box"></div><p id="warn" class="danger"></p></section>
<section class="card"><h2>2. 媒體準備</h2><p class="muted">請只載入已獲權利許可且通過獨立 QA 的兩段影像。Origin 在四個條件中必須完全一致。</p>
<div class="grid"><div><label>Origin：固定片段</label><input id="originFile" type="file" accept="video/mp4,video/*"/><video id="originVideo" controls playsinline preload="metadata"></video><small id="originName">尚未載入</small></div>
<div><label>Reveal：選定條件片段</label><input id="revealFile" type="file" accept="video/mp4,video/*"/><video id="revealVideo" controls playsinline preload="metadata"></video><small id="revealName">尚未載入</small></div></div></section>
<section class="card"><h2>3. Origin → Reveal → Origin</h2>
<div class="stage"><button id="stage1" class="sel">① 首次看 Origin</button><button id="stage2">② 看 Reveal</button><button id="stage3">③ 重看 Origin</button></div>
<p id="stageGuide" class="muted"></p><div id="promptBox" class="box"></div><label for="answer">觀看後自由回答（不能直接提示標準答案）</label><textarea id="answer" placeholder="請依畫面與聲音記錄直覺解讀。"></textarea>
<div class="row"><button id="saveStage">保存本階段答案</button><span id="saved" class="muted">目前未保存答案</span></div>
</section>
<section class="card"><h2>4. 匯出審核紀錄</h2><p>正式試驗仍需事先取得受試者同意、統一設備與響度校準、權利核對，並由兩位盲評者獨立評分。</p>
<div class="row"><button id="export">匯出 JSON</button><button id="reset">清空答案</button><strong id="status">REHEARSAL_ONLY</strong></div>
<p class="muted">所有資料只存於此頁的暫存狀態；不向外部伺服器傳送。影片檔不包含在 JSON 匯出中。</p></section>
<footer class="muted">原始 Shot IR / Sound IR 唯讀；無生成、無付費、無隱藏的實驗結果。</footer>
</main>
<script id="data" type="application/json">__DATA__</script><script>
(()=>{const DATA=JSON.parse(document.getElementById('data').textContent);
 const $=id=>document.getElementById(id);const state={phase:1,answers:{},files:{origin:null,reveal:null},urls:[],timestamps:{}};
 function setOptions(el,items,fn){el.innerHTML='';items.forEach(x=>{const o=document.createElement('option');o.value=x.id;o.textContent=fn(x);el.appendChild(o);});}
 setOptions($('arc'),DATA.arcs,a=>a.name);setOptions($('condition'),DATA.conditions,c=>`${c.id}｜${c.name}`);
 function arc(){return DATA.arcs.find(a=>a.id===$('arc').value)}
 function cond(){return DATA.conditions.find(c=>c.id===$('condition').value)}
 function pair(){return DATA.pairs.find(p=>p.arc===arc().id&&p.condition===cond().id)}
 function status(){const ready=!!state.files.origin&&!!state.files.reveal; $('status').textContent=ready?'MEDIA_LOADED_QA_NOT_VERIFIED':'REHEARSAL_ONLY';$('warn').textContent=ready?'本頁只能驗證已載入檔案，不能自動證明權利、亮度、響度或受試者同意。':'目前缺少真實 Origin／Reveal 影片；不可將排練結果列為正式研究。';}
 function guide(){const a=arc();const neutral=['這段影像讓你注意到什麼？請自由描述。','看完第二段後，有什麼元素讓你想到第一段？有什麼改變？','再次觀看第一段後，你的理解是否改變？請指出實際的畫面或聲音證據。']; $('promptBox').textContent=$('reviewMode').checked?(state.phase===1?a.first_question:state.phase===2?a.reveal_question:'重新觀看最初片段後，說明你的解讀是否改變；引用具體可見／可聽證據。'):neutral[state.phase-1]; $('stageGuide').textContent=`階段 ${state.phase}／3｜${state.phase===1?'先只看 Origin':state.phase===2?'再看 Reveal':'最後重看原 Origin'}`; $('answer').value=state.answers[state.phase]||'';
 [1,2,3].forEach(i=>$('stage'+i).classList.toggle('sel',i===state.phase));}
 function render(){const a=arc(),c=cond(),p=pair();const vis=c.visual?a.visual_on:a.visual_off;const aud=c.audio?a.audio_on:a.audio_off;const directorMode=$('reviewMode').checked;[...$('arc').options].forEach((o,i)=>o.textContent=directorMode?DATA.arcs[i].name:'測試片段 '+(i+1));[...$('condition').options].forEach((o,i)=>o.textContent=directorMode?(DATA.conditions[i].id+'｜'+DATA.conditions[i].name):'測試版本 '+(i+1)); $('arc').disabled=!directorMode; $('condition').disabled=!directorMode; $('originFile').style.display=directorMode?'':'none'; $('revealFile').style.display=directorMode?'':'none';
 $('director').textContent=$('reviewMode').checked?`物件事實：${a.baseline}\n視覺控制：${vis}\n聲音控制：${aud}\n藝術對標：${a.visual_art}／${a.audio_art}`:'正式觀看模式：隱藏條件與導演提示。';$('director').style.whiteSpace='pre-line';
 $('originName').textContent=directorMode?(state.files.origin?.name||`預期：${p.origin_file}`):(state.files.origin?'已載入影片':'尚未載入');$('revealName').textContent=directorMode?(state.files.reveal?.name||`預期：${p.reveal_file}`):(state.files.reveal?'已載入影片':'尚未載入');
 guide();status();}
 function clearMedia(){state.urls.forEach(u=>URL.revokeObjectURL(u));state.urls=[];state.files={origin:null,reveal:null};['originVideo','revealVideo'].forEach(id=>{$(id).removeAttribute('src');$(id).load();});['originFile','revealFile'].forEach(id=>$(id).value='');}
 function reset(){state.answers={};state.phase=1;state.timestamps={};clearMedia();render();}
 $('arc').addEventListener('change',reset);$('condition').addEventListener('change',reset);$('reviewMode').addEventListener('change',render);
 for(const id of ['origin','reveal']){$(id+'File').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;state.files[id]=f;const u=URL.createObjectURL(f);state.urls.push(u);$(id+'Video').src=u;render();});}
 [1,2,3].forEach(i=>$('stage'+i).addEventListener('click',()=>{state.answers[state.phase]=$('answer').value;state.phase=i;guide();}));
 $('saveStage').addEventListener('click',()=>{state.answers[state.phase]=$('answer').value;state.timestamps['stage'+state.phase]=new Date().toISOString();$('saved').textContent=`已保存階段 ${state.phase}（頁面暫存）`;});
 $('reset').addEventListener('click',reset);
 $('export').addEventListener('click',()=>{state.answers[state.phase]=$('answer').value;const ready=!!state.files.origin&&!!state.files.reveal;
 const payload={version:'v4.0',arc:arc().id,condition:cond().id,participant_code:$('participant').value||'',status:ready?'MEDIA_LOADED_QA_NOT_VERIFIED':'REHEARSAL_ONLY',origin_filename:state.files.origin?.name||null,reveal_filename:state.files.reveal?.name||null,answers:state.answers,timestamps:state.timestamps,exported_at:new Date().toISOString(),rights_review:'NOT_RUN',human_approval:'NOT_RUN'};
 const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=`j4_${arc().id}_${cond().id}_review.json`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 render();
})();</script></body></html>'''
(OUT/'j4_cross_modal_review_board_v4_0.html').write_text(html_template.replace('__DATA__',jsondata))

validator='''#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,csv,sys,collections
R=Path(__file__).resolve().parent
spec=json.loads((R/'j4_cross_modal_ir_v4_0.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f,h in spec['baseline_sha256'].items():
 assert sha(R/'baseline'/f)==h, f'baseline hash mismatch: {f}'
shots=json.loads((R/'baseline/j4_shots_v2_9.json').read_text())['shots']
sound=json.loads((R/'baseline/j4_sound_ir_v2_8.json').read_text())
assert len(shots)==25 and sum(s['duration_ms'] for s in shots)==90000
cursor=0
for s in shots:
 assert s['start_ms']==cursor and s['end_ms']-s['start_ms']==s['duration_ms']
 assert s['start_ms']*30%1000==0 and s['end_ms']*30%1000==0
 cursor=s['end_ms']
assert cursor==90000 and sound['sample_rate_hz']==48000
assert len(sound['phase_families'])==6 and all(x['forced_stop_ms']==63700 for x in sound['phase_families'])
assert len(spec['arcs'])==3 and len(spec['conditions'])==4
assert {(x['visual'],x['audio']) for x in spec['conditions']}=={(0,0),(1,0),(0,1),(1,1)}
rows=list(csv.DictReader(open(R/'j4_factorial_conditions_v4_0.csv',encoding='utf-8-sig')))
assert len(rows)==12 and all(x['review_state']=='NOT_RUN' for x in rows)
media=list(csv.DictReader(open(R/'j4_stimulus_manifest_v4_0.csv',encoding='utf-8-sig')))
assert len(media)==15 and all(x['material_status']=='MISSING_NOT_RUN' for x in media)
for x in spec['arcs']:
 assert x['origin'] in {s['id'] for s in shots} and x['reveal'] in {s['id'] for s in shots}
alloc=list(csv.DictReader(open(R/'j4_pilot_allocation_v4_0.csv',encoding='utf-8-sig')))
assert len(alloc)==32 and collections.Counter(x['assigned_condition'] for x in alloc)=={x['id']:8 for x in spec['conditions']}
assert all(x['status']=='UNASSIGNED_NO_HUMAN' for x in alloc)
assert spec['immutable_timeline']=={'sine_start_ms':500,'local_S10_cut_ms':38600,'S18_six_phase_stop_ms':63700,'S24_new_market_ms':84000,'S25_sine_only_ms':87000,'end_ms':90000}
print('PASS_STATIC_ONLY: 25 shots / 90,000ms / 6 phases / 3 arcs x 4 conditions / 15 missing media / 32 unassigned slots')
print('NOT_RUN: real media, rights clearance, loudness comparison, human studies, artistic QA')
'''
(OUT/'validate_v4_0.py').write_text(validator)

mediaqa='''#!/usr/bin/env python3
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
'''
(OUT/'media_qa_v4_0.py').write_text(mediaqa)

(OUT/'STATUS_v4_0.md').write_text('''# J4 v4.0 Current Status\n\n- `STATIC_STRUCTURAL`: pending actual test execution\n- `MATERIAL_STIMULI`: BLOCKED_NO_REAL_MEDIA\n- `ORIGINALITY`: NOT_RUN\n- `HUMAN_RECALL`: NOT_RUN\n- `NEON_DIRECTOR_GO`: NOT_OBTAINED\n- `CREDIT_SPEND`: 0 (no calls made in this milestone)\n- `REPOSITORY_MUTATION`: NONE\n''')
print('wrote',OUT, 'files:',len(list(OUT.rglob('*'))))
