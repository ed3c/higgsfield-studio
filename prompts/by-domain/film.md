# 電影 film

先空場景與角色表，再夜景、兩鏡定稿與鎖定結尾。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `film-empty-location` 空場景

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
Vertical 9:16 empty location of {place} at {time_of_day}. No people. Show the floor, the main practical light, and one depth cue such as a doorway or a window. Camera at standing eye height, 35mm. The light direction must be obvious enough to reuse in the next shot.
```

`{place}` 先用自己家或公開街景的結構。這張圖之後當 location reference。

### `film-character-sheet` 角色三視圖

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Seedream 5.0 Pro |
| aspect_ratio | 9:16 |
| est_credits | 2.5 |
| settings | 預設 |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 character sheet of {character_description}, front view, three-quarter view, and side view, same outfit, same neutral standing pose, even soft light, plain warm-gray background. No scene, no text labels, no weapons, no logos.
```

虛構角色用這條。真人用 Soul ID，不要用這條去複製某個公眾人物。

### `film-night-push` 夜景緩推

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
Slow push in toward the person at the window. Red practical light from a lamp, green practical light from the street outside, fine film grain, slight motion smear only on the rain on the glass. The person does not speak. No poster, no subtitle, no cut.
```

家中實景重拍。不要點名特定電影或導演，避免被模型當成要模仿某部作品的畫面。

### `film-two-shot-blue-hour` 藍時兩鏡

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Cinema Studio 4.0 |
| aspect_ratio | 9:16 |
| est_credits | 35 |
| settings | 5 秒，720p，可開聲音 |
| bucket | `methodology` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Two shots, one hard cut at 2.5 seconds. 9:16. Shot 1: wide, the person from the character reference stands small in the empty location, blue hour, camera slowly dollies in. Shot 2: close-up, a passing warm light crosses their face, they turn their head a little toward the light. No dialogue. Sound is only room tone and a distant vehicle. Outfit and light direction stay the same across the cut.
```

方法論定稿才用。參考圖用 `@` 標註自己的角色表與空場景。不要加長到 30 秒。

### `film-locked-exit` 鎖定離開

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Kling 4.0 |
| aspect_ratio | 9:16 |
| est_credits | 12.5 |
| settings | 5 秒，720p |
| bucket | `daily-life` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Locked-off camera. The person walks away from camera toward the doorway, stops, and looks back once. The lamp above the door does not flicker. No other person enters. End before they touch the handle.
```

官方指南把靜止鏡頭當作可描述的運鏡。這條用在結尾，不要加對白。
