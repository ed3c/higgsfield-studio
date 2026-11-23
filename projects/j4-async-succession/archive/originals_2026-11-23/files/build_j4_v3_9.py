#!/usr/bin/env python3
"""Build a zero-media, zero-generation J4 v3.9 sonic-object memory overlay."""
from __future__ import annotations
import csv, hashlib, html, json, shutil, zipfile
from pathlib import Path

ROOT=Path('/mnt/data')
SRC=ROOT/'j4_museum_v3_8'/'baseline'
OUT=ROOT/'j4_museum_v3_9'
OUT.mkdir(exist_ok=True)
source_paths={k:SRC/k for k in ('j4_shots_v2_9.json','j4_sound_ir_v2_8.json','j4_sound_dramaturgy_overlay_v3_7.json','j4_mix_delivery_profiles_v3_7.json')}
shots=json.loads(source_paths['j4_shots_v2_9.json'].read_text())['shots']
sound=json.loads(source_paths['j4_sound_ir_v2_8.json'].read_text())
shot_lookup={s['id']:s for s in shots}
assets=json.loads((ROOT/'j4_museum_v3_2'/'j4_object_registry_v3_2.json').read_text())['assets']
asset_lookup={a['asset_id']:a for a in assets}
art=[
 ('Studio DRIFT','Fragile Future','https://studiodrift.com/work/fragile-future/','physical fragility and hybrid electronics, not original sounds or shapes'),
 ('Rafael Lozano-Hemmer','Pulse Room','https://www.lozano-hemmer.com/pulse_room.php','different individual timing within shared light, not bulb array or actual heartbeat data'),
 ('Tim Noble & Sue Webster','Dirty White Trash (with Gulls)','https://www.moma.org/calendar/exhibitions/4798','material shadow/reinterpretation, not silhouette artwork'),
 ('Doris Salcedo','Atrabilious','https://www.moma.org/collection/','absence through material traces, not victim equivalence or memorial format'),
 ('Thomas Demand','Office','https://www.guggenheim.org/artwork/artist/thomas-demand','paper-built constructed reality, not original office composition'),
 ('Mierle Laderman Ukeles','Washing/Tracks/Maintenance: Inside','https://www.maintenanceartist.com/artworks','respect for maintenance gestures, not copying performance'),
 ('Janet Cardiff & George Bures Miller','The Murder of Crows','https://www.cardiffmiller.com/artworks/inst/murder_of_crows.html','spatial narrative via dispersed acoustic position, not installation recording'),
 ('Dan Graham','Present Continuous Past(s)','https://collection.centrepompidou.fr/artwork/150000000020624','time-delayed recognition, not video installation setup'),
 ('Ryuichi Sakamoto & Shiro Takatani','water state 1','https://www.ycam.jp/en/archive/works/water-state-1/','physical causality across water, sound and light; no sample or composition'),
 ('On Kawara','One Million Years','https://www.diaart.org/collection/collection/kawara-on-one-million-years-1993','duration beyond visibility, not recitation'),
]
# The source URLs are research pointers; this script does not claim fresh page verification.
families=[
 dict(id='BIRD_METAL',asset_id='filament_bird_v1',kind='PHYSICAL_SAME_OBJECT',source=['S04'],recall=['S24'],
      art=['Studio DRIFT — Fragile Future','Rafael Lozano-Hemmer — Pulse Room'],
      invariant='Single tungsten-like filament; three asymmetric joints; original micro-metal family retains identifiable attack spectrum contour, never samples an artist recording.',
      state_change='S04 tight brittle contact, S24 softened attack/longer environmental tail; same physical bird, new acoustic context.',
      test_var='presence of the SAME originally composed material fingerprint; retain onset, duration, level and full mix for both versions',
      negative='Use newly authored unrelated metallic contact, matched timing, amplitude envelope and perceived prominence; no stolen audio.'),
 dict(id='COAT_ARCHIVE',asset_id='archive_coat_B',kind='DECEPTIVE_SIMILAR_OBJECT',source=['S10'],recall=['S21','S24'],
      art=['Tim Noble & Sue Webster — Dirty White Trash (with Gulls)','Doris Salcedo — Atrabilious'],
      invariant='Archive B has NO left-hem repair. S10 sound MUST NOT claim it is coat A. Enclosure mesh/pitched tail belongs to S10, not founder identity.',
      state_change='S10 proximity and mesh contact place garment in archive; S21/S24 show DIFFERENT garment A. Shared textiles are not evidence of same physical identity.',
      test_var='archive B and main coat A may share wool/cotton family, but have distinguishing fabric friction and no reuse of exact B fingerprint',
      negative='Make both coats identical in acoustic fingerprint to test false identity cue; only for research, never promote to final.'),
 dict(id='COAT_MAIN',asset_id='founder_coat_A',kind='PHYSICAL_SAME_OBJECT',source=['S03','S17','S21'],recall=['S24'],
      art=['Doris Salcedo — Atrabilious','Dan Graham — Present Continuous Past(s)'],
      invariant='Same long work coat A with repaired LEFT hem across S03/S17/S21/S24; avoid celebrity cut or texture.',
      state_change='S21 no longer worn: dry woven fabric brush near empty chair; S24 held by multiple hands: wider cloth friction and outdoor wet air.',
      test_var='preserve same material family with environmental transformation, not a literal sound copy',
      negative='Unrelated fabric noise of equal length and prominence in S24 with identical visuals.'),
 dict(id='PAPER_FOLD',asset_id='paper_house_v1',kind='SHARED_FABRICATION_GRAMMAR',source=['S11'],recall=['S22','S23'],
      art=['Thomas Demand — Office','Mierle Laderman Ukeles — Washing/Tracks/Maintenance: Inside'],
      invariant='S11 and S22 paper houses are NOT same physical object. Preserve irregular roof fold and small nonrectangular window as design grammar.',
      state_change='S11 a tiny page edge responds to ventilation (quiet); S22 close fingernail/fold friction makes same construction audible; S23 residual paper-memory tail.',
      test_var='match paper fibre quality and folding articulation across both scenes while perspective and acoustic scale change',
      negative='Use distinct stock/fold-sound articulation in S22 with identical visual design/level to isolate memory effect.'),
 dict(id='HANDOVER_KEY',asset_id='handover_key',kind='SINGLE_HANDOVER',source=['S21'],recall=[],
      art=['Dan Graham — Present Continuous Past(s)'],
      invariant='Exactly one physical key; close brass contact; this is a transition punctuation, NOT a recurring sound recalling a second key.',
      state_change='Single metal contact decays after ownership has changed; transitions into paper handling through edited acoustic texture only.',
      test_var='no A/B identity test required; monitor whether this cue falsely suggests a second key',
      negative='Do not add duplicated or echoed key attack that sounds like a second object.'),
 dict(id='APPLAUSE_SPACE',asset_id='acoustic_reflector',kind='CONTRAST_THROUGH_ABSENCE',source=['S08'],recall=['S14','S24'],
      art=['Janet Cardiff & George Bures Miller — The Murder of Crows'],
      invariant='S08 human claps remain physically tied to individuals; S14 reverberation/indirect source dominates; S24 has NO applause.',
      state_change='Social claps -> institution apparently clapping itself -> people support coat silently, no consensus ritual.',
      test_var='spatial direct/reverberant ratio at S14 from v3.8 Trial B; do not test it as louder vs quieter',
      negative='S24 should remain free of applauding sound, even if generated audio hallucinates it.'),
 dict(id='SINE_GROUND',asset_id=None,kind='NON_OBJECT_PERPETUAL_ANCHOR',source=['S01'],recall=['S18','S25'],
      art=['Ryuichi Sakamoto & Shiro Takatani — water state 1','On Kawara — One Million Years'],
      invariant='ONE oscillator from 500ms to 90000ms; phase never restarts; 63700ms six families forced stop; 87000ms sine-only.',
      state_change='S01 unknown source -> S18 survivor of global cut -> S25 duration after visible world disappears.',
      test_var='never swap by independent per-scene samples; only change pre-locked synth design globally',
      negative='No retrigger or additional drone at S18/S25; export de-click is allowed at terminal only.'),
]

# Intended cue placement: absolute timeline ms, sample-accurate at 48kHz, not fabricated recorded sounds.
# Some cues remain silent constraints or nonaudible placeholders. Event durations are NOT actual sound renders.
cues=[
 ('SIN_001','S01',500,3000,'SINE_GROUND','STEM_01','continuous_oscillator_start','phase stable; persists beyond this shot'),
 ('BIRD_01','S04',13300,14000,'BIRD_METAL','STEM_03','material_contact','tiny original wire micro-contact when wire sculpture lifts; no heroic wingbeat'),
 ('CLAP_08','S08',29000,31950,'APPLAUSE_SPACE','STEM_03','human_gesture','gradually contagious handclaps; end in short room decay'),
 ('COAT_B_10','S10',37800,38600,'COAT_ARCHIVE','STEM_03','material_contact','mesh/fabric and local pitched tail; local tail cut exactly 38600'),
 ('PAPER_11','S11',42100,42600,'PAPER_FOLD','STEM_03','ambient_causality','paper-house loose edge gently moves due to ventilation; extremely subtle'),
 ('CLAP_14','S14',50500,52950,'APPLAUSE_SPACE','STEM_05','spatial_recontextualization','the SAME kind of clap events now distributed in opera acoustics; not more volume'),
 ('GLOBAL_18','S18',63700,63700,'SINE_GROUND','CONTROL','global_cut','six phase families forced to stop; continuous sine untouched'),
 ('KEY_21','S21',74550,74850,'HANDOVER_KEY','STEM_03','ownership_contact','one brass key click only, not doubling'),
 ('COAT_A_21','S21',75200,76000,'COAT_MAIN','STEM_03','material_contact','left in chair, close dry textile brush; archive B fingerprint not reused'),
 ('PAPER_22','S22',76900,77900,'PAPER_FOLD','STEM_03','close_material_fold','close dry fold/fingernail, same material grammar as S11, not same physical house'),
 ('PAPER_23','S23',79500,79800,'PAPER_FOLD','STEM_03','short_residual','single fading paper timbre, not a renewed paper-world loop'),
 ('COAT_A_24','S24',84450,85150,'COAT_MAIN','STEM_03','material_contact','group hands support empty coat, wide outdoor fabric friction'),
 ('BIRD_24','S24',85150,85850,'BIRD_METAL','STEM_03','timbre_recall','same bird material fingerprint as S04, softer attack and longer tail'),
 ('SINE_ONLY_25','S25',87000,87000,'SINE_GROUND','CONTROL','strip_to_sine','remove all other layers and preserve ONE phase-stable oscillator until 90000'),
]
for eid,sid,a,b,fam,stem,kind,note in cues:
    if sid!='S01' and not (shot_lookup[sid]['start_ms']<=a<=b<=shot_lookup[sid]['end_ms']): raise RuntimeError((eid,sid,a,b))
    if sid=='S01' and b>3000: raise RuntimeError('Bad sine range')

sha={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in source_paths.items()}
registry={
 'project':'J4 ASYNC: SUCCESSION','version':'v3.9 Sound-to-Object Recall Gate','status':'CANDIDATE_DESIGN_ONLY_NO_MEDIA_NO_GENERATION',
 'baseline_sha256':sha,'audio_sample_rate_hz':48000,'fps':30,'duration_ms':90000,
 'source_object_registry':{'path':'j4_museum_v3_2/j4_object_registry_v3_2.json','sha256':hashlib.sha256((ROOT/'j4_museum_v3_2'/'j4_object_registry_v3_2.json').read_bytes()).hexdigest()},
 'immutable_events':{'sine_start_ms':500,'local_pitched_tail_cut_ms':38600,'six_family_forced_stop_ms':63700,'new_market_memory_ms':84000,'sine_only_ms':87000,'end_ms':90000},
 'six_phase_families_unchanged':[{k:x[k] for k in ('id','start_ms','period_ms','forced_stop_ms')} for x in sound['phase_families']],
 'global_constraints':{'no_original_artist_audio':True,'do_not_derive_sound_from_protected_recording':True,
                       'no_actual_audio_generated':True,'no_new_keyframe_generated':True,
                       'never_confuse_design_family_with_physical_identity':True,
                       'phase_families_off_after_global_cut':True,
                       'permissions':'Neon explicit GO + Director estimate in AI Video Production Service + actual monthly credit check + rights check required before billable generation'},
 'families':families,
 'art_method_sources':[dict(artist=a,work=w,url=u,permitted_method=m,rights='RESEARCH_ONLY_NO_REPRODUCTION_RIGHT') for a,w,u,m in art],
 'event_count':len(cues),'event_policy':'Start/end times are DESIGN targets, never measured material; do not confuse these with actual recorded clips.',
}
(OUT/'j4_sonic_object_registry_v3_9.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')

cols=['event_id','shot_id','global_start_ms','global_end_ms','duration_ms','audio_start_sample_48k','audio_end_sample_48k','family_id','stem','event_kind','candidate_instruction','media_status','creative_gate','rights_status']
with (OUT/'j4_sound_object_cues_v3_9.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(cols)
 for eid,sid,a,b,fam,stem,kind,note in cues:
  w.writerow([eid,sid,a,b,b-a,a*48,b*48,fam,stem,kind,note,'NOT_RENDERED','PENDING','NOT_RUN'])

trials=[
 dict(id='R1_BIRD',name='同一光鳥的聽覺返場',origin='S04',reveal='S24',art='Studio DRIFT — Fragile Future / Rafael Lozano-Hemmer — Pulse Room',
      target='S24 using SAME authored material fingerprint as S04 with altered soft attack and longer physical room tail',
      control='S24 uses DIFFERENT authored micro-metallic material fingerprint with same timing, duration, space and perceived level',
      only_variable='micro-metal material fingerprint at S24, not volume or visual content',
      question='你是否覺得這個聲音曾出現？哪一段讓你想到它？',
      confounds=['visual same bird present','near-identical loudness','same pan and onset','no music swell','original-only sources'],
      status='NOT_RUN_NO_MEDIA'),
 dict(id='R2_COAT',name='外套 A/B 的材質相似與身分區分',origin='S10',reveal='S21',art='Tim Noble & Sue Webster — Dirty White Trash (with Gulls) / Doris Salcedo — Atrabilious',
      target='S10 mesh+archive-B cloth, S21/A distinct coarse-woven long-coat cloth; visually repaired left hem belongs only to A',
      control='remove distinguishing textile friction cue while preserving plot and shot timing; NEVER label B as A',
      only_variable='distinguishing textile friction detail, not clothing visibility, contact time or image',
      question='你認為兩鏡是同一件衣服嗎？你依據的是畫面還是聲音？',
      confounds=['two physical coats remain different in both conditions','S10 mesh event not reused','repair visibility identical','no narrator cue'],
      status='NOT_RUN_NO_MEDIA'),
 dict(id='R3_PAPER',name='S11 紙屋到 S22 紙海岸的聲音語法',origin='S11',reveal='S22',art='Thomas Demand — Office / Mierle Laderman Ukeles — Maintenance Art',
      target='same fibrous hand-fold articulation at S11 and S22 with different recording distance and acoustic scale',
      control='S22 another original paper texture of similar loudness and length, leaving visuals unchanged',
      only_variable='paper folding material/tactile grammar, not exact sonic sample or physical object identity',
      question='兩個場景的手工物件之間是否存在關係？你聽到了什麼共同特徵？',
      confounds=['S11 small prop still legible','S22 same paper model','same duration','same mix prominence','S23 residual retained'],
      status='NOT_RUN_NO_MEDIA'),
]
(OUT/'j4_recall_trials_v3_9.json').write_text(json.dumps({'version':'v3.9','trials':trials,
 'protocol':'Between-subject T/C, first unguided answer, reveal, rewatch, evidence quote; counterbalance groups; double-blind rating when real media exists.',
 'stimulus_status':'BLOCKED_NO_REAL_MEDIA',
 'claim_limit':'Pre-registration and cue design only; no human effects established.'},ensure_ascii=False,indent=2)+'\n')

# Cross-walk includes every designed event/family and a research citation, not media rights.
with (OUT/'j4_sonic_art_crosswalk_v3_9.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['family_id','asset_id','source_shots','recall_shots','art_method_references','relationship_type','prohibited_copy','approval'])
 for fa in families:
  w.writerow([fa['id'],fa['asset_id'] or 'SOUND_ONLY',';'.join(fa['source']),';'.join(fa['recall']),'; '.join(fa['art']),fa['kind'],'No reference audio/visuals; methods only','NOT_RUN'])

readme='''# J4 v3.9 — Sound-to-Object Recall Lock

**State: CANDIDATE / NO_REAL_MEDIA / NO_AUDIO_RENDER / NO_PAID_GENERATION / NO_DIRECTOR_SIGNOFF.**

v3.8 established four A/B listening tasks. v3.9 makes the sound–object identity constraints explicit and adds three P0 retrospective recall tests. It does not overwrite the v2.8 Sound IR or v2.9 Shot IR.

## New files

- `j4_sonic_object_registry_v3_9.json`: seven sonic families mapped to exact v3.2 asset IDs where available; explicit distinctions between physical identity, design grammar and metaphor.
- `j4_sound_object_cues_v3_9.csv`: proposed cue timings in global milliseconds and exact 48 kHz sample positions; **not rendered audio**.
- `j4_recall_trials_v3_9.json`: three controlled T/C hypotheses, not human test outcomes.
- `j4_sonic_art_crosswalk_v3_9.csv`: method-only art research, no rights implied.
- `SONIC_OBJECT_DIRECTOR_CONTRACT_v3_9.md`: creative/technical gates and cue source rules.
- `j4_sonic_object_board_v3_9.html`: offline cue and experiment review board, no audio playback; exports human notes as JSON.
- `validate_v3_9.py`: explicit constraints and baseline hashes.
- `TEST_REPORT_v3_9.md`: tests executed, blockers.

## Non-negotiable timing

- S01 sine begins at **500 ms**, remains ONE phase-stable sound source through 90,000 ms.
- S10 local pitched tail stops at **38,600 ms**, not a phase-family stop.
- S18 six existing phase families are forcibly stopped at **63,700 ms**. No restart later.
- S24 **84,000 ms** starts *new* human market ambience, never restarts the seven-second loop.
- S25 **87,000–90,000 ms** sine only; de-click at terminal edit.

## Crucial identity protections

1. Archive coat B is NOT founder coat A; superficial material similarity does not prove physical sameness.
2. Paper house S11 is NOT physically the same object as the paper dwelling of S22: shared fabrication grammar only.
3. Wire bird S04 and S24 is one physical prop identity; timbre may be transformed through space and decay, not replaced with original artist material.
4. Hand-over key is a single unique piece. Do not fake a second attack that implies two keys.
5. Avoid claiming music/sound marks are scientifically distinctive before audio is produced and tested.

## Governance

Keep all experiments DESIGN_ONLY. No sound synthesis, no prompts sent to generation endpoints, no video renders. Existing Neon explicit approval + Director estimates posted + actual 9,000-point ceiling verification remain mandatory for billable work. Art references are *methodology only*; sound and image rights not presumed.
'''
(OUT/'README_v3_9.md').write_text(readme)

contract='''# Director Sound-to-Object Contract — J4 v3.9

## 1. Three different meanings of sonic continuity

- **Identity** — S04/S24 filament bird; S21/S24 coat A: the SAME physical thing. Re-author original sounds for each space; preserve identifiable tactile family without direct sample reuse from protected art.
- **Grammar** — S11/S22 paper houses: DIFFERENT physical things made with the same folding language. A shared fibrous texture should not imply they were transported between scenes.
- **False friend** — S10 archived coat B and S21 main coat A: two garments that look similar. Their acoustic detail must NOT assert the same physical owner/identity.

## 2. Method references (never sound samples)

- **Studio DRIFT, *Fragile Future*** — material fragility of engineered light; applies to BIRD_METAL. No copying of dandelion form or recorded sounds.
- **Rafael Lozano-Hemmer, *Pulse Room*** — multiple personal timing regimes coexist; informs bird's return amid nonsynchronised people.
- **Tim Noble / Sue Webster, *Dirty White Trash (with Gulls)*** and **Doris Salcedo, *Atrabilious*** — perception of absent person and object's memory, without copying images, memorial material or equating business departures with violence victims.
- **Thomas Demand, *Office*** — constructed paper reality; paper grammar and truthful material friction.
- **Mierle Laderman Ukeles, *Washing/Tracks/Maintenance: Inside*** — valued maintenance gestures, distinguishing human labour from useless bureaucracy.
- **Janet Cardiff / George Bures Miller, *The Murder of Crows*** — dispersed sound source creates architectural meaning, not the audio or installation configuration.
- **Dan Graham, *Present Continuous Past(s)*** — late reinterpretation of a prior temporal state, not a literal sampled effect.
- **Sakamoto / Takatani, *water state 1*** and **On Kawara, *One Million Years*** — micro-material processes and time beyond any given image. No album or artwork audio used.

## 3. Timing controls

48 kHz sample positions in CSV use `sample = milliseconds * 48`. Time-stamped event ranges are cues-to-produce, not measurements of existing media. Do not quantize every event to musical beat. The only full interruption remains at 63.700 s and affects the six phase families; the uninterrupted oscillator is exempt.

## 4. Trial T/C and confounds

- Bird: identical original material fingerprint vs independently authored different material, while keeping visual track, event onset, amplitude envelope, perceived loudness and spatial position matched.
- Coats: preserve same *visible* coat A/B distinction in both conditions; vary only the audible discriminating textile texture. **Failure:** audience assumes a false physical identity because the audio intentionally lied.
- Paper: match sound-making hand-fold articulation across different paper objects. Control changes only texture/hinge language; scene, action timing and audio prominence held constant.

A small formative pilot cannot prove broad psychological effectiveness. Unmixed copies, silence samples, synthetic reference tones and inferred LUFS are **not** admissible as real stimulus results.

## 5. Real audio producer hand-off fields

Before production, each sound event requires: `recording_or_synth_source`, `license_or_authorship`, `take_id`, `sample_rate`, `channel_layout`, `sync_offset_samples`, `reverb_ir_ownership`, `measured_loudness`, `true_peak`, `mono_check`, `reviewer`, `approval_timestamp`.

## 6. Stop conditions

`NO_REAL_MEDIA`, `NO_RIGHTS_REVIEW`, `NO_DIRECTOR_SIGNOFF`, or missing Neon generation approval all block a promoted result. No silent auto-approval and no media generation in this milestone.
'''
(OUT/'SONIC_OBJECT_DIRECTOR_CONTRACT_v3_9.md').write_text(contract)

# validator, always independently executable after ZIP unpack.
validator=r'''#!/usr/bin/env python3
import csv,hashlib,json,sys
from pathlib import Path
p=Path(__file__).resolve().parent
reg=json.loads((p/'j4_sonic_object_registry_v3_9.json').read_text())
tr=json.loads((p/'j4_recall_trials_v3_9.json').read_text())
shots=json.loads((p/'baseline'/'j4_shots_v2_9.json').read_text())['shots']
sound=json.loads((p/'baseline'/'j4_sound_ir_v2_8.json').read_text())
assert len(shots)==25 and sum(s['duration_ms'] for s in shots)==90000
assert all(shots[i]['end_ms']==shots[i+1]['start_ms'] for i in range(24))
assert reg['immutable_events']=={'sine_start_ms':500,'local_pitched_tail_cut_ms':38600,'six_family_forced_stop_ms':63700,'new_market_memory_ms':84000,'sine_only_ms':87000,'end_ms':90000}
assert len(sound['phase_families'])==6 and all(f['forced_stop_ms']==63700 for f in sound['phase_families'])
assert len(reg['families'])==7 and len(tr['trials'])==3
ids={f['id'] for f in reg['families']}; aset={a['asset_id'] for a in json.loads((p/'baseline'/'j4_object_registry_v3_2.json').read_text())['assets']}
assert all(f['asset_id'] in aset for f in reg['families'] if f['asset_id'])
sl={s['id']:s for s in shots}
rows=list(csv.DictReader((p/'j4_sound_object_cues_v3_9.csv').open(encoding='utf-8-sig')))
assert len(rows)==reg['event_count']
assert len({r['event_id'] for r in rows})==len(rows)
for r in rows:
 a,b=int(r['global_start_ms']),int(r['global_end_ms'])
 assert a<=b and sl[r['shot_id']]['start_ms']<=a<=b<=sl[r['shot_id']]['end_ms']
 assert int(r['audio_start_sample_48k'])==a*48
 assert int(r['audio_end_sample_48k'])==b*48
 assert r['family_id'] in ids
 assert r['media_status']=='NOT_RENDERED' and r['creative_gate']=='PENDING'
assert next(r for r in rows if r['event_id']=='GLOBAL_18')['global_start_ms']=='63700'
assert next(r for r in rows if r['event_id']=='SINE_ONLY_25')['global_start_ms']=='87000'
assert len({x['id'] for x in tr['trials']})==3
for name,sha in reg['baseline_sha256'].items():
 assert hashlib.sha256((p/'baseline'/name).read_bytes()).hexdigest()==sha,(name,'hash mismatch')
assert reg['status'].startswith('CANDIDATE_') and tr['stimulus_status']=='BLOCKED_NO_REAL_MEDIA'
print(f'PASS: 25 shots / 90000 ms / {len(reg["families"])} sonic families / {len(rows)} cue events / 3 preregistered trials / immutable six-phase stop @63700 / baseline SHA256 unchanged / NO_MEDIA')
'''
(OUT/'validate_v3_9.py').write_text(validator)

# HTML is an offline score and object state inspector; no embedded audio, no network, no claimed previews.
html_data=json.dumps({'families':families,'events':[dict(event_id=eid,shot=sid,start=a,end=b,family=fam,stem=stem,kind=kind,note=note) for eid,sid,a,b,fam,stem,kind,note in cues],'trials':trials},ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>J4 v3.9 — 聲音物件記憶審核板</title><style>
:root{color-scheme:dark;--bg:#101215;--p:#1b2024;--b:#394148;--tx:#eff1ef;--mut:#a6b1b3;--accent:#dabf8f}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Noto Sans TC",sans-serif}.wrap{max-width:1100px;margin:auto;padding:24px 20px 60px}header{border-bottom:1px solid var(--b);padding-bottom:20px;margin-bottom:22px}h1{font-size:25px;line-height:1.25;margin:4px 0}h2{font-size:19px;margin:10px 0}.mut{color:var(--mut)}.eyebrow{font-size:12px;letter-spacing:.13em;color:var(--accent);text-transform:uppercase}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.panel{background:var(--p);border:1px solid var(--b);border-radius:12px;padding:18px;min-width:0}select,button,textarea,input{background:#252c31;color:var(--tx);border:1px solid #515d64;border-radius:7px;padding:9px;font:inherit;max-width:100%}select{width:100%}button{cursor:pointer}button:hover{border-color:var(--accent)}textarea{width:100%;min-height:85px;resize:vertical}small{font-size:12px}.tag{display:inline-block;border:1px solid #7a765e;color:#e9d6ab;padding:3px 8px;border-radius:30px;font-size:12px}.line{border-top:1px solid var(--b);margin:14px 0}.track{height:50px;background:#12171b;border:1px solid var(--b);border-radius:8px;position:relative;margin:12px 0 8px;overflow:hidden}.mark{position:absolute;top:12px;height:25px;background:#baa379;border-radius:3px;min-width:3px;opacity:.92}.sine{height:9px;top:31px;background:#9fafa8;opacity:.8}.tick{font-size:11px;display:flex;justify-content:space-between;color:var(--mut)}.item{padding:8px 0;border-bottom:1px solid var(--b)}.item:last-child{border-bottom:0}.highlight{color:var(--accent)}.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.state{font-weight:600;color:#e5c98e}.warning{background:#2b2925;border:1px solid #6e6751;border-radius:9px;padding:12px;margin:18px 0}.pill{display:inline-block;background:#30383c;border-radius:16px;padding:3px 9px;font-size:12px;margin:3px 3px 3px 0}@media(max-width:760px){.grid{grid-template-columns:1fr}.wrap{padding:16px}.panel{padding:14px}h1{font-size:23px}}</style></head><body><main class="wrap"><header><div class="eyebrow">J4 / Museum Cinema / v3.9</div><h1>聲音 → 物件 → 記憶</h1><div class="mut">Sound-to-Object Recall Gate · 25 鏡 / 90 秒 / 48 kHz</div><p class="warning"><strong>DESIGN ONLY</strong> · 無實際聲音可播放、無生成、無聽測結果。所有時間與音色描述都是待驗證設計。</p></header><section class="grid"><article class="panel"><h2>聲音物件</h2><label class="mut" for="family">切換物件聲音家族</label><select id="family"></select><div id="familyDetail"></div></article><article class="panel"><h2>90 秒聲音事件軌</h2><div class="mut">依全球時碼查看，白色線為持續正弦聲的設計狀態。</div><div class="track" id="track"><div class="mark sine" style="left:.5556%;width:99.4444%"></div></div><div class="tick"><span>0s</span><span>18s</span><span>36s</span><span>54s</span><span>72s</span><span>90s</span></div><div id="cueList" style="max-height:330px;overflow:auto"></div></article></section><section class="grid" style="margin-top:18px"><article class="panel"><h2>雙次觀看：正例與控制組</h2><select id="trial"></select><div class="controls" style="margin-top:12px"><button id="tBtn" type="button">設計正例 T</button><button id="cBtn" type="button">對照 C</button><span class="tag" id="condition">T</span></div><div id="trialDetail"></div></article><article class="panel"><h2>導演審核草稿</h2><p class="mut">僅儲存本頁當前輸入；匯出不等於正式簽核。</p><label for="status">狀態</label><select id="status"><option value="NOT_RUN">NOT_RUN</option><option value="NEEDS_REVISION">NEEDS_REVISION</option><option value="READY_FOR_REAL_MEDIA_TEST">READY_FOR_REAL_MEDIA_TEST</option></select><p><label for="notes">觀察與問題</label><textarea id="notes" placeholder="例如：外套 B 的聲音是否讓觀眾誤認成 A？"></textarea></p><button id="export" type="button">匯出審核 JSON</button><p class="mut" id="msg"></p></article></section><footer class="mut" style="margin-top:22px">參考作品僅為方法研究，不代表可複製任何聲音或視覺裝置。正式生成仍需 Neon／Director／餘額與權利審核。</footer></main>
<script>const DATA=__DATA__;const byId=id=>document.getElementById(id);let fam=DATA.families[0].id;let trial=DATA.trials[0].id;let cond='T';const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const pretty=ms=>(ms/1000).toFixed(3)+' s';byId('family').innerHTML=DATA.families.map(f=>`<option value="${esc(f.id)}">${esc(f.id)}</option>`).join('');byId('trial').innerHTML=DATA.trials.map(t=>`<option value="${esc(t.id)}">${esc(t.id)} — ${esc(t.name)}</option>`).join('');function drawFamily(){const f=DATA.families.find(x=>x.id===fam);byId('familyDetail').innerHTML=`<p><span class="tag">${esc(f.kind)}</span></p><p><strong>首次：</strong>${esc(f.source.join('、'))}<br><strong>回返：</strong>${esc(f.recall.join('、')||'無')}</p><p><strong>不可變：</strong>${esc(f.invariant)}</p><p><strong>狀態轉換：</strong>${esc(f.state_change)}</p><div class="line"></div><small class="mut">當代藝術研究</small><p>${f.art.map(x=>`<span class="pill">${esc(x)}</span>`).join('')}</p>`; const evs=DATA.events.filter(e=>e.family===fam);document.querySelectorAll('#track .cue').forEach(x=>x.remove());evs.forEach(e=>{let n=document.createElement('div');n.className='mark cue';n.style.left=(100*e.start/90000)+'%';n.style.width=Math.max(.28,100*(e.end-e.start)/90000)+'%';n.title=e.shot+' '+pretty(e.start)+' '+e.note;byId('track').appendChild(n)});byId('cueList').innerHTML=evs.map(e=>`<div class="item"><strong>${esc(e.shot)} ${esc(e.event_id)}</strong> · ${pretty(e.start)}–${pretty(e.end)}<div class="mut">${esc(e.note)}</div></div>`).join('')||'<div class="mut">無局部事件</div>';}function drawTrial(){let t=DATA.trials.find(x=>x.id===trial);byId('condition').textContent=cond;byId('trialDetail').innerHTML=`<p class="mut">${esc(t.origin)} → ${esc(t.reveal)}</p><p><strong>${cond==='T'?'設計正例 T':'對照 C'}：</strong>${esc(cond==='T'?t.target:t.control)}</p><p><strong>只能改：</strong>${esc(t.only_variable)}</p><div class="line"></div><p><strong>盲測問題：</strong>${esc(t.question)}</p><small class="mut">${esc(t.art)} · ${esc(t.status)}</small>`;}byId('family').onchange=e=>{fam=e.target.value;drawFamily()};byId('trial').onchange=e=>{trial=e.target.value;cond='T';drawTrial()};byId('tBtn').onclick=()=>{cond='T';drawTrial()};byId('cBtn').onclick=()=>{cond='C';drawTrial()};byId('export').onclick=()=>{const d={version:'v3.9',review_type:'DRAFT_ONLY',family:fam,trial,condition:cond,status:byId('status').value,notes:byId('notes').value,media_status:'NOT_RENDERED',human_trial_completed:false};const blob=new Blob([JSON.stringify(d,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);let a=document.createElement('a');a.href=url;a.download='j4_v3_9_director_review_draft.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);byId('msg').textContent='已匯出審核草稿（非正式批准）。'};drawFamily();drawTrial();</script></body></html>'''.replace('__DATA__',html_data)
(OUT/'j4_sonic_object_board_v3_9.html').write_text(page)

# ZIP includes exact immutable baseline snapshots and exact original asset definitions for independent validation.
baseout=OUT/'baseline';baseout.mkdir(exist_ok=True)
for p in source_paths.values(): shutil.copy2(p,baseout/p.name)
shutil.copy2(ROOT/'j4_museum_v3_2'/'j4_object_registry_v3_2.json',baseout/'j4_object_registry_v3_2.json')

# Validate and record result. No actual audio or image creation.
import subprocess
run=subprocess.run(['python',str(OUT/'validate_v3_9.py')],capture_output=True,text=True)
report='''# J4 v3.9 verification report

- `validate_v3_9.py`: **%s** — `%s`
- media/audio content: **NONE**; all cue cards `NOT_RENDERED`.
- audience listening tests: **NOT_RUN**.
- rights/IP review: **NOT_RUN**.
- generation approval: **BLOCKED**.
- project repository modified: **NO** (only new `/mnt/data/j4_museum_v3_9/` created).
- artist recordings, recognizable sound designs or copyrighted score: **NOT USED**.

## Caveat

The waveform/timbre descriptions do not prove acoustic uniqueness, timbral match or audience memory effects. Those remain hypotheses requiring authored sounds and blinded listening tests after explicit approval.
'''%('PASS' if run.returncode==0 else 'FAIL',(run.stdout.strip() or run.stderr.strip()))
(OUT/'TEST_REPORT_v3_9.md').write_text(report)
if run.returncode: raise RuntimeError(run.stderr)
zip_path=ROOT/'j4_museum_v3_9_bundle.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
print(run.stdout.strip())
print('ZIP',zip_path,'bytes',zip_path.stat().st_size,'files',len([x for x in OUT.rglob('*') if x.is_file()]))
