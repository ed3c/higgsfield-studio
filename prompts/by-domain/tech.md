# 科技 tech

無商標器物。揭示片先草稿再定稿。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `tech-object-hero` 器物主視覺

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Nano Banana Pro |
| aspect_ratio | 9:16 |
| est_credits | 2 |
| settings | 2K |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 hero still of {device} on a matte bench. One hard strip of light across the surface, dark background, the right third empty for a later caption. No logo, no UI, no screen text, no hands.
```

`{device}` 用無商標的自製物件或去掉標誌的通用器材。不要做真實公司的產品照。

### `tech-bench-macro` 工作檯切面

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
Vertical 9:16 still of a workbench at night. A small unlabeled device, a notebook with a blank page, a monitor glow with no readable interface. 35mm, slight overhead angle. No brand, no notification bubbles.
```

用自己的桌面。螢幕內容要模糊到讀不出字。

### `tech-reveal-draft` 揭示草稿

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Seedance 2.0 Mini |
| aspect_ratio | 9:16 |
| est_credits | 5 |
| settings | 5 秒，720p |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
A hand slides {device} from shadow into the strip of light, then lets go. Camera holds. No logo reveal, no screen turns on, no spoken claim.
```

草稿。過關再用 tech-reveal-final。三段式是官方產品廣告指南的結構，產品與動作是原創。

### `tech-reveal-final` 揭示定稿

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Seedance 2.5 |
| aspect_ratio | 9:16 |
| est_credits | 35 |
| settings | 5 秒，720p |
| bucket | `methodology` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Locked lighting. The unlabeled device rotates a quarter turn on the bench as the camera arcs slowly to the left. One specular highlight travels across the shell. No text, no logo, no cut, no music visualizer.
```

只在草稿通過後使用。不要升到 1080p（計畫中的 5 秒 1080p 是 80 點）除非 brief 寫明這是開場鏡。
