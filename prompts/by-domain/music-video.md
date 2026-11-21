# 音樂錄影帶 music video

人像與表演。歌曲在剪輯軟體另軌處理。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `mv-portrait-hold` 人像停頓

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul 2.0 |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `daily-life` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 portrait still, shoulders and head, the person looking just off camera. One colored practical behind them, dark room, 85mm, shallow depth of field. No microphone brand, no poster, no lyric text.
```

表演者是創作者本人或已同意的人。不要做特定偶像的臉。

### `mv-chorus-hit` 副歌一下

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Kling 4.0 Flash |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `trends` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
The person turns their head to camera on the first beat of movement and holds. A single practical flares and settles. Handheld, small shake, no lip sync, no lyric cards, no cut.
```

音樂在剪輯軟體另軌貼上，而且必須是可用的曲目。不要在提示詞裡寫歌名。

### `mv-orbit-neon` 霓虹半圈

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 15 |
| settings | 5 秒，1080p |
| bucket | `daily-life` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
A short orbital arc, about a quarter turn, around the person standing in a narrow alley of practical neon. They stay still. The lights do not form letters. No crowd, no cut.
```

官方 FAQ 寫明 orbital move 可以寫進提示詞。這條是短弧，不是 360 度展示。

### `mv-performance-wide` 窄空間表演

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Seedance 2.0 |
| aspect_ratio | 9:16 |
| est_credits | 22.5 |
| settings | 5 秒，720p |
| bucket | `methodology` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Wide vertical frame in a small room. The person shifts weight and lifts one hand, then returns to stillness. Camera is locked off. Practical lights stay constant. No band, no logo, no on-screen lyric.
```

方法論裡講音樂影像時才用這一檔。趨勢反應片退回 mv-chorus-hit。
