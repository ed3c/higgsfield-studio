---
name: methodology-breakdown
description: |
  製作一集鏡前方法論：用一個工業級做法，講藝術、時裝、電影、文學、科技或科幻，並給出觀眾能模仿的步驟。
  Use when: methodology episode, breakdown, on camera, 方法論, 拆解, 工業級, 鏡前講解.
  NOT for: 沒有講解的日常片（用 daily-life-remix）、純趨勢跟拍（用 trend-jacking）、
  無出鏡的 faceless 解說（官方 higgsfield-faceless-video；本系列要創作者出鏡講）。
---

# 方法論拆解 methodology breakdown

每集一個方法、一條工業級範例鏡、一次觀眾可以跟著做的演練。完整集 45–90 秒。另剪 12–15 秒鉤子給 TikTok 與 X。鏡前講解用創作者自己的聲音；示範畫面用 Higgsfield 定稿。

點數桶是 `methodology`（每月 2,520 點）。單集目標 180–280 點，不含重試預備。先跑 `python3 budget/track.py`。這個桶達到分配額 80% 時，當週第二集改成靜幀對比，不再開 Cinema Studio 1080p。

## 集數結構

時間軸與口播骨架用 `templates/episode-script.md`，分鏡用 `templates/episode-shot-list.md`。

| 段 | 時間 | 畫面點數原則 |
| --- | --- | --- |
| 鉤子 | 0–3 秒 | 本集最強的定稿鏡。不自我介紹 |
| 承諾 | 3–8 秒 | 成品與原始素材分屏，可用實拍 |
| 原料 | 8–18 秒 | 實拍，或 Soul / Soul Cinema 靜幀（0.12 點） |
| 方法 | 18–50 秒 | 螢幕錄影與中間稿。草稿影片用 3.75–7.5 點的模型 |
| 失敗與修正 | 50–65 秒 | 展示一次不過關的取次。用已經生成的失敗鏡，不要為了「表演失敗」再抽一條定稿 |
| 工業級輸出 | 65–85 秒 | 一條定稿。Cinema Studio 4.0 5 秒 720p（35 點）、Seedance 2.5 5 秒 720p（35 點）或 Kling 4.0 5 秒 1080p（18.75 點） |
| 呼籲 | 最後 5 秒 | 下集封面靜幀。Nano Banana Pro 2K（2 點）或 Soul（0.12 點） |

1080p 的 Seedance 或 Cinema（約 80 點一鏡）只用在開場或結尾，而且 `brief.md` 要寫明理由。30 秒 Cinema Studio 4.0 720p（210 點）不在單集計畫裡。

對口型優先 Kling Lipsync（官方頁面：5 秒 720p 為 2 點）。Sync Lipsync 3 預設 5 秒是帳戶估價 18 點，只在 Kling 對不上時改用。講解聲音以創作者實錄為主，生成語音不是預設。

## 選題

六個領域輪流：藝術、時裝、電影、文學、科技、科幻。題目庫見計畫裡的首月十集，正式開題時改寫進該集 `brief.md`，不要每集都重拍同一條捷運。

文學集不得把仍在著作權保護內的小說正文貼進提示詞或字幕。用創作者自己的句子，或已進入公共領域的短句，並在 `prompts-used.md` 註明出處。

研究誰的流程、而不是下載誰的畫布來重生成：

- 教學結構：JOEY（公開 skill 流程）
- 敘事完成度：PURGA、AIST
- 科幻方法：Yoav Yariv
- 文學轉影像：Authors First（官方案例是流程，不是可複製的劇本）
- 工業預製：Boxel Studio

名單與理由在 `creators/study-queue.md`。

## 與官方技能的分工

- 角色參考與場景參考的做法，讀官方 filmmaking 指南：https://higgsfield.ai/blog/how-to-master-ai-filmmaking
- 多鏡、`@image` 參考、延續上一條影片而不重做 keyframe：官方 Cinema Studio 指南只借用做法名稱，不複製其中的範例腳本。https://higgsfield.ai/blog/cinema-studio-3.0
- 送出生成用官方 `higgsfield-generate`。本技能不提供會直接扣點的指令。
- OSideMedia 的 MCSLA 只可當檢查清單（有沒有寫模型、鏡頭、主體、外觀、動作）。不要打開那個已停止維護的倉庫來複製提示詞。見 `skills/UPSTREAM.md`。

## 完成定義

- 三平台版本都記在 `published.md`：TikTok 完整或 45–60 秒、IG 45–90 秒、X 為 8–15 秒鉤子加一則方法串文。
- 串文用繁體中文步驟，英文三行以內。Hashtag 4–6 個，見 `templates/captions-hashtags.md`。
- 點數記入 `bucket=methodology`。失敗退點的列 `refunded=yes`。
