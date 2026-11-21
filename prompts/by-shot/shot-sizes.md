# 鏡位 shot size

靜幀鏡位。可套進任何領域，畫幅 9:16。

預設畫幅 9:16。改 `{占位符}` 之後再送出。

### `shot-ecu` 極特寫

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
Vertical 9:16 extreme close-up of {detail}. The background is only color. Focus sits on the nearest edge. No text.
```

`{detail}` 是眼睛、布邊、金屬緣這類局部。

### `shot-cu` 特寫

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul 2.0 |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `daily-life` |
| learned_from | 製作順序來自 How to Master AI Filmmaking（https://higgsfield.ai/blog/how-to-master-ai-filmmaking）：角色參考與空場景分開，再進影片。提示詞是原創模板。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 close-up of the face from the reference, three-quarter view. Eyes sharp, background fully soft, one light from the side. No beauty-filter skin, no text.
```

官方 filmmaking 指南的第二鏡就是臉部特寫。這條是靜幀版。

### `shot-ms` 中景

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
Vertical 9:16 medium shot, waist up, of the person in {place}. Hands visible and still. Eye-level camera. Room light matches the window. No props with logos.
```

腰部以上。

### `shot-ws` 廣角定場

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
Vertical 9:16 wide shot of {place}. The person stands near the lower third and is about one fifth of the frame height. Show floor and ceiling or sky. 35mm. No crowd faces.
```

人在畫面裡要小，才有定場的作用。

### `shot-ots` 過肩

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul Cinema |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `methodology` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 over-the-shoulder still. The near shoulder is soft in the foreground. Beyond it, the other person or the empty doorway is sharp. No dialogue caption.
```

官方多鏡範例使用過肩。第二個人若不是同意出鏡的對象，就改成看向空場景。

### `shot-low-angle` 低角度

| 欄位 | 內容 |
| --- | --- |
| kind | original-template |
| model | Soul 2.0 |
| aspect_ratio | 9:16 |
| est_credits | 0.12 |
| settings | 2K |
| bucket | `daily-life` |
| learned_from | 技法名稱來自 Higgsfield 官方 Cinema Studio Prompt Guide（Mariam Barova，https://higgsfield.ai/blog/cinema-studio-3.0）。提示詞是原創模板，不是該文的範例腳本。 點數來自 plan/monthly-usage-and-content-strategy.md 的 2026-11-21 帳戶估價。送出前以生成鍵為準。 |

```text
Vertical 9:16 low-angle still, camera near knee height, looking up at the person in {place}. Ceiling or sky occupies the top third. No heroic costume, no lens flare streak across the face.
```

官方指南把 low-angle 當作可指定的角度。
