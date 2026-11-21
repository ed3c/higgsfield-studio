---
name: draft-to-final-upscale
description: |
  把一支 Higgsfield 短影從靜幀草稿做到定稿，再決定要不要放大。強制記帳，並在每月點數達到分配額 80% 時停下。
  Use when: draft, final, upscale, reframe, 草稿, 定稿, 放大, 取次, credit budget, 點數.
  NOT for: 決定這支片屬於哪一條內容支柱（先用 daily-life-remix、trend-jacking 或 methodology-breakdown）、
  訓練 Soul ID（官方 higgsfield-soul-id）、手寫 Marketing Studio 或產品攝影的後端提示詞。
---

# 草稿到定稿 draft-to-final upscale

所有會扣點的步驟都走這份順序。模型單價以 `plan/monthly-usage-and-content-strategy.md` 的 2026-11-21 帳戶估價為計畫值，送出前以生成鍵為準。估價與生成鍵不一致時，以生成鍵記帳，並在 `note` 寫下差異。

## 0. 記帳閘門

```bash
python3 budget/track.py
```

- 該桶或當月 9,000 點合計達到 80%：不得新增定稿模型。可以停工，或只在網站上使用仍然免費的 Soul 次數。
- MCP、CLI、Canvas、Supercomputer 上的生成一律扣點。網站 Unlimited 與免費次數不要搬到這些路徑上重跑。
- 重試預備（1,620 點）只用於已完成但不夠好的定稿，不用來開新題。

## 1. 靜幀草稿

用 Soul 2.0 或 Soul Cinema，1.5K 或 2K，9:16，帳戶估價 0.12 點。先鎖定角色、服裝、場景與光線。文字標題卡才改用 GPT Image 2.6 low 1K（0.75 點）。

這一階可以多試。不要在外觀還沒鎖定時做影片。

## 2. 挑選一張

只讓一張靜幀進入影片。選不下去就改提示詞，而不是把五張都做成影片。

## 3. 影片草稿

5 秒。依序考慮：

| 用途 | 模型 | 帳戶估價 |
| --- | --- | ---: |
| 動作試看 | Wan 3.0 480p，或 Grok Video 1.5 Lite / Seedance 2.0 Mini 720p | 3.75–5 |
| 趨勢與已鎖定的日常草稿 | Wan 3.0 720p、Kling 4.0 Flash、Kling 3.0 Turbo | 7.5 |

Image-to-video 的提示詞只寫運動與鏡頭，不要把靜幀再描述一次。官方 `higgsfield-generate` 的 `references/prompt-engineering.md` 說明了這條限制。

## 4. 檢視

不過關的理由只能是下面其中一項，寫進 `edit-notes.md`：

- 身份或服裝漂移
- 動作不符合分鏡
- 鏡頭方向錯了
- 文字、手或結構明顯壞掉
- 光線與已鎖定的靜幀衝突

「感覺不夠酷」不是再抽一條同設定定稿的理由。先改提示詞或退回草稿模型。

## 5. 一次定稿

通過檢視的鏡才升檔。預設仍是 5 秒、9:16。

| 支柱 | 定稿 | 帳戶估價 |
| --- | --- | ---: |
| 趨勢 | 停在 7.5 點那一檔 | 7.5 |
| 日常 | Wan 3.0 1080p，或 Kling 4.0 720p／1080p | 12.5–18.75 |
| 方法論 | Cinema Studio 4.0 5 秒 720p、Seedance 2.5 5 秒 720p，或 Kling 4.0 1080p | 18.75–35 |

同一設定的定稿最多兩次（1.2–1.4 次取次）。第二次不過關：改提示詞，或退回草稿模型。不要第三次用同一設定抽定稿。第二次的點數記入 `bucket=retry`。

Veo 3.1 Preview ultra（120 點）、Seedance 2.5 十秒 1080p（160 點）、4K 與 30 秒 Cinema，只放在 `bucket=rnd`，而且 `brief.md` 要先寫假設。

## 6. 放大與改畫幅

先有鎖定的定稿，再放大。

- 圖像放大：ByteDance 圖像放大到 2K 或 4K，帳戶估價 2 點。只用於已決定發布的封面。
- 影片放大：計畫書把 ByteDance 影片放大標成估計（未帶來源檔時 2K 約 2 點、4K 約 4 點）。這兩個數字不完整。送出前讀生成鍵，並把實際點數寫進帳。
- 平台畫幅：先完成 9:16 母帶。X 的 1:1 或 IG 的 4:5 靜幀用裁切或官方指南所說的 Reframe，不要為了畫幅整支重生成。Reframe 的點數以生成鍵為準。

官方完成工具的名稱（Relight、Edit Color Palette、Trim、Extend、Reframe、Upscale）來自 https://higgsfield.ai/blog/how-to-master-ai-filmmaking 。能用這些改完成片時，不要整段重抽。

## 7. 記帳

每一筆，包含退點，都寫入專案的 `generations.csv`，並追加到 `budget/ledger.csv`：

```csv
date,bucket,model,settings,aspect_ratio,credits,project,outcome,refunded,prompt_id,note
```

- `bucket`：`methodology`、`daily-life`、`trends`、`retry`、`rnd` 之一。
- `refunded`：平台已退點寫 `yes`，否則 `no`。`budget/track.py` 不把退點算進花費。
- `outcome`：`draft`、`final`、`upscale`、`rejected` 之一。

記完再跑一次 `python3 budget/track.py`。
