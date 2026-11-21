# Neon 工業級流程需求：事實查核（2026-11-22）

原文：[neon-industrial-pipeline-brief.md](neon-industrial-pipeline-brief.md)。只用公開網頁與官方文件查核，沒有任何生成或扣點。

判定：「正確」＝官方來源寫明；「部分」＝大致對但有重要出入；「錯誤」＝與官方來源不符；「未證實」＝找不到可靠來源。

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 1 | Global Film Festival 2026 前三名：Listen to Meh（rococo_table_radical，US$500,000）、Fukushima（aist，US$200,000）、The Field Agent（zackmmurray，US$100,000）；約 5,000 部參賽 | 正確 | 官方得獎頁 https://higgsfield.ai/contests/higgsfield-global-film-festival?tab=winners 。補充：Listen to Meh 出自 Purga Studio（阿根廷）。總獎金官方頁寫 US$1,000,000，Higgsfield LinkedIn 貼文寫 US$2,000,000，兩者不一致 |
| 2 | 劇情與評語描述（高喬牧人與屋頂上的羊；福島資深工程師；汽車電影院影迷的任務） | 正確 | 同上，評審為 Paul W. S. Anderson、Alex Proyas、Phedon Papamichael（另有 Edwin Catmull） |
| 3 | PURGA 獲 2026 Cannes Lions Film 類 Bronze Lion | 正確 | 官方案例 https://higgsfield.ai/creator-hub/case-studies/purga-cannes-lions-case-study ；Purga Studio 官方 LinkedIn。補充：由 GUT Mexico City 報名，作品《Lorem Ipsum》含 Mafia、Samurai、Western 三支 |
| 4 | 《Lorem Ipsum》以 Cinema Studio 做角色、鏡頭與影像，動畫與音樂由其他 AI 工具完成；先定角色與視覺方向再建世界 | 正確 | 同上官方案例原文 |
| 5 | Cinema Studio 4.0 有 Director's Panel、最多 50 個參考、表情控制（Emotion Wheel）、影片延伸、局部編輯 | 正確 | https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide ；PR Newswire 2026-10-28。API 另限 30 圖＋10 影片＋10 音訊、總數 50 |
| 6 | 單次最長 30 秒，但「產品介紹頁」寫最長一分鐘 | 部分（一分鐘的說法不可信） | higgsfield.ai 官方部落格、說明文件、API（4–30 秒）與新聞稿一致寫 30 秒。「一分鐘、原生 4K」只出現在 higgsfield.company，這不是 higgsfield.ai 網域，無法確認是官方頁。排程一律用 30 秒；網站最高 1080p，API 480p/720p |
| 7 | Genjutsu 支援 4–30 秒參考影片，保留動作與運鏡，替換人物、物件、場景 | 正確 | https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-genjutsu 。網站最多 30 張參考圖；API 只收 1–8 張；超過 30 秒會被裁成 30 秒 |
| 8 | 官方開源 higgsfield-ai/skills，MIT；含影像／影片生成、Soul ID、商品攝影、品牌系統、廣告影片、Virality Predictor | 正確 | https://github.com/higgsfield-ai/skills （MIT）。本庫已收 v0.14.0 快照 |
| 9 | 安裝：`npm i -g @higgsfield/cli`、`higgsfield auth login`、`npx skills add higgsfield-ai/skills` | 正確（有補充） | npm 套件 `@higgsfield/cli` 存在（1.2.2，MIT），官方 CLI README 列為跨平台安裝法；skills 的 INSTALL.md 主推 `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh \| sh`，也可 Homebrew |
| 10 | CLI、MCP、Canvas 生成都扣點，網頁 Unlimited 不適用 | 正確 | https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work ：MCP、CLI、Canvas、Supercomputer 一律扣點；Unlimited 與免費次數只限 higgsfield.ai 標準生成。注意：Canvas 即使在網站上也扣點 |
| 11 | CLI Skills 不能據此推定能完整控制 Cinema Studio 4.0 的導演面板、共享專案與時間軸 | 正確（謹慎說法合理） | skills 的 model catalog 可叫 `cinematic_studio_video_4_0`（t2v / omni_reference / video_edit / video_extension），但沒有共享專案或時間軸指令 |
| 12 | Talent Contest：總獎金 US$1M、3–7 分鐘 | 正確 | 官方規則 https://higgsfield.ai/contests/talent-contest?tab=rules ：20 個獎，第一名 US$200,000 |
| 13 | 截止 2026-11-26 19:00 UTC＝台北 11-27 03:00 | 正確 | 同上 Timeline。換算正確 |
| 14 | 必須在指定 Higgsfield 專案中製作並保留素材與生成歷史；所有提交專案的 Prompt、生成紀錄與素材會公開 | 正確 | 規則 4.4、5.2、5.7：截止時所有提交作品連同 prompts、generation history、全部素材公開 |
| 15 | 外部 AI 素材不能原樣使用，須在 Higgsfield 專案中轉換 | 正確 | 規則 5.3 Qualifying Higgsfield Edit；放大、調色、裁切、改比例不算轉換 |
| 16 | 六個等權評審項目 | 正確 | 規則 9.4：Directing and Storytelling、Visual Quality、Art Direction、Sound、Editing、Originality and Concept，各 1–10 分。平均 ≥ 8、每項 ≥ 7 是本庫自訂門檻 |
| 17 | simcraft、open-edits、video-deconstructor | 存在，但都是第三方 | simcraft https://github.com/dotslashsimran/simcraft （MIT，約 540 星，含 `reverse-engineer-video`）；open-edits https://github.com/kevinbadi/open-edits （MIT，約 70 星，偏口播短片剪輯）；video-deconstructor https://github.com/shivam098/video-deconstructor （MIT，0 星，很新）。都不是 Higgsfield 官方 |
| 18 | 官方 Higgsfield ChatGPT Plugin | 正確 | https://openai.com/business/plugins/higgsfield/ ；需付費 Higgsfield 方案；走這條路徑一樣扣點 |

## 需求沒提、但會影響做法的比賽規則
- 音樂、人聲、對白、對嘴必須是 AI 生成；人聲錄音、授權音樂都不行（規則 5.5）。音效可以用有權利的非 AI 素材。
- 不得出現任何可辨識的真人或歷史人物肖像與聲音，包括自己（規則 6）。
- 要英文字幕或英文旁白，並以公開 YouTube 連結提交，浮水印與 packshot 必須完整（規則 5.1、5.6）。
- 所有 AI 影像都必須在 Contest Project、創作期內（11-12 至 11-26 UTC）生成。先前在一般專案跑的免費測試圖不能直接用。
- 公開專案的 prompts 會授權給所有 Higgsfield 用戶在站內重用（規則 11）。
- 18 歲以上；免費帳號也能參加。

## 未證實
- 在 Contest Project 裡生成是否也適用 7 天 Unlimited 圖像次數。規則沒寫；要在網站上看生成鍵。
