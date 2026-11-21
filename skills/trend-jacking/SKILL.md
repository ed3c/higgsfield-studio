---
name: trend-jacking
description: |
  在 24–48 小時內，用創作者自己的生活場景與 Higgsfield 工藝接上 IG Reels、TikTok、X 的當週趨勢。
  Use when: trend, trending audio, trend-jacking, 趨勢二創, 跟拍, 爆款聲音, 48 小時.
  NOT for: 復刻別人的成片、方法論長集（用 methodology-breakdown）、與趨勢無關的日常片（用 daily-life-remix）、
  為了跟趨勢使用 Seedance 1080p、Cinema Studio 30 秒或 4K。
---

# 趨勢二創 trend-jacking

只跟「48 小時內，用自己的生活素材加上 Higgsfield 工藝能做出差異」的趨勢。鉤子、節奏與音樂可借。鏡頭、場景與故事必須是自己的。不要逐鏡復刻別人的影片。

## 偵察

用 `templates/weekly-trend-scouting.md`。每天 08:00–08:30（台北時間）只記三件事：鉤子、音樂或句式、視覺模式。週一上午再做一次深度偵察。

選定之前寫下這三行，缺一行就換題：

- 這個趨勢的可借用部分（聲音、句式、剪輯節奏）
- 我自己的場景與物件（必須是這週真的拍得到的）
- 我不借用的部分（別人的臉、逐鏡分鏡、商標、未授權音樂）

音樂若要走商用，只用創作者已確認可用的曲目。不要把平台上聽到的歌名寫進生成提示詞裡冒充授權。

## 點數

桶是 `trends`（每月 1,980 點）。先跑 `python3 budget/track.py`。

趨勢片的成本上限：Soul 靜幀 0.12 點，加上一條 Wan 3.0 720p 或 Kling 4.0 Flash 5 秒（7.5 點）。一條趨勢片的計畫區間是 40–60 點，含少量草稿。不要為跟趨勢啟用 Seedance 1080p、Veo Preview 或 Cinema Studio 30 秒。

週中若已花掉當週約 2,250 點上限的 70%，而成品支數不夠，後續趨勢片只留 Wan / Kling Flash。

## 製作

1. 從 `projects/_template/` 複製專案夾。`brief.md` 寫趨勢來源（平台、日期、你觀察到的模式），不要貼上別人的完整影片檔。
2. 提示詞用 `prompts/by-domain/` 裡標了趨勢桶的模板，或 `prompts/by-shot/camera-moves.md` 的短動作句。畫幅 9:16。
3. 生成順序走 [draft-to-final-upscale](../draft-to-final-upscale/SKILL.md)，但定稿停在 7.5 點這一檔，除非 `brief.md` 寫明這條已從趨勢升格成日常定稿。
4. 當天中午前鎖定要發的一版。趕不上就放棄這條趨勢，不要追加定稿次數。
5. 文案用 `templates/captions-hashtags.md`。TikTok 更短、起點更快；IG 可留一句方法；X 用 8–15 秒鉤子。

## 發布之後

12 小時後看前 3 秒停留。低於自己的中位數時，在 `edit-notes.md` 寫鉤子問題。不要對同一模板再花錢。下一條趨勢片換鉤子再測。

每一筆寫入 `generations.csv` 與 `budget/ledger.csv`，`bucket` 為 `trends`。

## 參考

- 週曆：`plan/monthly-usage-and-content-strategy.md` 的趨勢偵察流程
- 可研究的節奏，不是可複製的成片：illusiovibe（短影音）、Kevin Charles（病毒內容）。索引在 `creators/index.md`
