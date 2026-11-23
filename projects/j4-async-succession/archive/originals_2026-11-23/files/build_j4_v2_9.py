from pathlib import Path
import json, hashlib, csv, zipfile, textwrap, html
from datetime import datetime

BASE=Path('/mnt/data/j4_museum_v2_8')
OUT=Path('/mnt/data/j4_museum_v2_9')
OUT.mkdir(parents=True,exist_ok=True)
shots_src=BASE/'j4_shots_v2_8.json'
sound_src=BASE/'j4_sound_ir_v2_8.json'
shots=json.loads(shots_src.read_text())
sound=json.loads(sound_src.read_text())
sha=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

meta={
 'version':'v2.9-p1-reference-composition-gate',
 'project':'J4 ASYNC: SUCCESSION',
 'baseline_shots':'j4_shots_v2_8.json',
 'baseline_shots_sha256':sha(shots_src),
 'baseline_sound':'j4_sound_ir_v2_8.json',
 'baseline_sound_sha256':sha(sound_src),
 'status':'DESIGN_ONLY_NOT_RENDERED_NOT_APPROVED',
 'media_used':'User-supplied visual references inspected only to document prohibited visual resemblance; no uploaded frame or image embedded into the deliverables',
 'focus_shots':['S03','S13','S22','S24'],
 'timeline':'25 shots / 90000 ms / 30 fps unchanged',
 'render_policy':'NO image/video/audio generation; NO Higgsfield calls; original repo untouched',
 'approval_gate':['Neon explicit GO','Director estimate posted to AI Video Production Service','current month balance/headroom verified against 9000-credit limit','rights and contest-specific review'],
 'frame_canvas':{'aspect':'9:16','design_pixels':[1080,1920],'units':'bbox normalized [x,y,width,height]','end_frame':'exclusive','horizontal':'must be authored independently in 16:9, never automatically certified by a 9:16 crop'},
 'acceptance_principle':'Spec geometry is a director target, not a measurement of generated output. Image, resemblance, accessibility and sound checks stay NOT_RUN until actual reviewed assets exist.'
}

def zone(name,bbox,role,first=True,p=2,minpx=None,notes=''):
 return {'name':name,'bbox':bbox,'priority':p,'required_at_first_frame':first,'min_width_px_on_1080':minpx,'role':role,'notes':notes}

boards=[
 {'shot_id':'S03','name':'The Source','time_ms':[7000,12000],'focus':'孤獨人物與不封閉的光學薄膜之關係','lens':'35mm','camera':'locked, eye height ~1.45m; no forced low-angle tank likeness',
  'frame_0_takeaway':'一位背對鏡頭的人站在巨大空間中，面對不封閉、非盒狀的光學薄膜','dominant_action':'一顆水滴緩慢移動；光影稍後偏移（後製時間偏差，不宣稱光速延遲）',
  'light':'Hidden pale fixture through curved translucent membranes; cold caustic floor pattern; a single warm spill, source motivated',
  'silence':'Marketplace bed recedes, one isolated piano attack independent of droplet; maintain room tail toward S04',
  'required_reference_transformation':['Source contains suspended square open glass water vessel; J4 uses non-closed, non-rectangular separated vertical curved polymer membranes','Reference is top-down close architectural object; J4 is floor-level wide with one small back-view figure','Reference glow/steam is literal; J4 uses restrained condensation and caustics without voluminous boiling cloud'],
  'forbidden_similarity':['four-sided suspended open tank','corner-cable aquarium geometry','identical high-angle rhombus outline','large white central boiling mist surface','copy of actual museum installation'],
  'zones':[
   zone('optical_membranes',[.14,.20,.75,.40],'layered non-closed curved light surfaces',True,1,500,'negative gaps between sheets must be visible'),
   zone('fictional_founder',[.41,.65,.18,.26],'back-only person wearing coat A',True,1,140,'feet supported by floor; face never visible'),
   zone('floor_caustic',[.19,.78,.64,.12],'physical floor-light response',True,2,350,'avoid literal glowing square under tank'),
   zone('warm_trace',[.48,.70,.08,.07],'local tungsten reflection only',False,3,40,'not a magical transported beam')],
  'negative_space':[{'bbox':[.02,.02,.96,.15],'why':'quiet architectural ceiling above system'},{'bbox':[.02,.49,.25,.26],'why':'keep lateral breathing room'}],
  'first_frame_must':['open gaps in membrane structure','small founder back silhouette','real floor and source of optical light'],
  'physical_guard':['caustics follow droplet geometry and local illumination, editorial delay is intentionally composited','figure cannot levitate','membranes must have plausible suspension without reproducing tank corner frame'],
  'exit_handoff':'Thin warm light trace in floor cuts to metal filament detail in S04',
  'risk':'IP/source shape similarity, unnatural refractive delay, silhouette identity',
  'review_dependencies':['S02','S04','S17','S23']},
 {'shot_id':'S13','name':'The Untuned','time_ms':[46000,50000],'focus':'工藝與自然時間的衝突，沒有災難畫面','lens':'35mm','camera':'locked medium-wide, three-quarter view from entrance; not the artwork installation view',
  'frame_0_takeaway':'受鹽霧影響的直立鋼琴與手持晶圓的年長技師同處臨海測試廳','dominant_action':'技師按下一個不完全回彈的琴鍵；琴聲缺席',
  'light':'A real window supplies marine grey daylight; wafer catches a narrow spot on piano keys; one working equipment LED',
  'silence':'Key mechanism only, not full note; thin unstable overtone crosses into S14 applause',
  'required_reference_transformation':['Do not recreate a documented tsunami piano installation; invented coastline test hall and unique piano wear','Camera must reveal technician+wafer+instrument spatial relationship rather than isolated damaged art object','Make instrument a plausible older upright without exact original tsunami-damage patterns'],
  'forbidden_similarity':['exact damaged real piano shape or damage distribution','real natural disaster photographs','original installation light and speaker arrangements','national banners or real factory names'],
  'zones':[
   zone('sea_window',[.08,.10,.86,.36],'off-screen daylight and sea atmosphere',True,2,550,'keep horizon through windows subtle'),
   zone('weathered_piano',[.12,.49,.47,.34],'aged upright, lower wood swelling',True,1,360,'keys visible on right-facing angle'),
   zone('technician',[.59,.39,.27,.44],'dignified elderly fictional technician',True,1,180,'near enough to reach keyboard without rubber limbs'),
   zone('wafer',[.56,.51,.13,.10],'one silicon disc, safe grasp',True,2,95,'small glint on keys, no brand')],
  'negative_space':[{'bbox':[.04,.04,.92,.06],'why':'cold ceiling / sense of quiet age'},{'bbox':[.16,.85,.7,.12],'why':'soundless bare floor'}],
  'first_frame_must':['piano identity and physical damage','technician and held wafer','window indicating coastal lab'],
  'physical_guard':['key moves down and may stick, no implausible large destruction','wafer one disc with realistic grip','wafer reflection occurs only with coherent lighting geometry'],
  'exit_handoff':'Incomplete key sound replaced by institutional applause in S14',
  'risk':'misreading as actual disaster footage; key/hand deformation; wafer reflection impossible',
  'review_dependencies':['S12','S14','S23']},
 {'shot_id':'S22','name':'The Paper Shore','time_ms':[76500,79500],'focus':'上班族、一座紙橋、遠方無人小屋；第一影格即可讀','lens':'35mm','camera':'locked slightly elevated three-quarter, NOT an extreme overhead photo of a Demand artwork',
  'frame_0_takeaway':'獨自在深夜辦公室工作的上班族用手維持一座沒有居民的紙世界','dominant_action':'唯一主動作：食指扶住被通風晃動的紙橋（0.6–1.7s）',
  'light':'Cold fluorescent office light; one small tungsten-lit but unoccupied house; workstation unobtrusive',
  'silence':'Finger on real paper prominent; one off-beat felt piano after action, room ventilation; no heroic cue',
  'required_reference_transformation':['Do not copy Death Stranding geography, transport costumes, BB technology or icon props; abstract isolation and fragile routes only','Do not recreate Thomas Demand Office camera, object layout or photographic sculpture; paper-making process is visible','Do not assert Japanese workers are generally unproductive; scene critiques certain organizational incentives'],
  'forbidden_similarity':['Death Stranding recognizable backpack, bridge devices, BB pod, iconography','a one-to-one scale recreation of Demand Office','left-right simplistic AI versus human billboard','Japanese flags, invented statistical captions'],
  'zones':[
   zone('real_city_window',[.10,.09,.82,.31],'dark but real metropolis beyond office',True,3,420,'secondary visual contrast'),
   zone('salaryman',[.07,.43,.33,.44],'dignified worker face not center',True,1,200,'hands visible and one fingertip touches bridge'),
   zone('paper_geography',[.26,.57,.63,.36],'real folded paper coast and settlements',True,1,480,'paper folds must be clear at first frame'),
   zone('fragile_bridge',[.44,.68,.23,.11],'one foreground critical bridge',True,1,155,'dominant gesture land here'),
   zone('empty_paper_house',[.67,.48,.16,.18],'tiny physically folded house with warm empty window',True,1,135,'visibly unoccupied, legible at 1x'),
   zone('local_compute',[.83,.42,.11,.08],'very small unbranded compact workstation',False,3,70,'never visual hero')],
  'negative_space':[{'bbox':[.01,.03,.09,.91],'why':'compress human under office scale'},{'bbox':[.42,.15,.30,.21],'why':'office negative space / no holograms'}],
  'first_frame_must':['worker silhouette','paper bridge','warm empty house','clear office rather than actual wasteland'],
  'physical_guard':['all structures paper with seams, bends and gravity','one fingertip stabilizes not repairs/constructs bridge','no apparently animated humans in miniatures','unbranded workstation stays idle'],
  'exit_handoff':'Paper scraping fades into vast optical-chamber room tone at S23',
  'risk':'too many story objects in 3 seconds; paper house illegible; game/art similarity',
  'review_dependencies':['S11','S21','S23']},
 {'shot_id':'S24','name':'The Return','time_ms':[84000,87000],'focus':'外套第一影格已被高舉，唯一主要動作是光鳥落下','lens':'35mm','camera':'fixed low moderate wide / intimate, no anthem crane-up',
  'frame_0_takeaway':'夜市日常中的人們默默托起一件空外套，細小光鳥即將落在肩部','dominant_action':'唯一主動作：不具徽章輪廓的細線發光小鳥落在外套肩部（0.8–2.0s）',
  'light':'Ordinary warm market lamps and wet pavement; rain already falling at frame 0, not triggered by landing',
  'silence':'Fresh human-market-memory sound, no 7s loop restart; note fragments; hard cut to sine-only at 87s',
  'required_reference_transformation':['No borrowed reference water vessel here; water appears only as ordinary rain and pavement reflections','No real IPO group photo, podium or all-at-once applause choreography','No Mockingjay silhouette, film costume or recognizable celebrity leather jacket'],
  'forbidden_similarity':['raised celebrity-identifiable leather jacket','large stylized bird emblem/pin','news ceremony group staging or podium','perfectly synchronized heartbeat bulb grid'],
  'zones':[
   zone('market_bulbs',[.08,.12,.84,.20],'irregular ordinary practical bulbs',True,2,460,'not grid/canopy copy from reference'),
   zone('coat_A',[.33,.38,.36,.30],'same unique work coat A empty and raised',True,1,250,'LEFT hem repair from Bible, no leather signature'),
   zone('supporting_hands',[.20,.59,.61,.20],'multiple ordinary hands already holding coat',True,2,380,'stable shoulders and five fingers'),
   zone('bird_entry',[.53,.27,.14,.13],'filament bird v1 approach zone',False,1,90,'visible after 0.8s, lands near coat shoulder'),
   zone('market_ensemble',[.06,.72,.90,.23],'fictional crowd differentiated by gesture',True,2,500,'faces not recognizable, no political protest'),
   zone('rain_pavement',[.04,.91,.92,.08],'subtle physical wet reflection',True,3,500,'rain already present at start')],
  'negative_space':[{'bbox':[.03,.34,.21,.18],'why':'give coat silhouette breathing space'},{'bbox':[.76,.38,.21,.16],'why':'avoid busy crowd behind bird landing'}],
  'first_frame_must':['raised EMPTY coat A','human hands clearly supporting','real market ambience and rain already visible'],
  'physical_guard':['one bird landing onto textile with contact/weight, no spontaneous material morph','same bird filament location and 3 join points as S04','no crowd lift motion after t=0, only incidental breathing'],
  'exit_handoff':'At 87.0s hard black; all fresh ambience stripped to phase-continuous sine',
  'risk':'coat vs old B, bird mismatch, motion overload, crowd action resemblance',
  'review_dependencies':['S02','S04','S21','S23','S25']}
]

asset_rows=[
 ('optical_membranes','S03,S17,S23','open separated curved translucent optical sheets','S03: sparse / S17: dense / S23: near-dormant','must not close into a suspended box or squared water vessel','DESIGN_ONLY'),
 ('founder_coat_A','S03,S17,S21,S24','long charcoal, small repair at LEFT hem','S03/S17 worn; S21 hangs from chair at start; S24 crowd holds same empty coat','distinct from archive coat B; no leather-celebrity cues','DESIGN_ONLY'),
 ('archive_coat_B','S10','short straight charcoal cotton, NO left-hem repair','archived earlier specimen; unrelated physical garment','never passed in S21 or raised in S24','DESIGN_ONLY'),
 ('filament_bird_v1','S04,S24','one soft tungsten filament, three minute wire joins, asymmetric','leaves S04; in S24 starts outside central coat then settles','never iconic logo/feathers or known fictional emblem','DESIGN_ONLY'),
 ('paper_house_v1','S11,S22','plain paper; irregular folded roof; one nonrectangular window','same fabrication grammar, NOT transported from S11 to S22','S22 house is unoccupied; must be legible on first frame','DESIGN_ONLY'),
 ('paper_bridge_v1','S22','folded office-paper bridge with real load-bearing crease','stabilized by one fingertip in one dominant action','no game-specific engineering structures','DESIGN_ONLY'),
 ('untuned_piano','S13,S23','aged upright with swollen lower timber; one slow returning key','S13 foreground original; S23 distant thematic echo on dolly','not the documented disaster-damaged instrument','DESIGN_ONLY'),
 ('market_environment','S02,S24','humble warm practical bulbs; humid surfaces; ordinary stall wear','same visual grammar, not same image or camera location','no copied original photo installation or news scene','DESIGN_ONLY'),
 ('warm_reflection','S02,S03,S04,S05,S06,S17,S23,S24','thin nonuniform warm reflection from LOCAL practical light','match in editorial form across scenes, not physically travelling','every scene must identify its own real source','DESIGN_ONLY'),
 ('handover_key','S21','one undecorated small brass key','hands share object at midpoint; founder already without coat','no teleport, no duplicated key or malformed contact','DESIGN_ONLY'),
 ('sine_master','S01-S25','single continuous original low sine from 0.5s','survives 63.7s global interruption and 87.0s ambience strip','no borrowed Sakamoto audio; de-click terminal boundary','DESIGN_ONLY')
]

# Per-shot framing notes and readiness fields; preserve original prompts without substitution.
shot_copy=json.loads(json.dumps(shots))
shot_copy['version']='v2.9-reference-composition-design-only'
shot_copy['status']='KEYFRAME_COMPOSITION_SPEC_ONLY; NO_ASSET_RENDERED; RIGHTS_QC_NOT_RUN'
shot_copy['governance']['v2_9_scope']='Add compositional references to S03/S13/S22/S24 only; v2.8 prompts/motion/timing/sound unchanged.'
shot_copy['governance']['v2_9_generation_allowed']=False
shot_copy['governance']['v2_9_reference_gate']='Four first-frame wireframe rectangles are planning targets; not approved/generated keyframes.'
board_by={b['shot_id']:b for b in boards}
for s in shot_copy['shots']:
 if s['id'] in board_by:
  b=board_by[s['id']]
  s['composition_gate']={
   'reference_board':'j4_keyframe_composition_v2_9.json',
   'first_frame_takeaway':b['frame_0_takeaway'],
   'focal_zones':[{k:z[k] for k in ['name','bbox','priority','required_at_first_frame']} for z in b['zones']],
   'evidence_state':'NOT_RUN_NO_FRAME',
   'signoff_required':['director','continuity','IP/source_similarity','sound_owner','Neon_generation_approval']
  }
 else:
  s['composition_gate']={'status':'NOT_IN_V2_9_FOCUS; v2_8 UNCHANGED','evidence_state':'NOT_RUN_NO_FRAME'}

board_data={'metadata':meta,'boards':boards}
(OUT/'j4_keyframe_composition_v2_9.json').write_text(json.dumps(board_data,ensure_ascii=False,indent=2)+'\n')
(OUT/'j4_shots_v2_9.json').write_text(json.dumps(shot_copy,ensure_ascii=False,indent=2)+'\n')

with (OUT/'j4_asset_lock_registry.csv').open('w',newline='') as f:
 w=csv.writer(f)
 w.writerow(['asset_id','shots','design_lock','continuity','forbidden','status'])
 w.writerows(asset_rows)

checklist=[]
for b in boards:
 for cat,items in [
  ('first_frame',b['first_frame_must']),('physical',b['physical_guard']),
  ('anti_recreation',b['forbidden_similarity']),
  ('handoff',[b['exit_handoff']]),
  ('source_transfer',b['required_reference_transformation'])]:
  for i,desc in enumerate(items,1):
   checklist.append({'shot_id':b['shot_id'],'category':cat,'check_id':f"{b['shot_id']}-{cat}-{i:02}",'acceptance':desc,'status':'NOT_RUN_NO_RENDER','reviewer':'','evidence_uri':'','notes':''})
with (OUT/'j4_composition_acceptance.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checklist[0]));w.writeheader();w.writerows(checklist)

# 9:16 storyboard target specs and independently authored 16:9 composition obligations.
md=[]
md.append('# J4 v2.9 — Reference & Keyframe Composition Gate\n')
md.append('**狀態：DESIGN_ONLY / NOT_GENERATED / NOT_APPROVED**。本包是幾何規格、人工驗收表和線框板，不是 AI 生成圖片或已確認的構圖。原始 repository 未修改。')
md.append('\n## 固定控制項\n')
md.extend(['- 基準：`j4_shots_v2_8.json`；25 鏡、90.000 秒、30 fps、2,700 frames **保持不變**。',
           '- 焦點：S03、S13、S22、S24。其他 21 鏡沿用 v2.8。',
           '- 9:16 構圖板坐標：1080×1920 的標準化 `[x,y,w,h]`；盒子是**目標視覺區域**，不是測到的畫面或模型保證。',
           '- 繪製方式：HTML 線框及原始幾何區域；**沒有生成圖片、影片、音訊或使用影片影格**。',
           '- 16:9 必須獨立構圖：不能僅從 9:16 畫面擴展／裁切後宣稱已通過；需重做 16:9 的區域佈局及檢查。',
           '- 全局聲音：S18 的 63.700 秒六組循環同時中斷；S25 正弦波仍持續；本輪不修改 Sound IR。',
           '- 生成閘口仍為 BLOCKED：Neon 明確 GO → Director 在 AI Video Production Service 貼最新估點 → 確認本月 9000 點額度餘裕 → 權利／賽規複核。'])
md.append('\n## 原始素材的轉譯邊界\n')
md.extend(['1. 原始水箱照片只提供懸吊、濕度、光學、水霧的**物理觀念**；J4 不採封閉方形玻璃箱、中央菱形吊框、四角吊線與上視角構圖。',
           '2. 原始 X 上市新聞截圖只提供制度表演、舞台行為與公眾儀式的**敘事觀念**；J4 不使用真實標誌、人物、新聞台字幕、講台或隊形。',
           '3. 當代藝術與《死亡擱淺》只借創作方法／孤獨運送機制；不重現任何作品的辨識性造型、音訊、場景或人物。',
           '4. 比賽候選版完全避開可辨認真人、政治新聞仿製或現有影像 plate；不因抽象化便宣稱必定合規。',
           '5. S03 的「光反射延遲」是**剪輯合成的時間概念**，不是可在同一介質中自然產生可見光速延遲的物理現象。'])
for b in boards:
 md.append(f"\n## {b['shot_id']}｜{b['name']}（{b['time_ms'][0]/1000:.1f}–{b['time_ms'][1]/1000:.1f}s）\n")
 md.append(f"**首影格須讀懂：** {b['frame_0_takeaway']}。\n")
 md.append(f"**鏡頭：** {b['lens']}，{b['camera']}。\n")
 md.append(f"**唯一動作：** {b['dominant_action']}。\n")
 md.append(f"**物理光線：** {b['light']}。\n")
 md.append(f"**聲音接力：** {b['silence']}。\n")
 md.append('| 物件／元素 | 正規化 x,y,w,h | 優先級 | 第一影格 |')
 md.append('|---|---|---|---|')
 for z in b['zones']:
  md.append('| '+z['name']+' | `'+','.join(f'{v:.2f}' for v in z['bbox'])+f"` | P{z['priority']} | "+('是' if z['required_at_first_frame'] else '否')+' |')
 md.append('\n**不可雷同的形狀：** '+ '；'.join(b['forbidden_similarity'])+'。')
 md.append('\n**前後連續性：** '+b['exit_handoff']+'。')
 md.append('\n**風險與前置鏡頭：** '+b['risk']+'；依賴 '+', '.join(b['review_dependencies'])+'。')
md.append('\n## 逐階段的 Gate（所有影像驗證目前 NOT_RUN）\n')
md.extend(['1. `G0 TEXT/GEOMETRY`：驗證 JSON、影格與道具 ID；只表示靜態契約可用。',
           '2. `G1 DIRECTOR COMPOSITION`：導演檢查四張線框板是否有故事焦點與負空間，至少一個獨立第一影格讀懂目標。',
           '3. `G2 REFERENCE DISTANCE`：對上傳原始照片、25 件對標藝術品做人工「不重製」審核；每鏡至少在物件幾何、攝影位置、敘事功能上保有獨立創作。不能只靠負面 Prompt。',
           '4. `G3 ASSET/CONTINUITY`：全片道具 Lock（coat A≠B、bird v1、paper house 工藝、optical membranes 三個階段）在未來真實 keyframe 中逐鏡比對。',
           '5. `G4 1× BLIND VIEWING`：只有真實影像可被評分；S22 先辨認紙橋與無人小屋、S24 一開始外套已舉起；未生成前不得填 PASS。',
           '6. `G5 AUDIO/LEGAL/ACCESSIBILITY`：原創音訊、人聲權利、照片敏感光反應、賽規與計點經實物和最新規則確認。',
           '7. `G6 PAID GO`：經 Neon 明確批准 + Director 貼估點 + 9000 點餘額核驗後，才可以啟動任何媒體生成。'])
md.append('\n## 尚未關閉的 Blockers\n')
md.extend(['- 原 repo `pipeline/build_animatic.py` 與 `shots.json` schema 尚未取得：legacy adapter compatibility `NOT_TESTED`。',
           '- 作品集版／比賽候選版是分流規格，不代表 90 秒預告符合原文記載的 3–7 分鐘正式片長。',
           '- 所有實際 keyframe、 motion、音訊、IP/肖像、字幕與光敏感審核仍 `NOT_RUN`。',
           '- 以上所有標示 P1、最小像素、區域距離都是 **設計門檻**，不是已經量測的模型輸出。'])
(OUT/'README_v2_9.md').write_text('\n'.join(md)+'\n')

# Lightweight browsable local geometry board; no real photos included.
html_source=r'''<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>J4 v2.9｜Keyframe Composition Gate</title>
<style>
:root{font-family:system-ui,-apple-system,"Noto Sans TC",sans-serif;color:#e6e9ed;background:#0c1118;color-scheme:dark}
*{box-sizing:border-box}body{margin:0}header{border-bottom:1px solid #303943;padding:24px max(4vw,18px);background:#131a22}
header h1{font-size:clamp(23px,3.5vw,37px);margin:0 0 8px}h2{font-size:22px;margin:0 0 12px}p{line-height:1.6}
.muted{color:#aab8c7}.pill{display:inline-block;border:1px solid #668197;color:#c9e8f8;border-radius:50px;padding:3px 10px;font-size:12px}
.shell{display:grid;grid-template-columns:minmax(260px,380px) minmax(260px,390px) minmax(280px,1fr);gap:24px;padding:28px max(4vw,18px)}
nav{display:flex;gap:9px;flex-wrap:wrap}.tab{border:1px solid #405363;background:#172331;color:#d7e6ef;padding:9px 12px;border-radius:8px;cursor:pointer}.tab[aria-selected=true]{background:#355b72;border-color:#87bdd4;color:white}
.panel{padding:16px;border:1px solid #324352;border-radius:14px;background:#121b24}ul{padding-left:20px}li{margin-bottom:8px;line-height:1.5}
.canvas-wrap{display:flex;justify-content:center;position:relative}.canvas{width:min(100%,330px);aspect-ratio:9/16;position:relative;background:linear-gradient(#19232c,#0e151a 63%,#242727);border:2px solid #607180;overflow:hidden}
.zone{position:absolute;border:1px solid;border-radius:4px;background:rgba(67,140,180,.18);font-size:11px;display:flex;align-items:center;justify-content:center;text-align:center;padding:3px;overflow:hidden;line-height:1.25}
.zone.p1{border-color:#c4ad7d;background:rgba(199,164,103,.2)}.zone.p2{border-color:#7cb4ce;background:rgba(79,136,160,.2)}.zone.p3{border-color:#8cabb5;background:rgba(86,117,132,.13)}
.zone span{background:rgba(8,15,22,.72);padding:2px;border-radius:3px}.negative{position:absolute;border:1px dashed #506375;background:repeating-linear-gradient(135deg,transparent,transparent 8px,rgba(95,117,136,.08) 8px,rgba(95,117,136,.08) 11px);pointer-events:none}
.note{font-size:12px;color:#aab8c7}.kicker{letter-spacing:.08em;font-size:12px;text-transform:uppercase;color:#88b1c5}.item{padding:12px 0;border-top:1px solid #273540}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px}.info-grid div{background:#1b2834;padding:10px;border-radius:6px}.small{font-size:13px}
footer{padding:20px max(4vw,18px);border-top:1px solid #29333c;color:#abb9c6}
@media(max-width:1040px){.shell{grid-template-columns:1fr 1fr}.details{grid-column:1/-1}}@media(max-width:650px){.shell{grid-template-columns:1fr}.details{grid-column:auto}}
</style></head><body>
<header><span class="pill">DESIGN ONLY • 0 IMAGE GENERATION • NOT APPROVED</span>
<h1>J4｜Keyframe Composition Gate</h1>
<p class="muted">v2.9｜四鏡 9:16 首影格構圖線框：只標示相對位置與動作優先順序。不是生成圖片，也不是通過視覺 QC。</p></header>
<div class="shell">
<section class="panel"><div class="kicker">選擇鏡頭</div><nav id="tabs" aria-label="鏡頭"></nav><div style="height:20px"></div>
<h2 id="title"></h2><p class="muted" id="takeaway"></p>
<div class="info-grid"><div><div class="kicker">Lens</div><strong id="lens"></strong></div><div><div class="kicker">Time</div><strong id="time"></strong></div></div>
<h3>第一影格必見</h3><ul id="firstframe"></ul><h3>唯一主動作</h3><p id="action"></p>
<p class="small muted">優先級：金色 P1 = 必須優先閱讀；藍色 P2 = 輔助；灰色 P3 = 背景。</p></section>
<section class="panel"><div class="canvas-wrap"><div class="canvas" role="img" aria-label="僅供構圖確認的9比16幾何線框示意" id="canvas"></div></div>
<p class="note">標記的位置不是定稿影格；需在未來實際生成後以 1× 速度測試可辨識度。</p></section>
<section class="panel details"><h2>參考來源轉譯與防重製</h2><p id="risk"></p><h3>不可複製</h3><ul id="banned"></ul>
<h3>聲音與接力</h3><p id="audio"></p><p id="handoff"></p>
<h3>道具與跨鏡對照</h3><p id="deps"></p>
<h3>需要真人審核</h3><p class="muted">Director 首影格、IP/素材差異、物理真實性、Motion、Sound、Contest eligibility。全部 <strong>NOT_RUN</strong>；沒有自動核准按鈕。</p></section>
</div><footer>J4 v2.9｜不連網、不包含實拍影格與生成圖、不呼叫任何媒體生成或計點 API。原始影片與圖片未嵌入。</footer>
<script>
const data=__BOARD_DATA__;
const tabs=document.getElementById('tabs');
let active='S03';
function esc(s){return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;')}
function render(){let b=data.boards.find(b=>b.shot_id===active);
 tabs.innerHTML=data.boards.map(x=>`<button class="tab" type="button" aria-selected="${x.shot_id===active}" data-id="${x.shot_id}">${x.shot_id}</button>`).join('');
 document.getElementById('title').textContent=b.shot_id+' · '+b.name;
 document.getElementById('takeaway').textContent=b.frame_0_takeaway;
 document.getElementById('lens').textContent=b.lens;
 document.getElementById('time').textContent=(b.time_ms[0]/1000).toFixed(1)+'–'+(b.time_ms[1]/1000).toFixed(1)+'s';
 document.getElementById('firstframe').innerHTML=b.first_frame_must.map(x=>`<li>${esc(x)}</li>`).join('');
 document.getElementById('action').textContent=b.dominant_action;
 const canvas=document.getElementById('canvas');
 canvas.innerHTML=b.negative_space.map(n=>{let [x,y,w,h]=n.bbox;return `<div class="negative" style="left:${x*100}%;top:${y*100}%;width:${w*100}%;height:${h*100}%" title="${esc(n.why)}"></div>`}).join('')+b.zones.map(z=>{let [x,y,w,h]=z.bbox;return `<div class="zone p${z.priority}" style="left:${x*100}%;top:${y*100}%;width:${w*100}%;height:${h*100}%" title="${esc(z.role)}"><span>${esc(z.name)}</span></div>`}).join('');
 document.getElementById('banned').innerHTML=b.forbidden_similarity.map(x=>`<li>${esc(x)}</li>`).join('');
 document.getElementById('risk').textContent=b.risk;
 document.getElementById('audio').textContent=b.silence;
 document.getElementById('handoff').textContent=b.exit_handoff;
 document.getElementById('deps').textContent=b.review_dependencies.join(' → ');
}
tabs.addEventListener('click',ev=>{let btn=ev.target.closest('button[data-id]');if(btn){active=btn.dataset.id;render()}});
render();
</script></body></html>'''
html_source=html_source.replace('__BOARD_DATA__',json.dumps(board_data,ensure_ascii=False).replace('</','<\\/'))
(OUT/'j4_wireframe_board_v2_9.html').write_text(html_source)

# Offline validation script, appropriate for run from any cwd.
validator='''from pathlib import Path
import json,csv,hashlib,sys
DIR=Path(__file__).resolve().parent
base=Path('/mnt/data/j4_museum_v2_8')
B=json.loads((DIR/'j4_keyframe_composition_v2_9.json').read_text())
X=json.loads((DIR/'j4_shots_v2_9.json').read_text())
baseX=json.loads((base/'j4_shots_v2_8.json').read_text())
baseS=base/'j4_sound_ir_v2_8.json'
assert hashlib.sha256((base/'j4_shots_v2_8.json').read_bytes()).hexdigest()==B['metadata']['baseline_shots_sha256']
assert hashlib.sha256(baseS.read_bytes()).hexdigest()==B['metadata']['baseline_sound_sha256']
assert len(X['shots'])==len(baseX['shots'])==25
assert X['duration_ms']==90000
assert [(s['id'],s['start_ms'],s['end_ms']) for s in X['shots']]==[(s['id'],s['start_ms'],s['end_ms']) for s in baseX['shots']]
assert X['shots'][-1]['end_ms']==90000 and X['shots'][17]['start_ms']==63700
assert all(s['image_prompt']==b['image_prompt'] and s['motion_prompt']==b['motion_prompt'] and s['sound_prompt']==b['sound_prompt'] for s,b in zip(X['shots'],baseX['shots']))
assert all(s['review_state']==b['review_state'] for s,b in zip(X['shots'],baseX['shots']))
assert len(B['boards'])==4 and {b['shot_id'] for b in B['boards']}==set(B['metadata']['focus_shots'])
for board in B['boards']:
 sh=next(s for s in X['shots'] if s['id']==board['shot_id'])
 assert board['time_ms']==[sh['start_ms'],sh['end_ms']]
 assert len(board['zones'])>=4
 assert any(z['priority']==1 and z['required_at_first_frame'] for z in board['zones'])
 for z in board['zones']:
  x,y,w,h=z['bbox']
  assert 0<=x<=1 and 0<=y<=1 and w>0 and h>0 and x+w<=1.000001 and y+h<=1.000001,(board['shot_id'],z)
  if z['min_width_px_on_1080'] is not None:assert w*1080>=z['min_width_px_on_1080'],(board['shot_id'],z['name'])
 for z in board['negative_space']:
  x,y,w,h=z['bbox'];assert x+w<=1.000001 and y+h<=1.000001
assert X['governance']['v2_9_generation_allowed'] is False
assert 'no_paid_generation_without' in X['governance']
with (DIR/'j4_composition_acceptance.csv').open() as f:
 checks=list(csv.DictReader(f))
assert len(checks)>=40 and all(r['status']=='NOT_RUN_NO_RENDER' and not r['reviewer'] for r in checks)
with (DIR/'j4_asset_lock_registry.csv').open() as f:
 assets=list(csv.DictReader(f))
assert len(assets)>=10 and all(r['status']=='DESIGN_ONLY' for r in assets)
print(f'PASS: 25 shots / 90000 ms unchanged; 4 boards; {len(checks)} unscored acceptance checks; {len(assets)} asset locks; no generation approval')
'''
(OUT/'validate_v2_9.py').write_text(validator)

# Include baseline source files by copy for portable validator; change validator base path accordingly.
(BASE/'j4_shots_v2_8.json').replace if False else None
(OUT/'baseline_j4_shots_v2_8.json').write_bytes(shots_src.read_bytes())
(OUT/'baseline_j4_sound_ir_v2_8.json').write_bytes(sound_src.read_bytes())
validator=validator.replace("base=Path('/mnt/data/j4_museum_v2_8')",'base=DIR').replace("base/'j4_shots_v2_8.json'","base/'baseline_j4_shots_v2_8.json'").replace("base/'j4_sound_ir_v2_8.json'","base/'baseline_j4_sound_ir_v2_8.json'")
(OUT/'validate_v2_9.py').write_text(validator)

# Manifest
files=[]
for p in sorted(OUT.iterdir()):
 if p.name!='j4_manifest_v2_9.json':files.append({'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
(OUT/'j4_manifest_v2_9.json').write_text(json.dumps({'status':meta['status'],'media_generated':False,'generation_allowed':False,'files':files},ensure_ascii=False,indent=2)+'\n')

print('Created v2.9 files:')
for p in sorted(OUT.iterdir()):print(p.name,p.stat().st_size)
