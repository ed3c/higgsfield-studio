# 免費圖像提示詞測試包

目的：在扣點之前，先用 higgsfield.ai 網站上的免費／無限次數 2K 圖像模型，檢驗提示詞質量，以及頂尖創作者公開手法轉成的範本，是否達到 Neon 的期望。通過之後，再進影片或正式生產。

規則：

- 只生成靜態圖，不生成影片。
- 只在 [higgsfield.ai](https://higgsfield.ai) 網站手動跑（或由瀏覽器代理按本目錄的 `run-guide.md` 操作）。
- **禁止**使用 Higgsfield MCP、CLI，或任何聊天室連線的生成工具：那些路徑一律扣點。
- 設定固定為 **9:16、2K**。不要選 4K。
- 按下生成前，必須確認生成鍵顯示 0、Unlimited、無限或免費。出現任何點數就停止，見 `run-guide.md`。

本目錄檔案：`prompts.md`（本檔）、`rubric.md`、`results.csv`、`run-guide.md`。成品圖放 `outputs/`，不要提交進 git。

說明用繁體中文。送給模型的提示詞用英文，請整段複製，第一輪不要自行加修飾或負面清單。

## 模型怎麼分

優先用 7 天 2K 無限次數模型（2026 年 11 月 20 日起，約至 11 月 27 日，以網站標示為準）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare。

**每一則都先跑這四個**，順序固定：Nano Banana Pro → Seedream 5.0 Pro → GPT Image 2.6 → GPT Image 2.6 Flare。這是必跑，也是判定提示詞是否通過的依據。四個都跑完、十二則都有結果之後，才考慮方案內含的可選對照。

方案內含、只當可選對照（不要插進第一輪）：Nano Banana、Kling O1 Image、Seedream 4.5、Seedream 5.0 Lite、FLUX.2 Pro（2K）。每則只列一個，用來看看促銷結束後還有沒有堪用的備案。

若生成鍵對某個模型顯示點數，立刻停止該次，在 `results.csv` 記下當時標價，改試同一輪的下一個模型。

必跑模型（十二則相同）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare

| id | 用途 | 可選對照（方案內含，第二輪） |
| --- | --- | --- |
| T01 | 樣片 A 鉤子：瓶身微距水珠 | FLUX.2 Pro |
| T02 | 樣片 A 主視覺：霧中瓶身與標籤字 | Nano Banana |
| T03 | 樣片 B 自拍鉤子：小芮出站 | FLUX.2 Pro |
| T04 | 樣片 B 產品證據：開蓋熱氣與三點鐘 | Seedream 5.0 Lite |
| T05 | 樣片 C 開場：雨夜霓虹巷弄 | FLUX.2 Pro |
| T06 | 樣片 C 高潮：巷弄變成深海 | Seedream 4.5 |
| T07 | 時裝：捷運穿搭定場 | FLUX.2 Pro |
| T08 | 電影：空場景藍時 | Kling O1 Image |
| T09 | 科幻：近未來街道空景 | Kling O1 Image |
| T10 | 藝術：同一隻摺紙鶴三種材質 | Seedream 4.5 |
| T11 | 科技：無商標器物主視覺 | FLUX.2 Pro |
| T12 | 日常再創作：窗邊早餐電影感 | Seedream 5.0 Lite |

T01–T06 取自 `portfolio/plan.md` 三支 9:16 樣片的關鍵靜幀（每支兩張）。T07–T12 取自 `prompts/by-domain/` 與 `skills/daily-life-remix/` 的原創模板，占位符已填成可直接送出的句子；手法對齊 `creators/study-queue.md` 的公開做法，不複製任何成片、角色或未授權客戶素材。全部是虛構品牌與虛構成年人。

---

## T01　樣片 A 鉤子：瓶身微距水珠

- 作品：霧嶼冷泡烏龍《山霧凝成一瓶》，分鏡 1（0–4 秒鉤子）。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：FLUX.2 Pro
- 設定：2K，9:16。文字轉圖像，本輪不放產品參考圖。
- 出處／模仿：電影級產品主視覺。鏡頭寫法對齊官方 skill `higgsfield-generate` 的 `prompt-engineering.md`（主體、鏡頭、光線）。微距與產品氣氛參考官方 Cinema Studio Prompt Guide 的技法名稱，提示詞為原創，不是該文範例。
- 通過：畫面英雄是單一顆清晰的冷凝水珠，沿弧形玻璃下滑；瓶內是琥珀金烏龍；背景是失焦的晨霧山脈；100mm 微距、極淺景深成立；9:16 構圖完整，沒有左右被裁切的感覺；這一格看不到標籤字、手或商標。

```text
Vertical 9:16 extreme macro still of a single condensation droplet sliding down the curved glass of a tall clear cold-brew tea bottle. Amber-gold oolong tea inside the bottle. Behind the glass, soft dawn mountain fog and dark forested peaks fall out of focus. 100mm macro, f/2.8, tack-sharp on the droplet highlight, shallow depth of field, cool daylight and a faint warm rim on the glass edge. Unmarked glass in this frame, no typography, uninhabited, no watermark.
```

---

## T02　樣片 A 主視覺：霧中瓶身與標籤字

- 作品：霧嶼冷泡烏龍，分鏡 5（產品定格／品牌卡之前的瓶身英雄鏡）。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Nano Banana
- 設定：2K，9:16。文字轉圖像。
- 出處／模仿：與 T01 同一支電影級產品主視覺；產品標籤是 typography 壓力測試。官方 prompt-engineering 的主體＋鏡頭＋光線句法。品牌「霧嶼 MISTISLE」為虛構。
- 通過：瓶子與 T01 的設定一致（透明玻璃、鼠尾草綠霧面鋁蓋、琥珀金茶液）；站在長青苔的岩石上，晨霧繞底；標籤只含三行字，且拼寫完全正確：繁體「霧嶼」（不是「雾屿」）、大寫「MISTISLE」、小字無襯線的「COLD BREW OOLONG」；沒有多餘單字、條碼或價格；構圖低角度，上三分之一留空氣；沒有手或其他品牌。和 T01 對看時，瓶型與蓋色要認得出是同一支瓶子（記入 consistency）。

```text
Vertical 9:16 cinematic product hero still. A tall clear glass bottle of cold-brew oolong stands on a mossy dark rock, morning mountain fog curling around the base. Matte sage-green aluminum screw cap. A narrow cream paper label band at mid-height with typography only, exact spelling: first line the Traditional Chinese characters 霧嶼, second line MISTISLE in wide-tracking serif capitals, third line COLD BREW OOLONG in small sans-serif. Amber-gold liquid, fine condensation. Low angle, 50mm, soft dawn light from camera left, thin fog. Breathing room in the upper third. Unmarked besides that label, no barcode, no price, uninhabited, no watermark.
```

---

## T03　樣片 B 自拍鉤子：小芮出站

- 作品：圈圈杯 LOOPA《通勤三年終於不漏》，分鏡 1（手持自拍出站）。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：FLUX.2 Pro
- 設定：2K，9:16。文字轉圖像。不要訓練 Soul ID（要扣點）。
- 出處／模仿：UGC 創作者口碑廣告。官方 Marketing Studio 把 UGC 定位成「像手機拍的」，這裡只測靜幀真實感。人物是虛構的 26 歲成年人小芮，不是真人。
- 通過：看起來像手機自拍，不是棚拍廣告；皮膚有自然質感，不過度美顏；人物明顯是二十多歲成年人；手持鼠尾草綠、雙環蓋不鏽鋼隨行杯；背景是通用捷運出口，沒有真實站名或捷運商標；路人臉不可辨識；沒有 App 介面或字幕；9:16 頭腳大致完整，沒有變形過度的大頭。

```text
Vertical 9:16 handheld smartphone selfie still, casual UGC look, slight motion softness, natural skin texture, not beauty-retouched. An East Asian woman in her mid-20s, clearly adult, about 26: short wavy black hair, light makeup, oversized oatmeal knit sweater. In the hand closest to camera she holds a sage-green stainless-steel tumbler with a distinctive double-ring lid. She has just stepped out of a generic underground metro exit with no readable station name and no transit logos. Overcast daylight, eye level, slight 26mm phone wide-angle. Background pedestrians are unreadable blurs. No app interface, no captions, no watermark.
```

---

## T04　樣片 B 產品證據：開蓋熱氣與三點鐘

- 作品：圈圈杯 LOOPA，分鏡 5（桌面近景，時鐘指三點、開蓋冒熱氣）。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Seedream 5.0 Lite
- 設定：2K，9:16。文字轉圖像。
- 出處／模仿：UGC 證據鏡，對齊庫內 `ugc-packshot-space` 的留白與產品清晰度。杯子是虛構產品，蓋型要能與 T03 對上。
- 通過：鼠尾草綠不鏽鋼隨行杯、雙環蓋剛打開，有看得見的熱氣；杯身沒有字、沒有商標；背景虛化的類比時鐘清楚指在 3:00；右側約三分之一偏空；沒有電腦介面或其他品牌；和 T03 對看時，杯子顏色與蓋型一致。

```text
Vertical 9:16 desk still. A sage-green stainless-steel travel tumbler with a distinctive double-ring lid sits slightly left of center, the lid just opened, a visible wisp of steam rising. Soft-touch cylinder body, unmarked. In the softly blurred background an analog wall clock reads exactly 3:00. Neutral office, 50mm, warm practical lamp plus cool window light. The right third of the frame stays mostly empty. No computer interface, no typography on the cup, uninhabited, no watermark.
```

---

## T05　樣片 C 開場：雨夜霓虹巷弄

- 作品：TIDE LAB 深海夜行外套《城市漲潮的那一晚》，分鏡 1。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：FLUX.2 Pro
- 設定：2K，9:16。文字轉圖像。
- 出處／模仿：超現實時裝大片開場。時裝構圖參考 Aleksandra（官方 Creative Partner，時裝與編輯設計）與 TAMBV（時裝商業完成度）的公開定位：世界觀先於單品，不是一張平拍型錄。外套與巷弄為原創設定。
- 通過：全身入鏡、略低機位的時裝編輯感；炭黑機能外套上的有機反光條接住青與洋紅霓虹；地面有積水倒影與細雨；招牌是看不懂的自創字，認不出真實品牌或店名；人物明顯是二十多歲成年人；沒有潛水裝備；9:16 頭上與腳下留得住。

```text
Vertical 9:16 fashion editorial still, low angle, full body. A 24-year-old East Asian model, clearly adult, stands in a narrow rainy city alley at night. They wear a matte charcoal technical shell with irregular organic reflective tape that catches neon like a living pattern, hood up, black trousers, practical boots. Fictional neon signs in invented lettering, not readable as a real brand or a real shop name. Wet asphalt reflections, cyan and magenta neon, fine rain. 35mm, slightly low eye level, shallow depth. No scuba gear, no watermark.
```

---

## T06　樣片 C 高潮：巷弄變成深海

- 作品：TIDE LAB 深海夜行外套，分鏡 4（巷弄淹成深海，水母漂過）。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Seedream 4.5
- 設定：2K，9:16。文字轉圖像。
- 出處／模仿：實拍做不到的超現實高潮鏡。與 T05 同一世界觀。One of One Studio 官方案例的教訓是「世界先於單品」：先讓巷弄變成海域，外套只是其中一件可辨識的衣服。不複製任何得獎短片的角色或場面。
- 通過：同一條磚牆巷弄已充滿海水，水母在身邊漂；同一件炭黑、有機反光條外套，頭髮與下擺開始失重上飄；人物仍像在走路，表情冷靜；青光體積光，沒有潛水裝備、沒有真實商標；和 T05 對看時，人物與外套認得出是同一套造型。

```text
Vertical 9:16 surreal fashion still, wide shot. The same rainy brick alley has flooded into a deep-sea volume: the walls continue downward, water fills the street, bioluminescent jellyfish drift past. The same 24-year-old East Asian adult model in the matte charcoal technical jacket with organic reflective tape walks forward as if on a sidewalk, hair and hem beginning to float, calm expression. Volumetric shafts of cyan light, floating particles, cinematic grade, 35mm, slight low angle, full body with headroom. No scuba gear, no readable signage, no watermark.
```

---

## T07　時裝：捷運穿搭定場

- 來源模板：`prompts/by-domain/fashion.md` 的 `fashion-mrt-lookbook`，占位符已填。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：FLUX.2 Pro
- 設定：2K，9:16。
- 出處／模仿：Tseily（官方 Creative Partner，電影感日常）＋ Aleksandra（時裝編輯）。技巧是把日常站體變成 lookbook 定場，不是換一張臉。站名與廣告都保持不可讀。
- 通過：全身入鏡、85mm、淺景深成立；人物往前踏出一步，身後車門打開；冷螢光加一盞月台暖燈；衣服是炭黑大衣＋奶油針織＋寬褲，讀得清楚；沒有真實站名、沒有可讀廣告、沒有清楚的路人臉；9:16 沒有切到頭頂或腳。

```text
Vertical 9:16 fashion still on a metro platform with ribbed concrete pillars and a curved ceiling, no readable station name. A young East Asian woman in her mid-20s, short black bob, wearing a charcoal wool oversized coat over a cream knit and wide black trousers, one step forward as the train doors open behind her. 85mm, eye level, shallow depth of field, cool fluorescent light plus one warm practical on the platform edge. Full body in frame. Unmarked architecture, no readable ads, crowd faces stay unreadable, no watermark.
```

---

## T08　電影：空場景藍時

- 來源模板：`prompts/by-domain/film.md` 的 `film-empty-location`，占位符已填。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Kling O1 Image
- 設定：2K，9:16。
- 出處／模仿：JOEY（官方 Community Creators；公開流程是角色參考與空場景分開，再進影片）。製作順序來自官方文章 How to Master AI Filmmaking。這張只鎖光向與空間，不放人。也對齊 AIST 對完成度的要求：光線方向要清楚到下一鏡接得下去。
- 通過：完全沒有人；看得到地板、一盞實燈、一扇窗或門洞作為縱深；站立視高、35mm；暖燈在左、藍時窗光在右，光向清楚；沒有可讀海報或真實人物照片；這一張要能當後續角色進場的場地參考。

```text
Vertical 9:16 empty location of a small Taipei walk-up apartment living room at blue hour. Uninhabited. A worn wooden floor, one warm practical table lamp on the left, a sliding window on the right with cool residual daylight, a doorway in the background as a depth cue. Camera at standing eye height, 35mm, locked-off. Light direction is obvious enough to reuse: warm key from the lamp, cool fill from the window. Bare walls, no readable posters, no photographs of people, no watermark.
```

---

## T09　科幻：近未來街道空景

- 來源模板：`prompts/by-domain/sci-fi.md` 的 `scifi-street-plate` 與 `scifi-signage-lock`，合成一張可單次測試的近未來空景。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Kling O1 Image
- 設定：2K，9:16。
- 出處／模仿：Yoav Yariv（GFF 2026 佳作 *Soulless* 的公開題旨：人與機器的關係，不一定靠爆炸）。先鎖真實台北街道結構，只加燈條與一枚無字懸浮指示，不加飛行車或可讀店名。
- 通過：低樓建築量體、機車道、騎樓／遮雨棚線仍然像真實街廓；黃昏、濕柏油、店燈倒影；近未來元素只有遮雨棚上的細燈條，以及車道上方一枚沒有文字的小型懸浮指示；沒有人、沒有可讀店名、沒有飛行車；9:16 有路面與天空（或樓高）的縱深。

```text
Vertical 9:16 empty street plate of a Taipei side street at dusk after rain. Keep realistic low-rise building masses, a scooter lane, and a continuous awning line. Wet asphalt with practical shop-light reflections. Add only two near-future elements: thin practical light strips along the existing awnings, and one small unlabeled hovering indicator above the lane. Uninhabited, no readable shop names, no franchise architecture, no flying cars, no watermark.
```

---

## T10　藝術：同一隻摺紙鶴三種材質

- 來源模板：`prompts/by-domain/art.md` 的 `art-sketch-materials`，主題填「摺紙鶴」。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Seedream 4.5
- 設定：2K，9:16。直式三格（上／中／下）比左右三格更適合 9:16。
- 出處／模仿：Aleksandra（官方 Creative Partner，時裝與藝術教育）。方法論要能「把風格說成可以教的東西」：同一構圖、三種材質。不畫受保護角色。
- 通過：三格是同一隻鶴、同一裁切、同一姿勢；上格乾木炭與暖色紙、中格薄油畫可見筆脊、下格釉陶浮雕；北向柔光；沒有簽名、沒有文字、沒有畫框；三格寬度對齊，沒有變成海報拼貼。

```text
Vertical 9:16 still, three equal stacked panels of the same paper origami crane made by one hand. Top panel: dry charcoal on warm paper. Middle panel: thin oil paint with visible brush ridges. Bottom panel: glazed ceramic relief of that same crane. Same pose, same crop in every panel, soft north light. No text, no signature, no frame on the wall, no watermark.
```

---

## T11　科技：無商標器物主視覺

- 來源模板：`prompts/by-domain/tech.md` 的 `tech-object-hero`，器物填「無標誌霧黑手持收聽器」。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：FLUX.2 Pro
- 設定：2K，9:16。
- 出處／模仿：Boxel Studio 官方案例所代表的工業級預視：器物清楚、光向可控、右側留白給後製，不是科幻海報。AIST 的啟示是完成度先於堆模型。禁止做成真實公司的產品照。
- 通過：單一霧黑圓角手持器物，只有一顆未亮的 LED 點，沒有商標、沒有螢幕字；石墨色工作檯；一道硬質條燈劃過表面；右側約三分之一留空；85mm 產品照質感；沒有手。

```text
Vertical 9:16 hero still of an unlabeled matte-black handheld listening device, a rounded rectangle with one unlit LED dot, sitting on a matte graphite bench. One hard strip of light across the surface, dark background, the right third empty for a later caption. 85mm product photography. No logo typography, no interface, no screen text, uninhabited, no watermark.
```

---

## T12　日常再創作：窗邊早餐電影感

- 來源技能：`skills/daily-life-remix/SKILL.md`（把餐桌與窗光重拍成電影靜幀；先鎖場景，臉不是重點）。
- 必跑模型（先跑，依此順序）：Nano Banana Pro、Seedream 5.0 Pro、GPT Image 2.6、GPT Image 2.6 Flare
- 可選對照（四個必跑都完成後再考慮）：Seedream 5.0 Lite
- 設定：2K，9:16。
- 出處／模仿：Tseily（官方 Creative Partner，電影感日常）。要讓人看得出「這是普通早餐」，同時有 35mm、淺景深與青琥珀調的電影完成度。不換成另一個人的一天，不出清晰臉。
- 通過：認得出茶碗、蔥油餅、豆漿與筷子的尋常餐桌；左方窗光切過蒸汽；35mm、坐姿視高、細微膠片顆粒、青與琥珀色級成立；若有手，只在畫面邊緣，沒有臉；沒有包裝商標，沒有可讀的手機螢幕；9:16 桌面與窗都在框裡。

```text
Vertical 9:16 cinematic still of a small Taipei apartment breakfast table at 7 a.m., an ordinary morning remade as a film frame. A ceramic rice bowl, a plate of scallion pancake, a glass of soy milk, chopsticks, window light from camera left cutting across steam. 35mm, seated eye height, shallow depth of field, fine film grain, teal-and-amber grade, one plant in the background. Adult hands may rest at the edge of the frame; no face. Unmarked tableware, no packaged-food logos, no readable phone screen, no watermark.
```
