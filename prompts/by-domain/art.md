# 藝術 art

素描、材質、色彩腳本與展間。方法論的藝術集從這裡拿靜幀。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `art-sketch-materials` 同一張素描的三種材質

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
Vertical 9:16 still, three equal panels of the same {sketch_subject} drawn by one hand. Left panel: dry charcoal on warm paper. Middle panel: thin oil paint with visible brush ridges. Right panel: glazed ceramic relief of that same drawing. Same pose, same crop, soft north light, no text, no signature, no frame on the wall.
```

`{sketch_subject}` 用創作者自己的素描主題，例如「一隻摺紙鶴」。不要畫受保護的角色。

### `art-pigment-macro` 顏料切面

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
Vertical 9:16 macro still of a cut stick of {pigment} pigment on a kitchen table. 85mm, tack sharp at the broken edge, crumbs in the foreground, window light from screen left, the rest of the table falling soft. No labels, no brand names, no hands.
```

`{pigment}` 用當天桌上真的有的顏色。

### `art-color-script-trio` 三張色彩腳本

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Nano Banana Pro |
| aspect_ratio | 9:16 |
| est_credits | 2 |
| settings | 2K |
| bucket | `methodology` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 color-script still of {place}. Palette limited to cobalt, warm paper white, and one copper accent. Empty of people. Show the light direction clearly: a single practical lamp and a cool window. No readable signage, no logos. This frame is a lighting reference, not a poster.
```

三張分開生成，`{place}` 同一地點。只在外觀鎖定後才進入 Seedance。

### `art-gallery-track` 小展間橫移

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
Slow lateral tracking shot along the wall, camera at eye height, constant speed. The frames drift through the shot one by one. Floor reflection moves with the camera. No new people enter. No whip, no zoom.
```

用已鎖定的展間靜幀當 start image。提示詞不要重描述畫作內容。
