from pathlib import Path
from itertools import permutations
from collections import Counter
import csv, hashlib, json, random, textwrap, zipfile

BASE=Path('/mnt/data'); ROOT=BASE/'j4_museum_v3_6'; ROOT.mkdir(exist_ok=True)
PARENT=BASE/'j4_museum_v3_5'/'j4_g2a_previs_lock_v3_5.json'
SRC=json.loads(PARENT.read_text()); assert len(SRC['arcs'])==3

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def put(path,s): (ROOT/path).write_text(textwrap.dedent(s).lstrip(),encoding='utf-8')
def put_json(path,obj): (ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvout(path,cols,rows):
 with open(ROOT/path,'w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)

# This is a candidate protocol, not a registered human study or released media.
ARCS={a['id']:a for a in SRC['arcs']}
CONDS={
 'G2A_COAT':{
  'hypothesis':'S21 主線外套 A 的左下襬修補可見時，比修補不可見時，觀眾更能以具體證據改判 S10 的檔案外套 B 並非同一實體。',
  'target_shot':'S21','target_roi':[.425,.3028,.054,.0336],
  'condition_main':'S21 的外套 A 左下襬在最後 21 格清楚可見修補。',
  'condition_control':'從同一個 S21 base plate 生成負對照，只在修補區域隱藏／局部修復紋理。若採實體遮擋，須在導演審核中另記干擾變項。',
  'target_frames':[99,120],
  'specific_cue':'左下襬修補有／無，不是外套顏色或人物臉孔',
  'human_question_before':'你看見什麼？這個物件讓你想到什麼？',
  'human_question_after':'重看前一鏡後，你的理解有改變嗎？請只用畫面中可見的細節解釋。',
  'risk':'S21 修補佔全 9:16 畫面約 0.1814%；在 360px 寬螢幕約 19px 寬。21 格僅 0.7s。手機可讀性高度存疑。',
  'roi_rationale':'v3.5 S21 chair-coat bbox [0.38,0.09,0.30,0.28] 乘相對 repair [0.15,0.76,0.18,0.12] 的計算結果。',
  'control_compatibility':'改為同底片局部修補陰性版本是 v3.6 建議，與 v3.5 既定「可信的遮擋」不同，須導演批准後才可採用。'
 },
 'G2A_PAPER':{
  'hypothesis':'S22 空紙屋重複 S11 屋頂偏斜摺線與不規則窄窗時，比不相容的折線與窗形更容易讓觀眾注意到兩鏡共享製作語法。',
  'target_shot':'S22','target_roi':[.70,.46,.18,.19],
  'condition_main':'S22 紙屋使用同 S11 屋頂偏斜摺線與不規則窄窗；實體不同。',
  'condition_control':'同一 S22 base plate 只替換紙屋局部屋頂摺線與窗形，保留空屋、紙材、位置、色調、手部動作與景深。',
  'target_frames':[0,90],
  'specific_cue':'非相同實體；相同的屋頂摺線加狹窗製作規則',
  'human_question_before':'這個場景裡有哪些物件？哪個物件令你注意？',
  'human_question_after':'重看前一鏡後，你認為兩個場景有關聯嗎？若有，是什麼可見線索？',
  'risk':'若在 S11 紙屋太小，受試者只會因「都是紙」而猜測連結；必須要求具體窗形或屋頂摺法。',
  'roi_rationale':'v3.5 S22 house_bbox [0.70,0.46,0.18,0.19]；最大 ROI 包住可替換的紙屋局部。',
  'control_compatibility':'沿用 v3.5，同時要求局部修改不改紙世界與人物。'
 },
 'G2A_AUTHORITY':{
  'hypothesis':'S19 三主燈位對應 S18 三光形 x≈[0.32,0.52,0.70] 時，比 S19 重新排列光位更容易讓觀眾辨識兩鏡有特定的空間對應。',
  'target_shot':'S19','target_roi':[.14,.49,.76,.22],
  'condition_main':'S19 保留五張空椅，三個核心光位順序和間距約 0.32/0.52/0.70。',
  'condition_control':'S19 仍有五張椅子、三個相同能量的光池，但光位中心改約 0.24/0.55/0.84；不改城市背景與音軌。',
  'target_frames':[21,120],
  'specific_cue':'三個光位的不等間距及排列，而非僅僅「三」這個數目',
  'human_question_before':'短暫畫面中，你注意到幾個主要元素？它們的關係是什麼？',
  'human_question_after':'重看前一鏡後，你是否注意到兩個場景的排列關係？請描述具體位置。',
  'risk':'移動 S19 光池會改變視覺重心與局部亮度，無法只用 ROI 一致性證明控制成功；需要空間 salience 盲審。',
  'roi_rationale':'三主要燈位所在設計區域的候選大範圍 ROI，待取得真實影格後重新標註。',
  'control_compatibility':'沿用 v3.5 位置，但要求保持席位數、總亮度與虛構新聞背景一致；移動座位／燈位的副作用要獨立記錄。'
 }
}
arc_specs=[];stimuli=[]; audits=[]; qrows=[]
for i,a in enumerate(SRC['arcs']):
 spec=CONDS[a['id']]; id=a['id']; source_info=[{'artist':z['artist'],'work':z['work'],'url':z['url'],'do_not_copy':z['not_to_copy']} for z in a['source_art']]
 d={'id':id,'A':a['a'],'B':a['b'],'source_art':source_info,'hypothesis':spec['hypothesis'],'manipulation':{'target_shot':spec['target_shot'],'target_roi_norm_xywh':spec['target_roi'],'frame_range_half_open':spec['target_frames'],'main':spec['condition_main'],'control':spec['condition_control'],'risk':spec['risk'],'compatibility_note':spec['control_compatibility'],'roi_rationale':spec['roi_rationale']},'first_read':a['first_read'],'second_read':a['second_read'],'cue':spec['specific_cue'],'runtime':a['timing'],'research_status':'NOT_RUN','director_status':'NOT_SIGNED','media_status':'MISSING','rights_status':'NOT_RUN'}
 arc_specs.append(d)
 for role,shot,variant in [('A',a['a'],'shared'),('B',a['b'],'main'),('B',a['b'],'control')]:
  dur=a['timing'][shot]['duration_ms']; frames=round(dur*30/1000)
  stimuli.append({'arc_id':id,'stimulus_id':f'{id}_{role}_{variant}','role':role,'shot':shot,'condition':variant,'duration_ms':dur,'frames_expected':frames,'fps_expected':30,'width_expected':1080,'height_expected':1920,'audio_policy':'MUTED_VISUAL_PILOT','media_relative_path':f'media/{id}_{role}_{variant}.mp4','sha256_actual':'','license_evidence_path':'','status':'MISSING_MEDIA'})
 for c,expect in [('main','TARGET_PRESENT'),('control','TARGET_ABLATED')]:
  for field,desc in [('duration_fps_resolution','Same 30 fps, 9:16, exact shot frame count'),('A_bytes','Shared A is identical across both conditions'),('B_outside_ROI','B variants identical outside planned manipulation ROI (within codec tolerance)'),('B_exposure_color','Consistent exposure/white balance, no global color change'),('motion_camera','Camera/framing/actor movement/temporal event timing unchanged'),('salience','No unplanned increase/decrease in noticeability caused by manipulation'),('audio','Visual-only pilot: both conditions muted'),('source_rights','Source material, generation/plate rights reviewed'),('originality','Artwork methods used without reproducing protected expression')]:
   audits.append({'arc_id':id,'condition':c,'metric':field,'expected':desc,'target_state':expect,'status':'NOT_RUN','evidence_path':'','reviewer':'','notes':''})
 qrows += [{'arc_id':id,'stage':'first_read','question_zh':spec['human_question_before'],'instruction':'Answer without earlier context, first exposure to shot A only'}, {'arc_id':id,'stage':'after_reveal','question_zh':spec['human_question_after'],'instruction':'After B, rewatch identical A; no design cue shown'}]

# Candidate prereg design and user data privacy.
(ROOT/'baseline_v3_5_previs_lock.json').write_bytes(PARENT.read_bytes())
PRE={
 'project':SRC['project'],'version':'v3.6','phase':'G2A_STIMULUS_REVEAL_PREREGISTRATION_DRAFT',
 'status':'CANDIDATE_NOT_SIGNED_NO_MEDIA_NO_HUMAN_RESULTS',
 'source':{'path':'baseline_v3_5_previs_lock.json','original_session_path':str(PARENT),'sha256':sha(PARENT),'version':'v3.5','parent_hash_guard':'READ_ONLY'},
 'film':SRC['film'],
 'design':{
  'unit':'viewer_arc_trial','conditions':['main','control'],'assignment':'between-subject per arc; one condition per viewer for the same arc; same arm assigned throughout pilot to avoid disclosure',
  'A_shared_identical_bytes':True,'B_main_vs_control':'only registered anchor manipulation','display':'9:16 vertical, source duration, identical device settings per participant; do not crop',
  'media_pilot':'VISUAL_ONLY_MUTED','full_sound_future':'separate audiovisual study with identical soundtrack per condition, after original score cleared',
  'protocol':['present A at source duration','free first read and confidence 1–5','present B at source duration','present byte-identical A again','free second read and evidence with confidence 1–5'],
  'blindness':'no cue description or art reference before response; two blinded raters independent',
  'assignment_slots':36,'orders':list(map(list,permutations(['G2A_COAT','G2A_PAPER','G2A_AUTHORITY']))),
  'pilot':{'n':8,'purpose':'UI/stimulus feasibility and qualitative failure detection only','limitation':'8 viewers cannot evenly cover two arms × six order permutations'},
  'feasibility_target':{'n':36,'note':'18 per arm / 3 per each of 6 permutations; illustrative planning, not statistical power calculation'},
  'primary_outcome':'evidence-backed reinterpretation: anchor_evidence_score=2 and semantic_revision_score=2',
  'secondary_outcomes':['anchor_evidence_score','semantic_revision_score','readability','unfounded_claim','confidence_delta'],
  'scoring':{'anchor_evidence_score':[0,1,2],'semantic_revision_score':[0,1,2],'readability':[1,2,3,4,5],'unfounded_claim':[0,1],'confidence':[1,2,3,4,5]},
  'pilot_screening_thresholds':{'main_anchor_evidence_rate':0.70,'main_semantic_revision_rate':0.50,'effect_direction':'main > control; no claim of statistical significance','two_independent_raters':True,'control_comparison':'must be lower than main on evidence-backed reinterpretation; small samples interpreted only descriptively'},
  'noncompliance':'Missing media, rights, director signature, invalid control matching => block human test and keep NOT_RUN',
  'privacy':'Pseudonymous slots only; no names, voice recordings or sensitive traits; raw answers kept local by researcher; do not upload without authorization'
 },
 'arcs':arc_specs,
 'gates':{'G1_director_visual_review':'NOT_RUN','G2_rights_originality':'NOT_RUN','G2A_stimulus_qa':'BLOCKED_NO_MEDIA','G2A_blind_human_pilot':'NOT_RUN','G3_real_keyframe_qc':'NOT_RUN','Higgsfield_paid_generation':'BLOCKED','Neon_explicit_approval':'NOT_RUN','director_cost_posted_to_service_chat':'NOT_RUN','monthly_9000_point_headroom':'NOT_CHECKED'},
 'scope_guard':{'canonical_shot_ir_mutated':False,'sound_ir_mutated':False,'original_repo_mutated':False,'generated_images':0,'generated_videos':0,'results_recorded':0}
}
put_json('j4_g2a_preregistration_v3_6.json',PRE)
# Generate read-only assignment slots. Every 6 slots for each arm has one of each permutation.
orders=list(permutations(['G2A_COAT','G2A_PAPER','G2A_AUTHORITY']))
slots=[]
for arm in ['main','control']:
 for r in range(3):
  for j,order in enumerate(orders):
   slots.append({'slot_id':'SLOT_PENDING','condition':arm,'order_1':order[0],'order_2':order[1],'order_3':order[2],'allocation_status':'UNASSIGNED','participant_code':'','consent_checked':'NOT_RUN','result_status':'NOT_RUN'})
rng=random.Random(3606307);rng.shuffle(slots)
for idx,s in enumerate(slots,1):s['slot_id']=f'SLOT_{idx:03d}'
put_json('j4_assignment_plan_v3_6.json',{'seed':3606307,'status':'PLANNED_ONLY','slots':slots})

csvout('j4_stimulus_manifest_v3_6.csv',list(stimuli[0]),stimuli)
csvout('j4_confound_audit_v3_6.csv',list(audits[0]),audits)
csvout('j4_blind_questions_v3_6.csv',list(qrows[0]),qrows)
csvout('j4_allocation_slots_v3_6.csv',list(slots[0]),slots)
# deliberately empty result template
ratings=[]
for a in SRC['arcs']:
 for rater in ('R1','R2'):
  ratings.append({'slot_id':'','arc_id':a['id'],'arm_blinded':'MASKED','rater_id':rater,'first_read':'','second_read':'','anchor_evidence_score':'','semantic_revision_score':'','readability':'','unfounded_claim':'','confidence_first':'','confidence_second':'','evidence_location':'','rating_status':'NOT_RUN'})
csvout('j4_blind_rating_template_v3_6.csv',list(ratings[0]),ratings)

put('G2A_PREREGISTRATION_v3_6.md', '''
# J4 G2-A v3.6｜候選預註冊：刺激與揭示控制

**狀態：`CANDIDATE_NOT_SIGNED / NO_MEDIA / NO_HUMAN_RESULTS`**。這是事前固定設計，不是已向任何公共登錄機構完成正式 preregistration，也不是觀眾測試。

## 研究問題

三條物件回響鏈是否能在沒有字幕、藝術家提示或導演解釋的情況下，使觀眾在後續鏡頭出現後，用**可見的物理線索**重新理解此前場景？

| Arc | A 首看 | B 揭示 | 正例 vs 負對照的唯一預期差異 | 參考藝術方法 |
| --- | --- | --- | --- | --- |
| G2A_COAT | S10 3.5s | S21 4.0s | S21 外套 A 的左下襬修補清楚可見 vs 不可見 | Tim Noble × Sue Webster《Dirty White Trash (with Gulls)》；Michelangelo Pistoletto《Man with Yellow Pants》 |
| G2A_PAPER | S11 4.0s | S22 3.0s | S22 紙屋屋頂折線與窄窗和 S11 一致 vs 不一致 | Liliana Porter《Untitled (with Cube – tall)》；Thomas Demand《Office》 |
| G2A_AUTHORITY | S18 1.3s | S19 4.0s | 主要光位的相對位置對應 vs 不對應 | Jim Campbell《Exploded Views》；James Turrell《Afrum I (White)》 |

以上是方法對標，不複製原藝術裝置、可辨識構圖或錄音。

## 觀眾試驗程序

1. 每位觀眾只看同一 arc 的一種條件：`main` 或 `control`，避免同一人看到兩種 B 影格。
2. 播 A（原鏡長），不公布用途；自由描述第一印象，記錄把握度 1–5。
3. 播 B（原鏡長），不提示物件線索。
4. **再次播與第一輪位元組相同的 A**；自由描述是否改讀，以及畫面中的具體證據。
5. 兩位不知條件的評分者獨立給 `anchor_evidence_score` 與 `semantic_revision_score`（均為 0–2）。0 無／不成立、1 模糊、2 有具體可見依據。另記 readability 1–5、無依據事實聲稱 0/1。
6. 不合併 9:16 與 16:9 的資料。正式流程只納入有合法來源的實際鏡頭媒體，不接受 SVG 模擬圖當作有效心理刺激。

## 樣本設計

- 先用 **8 人 pilot** 發現可見性、問題引導及裝置失敗。這不是正式推論研究，不能覆蓋完整的 2 arm × 6 種排列。
- 36 個**尚未指派**的匿名 slot 只是平衡分配方案：每組 18 個、6 種順序各 3 個。不是招募完成，也不是統計 power 計算。
- 候選 pilot 門檻（事前固定）：正例的具體 anchor 比率 ≥70%；有依據的語義改讀 ≥50%；正例優於對照；同時要檢查兩位盲評者的分歧。小樣本只供質性診斷。

## 視覺負對照：必須嚴格匹配

- `A` 僅有一個原始媒體檔，兩條 arm 均重播同一檔案，使用 SHA-256 保證相同。
- `B_main` 與 `B_control` 使用相同鏡長、影格率、解像度、裁切、相機軌跡及動作節拍；只允許註冊的 target ROI 發生改變。
- 本 pilot **無聲音**。聲音與畫面共同作用的研究可另做第二階段，兩條 arm 必須共享同一原創音軌。
- 需做非 ROI 區域逐影格亮度／像素差分與人工顯著性審核。即使差分低，也不能替代藝術／版權審查。

## 三組容易誤判的地方

**外套：** v3.5 設計的修補區面積約 0.1814% 全影格，360px 寬手機約 19px。最後 21 格只 0.7 秒。**不能因靜態截圖看得見，就宣稱正常播放可辨識。** 優先 G1 導演改動構圖／景深；不要直接增加字幕。

**紙屋：** 必須區分「同一件實體」與「相同製造語法」。S11 和 S22 不是同一個紙屋。觀眾只回答「兩個都是紙做的」不計為滿分 anchor。

**權力光形：** S18 光位置 x≈[0.32,0.52,0.70]，S19 對應三個主座；control 位置約 [0.24,0.55,0.84]。移動光位可能改變整體視覺重心。除了相對配置，必須盲審光池能量／視覺顯著性是否接近；不能把被燈光吸引誤認成記憶改讀。

## 嚴格閘口

`DESIGN DRAFT → DIRECTOR SIGN-OFF → RIGHTS CHECK → REAL MEDIA → AUTOMATED QA + HUMAN CONFOUND AUDIT → READY_FOR_PILOT → ACTUAL PILOT → REVIEW`。

缺媒體或沒有 Director／權利簽核時，`READY_FOR_PILOT` 必須保持 BLOCKED。所有 Higgsfield 點數生成還要額外通過 Neon 明確同意、Director 在指定聊天室發送估點、檢查 9,000 點月上限剩餘額度。

全片 25 鏡、90 秒、30 fps；S10 38.600s 局部殘響截止，S18 63.700s 六聲部全局中斷，皆不在本輪更動。
''')
put('README_v3_6.md','''
# J4 v3.6 — Pre-registered Stimulus & Reveal Gate（候選）

**DESIGN ONLY · NOT_SIGNED · NO REAL MEDIA · HUMAN TEST NOT_RUN · HIGGSFIELD BLOCKED**

父文件唯讀副本：`baseline_v3_5_previs_lock.json`（來源 `../j4_museum_v3_5/j4_g2a_previs_lock_v3_5.json`），SHA256 見 `j4_g2a_preregistration_v3_6.json`。父檔維持唯讀。

| 產物 | 作用 |
| --- | --- |
| `G2A_PREREGISTRATION_v3_6.md` | 正反條件、觀察假說、盲測問題、招募與記錄規則 |
| `j4_g2a_preregistration_v3_6.json` | 可機械核對的 3 arcs／6 條件事前規格 |
| `j4_stimulus_manifest_v3_6.csv` | 9 個預期獨立媒體槽（每 arc A 共用 1、B 正反各 1） |
| `j4_confound_audit_v3_6.csv` | 54 項雙條件混淆因子待審核 |
| `j4_allocation_slots_v3_6.csv` | 36 個尚未指派的平衡試驗位置，不代表受試者 |
| `j4_blind_questions_v3_6.csv` | 3 arcs 的首次觀看／揭示後中性問題 |
| `j4_blind_rating_template_v3_6.csv` | 雙人盲評模板，無任何已蒐集分數 |
| `j4_stimulus_media_qa_v3_6.py` | 媒體不存在則 BLOCKED；存在後檢查 fps、frames、尺寸與 ROI 外差異 |
| `j4_static_validate_v3_6.py` | 資料完整性與 parent hash 驗證 |
| `j4_g2a_prereg_board_v3_6.html` | 無媒體實驗設計審核，不是心理實驗結果 |
| `TEST_REPORT_v3_6.md` | 本次確實執行的測試和未執行項目 |

執行：

```bash
python j4_static_validate_v3_6.py
python j4_stimulus_media_qa_v3_6.py
```

沒有素材時第二個命令應印出 `BLOCKED_NO_REAL_MEDIA` 並以 exit code 2 結束，這是預期的 fail-closed 行為。

不對外聲稱預註冊已被正式機構接收，或實驗有真實測量結果。
''')
put('j4_static_validate_v3_6.py',r'''
#!/usr/bin/env python3
"""Static preflight for J4 v3.6. Never writes canonical project sources."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,math
P=Path(__file__).resolve().parent

def load_json(f):return json.loads((P/f).read_text(encoding='utf-8'))
def rows(f):
 with (P/f).open(newline='',encoding='utf-8-sig') as h:return list(csv.DictReader(h))
def hashf(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def req(b,msg):
 if not b: raise AssertionError(msg)

def run():
 x=load_json('j4_g2a_preregistration_v3_6.json'); parent=P/x['source']['path']
 req(parent.exists(),'parent missing')
 req(hashf(parent)==x['source']['sha256'],'parent modified')
 req(x['film']['shots']==25 and x['film']['duration_ms']==90000 and x['film']['frames']==2700,'film changed')
 req(x['film']['s18_global_cycle_cut_ms']==63700,'S18 changed')
 req(len(x['arcs'])==3,'wrong arcs')
 manifest=rows('j4_stimulus_manifest_v3_6.csv')
 req(len(manifest)==9,'expected 9 unique stimulus slots')
 qs=rows('j4_blind_questions_v3_6.csv');req(len(qs)==6,'expected six neutral questions')
 audit=rows('j4_confound_audit_v3_6.csv');req(len(audit)==54,'expected 54 pending confound rows')
 req(all(z['status']=='NOT_RUN' and not z['evidence_path'] for z in audit),'audit prematurely marked complete')
 slots=rows('j4_allocation_slots_v3_6.csv');req(len(slots)==36,'36 planned slots')
 groups=Counter(z['condition'] for z in slots);req(groups=={'main':18,'control':18},'unbalanced arm slots')
 counts=Counter((z['condition'],z['order_1'],z['order_2'],z['order_3']) for z in slots)
 req(len(counts)==12 and set(counts.values())=={3},'order permutations imbalance')
 req(all(z['allocation_status']=='UNASSIGNED' and not z['participant_code'] for z in slots),'not anonymous unassigned slots')
 for a in x['arcs']:
  id=a['id']; aa=[z for z in manifest if z['arc_id']==id]
  req(len(aa)==3 and {(z['role'],z['condition']) for z in aa}=={('A','shared'),('B','main'),('B','control')},'bad stimulus slots '+id)
  bmain=next(z for z in aa if z['condition']=='main');bctrl=next(z for z in aa if z['condition']=='control')
  req(bmain['frames_expected']==bctrl['frames_expected'] and bmain['duration_ms']==bctrl['duration_ms'], 'B timing mismatch '+id)
  req(all(z['status']=='MISSING_MEDIA' and not z['sha256_actual'] for z in aa),'unverified media '+id)
  fx=a['manipulation']['frame_range_half_open'];req(int(fx[1])<=int(bmain['frames_expected']),'ROI frame range overflow '+id)
  rr=a['manipulation']['target_roi_norm_xywh'];req(len(rr)==4 and 0<=rr[0]<=1 and 0<=rr[1]<=1 and rr[2]>0 and rr[3]>0 and rr[0]+rr[2]<=1 and rr[1]+rr[3]<=1,'bad ROI '+id)
  req(len(a['source_art'])==2 and all(z['url'].startswith('https://') for z in a['source_art']),'source refs missing '+id)
 req(x['gates']['Higgsfield_paid_generation']=='BLOCKED' and x['scope_guard']['results_recorded']==0,'permission/result mismatch')
 print('PASS_STATIC: 25 shots/90s/2700 frames; 3 arcs; 9 media slots missing; 54 audit checks NOT_RUN; 36 unassigned balanced slots; generation BLOCKED')
if __name__=='__main__':run()
''')

put('j4_stimulus_media_qa_v3_6.py',r'''
#!/usr/bin/env python3
"""Fail-closed media preflight. Tests don't establish copyright or psychological validity.
Run only on locally cleared stimulus files. No generation or network requests.
"""
from pathlib import Path
import csv,hashlib,json,subprocess,sys,math
P=Path(__file__).resolve().parent

def hashf(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def ffprobe(p):
 r=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,avg_frame_rate,nb_frames,duration','-of','json',str(p)],capture_output=True,text=True)
 if r.returncode:raise ValueError(r.stderr[:400])
 s=json.loads(r.stdout)['streams'][0];n,d=(int(v) for v in s['avg_frame_rate'].split('/'))
 s['fps']=n/d
 return s

def check_pair(main,ctrl,arc):
 import cv2,numpy as np
 m=cv2.VideoCapture(str(main));c=cv2.VideoCapture(str(ctrl));
 x,y,w,h=arc['manipulation']['target_roi_norm_xywh']; start,end=arc['manipulation']['frame_range_half_open']
 n=0; outside_delta=[]; target_delta=[];luma_deltas=[]
 while True:
  ok1,a=m.read();ok2,b=c.read()
  if not ok1 and not ok2:break
  if ok1!=ok2:raise ValueError('B frames mismatch')
  H,W=a.shape[:2];mask=np.ones((H,W),dtype=bool)
  # registered target mask, with narrow 2% buffer for compression falloff
  pad=.02
  x1=max(0,int((x-pad)*W));y1=max(0,int((y-pad)*H));x2=min(W,int((x+w+pad)*W));y2=min(H,int((y+h+pad)*H))
  if start<=n<end: mask[y1:y2,x1:x2]=False
  delta=np.abs(a.astype(np.float32)-b.astype(np.float32)).mean(axis=2)/255.0
  outside_delta.append(float(delta[mask].mean()))
  target_delta.append(float(delta[~mask].mean()) if (~mask).any() else 0.0)
  # comparable exposure outside target region; whole-frame brightness may legitimately differ in authority experiment
  luma_deltas.append(float(abs(a[mask].mean()-b[mask].mean())/255))
  n+=1
 m.release();c.release()
 if n==0:raise ValueError('no video frames')
 # Tolerances are candidate engineering guards; must be manually confirmed for codec type.
 return {'frames_compared':n,'mean_normalized_difference_outside_mask':sum(outside_delta)/n,'mean_normalized_difference_within_target':sum(target_delta)/n,'mean_luma_shift_outside_mask':sum(luma_deltas)/n,
 'machine_guard_outside_roi': 'PASS' if sum(outside_delta)/n<=.015 else 'NEEDS_REVIEW',
 'machine_guard_luma':'PASS' if sum(luma_deltas)/n<=.015 else 'NEEDS_REVIEW',
 'warning':'PASS is not human salience or artistic approval; moving light pools may fail confound review despite low pixel difference.'}

def main():
 with (P/'j4_stimulus_manifest_v3_6.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 prereg=json.loads((P/'j4_g2a_preregistration_v3_6.json').read_text())
 paths={z['stimulus_id']:P/z['media_relative_path'] for z in rows}
 missing=[str(p.relative_to(P)) for p in paths.values() if not p.is_file()]
 if missing:
  print('BLOCKED_NO_REAL_MEDIA: missing',len(missing),'of',len(paths),'expected clips. No video quality conclusion.')
  for p in missing: print(' -',p)
  return 2
 checks=[]
 for row in rows:
  p=paths[row['stimulus_id']];s=ffprobe(p);valid=(s['width']==int(row['width_expected']) and s['height']==int(row['height_expected']) and abs(s['fps']-float(row['fps_expected']))<.02)
  vframes=s.get('nb_frames');n=int(vframes) if vframes not in ('N/A',None) else None
  if n is None:
   import cv2
   cap=cv2.VideoCapture(str(p)); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.release()
  valid=valid and (n==int(row['frames_expected']))
  streamcheck=subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',str(p)],capture_output=True,text=True)
  silent=(streamcheck.returncode==0 and not streamcheck.stdout.strip())
  valid=valid and silent
  # picture-only pilot requires no audible guidance; videos may contain audio tracks but should be stripped before use
  checks.append({'stimulus':row['stimulus_id'],'path':row['media_relative_path'],'hash':hashf(p),'resolution_fps_frames_no_audio':'PASS' if valid else 'FAIL','frames_observed':n,'frames_expected':int(row['frames_expected'])})
 for arc in prereg['arcs']:
  i=arc['id'];checks.append({'arc':i,'B_pixel_control_comparison':check_pair(paths[f'{i}_B_main'],paths[f'{i}_B_control'],arc)})
 print(json.dumps({'status':'MEDIA_PREFLIGHT_COMPLETED_NOT_HUMAN_SIGNOFF','checks':checks},ensure_ascii=False,indent=2))
 if any(x.get('resolution_fps_frames_no_audio')=='FAIL' for x in checks):return 3
 if any('B_pixel_control_comparison' in x and (x['B_pixel_control_comparison']['machine_guard_outside_roi']!='PASS' or x['B_pixel_control_comparison']['machine_guard_luma']!='PASS') for x in checks):return 3
 return 0
if __name__=='__main__':sys.exit(main())
''')
board_js_data=json.dumps({'arcs':arc_specs,'film':SRC['film'],'gates':PRE['gates'],'stimuli':stimuli,'audit_count':len(audits),'slot_count':len(slots),'source_sha':sha(PARENT)},ensure_ascii=False).replace('</','<\\/')
html='''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>J4 v3.6｜刺激控制與揭示審核</title>
<style>
:root{color-scheme:dark;font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC",system-ui,sans-serif;background:#0e1212;color:#e6e8e4}
*{box-sizing:border-box}body{margin:0}header{background:#171d1b;border-bottom:1px solid #35423c;padding:28px 5vw}h1{font-size:clamp(22px,3vw,36px);margin:5px 0}h2{font-size:19px;margin:0 0 12px}h3{font-size:16px;margin:18px 0 8px}p,li{line-height:1.7}.muted{color:#a6b4ae}.small{font-size:13px}main{max-width:1300px;margin:auto;padding:24px 20px 70px}.status{border:1px solid #4b574e;border-radius:999px;padding:4px 10px;font-size:12px;color:#d6cdb1;display:inline-block}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:20px 0}.stat{border:1px solid #35443d;border-radius:12px;padding:14px;background:#18201d}.stat b{font-size:25px;display:block;margin:4px 0}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}.tabs button,button,select{border:1px solid #526157;background:#252f29;border-radius:9px;padding:10px 13px;color:#f2f4eb;cursor:pointer;font-size:14px}button.sel{background:#bdcdbb;color:#18231e;border-color:#bdcdbb}button:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid #eedbae;outline-offset:2px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.panel{border:1px solid #344039;background:#171e1b;border-radius:14px;padding:18px}.card{border:1px solid #394940;background:#1b2420;border-radius:12px;padding:13px;margin-bottom:12px}.sample{background:#0c1110;aspect-ratio:9/12;max-height:440px;display:flex;align-items:center;justify-content:center;overflow:hidden;border:1px solid #48564d;border-radius:10px}.sample svg{height:100%;max-width:100%}.tag{font-size:11px;letter-spacing:.07em;color:#c7d3b5}.warn{border-left:3px solid #c6ae77;padding:8px 12px;background:#2a2921}.ok{color:#bbd5b6}a{color:#b7d7c8;overflow-wrap:anywhere}.rows{display:grid;grid-template-columns:1fr 1fr;gap:10px}.rows label{font-size:13px;color:#b8c5b9}.row-label{font-weight:600;margin:9px 0 6px}textarea{width:100%;min-height:90px;background:#0e1411;color:#e5e9e3;border:1px solid #56675a;border-radius:9px;padding:12px;font:inherit}.foot{font-size:12px;color:#a4b3a8;line-height:1.7;margin-top:14px}.ref{border-bottom:1px solid #324137;padding:8px 0}.bar{height:7px;background:#28312b;border-radius:99px;overflow:hidden}.bar>div{height:100%;width:0;background:#a4c8b0}@media(max-width:760px){.grid,.rows{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}main{padding:18px 12px}.sample{max-height:330px}}
</style></head><body>
<header><div class="muted small">J4 / ASYNC: SUCCESSION · G2-A · v3.6</div><h1>物件狀態／實驗控制審核</h1><p class="muted">這是導演用實驗設計板。示意圖是原創 SVG，<strong>不是正式視覺刺激、沒有受試者結果，也不是影像生成授權。</strong></p><span class="status">CANDIDATE · NO MEDIA · NOT SIGNED</span></header>
<main>
<div class="stats"><div class="stat"><small>回響鏈</small><b>3</b><span class="muted small">H1 / H2 / H3</span></div><div class="stat"><small>待製作片段</small><b>9 / 9</b><span class="muted small">全部缺少實際媒體</span></div><div class="stat"><small>混淆因子核對</small><b>0 / 54</b><span class="muted small">全部 NOT_RUN</span></div><div class="stat"><small>人工試驗</small><b>0</b><span class="muted small">不宣稱效果已成立</span></div></div>
<div class="tabs" id="tabs"></div>
<div class="grid"><section class="panel"><h2 id="arc_title"></h2><p id="hypothesis"></p><div class="rows"><div class="card"><div class="row-label" id="a_title"></div><div class="sample" id="a_visual"></div><p class="small muted" id="a_desc"></p></div><div class="card"><div class="row-label" id="b_title"></div><div class="sample" id="b_visual"></div><p class="small muted" id="b_desc"></p></div></div><p class="foot">僅示意物件和線索位置，不足以判定美學、光學品質或正常觀看可讀性。</p></section>
<section class="panel"><div class="rows"><div><label for="condition">對照條件</label><select id="condition"><option value="main">正例：線索存在</option><option value="control">負對照：只替換線索</option></select></div><div><label for="device">線索的螢幕大小預估</label><select id="device"><option value="360">360px 寬手機</option><option value="1080">1080px 影片</option></select></div></div><h3>唯一允許的變更</h3><div id="manip" class="card"></div><h3>必須控制的混淆</h3><p class="warn" id="risk"></p><h3>線索大小</h3><div class="card" id="roi"></div><h3>當代藝術方法來源</h3><div id="artrefs"></div><h3>導演審核草稿（不等於簽核）</h3><textarea id="notes" placeholder="記錄需要修正的構圖、相位、光線或 IP 問題"></textarea><p><button id="export">匯出設計審核草稿 JSON</button></p></section></div>
<h3>試驗前必要閘口</h3><div class="panel"><p>G1 人工構圖審核：<b>NOT_RUN</b>　／　G2 權利審核：<b>NOT_RUN</b>　／　G2-A 真實媒體：<b>MISSING</b>　／　Higgsfield：<b>BLOCKED</b></p><div class="bar"><div></div></div><p class="foot">受試者只能看到經授權且經過配對檢查的實際片段，不能看到此審核頁、藝術家來源或導演預期答案。所有 25 鏡與 90 秒時碼保持原樣。來源 SHA：<code id="sha"></code></p></div>
</main>
<script>
const DATA=__EMBEDDED_DATA__;
const Q=id=>document.getElementById(id);
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
let active=DATA.arcs[0].id;let notes={};
function renderSvg(arc,shot,condition){
 const id=arc.id;const C='#d9d7c8',A='#ba9b74',F='#9baaa2';let g=[];
 const line=(x,y,x2,y2,c='#9ca9a0',w=2)=>`<line x1="${x}" y1="${y}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}"/>`;
 const rect=(x,y,w,h,c='#343e38')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}"/>`;
 g.push(rect(0,0,270,420,'#111714'));
 if(id==='G2A_COAT'){
  g.push(rect(25,60,220,300,'#25332d'));
  if(shot==='S10'){
   g.push('<path d="M127 93 L104 112 L84 135 L73 199 L96 209 L108 184 L108 278 L174 278 L174 184 L182 209 L205 199 L196 135 L171 113 L150 93 Z" fill="#69756e"/>');
   for(let x=40;x<246;x+=24)g.push(line(x,70,x,346,'#74847a',1));
   for(let y=70;y<352;y+=26)g.push(line(36,y,245,y,'#718278',1));
  }else{
   g.push('<path d="M123 71 L99 95 L83 135 L95 226 L172 226 L184 135 L161 94 L148 71 Z" fill="#758076"/>');
   g.push(rect(30,268,210,20,'#353f3a'),line(42,280,121,278,C,11),line(147,280,228,278,'#a6aca7',11));
   g.push('<circle cx="139" cy="280" r="9" stroke="#d6b57c" fill="none" stroke-width="4"/>');
   if(condition==='main')g.push('<rect x="110" y="201" width="18" height="11" fill="#d4b77e" stroke="#f9e6b6" stroke-width="1"/>');
  }
 }
 if(id==='G2A_PAPER'){
  g.push(rect(18,320,235,17,'#47534c'));
  if(shot==='S11'){g.push(rect(20,50,230,215,'#2c3e37'));
   for(let i=0;i<4;i++){let x=40+i*51;g.push(line(x,110,x+20,130,'#c6cab6',6));}
   g.push('<path d="M166 291 L188 273 L211 291 L211 313 L166 313 Z" fill="#ddd8ba"/>');g.push(rect(191,296,5,10,A));
  }else{
   g.push('<path d="M25 320 L66 259 L109 310 L159 243 L205 312 L247 271 L250 320 Z" fill="#d3cfbb" stroke="#a7a08d"/>');
   g.push('<path d="M70 284 L105 269 L128 295" fill="none" stroke="#9f8d6e" stroke-width="6"/>');
   if(condition==='main'){g.push('<path d="M179 231 L196 211 L214 223" fill="none" stroke="#bba98d" stroke-width="4"/>');g.push(rect(182,224,32,31,'#ece6cb'),rect(197,234,5,11,A));}
   else{g.push('<path d="M179 224 L198 204 L214 224" fill="none" stroke="#bba98d" stroke-width="4"/>');g.push(rect(182,224,32,31,'#ece6cb'),'<path d="M187 232 L201 239 L187 246 Z" fill="#ba9b74"/>');}
   g.push('<circle cx="66" cy="180" r="18" fill="#a4aaa0"/>','<path d="M48 197 L88 198 L113 280 L30 287 Z" fill="#727a71"/>');
  }
 }
 if(id==='G2A_AUTHORITY'){
  if(shot==='S18'){
   [0.32,0.52,0.70].forEach((x,i)=>{g.push(`<rect x="${Math.round(270*x-10)}" y="${113+i*16}" width="20" height="118" rx="8" fill="${i===0?'#c0a580':i===1?'#c6c9b8':'#a9b7b5'}" opacity=".34"/>`)});
  }else{
   g.push(rect(12,55,246,188,'#273f45'));
   [37,72,111,152,188,227].forEach((x,i)=>g.push(rect(x,149-(i%3)*20,24,102+(i%3)*20,'#517078')));
   g.push('<ellipse cx="135" cy="300" rx="110" ry="37" fill="#4a5a57" stroke="#adbab0" stroke-width="2"/>');
   const xx=condition==='main'?[.32,.52,.70]:[.24,.55,.84];
   xx.forEach(x=>{const px=x*270;g.push(`<ellipse cx="${px}" cy="260" rx="25" ry="13" fill="#d8c7a0" opacity=".40"/>`);g.push(`<rect x="${px-13}" y="256" width="26" height="24" rx="8" fill="#a4b1a7"/>`)});
   [25,245].forEach(px=>g.push(`<rect x="${px-11}" y="350" width="23" height="20" rx="6" fill="#4d5a52"/>`));
  }
 }
 return `<svg viewBox="0 0 270 420" role="img" aria-label="J4 ${shot} 原創線框示意，非正式媒體" xmlns="http://www.w3.org/2000/svg">${g.join('')}</svg>`;
}
function render(){
 const arc=DATA.arcs.find(a=>a.id===active),cond=Q('condition').value,sz=+Q('device').value;
 Q('tabs').innerHTML=DATA.arcs.map(a=>`<button class="${active===a.id?'sel':''}" data-id="${esc(a.id)}">${esc(a.A)} → ${esc(a.B)}</button>`).join('');
 Q('tabs').querySelectorAll('button').forEach(b=>b.onclick=()=>{notes[active]=Q('notes').value;active=b.dataset.id;Q('notes').value=notes[active]||'';render()});
 Q('arc_title').textContent=arc.id+'｜'+arc.A+' → '+arc.B;
 Q('hypothesis').textContent=arc.hypothesis;
 Q('a_title').textContent='A · '+arc.A+'（首次觀看，所有條件共用）';
 Q('b_title').textContent='B · '+arc.B+'（'+(cond==='main'?'正例':'負對照')+'）';
 Q('a_visual').innerHTML=renderSvg(arc,arc.A,cond);
 Q('b_visual').innerHTML=renderSvg(arc,arc.B,cond);
 Q('a_desc').textContent=arc.first_read;
 Q('b_desc').textContent=arc.second_read;
 Q('manip').textContent=arc.manipulation[cond];
 Q('risk').textContent=arc.manipulation.risk;
 const [x,y,w,h]=arc.manipulation.target_roi_norm_xywh;
 Q('roi').innerHTML=`<b>目標區域：</b> [${[x,y,w,h].map(n=>n.toFixed(3)).join(', ')}]（9:16 畫面 normalized xywh）<p class="small muted">約 ${Math.round(w*sz)} × ${Math.round(h*sz*16/9)} px，面積 ${(w*h*100).toFixed(3)}% · 估算只依幾何，不代表真實可讀性。</p>`;
 Q('artrefs').innerHTML=arc.source_art.map(z=>`<div class="ref"><b>${esc(z.artist)}</b> · <a href="${esc(z.url)}" target="_blank" rel="noopener">${esc(z.work)}</a><div class="small muted">禁用：${esc(z.do_not_copy)}</div></div>`).join('');
 Q('sha').textContent=DATA.source_sha.slice(0,18)+'…';
}
Q('condition').onchange=render;Q('device').onchange=render;
Q('export').onclick=()=>{notes[active]=Q('notes').value;const out={version:'v3.6',status:'DIRECTOR_DRAFT_NOT_SIGNED',media:false,human_test:false,notes,source_sha256:DATA.source_sha};const blob=new Blob([JSON.stringify(out,null,2)],{type:'application/json'});const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='j4_v3_6_director_draft.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)};
render();
</script></body></html>'''.replace('__EMBEDDED_DATA__',board_js_data)
put('j4_g2a_prereg_board_v3_6.html',html)

# Reproducible tests report is appended after actual test execution.
if __name__=='__main__':
 print('Built v3.6 candidate files:',len(list(ROOT.iterdir())))
