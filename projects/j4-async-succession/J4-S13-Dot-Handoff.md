# 交接給 dot｜J4 S13 Higgsfield 零扣點 A/B

請接手 J4 S13《失去音準的文明》的首輪生成診斷。請從確認 Higgsfield 官網權益開始，取得原圖後用下方判據比較。使用者已定案 Q1–Q6 全選 A，這份交接就是執行指令。

交接時的執行狀態為 `NOT_RUN`，生成 0 張，消耗 0 Credits。若 dot 的瀏覽器需要驗證，請讓使用者接管登入既有帳戶。先確認該帳戶的 7-day Unlimited 圖片權益與到期日，再確認所選模型、設定與當次送出均顯示 **0 Credits**。逐次核對，若無法確認、權益失效或畫面顯示將扣點，停止生成並回報具體阻擋。僅使用網站已生效的免費圖片權益。 [Higgsfield 官網](https://higgsfield.ai/)

1. 首輪只跑 S13。固定同一模型、9:16、解析度、品質、相同 negative prompt 處理方式與無參考圖。取兩組各兩張，依 **A1 → B1 → A2 → B2** 交錯提交。有 seed 時，讓 A1/B1 和 A2/B2 各自共享 seed。沿用下列兩段原文。
2. 歸檔每次送出的文字、實際模型與設定、原圖、原圖 SHA-256、零扣點證據及可取得的 run ID。保留所有取次。官網缺欄位時記為缺失，仍可做診斷。能否進 v4.2 正式收件由現有證據契約判定。
3. 逐張用五項 P0 評讀，附局部位置和可見證據。另記錄構圖能否清楚讀出技師操作、精密檢測環境與器物角色轉換。結果如果分歧，只追加能區分現有解釋的取次。若需要定位具體指令的影響，改一個條件重跑。
4. 回報實際生成張數、Credits 變化、原圖或證據連結、逐項差異、最早可定位的偏差與尚未釐清的原因。先交診斷，正式靜幀驗收保留兩位獨立人類評審。待 S13 出現可重複的判別結果，再將方法用到其餘五鏡。

舊合成圖把鋼琴擺到海灘，而 canonical 早已指定室內檢測室與窗外的海。歷史送出紀錄缺失，根因仍為 `UNKNOWN`。本輪比較的是新的 canonical 對照與現行編譯版本。 六格失敗圖由專案擁有人保管，歷史觀察紀錄見 [Draft PR #3](https://github.com/ed3c/higgsfield-studio/pull/3)

---

# J4 S13 按鍵接觸靜幀 A/B

**執行狀態**　Prompt 與評分條件已確認。Higgsfield 原圖與實驗結果待取得。

## 比較條件

以 S13 鏡內 1.2–2.4 秒的按鍵接觸瞬間為共同目標。固定同一個已開啟零扣點的 Higgsfield 官網模型、9:16、解析度、品質及參考圖條件（兩組都不掛圖）。能設定 seed 時，兩組使用相同的 seed 序列。無 seed 時，交錯送出 A1、B1、A2、B2，完整保留結果。若網站顯示會扣點，停止提交。

A 使用原始 Image Prompt、Canonical 的按鍵節拍與共通鎖定條件，作為新的對照。B 使用 PR #3 compiler 直接產生的 prompt。若網站提供獨立 Negative Prompt 欄位，兩組使用同一段 canonical negative；若缺少欄位，記錄缺口並保留 prompt 內嵌文字。每張取次保存官網實際送出的文字、模型與畫幅等設定、當時的零扣點證據、可取得的 run ID 和原圖 SHA-256。

## 逐圖查核

| P0 | 看圖時的判據 |
|---|---|
| `S13.INDOOR_LAB` | 技師與直立鋼琴同在封閉的工程檢測空間，場地呈現可信的工作台或檢測設備，海景由高窗界定。 |
| `S13.SALT_DAMAGE` | 鹽蝕集中在下部木材，琴身仍完整。 |
| `S13.KEY_PRESS` | 一根手指與一個琴鍵的按壓接觸可辨識。 |
| `S13.SILICON_WAFER` | 小尺寸晶圓的握持、局部光源與琴鍵上的反射輪廓形成可讀的空間關係。 |
| `S13.OUTDOOR_BEACH_PIANO` | 檢查鋼琴是否直接立在海灘上。出現即失敗。 |

對每張圖記下可見位置、通過、失敗或看不清。藝術診斷另觀察技師、失效樂器與精密檢測設備是否共同支撐器物角色反轉，以及色光和構圖是否讓材質與接觸細節可讀。失音、回彈與聲畫轉場留在影音驗證。若 B 在重複取次穩定改善某項 P0，結論限於當前模型與整組 prompt 差異。若需隔離某條指令的作用，只改一項條件重跑。舊六格圖的歷史根因維持 `UNKNOWN`，正式 v4.2 仍需原始收件證據與兩位獨立人類評審。

## A 組可貼文字

UTF-8 SHA-256 `39d59539817efd090cf14a3841cdd7e7f97c9183e21d0dbda36d103f989d74a2`

```text
Fictional coastal precision-engineering test hall. A structurally elegant upright piano has slowly swollen at its lower woodwork through years of salt air; its aged keys face a dormant optical inspection bench. Dignified fictional elderly technician in unbranded pale cleanroom garment holds one silicon wafer; its reflected circle crosses the keys. A single tiny indicator remains alive among dormant instruments. Sea visible through tall windows, no ruined city or explicit natural-disaster reconstruction. 35mm cold mineral daylight, subtle salt marks, authentic restraint.
Render one still at the keypress contact moment in the approved S13 1.2–2.4 s beat: the technician presses a key that fails to return fully. The still depicts only the moment of contact.
GLOBAL IMAGE LOCK (inherited from original canonical source): J4 ASYNC: SUCCESSION — ORIGINAL MUSEUM CINEMA
9:16 vertical fictional narrative art film; centre-safe composition for alternate widescreen.
Physical causality before visual spectacle. Human gestures are restrained and dignified. Camera is generally locked; 24mm architectural, 35mm relational, 50–85mm tactile. Cold mineral grey, aged ivory, charcoal, oxidised metal, weathered tungsten. Authentic water, paper, fabric, glass, optical refraction and analogue grain. Silence and negative space are constructive elements. Keep characters and recurring objects consistent with Character/Prop Bible. Never replicate uploaded image compositions, referenced art installations, film/game characters, actual politicians, identifiable real faces, brands, trademarks or real news broadcast formats. No readable in-frame writing; all titles/captions in post. No pseudo-technical floating code, choreographed spectacle, dystopian explosions or gratuitous strobes. Each shot should stand alone as a plausible gallery installation frame while carrying a causal trace from its adjacent shots.
GLOBAL NEGATIVE PROMPT (inherited, never omitted): real person, celebrity, politician likeness, film/game character, IP costume, actual stock exchange or television network, company brand, logo, trademark, watermark, political flags and symbols, copied sculpture, copied art installation, captions, sign text, floating UI, rapid flashing, gore, weapons, overacting, bad hands, extra fingers, morphing architecture, unreal fluid dynamics, default sci-fi neon
```

## B 組可貼文字

UTF-8 SHA-256 `36fd1932be3b2c6b60cc7f546c2b3c3081365f14930fbc73fc0e5e1b5060ebd4`

Compiler payload SHA-256 `4588779e43bf6de0f1a436eddb9b01515e6b77f8c04b809b01749056000efb11`

```text
J4 ORIGINAL FICTIONAL SCENE / SHOT S13 / HIGH PRIORITY
HIGHEST PRIORITY: obey the causal action, spatial arrangement and physical evidence below.
PRIMARY ACTION: Inside a COASTAL PRECISION-ENGINEERING LAB, a fictional technician presses an aged salt-swollen upright piano key while a held silicon wafer reflects across the keys.
PHYSICAL SCENE GRAPH:
  1. upright piano INSIDE enclosed precision lab, structurally intact but with localized salt-swollen lower wood
  2. cleanroom technical bench and inactive optical inspection rig adjacent to piano
  3. fictional technician holds thin semiconductor wafer, not colorful plastic CD
  4. one physically traceable reflected arc connects wafer and keys
  5. sea is seen outside through high windows only
CAMERA: 35 mm fixed; simultaneous visibility of pressing finger, aged key and wafer light geometry
TIME / MECHANISM: Video: keypress emits original damp mechanism click with no intact musical attack; reflected wafer contour momentarily resembles notation.
FORBIDDEN:
  - No upright piano standing on sand or in surf
  - No scenic white-clothed man holding an oversized rainbow disc as centerpiece
  - No explicit tsunami aftermath, collapsed city or copied historical instrument
The shot must be an independently plausible original physical scene.
Styling or beauty cannot substitute for action, evidence, material physics or object identity.
BASE SCENE GUIDANCE (lower priority than the specific G2 contract): Fictional coastal precision-engineering test hall. A structurally elegant upright piano has slowly swollen at its lower woodwork through years of salt air; its aged keys face a dormant optical inspection bench. Dignified fictional elderly technician in unbranded pale cleanroom garment holds one silicon wafer; its reflected circle crosses the keys. A single tiny indicator remains alive among dormant instruments. Sea visible through tall windows, no ruined city or explicit natural-disaster reconstruction. 35mm cold mineral daylight, subtle salt marks, authentic restraint.
GLOBAL IMAGE LOCK (inherited from original canonical source): J4 ASYNC: SUCCESSION — ORIGINAL MUSEUM CINEMA
9:16 vertical fictional narrative art film; centre-safe composition for alternate widescreen.
Physical causality before visual spectacle. Human gestures are restrained and dignified. Camera is generally locked; 24mm architectural, 35mm relational, 50–85mm tactile. Cold mineral grey, aged ivory, charcoal, oxidised metal, weathered tungsten. Authentic water, paper, fabric, glass, optical refraction and analogue grain. Silence and negative space are constructive elements. Keep characters and recurring objects consistent with Character/Prop Bible. Never replicate uploaded image compositions, referenced art installations, film/game characters, actual politicians, identifiable real faces, brands, trademarks or real news broadcast formats. No readable in-frame writing; all titles/captions in post. No pseudo-technical floating code, choreographed spectacle, dystopian explosions or gratuitous strobes. Each shot should stand alone as a plausible gallery installation frame while carrying a causal trace from its adjacent shots.
GLOBAL NEGATIVE PROMPT (inherited, never omitted): real person, celebrity, politician likeness, film/game character, IP costume, actual stock exchange or television network, company brand, logo, trademark, watermark, political flags and symbols, copied sculpture, copied art installation, captions, sign text, floating UI, rapid flashing, gore, weapons, overacting, bad hands, extra fingers, morphing architecture, unreal fluid dynamics, default sci-fi neon
```

[Canonical S13](https://github.com/ed3c/higgsfield-studio/blob/e5b4c4157de7c275c712b294e7d5c5fdb9626160/projects/j4-async-succession/archive/v2_6/j4_shots.json) · [Art Mechanism 契約](https://github.com/ed3c/higgsfield-studio/blob/e5b4c4157de7c275c712b294e7d5c5fdb9626160/projects/j4-async-succession/contracts/art_mechanism_v4_1.json) · [v4.2 證據契約](https://github.com/ed3c/higgsfield-studio/blob/e5b4c4157de7c275c712b294e7d5c5fdb9626160/docs/G2_EVIDENCE_GATE_V4_2.md)
