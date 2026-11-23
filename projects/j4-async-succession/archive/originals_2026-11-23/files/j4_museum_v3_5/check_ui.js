
const DATA={"arcs": [{"id": "G2A_COAT", "name_zh": "真假外套：身分的延遲揭示", "a": "S10", "b": "S21", "method": "PERCEPTUAL + NARRATIVE_RECONTEXT", "mechanism": "FIGURE_GROUND_SHADOW + OBJECT_IDENTITY_CONTRAST", "first_read": "外套影子似乎把不在場的人留在制度裡。", "second_read": "S21 外套 A 的左下襬有修補，而 S10 的 B 是無修補的檔案版本；觀眾改讀 S10。", "cue": "A 有左下襬修補，B 無；S10 短直衣擺，S21 較長。", "no_cheat": "不得靠服裝顏色、真人影射、旁白或獨立特寫解題。", "art_transfer": "以影子形成暫時的人形錯視，反射支持單物件多重讀法；禁止複製原藝術裝置。", "variant_A": "A 修補可見，讓 S10 暫時誤讀；S21 最末焦點讓左下襬成為可查證證據。", "variant_control": "只在 S21 以合理的椅背／袖子遮住修補痕；不得替換成另一件衣服。", "decision": "CANDIDATE_NOT_APPROVED", "media": "MISSING_REAL_STIMULUS", "analysis_guard": "影子是光影雙讀；真假衣服是敘事重釋，不應全稱光學錯視。", "cross_shots": ["S03", "S17", "S21", "S24"], "states": [{"shot": "S10", "object": "archive_coat_B", "state": "ARCHIVED_NO_PATCH", "length": "short", "repair": false, "identity": "B", "identity_policy": "REPLACE_CONSISTENTLY_ACROSS_OCCURRENCES", "registry_invariant": "short charcoal cotton; NO repaired left hem; NEVER A"}, {"shot": "S21", "object": "founder_coat_A", "state": "ON_CHAIR_REPAIRED", "length": "long", "repair": true, "identity": "A", "identity_policy": "REPLACE_CONSISTENTLY_ACROSS_OCCURRENCES", "registry_invariant": "long charcoal work coat, visible LEFT hem repair; same S03/S17/S21/S24"}], "beats": [{"shot": "S10", "local_start_frame": 0, "local_end_frame": 27, "action": "外套 B 首影格可見；光線讓影子近似人形"}, {"shot": "S10", "local_start_frame": 27, "local_end_frame": 93, "action": "鐵門沿途遮擋；38.600 秒局部殘響截斷"}, {"shot": "S10", "local_start_frame": 93, "local_end_frame": 105, "action": "門關後空袖移動，沒有真人"}, {"shot": "S21", "local_start_frame": 0, "local_end_frame": 54, "action": "唯一黃銅鑰匙由兩隻手準備交接；外套 A 在椅上"}, {"shot": "S21", "local_start_frame": 54, "local_end_frame": 99, "action": "鑰匙完成轉移；衣服不得憑空移動"}, {"shot": "S21", "local_start_frame": 99, "local_end_frame": 120, "action": "景深轉向外套 A 左下襬修補，須有可辨識的畫面證據"}], "visual_anchors": {"S10": {"coat_bbox": [0.32, 0.34, 0.36, 0.34], "shadow_bbox": [0.19, 0.28, 0.54, 0.46]}, "S21": {"chair_coat_bbox": [0.38, 0.09, 0.3, 0.28], "key_bbox": [0.44, 0.47, 0.16, 0.12], "repair_subregion_relative": [0.15, 0.76, 0.18, 0.12]}}, "acceptance": ["S10 影子可雙讀，但本體仍是空外套", "S21 同一影格只有一件主線外套 A 與一把鑰匙", "修補可在最後不少於 21 格的可讀視窗中看見", "兩人交接完整、不穿幫、不變手指", "A/B 物理區別不依賴顏色或字幕"], "source_arc_id": "ARC_COAT_FALSE", "source_art": [{"shot": "S10", "artist": "Tim Noble × Sue Webster", "work": "Dirty White Trash (with Gulls)", "url": "https://www.moma.org/calendar/exhibitions/4798", "not_to_copy": "不重製垃圾堆人像或原作投影角度"}, {"shot": "S21", "artist": "Michelangelo Pistoletto", "work": "Man with Yellow Pants", "url": "https://www.moma.org/collection/works/79435", "not_to_copy": "不重製真人等比例鏡畫構圖"}], "timing": {"S10": {"start_ms": 35500, "end_ms": 39000, "duration_ms": 3500}, "S21": {"start_ms": 72500, "end_ms": 76500, "duration_ms": 4000}}, "control_guard": "Control only changes the anchor cue, never the broad scene quality, shot duration, physical identity, soundtrack or legal status.", "trial_status": "NO_MEDIA_NOT_RUN"}, {"id": "G2A_PAPER", "name_zh": "紙屋：從小手作到無人居住的國家", "a": "S11", "b": "S22", "method": "SCALE_DUAL_READ + NARRATIVE_RECONTEXT", "mechanism": "MINIATURE_MATERIAL_EVIDENCE + SHARED_FABRICATION_GRAMMAR", "first_read": "工廠一張凳子上有尚未完成的小紙屋。", "second_read": "S22 精細紙構世界空無一人，S11 紙屋由背景細節變成人類努力的伏筆。", "cue": "偏斜的屋頂摺線＋一個不規則狹窗；兩屋是不同實體。", "no_cheat": "不把紙模型變成真實地景、不剪入遊戲素材，也不在 S11 放大伏筆。", "art_transfer": "用微型物件尺度與紙製空間的真實痕跡，建立雙重尺度認知；不重建原作模型。", "variant_A": "S11 紙屋是次要物件，但回看可辨折線；S22 紙海岸第一格就完整。", "variant_control": "S22 紙屋改用不相容的屋頂折線與窗形，紙張色溫、尺寸與環境保持相近。", "decision": "CANDIDATE_NOT_APPROVED", "media": "MISSING_REAL_STIMULUS", "analysis_guard": "這主要是尺度雙讀與敘事改讀；並非物件真的從小變大。", "cross_shots": ["S11", "S15", "S20", "S22"], "states": [{"shot": "S11", "object": "paper_house_v1", "state": "SMALL_INCOMPLETE_STOOL", "same_physical_as_S22": false, "identity_policy": "SHARE_DESIGN_GRAMMAR_NOT_PHYSICAL_IDENTITY", "registry_invariant": "one irregular folded roof and odd-shaped window; S11 and S22 NOT identical physical house"}, {"shot": "S22", "object": "paper_house_v1", "state": "DIFFERENT_HOUSE_SHARED_FOLD_GRAMMAR", "same_physical_as_S11": false, "identity_policy": "SHARE_DESIGN_GRAMMAR_NOT_PHYSICAL_IDENTITY", "registry_invariant": "one irregular folded roof and odd-shaped window; S11 and S22 NOT identical physical house"}], "beats": [{"shot": "S11", "local_start_frame": 0, "local_end_frame": 90, "action": "工廠運轉，紙屋作為已存在的次要實物線索"}, {"shot": "S11", "local_start_frame": 90, "local_end_frame": 120, "action": "輕微橫移讓紙屋更容易被第二次觀看發現，不作獨立特寫"}, {"shot": "S22", "local_start_frame": 0, "local_end_frame": 18, "action": "第一影格完整看見上班族、紙橋、紙世界、空屋"}, {"shot": "S22", "local_start_frame": 18, "local_end_frame": 51, "action": "唯一主要動作：食指扶住被空調吹動的紙橋"}, {"shot": "S22", "local_start_frame": 51, "local_end_frame": 75, "action": "紙橋穩住，人手停止；紙的物理痕跡清楚"}, {"shot": "S22", "local_start_frame": 75, "local_end_frame": 90, "action": "空屋持續無人，沒有新的揭示或動作"}], "visual_anchors": {"S11": {"house_bbox": [0.52, 0.63, 0.19, 0.12]}, "S22": {"worker_bbox": [0.07, 0.42, 0.31, 0.45], "coast_bbox": [0.26, 0.57, 0.63, 0.36], "bridge_bbox": [0.41, 0.68, 0.27, 0.13], "house_bbox": [0.7, 0.46, 0.18, 0.19]}}, "acceptance": ["S11 回看可辨紙屋、首次不搶產線主題", "S11 與 S22 的屋頂折線與窗形一致，但不是相同實物", "S22 第一格能看見工人、紙海岸、紙橋、空屋", "紙張纖維、膠帶接縫、摺線符合真實結構", "S22 僅有手指扶橋的主要動作，無魔法地景變形"], "source_arc_id": "ARC_PAPER", "source_art": [{"shot": "S11", "artist": "Liliana Porter", "work": "Untitled (with Cube – tall)", "url": "https://whitney.org/collection/works/39006", "not_to_copy": "不重製原作的照片立方體加線框"}, {"shot": "S22", "artist": "Thomas Demand", "work": "Office", "url": "https://www.guggenheim.org/artwork/artist/thomas-demand", "not_to_copy": "不重製史塔西辦公室或遊戲場景"}], "timing": {"S11": {"start_ms": 39000, "end_ms": 43000, "duration_ms": 4000}, "S22": {"start_ms": 76500, "end_ms": 79500, "duration_ms": 3000}}, "control_guard": "Control only changes the anchor cue, never the broad scene quality, shot duration, physical identity, soundtrack or legal status.", "trial_status": "NO_MEDIA_NOT_RUN"}, {"id": "G2A_AUTHORITY", "name_zh": "光形：從抽象訊號到座位權力", "a": "S18", "b": "S19", "method": "RETROSPECTIVE_SHAPE_MATCH", "mechanism": "THREE_POSITION_RELATIVE_GEOMETRY + ILLUMINATED_HIERARCHY", "first_read": "S18 的低亮三光形沒有國家、人物或地理識別。", "second_read": "S19 虛構新聞台三處核心燈光與先前同序、近似相對間距。", "cue": "安全框橫向中心 x=[0.32,0.52,0.70]；兩個暗席只在 S19 出現。", "no_cheat": "不靠國家配色、政治面孔、標示、閃光或主持人台詞。", "art_transfer": "借低解析度形態識別與光的空間權重研究，畫面完全原創。", "variant_A": "S18 單次柔和低亮揭露；S19 三處燈位繼承相對位置。", "variant_control": "S19 三個主位改成 x=[0.24,0.55,0.84] 的不等距排列；仍為三個、亮度接近。", "decision": "CANDIDATE_NOT_APPROVED", "media": "MISSING_REAL_STIMULUS", "analysis_guard": "S18/S19 是敘事空間重釋；不能以兩個畫面都出現三個光形宣稱知覺錯視成功。", "cross_shots": ["S18", "S19", "S21"], "states": [{"shot": "S18", "object": "three_abstract_light_volumes", "state": "LOW_LUMINANCE_ABSTRACT", "x_centres": [0.32, 0.52, 0.7], "identity_policy": "SHARE_DESIGN_GRAMMAR_NOT_PHYSICAL_IDENTITY", "registry_invariant": "three dim abstract volumes; low-intensity reveal; no geo coding"}, {"shot": "S19", "object": "five_chairs", "state": "THREE_LIT_TWO_DIM", "x_centres_lit": [0.32, 0.52, 0.7], "total_chairs": 5, "identity_policy": "LOCAL_ROLE_SWAP_WITH_TRANSITION_REVIEW", "registry_invariant": "exactly five seats, three privileged by light and two dim"}], "beats": [{"shot": "S18", "local_start_frame": 0, "local_end_frame": 10, "action": "黑場，六聲部已在 63.700 秒切斷；只剩正弦波"}, {"shot": "S18", "local_start_frame": 10, "local_end_frame": 21, "action": "單次低亮顯現三抽象光位，禁止 strobe"}, {"shot": "S18", "local_start_frame": 21, "local_end_frame": 30, "action": "低亮淡回黑，避免突變"}, {"shot": "S18", "local_start_frame": 30, "local_end_frame": 39, "action": "維持黑場直到 65.000 秒"}, {"shot": "S19", "local_start_frame": 0, "local_end_frame": 21, "action": "虛構攝影棚的城市背板逐漸顯現"}, {"shot": "S19", "local_start_frame": 21, "local_end_frame": 54, "action": "三個主位逐步亮起，兩個周邊席位維持暗"}, {"shot": "S19", "local_start_frame": 54, "local_end_frame": 111, "action": "虛擬城市反射微小時間差，所有椅子仍空著"}, {"shot": "S19", "local_start_frame": 111, "local_end_frame": 120, "action": "光位保持不平等狀態，切到記憶檔案室"}], "visual_anchors": {"S18": {"x_centres": [0.32, 0.52, 0.7]}, "S19": {"lit_seat_x_centres": [0.32, 0.52, 0.7], "dim_seats": 2, "seat_count": 5}}, "acceptance": ["S18 只用一次低亮顯現，不用高頻頻閃", "S19 是明顯虛構新聞台，沒有真實峰會標示", "三光位及三主位相對配置有精確可檢查的對應", "陰影裡保留另外兩個座位，不擬人化政治人物", "S18 63.700 秒全局聲音中斷與 S19 65.000 秒開場不變"], "source_arc_id": "ARC_AUTHORITY", "source_art": [{"shot": "S18", "artist": "Jim Campbell", "work": "Exploded Views", "url": "https://www.sfmoma.org/exhibition/jim-campbell/", "not_to_copy": "不重製 LED 空間矩陣與閃爍人物"}, {"shot": "S19", "artist": "James Turrell", "work": "Afrum I (White)", "url": "https://web.guggenheim.org/exhibitions/turrell/", "not_to_copy": "不重製角落光立方或真實新聞畫面"}], "timing": {"S18": {"start_ms": 63700, "end_ms": 65000, "duration_ms": 1300}, "S19": {"start_ms": 65000, "end_ms": 69000, "duration_ms": 4000}}, "control_guard": "Control only changes the anchor cue, never the broad scene quality, shot duration, physical identity, soundtrack or legal status.", "trial_status": "NO_MEDIA_NOT_RUN"}]};
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
  g.push(`<path d="${roof}" fill="none" stroke="#f0e5c5" stroke-width="3"/>`,rect(209,274,30,28,'#ddd7c6','#ded9c7'),rect(223,282,6,10,amber));
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
