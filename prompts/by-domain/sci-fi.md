# 科幻 sci-fi

先鎖真實街道，再加少量近未來光線。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `scifi-street-plate` 街頭空景

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
Vertical 9:16 empty street plate of {street}. Keep the real building masses, the scooter lane, and the awning line. No people, no readable shop names, dusk, wet asphalt, practical shop light only.
```

先做真實街道的結構參考，再在下一條加近未來物件。建築輪廓以參考圖為準。

### `scifi-signage-lock` 招牌鎖定

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul 2.0 |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Same street as the location reference, vertical 9:16. Add thin practical light strips along the existing awnings and one small hovering indicator above the lane. Do not move the buildings, do not translate any sign into readable text, do not add a crowd.
```

用 `@` 或參考圖鎖住 scifi-street-plate。新物件只有燈條，不改建築。

### `scifi-street-walk` 近未來街道行走

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Kling 4.0 |
| aspect_ratio | 9:16 |
| est_credits | 18.75 |
| settings | 5 秒，1080p |
| bucket | `methodology` |
| learned_from | 鏡頭詞彙對齊官方 skill higgsfield-generate 的 prompt-engineering.md（MIT，skills/vendor，v0.14.0）：主體、鏡頭、光線，image-to-video 只寫運動。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
The person walks along the locked street. Tracking shot beside them, medium distance, slight low angle. The added light strips stay fixed to the awnings. Reflections slide on the wet ground. No new vehicles enter, no readable text, no cut.
```

定稿鏡。身份用 Soul ID 或角色表。

### `scifi-cabin-console` 艙內控制台

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Cinema Studio 4.0 |
| aspect_ratio | 9:16 |
| est_credits | 35 |
| settings | 5 秒，720p |
| bucket | `rnd` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 cabin interior. One person, seen from behind, sits at an unlabeled console. Slow dolly in. Status lights change brightness but never form letters. No franchise costume, no known robot design, no dialogue.
```

實驗桶。確認生成鍵之後才送。不要做 4K。
