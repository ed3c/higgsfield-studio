from __future__ import annotations
import csv, hashlib, html, json, os, shutil, sys, zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path('/mnt/data')
OUT=ROOT/'j4_museum_v3_2'
OUT.mkdir(exist_ok=True)
BASE=ROOT/'j4_museum_v3_1'/'baseline_j4_shots_v2_9.json'
G1=ROOT/'j4_museum_v3_1'/'j4_g1_layout_candidate_v3_1.json'
SOUND=ROOT/'j4_museum_v2_8'/'j4_sound_ir_v2_8.json'
ASSETS=ROOT/'j4_museum_v2_9'/'j4_asset_lock_registry.csv'
shots_ir=json.loads(BASE.read_text())
shots=shots_ir['shots']
g1=json.loads(G1.read_text())
sound=json.loads(SOUND.read_text())
with ASSETS.open(newline='') as f:
    existing_locks={r['asset_id']:r for r in csv.DictReader(f)}

# ROLE | identity | invariant | first interchangeable treatment | second interchangeable treatment
# All replacements are original fictional art-direction treatments, not an instruction to copy any art/film prop.
SPEC='''
acoustic_reflector|ROLE|surface that returns applause unevenly|aged oxidized perforated metal reflector|cluster of blank angled wooden acoustic panels
archive_coat_B|PHYSICAL_ANCHOR|short charcoal cotton; NO repaired left hem; NEVER A|short dark cotton archivist coat|short faded mineral-grey wool coat with straight hem
artificial_air|ROLE|visible opposing air currents sourced by cooling hardware|near-ground condensation ribbon|thin dust stream refracted by cooling exhaust
child_suitcase|PHYSICAL_ANCHOR|unmarked worn child-sized luggage; later echo in human lane|small soft canvas case with round metal clasp|small hard-sided wood-fibre case with simple corner brackets
coastal_lab|ROLE|coastal precision lab; weathered but no disaster reenactment|salt-worn optics inspection hall|coastal calibration room with frosted windows
compact_local_compute|ROLE|small unbranded local inference device, not advertising|compact brushed-aluminium computer enclosure|small charcoal passive-cooled desktop compute box
compute_facility|ROLE|distant real industrial cooling/compute hall|low desert rack house with long cooling aperture|modular computing campus along rock shelf
 delayed_reflection|MOTIF|reflection delays behind figure by editorial compositing; no physical claim|thin refracted floor line one beat behind body|faint caustic shadow contour edited to remain behind step
empty_blue_stools|ROLE|human workstations unoccupied but not evidence of forced displacement|row of faded blue stools|row of plain grey wheeled task seats
empty_chair|ROLE|empty successor boardroom seat; A garment displayed|low aged oak boardroom chair|simple dark unmarked chair with slatted back
empty_cradle|ROLE|unoccupied symbol of care, no policy statement|small unmarked wooden cradle|simple woven bassinet on stand
empty_music_stand|ROLE|empty place for absent performance|one plain old sheet-music stand|unoccupied conductor's desk without notation
empty_podium|ROLE|empty focus of collective attention; never IPO podium|recessed oval ivory platform|unmarked low mineral-stone plinth
factory_arms|ROLE|credible 5-count automated assembly motion|compact articulated pick-and-place manipulators|linear vacuum grippers with enclosed rail
fan_horn|PHYSICAL_ANCHOR|fictional human acoustic instrument with rotating fan, no protest branding|plain conical metal fan resonator|small folded copper horn with visible impeller
fictional_news_roundtable|ROLE|empty circular TV analysis desk; explicitly fictional|smoked-glass circular discussion table|laminated black cork circular studio desk
filament_bird_v1|PHYSICAL_ANCHOR|one tungsten filament, three joins, asymmetric; same between S04/S24|four-stroke angular wire creature with three joints|open-wing wire loop creature with three joints
five_chairs|ROLE|exactly five seats, three privileged by light and two dim|five unbranded low-backed discussion chairs|five plain task stools of unequal distance
folded_gloves|ROLE|human work trace with no staged tragedy|plain cotton working gloves folded|well-worn anti-static cloth mitts folded
founder_coat_A|PHYSICAL_ANCHOR|long charcoal work coat, visible LEFT hem repair; same S03/S17/S21/S24|dark woven cotton long work coat with left-hem patch|charcoal wool work coat with left-hem triangular repair
handover_key|PHYSICAL_ANCHOR|single unmarked brass handover token; one physical copy|small undecorated flat brass key|plain notched brass access slug, still graspable by two hands
human_lane|ROLE|human flow slower due to care/coordination, not detainment|low-walled pedestrian walkway|open pathway indicated by warm handrails
marcher_coat|PHYSICAL_ANCHOR|dignified unbranded muted crimson garment; one fictional actor|weathered crimson wool overcoat|long faded rust-coloured weather coat
market_bulb|DESIGN_GRAMMAR|ordinary practical tungsten-light geometry; different real bulbs across scenes|small uneven amber bulbs|aged low-voltage porcelain-mounted lamps
mesh_enclosure|ROLE|archive garment enclosed by moving physical screen|sliding metal mesh partition|hinged perforated steel enclosure
multicolour_textile|ROLE|multiple threads meet incomplete care structure|ivory/ochre/blue handwoven cloth|faded multitone fibre braid
opera_coat|PHYSICAL_ANCHOR|aged unbranded opera coat; recurring via transport|long antique charcoal opera coat|soft faded brown theatre cloak on garment rack
optical_membranes|PHYSICAL_ANCHOR|OPEN separated asymmetric translucent sheets; sparse→dense→dormant|asymmetric curved optical polymer leaves|offset rippled transparent acrylic fins, no closed tank
paper_archive|ROLE|paper records partial pressure trace not real history|stacked fibre pages showing blank impressions|folded translucent paper dossiers with indentations
paper_house_v1|DESIGN_GRAMMAR|one irregular folded roof and odd-shaped window; S11 and S22 NOT identical physical house|one-sheet ivory paper hut with diagonal roof|two-fold plain-paper shelter with offset triangular window
paper_landscape|ROLE|real handmade miniature, simultaneously recognisable as paper and coast|layered contour-paper plateau and narrow bridges|hand-cut paper archipelago with folded ridges
paper_offcut|ROLE|fibrous precursor of paper world|one folded ivory paper scrap|thin unsized drafting-paper offcut
plain_glasses|ROLE|unremarkable glasses never public-figure signature|simple rectangular reading frames|small oval unbranded reading frames
red_phone_cord|PHYSICAL_ANCHOR|one plausible red tension line between rooms, no network|one lacquered red telephone cable|single muted red fabric-coated line fixed through metal guides
sealed_lamp|ROLE|bright concentrated light requires cooling and enclosure|frosted enclosed optical source with cooling pipes|plain sealed brass lamp in transparent service cage
sensing_fibre|ROLE|energy-monitoring strands not sacred bush|three slender inspection optical fibres|small flexible sensor whiskers from conduit
shared_paper_lamps|ROLE|lights passed person to person, serviceable|hand-repaired paper lamp cylinders|small exchangeable cloth-shaded lamp modules
silicon_wafer|ROLE|unmarked technical disk handled with skill|unmarked silver silicon wafer|plain dark test wafer with no circuitry icon
single_thread_textile|ROLE|single strand reinforced through repeated folds|earth-red single-warp textile|muted terracotta braided strip
sink_water|ROLE|water responds physically to working hands|steel sink with low shallow water|enamel wash basin with small surface ripples
three_abstract_light_volumes|MOTIF|three dim abstract volumes; low-intensity reveal; no geo coding|three vertical diffused light slit volumes|three narrow soft irregular illuminated planes
translucent_glass_record|ROLE|glass preserves incomplete optical trace|flat milky glass pane with light stain|thin etched translucent resin sheet with partial imprint
transport_lane|ROLE|compact parcel machines follow physically plausible route|flush embedded floor guide|plain narrow automated cart rail
untuned_piano|PHYSICAL_ANCHOR|salt-swollen upright, delayed return key; S13/S23 recognizably same|old dark upright with oxidized strings and one sticky key|small pale timber upright with warped lower panel and slow-return key
virtual_skyline|ROLE|fictionalized Shenzhen-like silhouette in clearly synthetic projection; not real news|abstract subtropical tower panorama with projection imperfections|invented layered harbour skyline with tall slender landmark-like silhouette
warm_reflection|MOTIF|local physically caused warm reflection, NOT same photon traveling cross-scenes|thin nonuniform copper-amber caustic line|soft broken tungsten reflection across wet surface
'''
specs={}
for line in SPEC.splitlines():
    if not line.strip(): continue
    a=[p.strip() for p in line.split('|')]
    if len(a)!=5: raise ValueError(('bad spec',line,a))
    aid,cls,inv,opt1,opt2=a
    if aid.startswith(' '): aid=aid.strip()
    if aid in specs: raise ValueError('duplicate '+aid)
    specs[aid]={'identity_class':cls,'invariant':inv,'variants':[{'id':'A','description':opt1},{'id':'B','description':opt2}]}
source_assets={p for sh in shots for p in sh['props']}
assert source_assets==set(specs), (sorted(source_assets-set(specs)),sorted(set(specs)-source_assets))

# Per-shot thematic / perceptual design. Four fields: foreground, second_reading, mechanism, recontextualization/reveal; add practical method and gating separately.
SCENES='''
S01|Black contains no image|A sound already implies an unseen mechanism|ACOUSMATIC_AMBIGUITY|S25 the same tone persists after all images leave|keep actual black in editor; do not render a waveform
S02|People share a bowl and light|Warm reflection is the first form of all subsequent computational light|REFLECTION_MATCH|S24 returns human light without machinery|wet steel with visible practical lamp; the line matches S03 by cut
S03|Founder observes a physical optical apparatus|Reflection reads as a pathway no one can yet cross|TRANSIENT_ANAMORPHIC_ALIGNMENT|S17 more paths conflict; S23 the last delayed path remains|multiple open optical surfaces, one coincident line at camera only; no copied tank
S04|Metal wire is a fragile handmade object|Closure makes it momentarily read as a living bird|GESTALT_CLOSURE|S24 wire bird returns, with same three joins|wire articulation + shallow focus, avoid recognizable emblem
S05|A hand washes a bowl|Water resembles system transmission, yet maintains real life|REFRACTED_MATERIAL_ECHO|S06 hand passes a lamp, re-reading maintenance as enabling others|water ripples from touch; no impossible animation
S06|A small lamp is passed onward|The bright sealed lamp is dependent on the same maintenance world|FOREGROUND_BACKGROUND_REVERSAL|S07 shows infrastructure sustaining concentrated light|deep-space staging, slow reallocation of focus not split screen
S07|Wind and fine mist appear naturally driven|Opposing dust and cooling-flow vectors reveal artificial weather|CAUSAL_SOURCE_AMBIGUITY|S08 same airflow becomes corporate ventilation|two visible motion vectors with different genuine sources
S08|Executives imitate applause around an empty space|The absent subject becomes more influential than those present|NEGATIVE_SPACE_FIGURE|S14 applause persists even without performers|audience eyelines converge on empty plinth; no ritual screen imitation
S09|A woman raises a fan horn|Speech and mechanical noise occupy the same apparent source|AUDIOVISUAL_SOURCE_CONFLICT|S10 voice disappears but metal resonance remains|fan rotation can obscure speech, never distort face
S10|An empty work garment casts a humanlike shadow|The archived coat B is assumed to be A, but is not the same object|SHADOW_FIGURE_GROUND|S21 A reappears with left-hem repair: S10 was archive copy|B must lack LEFT patch; close mesh creates human outline without literal apparition
S11|Empty factory stools appear abandoned|Small paper house says workers built worlds beyond assigned labor|SCALE_AND_ATTENTION_SHIFT|S22 whole paper coast reveals method of the tiny paper house|first frame paper house subtle, not a fabricated machine part
S12|A red line splits an empty room|A barrier becomes a connection under changed framing|OCCLUSION_REASSIGNMENT|S15 textile, S16 route, S17 reflected line reprise connection|red cable in real guide rings, no magic travelling signal
S13|An engineer presses a damaged piano key|Wafer reflection resembles a surviving musical notation without sound|MATERIAL_ROLE_REVERSAL|S14 applause erupts for absent performance; S23 piano departs|keep audible key mechanism without musical attack
S14|Audience applauds the stage|Auditorium itself is the performer and the audience|SELF_REFLECTION_REVERSAL|S24 community gathers without choreographed applause|light reflector catches audience silhouettes, avoid copying artwork
S15|Two people work in different rhythms|From fixed viewpoint two cloth edges nearly form a single route but remain apart|ILLUSORY_CONTOUR_COMPLETION|S16 separate pathways remain physically parallel|actual gap remains visible on second viewing, no forced perfect join
S16|Machines move while people wait for each other|Two independent passages look like one corridor at depth|PERSPECTIVE_COLLAPSE|S17 split optical paths never naturally sync|camera geometry creates apparent join while floor guide remains separate
S17|Founder opens hands beneath denser optical surfaces|Multiple possible continuations of a single reflected line compete|MULTISTABLE_CONTOUR|S18 forcibly terminates all rhythms; S23 one contour remains|distinct real local light paths, do not show exact data-verse graphics
S18|Three abstract light traces show briefly in black|They appear to foreshadow chairs before the viewer knows they are seats|RETROSPECTIVE_SHAPE_MATCH|S19 three highlighted seats retroactively decode geometry|single low intensity reveal, no flash/rapid stripes
S19|Five chairs in empty synthetic news studio|Three look like predetermined authorities, two like absences|ILLUMINATED_HIERARCHY|S21 one key transfer makes chair arrangement consequential|fictional virtual backdrop; physical chairs never move
S20|Paper and glass document a missing event|Their overlap looks like one truth, slight offset proves two incomplete records|DOUBLE_REGISTERED_IMAGE|S21 key cannot reconcile whose past is represented|two authentic media with shifted recorded contours
S21|One brass key transfers between hands|A reflection briefly seems like a second key or second possessor|REFLECTION_SINGLE_OBJECT|S22 paper bridge contrasts completed authority with incomplete society|one physical key, no duplicated object, left hem patch on A in background
S22|Salaryman steadies paper bridge in clear paper landscape|The miniature coast is both breathtaking craft and empty country|SCALE_DUAL_READING|S11 tiny paper house gains tragic context, S23 founder inherits the question|both hand and paper texture visible in first frame; no cinematic fake full-scale coast
S23|Man steps forward and looks up|Refracted floor reflection holds previous body position temporarily|TIME_OFFSET_COMPOSITE|S03/S17 earlier positions recalled; S24 returns line to wet market pavement|label as deliberate time-offset composite; not a claim of physical delayed light
S24|People already hold an empty coat under rain|Human-shaped negative space yields hope without the missing person returning|FIGURE_GROUND_RECONTEXT|S04 bird becomes fragile remembered purpose; S08 applause becomes hollow|A left hem repair visible, bird same wire joins, no collective political chant
S25|Black title and sine|An unheard continuing system remains after physical film stops|AUDITORY_AFTERIMAGE|S01 was the same sound before visual world existed|editorial black, no real abrupt digital click
'''
scene_fields={}
for line in SCENES.splitlines():
    if not line.strip(): continue
    fields=[v.strip() for v in line.split('|')]
    if len(fields)!=6: raise ValueError('scene fields '+line)
    scene_fields[fields[0]]=dict(zip(['first_read','second_read','illusion','payoff','implementation'], fields[1:]))
assert set(scene_fields)=={s['id'] for s in shots}

# Main role anchored to Shot IR actual props, no invented props inserted into canonical source.
PRIMARY={
'S01':[], 'S02':['market_bulb','warm_reflection'],'S03':['optical_membranes','warm_reflection'],
'S04':['filament_bird_v1','child_suitcase'],'S05':['sink_water'],
'S06':['shared_paper_lamps','sealed_lamp'],'S07':['compute_facility','artificial_air'],
'S08':['empty_podium'],'S09':['fan_horn','marcher_coat'],'S10':['archive_coat_B','mesh_enclosure'],
'S11':['paper_house_v1','factory_arms'],'S12':['red_phone_cord'],
'S13':['untuned_piano','silicon_wafer'],'S14':['empty_music_stand','acoustic_reflector'],
'S15':['single_thread_textile','multicolour_textile'],'S16':['transport_lane','human_lane'],
'S17':['optical_membranes','warm_reflection'],'S18':['three_abstract_light_volumes'],
'S19':['five_chairs','virtual_skyline'],'S20':['paper_archive','translucent_glass_record'],
'S21':['handover_key','founder_coat_A'],'S22':['paper_landscape','paper_house_v1'],
'S23':['optical_membranes','delayed_reflection'],'S24':['founder_coat_A','filament_bird_v1'],
'S25':[]}
for s in shots:
  assert set(PRIMARY[s['id']]).issubset(set(s['props']))

# Material identity vs family identity. State chain details are per occurrence and never equivalent to timeline reorder.
STATE_OVERRIDES={
 ('founder_coat_A','S03'):'WORN_HANDS_BEHIND',('founder_coat_A','S17'):'WORN_PALMS_OPEN',('founder_coat_A','S21'):'HUNG_EMPTY_LEFT_PATCH',('founder_coat_A','S24'):'RAISED_EMPTY_LEFT_PATCH',
 ('archive_coat_B','S10'):'ARCHIVED_NO_PATCH',
 ('filament_bird_v1','S04'):'ASSEMBLED_DEPARTS',('filament_bird_v1','S24'):'RETURNS_ON_COAT',
 ('paper_house_v1','S11'):'ONE_SMALL_WORKER_PAPER_HOUSE',('paper_house_v1','S22'):'DIFFERENT_PHYSICAL_EMPTY_PAPER_HOUSE',
 ('optical_membranes','S03'):'SPARSE_OPEN',('optical_membranes','S17'):'DENSE_ASYNC',('optical_membranes','S23'):'DORMANT_OPEN',
 ('untuned_piano','S13'):'LAB_PRESSED_KEY',('untuned_piano','S23'):'DOLLY_DEPARTURE',
 ('child_suitcase','S04'):'CLOSED_MARKET',('child_suitcase','S16'):'WAITING_HUMAN_LANE',
 ('warm_reflection','S02'):'LOCAL_MARKET_WET_STEEL',('warm_reflection','S03'):'LOCAL_REFRACTED_FLOOR',('warm_reflection','S04'):'LOCAL_SUITCASE_CLASP',
 ('warm_reflection','S05'):'LOCAL_SINK_WATER',('warm_reflection','S06'):'LOCAL_TABLE',('warm_reflection','S17'):'LOCAL_MEMBRANE_FLOOR',
 ('warm_reflection','S23'):'LOCAL_DORMANT_FLOOR',('warm_reflection','S24'):'LOCAL_RAIN_PAVEMENT',
 ('market_bulb','S02'):'MARKET_LAMP_INITIAL',('market_bulb','S04'):'LOW_FOCUS_BULB',('market_bulb','S24'):'MARKET_LAMP_RETURN',
 ('opera_coat','S14'):'OPERA_WARDROBE',('opera_coat','S23'):'ON_WHEELED_RACK_DEPARTING',
 ('handover_key','S21'):'ONE_KEY_HANDOVER',
}
# A few semantic memory arcs carry deliberate revelation / retrospective cues.
ARCS=[
 {'id':'ARC_LIGHT','source':['S02','S03','S04','S05','S06','S17','S23','S24'],'asset_ids':['warm_reflection','market_bulb','optical_membranes'],'class':'SEMANTIC_TRANSFORMATION','first_belief':'Light is warmth belonging to ordinary lives','late_revision':'The institutional light is a temporary, concentrated form of what returns to common life','reveal_shot':'S24','cue':'thin broken warm reflection; each shot names its local source','constraint':'not one photon, no magic travelling beam'},
 {'id':'ARC_BIRD','source':['S04','S24'],'asset_ids':['filament_bird_v1'],'class':'SAME_PHYSICAL_OBJECT','first_belief':'wire toy seems accidental','late_revision':'fragility itself becomes a carrier of memory, not a leader resurrected','reveal_shot':'S24','cue':'one tungsten filament, asymmetric silhouette, exactly three joins','constraint':'same physical prop; no recognizable logo or bird emblem'},
 {'id':'ARC_COAT_A','source':['S03','S17','S21','S24'],'asset_ids':['founder_coat_A'],'class':'SAME_PHYSICAL_OBJECT','first_belief':'person has possession of authorship','late_revision':'empty coat can be held in common without person returning to power','reveal_shot':'S24','cue':'LEFT hem repair and consistent charcoal weave','constraint':'exact physical A coat must be used across appearances'},
 {'id':'ARC_COAT_FALSE','source':['S10','S21'],'asset_ids':['archive_coat_B','founder_coat_A'],'class':'FALSE_CONTINUITY_REVEAL','first_belief':'archived coat could be founder main garment','late_revision':'S10 was B without left repair; S21 A remained with founder','reveal_shot':'S21','cue':'A LEFT hem repair, B lacks it','constraint':'must not accidentally imply B is A'},
 {'id':'ARC_PAPER','source':['S11','S15','S20','S22'],'asset_ids':['paper_house_v1','paper_offcut','paper_archive','paper_landscape'],'class':'SHARED_FABRICATION_GRAMMAR','first_belief':'one paper house is a forgotten human pastime','late_revision':'the salaryman has built an entire paper world but cannot populate it','reveal_shot':'S22','cue':'same paper fibre and irregular roof fold, distinct actual houses','constraint':'never say the S11 house physically travelled to S22'},
 {'id':'ARC_ROUTE','source':['S12','S15','S16','S17'],'asset_ids':['red_phone_cord','single_thread_textile','multicolour_textile','transport_lane','human_lane','optical_membranes'],'class':'SHAPE_MATCH_ONLY','first_belief':'lines link positions','late_revision':'many possible connections can remain separated in time','reveal_shot':'S17','cue':'one fine line, then two paths, then offset caustic rays','constraint':'do not morph physical thread into road'},
 {'id':'ARC_PERFORMANCE','source':['S08','S14','S19','S21'],'asset_ids':['empty_podium','empty_music_stand','five_chairs','handover_key'],'class':'SEMANTIC_RECONTEXT','first_belief':'public applause creates legitimacy','late_revision':'a small unobserved key transfer has actual authority','reveal_shot':'S21','cue':'empty focal positions and hands acting without audience','constraint':'no replica IPO staging or real summit broadcast'},
 {'id':'ARC_PIANO','source':['S13','S14','S23'],'asset_ids':['untuned_piano','empty_music_stand','opera_coat'],'class':'SAME_PHYSICAL_AND_THEMATIC','first_belief':'loss of functionality equals silence','late_revision':'cultural applause can persist after creation falters; object departs quietly','reveal_shot':'S23','cue':'swollen lower timber and slow-return key; do not replay actual disaster','constraint':'S13/S23 same fictional piano; S14 is thematic, not same physical room'},
 {'id':'ARC_AUTHORITY','source':['S18','S19','S21'],'asset_ids':['three_abstract_light_volumes','five_chairs','handover_key'],'class':'PROLEPTIC_MATCH','first_belief':'abstract light volumes seem unrelated','late_revision':'their positions match the three privileged studio chair lights and then real key transfer','reveal_shot':'S21','cue':'three pools, two unlit seats, single key','constraint':'avoid any factual claim about real political event'},
 {'id':'ARC_SINE','source':['S01','S18','S25'],'asset_ids':['sine_master'],'class':'SAME_CONTINUOUS_AUDIO_OBJECT','first_belief':'low tone is a starting sound','late_revision':'tone remains after all represented people and places leave','reveal_shot':'S25','cue':'continuous phase from 0.5s, no restart','constraint':'only global loop interruption S18; sine retained'}
]

# Pair each raw prop with every appearance. User-requested swap control is an overlay; the baseline Shot IR never gets overwritten.
occurrences=defaultdict(list)
for sh in shots:
    sid=sh['id']
    for p in sh['props']:
        occurrences[p].append({'shot':sid,'state':STATE_OVERRIDES.get((p,sid),'LOCAL_'+sid),'screen_start_ms':sh['start_ms']})

asset_out=[]
for aid in sorted(source_assets):
   s=specs[aid]
   lock=existing_locks.get(aid)
   cls=s['identity_class']
   asset_out.append({'asset_id':aid,'narrative_role':aid.replace('_',' '),'identity_class':cls,
     'physical_identity_policy': 'REPLACE_CONSISTENTLY_ACROSS_OCCURRENCES' if cls=='PHYSICAL_ANCHOR' else ('SHARE_DESIGN_GRAMMAR_NOT_PHYSICAL_IDENTITY' if cls in ('DESIGN_GRAMMAR','MOTIF') else 'LOCAL_ROLE_SWAP_WITH_TRANSITION_REVIEW'),
     'invariant':s['invariant'],'default_treatment':'v3.1 baseline prompt/prop bible',
     'swap_variants':s['variants'],'occurrences':occurrences[aid],
     'locked_v3_1':bool(lock),'original_lock':lock['design_lock'] if lock else None,
     'compatibility_requirements':['preserve narrative function','preserve first-frame legibility','check adjacent optical/sonic matching','no protected reference resemblance'],
     'status':'DESIGN_OPTIONS_NOT_APPROVED'})

shot_cards=[]
for sh in shots:
    sid=sh['id']; e=scene_fields[sid]
    if sid in ('S01','S25'): gate='EDITORIAL_SOUND_ILLUSION_ONLY'
    elif sid=='S18': gate='LOW_LUMINANCE_EDITORIAL_COMPOSITE'
    else: gate='PHYSICAL_OR_EDITORIAL_PERSPECTIVE_PROPOSAL'
    arc_hits=[a['id'] for a in ARCS if sid in a['source']]
    shot_cards.append({'shot_id':sid,'title_zh':sh['title_zh'],'start_ms':sh['start_ms'],'end_ms':sh['end_ms'],
      'duration_ms':sh['duration_ms'],'original_art_reference':sh['art_reference'],
      'first_read':e['first_read'],'second_read':e['second_read'],
      'illusion_type':e['illusion'],'optical_or_audio_implementation':e['implementation'],
      'recontextualization':e['payoff'],'primary_swappable_slots':PRIMARY[sid],
      'all_swappable_slots':sh['props'],'memory_arcs':arc_hits,'diegetic_layer':('ORIGIN_MEMORY' if int(sid[1:])<=5 else 'CONTESTED_SYSTEM' if int(sid[1:])<=18 else 'AFTER_HANDOVER_OR_MEMORY'),
      'viewer_attention_limit':'one primary action or visual reveal; secondary reading can be noticed on repeat viewing',
      'shot_safety':'No resemblance to protected original artwork or film prop. No recognizable politician or branded news.',
      'generation_gate':'BLOCKED','art_review':'NOT_RUN', 'optical_proof':'NOT_RUN', 'sound_review':'NOT_RUN', 'render_review':'NOT_RUN',
      'format_constraints':{'ratio_primary':'9:16','ratio_secondary':'16:9 requires separately authored composition','fps':30},'method':gate})

# Write consumable overlay files
meta={'project':'J4 ASYNC: SUCCESSION','version':'v3.2-object-state-time-illusion-DESIGN_ONLY',
 'baseline_shots_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),
 'baseline_g1_sha256':hashlib.sha256(G1.read_bytes()).hexdigest(),
 'baseline_sound_sha256':hashlib.sha256(SOUND.read_bytes()).hexdigest(),
 'timestamp_context':'2026-11-22 Asia/Taipei', 'source_shots_count':len(shots),
 'source_duration_ms':shots[-1]['end_ms'],'source_fps':30,'status':'NOT_GENERATED_NOT_HUMAN_APPROVED',
 'governance':'Neon approval + Director estimate posted in AI Video Production Service + monthly 9000-point headroom + rights checks before any paid production.',
 'no_original_files_overwritten':True,'optical_methods_are_original_implementations_not_copies':True}
(OUT/'j4_object_registry_v3_2.json').write_text(json.dumps({'metadata':meta,'assets':asset_out},ensure_ascii=False,indent=2)+'\n')
(OUT/'j4_shot_optical_ir_v3_2.json').write_text(json.dumps({'metadata':meta,'shots':shot_cards},ensure_ascii=False,indent=2)+'\n')
(OUT/'j4_memory_arcs_v3_2.json').write_text(json.dumps({'metadata':meta,'arcs':ARCS},ensure_ascii=False,indent=2)+'\n')

# 25 shot mini table as CSV
with (OUT/'j4_25shot_dual_reading.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['shot','time_s','main_slot','illusion','first_read','second_read','later_reveal','arc_ids','review_state'])
    w.writeheader()
    for c in shot_cards:
        w.writerow(dict(shot=c['shot_id'],time_s=f"{c['start_ms']/1000:.1f}–{c['end_ms']/1000:.1f}",
         main_slot=', '.join(c['primary_swappable_slots']),illusion=c['illusion_type'],first_read=c['first_read'],second_read=c['second_read'],later_reveal=c['recontextualization'],arc_ids=', '.join(c['memory_arcs']),review_state='NOT_RUN'))

# State machine and implementation spec
spec_md='''# J4 v3.2 — Object-State / Optical Illusion Contract

## Authority boundary
This is a **design-only overlay** over v3.1. It is not an approval to render. v3.1 source artifacts are immutable inputs. G1 reviews are still `NOT_RUN` and must not be relabeled PASS.

## Object-Slot contract
Each asset record has `asset_id`, `identity_class`, `invariant`, 2 replacement treatments, scene occurrences, and a review status. All 46 Shot IR asset identifiers have replacements; choices are proposals, never approved assets.

* `PHYSICAL_ANCHOR`: same physical identity across all appearance shots. A swap propagates everywhere, including unique wear/damage/repair cues. Cannot replace independently in later shots.
* `DESIGN_GRAMMAR`: same manufacturing/form vocabulary, **not** same physical prop (paper house at S11 versus S22).
* `MOTIF`: semantic and optical continuity, but each shot must have its own physically plausible source of light, reflection, air or geometry.
* `ROLE`: scene-local functional object; can be swapped only with a reblock check and narrative equivalence.

An alternative surface must preserve the *role*. Example: replacing `handover_key` with a brass access slug is possible only if two hands can physically transfer it and the control-transfer story remains clear.

## Memory-call mechanism
Each scene carries two simultaneous possible readings and only one primary action. `first_read` must be comprehensible at 1× in the original 9:16 layout. `second_read` may depend on a later shot, but cannot require an unsupported fact claim or a preexisting movie reference.

The 90-second screen order remains unchanged. No reverse footage or time-jumps are silently added. Nonlinear storytelling occurs as **retrospective reinterpretation**: later object states change what earlier images meant.

### Strong reveals (do not dilute)
- S10 archive coat B is *not* S21/S24 physical coat A. Reveal via A's LEFT-hem repair in S21.
- S11 tiny paper home and S22 full paper shore share fold grammar, **not the same physical structure**.
- S18 three light traces precede S19 three privileged light pools; their matched geometry should be visible only on second viewing.
- S21 completes physical key transfer, while S22 paper bridge remains unfinished. One moment does not solve the other.
- S24 the empty coat receives the same fictional bird as S04; an individual does **not** return.
- S25 residual sine is the same ongoing audio object started in S01; do not restart oscillator phase.

## Optical design rules
- Use *max 1 dominant optical mechanism per shot*, plus up to one secondary sound cue.
- Prefer practical occlusion, reflection, perspective alignment, depth staging, and editorial match-cut to opaque model 'magic'.
- If delayed light is composited (S23), label it `TIME_OFFSET_COMPOSITE`: it is a deliberate temporal image operation, **not real delayed refraction**.
- Anamorphosis requires a chosen viewpoint and fragmented surfaces: fixed cameras can show a single alignment but cannot show a changing point of view unless a carefully motivated camera move is approved.
- No distinctive Rubin vase, Varini artwork, Erlich pool, Nolan spinning top, wristwatch, photographs, fictional BB pods, Capitol costumes, or real IPO podium.
- Avoid duplicate false light sources: every reflection has a local cause.
- G1 attention budget: `one primary action`; 3-second S22 shows paper world from first frame; S24 coat is already raised when clip begins.
- S18 very low-luminance reveal, no stroboscopic flashing; no rapid high-contrast geometric patterns.

## Material/time layering
- `ORIGIN_MEMORY` S01–S05: light and labour seem simple.
- `CONTESTED_SYSTEM` S06–S18: systems separate and overlap.
- `AFTER_HANDOVER_OR_MEMORY` S19–S25: later scenes reinterpret earlier objects; this is a narrative time layer, not a literal timeline jump.

## Sound lock
Preserve existing five stems, six async cycles and 63.700-second global interruption. Original sine passes through S18 to S25. S10's local cue is separate from global stop. All music and sound original; no protected recordings or signature sound design.

## Proposed gate progression
`SWAP_DRY_RUN` → `G1_Director_Review` → `G2_Originality_Review` → `G3_Physical_Illusion_Test` → `G4_Animatic_OneX_Test` → `Neon/Director/Budget` → `Render`.
All gates initially `NOT_RUN` or `BLOCKED`.
'''
(OUT/'DIRECTOR_OBJECT_STATE_CONTRACT.md').write_text(spec_md)

# Simple stand-alone HTML tool from exact overlay records, no network.
payload=json.dumps({'shots':shot_cards,'assets':asset_out,'arcs':ARCS},ensure_ascii=False).replace('</','<\\/')
web_html=r'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>J4 v3.2 Object Memory Board</title><style>
:root{font-family:system-ui,-apple-system,'Noto Sans TC',sans-serif;color-scheme:dark;background:#111317;color:#e5e8ed} body{max-width:1240px;margin:0 auto;padding:26px 18px} h1{font-size:26px;margin-bottom:8px} .sub{color:#aab3be} .grid{display:grid;grid-template-columns:280px minmax(300px,1fr);gap:20px;margin-top:20px} .panel{background:#1b1e23;border:1px solid #353943;border-radius:12px;padding:15px} label{font-size:12px;color:#b4becc;display:block;margin:12px 0 6px}select,button{background:#292d35;color:#fff;padding:10px;border-radius:8px;border:1px solid #555d6b;max-width:100%;width:100%;font-size:14px}button{cursor:pointer;margin-top:12px}button:hover{background:#383f48} .row{border-bottom:1px solid #353943;padding:12px 0} .row:last-child{border:0} .small{font-size:12px;color:#aab3be;line-height:1.55} .tag{font-size:11px;letter-spacing:.05em;color:#d8cfa8} .headline{font-weight:650;margin-bottom:4px} .warn{color:#ffbf87} .ok{color:#a2e8c2} .card{background:#252932;border-radius:10px;padding:12px;margin-top:10px} .timeline{display:grid;grid-template-columns:repeat(5,1fr);gap:4px; margin-top:12px}.timeline button{margin:0;font-size:11px;padding:8px 0}.timeline button.active{border-color:#fff;background:#5a556b}@media(max-width:760px){.grid{grid-template-columns:1fr}} </style></head><body>
<h1>J4｜物件記憶與視覺錯視板 v3.2</h1><div class="sub">25 鏡 × 46 可抽換物件 × 10 長距離回響｜純文字設計，所有生成閘口仍 BLOCKED</div>
<div class="grid"><section class="panel"><div class="headline">鏡頭選取</div><label>Shot</label><select id="shot"></select><label>物件（僅預覽，不改寫原檔）</label><select id="asset"></select><label>選擇抽換版本</label><select id="variant"></select><button id="export">匯出乾跑替換提案 JSON</button><div class="small warn" style="margin-top:12px">所有替換均需人工審核身份、局部物理與跨鏡連續性。未取得 Neon / Director 授權前，不可付費生成。</div><div class="headline" style="margin-top:20px">跳轉鏡頭</div><div id="timeline" class="timeline"></div></section><section class="panel" id="info"></section></div>
<script>const DB=__PAYLOAD__;
const S=document.getElementById('shot'),A=document.getElementById('asset'),V=document.getElementById('variant'),I=document.getElementById('info'),T=document.getElementById('timeline');
for(const s of DB.shots){let op=document.createElement('option');op.value=s.shot_id;op.textContent=`${s.shot_id} ${s.title_zh}`;S.appendChild(op);let b=document.createElement('button');b.textContent=s.shot_id;b.onclick=()=>{S.value=s.shot_id;update()};T.appendChild(b)}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function activeShot(){return DB.shots.find(s=>s.shot_id===S.value)} function activeAsset(){return DB.assets.find(a=>a.asset_id===A.value)}
function updateAssets(){const s=activeShot();let keep=A.value;A.innerHTML=''; for(const id of s.all_swappable_slots){const o=document.createElement('option');o.value=id;o.textContent=id;A.appendChild(o)}if(s.all_swappable_slots.includes(keep))A.value=keep;updateVariants()}
function updateVariants(){const a=activeAsset();V.innerHTML='';if(a){for(const v of a.swap_variants){const o=document.createElement('option');o.value=v.id;o.textContent=v.id+' · '+v.description;V.appendChild(o)}} updateInfo()}
function updateInfo(){const s=activeShot(),a=activeAsset();document.querySelectorAll('.timeline button').forEach(b=>b.classList.toggle('active',b.textContent===S.value));const arcs=DB.arcs.filter(x=>s.memory_arcs.includes(x.id));I.innerHTML=`<div class="tag">${esc(s.shot_id)} · ${(s.start_ms/1000).toFixed(1)}–${(s.end_ms/1000).toFixed(1)} s</div><h2>${esc(s.title_zh)}</h2><div class="row"><div class="small">第一眼</div>${esc(s.first_read)}</div><div class="row"><div class="small">第二層</div>${esc(s.second_read)}</div><div class="row"><div class="small">錯視機制</div><b>${esc(s.illusion_type)}</b><div class="small">${esc(s.optical_or_audio_implementation)}</div></div><div class="row"><div class="small">延遲呼喚</div>${esc(s.recontextualization)}</div><div class="row"><div class="small">物件變體</div>${a?`<b>${esc(a.asset_id)}</b> <span class="small">${esc(a.identity_class)}</span><div class="small">不可變：${esc(a.invariant)}</div><div class="card">${esc(a.swap_variants.find(v=>v.id===V.value)?.description)}</div><div class="small">影響鏡頭：${esc(a.occurrences.map(o=>o.shot).join(', '))}</div>`:'本鏡純黑／後製，不含實體物件'}</div><div class="row"><div class="small">跨鏡記憶</div>${arcs.map(x=>`<div class="card"><b>${esc(x.id)}</b><div class="small">${esc(x.first_belief)} → ${esc(x.late_revision)}<br>揭示：${esc(x.reveal_shot)}</div></div>`).join('')}</div><div class="small warn">G1 / G2 / G3 / G4：NOT_RUN　｜　任何生成：BLOCKED</div>`}
function update(){updateAssets()} S.onchange=update;A.onchange=updateVariants;V.onchange=updateInfo;
document.getElementById('export').onclick=()=>{const s=activeShot(),a=activeAsset();if(!a){alert('本鏡無物件可抽換');return}const doc={mode:'DRY_RUN_ONLY',asset:a.asset_id,variant:V.value,description:a.swap_variants.find(v=>v.id===V.value).description,shots_to_review:a.occurrences.map(o=>o.shot),identity_class:a.identity_class,review:'NOT_RUN',paid_generation:'BLOCKED'};const blob=new Blob([JSON.stringify(doc,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=`j4_swap_${a.asset_id}_${V.value}.json`;link.click();URL.revokeObjectURL(url)};
update();</script></body></html>'''
(OUT/'j4_object_memory_board_v3_2.html').write_text(web_html.replace('__PAYLOAD__',payload),encoding='utf-8')

# Handy CLI dry-run.
swap_py='''#!/usr/bin/env python3
"""J4 v3.2: propose an object variant; never call an image/model service."""
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--asset',required=True)
p.add_argument('--variant',required=True,choices=['A','B'])
p.add_argument('--out',default=None)
a=p.parse_args()
db=json.loads((HERE/'j4_object_registry_v3_2.json').read_text())
item=next((v for v in db['assets'] if v['asset_id']==a.asset),None)
if item is None: p.error('Unknown asset ID')
choice=next(v for v in item['swap_variants'] if v['id']==a.variant)
proposal={'mode':'DRY_RUN_ONLY','status':'NOT_APPROVED','paid_generation':'BLOCKED',
 'asset_id':a.asset,'variant':a.variant,'description':choice['description'],
 'required_invariant':item['invariant'],'identity_class':item['identity_class'],
 'affected_shots':[v['shot'] for v in item['occurrences']],
 'camera_and_sound_review':'REQUIRED','human_G1_G2_G3_G4':'NOT_RUN',
 'new_prompt_suffix':'Original prop treatment: '+choice['description']+'. Preserve: '+item['invariant']+'. Do not copy source imagery.',
 'note':'Append only during local editorial review; never overwrite baseline Shot IR.'}
result=json.dumps(proposal,ensure_ascii=False,indent=2)+'\\n'
if a.out: Path(a.out).write_text(result)
else:print(result)
'''
(OUT/'j4_swap_dryrun.py').write_text(swap_py)

# Markdown overview with 25-shot table and exemplar state-based prompts.
md=['# J4 Museum Cinema v3.2｜物件狀態 × 藝術錯視 × 延遲情感回響','',
'**DESIGN ONLY**。已讀取 v3.1 Shot IR、G1 layout、v2.8 Sound IR；沒有改寫基準，也沒有任何影像／音訊生成。',
'', '## 導演規則', '',
'1. 保留 25 鏡 90.000 秒及順序；讓後段的物件狀態重解讀前段，而非照搬諾蘭電影剪輯或道具。',
'2. 每件物件都可提出替代版本，但 **身份／語法／象徵** 三種類型有不同抽換限制；每個方案必須有實體性與原創距離。',
'3. 每鏡只允許一個主要錯視機制與一個主要動作；首影格負責明確資訊，第二層意義可以留給重看。',
'4. 某些物件（例如 `founder_coat_A`）必須跨鏡維持同一實體；某些（例如 `paper_house_v1`）則必須維持相似摺法但不是同一物件。',
'5. S23 延遲反射是 **受控時間合成效果**，不是聲稱實際光學會延遲 1 秒。',
'6. 保留 S18 63.700 秒唯一全局聲部停止事件與正弦波不間斷。',
'', '## 25 鏡兩層讀法','', '| 鏡 | 首眼 | 重看第二層 | 錯視技法 |','|---|---|---|---|']
for c in shot_cards: md.append(f"| {c['shot_id']} | {c['first_read']} | {c['second_read']} | `{c['illusion_type']}` |")
md.extend(['','## 強制長距離回響',''])
for a in ARCS: md.append(f"- **{a['id']}**（{', '.join(a['source'])}；解鎖 {a['reveal_shot']}）：{a['first_belief']} → {a['late_revision']}。限制：{a['constraint']}。")
md.extend(['','## 三個高價值改寫範例','',
'### S10 → S21：兩件「很像」但不是同一件的外套',
'**S10 鏡頭附加句：** `The archived short charcoal coat carries no repair on its left hem. From the fixed camera angle its shadow resembles a standing person, but the empty enclosure and bare hanger remain physically visible.`',
'**S21 鏡頭附加句：** `The actual founder work coat hangs behind the two hands. A tiny repair on the LEFT hem is now legible, proving that the archived coat seen earlier was a different specimen. One single brass key transfers between hands.`',
'**效果：** S21 讓觀眾回頭懷疑 S10 的直覺，不靠台詞。',
'', '### S11 → S22：紙屋不是同一件，而是相同制度的產物',
'**S11 附加句：** `A tiny unfinished folded paper shelter sits on an empty worker stool, its irregular roofline noticeable only after the viewer has followed the robotic line.`',
'**S22 附加句：** `The entire paper coastline is already visible on the first frame. The distant vacant paper shelter shares the same irregular roof-fold grammar as S11, but has different scale and folds. The sole action is one worker steadying a vulnerable paper bridge.`',
'**效果：** 後段把「手工技藝」升級成「一生投入的虛構世界」，不是貶低勞動者。',
'', '### S18 → S19 → S21：看不見的權力先於公開的權力',
'**S18：** `Three very dim abstract light slices briefly occupy an otherwise black field, without revealing any identities.`',
'**S19：** `Three of five empty broadcast seats acquire matching pools of soft light. The synthetic coastal skyline remains visibly fictional.`',
'**S21：** `The public light arrangement becomes a private physical transfer: a single brass key changes hands; no person observes from a stage.`',
'**效果：** 三個光形沒有新聞事件的真假宣稱，而成為往後才懂的排列線索。',
'', '## 人工 QC Gate','',
'G1: 首影格辨識；G2: 來源、實際物件與受保護 IP 距離；G3: 光線／張力／反射／視點可實作性；G4: 1× 播放下回響能否被辨認。每項均 `NOT_RUN`。',
'', '## 操作','',
'```bash\npython j4_swap_dryrun.py --asset paper_house_v1 --variant B\npython validate_v3_2.py\n```','',
'本工程包只會輸出替換提案，不會生成圖片／影片、存取 Higgsfield 或授權製作。'])
(OUT/'DIRECTOR_REVIEW_v3_2.md').write_text('\n'.join(md)+'\n')

# deterministic validator; outputs required evidence without claiming media/rights approval.
validator='''#!/usr/bin/env python3
import json,hashlib,sys
from collections import defaultdict
from pathlib import Path
P=Path(__file__).resolve().parent
bs=json.loads((P/'baseline_shots_v3_1.json').read_text())
rr=json.loads((P/'j4_object_registry_v3_2.json').read_text())
ss=json.loads((P/'j4_shot_optical_ir_v3_2.json').read_text())
ma=json.loads((P/'j4_memory_arcs_v3_2.json').read_text())
assert len(bs['shots'])==len(ss['shots'])==25
assert bs['shots'][-1]['end_ms']==90000
assert sum(x['duration_ms'] for x in bs['shots'])==90000
assert all(x['start_ms']==(bs['shots'][i-1]['end_ms'] if i else 0) for i,x in enumerate(bs['shots']))
assert all(x['end_ms']-x['start_ms']==x['duration_ms'] for x in bs['shots'])
assert all((x['start_ms']*30)%1000==0 and (x['end_ms']*30)%1000==0 for x in bs['shots'])
ids={x['asset_id'] for x in rr['assets']}; baseline_ids={p for x in bs['shots'] for p in x['props']}
assert len(ids)==46 and ids==baseline_ids
assert len(set(x['shot_id'] for x in ss['shots']))==25
assert all(len(x['swap_variants'])>=2 for x in rr['assets'])
assert all(x['art_review']=='NOT_RUN' and x['generation_gate']=='BLOCKED' for x in ss['shots'])
assert all(set(x['all_swappable_slots']).issubset(ids) for x in ss['shots'])
for a in rr['assets']:
 expected=[x['id'] for x in bs['shots'] if a['asset_id'] in x['props']]
 assert expected==[v['shot'] for v in a['occurrences']],a['asset_id']
 assert len({v['shot'] for v in a['occurrences']})==len(a['occurrences'])
for arc in ma['arcs']:
 assert set(arc['source']).issubset({x['id'] for x in bs['shots']})
 assert arc['reveal_shot'] in arc['source']
 assert set(arc['asset_ids']).issubset(ids|{'sine_master'})
coats={a['asset_id']:a for a in rr['assets'] if 'coat' in a['asset_id']}
assert [o['shot'] for o in coats['founder_coat_A']['occurrences']]==['S03','S17','S21','S24']
assert [o['shot'] for o in coats['archive_coat_B']['occurrences']]==['S10']
assert next(a for a in rr['assets'] if a['asset_id']=='paper_house_v1')['physical_identity_policy']=='SHARE_DESIGN_GRAMMAR_NOT_PHYSICAL_IDENTITY'
assert next(x for x in ss['shots'] if x['shot_id']=='S18')['method']=='LOW_LUMINANCE_EDITORIAL_COMPOSITE'
assert next(x for x in ss['shots'] if x['shot_id']=='S23')['illusion_type']=='TIME_OFFSET_COMPOSITE'
print('PASS: 25 shots; 90.000s; 2700 frames @30fps; 46 swappable slots; 10 memory arcs; review NOT_RUN; paid gate BLOCKED')
'''
(OUT/'validate_v3_2.py').write_text(validator)
shutil.copy2(BASE,OUT/'baseline_shots_v3_1.json')
shutil.copy2(G1,OUT/'baseline_g1_layout_v3_1.json')
shutil.copy2(SOUND,OUT/'baseline_sound_v2_8.json')

# Use built-ins only: quick test
import subprocess
r=subprocess.run([sys.executable,str(OUT/'validate_v3_2.py')],capture_output=True,text=True)
if r.returncode:
    print('validator failure',r.stdout,r.stderr);raise RuntimeError('failed validator')
print(r.stdout.strip())
# Generate example dryrun to a *file* (not approval)
r=subprocess.run([sys.executable,str(OUT/'j4_swap_dryrun.py'),'--asset','founder_coat_A','--variant','B','--out',str(OUT/'example_swap_coat_A_B_DRYRUN.json')],capture_output=True,text=True)
if r.returncode:raise RuntimeError(r.stderr)
# manifest
manifest={'version':'v3.2','generated_from':'v3.1 actual source files','shot_count':25,'duration_ms':90000,'fps':30,'swappable_shot_props':46,'memory_arcs':10,'unique_illusion_designs':len(set(x['illusion_type'] for x in shot_cards)),'generated_media':0,'paid_credits':0,'review_state':'NOT_RUN','authorization':'BLOCKED','source_hash':meta['baseline_shots_sha256'],'files':sorted(p.name for p in OUT.iterdir() if p.is_file())}
(OUT/'manifest_v3_2.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
ZIP=ROOT/'j4_museum_v3_2_bundle.zip'
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file():z.write(p,arcname='j4_museum_v3_2/'+p.name)
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
print('FILES',len(list(OUT.iterdir())),'ZIP',ZIP.stat().st_size)
