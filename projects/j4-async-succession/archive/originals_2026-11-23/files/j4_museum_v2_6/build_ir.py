from pathlib import Path
import json,csv,math,re,textwrap,zipfile
D=Path('/mnt/data/j4_museum_v2_6')
MASTER_IMAGE = '''J4 ASYNC: SUCCESSION — ORIGINAL MUSEUM CINEMA
9:16 vertical fictional narrative art film; centre-safe composition for alternate widescreen.
Physical causality before visual spectacle. Human gestures are restrained and dignified. Camera is generally locked; 24mm architectural, 35mm relational, 50–85mm tactile. Cold mineral grey, aged ivory, charcoal, oxidised metal, weathered tungsten. Authentic water, paper, fabric, glass, optical refraction and analogue grain. Silence and negative space are constructive elements. Keep characters and recurring objects consistent with Character/Prop Bible. Never replicate uploaded image compositions, referenced art installations, film/game characters, actual politicians, identifiable real faces, brands, trademarks or real news broadcast formats. No readable in-frame writing; all titles/captions in post. No pseudo-technical floating code, choreographed spectacle, dystopian explosions or gratuitous strobes. Each shot should stand alone as a plausible gallery installation frame while carrying a causal trace from its adjacent shots.'''
MASTER_SOUND = '''ORIGINAL SOUND PRINCIPLE: separate five stems (sine/electrical constant; nature/water/air; tactile labour and machines; sparse original pitched motif; voice/space). Spatial location, phase-continuous non-synchronised cycles and natural decay matter more than a conventional score. Never copy a Ryuichi Sakamoto melody, recording, chord sequence, sample or distinctive sonic signature, nor any contemporary-art installation audio. No artist names in audio-generation prompts. Distinct ambience can cross picture cuts; preserve the phase of an active/gated loop. The only intentional global interruption is at 63.700 s (S18); the sine survives. S10 deliberately interrupts one unfinished piano-like tail. Final digital boundary at 90 s must be de-clicked.'''
NEGATIVE = 'real person, celebrity, politician likeness, film/game character, IP costume, actual stock exchange or television network, company brand, logo, trademark, watermark, political flags and symbols, copied sculpture, copied art installation, captions, sign text, floating UI, rapid flashing, gore, weapons, overacting, bad hands, extra fingers, morphing architecture, unreal fluid dynamics, default sci-fi neon'
shots=[]
def add(n,a,b,zh,en,artist,work,method,image,motion,sound,prop='',characters='',prev='',nxt='',contest='',mode='video'):
    shots.append(dict(id=f'S{n:02d}',start_ms=round(a*1000),end_ms=round(b*1000),duration_ms=round((b-a)*1000),act=1 if a<20 else (2 if a<65 else 3),title_zh=zh,title_en=en,
      art_reference=dict(artist=artist,work=work,transfer_method=method,do_not_copy=True),
      generation_mode=mode, image_prompt=textwrap.dedent(image).strip(),motion_prompt=textwrap.dedent(motion).strip(),sound_prompt=textwrap.dedent(sound).strip(),
      global_image_lock_ref='MASTER_IMAGE_V2_6', global_sound_lock_ref='MASTER_SOUND_V2_6',negative_prompt_ref='GLOBAL_NEGATIVE_V2_6',
      props=[s.strip() for s in prop.split(',') if s.strip()], characters=[s.strip() for s in characters.split(',') if s.strip()],
      in_transition=prev,out_transition=nxt,contest_override=contest or 'Use fully fictional, non-identifiable subjects; copyright/IP/legal review required. Not a guaranteed contest eligibility determination.',
      review_state='TEXT_DRAFT_NORMALIZED_NOT_GENERATED',generation_recipe=(dict(render_provider='editor',billable_generation=False,planned_takes=0) if mode=='editorial' else dict(render_provider='Cinema Studio 4.0 720p candidate',minimum_billable_ms=5000,planned_takes=2,render_then_trim=True,portfolio_genjutsu_plate_candidate=(n in [3,17,23]),contest_requires_original_generation=True))))

add(1,0,3,'第一束光之前','Before the First Light','Ryoji Ikeda','test pattern [nº1] (2008)','Signal precedes image; use no original optical patterns.',
'''EDITOR ONLY. Pure absolute-black frame, with optional short fictional-allegory disclaimer composed only in editing software. No grain, particles, glowing borders, interface, or visible apparatus. The darkness is the withheld image, not a depiction of space.''',
'''0.0–0.5 absolute black and silence. 0.5–1.5 introduce low original sine. 1.5–2.5 optional tiny disclaimer; clear it before 3.0. Keep black. Human market ambience enters just before the next picture cut.''',
'''Start a continuously phase-stable sine at 0.500 s; layer distant utensils, room air and indistinct conversation just before 3.000 s. No melody, impact, or electronic startup sound.''',prev='Film opens in acoustic near-zero',nxt='Market audio J-cut by ~0.3 s into S02',mode='editorial')
add(2,3,7,'被分享的光','A Light Shared','Rirkrit Tiravanija','untitled 1990 (pad thai) (1990)','Human encounter as the artwork; do not recreate original participation scene.',
'''A small, physically real fictional Taiwan-style night market on a humid evening. An adult vendor cooks quietly under worn awnings and irregular tungsten lamps; a bowl passes between two customers; a child rests asleep against a parent. Wet steel, steam, plastic stools and modest food stalls form layers of ordinary shared life. The camera sees relationships, not spectacular neon tourism. 24mm at human height, subdued amber and charcoal, slight moisture and authentic wear. Fictional non-identifiable people; no market signs or text.''',
'''0–1.2 vendor makes one small cooking gesture; 1.2–2.4 a bowl passes hand to hand; 2.4–3.3 steam briefly crosses a lamp; 3.3–4.0 a warm reflection travels across wet steel. Minimal forward move, horizon locked.''',
'''Seven-second market ambience cycle begins at absolute 3.0 s: bowls, food friction, steps and indistinct conversation. Phase continues across cuts while active. Persistent low sine remains beneath; no metered percussion.''',prop='market_bulb, warm_reflection',characters='market_ensemble',prev='Black opens on human activity',nxt='Warm water-light match-cuts into S03 cold optical reflection')
add(3,7,12,'光的源頭','The Source','Ryuichi Sakamoto × Shiro Takatani','water state 1 (2013)','Water-light timing and physical response; explicitly not the original water installation.',
'''Vast silent mineral-stone chamber. Several thin, curved translucent optical membranes hang independently at irregular angles, openly spaced, with accumulating condensation. A hidden pale white source refracts through droplets into fractured floor caustics. One fictional adult founder figure appears tiny, from behind, wearing a plain charcoal work coat, hands loosely clasped. A single warm reflection touches a shoulder. No rectangular suspended water tank, cube, gallery replica, hologram or hardware billboard. 35mm locked, severe negative space and precise optical physics.''',
'''0–1.5 figure still as droplets form; 1.5–3.5 one droplet descends and its floor reflection follows with slight delay; 3.5–4.5 light reaches the person's shadow; 4.5–5.0 a warm thread appears. Cut before it stabilises.''',
'''Market ambience retreats as a distant acoustic memory; introduce isolated soft original piano tone and low room resonance. Separate droplet contact from delayed reflection cue. Leave acoustic decay crossing into S04.''',prop='optical_membranes, warm_reflection, founder_coat_A',characters='founder',prev='S02 reflected bulb becomes refraction',nxt='The warm light thread becomes S04 delicate filament')
add(4,12,16,'脆弱的離開','Fragile Departure','Studio DRIFT','Fragile Future III','Fragility of handmade electronic life; no copying dandelion LEDs.',
'''In a dim corner beneath the market practicals, a worn 1970s-style unmarked child suitcase sits closed. An ordinary bulb hangs above; beside it a tiny irregular bird-like original wire object, handmade from sparse metal curves, with one weak incandescent filament. No ornamental wing pattern or emblem silhouette. Condensation softens the glass and a warm glint touches the suitcase clasp. 85mm macro, extraordinarily sparse material realism, handmade imperfections; avoid logo-bird resemblance or magical creature treatment.''',
'''0–1.1 tiny filament glows; 1.1–2.2 warm air gently moves the wire; 2.2–3.2 its nearly invisible support allows slight lift/rotation; 3.2–4.0 object moves just beyond frame. Do not show transformative wings or flight spectacle.''',
'''Continue S03 decay; add minute electrical crackle and wire resonance; place second isolated original motif pitch. Sink water from S05 begins underneath final tail.''',prop='filament_bird_v1, child_suitcase, market_bulb',prev='S03 narrow warm reflection becomes heated wire',nxt='Wire leaves frame; water sound reveals diner sink')
add(5,16,20,'維持世界的人','Maintenance of the World','Mierle Laderman Ukeles','Washing/Tracks/Maintenance: Inside (1973)','Reveal dignity of maintenance work; not original performance documentation.',
'''Fictional unbranded late-night roadside restaurant back kitchen. Tactile close view of anonymous adult gloved hands washing a ceramic bowl in a worn stainless sink; a clean stack and a few remaining used bowls imply an endless necessary task. Cool fluorescent water ripples reflect a small warm dining-room glow and a fractured linear highlight associated with S03. Real labour, neither heroic nor degrading; realistic wet metal, ceramic and gloves; 50mm static, no Denny’s or biographical ping-pong detail.''',
'''0–1.0 lift bowl; 1.0–2.1 turn once as water drains; 2.1–3.1 place it onto clean stack; 3.1–4.0 hands return and the water continues moving. One locked camera.''',
'''Start eleven-second maintenance ambience phase at 16 s: running water, ceramic on metal, gloves, ventilation. Third isolated motif tone enters very softly. Let ripple decay cross into S06.''',prop='sink_water, warm_reflection',characters='dishwasher_hands',prev='S04 fine electrical sound thins into water',nxt='Hand performs maintenance; S06 hand passes maintained lamp')
add(6,20,24,'使用光的權利','The Right to Light','Felix Gonzalez-Torres','“Untitled” (Placebo) (1991)','Participation, take-and-renew; no candy pile or installation form.',
'''Fictional communal illumination workshop. At a worn worktable, fictional adults repair small individually patched paper-covered electric lamps and pass a single live lamp module between them. In deep background, behind thick glass, stands a precise sealed brighter technical light source with condensation along cooling surfaces. Both systems give useful light, but have distinct access and maintenance rules. Depth composition, not a simplistic split-screen. 35mm, aged paper, brass, mineral grey, restrained warm/cold light. No branded hardware or moral propaganda.''',
'''0–1.0 one person finishes repair; 1.0–2.0 passes module; 2.0–3.1 second person installs module in a dark paper lamp; 3.1–4.0 it glows gently, while sealed apparatus remains steady. Locked camera.''',
'''Start five-second compute/cooling phase at 20 s, maintained thereafter without phase reset. Foreground paper and contacts are irregular, background cooling a steady note. Fourth fragmentary original motif note may appear; no resolved tune.''',prop='shared_paper_lamps, sealed_lamp, warm_reflection',characters='workshop_adults',prev='Washing hands become lamp-passing hands',nxt='Technical cooling air becomes S07 artificial weather')
add(7,24,28,'人造氣候','A Manufactured Climate','Olafur Eliasson','The weather project (2003)','Manufactured atmosphere; do not recreate artificial sun/mirror.',
'''Wide fictional high-desert compute research site in blue hour. Low elongated modules and cooling apertures track the edge of a mineral basin; small environmental sensor fibres emerge from a buried conduit, with weak travelling indicator points. Dust moves with the natural wind, while a slim condensation ribbon moves in a different direction under cooling exhaust. Tiny isolated technician far away; physically credible energy, water and weather dependence. 24mm static and desaturated, vast negative space. No sun disc, Babel tower, burning bush, flags or religious reference.''',
'''0–1.1 dust drifts; 1.1–2.2 artificial moist air emerges close to floor; 2.2–3.2 faint point travels within a sensor fibre; 3.2–4.0 cooling airflow dominates. No camera motion or storm spectacle.''',
'''Start separate thirteen-second environmental phase at 24 s. Cool-air noise from S06 becomes ambiguous desert wind; weak structural vibration, not epic desert score. Air continues as ventilation under S08.''',prop='compute_facility, sensing_fibre, artificial_air',prev='Cooling sound reveals landscape scale',nxt='Exterior airflow becomes S08 institutional ventilation')
add(8,28,32,'共識製造機','The Consent Machine','Tino Sehgal','This Situation (2007)','Social consensus produced by participant behaviour; no recreation of the performance.',
'''An austere fictional institutional rehearsal chamber, not a stock exchange. Narrow isolated acoustic alcoves hold different fictional adults in plain formal garments facing an empty low oval presentation floor. A few 1970s broadcast controls appear beyond smoked panels. One person is poised to clap; others wait, without knowing what is being celebrated. Muted ivory stone, charcoal, isolated amber lamps, 35mm fixed architectural framing, no actual podium/ceremonial bell, brand, ticker, or group photo.''',
'''0–0.9 one dry clap; 0.9–2.0 two delayed responses; 2.0–3.2 others join but do not fully synchronise; 3.2–4.0 one person remains silent briefly. No smiling or celebration. Locked camera.''',
'''Exterior S07 wind becomes enclosed ventilation. Separate human claps enter at slightly different times and spatial locations, with faint unresolved low note. Last clap decay passes into S09 fan/urban sound.''',prop='empty_podium',characters='ceremony_ensemble',prev='Exterior air turns into rehearsal-room HVAC',nxt="Institutional applause becomes individual's struggling voice")
add(9,32,35.5,'無人接收的頻率','The Unheard Frequency','Tania Bruguera','Tatlin’s Whisper #6 (Havana Version) (2009)','Speech as a spatial right; no direct staging or political event replay.',
'''Fictional adult woman in a weathered deep-crimson coat under an urban concrete overhang on a wet night. She holds an original handmade acoustic horn integrated with a small computer cooling-fan housing; face wholly fictional and unrecognizable. A few distant pedestrians, one momentarily listening, occupy a quiet street without banners. 50mm human-level, faded sodium reflections on damp concrete, restrained dignity and uncertainty. No protest logos or recognizable megaphone style.''',
'''0–0.8 rain edges move; 0.8–1.7 woman raises device as fan starts; 1.7–2.7 lips move quietly and wind touches hair; 2.7–3.5 voice increasingly obscured by fan. No shouting or slogans.''',
'''S08 last clap echoes into rain and small fan whir; original fictional voice becomes indistinct under rotating air noise. Metallic fan resonance leads into S10 mesh.''',prop='marcher_coat, fan_horn',characters='marcher',prev='Social unison cuts to solitary speech',nxt='Fan housing metal contact becomes S10 sliding enclosure')
add(10,35.5,39,'缺席的創造者','The Absent Author','Doris Salcedo','Atrabilious (1992–93)','Absence through objects, without equating business exit with violence victims.',
'''Institutional storage corridor. Mesh steel enclosure contains an empty plain charcoal archival work coat, variant B (shorter cut and distinctly different cuff wear from founder coat A), and ordinary undistinguished glasses. Warm lamp over aged textile; one large blurred coat shadow falls across cold wall. No portraits, ID labels, political or celebrity cues. This is an archive copy of an earlier garment, NOT the founder coat that will be worn in S17 and passed through S21. 50mm fixed, severe quiet geometry.''',
'''0–0.9 still; 0.9–1.8 gloved hand slides mesh door; 1.8–2.7 mesh shadow crosses textile; 2.7–3.5 door closes and one sleeve moves in displaced air. No ghost effect.''',
'''Thin metallic residue from S09; quiet mesh slide, fabric and small door contact. Intentional interruption of any unfinished short piano-like tail here (exception to natural decay). Metallic contact becomes S11 actuator.''',prop='archive_coat_B, plain_glasses, mesh_enclosure',characters='archive_hand',prev='Individual voice leaves room; only archived object remains',nxt='Sliding steel becomes robotic actuator')
add(11,39,43,'沒有交班的工廠','The Factory Without a Shift','Cao Fei','Whose Utopia (2006)','Worker dreams beyond factory standardization; do not reproduce the film.',
'''Vast fictional electronics line with precise robotic arms and one-point perspective. Row of empty blue stools holds folded cotton gloves; on one stool is a tiny unfinished folded paper house (PAPER_HOUSE_ID), with pencil and offcut. No evidence of panic—work may have moved elsewhere. Cold ventilation bead slowly forms above polished concrete; muted mechanical indicator, restrained mineral tones and credible manufacturing detail. 24mm low human height. Human hopes are not described as obsolete.''',
'''0–1.0 robotic joints cycle; 1.0–2.1 assembly repeats as droplet gathers; 2.1–3.0 droplet falls; 3.0–4.0 subtle lateral camera move reveals paper house. No shutdown or alarm.''',
'''Reuse five-second compute phase from S06, without reset. Convey actuators, belt and air as layered physically timed sounds; droplet falls outside machine rhythm. Thin overtone moves into S12.''',prop='paper_house_v1, empty_blue_stools, folded_gloves, factory_arms',prev='Storage mesh contact becomes actuator sound',nxt='Mechanical high overtone becomes tensioned telephone cable')
add(12,43,46,'看不見的協議','The Invisible Agreement','Chiharu Shiota','Uncertain Journey (2016)','Invisible human links visualized via one line; no red-thread nets or boats.',
'''Empty narrow private institutional dining chamber. Two dark wood tables sit far apart. An aged muted-red lacquer telephone receiver rests on one, with one taut, physically plausible red cable crossing open floor through discrete guide loops to a destination outside frame. Unused napkin, cold teacup, one thin cable shadow, cool high-window light. 50mm static architectural emptiness. No companion character, sex/ethnic stereotype, real political meeting, dense yarn installation, or lettering.''',
'''0–0.8 still; 0.8–1.7 unseen tension pulls receiver a few millimetres; 1.7–2.4 a small vibration travels along cable; 2.4–3.0 receiver stops, cable residual movement continues.''',
'''S11 high metallic resonance leads into dry cord friction and near-empty room. Cable's small inharmonic tail is transformed by editing into S13 piano mechanism, not thriller score.''',prop='red_phone_cord',prev='Machine vibration becomes private cable tension',nxt='Cable resonance becomes untuned piano mechanism')
add(13,46,50,'失去音準的文明','The Untuned','Ryuichi Sakamoto × Shiro Takatani','IS YOUR TIME (2017)','Nature and time re-tune a technical object; no literal tsunami instrument replica.',
'''Fictional coastal precision-engineering test hall. A structurally elegant upright piano has slowly swollen at its lower woodwork through years of salt air; its aged keys face a dormant optical inspection bench. Dignified fictional elderly technician in unbranded pale cleanroom garment holds one silicon wafer; its reflected circle crosses the keys. A single tiny indicator remains alive among dormant instruments. Sea visible through tall windows, no ruined city or explicit natural-disaster reconstruction. 35mm cold mineral daylight, subtle salt marks, authentic restraint.''',
'''0–1.2 engineer tilts wafer; 1.2–2.4 presses a key that fails to return fully; 2.4–3.4 mechanism shifts faintly; 3.4–4.0 hand still as sea air moves a small strand. Locked camera.''',
'''Original wind, swollen wood, quiet key mechanism and unstable overtone, NOT a recognizable piano melody. Mechanical after-sound carries into S14 applause—a deliberate contrast between failed tone and abundant acclaim.''',prop='untuned_piano, silicon_wafer, coastal_lab',characters='lithographer',prev='Cable vibration becomes imperfect string overtone',nxt='Absent piano note juxtaposed with abundant applause')
add(14,50,53,'最後的喝采','The Last Ovation','Janet Cardiff × George Bures Miller','The Murder of Crows (2008)','Speakerless spatial narrative via sound; no borrowed 98-speaker arrangement or audio.',
'''View from abandoned stage into monumental fictional old opera theatre: gilded private boxes with sparse composed spectators, weathered velvet, oxidized metal and an empty orchestra pit. A solitary vacant music stand receives warm spotlight; a tarnished irregular acoustic reflector distorts light in the upper wall without becoming a literal mirror of an existing artwork. Some fictional audience members begin applauding despite no performance. 35mm fixed architectural view, quiet beautiful decay, no recognizable Hunger Games Capitol design, characters, or real opera venue.''',
'''0–0.8 silent empty music stand; 0.8–1.8 applause starts in separated boxes, including audio positions with no visible people; 1.8–2.5 clapping gestures lessen as reverberation dominates; 2.5–3.0 chandelier dims fractionally. No sudden horror effect.''',
'''S13 imperfect key resonance underneath location-distant original claps, independently located balcony/empty-stage responses. Room decay outlasts bodies. Acoustic claps crossfade into S15 wood and textile shuttle sounds.''',prop='opera_coat, empty_music_stand, acoustic_reflector',characters='opera_audience',prev='Piano cannot properly sound, but the audience applauds',nxt='Applause tail is reinterpreted as weaving shuttle contact')
add(15,53,57,'兩種編織未來的方法','Two Ways of Weaving','Chiharu Shiota','The Key in the Hand (2015)','Care and memory via unfinished joining; no giant thread web/key boats.',
'''Two fictional adult women in quiet conservation workshop work separately at a single long table. One reinforces muted terracotta fabric with one strand; the other joins several natural fibres in ivory, ochre, faded blue and mineral grey. Both incomplete pieces approach a small worn empty wooden cradle but do not meet. Fine material tension and hand skill; a tiny folded paper offcut previews S22. 50mm locked, warm sliver at cradle, natural realism. No national/ethnic symbols, birth-policy slogan or imitation of red-thread installation.''',
'''0–0.9 left hand completes one small thread pass; 0.9–1.8 right hand works separately; 1.8–2.9 independent movement with air lifting one loose strand; 2.9–4.0 textiles remain separated by a narrow gap. Locked camera.''',
'''S14 applause tail becomes textile and wood contact. Two internally different phrases can loosely refer to 7 and 13 second phases, but use local clipped fragments only. Do not restart global sound loops on shot boundary.''',prop='single_thread_textile, multicolour_textile, empty_cradle, paper_offcut',characters='weaver_left, weaver_right',prev='Cultural applause becomes real material work',nxt='Two lines of textile match-cut to two transit paths')
add(16,57,60.5,'平行通道','Parallel Passage','Rafael Lozano-Hemmer','Border Tuner (2019)','Human connection needs consent/participation; no existing searchlight composition.',
'''Fictional modern logistics/transit hall with two parallel open routes. One floor-guided lane conveys compact unbranded non-humanoid autonomous parcel carriers at stable intervals. In adjacent human corridor, a few fictional adult travellers carry bags and wait for one another; one holds an old suitcase linked to S04, another studies a blank wayfinding panel. Nobody is stopped by state agents. Both lanes tend toward same distant opening but do not merge on-screen. 35mm locked, worn stone, pale ceiling strips. No borders, passports, visa claims, flags or real checkpoint.''',
'''0–0.8 one carrier passes; 0.8–1.8 second carrier follows while human pauses for companion; 1.8–2.8 suitcase handle is adjusted; 2.8–3.5 two travellers acknowledge and start walking together. No confrontation.''',
'''Transform textile phases into two kinetic pathways: mechanical motor regularity vs footsteps/breath/suitcase-wheels variation. Human-route ambience may reference eleven-second family while current phase continues. All layers accumulate into S17.''',prop='child_suitcase, transport_lane, human_lane',characters='travellers',prev='Thread lines become two routes',nxt='Ceiling route strips become light reflections')
add(17,60.5,63.7,'資訊的重量','The Weight of Information','Ryoji Ikeda','data-verse 1 (2019)','Scale and overload via physical optics and independent audio, not data graphics.',
'''Return to S03 mineral-stone chamber, same fictional founder, same plain charcoal work coat A. Curved open optical membranes have expanded to layers and droplets react at independent rates; fractured cold reflections converge with small warm market-memory trace. Founder seen from behind opens both palms cautiously, no worship or superhero pose. Light appears complex only through real moisture/surface interactions, not codes or holograms. 35mm static, profound negative space, original optical installation distinct from uploaded water-tank reference.''',
'''0–0.7 weak reflections; 0.7–1.5 hands open as line approaches; 1.5–2.4 delayed second line arrives; 2.4–3.0 brightness becomes irregular; 3.0–3.2 subtle instability, hard cut. No flash barrage.''',
'''Highest concurrent sound density, not highest loudness: extant 7/11/5/13/19/17 second phase families masked/unmasked independently, never restart. Incomplete original motif fragments and sine below. At 63.700 s stop every independent environmental/tonal loop on single master cut, not by waiting for alignment.''',prop='optical_membranes, founder_coat_A, warm_reflection',characters='founder',prev='Transit light routes become delayed membrane caustics',nxt='All active non-sine loops forced off at 63.700s')
add(18,63.7,65,'被強制的同步','The Forced Consensus','Carsten Nicolai (alva noto)','unidisplay (2011/2012)','Exact negative-space perception and interruption; no monochrome pattern/installation.',
'''EDITORIAL COMPOSITE rather than paid video generation. Near-black abstract original space, briefly revealing three soft low-intensity vertical light volumes at differing depths: warm ivory, neutral mineral-white and silver-grey. No people, chess kings, city, flags, national colours, grid, high-frequency flashing or throne. The volumes hint at a future unequal three-seat configuration in S19. Main image remains almost completely black.''',
'''0.00–0.25 black; 0.25–0.40 first low-intensity reveal; 0.40–0.83 black; 0.83–1.00 second dimmer reveal; 1.00–1.30 black. An accessibility alternative uses one gentle fade instead of two reveals. Cut to S19 at exactly 65.000s.''',
'''At 63.700s simultaneously stop six phase-independent sound families with micro-declick envelopes; do NOT align their phases. Continuous sine continues from S01. No impact, bass drop or sound effect for reveals. At 65s allow new quiet S19 electronics ambience.''',prop='three_abstract_light_volumes',prev='Forced interruption, not natural 7/11/5/13/19/17s alignment',nxt='Match three light volumes to S19 illuminated chair positions',mode='editorial')
add(19,65,69,'峰會前的放送','The Broadcast Before the Summit','Hito Steyerl','Factory of the Sun (2015)','Media constructs reality; no blue-grid/game/video replication.',
'''Entirely fictional empty late-night news-analysis studio. Smoked glass/aluminium circular discussion table with five unoccupied chairs, three near camera-axis in pale shafts and two dim at periphery. Behind, curved virtual scene shows a deliberate 3D reconstruction of Shenzhen Futian city skyline at blue hour, with obvious mild projected depth flaws and analogue noise—not a real broadcast or event. Obsolete 1970s control desk behind partition; delayed water-reflection echo along table. 35mm near symmetry, cold mineral palette, no presenter, network graphic, political leader or headline. Contest version replaces Shenzhen with a wholly fictional coastal technology city.''',
'''0–0.7 projection resolves from dark; 0.7–1.8 three pools of light rise; 1.8–3.1 skyline reflection moves a fraction later than architecture; 3.1–3.7 projected image freezes gently; 3.7–4.0 chair distribution remains unequal. No seats move, people enter or announcement occurs.''',
'''Sine persists; faint broadcast electronics and two soft original unresolved piano events, with no city ambience. Projection freeze briefly gates noise; move into close paper/glass room sound S20. No fake newscast ident.''',prop='fictional_news_roundtable, five_chairs, virtual_skyline',prev='Three S18 light volumes become chair pool locations',nxt="Broadcast's constructed image becomes two incompletely preserved records",contest='Replace Shenzhen with an entirely fictional unnamed coastal technology city. Remove recognizable topography and any interpretation of actual political events; do not represent as true news.')
add(20,69,72.5,'缺席者的檔案','The Archive of Absence','Walid Raad','The Atlas Group (1989–2004)','Fiction/archive ambiguity without copying war documents or testimonies.',
'''Quiet fictional archive conservation room: at one aged oak table, left an opened folded paper archive bearing physical impressions without legible text; right a translucent upright glass pane with a different faint light-sensitive imprint. Only two careful anonymous archivists' hands visible, holding paper and glass. The light-reflection trace resembles the paper impression but never exactly matches. 50mm balanced frame, subdued warm and mineral-white light, no candles, religious ritual, cultural stereotyping, war documents or actual historical photos.''',
'''0–0.9 left hand opens paper; 0.9–1.8 glass takes reflection; 1.8–2.8 reflection crosses physical impression without alignment; 2.8–3.5 hands pause while light trace changes. No digital reconstruction.''',
'''S19 electronics recedes; dry paper, modest glass support vibration, two independent close spatial layers and soft inharmonic piano. Keep sine beneath. Paper fold decays toward S21 fabric/key.''',prop='paper_archive, translucent_glass_record',characters='archivist_left_hand, archivist_right_hand',prev='Constructed live city vs incomplete historical archive',nxt='Archive paper contact shifts into handover hands')
add(21,72.5,76.5,'時間的交接','The Transfer of Time','Felix Gonzalez-Torres','“Untitled” (Perfect Lovers) (1987–90)','Inescapable time drift, not paired clocks.',
'''Close tactile dark fictional boardroom. An adult founder hand in a plain charcoal SHIRT sleeve passes one original undecorated brass key to a second fictional adult hand emerging from a structured frost-white formal sleeve. Both faces remain out of frame. Beyond, the empty chair already bears the founder coat A, removed off-screen during the time gap between S17 and S21. The founder is NOT wearing the coat at this moment, preventing any object teleportation. Two slightly mismatched reflections approach across the key. 85mm close focus, dark quiet table, no real-world identities.''',
'''0–0.8 key supported by founder hand; 0.8–1.8 receiving hand opens below; 1.8–2.6 handover contact; 2.6–3.3 founder sleeve withdraws; 3.3–4.0 rack focus to empty chair and coat. Founder remains in charcoal shirt sleeves throughout S21; coat A has been on chair from the start of this shot. No garment movement or teleportation.''',
'''Paper archive residual sound fades; two independent quiet breath/fabric pulses, single close brass-metal contact with decay. No clocks/ticking, victorious music or vocal narration. Metal decay leads to S22 dry paper.''',prop='handover_key, founder_coat_A, empty_chair',characters='founder_hand, steward_hand',prev='Two methods of archive become two human temporal rhythms',nxt='Hands on key match hands building paper bridge',contest='Use two clearly fictional non-identifiable adult hands and generic neutral sleeves; no biographical CEO cues or company references.')
add(22,76.5,79.5,'紙的海岸','The Paper Shore','Thomas Demand','Office (1996)','Hand-built plausible paper reconstruction; do not reproduce his office.',
'''Huge nearly empty fictional Japanese corporate office at night. One dignified middle-aged salaryman in a worn charcoal suit kneels to make a detailed miniature coastline, mountains, little settlements and a fragile crossing bridge using real office paper, binder clips, glue and stamps. Paper terrain spreads from table across floor; far tiny paper house (same origami method as S11, not necessarily identical physical piece) has warm unoccupied window, while real city outside is dark. A distant unbranded compact local compute device is scarcely noticed. All handmade fibres/folds credible; 35mm slightly elevated three-quarter, quiet scale and human isolation. Never replicate Death Stranding game objects, characters, or physical art models.''',
'''0–0.8 hand secures final fold of narrow paper bridge; 0.8–1.7 ventilation gently moves paper; 1.7–2.5 man steadies the crossing; 2.5–3.0 bridge stands but empty house remains distant. No paper world magical transformation.''',
'''S21 key's metal tail disappears into close paper/fingernail friction and HVAC. Original quiet felt-muted piano tone near 1.7s, intentionally off physical hand gesture; distant compute overtone not triumphant. Paper residue J-cuts S23.''',prop='paper_landscape, paper_house_v1, compact_local_compute',characters='salaryman',prev='Brass key transfers in a second; paper bridge remains unfinished',nxt='Paper friction thins into large optical chamber ambience',contest='Entirely original paper geography, no game-inspired iconic cargo rigs, BB pod, porter costume, proprietary logos or real person plates.')
add(23,79.5,84,'遲到的倒影','The Delayed Reflection','Bill Viola','The Reflecting Pool (1977–79)','Human action and material reflection have different time states; no pool/jump imagery.',
'''Final return to same S03/S17 mineral chamber. Suspended translucent optical membranes are now mostly dark, one slight refracted light remaining. Same fictional founder from behind, now in plain charcoal shirt, no coat. A narrow floor reflection retains the previous position after he steps. Two small anonymous workers in very distant passages withdraw separate cultural/technical objects: old piano on practical dolly and empty antique opera coat on rolling rack. They are background elements, not personifications of countries. 35mm locked and generous negative space; no face or copied art video.''',
'''0–1.0 founder stands and distant workers move; 1.0–2.0 one small step, light reflection lingers; 2.0–3.1 delayed reflection moves toward new position as figure lifts gaze; 3.1–4.0 objects disappear through exits; 4.0–4.5 reflection catches up, hold.''',
'''S22 paper friction decays; large chamber tone, one honest footstep, a second original electroacoustic resonance later than movement. Old Japan/Europe timbral residue may appear as new one-shots but NEVER restart pre-S18 19/17-second loops. Sine persists into S24.''',prop='optical_membranes, delayed_reflection, untuned_piano, opera_coat',characters='founder, distant_workers',prev='Human paper work vs quiet former creator, same hand-to-light motif',nxt='Delayed floor light becomes wet-pavement reflection in S24',contest='Generate all fictional people and motion from scratch; no use of identifiable participant real footage or reference plate in contest master.')
add(24,84,87,'不同步的生命','The Return','Rafael Lozano-Hemmer','Pulse Room (2006)','Collective light from different life rhythms; no hanging heart-rate grid.',
'''Return to same fictional intimate Taiwan-style night market as S02, rainy now. A few ordinary fictional adults gently raise the SAME plain charcoal founder work coat A, while the unique irregular small incandescent filament bird from S04 rests on its shoulder. People move at different rhythms; some continue selling food; no mass choreography or political demonstration. Bare lamps vary naturally in brightness, not biometric synchronisation. Warm reflections on rain-dark pavement echo S03/S23 optical geometry in human-scale world. 35mm low moderate wide, intimate, physical, dignified, bittersweet. No celebrity leather-jacket cues, emblem-bird, slogans, flags or lookalike crowds.''',
'''0–0.8 multiple hands lift coat separately; 0.8–1.7 delicate bird settles on shoulder; 1.7–2.5 one rain droplet hits puddle, bulbs remain independent; 2.5–3.0 coat steadies as people breathe naturally, hard cut black at 87.0. No triumphal camera crane.''',
'''Bring back new near-market room tone (not restart original seven-second loop), restrained rain, fabric and original four-note idea only as unresolved fragments. At 87.0 simultaneously remove all non-sine sounds, sine continues unchanged into S25. No victory chord.''',prop='founder_coat_A, filament_bird_v1, market_bulb, warm_reflection',characters='market_ensemble',prev='S23 delayed optical reflection becomes natural wet-market reflection',nxt='All images disappear, original persistent sine remains')
add(25,87,90,'尚未結束的時間','The Unfinished Duration','On Kawara','One Million Years (Future), audio realization 1993','Duration outlives image; no year reading or original audio.',
'''EDITOR ONLY. Absolute black frame with restrained original typography ASYNC: SUCCESSION placed in post at centre-safe area; licensed typeface, static title, no animated glints, particles, digital texture, logo or visuals. Title disappears to pure black before file boundary.''',
'''0–0.5 hard-cut black; 0.5–1.0 title fades on minimally; 1.0–2.5 fixed title; 2.5–3.0 title fades off. 90.000s hard picture finish. No extra motion.''',
'''At 87.000 remove all S24 ambience and motif fragments, preserve only the single sine that began at 0.500 s, phase-continuously. No final chord or spoken years. Finish at 90.000 s with technically de-clicked edit; artistic impression of persistence, not audible digital pop.''',prev='S24 rain and crowd disappear',nxt='Playback ends at 90.000s; tone conceptually continues',mode='editorial')

# Other output components
characters = {
 'founder':{'description':'Fictional adult, back/hand views only; plain charcoal coat A for S03/S17, coat removed off-screen before S21 and hanging on chair during S21; plain shirt S23. No real CEO biographical cues.','shots':['S03','S17','S21','S23']},
 'steward_hand':{'description':'Fictional adult successor, frost-white structured sleeve, plain brass key; no recognizable film costume.','shots':['S21']},
 'marcher':{'description':'Fictional woman in weathered deep-crimson coat, custom fan-horn; neutral expression and no slogans.','shots':['S09']},
 'lithographer':{'description':'Fictional elderly technical worker, aged unbranded pale cleanroom suit, single wafer; dignity over decline stereotype.','shots':['S13']},
 'weaver_left':{'description':'Fictional adult woman repairing muted terracotta fabric; natural hand skill.','shots':['S15']},
 'weaver_right':{'description':'Fictional adult woman working multiple muted natural fibres; natural hand skill.','shots':['S15']},
 'salaryman':{'description':'Fictional middle-aged Japanese office worker, charcoal suit, physically hand-constructs entire paper geography; no game costume.','shots':['S22']},
 'market_ensemble':{'description':'Fictional multigenerational ordinary night-market adults; S02 and S24 evoke same place, no identifiable person or real plate.','shots':['S02','S24']}
}
props = {
 'founder_coat_A':{'continuity':'S03 and S17 worn by founder; S21 already hanging on chair when shot starts; founder wears plain charcoal shirt sleeve; S23 not worn; S24 same design raised by crowd. Distinct from archive coat B.','markers':'plain charcoal work coat, unique subtle cuff-repair stitching near LEFT hem; no signature leather look','shots':['S03','S17','S21','S24']},
 'archive_coat_B':{'continuity':'S10 archive copy from earlier period; different short cut and cuff wear; must never be confused with A.','markers':'shorter straight charcoal cotton coat, no left hem repair; shelf glasses generic','shots':['S10']},
 'filament_bird_v1':{'continuity':'Same original irregular wire joins and filament placement in S04 and S24; no resemblance to Mockingjay or other emblem.','markers':'asymmetric abstract bird, one warm filament, three very small wire joints, not a logo silhouette','shots':['S04','S24']},
 'optical_membranes':{'continuity':'S03 three-layer open, S17 more layered, S23 nearly dormant; NEVER suspended rectangular tank or original artwork replica.','markers':'curved translucent polymer glass blades with condensation and physically real caustics','shots':['S03','S17','S23']},
 'paper_house_v1':{'continuity':'Tiny paper house in S11 foreshadows S22 paper-city craft method and warm window; not a physically transported prop.','markers':'uneven folded roof and small nonrectangular single window, plain office paper','shots':['S11','S22']},
 'handover_key':{'continuity':'One key in S21 only, original simple design.','markers':'small undecorated brass key, no corporate insignia','shots':['S21']},
 'warm_reflection':{'continuity':'S02 wet steel -> S03 membrane -> S04 suitcase -> S05 water -> S06 light -> S17 optical -> S23 floor -> S24 rain pavement. Cause is real local light, not magical light travelling locations.','markers':'thin broken warm line, never identical scene replication','shots':['S02','S03','S04','S05','S06','S17','S23','S24']},
 'untuned_piano':{'continuity':'S13 coastal hall aged piano, S23 distant piano dolly is echo/transported object, no literal inter-country transport claim.','markers':'weathered upright with worn lower wooden panel and one incomplete-return key','shots':['S13','S23']},
 'opera_coat':{'continuity':'S14 costume/archive motif remains indirect; S23 on rolling rack held by anonymous worker.','markers':'antique dark opera coat, muted design without movie reference','shots':['S14','S23']}
}

sound_ir={
 'version':'J4-SOUND-IR-v2.6','duration_ms':90000,'sample_rate_hz':48000,'master_lufs_target':-14,'max_true_peak_dbTP':-1,
 'source_note':'Design targets only; not an audio master or measured compliance.',
 'stems':[{'id':'STEM_01','name':'Continuous sine/electrical ground','rule':'One phase-stable tone starts at 500ms and persists until 90,000ms; de-click only at export boundary.'},
          {'id':'STEM_02','name':'Nature, water, airflow and physical ambience','rule':'Independent natural events, never over-musicalized.'},
          {'id':'STEM_03','name':'Labour, material, machines and gestures','rule':'Tactile sounds preserve microtiming.'},
          {'id':'STEM_04','name':'Original pitched material','rule':'Original sparse four-note motif introduced at S03/04/05/06; never copy artist melodies.'},
          {'id':'STEM_05','name':'Voice, space, room decay','rule':'Fictional intelligibility optional, spatial response important; no cloned voice.'}],
 'phase_families':[{'id':'COMMUNITY_7','start_ms':3000,'period_ms':7000,'theme':'market/community','forced_stop_ms':63700},
                   {'id':'MAINTENANCE_11','start_ms':16000,'period_ms':11000,'theme':'human labour','forced_stop_ms':63700},
                   {'id':'COMPUTE_5','start_ms':20000,'period_ms':5000,'theme':'distributed/centralised compute','forced_stop_ms':63700},
                   {'id':'ENVIRONMENT_13','start_ms':24000,'period_ms':13000,'theme':'artificial climate','forced_stop_ms':63700},
                   {'id':'JAPAN_19','start_ms':46000,'period_ms':19000,'theme':'untuned instrument','forced_stop_ms':63700},
                   {'id':'EUROPE_17','start_ms':50000,'period_ms':17000,'theme':'opera/architecture','forced_stop_ms':63700}],
 'events':[{'at_ms':500,'kind':'start_sine','phase_continuous':True},
           {'at_ms':7000,'kind':'motif_note','index':1},{'at_ms':12000,'kind':'motif_note','index':2},
           {'at_ms':16000,'kind':'motif_note','index':3},{'at_ms':20000,'kind':'motif_note','index':4},
           {'at_ms':35500,'kind':'deliberate_exception','detail':'S10 archival door interrupts unfinished piano-like decay'},
           {'at_ms':63700,'kind':'forced_global_cut','target':'all six phase families plus secondary motif textures','preserve':['STEM_01']},
           {'at_ms':65000,'kind':'new_post_cut_ambience','detail':'S19 news-studio electronics; six phase families stay off'},
           {'at_ms':84000,'kind':'new_market_memory','detail':'S24 new short market ambience, not re-start of COMMUNITY_7 cycle'},
           {'at_ms':87000,'kind':'strip_to_sine','preserve':['STEM_01']},
           {'at_ms':90000,'kind':'end_file','detail':'edit de-click at terminal; perceptual continuity, not raw pop'}],
 'shot_sound_cues':[{'shot_id':s['id'],'start_ms':s['start_ms'],'end_ms':s['end_ms'],'sound_prompt':s['sound_prompt']} for s in shots]
}

# Validate shot table and temporal invariants
assert len(shots)==25
for i,s in enumerate(shots):
 assert s['id']==f'S{i+1:02d}'
 if i: assert s['start_ms']==shots[i-1]['end_ms'], (shots[i-1]['id'],s['id'])
 assert s['duration_ms']>0 and s['end_ms']-s['start_ms']==s['duration_ms']
assert shots[-1]['end_ms']==90000
assert sum(s['duration_ms'] for s in shots)==90000
assert [s['id'] for s in shots if s['generation_mode']=='editorial']==['S01','S18','S25']
# Budget using user's historical planning unit rates, NOT current account prices.
cinema = 7*5*2  # credits/shot: 5s min, 2 takes
swap = 32*2
upscale = 4
reserve=0.15
ceil=lambda x:math.ceil(x)
orig_portfolio=(20*cinema+3*swap+23*upscale+5.4)*(1+reserve)
new_portfolio=(19*cinema+3*swap+22*upscale+5.4)*(1+reserve)
orig_contest=(23*cinema+23*upscale+2.8+25)*(1+reserve)
new_contest=(22*cinema+22*upscale+2.8+25)*(1+reserve)
new_portfolio_all_cinema=(22*cinema+22*upscale+5.4)*(1+reserve)
portfolio_plates_no_swap=(19*cinema+22*upscale+5.4)*(1+reserve)
budget={
 'source':'User-supplied historical J4 costing assumptions, not live Higgsfield pricing','currency':'Higgsfield planning credits',
 'inputs':{'cinema_720p_credits_per_second':7,'min_billable_seconds':5,'takes':2,'swap_genjutsu_lite_credits_per_take':32,'upscale_per_shot':4,'repair_reserve':0.15,'contest_soul_id':25,'portfolio_voice':5.4,'contest_voice':2.8},
 'original_90s_baseline':{'portfolio_round_up':ceil(orig_portfolio),'contest_round_up':ceil(orig_contest)},
 'v2_6_S18_editorial':{'portfolio_19_cinema_3_swap_round_up':ceil(new_portfolio),'contest_22_cinema_round_up':ceil(new_contest),'portfolio_if_all_22_video_shots_cinema_round_up':ceil(new_portfolio_all_cinema),'portfolio_if_three_plates_no_swap_round_up':ceil(portfolio_plates_no_swap)},
 'excluded':'Audio composition/voice fees beyond listed prompts, asset licensing, any paid stills, extra failed takes, account current consumption and actual contest rules remain unverified.',
 'rule':'Never generate without Neon approval + estimate posted to AI Video Production Service + current monthly 9000-point headroom verified.'}

# Write IRs
shot_ir={'project':'J4 ASYNC: SUCCESSION','version':'v2.6-normalized','status':'text-only draft no generation','aspect_ratio':'9:16','duration_ms':90000,
 'master_image_lock':MASTER_IMAGE,'master_sound_lock':MASTER_SOUND,'global_negative_prompt':NEGATIVE,
 'governance':{'no_paid_generation_without':'Neon explicit approval, Director posted credits estimate to AI Video Production Service, and live monthly headroom confirmation','contest':'Not eligible yet: 90s teaser < claimed 3-minute minimum; all contest permission/IP/real-person/current rules must be reverified','reference_rule':'25 contemporary-art methods are research only, not license to replicate images/audio'},
 'shots':shots}
(D/'j4_shots.json').write_text(json.dumps(shot_ir,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(D/'j4_sound_ir.json').write_text(json.dumps(sound_ir,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(D/'j4_budget_audit.json').write_text(json.dumps(budget,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# CSV shotlist
with (D/'j4_shotlist.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['shot_id','act','start_seconds','end_seconds','duration_seconds','title_zh','title_en','artist','artwork','mode','props','characters','text_status'])
 w.writeheader()
 for s in shots:
  w.writerow({'shot_id':s['id'],'act':s['act'],'start_seconds':s['start_ms']/1000,'end_seconds':s['end_ms']/1000,'duration_seconds':s['duration_ms']/1000,'title_zh':s['title_zh'],'title_en':s['title_en'],'artist':s['art_reference']['artist'],'artwork':s['art_reference']['work'],'mode':s['generation_mode'],'props':'; '.join(s['props']),'characters':'; '.join(s['characters']),'text_status':s['review_state']})

# QC matrix: each criterion is a real gate, not a claim of passing.
qcs=[]
def qc(scope,criterion,method,gate,owner='Director / QC'):
 qcs.append(dict(scope=scope,criterion=criterion,verification_method=method,threshold_or_gate=gate,owner=owner,status='NOT_RUN',evidence_uri=''))
qc('GLOBAL','Continuous 90s timeline','Parse and sum milliseconds in JSON','End 90,000ms, 25 shots contiguous, no overlaps','Automated')
qc('GLOBAL','Original sound rights','Human asset provenance and fingerprint review','No borrowed composition, vocal likeness or art-installation sample','Sound Director')
qc('GLOBAL','Reference distance','Shot-by-shot image comparison against uploaded clips and referenced artworks','No recognisable replication, brand, film/game costume, real person','Art Director')
qc('GLOBAL','Contest source and eligibility','Re-check current contest rules and all visible/underlying assets','Separately approved full contest version; 90s teaser not submission ready','Legal/Director')
qc('GLOBAL','Generation authorization','Check approval record and account ledger','Neon GO, Director credit note, real monthly headroom all required','Producer')
qc('GLOBAL','Audio delivery','Measure master with loudness and true-peak analyzer','Target -14 LUFS and <= -1 dBTP; audio generated/mastered first','Sound Director')
qc('GLOBAL','Picture creative score','Six-dimensional panel assessment, original J4 pipeline','Average >=8, each >=7, documentary claims flagged','Director')
qc('S01','Absolute black','Frame inspection','No particle, grey noise, unintended logo')
qc('S03','Optical membrane originality','Reference image comparison + physics check','No suspended tank/cube; causal refraction')
qc('S04/S24','Bird design lock','Compare keyframes and silhouette','Same unique prop, original non-logo form')
qc('S10/S17/S21/S24','Coat identity','Compare hem/stitching and shot chronology','Archive B distinct; founder A consistent')
qc('S11/S22','Paper house foreshadow','Material/fold and warm window comparison','Same construction language, not magic transport')
qc('S13/S23','Piano continuity','Compare upright shape and weathering','Distant S23 object references S13 design without catastrophe copying')
qc('S14','Audience/acoustic incongruity','Silent-view + audio-view test','No performance yet applause exists; no film IP copy')
qc('S17/S18','Forced interruption precision','Audio waveform and timeline gates','Cut exactly 63,700ms; sine continuous; no loop natural alignment','Sound Director')
qc('S18','Accessibility for flashes','Review light transition and photosensitivity alternative','No rapid high-intensity flashing; low-light non-strobe export possible')
qc('S18/S19','Three positions match','Visual correspondence across cut','Three abstract lights map to three lit chairs')
qc('S19','Fictional broadcast integrity','Text/logo/political-landmark review','No claim or appearance of real news footage')
qc('S21','Hand and key physics','Single-frame hand/finger and object contact review','No finger morph, no key teleport, coat A edit practical')
qc('S22','Craft material and worker dignity','Object/hand/scale check','Actual paper folds, physically credible, no game IP')
qc('S23','Reflection temporal cue','Frame-by-frame motion vs optical trace','Measurable restrained delay; same fictional founder, no original footage in contest')
qc('S24','Crowd and lighting','Frame-by-frame gestures and object identity','Non-unison crowd, original bird, real wet-surface physics')
qc('S25','End of file audio','Listen to final 50 ms with meters','No end click; conceptual sine continuity')
with (D/'j4_qc_matrix.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['scope','criterion','verification_method','threshold_or_gate','owner','status','evidence_uri'])
 qcs[0]['status']='PASS_STATIC';qcs[0]['evidence_uri']='j4_shots.json validated by build_ir.py contiguous-ms assertions'
 w.writeheader();w.writerows(qcs)

# Prompt book markdown
lines=['# J4《非同步：繼承》— Master Prompt Book v2.6', '', '> 25 鏡定稿內容之**標準化、非逐字轉錄**版本，對應本對話 v2.0–v2.5 的創作決策。此文件為 0 點文字製作；沒有生成任何媒體。', '', '## 全片影像鎖','', '```text',MASTER_IMAGE,'```','', '## 全片原創聲音鎖','', '```text',MASTER_SOUND,'```','', '## Global Negative Prompt','', '```text',NEGATIVE,'```','']
for s in shots:
 lines += [f"## {s['id']} — {s['title_zh']} / {s['title_en']} | {s['start_ms']/1000:.1f}–{s['end_ms']/1000:.1f}s", '',f"**藝術對標：** {s['art_reference']['artist']}，*{s['art_reference']['work']}*。借用方法：{s['art_reference']['transfer_method']}", '',f"**模式：** {s['generation_mode']}｜**道具：** {', '.join(s['props']) or '無'}｜**角色：** {', '.join(s['characters']) or '無'}", '', '### Image Prompt','```text',s['image_prompt'],'```', '', '### Motion / Editorial Prompt','```text',s['motion_prompt'],'```', '', '### Original Sound Prompt','```text',s['sound_prompt'],'```', '',f"**進場：** {s['in_transition']}  **出場：** {s['out_transition']}", '',f"**Contest override：** {s['contest_override']}",'','---','']
(D/'j4_master_prompt_book.md').write_text('\n'.join(lines),encoding='utf-8')
# Character/prop bible
b=['# J4 Character & Prop Bible v2.6','','> 所有角色皆為虛構；藝術史參考只借方法，不重製。以下條目供 Shot IR、關鍵幀種子、剪輯與 QC 交叉比對。','', '## 角色鎖','']
for k,v in characters.items(): b += [f'### `{k}`','',v['description'],f"使用鏡頭：{', '.join(v['shots'])}",'']
b += ['## 道具與時間連續性','']
for k,v in props.items():b += [f'### `{k}`','',f"- 連續性：{v['continuity']}",f"- 特徵鎖：{v['markers']}",f"- 鏡頭：{', '.join(v['shots'])}",'']
b += ['## 重要的防錯約束','','- S10 的 B 外套是檔案副本；S03/S17/S21/S24 的 A 外套才是主線原物。','- S21 的外套 A 已在 S17 到 S21 的畫面時間空隙由主角脫下，S21 開頭起始終掛在椅上；遞鑰匙的手只能穿無特徵深色襯衫袖口。','- S11 與 S22 是紙屋製作方法相同，不代表它是從工廠被物理搬到另一個國家。','- S13 的技術工藝不是對日本整體經濟能力的事實判決。','- S19 比賽版更換為虛構城市，不呈現真正新聞、政治人物或所謂會面現場。','- 比賽版 S03/S17/S23 不得使用參賽者可辨識的真人實拍 plate；使用完全新生成虛構角色。']
(D/'j4_character_prop_bible.md').write_text('\n'.join(b)+'\n',encoding='utf-8')
# Master specification
spec=f'''# J4《非同步：繼承》工程整合規格 v2.6

**狀態：TEXT_ONLY / NOT_GENERATED / NOT_APPROVED_FOR_PAID_RENDER**  
**時長：90.000 秒**｜**鏡頭：25**｜**格式：9:16**｜**藝術對標：25 件（方法參考，非臨摹）**  

## 檔案索引

- `j4_shots.json`: 單一結構化 Shot IR，含完整 image / motion / sound prompt、藝術方法、進出場銜接、道具與 contest override。
- `j4_sound_ir.json`: 五軌聲音設計、六組 phase-family、精確中斷事件及逐鏡聲音指令。
- `j4_master_prompt_book.md`: 25 鏡可人工閱讀的完整提示詞集（**標準化重寫**，並非舊回答逐字副本）。
- `j4_character_prop_bible.md`: 角色與道具的 ID、材質、鏡頭時間線、防錯約束。
- `j4_qc_matrix.csv`: 逐項人工與機械驗收，僅時碼資料檢查為 `PASS_STATIC`，其餘預設 `NOT_RUN`。
- `j4_shotlist.csv`: 可匯入剪輯規劃的鏡頭清單。
- `j4_budget_audit.json`: 使用原先預算表假設作的數學試算，不是即時 Higgsfield 報價。

## 戲劇結構

| 幕 | 時間 | 敘事 |
|---|---|---|
| 1 | 0–20s | 光的起源：日常、技術、維護勞動 |
| 2 | 20–65s | 光被分配：集體儀式、機器、連結、強制同步 |
| 3 | 65–90s | 權力繼承、紙世界、普通人的未來 |

## 相容性註記

此 JSON 是 v2.6 的**規範化 canonical IR**，尚未確認與原 repository `pipeline/build_animatic.py`、`shots.json` schema 一致。接入前須提供原始 schema 或撰寫薄型 adapter；不得直接覆寫現有 pipeline 檔案。

## 工程檢查結果（資料層）

- `len(shots)=25`，時間排序 S01–S25 無缺號。
- 毫秒區間連續，無重疊、無間隙，合計 **90000 ms**。
- S18 為 **63700–65000 ms**，短暫低亮度抽象光形採後製，取代原 5 秒最低計費的影片生成假設。
- S01、S18、S25 為 `editorial`；其餘 22 鏡列作候選影片生成鏡頭。
- 六組週期在 **63700 ms** 強制中斷；S24 夜市聲重返時是新的短暫聲場，不恢復七秒週期。
- `STEM_01` 原創正弦從 500 ms 至 90000 ms 保持相位連續；最後需技術防爆音處理。
- 作品集／比賽版本分流仍是待審；**90 秒不符合原文件所稱的 3–7 分鐘正式參賽片長**。

## 進一步人工審核事項

1. S21 的外套物理連續性：主角在鏡頭開始前已脫下外套；畫面中只能看到深色襯衫袖與椅上外套。
2. S03/S17/S23 的虛構角色要有一致的姿態和比例；比賽版不使用可辨識真人素材。
3. 避免把 S13／S22 的藝術性批判當作「日本沒有能力做軟體」的實證論斷。
4. 任何聲音生成工具皆不得重製坂本龍一作品或其他當代藝術家的受保護錄音。
5. `source / date` 核對欄不在本資料集中聲稱驗證；另維護來源登記簿與權利清冊。

## 權限閘口

> Neon 明確批准 → Director 在「AI Video Production Service」聊天室貼出依最新帳戶價格計算的估點 → 核對本月 9000 點上限與已使用餘額 → 才能進入生成。

本階段未呼叫任何圖片／影片生成、MCP／CLI 動畫或付費服務；以下成本為**原文件歷史公式**所做的紙上估算。

## 成本修正（原單價假設）

- 原始作品集版：{ceil(orig_portfolio)} 點；若 S18 改後製且其餘路徑維持，約 **{ceil(new_portfolio)} 點**。
- 原始 90 秒比賽候選版：{ceil(orig_contest)} 點；若 S18 改後製，約 **{ceil(new_contest)} 點**（含一筆 Soul ID 25 點）。
- 如果 S03/S17/S23 因構圖大改而不能使用 Genjutsu，22 鏡全走 Cinema，作品集版約 **{ceil(new_portfolio_all_cinema)} 點**，未包含另外授權與音樂生成費。
- 已有的真實 plate 若直接使用可減少點數，但不代表符合比賽允許的媒體來源條款。

**注意：以上都不是正式報價或帳戶核銷結果。**
'''
(D/'j4_master_spec.md').write_text(spec,encoding='utf-8')
# zip without build script
with zipfile.ZipFile('/mnt/data/j4_museum_v2_6_bundle.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for fn in ['j4_shots.json','j4_sound_ir.json','j4_master_prompt_book.md','j4_character_prop_bible.md','j4_qc_matrix.csv','j4_shotlist.csv','j4_budget_audit.json','j4_master_spec.md']:
  z.write(D/fn,arcname=fn)
print('VALIDATED',len(shots),'shots',sum(s['duration_ms'] for s in shots),'ms')
print('COSTS',budget['original_90s_baseline'],budget['v2_6_S18_editorial'])
for f in sorted(D.glob('*')):print(f.name,f.stat().st_size)
print('/mnt/data/j4_museum_v2_6_bundle.zip',Path('/mnt/data/j4_museum_v2_6_bundle.zip').stat().st_size)
