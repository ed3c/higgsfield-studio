---
name: daily-life-remix
description: |
  把台灣創作者的日常生活素材重拍成 IG Reels、TikTok 與 X 的短影或靜幀。
  Use when: daily life remix, commute, breakfast, night market, living room,
  日常再創作, 把今天的照片重拍, 捷運穿搭, 原地素材.
  NOT for: 24–48 小時趨勢跟拍（用 trend-jacking）、鏡前方法論長集（用 methodology-breakdown）、
  只做放大或記帳（用 draft-to-final-upscale）、訓練 Soul ID（用官方 higgsfield-soul-id）。
---

# 日常再創作 daily-life remix

把通勤、餐桌、街景、家中光線重拍成時裝、電影或音樂錄影式短片。觀眾要看到「原地材料 → 工業級輸出」。不要重拍成另一個人的一天。

## 開始之前

1. 確認這支片的桶是 `daily-life`（每月 2,250 點）。跑 `python3 budget/track.py`。這個桶或當月合計已達 80% 時，只做 Soul 靜幀，不做 1080p 定稿。
2. 開一個 `projects/YYYY-MM-DD-slug/`（從 `projects/_template/` 複製）。在 `brief.md` 寫下原地素材是什麼、要變成哪一種完成片。
3. 素材用創作者自己拍的照片或短片。不要用路人可辨識的臉當作主角，除非已有使用同意。
4. 畫幅預設 9:16。提示詞從 `prompts/by-domain/` 選一條原創模板再改 `{占位符}`，並把用到的 id 寫進 `prompts-used.md`。

## 製作順序

靜幀與影片的模型分級、以及「第二次定稿不過關就停止」，走 [draft-to-final-upscale](../draft-to-final-upscale/SKILL.md)。這份技能只決定日常片的內容。

1. **鎖一個轉換**。一支片只做一種：時裝週式穿搭、夜景電影感、或音樂錄影式人像。不要在同一條 15 秒裡三個都做。
2. **先出原地對照**。留一張未重拍的生活照，完成片要讓人看得出起點。對照可以是實拍，不必再花點數。
3. **角色一致**。出鏡的是創作者本人時，用已訓練的 Soul ID（官方技能 `higgsfield-soul-id` 的 `reference_id`）。還沒訓練時，第一週只做不靠臉的物件、服裝與空間；Soul ID 訓練是官方頁面所列的一次性 25 點，從實驗研發或當週日常桶支出，並記帳。
4. **場景先於動作**。用 Soul Cinema 做一張空的場景靜幀，再把人放進去。這是官方 filmmaking 指南的順序：角色參考與場景參考分開，再進影片。見 https://higgsfield.ai/blog/how-to-master-ai-filmmaking
5. **草稿影片 5 秒**。日常桶的草稿用 Wan 3.0 720p、Kling 4.0 Flash 或 Kling 3.0 Turbo（帳戶估價各 7.5 點）。過關後的定稿才用 Wan 3.0 1080p 或 Kling 4.0 720p／1080p（12.5–18.75 點）。
6. **剪接**。默認兩到三條 5 秒鏡，剪成 12–25 秒。不要為日常片開 30 秒 Cinema Studio（720p 為 210 點）。
7. **文案**。用 `templates/captions-hashtags.md`。中文第一句單獨成立，英文給 X 與海外流量。標 4–6 個 hashtag。

## 完成定義

- `generations.csv` 每一條生成都有點數、模型、prompt id、是否退點。
- 同一列追加到 `budget/ledger.csv`，`bucket` 為 `daily-life`。
- `published.md` 留下三平台連結與發布後 12 小時的前 3 秒停留。沒發的平台寫「未發」與原因。

## 參考

- 點數與週曆：`plan/monthly-usage-and-content-strategy.md`
- 提示詞：`prompts/by-domain/fashion.md`、`film.md`、`music-video.md`
- 官方執行：`skills/vendor/higgsfield-ai-skills/higgsfield-generate/SKILL.md`
- 可研究的創作者：Tseily（電影感日常）、Aleksandra（時裝與藝術教育）。見 `creators/study-queue.md`
