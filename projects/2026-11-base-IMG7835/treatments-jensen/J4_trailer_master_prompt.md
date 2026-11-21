# J4《非同步：繼承 ASYNC: SUCCESSION》— Higgsfield 工業級預告片主提示詞

> 由 `build_j4.py` 從 `j4_shots.json` 產生（2026-11-22，台北時間）。**這份文件 0 點**：只寫提示詞，沒有任何生成、沒有 MCP／CLI／Canvas 呼叫。
> 生成前必須：(1) Neon 明確批准；(2) Director 先把估點貼到「AI Video Production Service」聊天室；(3) 確認當月 9,000 點上限還夠。

## 0A. 比賽資格（Higgsfield Talent Contest）先看這裡

已查證的取消資格條件：第三方受保護 IP（角色、系列作品、品牌、商標、音樂、美術作品）；政治聲明、背書、宣傳或不實資訊；宗教聲明或貶抑；誹謗；任何可辨識的真人（**包含參賽者本人**與公眾人物，不論用什麼方式，包括實拍影片），以及模仿真人的聲音。

所以本文件有兩個版本：**作品集版**（完整寓言，不投稿）與**比賽版**（照下表抽象化）。比賽版原則：不把任何國家或宗教主張寫成陳述，只留曖昧；不借任何品牌、系列或電影角色的外型；不出現任何真人，也不出現 Neon 本人。

| 劇本元素（Neon 的原始要求） | 比賽資格 | 比賽版的安全抽象化 |
| --- | --- | --- |
| 黃仁勳／NVIDIA 的故事、黑皮衣 | 不可（可辨識的公眾人物、品牌） | 虛構創辦人；無特徵的深色舊工作外套；拿掉傳記線索（桌球、Denny's） |
| CFO 繼任 CEO、「長得像飢餓遊戲角色」 | 不可（真人＋系列作品 IP＋可能構成不實資訊） | 虛構公司裡的虛構交接；管家只借「篡位的管家」故事功能，不借柯茵的外型、服裝、演員 |
| Mockingjay／#BringJensenBack | 不可（系列 IP；對真人的呼籲） | 自創的鎢絲光鳥；人群舉起的是無特徵的外套；畫面與字幕都沒有 hashtag |
| 川普、普丁、習近平；深圳接待的大國座次 | 不可（真人、政治陳述） | 三個抽象彩色光柱或無冠幾何棋子；一般會議桌與被推開的椅子；不出現城市地標、國家配色、真實事件引語 |
| 美國、以色列爭 AI 霸權的宗教隱喻 | 不可（宗教與政治陳述） | 沙漠裡發光的光纖灌木與未完成的機櫃塔；不引經文、不出現宗教典故或國家 |
| 金牛犢（市值崇拜） | 不可（宗教典故） | 晶片鑄的巨大金燈泡 |
| 中國情婦 | 不可（族群／性別刻板、政治影射） | 只在作品集版；比賽版改成一條橫過空宴會廳的紅色電話線 |
| 華人不接受猶太人的受害心理 | 不可（宗教／族群陳述） | 只在作品集版；比賽版改成兩個走速不同的時鐘 |
| 美國左派女權 vs 男性被邊緣化（坂本眼鏡＋皮衣） | 不可（政治陳述；眼鏡＋皮衣可辨識真人） | 不出現口號與立場台詞；普通眼鏡、普通外套被關進鐵籠，只留畫面 |
| 女性回歸家庭、AI 取代女性勞動、中國體制壓制女權 | 不可（政治陳述） | 空凳子的廠房（不配主張）；手在圍裙與實驗袍之間猶豫、不做選擇 |
| 移民不再是資產；單一文化生育＝國家穩定 | 不可（政治陳述） | 閘門與機器人並行、兩人用不同節奏織線；都不配台詞 |
| 日本半導體衰落、歐洲邊緣化 | 可，只要不陳述事實 | 泡水鋼琴、白色無塵衣、空歌劇院；不出現國旗、地名、數據 |
| 台灣夜市的日常與安全感 | 可 | 通用夜市；不加國名字卡 |
| AI 開源 vs 閉源 | 可，只要不點名 | 共享的紙燈籠 vs 上鎖的黃銅燈；不寫任何公司或模型名 |
| 坂本龍一的音樂理論 | 可（只借理論） | 不用他的錄音、旋律、取樣、肖像、聲音；配樂全部 AI 原創 |
| Neon 的 IMG_7835 原片（S03、S17、S18、S23） | 不可（參賽者本人可辨識，含實拍影片） | 比賽版不用任何 plate；這四鏡改用 Cinema Studio 4.0 生成虛構 AI 主角（Soul ID 鎖臉），S18 全黑段也純生成 |

每鏡的 `contest` 欄位（見第 5 節）：contest-safe 8 鏡、needs-abstraction 15 鏡、portfolio-only 2 鏡。比賽版 90 秒估點 **1990 點**（見第 7 節）。

比賽版改提示詞時：Master Prompt 裡的 "black leather jacket" 全部換成 "worn dark work coat with no distinctive features"，"round black eyeglass frames" 換成 "ordinary reading glasses"，三王換成 "three abstract light pillars in gold, green and white"。

## 0. 一鍵複製：Master Prompt（風格鎖＋角色鎖＋負面提示詞）

每一張關鍵幀、每一段影片，都把這一段貼在個別鏡頭提示詞**前面**。

```text
STYLE LOCK — "ASYNC: SUCCESSION" (fictional political allegory, 9:16 vertical; 16:9 alt by pillar-safe centre framing)
Look: deadpan symmetric framing, one-point perspective, characters mostly still while the world moves (PURGA deadpan) + era clash (1970s objects inside 2020s machinery). Bleach-bypass grade, crushed blacks, hard top light, warm tungsten vs cold fluorescent, fine 35mm grain. Lenses 24mm (worlds), 35mm (rooms), 50–85mm (objects, hands). Camera locked or slow push; no handheld shake.
Recurring motifs: a glowing suspended water tank (the light / compute); bare tungsten bulbs with tiny processor cores inside; a small bird woven from incandescent tungsten filament wire; an EMPTY black leather jacket; round black eyeglass frames with no lenses; three faceless carved king chess pieces (gold / jade-green / frost-white); an antique opera coat (Europe); a seawater-damaged upright piano (Japan).
CHARACTER LOCKS (all fictional adults, never resembling any real person or any actor or film character):
- THE JACKET: founder figure, seen only from behind or as hands; black leather jacket, short dark hair. Never a face.
- THE STEWARD: successor; frost-white, high-collared, structured uniform; neat dark hair tied back; calm, flat; carries one plain brass handover key.
- THE MARCHER: woman, 30s, long crimson wool coat, megaphone with a server-fan bell; determined, dignified.
- THE COMPANION: woman, 40s, tailored jade-green silk coat, red lacquer telephone handset; composed, never sexualised.
- THE LITHOGRAPHER: elderly man, white cleanroom suit hood down, holds one silicon wafer.
- THE WEAVERS: two women, plain linen; one weaves a single deep-red thread, one weaves many colours.
- THE KEEPER and THE ACCOUNTANT: two elderly mourners of equal dignity; candles in an ark-shaped cabinet vs paper offerings and a ledger.
- GOLD KING / JADE KING / FROST KING: faceless carved chess pieces only; never human faces.
NEGATIVE PROMPT: real person, celebrity, politician, lookalike, likeness of any actor or film character, recognisable face, portrait of a real CEO, logos, brand names, trademarks, company signage, on-screen text, captions, hashtags, watermarks, flags, national emblems, party symbols, religious caricature, ethnic stereotype, exaggerated racial features, mocking expression, slur, nudity, sexualised pose, gore, weapons pointed at camera, extra fingers, warped hands, melted faces, oversaturated neon cliché.
```

## 1. 片名、Logline、片長

- **片名（建議）**：《非同步：繼承》ASYNC: SUCCESSION。備選：《奈秒之後》AFTER THE NANOSECOND、《光稅》THE LIGHT TAX。
- **Logline**：一盞從台灣夜市燈泡開始的光，被美國、聖地、深圳棋盤上的三個王爭奪；創辦人把鑰匙交給霜白制服的管家，留下一件空皮衣——而夜市裡的人，把那件空外套舉了起來。
- **片長**：預告 90 秒（25 鏡）。比賽片長規定 3–7 分鐘；比賽版的抽象化見第 0A 節，估點見第 7 節。
- **一句話的立場**：片子不下結論。所有爭議主張（女性回歸家庭、移民不再是資產、單一文化生育、拒絕受害敘事、男性被邊緣化）都是**角色的立場**，在片中被另一個角色反駁或留白。旁白只講光、時間、聲音。
- **開頭字卡**（剪輯時打字，不讓模型生成）："A fictional allegory. All characters are invented."

## 2. 三幕結構 × 坂本龍一理論

採用「篡位的管家」（usurping steward）這個**敘事角色原型**：一個冷靜、被低估的繼承者，在亂局中接過權柄。**只借故事功能**，不借任何電影、演員、系列的外型、服裝、髮型或台詞（不是灰色披風、不是長灰色鮑伯頭）。

| 幕 | 時間 | 故事 | 坂本理論節拍 | S:N:M |
| --- | --- | --- | --- | --- |
| 一：光的起源 | 0:00–0:20 | 夜市、移民男孩、洗碗槽；鎢絲光鳥誕生飛走 | 田野錄音當底；四音五聲動機一音一音出現；各地區循環開始（質數秒） | 6:4:0 |
| 二：爭光 | 0:20–1:05 | 開源 vs 閉源、聖地、金牛犢、女權 vs 被收走的皮衣與眼鏡、深圳廠房、伴侶、日本、歐洲、織者、閘門；**1:03.7–1:05.0 全黑**＝全片唯一同步點，三王現身 | async：台灣 7、美國 11、聖地 13、深圳 5、歐洲 17、日本 19 秒循環互不對拍；海嘯鋼琴越接近權力越走音；《Life, Life》式七語疊念 | 3:5:2 → 0:0:0（全黑） |
| 三：繼承 | 1:05–1:30 | 峰會座次、兩種記憶、鑰匙交給管家、圍裙 vs 實驗袍、歐日剪影離場；**高潮：光鳥落在空皮衣上，夜市人群把空皮衣舉起**（回來的是象徵，不是人） | 聲音結束才切；動機回到台灣只剩旋律沒有和弦；more trees：水箱的水化成雨；最後只剩永不消散的正弦嗡聲 | 4:2:4 → 只剩正弦 |

**Mockingjay 對應物（只取「希望象徵」的敘事功能）**：一隻用鎢絲編成的小光鳥。S04 從夜市燈泡天棚誕生飛走 → S24 飛回，落在空皮衣肩上 → 人群高舉空皮衣。不使用任何既有電影的鳥徽、胸針、手勢或配色。

## 3. 角色聖經（虛構原型）

「影射」欄只給 Neon 核對時事用，**絕不寫進任何生成提示詞**。

| 角色 | 服裝／道具／顏色鎖 | 聲音（AI） | 立場（片中台詞） | 私人核對欄：影射 |
| --- | --- | --- | --- | --- |
| THE JACKET 外套 | 黑皮衣，只拍背影或手；後段皮衣變空的 | 只在畫外說一句 | 「他們先讓外套退休，才讓人退休。」 | alludes to: GPU 公司創辦人／執行長 |
| THE STEWARD 管家 | 霜白高領結構制服（非灰披風、非長灰鮑伯頭）；深色頭髮束起；一把素面黃銅交接鑰匙 | 冷靜、平板 | 「什麼都沒變。什麼都變了。」 | alludes to: 網路上「新任 CEO 接班」的迷因（含 CFO 接任說）——**verify：是否有任何正式公告；若無，屬虛構** |
| THE MARCHER 遊行者 | 長版深紅羊毛大衣；伺服器風扇擴音器 | 清楚、堅定 | 「是我們的勞動造了你的光。」「那由誰決定？」 | alludes to: 美國左派女權運動（to verify：對應事件） |
| THE COMPANION 伴侶 | 玉綠絲質外套；紅漆電話聽筒 | 低、從容 | 「我從來不是資產。我是橋。」 | alludes to: 「中國情婦」政商中間人敘事（to verify：Neon 指的報導） |
| THE LITHOGRAPHER 製版師 | 白色無塵衣、兜帽放下；一片晶圓；泡水鋼琴 | 不說話 | 按下沒有聲音的琴鍵 | alludes to: 日本半導體產業 |
| OPERA COAT 歌劇院大衣 | 古董長大衣，只當物件／剪影 | 無 | 被推到牆邊、走出畫面 | alludes to: 歐洲 |
| THE WEAVERS 織者 | 素麻衣；單一深紅線 vs 多色線；同一個空搖籃 | 兩人輪流 | 「一條線撐得住。」／「一條線會斷。」 | alludes to: 單一文化生育率 vs 移民的人口政策辯論 |
| THE KEEPER／THE ACCOUNTANT 守護者／帳房 | 方舟形木櫃與白蠟燭／黃銅盆紙錢與帳本；兩人同等尊嚴 | 兩種語言的低聲 | 「我們自己記帳自己的傷。」／「記憶是約，不是武器。」 | alludes to: 華人對猶太受害敘事的不同看法（to verify：Neon 指的言論）。**兩方並陳、無反派** |
| GOLD KING 金王 | 無臉金色棋子；迷你收費閘門 | 只以字幕存在 | 「我要兩成。」「機器不需要簽證。」 | alludes to: 美國總統 |
| JADE KING 玉王 | 無臉玉綠棋子；紅漆屏風 | 只以字幕存在 | 「一成五。」「工廠不再需要你，家庭需要。」 | alludes to: 中國國家主席 |
| FROST KING 霜王 | 無臉霜白冰紋棋子；坐在棋盤外結冰的格子 | 無 | 被移到玉王身旁 | alludes to: 俄羅斯總統 |
| NIGHT-MARKET CROWD 夜市人群 | 攤販、學生、阿公阿嬤的日常衣著 | 台語叫賣、笑聲 | 高舉空皮衣 | alludes to: 台灣日常的安全感 |

顏色衝突提醒：管家（霜白**布料制服**、人類）與霜王（霜白**冰紋雕刻棋子**、無臉）同色是刻意的「管家向霜王靠攏」暗示；鎖定圖要讓材質一眼分得開。

## 4. 八階段工業流程對應（沿用 `pipeline/`）

| # | 階段 | J4 交付物 | 模型／工具 | 門檻 | 點數 |
| --- | --- | --- | --- | --- | --- |
| 01 | 逆向工程 | `reference-report.md`、`style-bible.md`（PURGA deadpan、tupacabra 年代衝撞、坂本理論） | 本地拆解工具 | 每個技法有來源；禁用清單：不抄角色、片段、品牌、真人肖像、電影角色外型 | 0 |
| 02 | 故事開發 | 本文件第 1–2 節 → `story-bible.md` | — | Script Lock：0–20／20–65／65–90 寫死；全部虛構成年人；`gate 02 --by Neon` | 0 |
| 03 | 視覺開發 | `character-bible.md`（第 3 節，每角色正、側、全身）、`location-bible.md`、`prop-bible.md`（空皮衣、無鏡片眼鏡框、光鳥、三王、鑰匙、泡水鋼琴） | 網站 Unlimited：Nano Banana Pro（角色、道具）、Seedream 5.0 Pro（大場景）、GPT Image 2.6 Flare（臉）；生成鍵顯示 UNLIMITED 才按 | 導演簽 `gate 03` | 0（Soul ID 每人約 25 點另計，需批准） |
| 04 | 預演 | `shots.json`（Shot IR）、`selects.csv`、Animatic | 每鏡一張 Unlimited 關鍵幀 → `pipeline/build_animatic.py` | Timing Lock：鏡長加總 90 ± 1 秒；看完整 Animatic；`gate 04` | 0 |
| 05 | 鏡頭製作 | `takes.csv` | Cinema Studio 4.0（720p，每次 ≤ 30 秒）；Genjutsu Lite（原片 plate 換人）；Draft→Select→Render→Repair→Promote | 每鏡一個 promoted take；每次付費都記 generation id 與點數 | 見第 6 節 |
| 06 | 後製 | `post-lock.md`、英文字幕檔 | DaVinci Resolve；AI 配樂與 AI 人聲；片名、字幕、字卡都在剪輯軟體打 | Picture Lock、Sound Lock；-14 LUFS、≤ -1 dBTP | 0 |
| 07 | QC | `qc-report.json` | `qc/creative_score.py`、`qc/mech_check.py`；另加本片的「政策 QC」：每鏡風險旗標 = 高 的要逐項簽 | 六維平均 ≥ 8 且每項 ≥ 7；機械全 pass | 0 |
| 08 | 交付 | `delivery.md` | `delivery/profiles.json` | 來源紀錄、時事核對欄全部填完（沒填完不交付） | 0 |

原片主幹（IMG_7835，58.1 秒，直式 2160×3840）：S03＝P01（00:00–00:05）、S17＝P05–P06（00:35–00:38.5）、S18＝P07 全黑（00:41.2–00:42.5，1.3 秒）、S23＝P09–P11（00:48.5–00:58）。作品集版可保留 Neon 本人；比賽版必須用 Genjutsu 換成虛構的人。

## 5. 鏡頭表（25 鏡，90.0 秒）

### 5a. 總表

| 鏡 | 時間 | 秒 | 幕 | 節拍 | 原片 | 模型 | 風險 | 比賽 | 估點 | 比賽版估點 |
| --- | --- | ---: | :-: | --- | --- | --- | --- | --- | ---: | ---: |
| S01 | 0:00.0–0:03.0 | 3.0 | 1 | 冷開場：黑畫面＋虛構寓言字卡；正弦嗡聲進 | — | 剪輯軟體 | 低 | contest-safe | 0.0 | 0 |
| S02 | 0:03.0–0:07.0 | 4.0 | 1 | 台灣夜市：日常與安全感（台灣循環 7 秒起點） | — | Seedream 5.0 Pro（關鍵幀）→ Cinema Studio 4.0 | 低 | contest-safe | 85.3 | 85.3 |
| S03 | 0:07.0–0:12.0 | 5.0 | 1 | 原片主幹：發光水箱下背手抬頭的人＝『外套』（皮衣創辦人）背影 | P01（原片 00:00–00:05） | Genjutsu Lite（原片動作遷移） | 中 | needs-abstraction | 78.2 | 85.1 |
| S04 | 0:12.0–0:16.0 | 4.0 | 1 | 移民男孩的舊行李箱；燈泡裡的運算核心；一根鎢絲鬆開，織成一隻光鳥飛起（象徵誕生） | — | Nano Banana Pro（道具）→ Cinema Studio 4.0 | 低 | contest-safe | 85.3 | 85.3 |
| S05 | 0:16.0–0:20.0 | 4.0 | 1 | 美國（11 秒循環）：深夜餐館洗碗槽、桌球彈起 | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 低（不出現 Denny's 招牌） | needs-abstraction | 85.3 | 85.3 |
| S06 | 0:20.0–0:24.0 | 4.0 | 2 | 開源 vs 閉源：一排任何人都能點的紙燈籠 vs 一盞上鎖的黃銅燈（深圳 5 秒循環） | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 低 | contest-safe | 85.3 | 85.3 |
| S07 | 0:24.0–0:28.0 | 4.0 | 2 | 聖地（13 秒循環）：燃燒不毀的光纖荊棘、伺服器巴別塔 | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 中 | needs-abstraction | 86.7 | 85.1 |
| S08 | 0:28.0–0:32.0 | 4.0 | 2 | 金牛犢：人群圍著晶片做的金色小牛跳舞（市值崇拜） | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 中 | needs-abstraction | 85.1 | 85.1 |
| S09 | 0:32.0–0:35.5 | 3.5 | 2 | 『遊行者』（美國左派女權立場）在街頭，伺服器風扇做的擴音器 | — | GPT Image 2.6 Flare（臉）→ Cinema Studio 4.0 | 中 | needs-abstraction | 85.3 | 85.3 |
| S10 | 0:35.5–0:39.0 | 3.5 | 2 | 空的皮衣與圓框黑眼鏡被收進『失物招領』鐵籠（男性被邊緣化的主張） | — | Nano Banana Pro（道具）→ Cinema Studio 4.0 | 中 | needs-abstraction | 85.3 | 85.1 |
| S11 | 0:39.0–0:43.0 | 4.0 | 2 | 深圳廠房：機械手臂接手，女工的空凳子（AI 取代勞動力） | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 低 | contest-safe | 85.1 | 85.1 |
| S12 | 0:43.0–0:46.0 | 3.0 | 2 | 『伴侶』（中國情婦原型）：玉綠絲外套、紅漆電話在兩張桌之間遞送 | — | GPT Image 2.6 Flare（臉）→ Cinema Studio 4.0 | 高 | portfolio-only | 85.3 | 85.1 |
| S13 | 0:46.0–0:50.0 | 4.0 | 2 | 日本（19 秒循環）：白色無塵衣的『製版師』、海邊泡水的鋼琴、熄燈的晶圓廠 | — | Seedream 5.0 Pro（大場景）＋Flare（臉）→ Cinema Studio 4.0 | 低 | contest-safe | 85.3 | 85.3 |
| S14 | 0:50.0–0:53.0 | 3.0 | 2 | 歐洲（17 秒循環）：空蕩歌劇院，一排熄滅的舊燈泡，歌劇院大衣 | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 低 | contest-safe | 85.1 | 85.1 |
| S15 | 0:53.0–0:57.0 | 4.0 | 2 | 兩位織者：單色線（單一文化生育＝穩定）vs 多色線（移民＝資產）——兩個立場對峙 | — | Nano Banana Pro → Cinema Studio 4.0 | 高 | needs-abstraction | 85.6 | 85.1 |
| S16 | 0:57.0–1:00.5 | 3.5 | 2 | 閘門數行李箱：機器人不需要簽證走過去（移民不再是資產的主張） | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 中 | needs-abstraction | 85.1 | 85.1 |
| S17 | 1:00.5–1:03.7 | 3.2 | 2 | 原片主幹：攤開手掌接光，燈開始閃 | P05–P06（原片 00:35–00:38.5） | Genjutsu Lite | 中 | needs-abstraction | 78.2 | 85.1 |
| S18 | 1:03.7–1:05.0 | 1.3 | 2 | 全黑＝全片唯一同步點：頻閃中出現三個無臉的王（金、玉、霜）在深圳天際線棋盤上 | P07（原片 00:41.2–00:42.5 全黑） | Nano Banana Pro → Cinema Studio 4.0（生 5 秒，剪 1.3 秒） | 高 | needs-abstraction | 85.1 | 85.1 |
| S19 | 1:05.0–1:09.0 | 4.0 | 3 | 峰會大廳：玉王的手（棋子之手）安排金王、霜王座位；歐洲與日本的椅子被推到牆邊 | — | Seedream 5.0 Pro → Cinema Studio 4.0 | 中 | needs-abstraction | 85.1 | 85.1 |
| S20 | 1:09.0–1:12.5 | 3.5 | 3 | 兩種記憶：方舟守護者的燭火 vs 帳房的紙錢——『受害敘事』之爭，兩方並陳 | — | Nano Banana Pro → Cinema Studio 4.0 | 高 | portfolio-only | 85.6 | 85.1 |
| S21 | 1:12.5–1:16.5 | 4.0 | 3 | 交接：『管家』（Steward，霜白制服）從皮衣袖口的手中接過交接鑰匙；皮衣留在椅上，空了 | — | Nano Banana Pro（道具、手）→ Cinema Studio 4.0 | 中 | needs-abstraction | 85.3 | 85.3 |
| S22 | 1:16.5–1:19.5 | 3.0 | 3 | 圍裙 vs 實驗袍：女性回到家庭的主張 vs 遊行者的回應——懸而不決 | — | Nano Banana Pro → Cinema Studio 4.0 | 高 | needs-abstraction | 85.1 | 85.1 |
| S23 | 1:19.5–1:24.0 | 4.5 | 3 | 原片主幹：上前一步再抬頭；背景兩個剪影（歌劇院大衣、抱泡水鋼琴的人）走出畫面 | P09–P11（原片 00:48.5–00:58） | Genjutsu Lite | 中 | needs-abstraction | 79.8 | 86.7 |
| S24 | 1:24.0–1:27.0 | 3.0 | 3 | 高潮：鎢絲光鳥飛回，落在空皮衣上；夜市人群把空皮衣高舉在燈泡天棚下（回來的是象徵，不是人）；水箱的水化成雨 | — | Seedream 5.0 Pro（大場景）→ Cinema Studio 4.0 | 中 | needs-abstraction | 85.1 | 85.1 |
| S25 | 1:27.0–1:30.0 | 3.0 | 3 | 片名：黑畫面上只剩正弦嗡聲 | — | 剪輯軟體 | 低 | contest-safe | 0.0 | 0 |
| **合計** | | **90.0** | | | | | | | **1943** | **1961**（另加 Soul ID 29） |

### 5b. 逐鏡提示詞（貼上時前面先貼第 0 節的 Master Prompt）

比例：全部 9:16。要出 16:9 版時，關鍵幀改成 `16:9 horizontal`，主體留在畫面中央 9:16 安全框內，兩側只放環境。

#### S01 · 0:00.0–0:03.0 · 第 1 幕 · 3.0 秒
- 節拍：冷開場：黑畫面＋虛構寓言字卡；正弦嗡聲進
- 原片：—　模型：剪輯軟體　估點：0.0
- Image prompt:
  ```text
  (no generation) Black frame. Editor title card typed in post: 'A fictional allegory. All characters are invented.'
  ```
- Motion prompt:
  ```text
  (none) hold black; sine tone fades in from silence.
  ```
- 聲音／坂本：S:N:M = 0:0:0 → 正弦嗡聲（全片唯一不消散的聲音）淡入。
- English subtitle: `A fictional allegory. All characters are invented.`
- 時事核對：—　**verify：source / date ＿＿＿＿**
- 風險：低
- 比賽（contest）：**contest-safe**

#### S02 · 0:03.0–0:07.0 · 第 1 幕 · 4.0 秒
- 節拍：台灣夜市：日常與安全感（台灣循環 7 秒起點）
- 原片：—　模型：Seedream 5.0 Pro（關鍵幀）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical film still. A crowded Taiwanese night market at 10 pm seen from a low wide angle: a canopy of hundreds of bare tungsten light bulbs, steam from a griddle, a middle-aged woman vendor flipping an oyster omelette with calm hands, families eating on plastic stools, a child asleep on a parent's shoulder. Warm practical light against crushed blacks, bleach-bypass grade, 24mm, strict symmetry, deadpan stillness. No text, no logos, no flags.
  ```
- Motion prompt:
  ```text
  Slow 4-second push-in under the bulb canopy; steam drifts; the vendor never looks up. Camera locked to horizon, no shake.
  ```
- 聲音／坂本：台灣循環 7 秒：炒鍋、拖鞋、台語叫賣（AI 田野錄音）。S:N:M = 6:4:0。
- English subtitle: `The light started at a night market.`
- 時事核對：台灣夜市的日常安全感（象徵，非事實陳述）；黃仁勳曾公開逛夜市（repo sources.md：2023-05-25 饒河、2024-05-29 寧夏）。　**verify：source / date ＿＿＿＿**　（Neon 核對：引用的夜市行程與日期是否沿用 sources.md）
- 風險：低
- 比賽（contest）：**contest-safe**：通用夜市，不加國名字卡。

#### S03 · 0:07.0–0:12.0 · 第 1 幕 · 5.0 秒
- 節拍：原片主幹：發光水箱下背手抬頭的人＝『外套』（皮衣創辦人）背影
- 原片：P01（原片 00:00–00:05）　模型：Genjutsu Lite（原片動作遷移）　估點：78.2
- Image prompt:
  ```text
  9:16 vertical still. Keep the reference composition: one man centred in a dark exhibition hall under a suspended glowing water tank, hands behind his back, looking up; caustic water-light patterns on the floor. Replace him with a fictional man seen only from behind: black leather jacket, short dark hair, no face visible. Bleach-bypass, crushed blacks, hard top light, 35mm. No text, no logos.
  ```
- Motion prompt:
  ```text
  Genjutsu Lite: keep Neon's original motion from IMG_7835 00:00–00:05, swap the figure for the fictional back-view jacket figure; floor caustics continue.
  ```
- 聲音／坂本：夜市聲在水箱嗡聲下延續；原創四音五聲動機第一次出現（鐘音色）。
- English subtitle: `(no subtitle)`
- 時事核對：人物＝虛構創辦人原型。　**verify：source / date ＿＿＿＿**
- 風險：中：皮衣背影可能被聯想到真人 → 不露臉、不寫名字、不放商標
- 比賽（contest）：**needs-abstraction**：原片有 Neon 本人：比賽版不用 plate，改用 Cinema Studio 4.0 生成虛構 AI 主角（Soul ID 鎖臉）；黑皮衣換成無辨識度的深色舊工作外套。

#### S04 · 0:12.0–0:16.0 · 第 1 幕 · 4.0 秒
- 節拍：移民男孩的舊行李箱；燈泡裡的運算核心；一根鎢絲鬆開，織成一隻光鳥飛起（象徵誕生）
- 原片：—　模型：Nano Banana Pro（道具）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical macro still. Under a night-market bulb canopy, a battered 1970s child's suitcase stands beside a food stall. Inside each bare bulb a tiny glowing processor core is visible instead of a filament. One bulb's tungsten filament has unwound and is weaving itself into a small glowing bird made only of thin incandescent wire. Shallow depth of field, 85mm, warm tungsten against black. No text, no logos.
  ```
- Motion prompt:
  ```text
  The wire bird finishes weaving itself, flutters once and rises out of frame toward the dark sky; bulbs flicker in a 7-count pattern. 4 seconds.
  ```
- 聲音／坂本：鎢絲燒熱的細微爆裂聲；動機第二音。
- English subtitle: `A boy arrived with one suitcase.`
- 時事核對：移民男孩背景（repo sources.md：9 歲赴美、肯塔基寄宿學校）。光鳥＝『希望的象徵』，只取敘事功能，不引用任何既有電影的鳥徽造型。　**verify：source / date ＿＿＿＿**
- 風險：低
- 比賽（contest）：**contest-safe**

#### S05 · 0:16.0–0:20.0 · 第 1 幕 · 4.0 秒
- 節拍：美國（11 秒循環）：深夜餐館洗碗槽、桌球彈起
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical still. An American roadside diner kitchen at 2 am: a steel dishwashing sink full of water, the same caustic light ripples as the exhibition floor, a white ping-pong ball floating among the plates, a teenage dishwasher's rubber-gloved hands seen from above. Fluorescent green-white light, crushed blacks, 35mm, symmetric overhead. No text, no logos, no brand signage.
  ```
- Motion prompt:
  ```text
  The ping-pong ball pops up out of the water and hangs mid-air for a beat before falling; ripples spread. 4 seconds, locked overhead camera.
  ```
- 聲音／坂本：美國循環 11 秒：杯盤、排風扇。動機第三音。
- English subtitle: `The first thing he learned was to wash the dishes clean.`
- 時事核對：repo sources.md：15 歲在 Denny's 洗碗；1993 年在 Denny's 創立公司。　**verify：source / date ＿＿＿＿**
- 風險：低（不出現 Denny's 招牌）
- 比賽（contest）：**needs-abstraction**：拿掉桌球（真人傳記線索），只留洗碗槽與水紋。

#### S06 · 0:20.0–0:24.0 · 第 2 幕 · 4.0 秒
- 節拍：開源 vs 閉源：一排任何人都能點的紙燈籠 vs 一盞上鎖的黃銅燈（深圳 5 秒循環）
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical split-symmetry still. Left half: a corridor of hundreds of paper lanterns, each with an open door, people of all ages lighting them from each other's flames. Right half: a single sealed brass lantern with a heavy keyhole, glowing brighter than all of them, guarded by an empty velvet rope. A seam of darkness down the middle. Bleach-bypass, 24mm. No text, no logos, no flags.
  ```
- Motion prompt:
  ```text
  The paper lanterns light one by one in a 5-count wave leftward; the brass lantern's glow pulses steadily, unchanged. 4 seconds, static camera.
  ```
- 聲音／坂本：深圳循環 5 秒：廠房馬達、紙張摩擦。S:N:M = 3:5:2。
- English subtitle: `One light is shared. One light is sold.`
- 時事核對：AI 開源權重 vs 閉源模型之爭；repo sources.md：華為開源 CANN 對抗 CUDA。　**verify：source / date ＿＿＿＿**　（Neon 核對：要對應哪一個開源／閉源事件（模型名、日期））
- 風險：低
- 比賽（contest）：**contest-safe**：字幕保留模糊句，不點名任何公司或模型。

#### S07 · 0:24.0–0:28.0 · 第 2 幕 · 4.0 秒
- 節拍：聖地（13 秒循環）：燃燒不毀的光纖荊棘、伺服器巴別塔
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：86.7
- Image prompt:
  ```text
  9:16 vertical still. A desert at blue hour. In the foreground a bush made of glowing fibre-optic strands burns with white light without being consumed. Far behind, a tower built of stacked server racks rises into the clouds, unfinished, scaffolding at the top. No people. Wide 24mm, strict symmetry, cold sand and hot light. No text, no religious symbols beyond the burning bush, no flags.
  ```
- Motion prompt:
  ```text
  Fibre strands flicker like flame; slow 4-second tilt up from the bush to the top of the tower where a crane pauses. 
  ```
- 聲音／坂本：聖地循環 13 秒：沙漠風；七語疊念第一次（AI 聲音）。
- English subtitle: `The bush was burning, yet it was not consumed.`
- 時事核對：repo sources.md：2020-04 收購以色列 Mellanox；2025-12 Kiryat Tivon 園區。宗教意象（荊棘、巴別塔）只作寓言。　**verify：source / date ＿＿＿＿**　（Neon 核對：『美國、以色列爭 AI 霸權』要對應哪一則報導）
- 風險：中：宗教隱喻 → 不連結當前戰爭、不出現人物、不嘲諷任何宗教
- 比賽（contest）：**needs-abstraction**：拿掉經文式字幕與『燃燒不毀的荊棘』；改成沙漠裡一叢發光的光纖灌木＋未完成的機櫃塔，不帶宗教典故、不指涉任何國家。

#### S08 · 0:28.0–0:32.0 · 第 2 幕 · 4.0 秒
- 節拍：金牛犢：人群圍著晶片做的金色小牛跳舞（市值崇拜）
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical deadpan still. In a marble trading hall, a life-size calf sculpted entirely from gold-plated computer chips stands on a plinth; a crowd in identical business suits dances around it in a slow ring, faces turned away from camera. Gold light from below, crushed blacks, 35mm. No text, no logos, no ticker symbols.
  ```
- Motion prompt:
  ```text
  The ring of dancers rotates slowly clockwise; the calf's chips glint in sequence. 4 seconds, locked camera.
  ```
- 聲音／坂本：美國循環第二輪（11 秒）落在這裡的中段；鋼琴開始輕微走音。
- English subtitle: `(no subtitle)`
- 時事核對：市值崇拜的寓言，無具體事實陳述。　**verify：source / date ＿＿＿＿**
- 風險：中：宗教典故 → 人群穿現代西裝、無族群特徵
- 比賽（contest）：**needs-abstraction**：金牛犢是宗教典故：改成晶片鑄的巨大金燈泡，人群圍繞；不用任何知名雕塑（例如華爾街銅牛）造型。

#### S09 · 0:32.0–0:35.5 · 第 2 幕 · 3.5 秒
- 節拍：『遊行者』（美國左派女權立場）在街頭，伺服器風扇做的擴音器
- 原片：—　模型：GPT Image 2.6 Flare（臉）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical portrait still. A fictional woman in her thirties in a long crimson wool coat stands on a wet city street at night, holding a megaphone whose bell is made of a server cooling fan. Determined, calm expression, not caricatured. Behind her, a blurred crowd with blank placards. Hard sodium street light, 50mm, shallow depth of field. No text on placards, no logos, no real person.
  ```
- Motion prompt:
  ```text
  She lifts the megaphone; the fan blades start spinning and the air moves her hair. 3.5 seconds.
  ```
- 聲音／坂本：群眾低語（AI）；風扇聲變成她的聲音。
- English subtitle: `MARCHER: "Our labour built your light."`
- 時事核對：美國左派女權運動的立場（角色主張，非片子結論）。　**verify：source / date ＿＿＿＿**　（Neon 核對：要對應哪一場運動或事件（名稱、日期））
- 風險：中：政治立場 → 角色有尊嚴、不醜化；與 S10、S22 互相反駁
- 比賽（contest）：**needs-abstraction**：不出現運動口號；台詞改成模稜兩可的 "Who keeps the light on?"；不暗示任何真實運動。

#### S10 · 0:35.5–0:39.0 · 第 2 幕 · 3.5 秒
- 節拍：空的皮衣與圓框黑眼鏡被收進『失物招領』鐵籠（男性被邊緣化的主張）
- 原片：—　模型：Nano Banana Pro（道具）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical still life. Inside a steel lost-and-found cage in an empty corridor: an empty black leather jacket on a wire hanger, and a pair of round black eyeglass frames with no lenses resting on a shelf. A single bare bulb above. Deadpan symmetry, 50mm, bleach-bypass. No people, no text, no labels.
  ```
- Motion prompt:
  ```text
  A gloved hand (no face) closes the cage door; the bulb sways and the jacket's shadow swings. 3.5 seconds.
  ```
- 聲音／坂本：鐵門關上的金屬聲 → 一聲沒有衰減完就被切掉的鋼琴音（片中唯一一次違反『聲音結束才切』，刻意）。
- English subtitle: `THE JACKET (off-screen): "They retired the jacket before they retired the man."`
- 時事核對：眼鏡框＝作曲家的象徵物（只用道具，不出現本人）；皮衣＝創辦人象徵物。立場由角色說出。　**verify：source / date ＿＿＿＿**
- 風險：中：性別爭議 → 與 S09 的台詞成對出現，不下結論
- 比賽（contest）：**needs-abstraction**：皮衣＋圓框眼鏡組合可辨識真人：改成無特徵的舊外套與普通眼鏡；拿掉性別立場台詞，只留鐵籠關門。

#### S11 · 0:39.0–0:43.0 · 第 2 幕 · 4.0 秒
- 節拍：深圳廠房：機械手臂接手，女工的空凳子（AI 取代勞動力）
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical wide still. A vast electronics assembly hall at night: robotic arms work an endless line under red-tinted light; along the line, a row of empty blue plastic stools where workers used to sit, each with a pair of folded cotton work gloves left on it. No people. 24mm, strict one-point perspective, crushed blacks. No text, no logos, no flags.
  ```
- Motion prompt:
  ```text
  The robot arms move in perfect 5-count sync; camera dollies slowly down the row of empty stools. 4 seconds.
  ```
- 聲音／坂本：深圳循環 5 秒；機械完美同步的節拍（對照全片的不同步）。
- English subtitle: `STEWARD'S LEDGER (caption): "Line 7: headcount zero."`
- 時事核對：AI／自動化取代製造業勞動力（含女性勞工）；repo sources.md：華為（深圳）昇騰。　**verify：source / date ＿＿＿＿**　（Neon 核對：引用的自動化或女性勞動參與數據（來源、年份））
- 風險：低
- 比賽（contest）：**contest-safe**：字幕可保留（無政治主張）。

#### S12 · 0:43.0–0:46.0 · 第 2 幕 · 3.0 秒
- 節拍：『伴侶』（中國情婦原型）：玉綠絲外套、紅漆電話在兩張桌之間遞送
- 原片：—　模型：GPT Image 2.6 Flare（臉）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical still. A fictional woman in her forties wearing a tailored jade-green silk coat walks between two long banquet tables in a dim private dining room, carrying a red lacquer telephone handset with its cord trailing to the other table. Composed, intelligent expression, not sexualised. Low warm light, 50mm, symmetric. No text, no flags, no logos.
  ```
- Motion prompt:
  ```text
  She sets the red handset down on the far table without breaking stride; the cord tightens across the room. 3 seconds.
  ```
- 聲音／坂本：電話線拉緊的弦樂泛音；動機以二胡式音色重現。
- English subtitle: `COMPANION: "I was never the asset. I was the bridge."`
- 時事核對：『中國情婦』＝政商影響力敘事中的中間人原型（角色，不指涉特定真人）。　**verify：source / date ＿＿＿＿**　（Neon 核對：你指的是哪一則報導（人名不放進片中，只放私人欄））
- 風險：高：可能被讀成族群／性別刻板印象 → 角色主動、有尊嚴；不性化；不對應具名真人
- 比賽（contest）：**portfolio-only**：『中國情婦』原型帶族群／性別指涉與政治影射。比賽版替代鏡：空宴會廳裡一條紅色電話線橫過兩張空桌，無人物、無台詞。

#### S13 · 0:46.0–0:50.0 · 第 2 幕 · 4.0 秒
- 節拍：日本（19 秒循環）：白色無塵衣的『製版師』、海邊泡水的鋼琴、熄燈的晶圓廠
- 原片：—　模型：Seedream 5.0 Pro（大場景）＋Flare（臉）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical still. A grey beach at dawn: an old upright piano half-buried in sand, swollen by seawater, several keys missing. Beside it stands a fictional elderly man in a white cleanroom suit with the hood down, holding a single silicon wafer like a dinner plate. Far behind, a dark shuttered semiconductor fab. Muted cold palette, 35mm, deadpan symmetry. No text, no logos, no flags.
  ```
- Motion prompt:
  ```text
  He presses one remaining piano key; nothing sounds; a wave reaches his boots. 4 seconds, locked camera.
  ```
- 聲音／坂本：日本循環 19 秒：泡水鋼琴音色，缺鍵、走音（被自然調音）。
- English subtitle: `Some once made the light. Now they tune what's left.`
- 時事核對：日本半導體產業的衰落與重建（象徵）。　**verify：source / date ＿＿＿＿**　（Neon 核對：引用的市占數字或事件（例如記憶體產業、新晶圓廠計畫）與年份）
- 風險：低
- 比賽（contest）：**contest-safe**：不出現國旗、地名或產業數據。

#### S14 · 0:50.0–0:53.0 · 第 2 幕 · 3.0 秒
- 節拍：歐洲（17 秒循環）：空蕩歌劇院，一排熄滅的舊燈泡，歌劇院大衣
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical still. An empty gilded European opera house; on stage a single long antique opera coat hangs on a stand, and a row of old footlight bulbs goes dark one by one from left to right. Red velvet seats, dust in the air, 35mm, symmetric from the stalls. No people, no text, no flags.
  ```
- Motion prompt:
  ```text
  Footlights die one by one; dust drifts. 3 seconds.
  ```
- 聲音／坂本：歐洲循環 17 秒：空廳殘響；德布西式延伸和弦只剩一半。
- English subtitle: `(no subtitle)`
- 時事核對：歐洲在 AI／晶片競賽中被邊緣化（象徵）。　**verify：source / date ＿＿＿＿**　（Neon 核對：對應的政策或事件）
- 風險：低
- 比賽（contest）：**contest-safe**：不出現國旗或地名。

#### S15 · 0:53.0–0:57.0 · 第 2 幕 · 4.0 秒
- 節拍：兩位織者：單色線（單一文化生育＝穩定）vs 多色線（移民＝資產）——兩個立場對峙
- 原片：—　模型：Nano Banana Pro → Cinema Studio 4.0　估點：85.6
- Image prompt:
  ```text
  9:16 vertical split-symmetry still. Two fictional women sit facing each other across a wooden cradle. The left woman weaves a cloth from a single deep-red thread; the right woman weaves from dozens of different coloured threads. Both cloths feed into the same empty cradle. Soft top light, 50mm, deadpan. No text, no religious or national symbols.
  ```
- Motion prompt:
  ```text
  Both shuttles move at different tempos (7 and 13 count); the cradle rocks slightly. 4 seconds.
  ```
- 聲音／坂本：兩條節奏不同的織布機聲，永不對拍。
- English subtitle: `LEFT WEAVER: "One thread holds." / RIGHT WEAVER: "One thread breaks."`
- 時事核對：人口政策辯論：單一文化生育率 vs 移民（兩方立場並陳）。　**verify：source / date ＿＿＿＿**　（Neon 核對：引用的出生率、移民政策數據（國家、來源、年份））
- 風險：高：生育／移民立場 → 兩方台詞等長並陳、不由旁白下結論；不出現族群特徵
- 比賽（contest）：**needs-abstraction**：拿掉兩句台詞（生育／移民主張），只留兩人以不同節奏織線的畫面，讓觀眾自己解讀。

#### S16 · 0:57.0–1:00.5 · 第 2 幕 · 3.5 秒
- 節拍：閘門數行李箱：機器人不需要簽證走過去（移民不再是資產的主張）
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical still. A steel border turnstile gate in a white hall; a queue of travellers with suitcases waits behind a closed bar, while a line of identical humanoid robots walks through an open lane beside them without stopping. The child's 1970s suitcase from earlier sits alone at the front of the human queue. 35mm, cold fluorescent light, symmetric. No text, no flags, no national emblems.
  ```
- Motion prompt:
  ```text
  The robot lane flows continuously; the human gate stays shut. 3.5 seconds.
  ```
- 聲音／坂本：閘門嗶聲以 11 拍循環；行李輪子聲停住。
- English subtitle: `GOLD KING (caption): "Machines don't need visas."`
- 時事核對：移民政策收緊與 AI 替代的論述（角色主張）。　**verify：source / date ＿＿＿＿**　（Neon 核對：引用的簽證／移民政策事件與日期）
- 風險：中：移民議題 → 呼應 S04 行李箱，讓觀眾自己判斷
- 比賽（contest）：**needs-abstraction**：拿掉金王字幕（移民政策主張），只留閘門與機器人並行的畫面。

#### S17 · 1:00.5–1:03.7 · 第 2 幕 · 3.2 秒
- 節拍：原片主幹：攤開手掌接光，燈開始閃
- 原片：P05–P06（原片 00:35–00:38.5）　模型：Genjutsu Lite　估點：78.2
- Image prompt:
  ```text
  9:16 vertical still. Keep the reference pose: the man centred under the glowing tank, palms up and open toward the light. Replace with the fictional back-view figure in the black leather jacket. Bleach-bypass, crushed blacks. No text, no logos.
  ```
- Motion prompt:
  ```text
  Genjutsu Lite: keep original motion 00:35–00:38.5; the tank light starts to stutter.
  ```
- 聲音／坂本：六條地區循環同時都在響、互相錯開，密度最高。
- English subtitle: `(no subtitle)`
- 時事核對：—　**verify：source / date ＿＿＿＿**
- 風險：中：同 S03
- 比賽（contest）：**needs-abstraction**：原片有 Neon 本人：改用虛構 AI 主角重新生成，不用 plate。

#### S18 · 1:03.7–1:05.0 · 第 2 幕 · 1.3 秒
- 節拍：全黑＝全片唯一同步點：頻閃中出現三個無臉的王（金、玉、霜）在深圳天際線棋盤上
- 原片：P07（原片 00:41.2–00:42.5 全黑）　模型：Nano Banana Pro → Cinema Studio 4.0（生 5 秒，剪 1.3 秒）　估點：85.1
- Image prompt:
  ```text
  9:16 vertical strobe still. Near-total darkness lit by one white strobe flash: a giant chessboard laid over a night city skyline of glass towers and a harbour. Three faceless carved king pieces taller than people: a gold king beside a miniature toll gate, a jade-green king behind a red lacquer folding screen, a frost-white king seated on a frozen square at the board's edge. No faces, no text, no flags, no national emblems.
  ```
- Motion prompt:
  ```text
  Two strobe flashes inside 1.3 s; everything else black. Cut on the second flash.
  ```
- 聲音／坂本：所有聲部同時停：全片唯一同步。只剩正弦嗡聲。
- English subtitle: `(caption) "I want twenty." "Fifteen."`
- 時事核對：repo sources.md：2025-08 H20 出口許可換 15% 營收、公開說『開 20% 被殺到 15%』。三王＝大國領導人的寓言。　**verify：source / date ＿＿＿＿**　（Neon 核對：深圳接待各國領袖的時事（是否發生、日期、場合））
- 風險：高：三王可能被認出原型 → 無臉、無國旗、無國徽
- 比賽（contest）：**needs-abstraction**：P07 全黑段仍有 Neon 剪影：比賽版純生成；拿掉深圳天際線與『兩成／一成五』字幕（真實事件與政治人物影射），三王改成三個抽象的彩色光柱或無冠的幾何棋子。

#### S19 · 1:05.0–1:09.0 · 第 3 幕 · 4.0 秒
- 節拍：峰會大廳：玉王的手（棋子之手）安排金王、霜王座位；歐洲與日本的椅子被推到牆邊
- 原片：—　模型：Seedream 5.0 Pro → Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical overhead still. A circular summit table in a vast hall of red lacquer and glass, viewed from directly above. Three tall high-backed chairs: gold, jade-green and frost-white, arranged at the table. Against the far wall, two smaller chairs pushed aside: one draped with an antique opera coat, one with a seawater-stained piano bench cushion. No people, no flags, no text, no emblems. Symmetric, 24mm.
  ```
- Motion prompt:
  ```text
  An unseen force slides the frost-white chair to the table beside the jade chair; the two wall chairs stay. 4 seconds, locked overhead.
  ```
- 聲音／坂本：鋼琴走音到最大；動機只剩兩個音。
- English subtitle: `(no subtitle)`
- 時事核對：大國角色變遷、歐洲與日本被邊緣化（寓言）。　**verify：source / date ＿＿＿＿**　（Neon 核對：峰會座次、出席名單、日期（尚未查證，不可自填））
- 風險：中：政治 → 只用椅子與顏色
- 比賽（contest）：**needs-abstraction**：拿掉紅漆、霜椅靠向玉椅的政治暗示：一般的會議桌，三張椅子與兩張被推到牆邊的椅子，不帶國家配色。

#### S20 · 1:09.0–1:12.5 · 第 3 幕 · 3.5 秒
- 節拍：兩種記憶：方舟守護者的燭火 vs 帳房的紙錢——『受害敘事』之爭，兩方並陳
- 原片：—　模型：Nano Banana Pro → Cinema Studio 4.0　估點：85.6
- Image prompt:
  ```text
  9:16 vertical split still. Left: a fictional elderly scholar in a dark coat lights a row of plain white candles inside a wooden ark-shaped cabinet. Right: a fictional elderly accountant in a grey tunic burns folded paper offerings in a small brass bowl beside an open ledger. Both are dignified and mourning, facing each other across darkness. Warm firelight, 50mm. No religious insignia beyond candles and paper, no national symbols, no text.
  ```
- Motion prompt:
  ```text
  Both flames rise at the same moment, then sway independently. 3.5 seconds.
  ```
- 聲音／坂本：兩種語言的低聲祈禱（AI）錯開，不對拍。
- English subtitle: `ACCOUNTANT: "We keep our own wounds." / KEEPER: "Memory is a covenant, not a weapon."`
- 時事核對：兩種歷史記憶的爭論（角色立場並陳）。　**verify：source / date ＿＿＿＿**　（Neon 核對：要對應哪一則公開言論（只放私人欄））
- 風險：高：宗教／族群 → 兩人同等尊嚴、不出現刻板外貌、不讓任何一方成反派
- 比賽（contest）：**portfolio-only**：受害敘事之爭屬宗教／族群陳述。比賽版替代鏡：牆上兩個走速不同的時鐘，無人物、無台詞。

#### S21 · 1:12.5–1:16.5 · 第 3 幕 · 4.0 秒
- 節拍：交接：『管家』（Steward，霜白制服）從皮衣袖口的手中接過交接鑰匙；皮衣留在椅上，空了
- 原片：—　模型：Nano Banana Pro（道具、手）→ Cinema Studio 4.0　估點：85.3
- Image prompt:
  ```text
  9:16 vertical still. A dark boardroom. Close on two hands over a long table: a hand in a black leather jacket sleeve passes a single plain brass handover key to a hand in a frost-white, high-collared structured uniform sleeve. Beyond them, an empty chair. No faces, 85mm, crushed blacks, top light. No text, no logos.
  ```
- Motion prompt:
  ```text
  The key changes hands; the leather sleeve withdraws; camera racks focus to the chair where the empty leather jacket now hangs. 4 seconds.
  ```
- 聲音／坂本：鑰匙落掌的一聲，衰減完才切。
- English subtitle: `THE STEWARD: "Nothing changes. Everything changes."`
- 時事核對：虛構的接班交接（Steward 為虛構角色）。　**verify：source / date ＿＿＿＿**　（Neon 核對：是否真有接班公告；若無，片頭虛構字卡已涵蓋）
- 風險：中：接班情節 → 純虛構，不對應任何公告
- 比賽（contest）：**needs-abstraction**：接班可能被讀成對真實公司的不實陳述：皮衣袖改成無特徵深色袖子，交接純屬虛構公司；台詞保留。

#### S22 · 1:16.5–1:19.5 · 第 3 幕 · 3.0 秒
- 節拍：圍裙 vs 實驗袍：女性回到家庭的主張 vs 遊行者的回應——懸而不決
- 原片：—　模型：Nano Banana Pro → Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical still life. On a white wall, two hooks side by side: one holds a plain cotton apron, the other a laboratory coat with an access badge (blank). Below, a woman's hand (no face) hovers between them. On the floor, the crimson coat from the street is folded neatly. Soft daylight, 50mm, deadpan. No text, no logos.
  ```
- Motion prompt:
  ```text
  The hand hovers and does not choose; cut before any decision. 3 seconds.
  ```
- 聲音／坂本：靜默中只有正弦嗡聲與遠處夜市聲（回到台灣的預告）。
- English subtitle: `JADE KING (caption): "The factory no longer needs you. The family does." / MARCHER: "Then who decides?"`
- 時事核對：國家政策鼓勵女性回歸家庭的論述 vs 女權回應（立場並陳）。　**verify：source / date ＿＿＿＿**　（Neon 核對：引用的政策或官方言論（來源、日期））
- 風險：高：性別政策 → 由角色說出、留白不決
- 比賽（contest）：**needs-abstraction**：拿掉玉王字幕與遊行者回話（性別政策主張），只留手在圍裙與實驗袍之間猶豫。

#### S23 · 1:19.5–1:24.0 · 第 3 幕 · 4.5 秒
- 節拍：原片主幹：上前一步再抬頭；背景兩個剪影（歌劇院大衣、抱泡水鋼琴的人）走出畫面
- 原片：P09–P11（原片 00:48.5–00:58）　模型：Genjutsu Lite　估點：79.8
- Image prompt:
  ```text
  9:16 vertical still. Keep the reference composition: the figure steps forward and looks up at the glowing tank; two small silhouettes cross the deep background. Replace the central figure with the fictional figure, now WITHOUT the leather jacket (plain dark shirt), seen from behind. Background silhouettes: one in a long antique opera coat, one carrying a water-damaged upright piano on a dolly. Bleach-bypass. No text, no logos.
  ```
- Motion prompt:
  ```text
  Genjutsu Lite: keep original motion 00:48.5–00:53; background figures exit right to left.
  ```
- 聲音／坂本：七語疊念最後一次；歐洲、日本循環淡出。
- English subtitle: `Some once saved this light. Now they can only walk past it.`
- 時事核對：歐洲、日本邊緣化（寓言）。　**verify：source / date ＿＿＿＿**
- 風險：中：同 S03
- 比賽（contest）：**needs-abstraction**：原片有 Neon 本人與他人剪影：改用虛構 AI 主角重新生成，背景剪影也生成。

#### S24 · 1:24.0–1:27.0 · 第 3 幕 · 3.0 秒
- 節拍：高潮：鎢絲光鳥飛回，落在空皮衣上；夜市人群把空皮衣高舉在燈泡天棚下（回來的是象徵，不是人）；水箱的水化成雨
- 原片：—　模型：Seedream 5.0 Pro（大場景）→ Cinema Studio 4.0　估點：85.1
- Image prompt:
  ```text
  9:16 vertical low-angle still. Under the Taiwanese night-market bulb canopy, a crowd of ordinary people (vendors, students, grandparents) lifts an EMPTY black leather jacket high above their heads like a banner. The small glowing bird woven from tungsten filament wire is perched on the jacket's shoulder. Light rain falls through the bulbs. Warm tungsten against black, 24mm, symmetric. No faces in focus, no text, no hashtags, no logos, no flags.
  ```
- Motion prompt:
  ```text
  The wire bird lands on the jacket's shoulder; the crowd raises the jacket higher; rain begins. 3 seconds.
  ```
- 聲音／坂本：台灣循環回來：只有四音動機，沒有和弦；雨聲。
- English subtitle: `(no subtitle)`
- 時事核對：象徵回歸，非任何真人回任。　**verify：source / date ＿＿＿＿**　（私人備註（僅作品集版）：網路上 #BringJensenBack 的討論熱度——待 Neon 查證；片中不出現任何 hashtag 文字）
- 風險：中：群眾高舉物件可能被讀成政治集會 → 夜市日常服裝、無標語
- 比賽（contest）：**needs-abstraction**：空皮衣換成無辨識度的舊外套；不帶任何 hashtag、標語或對真人的呼籲（#BringJensenBack 只限作品集版）。

#### S25 · 1:27.0–1:30.0 · 第 3 幕 · 3.0 秒
- 節拍：片名：黑畫面上只剩正弦嗡聲
- 原片：—　模型：剪輯軟體　估點：0.0
- Image prompt:
  ```text
  (no generation) Black frame; title typed in editor.
  ```
- Motion prompt:
  ```text
  (none)
  ```
- 聲音／坂本：所有聲音退掉，只剩正弦嗡聲，不淡出（剪掉時仍在響）。
- English subtitle: `ASYNC: SUCCESSION`
- 時事核對：—　**verify：source / date ＿＿＿＿**
- 風險：低
- 比賽（contest）：**contest-safe**

## 6. 點數估算（0 點已花）

單價沿用 `treatments-jensen/README.md` 與 `budget/cost-table.csv`：Cinema Studio 4.0 720p 每秒 7 點、最少 5 秒、每鏡 2 take；Genjutsu Lite 每段 ≤ 15 秒 32 點、2 take；放大每鏡 4 點；AI 旁白每句 0.2 點（S07、S23 七語疊念各算 7 句）；再加 15% 修補預備。關鍵幀全部走網站 Unlimited，0 點。AI 配樂的點數**未列入、待查**。

| 項目 | 點數 |
| --- | ---: |
| 影片（20 鏡 Cinema Studio 4.0 + 3 段 Genjutsu Lite） | 1592 |
| 放大（23 鏡） | 92 |
| 旁白 | 5.4 |
| 小計 | 1689.4 |
| **合計（含 15%）** | **1943** |
| 作品集版（保留 Neon 原片，不跑 Genjutsu） | 1709 |

- 對照每月 9,000 點上限：預告片約占 22%。本月已用多少點**要先查帳戶**再決定。
- 生成前流程：Neon 批准 → Director 在「AI Video Production Service」聊天室貼估點 → 才按生成。

## 7. 比賽版（contest cut）估點與擴充

- 比賽版不能用 Neon 的 IMG_7835 原片：S03、S17、S18、S23 都要換成虛構 AI 主角，而且不拿 plate 當底，全部用 Cinema Studio 4.0 重新生成。用 Genjutsu 換掉他、但保留他實拍的動作，算不算「以實拍影片呈現參賽者」不確定，所以這裡採保守的全生成估點。
- portfolio-only 的 S12、S20 換成同長度的替代鏡（點數相同）；被拿掉的台詞不配音。
- 虛構主角的 Soul ID 訓練一次 25 點。

| 項目 | 點數 |
| --- | ---: |
| 影片（23 鏡 Cinema Studio 4.0，每鏡 2 take） | 1610 |
| 放大 | 92 |
| 旁白 | 2.8 |
| Soul ID | 25 |
| **比賽版 90 秒合計（含 15%）** | **1990** |

- 比賽片長規定 3–7 分鐘，90 秒預告本身不夠長。每秒約 21.8 點 → 3 分鐘約 4,000 點、4 分鐘約 5,300 點、5 分鐘約 6,600 點。
- 擴充方式：每個地區循環從 1 鏡擴成 3–4 鏡；全黑頻閃仍只出現一次；高潮與片尾不加長。
- 其他規則：截止 11/27 03:00（台北時間）；所有影像在 Contest Project 內、11/12–11/26 生成（網站 Unlimited 靜幀在 Contest Project 裡是否仍免費：to verify）；音樂與人聲必須 AI，且不可模仿真人聲音；英文字幕；交 YouTube 連結。
- 是否投稿由 Neon 決定；作品集版保留完整寓言，不投稿。

## 8. 時事核對總表（Neon 用）

我只填 repo 裡已經有來源的事實（`sources.md`）；其他全部標 **to verify**，沒有自己編日期或事件。

| 鏡 | 引用的事件／主張 | 已有來源 | 待核對 |
| --- | --- | --- | --- |
| S02 | 台灣夜市的日常安全感（象徵，非事實陳述）；黃仁勳曾公開逛夜市（repo sources.md：2023-05-25 饒河、2024-05-29 寧夏）。 | 是（sources.md） | Neon 核對：引用的夜市行程與日期是否沿用 sources.md |
| S03 | 人物＝虛構創辦人原型。 | — | to verify |
| S04 | 移民男孩背景（repo sources.md：9 歲赴美、肯塔基寄宿學校）。光鳥＝『希望的象徵』，只取敘事功能，不引用任何既有電影的鳥徽造型。 | 是（sources.md） | — |
| S05 | repo sources.md：15 歲在 Denny's 洗碗；1993 年在 Denny's 創立公司。 | 是（sources.md） | — |
| S06 | AI 開源權重 vs 閉源模型之爭；repo sources.md：華為開源 CANN 對抗 CUDA。 | 是（sources.md） | Neon 核對：要對應哪一個開源／閉源事件（模型名、日期） |
| S07 | repo sources.md：2020-04 收購以色列 Mellanox；2025-12 Kiryat Tivon 園區。宗教意象（荊棘、巴別塔）只作寓言。 | 是（sources.md） | Neon 核對：『美國、以色列爭 AI 霸權』要對應哪一則報導 |
| S08 | 市值崇拜的寓言，無具體事實陳述。 | — | to verify |
| S09 | 美國左派女權運動的立場（角色主張，非片子結論）。 | — | Neon 核對：要對應哪一場運動或事件（名稱、日期） |
| S10 | 眼鏡框＝作曲家的象徵物（只用道具，不出現本人）；皮衣＝創辦人象徵物。立場由角色說出。 | — | to verify |
| S11 | AI／自動化取代製造業勞動力（含女性勞工）；repo sources.md：華為（深圳）昇騰。 | 是（sources.md） | Neon 核對：引用的自動化或女性勞動參與數據（來源、年份） |
| S12 | 『中國情婦』＝政商影響力敘事中的中間人原型（角色，不指涉特定真人）。 | — | Neon 核對：你指的是哪一則報導（人名不放進片中，只放私人欄） |
| S13 | 日本半導體產業的衰落與重建（象徵）。 | — | Neon 核對：引用的市占數字或事件（例如記憶體產業、新晶圓廠計畫）與年份 |
| S14 | 歐洲在 AI／晶片競賽中被邊緣化（象徵）。 | — | Neon 核對：對應的政策或事件 |
| S15 | 人口政策辯論：單一文化生育率 vs 移民（兩方立場並陳）。 | — | Neon 核對：引用的出生率、移民政策數據（國家、來源、年份） |
| S16 | 移民政策收緊與 AI 替代的論述（角色主張）。 | — | Neon 核對：引用的簽證／移民政策事件與日期 |
| S18 | repo sources.md：2025-08 H20 出口許可換 15% 營收、公開說『開 20% 被殺到 15%』。三王＝大國領導人的寓言。 | 是（sources.md） | Neon 核對：深圳接待各國領袖的時事（是否發生、日期、場合） |
| S19 | 大國角色變遷、歐洲與日本被邊緣化（寓言）。 | — | Neon 核對：峰會座次、出席名單、日期（尚未查證，不可自填） |
| S20 | 兩種歷史記憶的爭論（角色立場並陳）。 | — | Neon 核對：要對應哪一則公開言論（只放私人欄） |
| S21 | 虛構的接班交接（Steward 為虛構角色）。 | — | Neon 核對：是否真有接班公告；若無，片頭虛構字卡已涵蓋 |
| S22 | 國家政策鼓勵女性回歸家庭的論述 vs 女權回應（立場並陳）。 | — | Neon 核對：引用的政策或官方言論（來源、日期） |
| S23 | 歐洲、日本邊緣化（寓言）。 | — | to verify |
| S24 | 象徵回歸，非任何真人回任。 | — | 私人備註（僅作品集版）：網路上 #BringJensenBack 的討論熱度——待 Neon 查證；片中不出現任何 hashtag 文字 |

**私人備註（只限作品集版，不進任何提示詞或畫面）**：#BringJensenBack 這個 hashtag 的網路討論——是否存在、熱度、時間都 to verify。片中不出現任何 hashtag 或標語文字。

## 9. 政策與風險清單

- 真人：不畫任何真實人物的臉；不寫「長得像某人／某演員／某電影角色」；權力人物只以無臉棋子、椅子、字幕存在。
- 意識形態主張：一律由角色說出，且每一個都有另一個角色反駁或留白（S09↔S10、S15 兩織者、S20 兩種記憶、S22 圍裙 vs 實驗袍）。旁白不替任何一方下結論。
- 宗教：荊棘、巴別塔、金牛犢、方舟只作寓言；不連結當前戰爭；不嘲諷任何宗教；任何族群都不當反派、不畫刻板外貌。
- 商標：不出現公司名、產品名、招牌；字幕也不寫公司名。
- 坂本龍一：只借理論，不用錄音、旋律、取樣；動機原創，不可近似〈戰場上的快樂聖誕〉。
- 「篡位的管家」：只借敘事角色功能，不借任何電影的服裝、髮型、演員或台詞。
