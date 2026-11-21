# 文學 literature

只處理創作者自己的句子或已確認的公共領域短句。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `lit-title-card` 一句話標題卡

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | GPT Image 2.6 |
| aspect_ratio | 9:16 |
| est_credits | 0.75 |
| settings | low，1K |
| bucket | `methodology` |
| learned_from | 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 title card. The only words are: "{line}". Set them in a plain serif, lower third, on a dim room photograph with one lamp. No author name, no book cover, no publisher mark, no extra slogan.
```

`{line}` 只能是創作者自己寫的句子，或已確認進入公共領域的短句。不要貼仍受保護的小說正文。

### `lit-room-from-sentence` 由句子長出的房間

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul Cinema |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `methodology` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 empty room that could illustrate this original sentence: "{line}". Show only the objects named in that sentence, plus one window. No people, no printed book, no cover typography. Light matches the mood of the sentence without adding new plot.
```

用自己的句子描述光線與物件，不要描述某本書的角色名。

### `lit-object-memory` 物件記憶特寫

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
Vertical 9:16 close still of {object} on a reading table. A cup ring, a folded blank page, warm lamp, cool window. No readable writing, no printed paragraph, no portrait.
```

`{object}` 用桌上現成的東西。

### `lit-vertical-adaptation` 直式轉場

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `methodology` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
A slow push from the object on the table up to the window. Curtain moves once. No one enters. No words appear. No music cue in the picture.
```

start image 用 lit-room-from-sentence 的靜幀。
