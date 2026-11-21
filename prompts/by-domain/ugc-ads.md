# UGC／廣告

問題、一步教學、packshot。貴的 Marketing Studio 放在實驗桶。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `ugc-hands-problem` 問題是一雙手

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul 2.0 |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `trends` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 still, close on two hands at a kitchen counter, paused before using {product}. Morning window light. The product is generic packaging with no logo. Face is out of frame. No app UI, no captions.
```

官方產品廣告指南把廣告分成問題、解法、packshot。這裡只做問題靜幀，產品用自己的。

### `ugc-howto-step` 一步教學

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `trends` |
| learned_from | 行銷模式名稱來自官方 skills README 的 Marketing Studio 模式表（MIT，v0.14.0）。這是交給官方 higgsfield-generate 的 brief，不是手寫的後端提示詞。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Hands complete one step with {product}: open, place, and stop. Camera stays overhead, static. No second step, no talking head, no lower-third text.
```

若改走 Marketing Studio 的 `ugc_how_to`，用官方技能，不要把這段再改寫成後端提示詞。這段是一般影片草稿。

### `ugc-packshot-space` 留白的 packshot

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Nano Banana Pro |
| aspect_ratio | 9:16 |
| est_credits | 2 |
| settings | 2K |
| bucket | `daily-life` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 packshot. {product} held at the left third, neutral background, soft light. The right third is empty. No letters, no logo, no extra props.
```

右側留白是為了後製貼自己的字，不要讓模型生成文字。

### `ugc-marketing-studio-brief` Marketing Studio 任務說明

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Marketing Studio |
| aspect_ratio | 9:16 |
| est_credits | 60 |
| settings | 12 秒，720p，含音訊 |
| bucket | `rnd` |
| learned_from | 行銷模式名稱來自官方 skills README 的 Marketing Studio 模式表（MIT，v0.14.0）。這是交給官方 higgsfield-generate 的 brief，不是手寫的後端提示詞。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Brief, not a final model prompt: 9:16, 12 seconds, mode {marketing_mode}. Product is {product}, photographed by me, no trademark. Show one problem and one use. Leave the lower third clear of generated text. Do not invent claims about health, price, or reviews.
```

60 點一條，只放實驗桶，而且一個月最多評估一次。模式用官方的 `ugc`、`ugc_how_to`、`ugc_unboxing`、`product_showcase` 或 `product_review`。交給 higgsfield-generate，不要自己組最終 prompt。
