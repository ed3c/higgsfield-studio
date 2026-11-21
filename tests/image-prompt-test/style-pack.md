# 風格包：向頂尖創作者借技法，不要普通畫面

Neon 看過 T01–T03 後認為太普通。這一包改測「會讓人在 IG／TikTok／X 停下來的單幀」，只借技法（光線、鏡頭、色調、構圖邏輯、概念結構），不複製對方的成片、角色、台詞、真實人名或真實品牌。人物皆為虛構成年人。虛構品牌才准出現。

跑法與原本測試包相同：只在 [higgsfield.ai](https://higgsfield.ai) 網站生成靜態圖，9:16、2K。先跑 7 天無限次數的 Nano Banana Pro → Seedream 5.0 Pro → GPT Image 2.6 → GPT Image 2.6 Flare。生成鍵若出現點數，立刻停止。見 `run-guide.md`。評分仍用 `rubric.md`，但通過與否另外看各則的「什麼才不算普通」。

說明用繁體中文。提示詞用英文，整段複製，第一輪不要加修飾。

研究截止：台北時間 2026 年 11 月 21 日。來源能直接看見的寫「來源所示」；我從來源推論的寫「推論」。Higgsfield 個人頁（如 `@aist`、`@tambv`）以 WebFetch 幾乎取不到作品內容，故改用官方競賽頁、案例、新聞與可下載的公開劇照。

---

## 七種風格的視覺簽名

### PURGA Studio（Listen to Meh）

來源所示：官方競賽頁與 AWN（https://www.awn.com/news/argentinas-listen-meh-wins-500k-higgsfield-ai-film-prize）寫這是一支發生在阿根廷潘帕斯牧場的無對白短片，高喬人與一再回到屋頂的黑羊陷入荒謬對峙，風暴逼近；評審讚「visuals, color, composition and sound」，並點出荒謬、懸疑與魔幻寫實。AWN 公開海報劇照是近乎單色的剪影：暴風雲、一道閃電當作主光、農舍屋頂上站著一隻羊的黑色輪廓，左側大片留給標題。推論：戲劇不靠特效堆量，而靠「日常地景 + 一個不該在那裡的東西 + 天氣當燈」。

### AIST（Fukushima）

來源所示：官方競賽頁與評審評語——資深工程師面對災難；Paul W. S. Anderson 稱「Excellent visual style and immersive sound work」，Phedon Papamichael 稱「Excellent realism, character expressions」。團隊為賽普勒斯的 AI 工作室，Instagram / YouTube 從官方檔案寫出。我沒有取得可檢驗的公開劇照，因此光圈、色盤與構圖屬推論：把面部表情與寫實質感放在災難奇觀前面，工業現場只用實燈與背景暗示。

### Ash Gevorkyan（SCRATCH，與 Aram Gevorkyan）

來源所示：PR Newswire 與官方競賽頁寫五天完成，觀眾誤以為是院線預告片。Higgsfield 提交頁（https://higgsfield.ai/contests/make-your-action-scene/submissions/e142c884-79cc-42ba-961f-04e03ef6f5ab）的劇情是兩具撞擊測試假人逃亡，公開縮圖是暖琥珀光的近景雙人構圖：刮傷的假人臉、運動墨鏡、針織與高領、電影標題字疊在時尚雜誌式親密構圖上。X 帳號 @Gevorkyanshot 簡介為 Directing/photo/retouch/music，但近年公開貼文是 2022 年的攝影／NFT，不能代表 SCRATCH。推論：院線預告感來自高反差、暖色定調、把「非人」或受傷的表面當角色來拍，而不是只堆爆炸。

### TAMBV（GIRLS / DEMONS）

來源所示：官方競賽簡介是 90 年代風動畫，慾望、信任與隱藏的黑暗，混雜愛情、恐怖與霓虹夜生活。Future Lantern 與 Forma 的公開說明（創作者 Lucas Tamburini）把畫面寫成「遺失的 late-90s 日本動畫」：手繪 2D 質感、不完美的運動、霓虹夜晚、綠與琥珀光、雨、散景、車燈、地下空間、憂傷的安靜。不要複製該片角色或東京巷名。推論：時尚與夜生活可以走同一套光色，恐懼用氣氛而不是堆惡魔造型。

### sssacccade 與 curious_media_2026（HUNGER、The Elevator）

來源所示：兩支佳作被 Neon 合成一種「超現實寓言」。HUNGER（sssacccade / Daria Mozhaeva，https://sssacccade.com/en/、https://briefandbutter.com/work/hunger-sssacccade）是無對白、約 4 分 12 秒，把過度消費變成一個會長大的生物；工作室寫要讓奇幻「看起來盡量寫實」，角色與服裝先設計再生成；Brief & Butter 寫明 early-digital-video 的模樣，以及公寓會被物品填滿。The Elevator（官方用戶名 curious_media_2026，對外亦作 Marvs AI / Marvin Curioso）是一場穿越愈來愈超現實樓層的電梯旅程；Starbelo 根據 YouTube 說明寫作法是「先做靜幀再動畫」，工具含 Cinema Studio、Seedance 2.5、Nano Banana、Soul、GPT Image、Seedream。不要用 Lora、Yoki 或對方的九層關卡。推論：寓言靠「一個日常生活容器被一個不可能的事實撐破」，畫面要寫實到讓那個不可能成立。

### Vertex CGI（文化時刻廣告）

來源所示：官方案例 https://higgsfield.ai/creator-hub/case-studies/vertexcgi-higgsfield-nba-finals-case-study 自述是「attention company」：先研究受眾與平台，開會時即時生成分鏡，720p 迭代再 1080p，模型含 Nano Banana Pro、GPT Image 2、Kling 3.0。要讓不同圈內人各自找到彩蛋。X 帳號 @vertex_cgi 的近期 9:16 影片縮圖（來源所示，2026 年 7–10 月）反覆使用同一套手法：把一個大家都認得的地標或典禮改寫成當下文化時刻（時裝周的失重、運動金盃、第一人稱車把），低角度、寫實、前景常有觀眾或手機。本包禁止使用真實品牌、球隊、聯盟或那些地標本身。推論：停滑的關鍵是「一個被改寫的公共符號 + 一個不可能的物理動作」，不是產品棚拍。

### @tupacabra（研究較詳）

來源所示：X 簡介為「UFO RESEARCH & MEDIA」，已認證，網站 http://www.tupa-cabra.com（欄目含 Alien Mummiez、Shadows of the Invisible Sun: UFOs, Consciousness, & the Soul）。約 16.8 萬追蹤、6,116 則媒體。本人貼文寫「Made with @VeniceAI」「Videos generated with @VeniceAI」，並稱自己是 *NUREMBERG* 的唯一作者。2026 年 11 月 13 日（UTC）發布的 *NUREMBERG - Official Trailer* 在 X 上獲得極高轉發；Art Evolves 與 Top5Apps 的分鏡統計寫 86.6 秒、59 個鏡頭、中位長度 1 秒、沒有對口型對白，把都鐸式燭光宮廷、發光的環形門、南極冰牆艦隊、冷戰控制室與現代城市交火硬切在一起。我檢視過的公開縮圖：一張是去飽和藍灰的戰場城市，橘色曳光彈劃過天空，三名戰術裝備的人蹲在屋頂前景，像預告片寬銀幕定格；一張是 9:16 的神話標題卡，整顆燃燒的太陽佔滿畫面，粗黑體標題壓在火球上。另有一張日光紀實風：藍膚、連帽背心的非人形象走在鼓掌的人群中（這類「披露」諧仿不要直接拿真人面孔做）。推論：他的停滑技法是「一幅安靜的預告片靜幀裡，讓兩個不屬於同一時代的世界相撞」，加上電影級反差與留給標題的空間。本包不使用紐倫堡 1561、南極艦隊、美國旗幟的門，或任何真實公眾人物。

---

## S01　PURGA：屋頂上不該出現的東西

- 風格：PURGA Studio 的魔幻寫實對峙
- 領域：日常再創作 × 文學
- 借的技法：把日常屋脊做成剪影舞台，用閃電當唯一主光，讓一個「不該在那裡的物件」像剪紙一樣站在天際線上（來源：AWN 海報劇照與競賽簡介的對峙結構，https://www.awn.com/news/argentinas-listen-meh-wins-500k-higgsfield-ai-film-prize）。
- 設定：2K，9:16。必跑四個 7 天無限次數模型。
- 什麼才不算普通：不是漂亮的夜市風景照。必須是近乎單色的剪影對峙，閃電是主光，蒸籠或屋頂物的輪廓要一眼可读；沒有羊、沒有牧場、沒有高喬人。

```text
Vertical 9:16 almost monochrome film still, a silent standoff after closing time on a narrow Taiwan night-market alley. A weathered corrugated stall roof fills the lower half as a hard black silhouette. On the ridge sits one giant steamed bun, perfectly still, the size of a stray dog, cut out against the sky like a woodblock print. A single lightning bolt is the only key light, freezing the wet alley and a lone adult night-market cook in his fifties looking up from the doorway, face unreadable. Huge storm sky, empty street, no neon color, no crowd, no typography, no watermark.
```

---

## S02　PURGA：水田裡的荒謬對質

- 風格：PURGA Studio 的魔幻寫實對峙
- 領域：電影 × 文學
- 借的技法：廣闊地景裡只放兩造、表情死板、天氣比動作大聲（來源：AWN 對「absurd standoff」與風暴的描述；評審對構圖的強調）。
- 設定：2K，9:16。
- 什麼才不算普通：不是宜蘭風景明信片。辦公椅必須荒唐到令人發笑，卻用嚴肅的電影構圖來拍；人物與物件都很小，天空很大。

```text
Vertical 9:16 cinematic still, Yilan rice paddies at the edge of a storm, deadpan magical realism. In the center of a flooded field stands a perfectly ordinary office swivel chair, upright, unmoving, slightly too clean. A farmer in his forties, clearly adult, in soaked work clothes, stands twenty paces away and stares at it as if in a duel. Low horizon, enormous blue-grey sky, a distant lightning sheet for key light, muddy reflections, 35mm, locked-off, no smile, no crowd, no text, no watermark.
```

---

## S03　AIST：災難只發生在臉上

- 風格：AIST 的災難寫實，表情先於特效
- 領域：電影 × 科技
- 借的技法：把「優秀的寫實與角色表情」當成畫面主體，災難只以失焦的警報與實燈存在（來源：官方競賽頁評審評語，https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=winners）。未見該片劇照，光圈與構圖為推論。
- 設定：2K，9:16。
- 什麼才不算普通：不能靠爆炸、裂開的反應爐或英雄姿態取勝。若把臉裁掉就不再是這張圖，才算通過。不是福島、不是真實核電廠、不是真實災害新聞畫面。

```text
Vertical 9:16 documentary close-up, 85mm, of a 52-year-old East Asian woman, clearly adult, a night-shift supervisor in a fictional metro control room in Taipei. Sweat, tired skin, no beauty retouch. Red emergency practicals stripe her face; a wall of unlabeled alarm lights falls completely out of focus behind her. She is not posing; she has just understood that the system will not hold. Handheld tightness, fine grain, realistic pores, no explosion, no wreckage filling the frame, no readable screens, no typography, no watermark.
```

---

## S04　AIST：公寓樓梯間的颱風

- 風格：AIST 的災難寫實
- 領域：日常再創作 × 電影
- 借的技法：生活空間裡的災難，情緒在身體與臉，奇觀留在畫面邊緣（來源：同上評審對 realism 與 expressions 的強調；場景為原創，推論）。
- 設定：2K，9:16。
- 什麼才不算普通：不是「颱風外拍很帥」。停電樓梯間必須又窄又髒，父親的表情比窗外那一道變壓器閃光重要。

```text
Vertical 9:16 still, documentary handheld, a Taipei walk-up stairwell during a blackout. A 41-year-old father, clearly adult, sits on a concrete step holding a cheap plastic lantern, listening. The typhoon exists only as rain on a narrow window and one distant transformer flash, far out of focus. Dirty practical light, peeling paint, wet sandals, natural skin, 35mm, eye level. No heroic pose, no destroyed cityscape, no logos, no typography, no watermark.
```

---

## S05　Gevorkyan：預告片式的近景定裝

- 風格：Ash Gevorkyan 的院線預告美學
- 領域：時裝 × 電影
- 借的技法：暖琥珀光、高反差、把受傷或非完美的表面當時尚角色來拍的親密雙人近景，看起來像一張預告海報的裁切（來源：SCRATCH 公開縮圖，https://higgsfield.ai/contests/make-your-action-scene/submissions/e142c884-79cc-42ba-961f-04e03ef6f5ab）。禁止撞擊測試假人、禁止該片角色。
- 設定：2K，9:16。
- 什麼才不算普通：不能只是潮牌穿搭照。皮膚或護目鏡上要有刮傷與雨水，構圖要緊到像海報，色調要暖而壓黑，讓人以為這是一部還沒上映的動作片劇照。

```text
Vertical 9:16 theatrical-trailer close still, warm tungsten and crushed blacks. Two adults in their late twenties sit shoulder to shoulder in a Taipei underpass, rain-soaked, not posing for a catalog. One wears a cracked sport visor and a black turtleneck; the other a soaked knit and dark glasses. Scuffs and rain on skin and plastic read as character, not glamour retouch. Tight two-shot, shallow depth, amber grade, filmic contrast, breathing room at the bottom for a title that is not generated. No mannequins, no crash-test dummies, no logos, no typography, no watermark.
```

---

## S06　Gevorkyan：會被誤認作院線預告的一格

- 風格：Ash Gevorkyan 的院線預告美學
- 領域：電影 × 日常再創作
- 借的技法：五天內做出「觀眾以為有全片」的預告完成度——低角度、濕地反光、變形鏡頭光斑、被凍結的動作（來源：PR Newswire 引述 Ash「They actually thought it was a real trailer for an existing film.」，https://www.prnewswire.com/news-releases/the-largest-ai-film-competition-highlights-emerging-trends-in-global-ai-filmmaking-302717810.html）。
- 設定：2K，9:16。
- 什麼才不算普通：不是帥的機車廣告。必須有電影院預告的體積感與危險，下三分之一留空，沒有產品標誌。

```text
Vertical 9:16 action-trailer still, low angle, wet riverside expressway in Taipei at night. A lone adult scooter courier, mid-thirties, frozen mid-lean at speed, a sheet of white-hot sparks blooming behind the bike like a curtain. Anamorphic horizontal flare, crushed blacks, slick asphalt reflections, theatrical contrast, 35mm slightly wide. The lower third stays empty for a title that is not generated. No brand on the helmet or bike, no readable road signs, no crowd, no watermark.
```

---

## S07　TAMBV：綠與琥珀的雨夜動畫

- 風格：TAMBV 的 90 年代動畫與霓虹夜生活
- 領域：時裝 × 藝術
- 借的技法：手繪 2D、晚九零年代動畫質感、綠與琥珀光、雨、散景、憂傷的安靜（來源：Future Lantern 對 GIRLS / DEMONS 畫面的公開描述，https://futurelantern.com/film/2a3dee75-01e1-48d0-a8f9-9c2eac6dc7ef；官方競賽簡介的 neon-soaked nightlife）。不要複製該片角色或惡魔形象。
- 設定：2K，9:16。
- 什麼才不算普通：不是現代 3D 動漫或光滑的 AI 插畫。必須看得出賽璐璐與不完美線條，光色是綠對琥珀，雨要在空中。

```text
Vertical 9:16 still in the manner of a lost late-1990s 2D anime frame, not 3D CGI. Two adults in their mid-twenties stand under a pedestrian overpass in Ximending, Taipei, not speaking. Green neon from a fictional arcade sign versus warm amber sodium from the street, heavy rain, bokeh, drifting taillights, cel shading with slightly imperfect linework and visible paint texture. Melancholic, quiet, full figures in frame, shallow nocturnal depth. No demons, no fangs, no logos, no typography, no watermark.
```

---

## S08　TAMBV：凌晨便利商店的動畫靜幀

- 風格：TAMBV 的 90 年代動畫與霓虹夜生活
- 領域：日常再創作 × 時裝
- 借的技法：把最普通的深夜消費空間，用同一套綠／琥珀光與手繪質感拍成心理戲的一格（來源：同上；場景為原創）。
- 設定：2K，9:16。
- 什麼才不算普通：不是開架商品照。玻璃上的雨與冰箱的綠光要壓過商品，人物像在一場還沒發生的心理恐懼裡，但畫面裡沒有怪物。

```text
Vertical 9:16 late-90s 2D anime still, 2 a.m. inside a small unlabeled corner convenience store in Taipei. A 24-year-old woman, clearly adult, stands at the glass door with a canned coffee, looking out at the rain. Interior light is cold green from the drink cases; outside is amber street rain on the pane. Hand-drawn line, imperfect cel texture, quiet psychological tension, no monster in frame. No readable chain-store logo, no prices, no typography, no watermark.
```

---

## S09　超現實寓言：消費長出形狀（HUNGER 的結構）

- 風格：sssacccade 的消費寓言
- 領域：藝術 × 日常再創作 × 趨勢（過度包裝／外送）
- 借的技法：無對白、把慾望變成一個可被看見且持續變大的生物，公寓作為容器，早期數位錄像質感，奇幻卻要寫實（來源：https://briefandbutter.com/work/hunger-sssacccade 、https://sssacccade.com/en/）。禁止 Lora、Yoki 或「靠丟棄物長大」的同一設定。
- 設定：2K，9:16。
- 什麼才不算普通：不是一張「房間很亂」的生活照。生物必須由外送泡沫與膠帶長出來，並與狹窄的台北公寓處於同一個寫實光源裡。

```text
Vertical 9:16 dialogue-free allegorical still, early-digital-video texture, slightly soft and over-lit like a 2000s home camera. In a tiny Taipei walk-up living room, a 29-year-old woman, clearly adult, has just opened another delivery bag on the low table. Behind the sofa, a fictional creature formed of packing foam, tape and receipt paper has grown to the size of an armchair, its mouth mid-chew, still lit by the same cheap ceiling bulb as the room. Realistic space continuity, no jump into fantasy lighting. Unmarked packaging, no real courier logos, no typography, no watermark.
```

---

## S10　超現實寓言：門打開是另一個世界（The Elevator 的結構）

- 風格：curious_media_2026 / Marvs AI 的樓層寓言
- 領域：科幻 × 文學 × 日常
- 借的技法：以日常容器（電梯）做重複結構，每一層只透露一個不可能；先當成靜幀來構圖（來源：官方競賽簡介；Starbelo 對「stills first, then animate」的整理，https://starbelo.com/use-case/the-elevator-ai-comedy-thriller-higgsfield-seedance-88k/）。不要用對方的九層關卡或洗衣房生物。
- 設定：2K，9:16。
- 什麼才不算普通：電梯內部必須完全寫實（鏡面、按鈕、日光燈），門外卻是被壓縮進來的稻田；兩個空間共用一個門框，沒有夢幻濾鏡把兩邊抹平。

```text
Vertical 9:16 locked-off still, a standard municipal elevator interior in Taipei, fluorescent, scratched steel, unmarked buttons, slightly dirty mirror. The doors are half open. Beyond the threshold, instead of a lobby, a flooded rice paddy at dusk is packed into the shaft, wind moving the stalks, a single egret in the distance. An adult office worker in his thirties stands in the lift in wet shoes, one hand holding the door, face caught between comedy and dread. Documentary elevator lighting inside, natural dusk outside, both worlds sharing one door frame. No text on the buttons, no logo, no watermark.
```

---

## S11　Vertex：把公共符號改寫成文化時刻

- 風格：Vertex CGI 的工業級文化時刻廣告
- 領域：趨勢二創 × 科技
- 借的技法：選一個大家都認得的城市符號，為一個正在發生的集體時刻做不可能的改寫，9:16 低角度、寫實、前景有圍觀者或手機（來源：NBA Finals 案例的受眾與彩蛋思維，https://higgsfield.ai/creator-hub/case-studies/vertexcgi-higgsfield-nba-finals-case-study；以及 @vertex_cgi 近期 9:16 縮圖反覆出現的「地標被改寫」構圖）。禁止真實球隊、聯盟、商標與外國地標翻拍。
- 設定：2K，9:16。
- 什麼才不算普通：不能是 101 的觀光照或普通煙火。塔身必須被一項虛構的慶典裝置改寫，前景要有人舉手機，像一則會被轉發的文化廣告。

```text
Vertical 9:16 photoreal cultural-moment still, low angle at dusk, Taipei 101 seen from a plaza. The tower is not a postcard: a colossal fictional championship lantern, coral and gold, is docked against the facade as if the building itself were holding it up, lighting the glass. In the immediate foreground, adult spectators raise phones, slightly out of focus. Clean commercial realism, crisp twilight, 24mm, no real team names, no league marks, no sponsor logos, no typography, no watermark.
```

---

## S12　Vertex：第一人稱看見不可能的遊行

- 風格：Vertex CGI 的工業級文化時刻廣告
- 領域：趨勢二創 × 日常再創作
- 借的技法：第一人稱載具前景 + 失重或改寫過的公共空間，讓觀眾覺得自己在現場（來源：@vertex_cgi 縮圖中的車把前景與「gravity optional」構圖邏輯；案例中「why people will care enough to stop scrolling」）。
- 設定：2K，9:16。
- 什麼才不算普通：不能只是機車行車紀錄器。夜市攤車必須離地漂行，手把要在畫面底部，透視要像現場廣告而不是插畫。

```text
Vertical 9:16 photoreal still from a moving scooter, first-person, handlebars sharp in the lower frame. On a familiar Taipei overpass at night, a procession of night-market stall carts floats a meter above the asphalt, their lamps level, steam trailing, no wheels touching the road. Adult passengers on the carts hold oil-paper lamps. Practical tungsten and motorcycle headlight, slight motion smear only in the far lights, 24mm. No real stall brands, no readable prices, no typography, no watermark.
```

---

## S13　tupacabra：兩個時代在同一格相撞

- 風格：@tupacabra 的沉默預告片碰撞
- 領域：科幻 × 文學／史
- 借的技法：無對白的預告片靜幀，把本地歷史空間與一個無法歸類的發光幾何體硬切在同一構圖裡，去飽和、電影反差、上方留標題空間（來源：Art Evolves 與 Top5Apps 對 *NUREMBERG* 鏡頭碰撞與無對白剪接的描述，https://www.artevolves.com/culture/the-phenomenon-that-is-tupacabra/ ；以及該預告公開縮圖的去飽和城市＋前景人物剪影）。禁止紐倫堡、南極、國旗門、真實歷史名人。工具備註：作者公開寫使用 Venice；本測試仍在 higgsfield.ai 用免費 2K 模型跑同一構圖邏輯。
- 設定：2K，9:16。
- 什麼才不算普通：不能是俗套飛碟疊在風景上。廟埕與磚倉必須像歷史照片，光環必須像工業幾何而不是漫畫飛碟；沒有人看鏡頭，沒有字幕。

```text
Vertical 9:16 silent trailer still, desaturated cinematic grade. Dusk in a Japanese-era brick sugar warehouse courtyard on the southwest Taiwan coast. A small temple procession of adults in older work clothes is frozen mid-step among sugar carts, faces not toward camera. In the courtyard, a vast unlabeled ring of hard white light stands upright, industrial and geometric, not a saucer, not a national flag, pouring a column of light into the bricks. 35mm, locked-off, crushed blacks, headroom in the upper third for a title that is not generated. No typography, no watermark, no recognizable public figures.
```

---

## S14　tupacabra：神話標題卡，字是留白而不是亂生

- 風格：@tupacabra 的沉默預告片碰撞
- 領域：藝術 × 科幻
- 借的技法：9:16 單物件神話標題卡，一個佔滿畫面的天體或光孔，粗體標題的位置被留白，作者字級的簽名位置保持乾淨（來源：X 貼文 *The Book of Enoch - 2050* 的公開縮圖構圖，https://x.com/i/status/2118745374349476266）。不要生成「ENOCH」或任何真實經文書名。
- 設定：2K，9:16。
- 什麼才不算普通：不是一般的日出美圖。必須是垂直的、近乎圖騰的構圖，中央一塊刻意留白給標題，火焰或光孔要有物質感，沒有亂字。

```text
Vertical 9:16 mythic title-card still, silent, no people. Over the dark Taiwan Strait at night, a perfectly circular aperture of pale machine-fire hangs above the water, large enough to dominate the frame, textured like burning metal rather than a pretty sun. The exact center of the fireball is kept visually quiet, a dark untextured disc left empty for typography that must not be generated. High contrast, black sky, faint clouds, 50mm, no land marks, no readable text, no logo, no watermark.
```

---

## 使用順序

1. 先跑 S01 到 S14 的必跑四模型（與 `run-guide.md` 第一輪相同）。
2. 用各則「什麼才不算普通」當硬標準；五維評分仍填 `results.csv`，可在 `notes` 標 `pack=style`。
3. 若某則四個模型都普通，先改提示詞再重測，不要立刻進影片。

---

## S13 / S14 改版（依《NUREMBERG》官方預告拆解，2026-11-21）

來源：[@tupacabra NUREMBERG - Official Trailer](https://x.com/tupacabra/status/2121357879341166683)（87 秒，約 3,500 萬觀看）。拆解重點：bleach bypass 去飽和、冷石板灰與冰藍；只留橘火與藍白光環當暖冷重點；中央對稱構圖，用巨大建築或科技物壓小人物；天空物件佔上三分之一、從低雲中破出；跨時代道具相撞（古代服裝 × 軍事科技）；體積霧與神光、科技物給輪廓光；全畫面有機膠片顆粒、降低微反差以去除 AI 塑膠感；標題置中、白色寬字距無襯線（本測試不生成文字，只留位置）。

S13 v2
```text
Vertical 9:16 cinematic trailer still, bleach-bypass grade, desaturated cold slate grey and icy blue, heavy organic film grain, subdued micro-contrast, no plastic AI sheen. Inside a vast Japanese-era railway workshop hangar in Taipei, rows of steel trusses vanish into fog. Perfectly symmetrical, center-weighted: a line of adult soldiers in plain 1940s-style uniforms with no insignia stand at attention, dwarfed by a colossal upright ring of blue-white energy at the far end of the hangar, its light rim-lighting their silhouettes and cutting god rays through the haze. Beside them, one Qing-dynasty temple elder in dark robes holds an incense stick, its orange ember the only warm accent. 35mm, locked-off, eye level. No flags, no insignia, no typography, no watermark.
```

S14 v2
```text
Vertical 9:16 epic wide trailer still, bleach-bypass grade, desaturated grey sea and icy blue sky, heavy organic film grain, subdued micro-contrast. On a coastal road at the foot of sheer east-coast Taiwan sea cliffs under a low overcast ceiling, a silent night-time temple pilgrimage procession of adults carries a carved palanquin and a line of orange torches, small and center-weighted in the lower third. In the upper third, a colossal matte-black disc-shaped craft breaks through the low cloud, enormous in scale, its underside faintly rim-lit by the torches, fog pouring off its edge. Symmetrical composition, ultra-wide 18mm, slight low angle, a dark empty band at the exact center of the frame left quiet for a title that must not be generated. No readable text, no logos, no recognizable people, no watermark.
```
