import json,csv,hashlib,zipfile,pathlib,html,subprocess,sys,copy
ROOT=pathlib.Path('/mnt/data'); OUT=ROOT/'j4_museum_v3_5'; OUT.mkdir(exist_ok=True)
BASE={
 'g2a_manifest':ROOT/'j4_museum_v3_4/j4_g2a_trial_manifest_v3_4.json',
 'g2a_crosswalk':ROOT/'j4_museum_v3_4/j4_g2a_art_crosswalk.csv',
 'g2a_prompt_delta':ROOT/'j4_museum_v3_4/G2A_CANDIDATE_PROMPT_DELTAS.md',
 'object_registry':ROOT/'j4_museum_v3_2/j4_object_registry_v3_2.json',
 'optical_ir':ROOT/'j4_museum_v3_3/j4_illusion_ir_v3_3.json',
 'shots':ROOT/'j4_museum_v3_2/baseline_shots_v3_1.json',
 'sound':ROOT/'j4_museum_v3_2/baseline_sound_v2_8.json',
 'g1_layout':ROOT/'j4_museum_v3_1/j4_g1_layout_candidate_v3_1.json',
}
raw={k:json.load(open(v,encoding='utf-8')) for k,v in BASE.items() if v.suffix=='.json'}
old_trials={t['id']:t for t in raw['g2a_manifest']['trials']}
art_rows=list(csv.DictReader(open(BASE['g2a_crosswalk'],encoding='utf-8-sig')))
art={(r['trial_id'],r['shot_id']):r for r in art_rows}
all_assets={a['asset_id']:a for a in raw['object_registry']['assets']}
base_shots={s['id'] if 'id' in s else s['shot_id']:s for s in raw['shots']['shots']}
# verify the exact pairs before creating artifacts
expected={'G2A_COAT':('S10','S21'),'G2A_PAPER':('S11','S22'),'G2A_AUTHORITY':('S18','S19')}
assert len(raw['shots']['shots'])==25 and raw['shots']['duration_ms']==90000
for tid,(a,b) in expected.items():
 t=old_trials[tid];assert (t['a'],t['b'])==(a,b)
 assert t['a_media']['start_ms']==base_shots[a]['start_ms']
 assert t['b_media']['end_ms']==base_shots[b]['end_ms']
 assert (tid,a) in art and (tid,b) in art

arcs=[
 {'id':'G2A_COAT','name_zh':'真假外套：身分的延遲揭示','a':'S10','b':'S21','method':'PERCEPTUAL + NARRATIVE_RECONTEXT','mechanism':'FIGURE_GROUND_SHADOW + OBJECT_IDENTITY_CONTRAST','first_read':'外套影子似乎把不在場的人留在制度裡。','second_read':'S21 外套 A 的左下襬有修補，而 S10 的 B 是無修補的檔案版本；觀眾改讀 S10。','cue':'A 有左下襬修補，B 無；S10 短直衣擺，S21 較長。','no_cheat':'不得靠服裝顏色、真人影射、旁白或獨立特寫解題。','art_transfer':'以影子形成暫時的人形錯視，反射支持單物件多重讀法；禁止複製原藝術裝置。','variant_A':'A 修補可見，讓 S10 暫時誤讀；S21 最末焦點讓左下襬成為可查證證據。','variant_control':'只在 S21 以合理的椅背／袖子遮住修補痕；不得替換成另一件衣服。','decision':'CANDIDATE_NOT_APPROVED','media':'MISSING_REAL_STIMULUS','analysis_guard':'影子是光影雙讀；真假衣服是敘事重釋，不應全稱光學錯視。','cross_shots':['S03','S17','S21','S24'],
  'states':[{'shot':'S10','object':'archive_coat_B','state':'ARCHIVED_NO_PATCH','length':'short','repair':False,'identity':'B'},{'shot':'S21','object':'founder_coat_A','state':'ON_CHAIR_REPAIRED','length':'long','repair':True,'identity':'A'}],
  'beats':[{'shot':'S10','local_start_frame':0,'local_end_frame':27,'action':'外套 B 首影格可見；光線讓影子近似人形'},{'shot':'S10','local_start_frame':27,'local_end_frame':93,'action':'鐵門沿途遮擋；38.600 秒局部殘響截斷'},{'shot':'S10','local_start_frame':93,'local_end_frame':105,'action':'門關後空袖移動，沒有真人'},{'shot':'S21','local_start_frame':0,'local_end_frame':54,'action':'唯一黃銅鑰匙由兩隻手準備交接；外套 A 在椅上'},{'shot':'S21','local_start_frame':54,'local_end_frame':99,'action':'鑰匙完成轉移；衣服不得憑空移動'},{'shot':'S21','local_start_frame':99,'local_end_frame':120,'action':'景深轉向外套 A 左下襬修補，須有可辨識的畫面證據'}],
  'visual_anchors':{'S10':{'coat_bbox':[0.32,0.34,0.36,0.34],'shadow_bbox':[0.19,0.28,0.54,0.46]},'S21':{'chair_coat_bbox':[0.38,0.09,0.30,0.28],'key_bbox':[0.44,0.47,0.16,0.12],'repair_subregion_relative':[0.15,0.76,0.18,0.12]}},
  'acceptance':['S10 影子可雙讀，但本體仍是空外套','S21 同一影格只有一件主線外套 A 與一把鑰匙','修補可在最後不少於 21 格的可讀視窗中看見','兩人交接完整、不穿幫、不變手指','A/B 物理區別不依賴顏色或字幕']},
 {'id':'G2A_PAPER','name_zh':'紙屋：從小手作到無人居住的國家','a':'S11','b':'S22','method':'SCALE_DUAL_READ + NARRATIVE_RECONTEXT','mechanism':'MINIATURE_MATERIAL_EVIDENCE + SHARED_FABRICATION_GRAMMAR','first_read':'工廠一張凳子上有尚未完成的小紙屋。','second_read':'S22 精細紙構世界空無一人，S11 紙屋由背景細節變成人類努力的伏筆。','cue':'偏斜的屋頂摺線＋一個不規則狹窗；兩屋是不同實體。','no_cheat':'不把紙模型變成真實地景、不剪入遊戲素材，也不在 S11 放大伏筆。','art_transfer':'用微型物件尺度與紙製空間的真實痕跡，建立雙重尺度認知；不重建原作模型。','variant_A':'S11 紙屋是次要物件，但回看可辨折線；S22 紙海岸第一格就完整。','variant_control':'S22 紙屋改用不相容的屋頂折線與窗形，紙張色溫、尺寸與環境保持相近。','decision':'CANDIDATE_NOT_APPROVED','media':'MISSING_REAL_STIMULUS','analysis_guard':'這主要是尺度雙讀與敘事改讀；並非物件真的從小變大。','cross_shots':['S11','S15','S20','S22'],
  'states':[{'shot':'S11','object':'paper_house_v1','state':'SMALL_INCOMPLETE_STOOL','same_physical_as_S22':False},{'shot':'S22','object':'paper_house_v1','state':'DIFFERENT_HOUSE_SHARED_FOLD_GRAMMAR','same_physical_as_S11':False}],
  'beats':[{'shot':'S11','local_start_frame':0,'local_end_frame':90,'action':'工廠運轉，紙屋作為已存在的次要實物線索'},{'shot':'S11','local_start_frame':90,'local_end_frame':120,'action':'輕微橫移讓紙屋更容易被第二次觀看發現，不作獨立特寫'},{'shot':'S22','local_start_frame':0,'local_end_frame':18,'action':'第一影格完整看見上班族、紙橋、紙世界、空屋'},{'shot':'S22','local_start_frame':18,'local_end_frame':51,'action':'唯一主要動作：食指扶住被空調吹動的紙橋'},{'shot':'S22','local_start_frame':51,'local_end_frame':75,'action':'紙橋穩住，人手停止；紙的物理痕跡清楚'},{'shot':'S22','local_start_frame':75,'local_end_frame':90,'action':'空屋持續無人，沒有新的揭示或動作'}],
  'visual_anchors':{'S11':{'house_bbox':[0.52,0.63,0.19,0.12]},'S22':{'worker_bbox':[0.07,0.42,0.31,0.45],'coast_bbox':[0.26,0.57,0.63,0.36],'bridge_bbox':[0.41,0.68,0.27,0.13],'house_bbox':[0.70,0.46,0.18,0.19]}},
  'acceptance':['S11 回看可辨紙屋、首次不搶產線主題','S11 與 S22 的屋頂折線與窗形一致，但不是相同實物','S22 第一格能看見工人、紙海岸、紙橋、空屋','紙張纖維、膠帶接縫、摺線符合真實結構','S22 僅有手指扶橋的主要動作，無魔法地景變形']},
 {'id':'G2A_AUTHORITY','name_zh':'光形：從抽象訊號到座位權力','a':'S18','b':'S19','method':'RETROSPECTIVE_SHAPE_MATCH','mechanism':'THREE_POSITION_RELATIVE_GEOMETRY + ILLUMINATED_HIERARCHY','first_read':'S18 的低亮三光形沒有國家、人物或地理識別。','second_read':'S19 虛構新聞台三處核心燈光與先前同序、近似相對間距。','cue':'安全框橫向中心 x=[0.32,0.52,0.70]；兩個暗席只在 S19 出現。','no_cheat':'不靠國家配色、政治面孔、標示、閃光或主持人台詞。','art_transfer':'借低解析度形態識別與光的空間權重研究，畫面完全原創。','variant_A':'S18 單次柔和低亮揭露；S19 三處燈位繼承相對位置。','variant_control':'S19 三個主位改成 x=[0.24,0.55,0.84] 的不等距排列；仍為三個、亮度接近。','decision':'CANDIDATE_NOT_APPROVED','media':'MISSING_REAL_STIMULUS','analysis_guard':'S18/S19 是敘事空間重釋；不能以兩個畫面都出現三個光形宣稱知覺錯視成功。','cross_shots':['S18','S19','S21'],
  'states':[{'shot':'S18','object':'three_abstract_light_volumes','state':'LOW_LUMINANCE_ABSTRACT','x_centres':[.32,.52,.70]},{'shot':'S19','object':'five_chairs','state':'THREE_LIT_TWO_DIM','x_centres_lit':[.32,.52,.70],'total_chairs':5}],
  'beats':[{'shot':'S18','local_start_frame':0,'local_end_frame':10,'action':'黑場，六聲部已在 63.700 秒切斷；只剩正弦波'},{'shot':'S18','local_start_frame':10,'local_end_frame':21,'action':'單次低亮顯現三抽象光位，禁止 strobe'},{'shot':'S18','local_start_frame':21,'local_end_frame':30,'action':'低亮淡回黑，避免突變'},{'shot':'S18','local_start_frame':30,'local_end_frame':39,'action':'維持黑場直到 65.000 秒'},{'shot':'S19','local_start_frame':0,'local_end_frame':21,'action':'虛構攝影棚的城市背板逐漸顯現'},{'shot':'S19','local_start_frame':21,'local_end_frame':54,'action':'三個主位逐步亮起，兩個周邊席位維持暗'},{'shot':'S19','local_start_frame':54,'local_end_frame':111,'action':'虛擬城市反射微小時間差，所有椅子仍空著'},{'shot':'S19','local_start_frame':111,'local_end_frame':120,'action':'光位保持不平等狀態，切到記憶檔案室'}],
  'visual_anchors':{'S18':{'x_centres':[.32,.52,.70]},'S19':{'lit_seat_x_centres':[.32,.52,.70],'dim_seats':2,'seat_count':5}},
  'acceptance':['S18 只用一次低亮顯現，不用高頻頻閃','S19 是明顯虛構新聞台，沒有真實峰會標示','三光位及三主位相對配置有精確可檢查的對應','陰影裡保留另外兩個座位，不擬人化政治人物','S18 63.700 秒全局聲音中斷與 S19 65.000 秒開場不變']},
]
for arc in arcs:
 t=old_trials[arc['id']]
 arc['source_arc_id']=t['arc_id']
 arc['source_art']=[{'shot':shot, 'artist':art[(arc['id'],shot)]['artist'], 'work':art[(arc['id'],shot)]['reference_work'], 'url':art[(arc['id'],shot)]['reference_url'], 'not_to_copy':art[(arc['id'],shot)]['not_to_copy']} for shot in (arc['a'],arc['b'])]
 for st in arc['states']:
  a=all_assets[st['object']]
  st['identity_policy']=a['physical_identity_policy']
  st['registry_invariant']=a['invariant']
 arc['timing']={s:{'start_ms':base_shots[s]['start_ms'],'end_ms':base_shots[s]['end_ms'],'duration_ms':base_shots[s]['duration_ms']} for s in (arc['a'],arc['b'])}
 arc['control_guard']='Control only changes the anchor cue, never the broad scene quality, shot duration, physical identity, soundtrack or legal status.'
 arc['trial_status']='NO_MEDIA_NOT_RUN'

manifest={
 'project':'J4 ASYNC: SUCCESSION','version':'v3.5','phase':'G2-A_OBJECT_STATE_PREVIS_LOCK_CANDIDATE','status':'DESIGN_ONLY_NOT_SIGNED','source_lineage':{k:{'path':str(v),'sha256':hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in BASE.items()},
 'film':{'shots':25,'duration_ms':90000,'frame_rate':30,'frames':2700,'s10_local_tail_cut_ms':38600,'s18_global_cycle_cut_ms':63700},
 'governance':{'paid_generation':'BLOCKED','free_visual_generation':'NOT_AUTHORIZED_BY_THIS_PACKAGE','Neon_explicit_approval':'NOT_RUN','director_estimate_posted':'NOT_RUN','9000_monthly_headroom':'NOT_CHECKED','rights_review':'NOT_RUN','source_media_used':False,'original_repo_mutated':False},
 'experiment':{'purpose':'Check whether viewers revise meaning after reveal, based on visible evidence.','status':'NOT_RUN','actual_media':'MISSING','human_participants':0,'human_scores':0,'pilot_recommendation':'5-8 participants; blinded independent reviewers; separate main and negative-control arms','stimulus_warning':'SVG schematics cannot be treated as psychological or optical effect evidence.'},
 'arcs':arcs,
 'source_preservation':'All parent baselines are read-only and original shot prompts remain untouched.',
}
(OUT/'j4_g2a_previs_lock_v3_5.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# 30fps single-source beat table
beat_rows=[]
for a in arcs:
 for b in a['beats']:
  shot=base_shots[b['shot']]
  start_global=int(shot['start_ms']/1000*30)+b['local_start_frame']
  end_global=int(shot['start_ms']/1000*30)+b['local_end_frame']
  beat_rows.append({'arc_id':a['id'],'shot_id':b['shot'],'local_first_frame':b['local_start_frame'],'local_end_frame_exclusive':b['local_end_frame'],'global_first_frame':start_global,'global_end_frame_exclusive':end_global,'absolute_start_ms':round(start_global*1000/30,3),'absolute_end_ms':round(end_global*1000/30,3),'action':b['action'],'status':'DESIGN_ONLY'})
with open(OUT/'j4_g2a_frame_beats_v3_5.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(beat_rows[0]));w.writeheader();w.writerows(beat_rows)

art_out=[]
for a in arcs:
 for r in a['source_art']:
  art_out.append({'arc_id':a['id'],'shot_id':r['shot'],'artist':r['artist'],'artwork':r['work'],'source_url':r['url'],'original_transfer':a['art_transfer'],'do_not_copy':r['not_to_copy'],'source_verification':'INHERITED_FROM_V3.4_NOT_RECHECKED_TODAY','human_rights_review':'NOT_RUN'})
with open(OUT/'j4_g2a_art_optical_crosswalk_v3_5.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(art_out[0]));w.writeheader();w.writerows(art_out)

# state machine DAG / directed transitions
edge_rows=[]
for a in arcs:
 edge_rows.append({'arc_id':a['id'],'source_shot':a['a'],'target_shot':a['b'],'initial_evidence':a['first_read'],'late_reinterpretation':a['second_read'],'physical_anchor':a['cue'],'positive_condition':a['variant_A'],'negative_control':a['variant_control'],'human_readability':'NOT_RUN','rights_status':'NOT_RUN','authorization':'BLOCKED'})
with open(OUT/'j4_g2a_state_transitions_v3_5.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(edge_rows[0]));w.writeheader();w.writerows(edge_rows)

prompts='''# J4 G2-A Object-State Previs Lock｜v3.5（候選增量，尚未授權生成）

本文只新增可驗證的視覺線索，不覆寫 v3.4 的正式 Image/Motion/Sound Prompt。所有藝術品僅供方法研究，不要求模型模仿藝術品。

## G2A_COAT｜S10 → S21

**當代藝術機制：** Tim Noble × Sue Webster《Dirty White Trash (with Gulls)》的物件與影子雙讀；Michelangelo Pistoletto《Man with Yellow Pants》的反射與在場者問題。僅為方法類比，不複製其裝置／構圖。

**S10 — Image addition**

```text
Archived coat B: short, straight-cut, matte charcoal with no repair on the wearer's anatomical LEFT hem. Under a physically motivated overhead practical, the coat, hanger and mesh can cast a mildly human-like shadow; never construct a literal ghost silhouette or recognizable person. The lower hem remains verifiably straight and unpatched on rewatch. Keep the entire structure original.
```

**S21 — Image + Motion addition**

```text
The founder's long coat A is already on the empty chair at frame zero, and the figure passing the key wears only a charcoal SHIRT sleeve. Keep the wearer's LEFT-hem repair in the camera-visible portion of the coat, within the existing chair-with-coat composition zone. After the single brass key changes hands, let focus travel toward the repaired hem for the final 21 frames (0.7 seconds), without an extra cut or zoom. No coat duplication or teleportation. The reflection may briefly split the key's highlight, but only ONE physical key exists.
```

**Control only:** hide A's patch through physically credible occlusion in S21; do NOT turn A into B or change the first shot.

## G2A_PAPER｜S11 → S22

**當代藝術機制：** Liliana Porter 的尺度安排、Thomas Demand 以紙造模型建立「像真實又可看出人造」的雙讀。不能重製其原作，也不能採用《死亡擱淺》專屬道具。

**S11 — Image/Motion addition**

```text
The paper house is an incidental handmade object visible on the blue stool from the start. Its off-centre roof fold and single irregular narrow window must be physically plausible and detectable when replayed, but it must NOT take attention away from the assembly line. No close-up. In the final 30 frames, restrained lateral parallax helps separate the paper house from the background without making it the first-read hero.
```

**S22 — Image/Motion addition**

```text
First frame already includes the fictional Japanese salaryman, a complete miniature handmade paper coastline, one fragile paper bridge and a distant EMPTY illuminated paper house. The house is NOT the S11 physical object, but retains its off-centre roof-fold grammar and a single irregular narrow window. From frame 18 to frame 51, only one fingertip steadies the bridge moved by ventilation. Hold the final frame with the paper shelter still unoccupied. Preserve visible paper fibres, folds and adhesive joins, not a photoreal terrain transformation.
```

**Control only:** change the roof-fold and window geometry of the S22 house while preserving paper quality, lighting, scale, scene complexity and timing.

## G2A_AUTHORITY｜S18 → S19

**當代藝術機制：** Jim Campbell《Exploded Views》的形態聚合與事後辨識；James Turrell《Afrum I (White)》的光／空間體積感。僅借抽象原理，不重製 LED 網格或角落光體。

**S18 — Editor composite addition (NO paid generation)**

```text
Preserve a near-black 9:16 scene. Three abstract dim light centres occupy normalized screen x=0.32, 0.52 and 0.70. Maintain their distinctive unequal spacing. One SOFT low-luminance emergence only, no high-frequency strobe: local frames 0–9 black; frames 10–20 gently reveal; frames 21–29 recede; frames 30–38 return to black. No kings, nations, emblems, numerical annotations, face-like shadows or chairs. Sound cycles remain cut at absolute 63.700 s, with only the persistent original sine underneath.
```

**S19 — Image/Motion addition**

```text
In an unmistakably fictional late-night news-analysis studio, five EMPTY discussion seats surround a circular desk. Three principal soft light pools inherit the x-order and approximate relative spacing of S18's abstract volumes (x=0.32, 0.52, 0.70 normalized inside the 9:16 safe area); two additional seats remain dim. The digital Shenzhen-like skyline is artificial scenery and MUST NOT resemble a real summit broadcast. No news logos, ticker, recognizable politician, geographic national colors or title overlays. No seat actually moves.
```

**Control only:** retain three equally bright main pools but rearrange their normalized x centres to 0.24, 0.55, 0.84; the control is not part of the film.

## Gate

- `DESIGN_ONLY`: all deltas remain candidate; no Canonical Shot IR overwrite.
- Real 9:16 stimuli, signed rights checks, source identity review and Director visual approval must precede human G2-A testing.
- G2-A passage is a separate gate from Higgsfield spending; no generation or points without Neon approval, posted estimate and 9,000-point monthly headroom confirmation.
- Do not call CSS/SVG schematics optical evidence. No human memory data has been gathered.
'''
(OUT/'DIRECTOR_PROMPT_DELTAS_v3_5.md').write_text(prompts,encoding='utf-8')

report=f'''# J4 G2-A v3.5｜Object-State Previs Lock（設計候選）

## 資料來源
本版本直接讀取本次工作環境可存取的 `j4_g2a_trial_manifest_v3_4.json`、`j4_g2a_art_crosswalk.csv`、v3.2 `j4_object_registry_v3_2.json`、v3.1 G1 Layout 及 v3.2 Shot Baseline。父檔保持唯讀，SHA-256 記在 `j4_g2a_previs_lock_v3_5.json`。

## 本次實際完成
- 三條 P0 回響鏈：外套（S10→S21）、紙屋（S11→S22）、權力光形（S18→S19）。
- 六個鏡頭各有原有的藝術對標：Tim Noble × Sue Webster／Michelangelo Pistoletto／Liliana Porter／Thomas Demand／Jim Campbell／James Turrell。
- 記錄正例、反例、不可變物理特徵、原創性排除條件、逐鏡 30 fps 時間窗。
- 預演板為 CSS/SVG 示意圖，並不構成正式視覺刺激、錯視效果或觀眾證據。
- 原 Canonical Shot IR 與原聲音規格完全未修改。

## 三種不同的驗證目的
1. **外套：物件身分。** S10 外套 B 無修補，S21 外套 A 有左下襬修補；不能僅靠相似剪裁推斷兩者相同。 S21 唯一黃銅鑰匙的交接另有物理連續性 Gate。
2. **紙世界：製造語法。** S11 的小紙屋與 S22 的空紙屋不是同一實體，僅共享屋頂折線與窗形。若畫面太小看不到，不得宣稱已建立記憶錨點。
3. **光形：空間排序。** S18 三光位近似 x=[0.32,0.52,0.70]，S19 三核心燈位繼承此順序。若只是「都有三個」，而無法指出間距關係，不計為成功。

## 時碼與計畫
- 25 鏡／90.000 秒／30 fps／2,700 frames。
- S10 本地 3.1 秒、全片 38.600 秒局部音尾截斷，與全局循環無關。
- S18 全片 63.700 秒、1.300 秒，對應 39 影格；無重複頻閃。
- S19 65.000 秒開始，光形 → 座位才揭示意義。
- 作品集與比賽版分開管理；本次示意資料沒有真人照片、作品圖像或品牌資產。

## Sign-off 狀態
| Gate | 狀態 |
|---|---|
| G1 導演人工構圖簽核 | NOT_RUN |
| G2 原創性與權利審核 | NOT_RUN |
| G2-A 真實媒體盲測 | NOT_RUN |
| G3 實際關鍵幀 QC | NOT_RUN |
| Higgsfield 付費生成 | BLOCKED |

## 下一個具體動作
由 Director 檢視本文件與 SVG 線框，決定哪一組 Prompt Delta 值得進入正式 G1 人工簽核。當有具合法權利的實際影像後，使用 v3.4 盲測協定做首次觀看 → 揭示 → 重看，並將正例與負例分配給不同的受試者。

**不能把 SVG 審核板的按鍵測試當成觀眾錯視測試通過。**
'''
(OUT/'DIRECTOR_OBJECT_STATE_LOCK_v3_5.md').write_text(report,encoding='utf-8')
# Build a self-contained SVG *schematic*, not an image or a valid human study stimulus.
board=r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>J4 v3.5｜物件狀態預演</title><style>
:root{font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Noto Sans TC",system-ui,sans-serif;color:#e8e5df;background:#131716}*{box-sizing:border-box}body{margin:0}header{border-bottom:1px solid #363d3a;padding:22px clamp(16px,4vw,52px);background:#171d1b}h1{font-size:clamp(1.35rem,3vw,2rem);margin:.2rem 0}.muted{color:#a8b2ad}.small{font-size:.82rem}.container{max-width:1300px;margin:0 auto;padding:22px 18px 70px}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}.tabs button,.controls button,select{border:1px solid #49564e;background:#242c29;color:#eee9dd;border-radius:10px;padding:10px 13px;cursor:pointer}button.active{background:#adbdab;color:#142018;border-color:#adbdab}button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid #d9ce9c;outline-offset:2px}.card{border:1px solid #3c4841;border-radius:16px;padding:18px;background:#1d2421}.heading{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}h2{font-size:1.24rem;margin:.2em 0}h3{font-size:1.05rem}.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.screen{aspect-ratio:9/16;max-height:510px;max-width:300px;width:100%;margin:auto;border:1px solid #5c6761;border-radius:8px;overflow:hidden;background:#0b0e0e}.screen svg{display:block;width:100%;height:100%}.screenholder{padding:10px;background:#161b19;border-radius:12px;min-height:460px;text-align:center}.tag{font-size:.72rem;letter-spacing:.09em;color:#b4bea4;margin:7px}.note{border-left:3px solid #798d83;padding-left:11px;color:#ced5cc;font-size:.9rem;line-height:1.6}.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:16px 0}.controls label{font-size:.9rem;display:flex;align-items:center;gap:8px}.controls input[type=range]{width:clamp(110px,25vw,300px);accent-color:#aac0a9}a{color:#b9d4c8;overflow-wrap:anywhere}p{line-height:1.7}.reference{padding:9px 0;border-bottom:1px solid #364039}.readouts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:15px 0}.readouts > div{padding:12px;border-radius:10px;background:#27312b;font-size:.82rem}.summary{font-size:.94rem;line-height:1.7}textarea{resize:vertical;width:100%;background:#101715;border:1px solid #43534a;border-radius:8px;color:#fff;padding:11px;font-size:.9rem}.footer{margin-top:18px;font-size:.85rem;color:#a9b6ad}strong{color:#fff}.mini{font-size:.78rem;color:#a8b4ac}.pill{border:1px solid #54685c;border-radius:99px;padding:3px 8px;font-size:.72rem}.global{font-variant-numeric:tabular-nums}@media(max-width:700px){.two{grid-template-columns:1fr}.readouts{grid-template-columns:1fr}.screenholder{min-height:auto}.screen{max-height:440px}}
</style></head><body>
<header><div class="muted small">J4 ASYNC: SUCCESSION · G2-A · v3.5</div><h1>物件狀態與記憶呼喚｜導演預演</h1><p class="muted">本頁僅是自製 SVG 構圖示意。不是原作圖像、真實生成影格，也不是合格的心理學受試刺激。所有導演簽核維持 NOT_RUN，Higgsfield 生成仍 BLOCKED。</p></header>
<main class="container"><div class="tabs" id="tabs"></div><div class="card">
<div class="heading"><h2 id="title"></h2><span class="pill">DESIGN ONLY</span></div><div class="summary" id="intro"></div>
<div class="controls"><label>條件 <select id="condition"><option value="main">正例（預期回響）</option><option value="control">負對照（移除關鍵線索）</option></select></label><label>局部播放位置 <input id="timeline" type="range" min="0" max="100" step="1" value="0"></label><span class="pill global" id="timeReadout">0%</span><button id="reset">回到第一影格</button><button id="export">匯出審核草稿</button></div>
<div class="two"><section class="screenholder"><div class="tag" id="leftlabel"></div><div class="screen" id="leftsvg"></div><p class="mini" id="leftnote"></p></section><section class="screenholder"><div class="tag" id="rightlabel"></div><div class="screen" id="rightsvg"></div><p class="mini" id="rightnote"></p></section></div>
<div class="readouts"><div><strong>物理錨點</strong><p id="cue"></p></div><div><strong>第二次改讀</strong><p id="reveal"></p></div><div><strong>禁止捷徑</strong><p id="guard"></p></div></div>
<h3>當代藝術方法（逐鏡可追溯）</h3><div id="art"></div><h3>人工審核紀錄（只保存草稿，不給出 PASS）</h3><label class="small muted">導演備註</label><textarea rows="3" id="note" placeholder="記錄哪個物理線索可見／不可見；若有真實影像應附版本與時碼"></textarea>
<div class="footer">注意：本頁正例與負對照只有示意構圖，沒有盲測資料或受試者反應。請使用 v3.4 真正的雙次觀看程序，並提供有權使用的實際影格後才可評分。</div>
</div></main>
<script>
const DATA=__MANIFEST_JSON__;
const ids=DATA.arcs.map(x=>x.id);let selected=ids[0],notes={};
const Q=id=>document.getElementById(id);
function esc(s){return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;')}
function shape(type,condition,percent){
 const g=[];const light='#cad4bd',cold='#91a7a8',amber='#cbaa70';
 const rect=(x,y,w,h,fill,stroke='none',rx=0)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}" rx="${rx}"/>`;
 const line=(x,y,x2,y2,stroke,width=2,opacity=1)=>`<line x1="${x}" y1="${y}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}" opacity="${opacity}"/>`;
 const circ=(x,y,r,fill,opacity=1)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" opacity="${opacity}"/>`;
 g.push(rect(0,0,300,534,'#111715'));
 if(type==='S10'){
  g.push(rect(22,35,256,420,'#1e2826'),rect(44,73,210,344,'#293531','#53655e'),line(80,76,80,410,'#526860'),line(215,76,215,410,'#526860'));
  g.push(`<path d="M140 126 L125 142 L105 149 L93 232 L119 243 L126 219 L126 306 L184 306 L184 219 L191 243 L216 232 L205 149 L175 140 L161 126 Z" fill="#626b66" stroke="#b5bdb5" stroke-width="1.8"/>`);
  g.push(line(151,124,151,98,'#a5b9ad',3),`<path d="M141 98 Q151 88 161 98" fill="none" stroke="#b1b7aa" stroke-width="2"/>`);
  g.push(`<path d="M175 137 L213 185 L228 304 L190 287 Z" fill="#64746b" opacity=".15"/>`);
  for(let x=60;x<240;x+=18)g.push(line(x,76,x,400,'#97ab9c',.8,.3));
  for(let y=80;y<410;y+=20)g.push(line(47,y,254,y,'#97ab9c',.8,.3));
  g.push(rect(55,358,190,8,'#65695b'),`<ellipse cx="153" cy="377" rx="35" ry="9" fill="none" stroke="#b9bdaf" stroke-width="2"/>`);
  if(percent>60)g.push(rect(40,100,9,330,'#a9b9ad', 'none',0));
  // B always unpatched
 }
 if(type==='S21'){
  g.push(rect(0,400,300,134,'#242826'),rect(99,56,113,140,'#35403c','#586960',6),rect(113,70,84,122,'#5a6158'));
  g.push(`<path d="M144 71 L123 89 L109 114 L120 179 L185 179 L194 114 L177 88 L164 71 Z" fill="#636d63" stroke="#a2aa9a" stroke-width="2"/>`);
  if(condition==='main' && percent>72) g.push(`<path d="M128 166 l10 -1 l0 10 l-10 0 Z" fill="#cbb187" stroke="#fff4c8" stroke-width=".7"/>`);
  g.push(`<path d="M20 281 Q87 282 130 308 L142 326 Q130 340 109 326 L20 304 Z" fill="#535d59"/>`, `<path d="M280 281 Q224 275 174 310 L166 329 Q185 337 196 320 L280 302 Z" fill="#abb2aa"/>`);
  g.push(rect(144,307,39,7,amber,'#fff1b8',3),circ(141,310,9,'none'), `<circle cx="141" cy="310" r="8" fill="none" stroke="#cbaa70" stroke-width="4"/>`);
  g.push(line(24,376,276,376,'#49544f',5));
 }
 if(type==='S11'){
  g.push(rect(18,70,264,260,'#33423e'),rect(36,100,228,95,'#62746e'),rect(35,215,230,15,'#7c8179'));
  for(let i=0;i<4;i++){let x=50+i*63;g.push(line(x,97,x,136,'#b0bdad',5),line(x,132,x+23,152,'#a6b5a8',6),circ(x+25,156,6,'#e2c38a'))}
  for(let i=0;i<3;i++){let x=52+i*89;g.push(rect(x,368,48,8,'#678392'),line(x+11,376,x+10,418,'#8b9d9d',4),line(x+38,376,x+39,418,'#8b9d9d',4))}
  g.push(`<path d="M169 360 L190 338 L211 360 L211 372 L169 372 Z" fill="#d5cfb5" stroke="#9e9b83" stroke-width="1.5"/>`);g.push(`<path d="M169 360 L192 340 L211 360" fill="none" stroke="#baaa89" stroke-width="2"/>`);
  g.push(rect(190,354,6,11,'#514d44'));
 }
 if(type==='S22'){
  g.push(rect(23,38,254,100,'#32403f'),line(20,154,280,154,'#4f5f5a',3),rect(30,240,239,215,'#48514b'));
  // worker left silhouette
  g.push(circ(73,256,21,'#8d8d7c'),`<path d="M50 276 L102 284 L132 420 L25 420 Z" fill="#5b6058"/>`,line(103,314,149,380,'#aa9880',12));
  g.push(`<path d="M94 405 L150 343 L192 409 L245 345 L265 429 L110 448 Z" fill="#d7d4be" stroke="#aba78d" stroke-width="2"/>`);
  g.push(`<path d="M146 387 Q168 359 187 387" fill="none" stroke="#a88e68" stroke-width="6"/>`);
  // small warm empty house top right
  const roof=condition==='main'?`M207 282 L221 263 L239 275`:`M207 274 L221 254 L239 274`;
  g.push(`<path d="${roof}" fill="none" stroke="#f0e5c5" stroke-width="3"/>`,rect(209,274,30,28,'#ddd7c6','#ded9c7'),condition==='main'?rect(223,282,6,10,amber):`<path d="M215 281 L229 288 L215 295 Z" fill="${amber}"/>`);
  g.push(line(165,423,196,432,'#af9b78',4));
 }
 if(type==='S18'){
  if(percent>=26 && percent<=79){
   const alpha=percent<55?(percent-26)/29*.65:(79-percent)/24*.65;
   const cs=[96,156,210];
   cs.forEach((x,i)=>{g.push(`<rect x="${x-9}" y="${150+i*17}" width="18" height="${140-i*16}" rx="8" fill="${['#d4bd9a','#d5ded4','#b5cad0'][i]}" opacity="${Math.max(0,alpha)}"/>`)});
  }
 }
 if(type==='S19'){
  g.push(rect(20,52,260,205,'#29373b'),rect(22,55,256,190,'#35494e'));
  for(let i=0;i<13;i++){let x=28+i*19,h=[55,85,49,105,65,141,100,70,123,80,98,59,61][i];g.push(rect(x,240-h,12,h,'#617c80'))}
  g.push(`<ellipse cx="150" cy="355" rx="100" ry="38" fill="#475858" stroke="#83908a" stroke-width="3"/>`);
  const centres=condition==='main'?[96,156,210]:[72,165,252];
  centres.forEach((x,i)=>{g.push(`<ellipse cx="${x}" cy="316" rx="23" ry="14" fill="#d5ccb0" opacity=".29"/>`,rect(x-14,302,28,15,'#a4aca4','#d2d3bc',7))});
  [50,270].forEach(x=>g.push(rect(x-13,395,26,15,'#434c4b','#778581',6)));
  g.push(line(40,460,260,460,'#65746b',2));
 }
 let id=`${type}${condition}${percent}`.replaceAll(/[^a-zA-Z0-9]/g,'');
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 534" role="img" aria-label="${esc(type)} 設計構圖示意，非實際畫面"><defs><linearGradient id="bg${id}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#0f1514"/><stop offset="1" stop-color="#25302b"/></linearGradient></defs>${g.join('')}<rect x="1" y="1" width="298" height="532" fill="none" stroke="#647267" stroke-opacity=".4"/></svg>`;
}
function render(){
 const a=DATA.arcs.find(a=>a.id===selected),cond=Q('condition').value,pct=+Q('timeline').value;
 Q('tabs').innerHTML=DATA.arcs.map(x=>`<button class="${x.id===selected?'active':''}" data-id="${x.id}">${esc(x.name_zh)}</button>`).join('');
 Q('tabs').querySelectorAll('button').forEach(b=>b.onclick=()=>{notes[selected]=Q('note').value;selected=b.dataset.id;Q('timeline').value='0';Q('note').value=notes[selected]||'';render()});
 Q('title').textContent=`${a.a} → ${a.b}｜${a.name_zh}`;
 Q('intro').innerHTML=`<p>${esc(a.first_read)}<br><strong>揭示：</strong>${esc(a.second_read)}</p>`;
 const left=a.a,right=a.b;
 Q('leftlabel').textContent=`A・首次觀看 ${left}｜${(a.timing[left].duration_ms/1000).toFixed(1)}s`;
 Q('rightlabel').textContent=`B・後續揭示 ${right}｜${(a.timing[right].duration_ms/1000).toFixed(1)}s`;
 Q('leftsvg').innerHTML=shape(left,cond,pct);Q('rightsvg').innerHTML=shape(right,cond,pct);
 Q('leftnote').textContent=a.states[0].state;
 Q('rightnote').textContent=a.states[1].state;
 Q('timeReadout').textContent=`局部進度 ${pct}%｜${cond==='main'?'正例':'負對照'}（示意）`;
 Q('cue').textContent=a.cue;Q('reveal').textContent=a.second_read;Q('guard').textContent=a.no_cheat;
 Q('art').innerHTML=a.source_art.map(r=>`<div class="reference"><strong>${esc(r.shot)}｜${esc(r.artist)}</strong> — <a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.work)}</a><div class="mini">不複製：${esc(r.not_to_copy)}</div></div>`).join('');
}
Q('timeline').oninput=render;Q('condition').onchange=render;Q('reset').onclick=()=>{Q('timeline').value=0;render()};
Q('export').onclick=()=>{notes[selected]=Q('note').value;const data={version:'v3.5',status:'DIRECTOR_NOT_RUN',mode:'SCHEMATIC_ONLY',selected_arc:selected,condition:Q('condition').value,notes,generated_media:false,human_study:false};const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='j4_g2a_v3_5_director_draft.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),3000)};
render();
</script></body></html>'''
board=board.replace('__MANIFEST_JSON__',json.dumps({'arcs':arcs},ensure_ascii=False).replace('</','<\\/'))
(OUT/'j4_g2a_previs_board_v3_5.html').write_text(board,encoding='utf-8')

# self-check program
validator='''#!/usr/bin/env python3
"""Design-only structural check; does not approve images, rights or generation."""
import json,csv,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'j4_g2a_previs_lock_v3_5.json').read_text(encoding='utf-8'))
assert D['film']=={'shots':25,'duration_ms':90000,'frame_rate':30,'frames':2700,'s10_local_tail_cut_ms':38600,'s18_global_cycle_cut_ms':63700}
assert D['governance']['paid_generation']=='BLOCKED' and D['experiment']['status']=='NOT_RUN'
assert len(D['arcs'])==3
expect={'G2A_COAT':('S10','S21'),'G2A_PAPER':('S11','S22'),'G2A_AUTHORITY':('S18','S19')}
for a in D['arcs']:
 assert (a['a'],a['b'])==expect[a['id']]
 assert a['trial_status']=='NO_MEDIA_NOT_RUN'
 assert len(a['source_art'])==2
 assert len(a['states'])==2
 for s in (a['a'],a['b']):
  beats=sorted([x for x in a['beats'] if x['shot']==s],key=lambda x:x['local_start_frame'])
  assert beats[0]['local_start_frame']==0
  assert beats[-1]['local_end_frame']==a['timing'][s]['duration_ms']*30//1000
  assert all(beats[i]['local_end_frame']==beats[i+1]['local_start_frame'] for i in range(len(beats)-1))
 for ref in a['source_art']:
  assert ref['url'].startswith('https://') and ref['artist'] and ref['work']
A={x['id']:x for x in D['arcs']}
assert A['G2A_COAT']['states'][0]['identity']=='B' and A['G2A_COAT']['states'][1]['identity']=='A'
assert not A['G2A_COAT']['states'][0]['repair'] and A['G2A_COAT']['states'][1]['repair']
assert A['G2A_PAPER']['states'][0]['same_physical_as_S22'] is False
assert A['G2A_AUTHORITY']['states'][0]['x_centres']==A['G2A_AUTHORITY']['states'][1]['x_centres_lit']
assert A['G2A_AUTHORITY']['timing']['S18']['duration_ms']==1300
for f in ['j4_g2a_previs_board_v3_5.html','DIRECTOR_OBJECT_STATE_LOCK_v3_5.md','DIRECTOR_PROMPT_DELTAS_v3_5.md']:
 assert (R/f).stat().st_size>1000
print('PASS: 3 arcs, 6 sourced shot refs, 30fps beat coverage, 90s unchanged, all media NOT_RUN, paid generation BLOCKED')
'''
(OUT/'validate_v3_5.py').write_text(validator,encoding='utf-8')

# build reproducible manifest and zip
checks={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.is_file()}
(OUT/'FILE_SHA256.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
zip_path=ROOT/'j4_museum_v3_5_bundle.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file():z.write(p,arcname=f'j4_museum_v3_5/{p.name}')
print('Built',zip_path,zip_path.stat().st_size,'bytes; files',len(list(OUT.iterdir())))
