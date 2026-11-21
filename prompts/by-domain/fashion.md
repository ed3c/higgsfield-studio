# 時裝 fashion

捷運、夜市、飾品與走步。日常桶為主，一條留給趨勢節奏。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `fashion-mrt-lookbook` 捷運穿搭定場

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
Vertical 9:16 fashion still on a metro platform at {station}. The same person as the reference, wearing {garment}, one step forward as the train doors open behind them. 85mm, eye level, shallow depth of field, cool fluorescent light plus one warm practical on the platform edge. Full body in frame. No logos, no readable ads, no crowd faces.
```

`{garment}` 用今天真的穿出門的衣服。`{station}` 用站體結構，不要拍到可辨識的路人臉。

### `fashion-night-market-cloth` 夜市布料

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul Cinema |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `trends` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 still of {textile} hanging in a night-market stall. Steam in the background, tungsten bulbs, the cloth catching a rim of light. Close enough to read the weave. No brand marks, no food logos, no readable prices.
```

`{textile}` 用看得到織紋的布。趨勢片只用這張靜幀加一條 7.5 點的影片。

### `fashion-jewelry-macro` 飾品靜物

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
Vertical 9:16 still life of {jewelry} on dark stone. Soft top light, a thin rim light separating the metal from the background, one reflection on the table, the right third of the frame left empty and dark. No text, no box logo, no fingers.
```

只拍自己的飾品。官方產品攝影技能的後端提示詞不要手寫；這條是一般圖像模型用的靜物模板。

### `fashion-runway-walk` 五秒走步定稿

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Kling 4.0 |
| aspect_ratio | 9:16 |
| est_credits | 18.75 |
| settings | 5 秒，1080p |
| bucket | `daily-life` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
The person walks three steps toward camera and stops. Subtle dolly out to keep the full body in frame. Coat and hair react after the step, not before it. Background stays the same platform. No cut, no turn to a new outfit.
```

靜幀通過之後才用。image-to-video，不要重寫衣服。

### `fashion-trend-cut` 趨勢節奏短切

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
One continuous five-second take. A hand lifts {garment} into the light, then the camera tilts up to the collar. Movement is a single smooth tilt, not a montage. No beat markers, no on-screen text, no logo.
```

只借節奏，不借別人的運鏡逐格。一天內要發布。
