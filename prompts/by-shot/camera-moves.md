# 運鏡 camera move

給 image-to-video。只寫運動，不要把靜幀再描述一次。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `move-locked-off` 鎖定機位

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `daily-life` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Locked-off camera. Only the subject moves: a small shift of weight and one breath. Background geometry stays fixed. No zoom.
```

image-to-video。官方指南的結尾鏡可以是靜止機位。

### `move-dolly-in` 緩推

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `daily-life` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Slow dolly in, straight toward the subject, constant speed, no change of height. The subject holds still. Stop before the face fills the frame.
```

官方 prompt 指南把 dolly in 與 slow push 列為運動詞。

### `move-tracking` 側向跟拍

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Kling 4.0 Flash |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `trends` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Handheld tracking shot moving with the walking person, camera at their side, medium distance. Keep their full torso in frame. Background slides. No whip, no cut.
```

官方指南使用 handheld tracking 與 tracking shot。

### `move-telephoto` 望遠鏡頭壓縮

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Telephoto look, background stacked close behind the subject. Very slow dolly in. The subject blinks once. No change of outfit.
```

官方多鏡範例以 telephoto 開場。這條只測試壓縮感，人不需要跑。

### `move-arc-orbit` 弧線

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 7.5 |
| settings | 5 秒，720p |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
A short arc shot, less than a quarter orbit, camera rising slightly. Subject stays planted. End on a three-quarter view. No 360 spin, no cut.
```

官方 FAQ 點名 dolly、arc、tracking、orbital。弧線不要轉滿一圈。

### `move-whip` 甩鏡

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Grok Video 1.5 Lite |
| aspect_ratio | 9:16 |
| est_credits | 5 |
| settings | 5 秒，720p |
| bucket | `trends` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Fast whip pan from the object on the table to the person's face, then settle and hold. One move only. The face is sharp at the end. No second whip.
```

官方 prompt-engineering 提到 fast whip。只在趨勢草稿用，定稿前先看會不會糊掉主體。

### `move-drone` 高處下降

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Seedance 2.0 Mini |
| aspect_ratio | 9:16 |
| est_credits | 5 |
| settings | 5 秒，720p |
| bucket | `trends` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Wide-angle descent from above the street canopy down to standing height, smooth, no rotation. Reveal one person already waiting. No readable signs, no faces in the crowd, crowd stays out of focus if present at all.
```

官方產品廣告範例使用過寬角的 drone 運動。這條改成街景，不拍真實航班或私人窗內。

### `move-pov` 主觀前進

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Wan 3.0 |
| aspect_ratio | 9:16 |
| est_credits | 3.75 |
| settings | 5 秒，480p |
| bucket | `daily-life` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Point of view, walking forward through {place}, camera at eye height, natural head bob, no hands in frame. Stop at the doorway. No text, no map overlay.
```

最便宜的動作草稿。過關再換 720p。
