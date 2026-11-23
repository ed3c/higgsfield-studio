from pathlib import Path
import json, csv, hashlib, zipfile, subprocess
from collections import Counter
root=Path('/mnt/data')
out=root/'j4_museum_v3_7'; out.mkdir(exist_ok=True)
shot_path=root/'j4_museum_v2_9/j4_shots_v2_9.json'
sound_path=root/'j4_museum_v2_8/j4_sound_ir_v2_8.json'
illusion_path=root/'j4_museum_v3_3/j4_illusion_ir_v3_3.json'
shots=json.loads(shot_path.read_text())['shots']
sound=json.loads(sound_path.read_text())
illusions={s['shot_id']:s for s in json.loads(illusion_path.read_text())['shots']}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
# V0: none; V1: nonsemantic human texture; V2: fragmented/partly masked; V3: meaning-bearing, clear or duplicated through visuals and subtitles
# 25 authored policies, not source-derived audio or an actual musical score
spec={
'S01':('V0','acousmatic','Start in digital silence; after 0.50 s introduce a quiet, phase-stable original sine. Market ambience J-cuts under the last 0.3 s.','The first sine becomes recognisable only after S18 and S25.','Janet Cardiff — The Forty Part Motet'),
'S02':('V1','acoustic ecology','Layer location-independent invented market chatter, bowls, frying, damp steps and air. Speech indistinct and socially present rather than informational.','Warm night-market air reappears as human life in S24, but its seven-second phase family does not restart after S18.','Rirkrit Tiravanija — untitled 1990 (pad thai)'),
'S03':('V0','material resonance','One isolated water droplet, optical-installation room decay and a single soft original pitch. Sound response trails the visible droplet; do not falsely claim natural seconds-long light delay.','Cold optical material returns with accumulated complexity at S17 and delayed composite at S23.','Ryuichi Sakamoto & Shiro Takatani — water state 1'),
'S04':('V0','source migration','A tiny electrically heated filament ticks and a fragile metal structure resonates. Let a partial pitched motif emerge without upward cinematic swell.','The exact wire-bird timbre returns softened, never identical, at S24.','Studio DRIFT — Fragile Future'),
'S05':('V0','tactile temporality','Ceramic-water contact and gloved friction remain intimate, non-loop-like and valuable; do not score the worker as a metronome.','Maintenance sound is recalled but ethically inverted in S22: meaningful care versus institutional futility.','Mierle Laderman Ukeles — Washing/Tracks/Maintenance: Inside'),
'S06':('V0','foreground-background reversal','Lamp paper, hand-off, small contacts in near field; climate-controlled lamp cooling hum in far field at an independent five-second phase.','The mechanical hum becomes artificial weather in S07.','Felix Gonzalez-Torres — “Untitled” (Placebo)'),
'S07':('V0','causal ambiguity','Dry wind and computing-cooling exhaust initially occupy the same texture, then diverge spatially. No epic desert or religious choir.','The sound continues as the air conditioning in S08, revealing institutional scale.','Olafur Eliasson — The weather project'),
'S08':('V0','social entrainment','Separate claps emerge from isolated acoustic alcoves and approach, but do not reach, a common grid. No applause sample from any event.','S14 echoes the social process without an original occasion for applause.','Tino Sehgal — This Situation'),
'S09':('V2','semantic masking','A fictional speaker starts a quiet statement; the DIY fan megaphone masks consonants but leaves vocal human presence. No mandatory plot claim should rely on the words.','The final horn-ring continues into S10 where its human source is gone.','Tania Bruguera — Tatlin’s Whisper #6'),
'S10':('V0','shadow/acousmatic residue','Close mesh door, cloth sway and an unnaturally truncated *local* pitched tail at global 38.600 s. The six phase families continue.','S21 actual key-hand-off reinterprets apparent archived founder identity; do not use a person-voice phantom that falsely identifies the coat.','Doris Salcedo — Atrabilious'),
'S11':('V0','mechanical pulse vs chance','Robotic actuators expose a five-second underlying period; a single condensate drop interrupts it. Paper-house detail has no sonic annotation.','S22 reveals paper fabrication as human effort; the mechanical sound is not evidence the miniature traveled.','Cao Fei — Whose Utopia'),
'S12':('V0','tension resonance','Cable and wood friction create a narrow, naturally decaying harmonic in an empty banquet room. Do not add an actual phone call.','Cable overtone crossfades to S13 imperfect piano-string harmonic.','Chiharu Shiota — Uncertain Journey'),
'S13':('V0','object de-tuning','A wet piano key yields mechanical friction, not a conventional note. Sea-air and a late inharmonic overtone enter the hall.','A silent piano followed by S14 applause reframes the meaning of cultural acclaim.','Ryuichi Sakamoto & Shiro Takatani — IS YOUR TIME'),
'S14':('V0','spatial dislocation','Original claps from distant nonuniform boxes; audible crowd is larger than visible cast. Reverb becomes more present while direct attacks recede.','Institutional claps of S08 return as self-perpetuating applause for an empty stage.','Janet Cardiff & George Bures Miller — The Murder of Crows'),
'S15':('V0','polytemporal material','Two different weaving gestures and organic fibres cycle separately, under the tail of applause. Do not force 7 and 13 to meet in four seconds.','Shuttles transform timbrally into two routes in S16.','Chiharu Shiota — The Key in the Hand'),
'S16':('V1','tempo contrast','Quiet human footfall and luggage wheels stand next to reliable small motors; waiting sounds are not "defective" machine rhythms. Wordless human presence only.','Different pathways enter as competing sound systems at S17.','Rafael Lozano-Hemmer — Border Tuner'),
'S17':('V1','asynchronous counterpoint','Dense but controlled six-phase ambience; retain independent start phases, spatial positions and decay. A human breath can be heard without a speech line.','Cut all six cyclical layers simultaneously at 63.700 s; sine remains.','Ryoji Ikeda — data-verse 1'),
'S18':('V0','forced silence','At 63.700 s stop all six phase families via tiny de-click envelopes; no impact, no ticking and no flash-synchronised hit. Keep one continuous sine.','Three faint forms receive their semantic explanation in S19; all other ambience is a sudden absence.','Carsten Nicolai — unidisplay'),
'S19':('V0','image-sound offset','Virtual skyline appears while a near silent pre-broadcast electric tone and sparse piano fail to align with projected motion. No anchor, speech, or news sting.','Three lit seats clarify the abstract positions in S18.','Hito Steyerl — Factory of the Sun'),
'S20':('V0','split acoustic archive','Dry paper, subtle glass vibration and different room positions. Two methods of recording remain incomplete; no prayer or documentary testimony.','Two archive hand-actions prepare the key transfer of S21.','Walid Raad — The Atlas Group'),
'S21':('V3_OPTIONAL','semantic hinge','Prefer wordless close brass-key contact. If a fictional one-line statement is retained, place it clearly in a protected pocket or show the full text in accessible captions; NEVER mask a unique plot fact.','A single key changes hands; dry sleeve/paper contact crosses into S22.','Felix Gonzalez-Torres — “Untitled” (Perfect Lovers)'),
'S22':('V0','microtexture as terrain','Mic the paper fold, sleeve and ventilation to feel immense without making it loud. The worker has dignified hands; sparse felted note not synchronised to repair.','The paper-house manufacturing grammar, not the same miniature, retrospectively links to S11.','Thomas Demand — Office'),
'S23':('V0','delayed acoustic reflection','Footstep is on-screen; a softer separately designed resonance follows later. Use a deliberate composition effect, not a claim about natural optical propagation.','Delayed time from S03/S17 resolves as acceptance of an uncontrollable creation.','Bill Viola — The Reflecting Pool'),
'S24':('V1','polyphonic community','Market room tone, breaths, rain and independent bulb flux; child-like micro-metal from bird returns. Crowd need not chant or cheer. Original motif only fragments.','S04 bird and S21 coat return as collective memory; no literal resurrection or claim about real persons.','Rafael Lozano-Hemmer — Pulse Room'),
'S25':('V0','auditory persistence','Remove all new ambience at 87.000 s; preserve only exact phase-continuous sine from 0.500 s. End at 90.000 s with click-safe boundary.','End of image != end of conceptual time; S01 sound finally receives an interpretation.','On Kawara — One Million Years (Future)')
}
assert len(spec)==25
# Changes are overlay; all existing file contents immutable.
slots=[]
for s in shots:
 sid=s['id']; mode,mechanism,prompt,recall,artist=spec[sid]
 old=sound.get('shot_sound_cues',[])
 ir=illusions.get(sid,{})
 slots.append({'shot_id':sid,'start_ms':s['start_ms'],'end_ms':s['end_ms'],'duration_ms':s['duration_ms'],'title':s['title_zh'],'voice_mode':mode,'semantic_intent':mechanism,'original_sound_prompt_en':prompt,'object_sonic_recall':recall,'art_method_cross_reference':artist,'illusion_id':ir.get('illusion_id'),'generation_action':'NONE', 'approval_state':'CANDIDATE_NOT_SIGNED','human_audio_qc':'NOT_RUN','rights_qc':'NOT_RUN'})
# audio references only verified known/official URLs; no sampling
references=[
 {'subject':'Nolan 2014 impressionistic dialogue-as-effect','url':'https://www.theguardian.com/film/2014/nov/17/interstellar-sound-christopher-nolan','scope':'Some purposeful masking; story clarity should be multimodal, not generally inaudible.'},
 {'subject':'Nolan 2020 radical mixing controversy','url':'https://www.the-independent.com/arts-entertainment/films/news/christopher-nolan-sound-mixing-variations-complaints-b1722463.html','scope':'Mixed reception; no universal rule to obscure dialogue.'},
 {'subject':'Sakamoto async direct interview','url':'https://ototoy.jp/feature/20170417','scope':'Irregular rhythms, tactile sound, domestic piano and presence of street noise.'},
 {'subject':'Sakamoto sound and noise interview','url':'https://www.thefader.com/2017/05/05/ryuichi-sakamoto-async-interview/','scope':'Listening to non-musical everyday sounds as musical material.'},
 {'subject':'Water state 1 YCAM','url':'https://www.ycam.jp/archive/works/water-state-1/','scope':'Material relationship of droplets, ripples, light and spatial sound.'},
 {'subject':'IS YOUR TIME artist archive','url':'https://www.sitesakamoto.com/artworks/18/','scope':'Damaged piano, sound-as-object and controlled gallery sound environment.'},
 {'subject':'EBU R128 broadcast target','url':'https://tech.ebu.ch/publications/r128/','scope':'-23 LUFS for EBU programmes; not universal for cinema or platform social video.'}
]
# 5 stems unchanged; new voice V2 vs V3 policies; no peak claim universal
model={
 'project':'J4 ASYNC: SUCCESSION', 'version':'v3.7-design-only',
 'status':'CANDIDATE_NOT_SIGNED_NO_SOUND_RENDER_NO_PAID_GENERATION',
 'baseline':{'shot_ir_path':str(shot_path),'shot_ir_sha256':sha(shot_path),'sound_ir_path':str(sound_path),'sound_ir_sha256':sha(sound_path),'illusion_ir_path':str(illusion_path),'illusion_ir_sha256':sha(illusion_path)},
 'fixed_timeline':{'fps':30,'duration_ms':90000,'shot_count':25,'local_s10_event_ms':38600,'global_stop_ms':63700,'sine_start_ms':500,'sine_end_ms':90000},
 'principles':{'nolan':'Information, sound and emotion may be distributed across multiple channels; do not hide indispensable plot information.', 'sakamoto':'Non-musical material, natural micro-timing, sound/noise/music boundaries, and acoustic space; no copying recordings or characteristic composition.', 'sound_is_not_loudness':'Create meaning via source identity, spectral masking, spatial position, rhythm, decay and temporal offset instead of indiscriminate level increase.', 'source_speaker':'All voices fictional and original; no imitations.'},
 'voice_modes':{'V0':'No words; meaningful ambience and Foley only.','V1':'Nonsemantic human texture; no essential speech.','V2':'Purposefully fragmented speech; no unique plot fact may depend on the obscured words.','V3_OPTIONAL':'Meaning-bearing fictional speech only in explicit selected shot; guaranteed by clear mix or visual and caption fallback.'},
 'stems_inherited':['STEM_01','STEM_02','STEM_03','STEM_04','STEM_05'],
 'mix_rules':{'g1':'Critical meaning must be understandable in a muted picture or recoverable via accessible captions without an inaccurate claim.', 'g2':'Masking must be motivated by a real source or a deliberate narrative cue; avoid blanket dialogue suppression.', 'g3':'S18 cuts only six designated phase families while phase-continuous original sine survives.', 'g4':'S10 local pitch-tail exception at 38600ms is not a global cycle event.', 'g5':'Check headphones, mobile mono and quiet playback; stereo-only positional plot clues need alternate support.', 'g6':'-14 LUFS / -1 dBTP from legacy draft is one proposed online delivery setting, not an IMAX, cinema or universal platform standard.', 'g7':'Original sound only: no Sakamoto, Nolan film composer, contemporary-art installation recording, voice clone or identifiable sample.'},
 'source_register':references,
 'shots':slots,
 'gates':{'creative_director':'NOT_RUN','media_playback':'NOT_RUN','semantic_intelligibility':'NOT_RUN','originality_rights':'NOT_RUN','delivery_loudness_measured':'NOT_RUN','higgsfield_authorization':'BLOCKED'}
}
(out/'j4_sound_dramaturgy_overlay_v3_7.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
with (out/'j4_25shot_voice_sound_matrix_v3_7.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(slots[0].keys()));w.writeheader();w.writerows(slots)
# Memory arcs specifically named, with sound reinterpretation and cue state
arcs=[
 ('ARC_SINE','S01','S18','S25','Sine starts as unexplained signal; at forced stop the audience hears what survived; at end its continued phase means invisible time persists.','Janet Cardiff — The Forty Part Motet; On Kawara — One Million Years'),
 ('ARC_LIGHT','S02','S03','S24','Domestic light transforms to abstract institutional reflection and back to weathered human light. Sound crosses via electricity, vapor and street tone.','Ryuichi Sakamoto & Shiro Takatani — water state 1'),
 ('ARC_BIRD','S04','S24','S25','Small fragile metal micro-ring becomes a collective memory cue; do not claim the same original sample is copied from outside.','Studio DRIFT — Fragile Future; Rafael Lozano-Hemmer — Pulse Room'),
 ('ARC_COAT','S10','S21','S24','Metal cage resonance evokes missing identity; the key handoff reveals a different coat; sound cannot falsely identify coat A or B.','Tim Noble & Sue Webster — Dirty White Trash (with Gulls)'),
 ('ARC_PAPER','S11','S22','S23','Factory paper house is inaudible detail; later paper-fold Foley changes understanding; S23 retains one short dry texture decay.','Thomas Demand — Office'),
 ('ARC_APPLAUSE','S08','S14','S24','Contagious claps become empty institutional echoes, finally replaced by breathing/rain without applause.','Tino Sehgal — This Situation; Janet Cardiff & George Bures Miller — The Murder of Crows'),
 ('ARC_THREADS','S12','S13','S15','Telephone cable harmonic becomes detuned piano string and ultimately textile fiber friction.','Chiharu Shiota — Uncertain Journey'),
 ('ARC_AUTHORITY','S18','S19','S21','Silent three-forms gain political-looking institutional seats, key contact gives tactile evidence of control transfer.','Carsten Nicolai — unidisplay; Hito Steyerl — Factory of the Sun')
]
with (out/'j4_sonic_recall_arcs_v3_7.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['arc_id','origin_shot','reveal_shot','later_shot','sonic_causality','art_reference']);w.writerows(arcs)
profiles={
 'status':'PROPOSED_NOT_MEASURED','base_sample_rate_hz':48000,'native_stems':5,
 'profiles':[
  {'id':'GALLERY','format':'48kHz PCM 24-bit multichannel or stereo according to room','loudness_target':'calibrate by room acoustics and SPL measurement; do not adopt -14 LUFS blindly','dynamic':'preserve designed silence with safety maximum and accessibility alternative','requirements':['sound-system calibration','room impulse check','listening position tests','no unmonitored extreme sub-bass']},
  {'id':'ONLINE_STEREO','format':'48kHz stereo PCM master to encoded platform format','loudness_target':'-14 LUFS integrated as INTERNAL candidate only; measure platform behavior','true_peak_ceiling':'-1 dBTP as internal safety target, validate codec','requirements':['quiet earphones','phone speaker','mono downmix','captions on/off']},
  {'id':'ACCESSIBLE','format':'stereo plus accurately timed English subtitles / optional dialogue-forward alternate','loudness_target':'platform tested, not inherited from gallery','requirements':['all plot-essential voice either clear or mirrored by visuals/captions','avoid unaudited flashing or distressing levels','readable text alternatives','transcript']}
 ],
 'note':'EBU R128 -23 LUFS refers to EBU programme context. Existing J4 -14 LUFS / -1 dBTP is a proposal, not a universal broadcaster or platform requirement.'
}
(out/'j4_mix_delivery_profiles_v3_7.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n')
# Human readable detailed note
header='''# J4 v3.7 — 聲音即敘事：Nolan × 坂本龍一\n\n**Status:** 候選聲畫敘事規格；未生成聲音、未混音、未修改既有 Shot/Sound IR、未通過真人聽測。\n\n## 核心判斷\n\nNolan 的可用方法不是「全部台詞聽不見」，而是將 *非必要的語言資訊* 改造成有空間與情緒功能的聲響。坂本龍一的可用方法是從物質、雨、水、舊設備、呼吸與不規則節奏中尋找音樂性。J4 把兩者結合為可驗證的敘事規則，而非音量競賽。\n\n## 人聲重要性契約\n\n- **V0**：無語義人聲，物件與空間說故事。\n- **V1**：人類存在的音色或含混話聲，不承擔劇情資訊。\n- **V2**：部分被遮蔽的人聲，遮蔽本身具有戲劇功能，不能藏唯一重要的資訊。\n- **V3_OPTIONAL**：重要虛構台詞若保留，必須可聽懂，或有可理解的視覺／字幕替代；S21 最合理。\n\n**混音原則：** 覆蓋人聲不等於提高音樂的 LUFS。優先設計聲源合理性、不同頻段的遮蔽、空間反射、聽覺距離與時間差；聲學密度高不必音量大。\n\n## 四位藝術家分工不變\n\n- 坂本龍一 × 高谷史郎：聲源物質、殘響、空間、自然非同步。\n- Ryoji Ikeda：相位與週期、時間事件、訊號密度的精確調度。\n- 塩田千春：物件和缺席人物的情感召喚、跨鏡記憶。\n- Thomas Demand：物件聲音要對應可信的材質與施工，不許浮空音效。\n\nNolan 提供 *sound dramaturgy* 的敘事參考，不被列為新增一位真正的藝術導演，也不重製任何既有電影音樂。\n\n## 全片非同步約束\n\n- 0.500s 的原創 sine 到 90.000s 保持同一聲源與相位。\n- 六個 phase family 保持原基準起點與 7/11/5/13/19/17 秒週期；這是設計時鐘，不代表需一直被聽見。\n- 38.600s S10 只切 **局部音尾**，不可切斷六個 phase family。\n- 63.700s S18 全部六組運作聲源被迫同時中斷；sine 不停止。\n- 65s 後新的局部音色可回歸，但 **不要自動重啟** 原相位循環。\n- 87s S25 去掉環境聲，只留 sine；90s 概念上未結束，技術上需 clean boundary 避免 click。\n\n## 25 鏡聲音敘事表\n\n'''
lines=['| Shot | Voice | 聲畫機制 | 物件／時間回響 |','|---|---|---|---|']
for row in slots:
 lines.append('| '+row['shot_id']+' | '+row['voice_mode']+' | '+row['semantic_intent']+' | '+row['object_sonic_recall'].replace('|','/')+' |')
md=header+'\n'.join(lines)+'''\n\n## 要先審的 6 個高風險聲畫節點\n\n1. **S09（遮蔽）**：可有模糊的原創女性聲線，但此鏡不能靠她說出某個政策主張才成立。盲測只問：誰在對誰發聲？\n2. **S10（局部斷尾）**：38.600s 只切主觀鋼琴-like 殘響；不能誤觸 S18 全局事件。\n3. **S14（空洞掌聲）**：遠處掌聲聲源位置與可見群眾人數不相等；情緒應是空間回聲而非恐怖大音量。\n4. **S17–S18（非同步到強制中斷）**：聲部最多但不是最響；沒有大爆炸、超低頻音壓或硬切波形 click。\n5. **S21（語義樞紐）**：鑰匙交到另一隻手即可傳遞關鍵資訊。若要保留 `Nothing changes. Everything changes.` 應給獨立可理解版本；比賽版可以無詞。\n6. **S22–S24（記憶回返）**：紙折聲不表示笨拙；S24 重回人聲與雨，但不恢復 7s phase。光鳥回到外套上時避免音樂作「英雄降臨」的音效。\n\n## 多平台混音\n\n保留 5 stems 原格式；設三種交付用途：GALLERY、ONLINE_STEREO、ACCESSIBLE。此前 `-14 LUFS / <= -1 dBTP` 僅視為線上候選，不能當作 IMAX 或美術館要求。EBU R128 的 -23 LUFS 是廣播標準脈絡，不能直接移用到所有交付版本。最終以實測 true peak、integrated loudness、LRA、單聲道、手機喇叭、低音量耳機與字幕可讀性決定。\n\n## 尚未執行\n\n沒有合法音源檔、沒有實際混音、沒有 LUFS / dBTP 測量、沒有受測觀眾，所有 Sound QC = NOT_RUN。Higgsfield 仍 BLOCKED，需要原先三道授權與額度檢查。\n\n## 研究來源（方法參考，非授權音源）\n\n'''
md+='\n'.join(f'- {x["subject"]}: {x["url"]}' for x in references)+'\n'
(out/'SOUND_DRAMATURGY_v3_7.md').write_text(md)
(out/'README_v3_7.md').write_text('''# J4 v3.7 — Sound Is Narrative\n\n此工程包是對既有 v2.8 Sound IR 和 v2.9 Shot IR 的 **read-only overlay**，不覆寫原始檔案。\n\n- `SOUND_DRAMATURGY_v3_7.md`：導演方法與每鏡聲音的敘事位置。\n- `j4_sound_dramaturgy_overlay_v3_7.json`：25 鏡可機械讀取的 Voice / Sound 層。\n- `j4_25shot_voice_sound_matrix_v3_7.csv`：25 鏡可審核表。\n- `j4_sonic_recall_arcs_v3_7.csv`：8 條記憶聲音回響。\n- `j4_mix_delivery_profiles_v3_7.json`：美術館、網路、無障礙交付候選。\n- `validate_v3_7.py`：獨立驗證（只讀原檔）。\n\n## Gate status\n\nCANDIDATE_NOT_SIGNED_NO_SOUND_RENDER_NO_PAID_GENERATION；六組聲部中斷與 90 秒不變。音訊人工 QC、來源權利、生成授權皆未通過。\n''')
# validator in standalone bundle uses baseline snapshot only for content hash regression
snapshot=out/'baseline';snapshot.mkdir(exist_ok=True)
(snapshot/'j4_shots_v2_9.json').write_bytes(shot_path.read_bytes())
(snapshot/'j4_sound_ir_v2_8.json').write_bytes(sound_path.read_bytes())
validator='''from pathlib import Path\nimport json,csv,hashlib\nroot=Path(__file__).resolve().parent\nd=json.loads((root/'j4_sound_dramaturgy_overlay_v3_7.json').read_text())\nshots=json.loads((root/'baseline/j4_shots_v2_9.json').read_text())['shots']\nsound=json.loads((root/'baseline/j4_sound_ir_v2_8.json').read_text())\nassert len(shots)==25==len(d['shots'])\nassert [s['id'] for s in shots]==[s['shot_id'] for s in d['shots']]\nassert shots[0]['start_ms']==0 and shots[-1]['end_ms']==90000\nassert all(x['end_ms']==y['start_ms'] for x,y in zip(shots,shots[1:]))\nassert all(s['start_ms']==m['start_ms'] and s['end_ms']==m['end_ms'] for s,m in zip(shots,d['shots']))\nassert all(p['forced_stop_ms']==63700 for p in sound['phase_families']) and len(sound['phase_families'])==6\nassert [p['period_ms'] for p in sound['phase_families']]==[7000,11000,5000,13000,19000,17000]\nassert d['fixed_timeline']['global_stop_ms']==63700 and d['fixed_timeline']['local_s10_event_ms']==38600\nassert len(set(s['shot_id'] for s in d['shots']))==25\nassert all(s['human_audio_qc']=='NOT_RUN' and s['generation_action']=='NONE' for s in d['shots'])\nassert d['gates']['higgsfield_authorization']=='BLOCKED'\nfor path,key in [('j4_shots_v2_9.json','shot_ir_sha256'),('j4_sound_ir_v2_8.json','sound_ir_sha256')]:\n p=root/'baseline'/path\n assert hashlib.sha256(p.read_bytes()).hexdigest()==d['baseline'][key]\nwith (root/'j4_sonic_recall_arcs_v3_7.csv').open() as f:\n assert len(list(csv.DictReader(f)))==8\nprint('PASS: 25 shots, 90s, 6 phases, 8 sonic arcs, no generation, original baseline checksum.')\n'''
(out/'validate_v3_7.py').write_text(validator)
subprocess.run(['python',str(out/'validate_v3_7.py')],check=True)
zipf=root/'j4_museum_v3_7_bundle.zip'
with zipfile.ZipFile(zipf,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.rglob('*')):
  if p.is_file(): z.write(p,p.relative_to(root))
with zipfile.ZipFile(zipf) as z:
 assert z.testzip() is None
print('WROTE',zipf,zipf.stat().st_size,'bytes')
print('VOICE MODES',dict(Counter(s['voice_mode'] for s in slots)))
