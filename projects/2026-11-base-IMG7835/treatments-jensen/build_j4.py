"""Build J4_trailer_master_prompt.md from j4_shots.json. 0 credits: writing only."""
import json, math, pathlib
HERE = pathlib.Path(__file__).parent
shots = json.loads((HERE / "j4_shots.json").read_text())

CS_PER_S, CS_MIN, TAKES, GJ_SEG, UPSCALE, VO_LINE, RESERVE = 7, 5, 2, 32, 4, 0.2, 1.15
STACKED = {"S07", "S23"}  # seven-voice stacked VO

def cost(s):
    if s["tool"] == "cs":
        v = max(s["dur"], CS_MIN) * CS_PER_S * TAKES
    elif s["tool"] == "gj":
        v = GJ_SEG * TAKES
    else:
        return 0, 0, 0
    sub = s["sub"]
    lines = 0 if sub.startswith("(no") or sub.startswith("(caption)") or "(caption)" in sub.split(":")[0] else sub.count(" / ") + 1
    if s["id"] in STACKED: lines = 7
    return v, UPSCALE, lines * VO_LINE

rows = []
tot_v = tot_u = tot_vo = 0
for s in shots:
    v, u, vo = cost(s)
    tot_v += v; tot_u += u; tot_vo += vo
    s["credits"] = round((v + u + vo) * RESERVE, 1)
raw = tot_v + tot_u + tot_vo
total = math.ceil(raw * RESERVE)
gj_raw = sum(cost(s)[0] for s in shots if s["tool"] == "gj")
portfolio = math.ceil((raw - gj_raw - 4 * sum(1 for s in shots if s["tool"] == "gj")) * RESERVE)
per_s = total / 90
n_gen = sum(1 for s in shots if s["tool"] != "edit")

# Contest cut: no IMG_7835 plates (Neon is identifiable) -> every plate shot becomes a full Cinema Studio 4.0
# generation of a fictional AI lead; portfolio-only shots are replaced by same-length contest-safe alternates;
# dropped dialogue is not voiced.
SOUL_ID = 25
CONTEST_VO = {"S02": 1, "S04": 1, "S05": 1, "S06": 1, "S09": 1, "S13": 1, "S21": 1, "S23": 7}
c_v = c_u = c_vo = 0
for s in shots:
    if s["tool"] == "edit":
        s["contest_credits"] = 0
        continue
    v = max(s["dur"], CS_MIN) * CS_PER_S * TAKES
    vo = CONTEST_VO.get(s["id"], 0) * VO_LINE
    c_v += v; c_u += UPSCALE; c_vo += vo
    s["contest_credits"] = round((v + UPSCALE + vo) * RESERVE, 1)
contest_raw = c_v + c_u + c_vo + SOUL_ID
contest_total = math.ceil(contest_raw * RESERVE)
soul_res = math.ceil(SOUL_ID * RESERVE)
contest_per_s = (contest_total - soul_res) / 90
def contest_len(sec):
    return f"{math.ceil((contest_per_s * sec + soul_res) / 100) * 100:,}"
from collections import Counter
cc = Counter(s["contest"] for s in shots)

def tc(x):
    return f"{int(x//60)}:{x%60:04.1f}"

out = []
W = out.append
W(f"""# J4《非同步：繼承 ASYNC: SUCCESSION》— Higgsfield 工業級預告片主提示詞

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

每鏡的 `contest` 欄位（見第 5 節）：contest-safe {cc['contest-safe']} 鏡、needs-abstraction {cc['needs-abstraction']} 鏡、portfolio-only {cc['portfolio-only']} 鏡。比賽版 90 秒估點 **{contest_total} 點**（見第 7 節）。

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
- **片長**：預告 90 秒（{len(shots)} 鏡）。比賽片長規定 3–7 分鐘；比賽版的抽象化見第 0A 節，估點見第 7 節。
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

## 5. 鏡頭表（{len(shots)} 鏡，90.0 秒）

### 5a. 總表

| 鏡 | 時間 | 秒 | 幕 | 節拍 | 原片 | 模型 | 風險 | 比賽 | 估點 | 比賽版估點 |
| --- | --- | ---: | :-: | --- | --- | --- | --- | --- | ---: | ---: |""")
for s in shots:
    W(f"| {s['id']} | {tc(s['start'])}–{tc(s['start']+s['dur'])} | {s['dur']} | {s['act']} | {s['beat']} | {s['plate'] or '—'} | {s['model']} | {s['risk'].split('：')[0]} | {s['contest']} | {s['credits']} | {s['contest_credits']} |")
W(f"| **合計** | | **90.0** | | | | | | | **{total}** | **{contest_total - soul_res}**（另加 Soul ID {soul_res}） |")
W("""
### 5b. 逐鏡提示詞（貼上時前面先貼第 0 節的 Master Prompt）

比例：全部 9:16。要出 16:9 版時，關鍵幀改成 `16:9 horizontal`，主體留在畫面中央 9:16 安全框內，兩側只放環境。
""")
for s in shots:
    W(f"""#### {s['id']} · {tc(s['start'])}–{tc(s['start']+s['dur'])} · 第 {s['act']} 幕 · {s['dur']} 秒
- 節拍：{s['beat']}
- 原片：{s['plate'] or '—'}　模型：{s['model']}　估點：{s['credits']}
- Image prompt:
  ```text
  {s['img']}
  ```
- Motion prompt:
  ```text
  {s['motion']}
  ```
- 聲音／坂本：{s['audio']}
- English subtitle: `{s['sub']}`
- 時事核對：{s['fact']}　**verify：source / date ＿＿＿＿**{('　（' + s['verify'] + '）') if s['verify'] else ''}
- 風險：{s['risk']}
- 比賽（contest）：**{s['contest']}**{('：' + s['contest_how']) if s['contest_how'] else ''}
""")
W(f"""## 6. 點數估算（0 點已花）

單價沿用 `treatments-jensen/README.md` 與 `budget/cost-table.csv`：Cinema Studio 4.0 720p 每秒 7 點、最少 5 秒、每鏡 2 take；Genjutsu Lite 每段 ≤ 15 秒 32 點、2 take；放大每鏡 4 點；AI 旁白每句 0.2 點（S07、S23 七語疊念各算 7 句）；再加 15% 修補預備。關鍵幀全部走網站 Unlimited，0 點。AI 配樂的點數**未列入、待查**。

| 項目 | 點數 |
| --- | ---: |
| 影片（{sum(1 for s in shots if s['tool']=='cs')} 鏡 Cinema Studio 4.0 + {sum(1 for s in shots if s['tool']=='gj')} 段 Genjutsu Lite） | {tot_v:.0f} |
| 放大（{n_gen} 鏡） | {tot_u:.0f} |
| 旁白 | {tot_vo:.1f} |
| 小計 | {raw:.1f} |
| **合計（含 15%）** | **{total}** |
| 作品集版（保留 Neon 原片，不跑 Genjutsu） | {portfolio} |

- 對照每月 9,000 點上限：預告片約占 {total/9000:.0%}。本月已用多少點**要先查帳戶**再決定。
- 生成前流程：Neon 批准 → Director 在「AI Video Production Service」聊天室貼估點 → 才按生成。

## 7. 比賽版（contest cut）估點與擴充

- 比賽版不能用 Neon 的 IMG_7835 原片：S03、S17、S18、S23 都要換成虛構 AI 主角，而且不拿 plate 當底，全部用 Cinema Studio 4.0 重新生成。用 Genjutsu 換掉他、但保留他實拍的動作，算不算「以實拍影片呈現參賽者」不確定，所以這裡採保守的全生成估點。
- portfolio-only 的 S12、S20 換成同長度的替代鏡（點數相同）；被拿掉的台詞不配音。
- 虛構主角的 Soul ID 訓練一次 {SOUL_ID} 點。

| 項目 | 點數 |
| --- | ---: |
| 影片（{n_gen} 鏡 Cinema Studio 4.0，每鏡 2 take） | {c_v:.0f} |
| 放大 | {c_u:.0f} |
| 旁白 | {c_vo:.1f} |
| Soul ID | {SOUL_ID} |
| **比賽版 90 秒合計（含 15%）** | **{contest_total}** |

- 比賽片長規定 3–7 分鐘，90 秒預告本身不夠長。每秒約 {contest_per_s:.1f} 點 → 3 分鐘約 {contest_len(180)} 點、4 分鐘約 {contest_len(240)} 點、5 分鐘約 {contest_len(300)} 點。
- 擴充方式：每個地區循環從 1 鏡擴成 3–4 鏡；全黑頻閃仍只出現一次；高潮與片尾不加長。
- 其他規則：截止 11/27 03:00（台北時間）；所有影像在 Contest Project 內、11/12–11/26 生成（網站 Unlimited 靜幀在 Contest Project 裡是否仍免費：to verify）；音樂與人聲必須 AI，且不可模仿真人聲音；英文字幕；交 YouTube 連結。
- 是否投稿由 Neon 決定；作品集版保留完整寓言，不投稿。

## 8. 時事核對總表（Neon 用）

我只填 repo 裡已經有來源的事實（`sources.md`）；其他全部標 **to verify**，沒有自己編日期或事件。

| 鏡 | 引用的事件／主張 | 已有來源 | 待核對 |
| --- | --- | --- | --- |""")
for s in shots:
    if s['fact'] == '—': continue
    has = 'sources.md' in s['fact']
    W(f"| {s['id']} | {s['fact']} | {'是（sources.md）' if has else '—'} | {s['verify'] or ('—' if has else 'to verify')} |")
W("""
**私人備註（只限作品集版，不進任何提示詞或畫面）**：#BringJensenBack 這個 hashtag 的網路討論——是否存在、熱度、時間都 to verify。片中不出現任何 hashtag 或標語文字。

## 9. 政策與風險清單

- 真人：不畫任何真實人物的臉；不寫「長得像某人／某演員／某電影角色」；權力人物只以無臉棋子、椅子、字幕存在。
- 意識形態主張：一律由角色說出，且每一個都有另一個角色反駁或留白（S09↔S10、S15 兩織者、S20 兩種記憶、S22 圍裙 vs 實驗袍）。旁白不替任何一方下結論。
- 宗教：荊棘、巴別塔、金牛犢、方舟只作寓言；不連結當前戰爭；不嘲諷任何宗教；任何族群都不當反派、不畫刻板外貌。
- 商標：不出現公司名、產品名、招牌；字幕也不寫公司名。
- 坂本龍一：只借理論，不用錄音、旋律、取樣；動機原創，不可近似〈戰場上的快樂聖誕〉。
- 「篡位的管家」：只借敘事角色功能，不借任何電影的服裝、髮型、演員或台詞。
""")
(HERE / "J4_trailer_master_prompt.md").write_text("\n".join(out))
print(len(shots), total, portfolio, raw, contest_total, dict(cc))
