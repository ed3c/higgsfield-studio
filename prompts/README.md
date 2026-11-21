# 提示詞庫

給 IG Reels、TikTok 與 X 的直式畫面。預設畫幅 **9:16**。說明用繁體中文，送給模型的提示詞用英文。

每一條都是 `original-template`：句法是這個製作環境寫的。`learned_from` 指向公開技法或官方技能裡的鏡頭詞彙，不是把對方的範例整段抄進來。

沒有收錄的東西：

- OSideMedia/higgsfield-ai-prompt-skill 的提示詞。該庫已停止維護，見 `skills/UPSTREAM.md`。
- Gumroad 等付費包。研究筆記裡只記錄它們存在，沒有購置，也沒有轉貼。
- 官方 Cinema Studio 指南裡的飯店走廊、拆除大樓、披薩廣告、動畫對打等完整範例。那些文章的網址留在 `learned_from`，正文不複製。

點數是 2026-11-21 的帳戶估價。生成鍵不同就以生成鍵為準，並改記帳，不回改這份庫，除非整份計畫一起更新。

Image-to-video 用 `by-shot/camera-moves.md`，不要把靜幀內容再寫一次。

## 目錄

| id | 領域 | model | est. credits | bucket |
| --- | --- | --- | ---: | --- |
| `art-sketch-materials` | 藝術 art | Soul Cinema | 0.12 | `methodology` |
| `art-pigment-macro` | 藝術 art | Soul 2.0 | 0.12 | `daily-life` |
| `art-color-script-trio` | 藝術 art | Nano Banana Pro | 2 | `methodology` |
| `art-gallery-track` | 藝術 art | Wan 3.0 | 7.5 | `methodology` |
| `fashion-mrt-lookbook` | 時裝 fashion | Soul 2.0 | 0.12 | `daily-life` |
| `fashion-night-market-cloth` | 時裝 fashion | Soul Cinema | 0.12 | `trends` |
| `fashion-jewelry-macro` | 時裝 fashion | Nano Banana Pro | 2 | `daily-life` |
| `fashion-runway-walk` | 時裝 fashion | Kling 4.0 | 18.75 | `daily-life` |
| `fashion-trend-cut` | 時裝 fashion | Kling 4.0 Flash | 7.5 | `trends` |
| `film-empty-location` | 電影 film | Soul Cinema | 0.12 | `methodology` |
| `film-character-sheet` | 電影 film | Seedream 5.0 Pro | 2.5 | `methodology` |
| `film-night-push` | 電影 film | Wan 3.0 | 7.5 | `daily-life` |
| `film-two-shot-blue-hour` | 電影 film | Cinema Studio 4.0 | 35 | `methodology` |
| `film-locked-exit` | 電影 film | Kling 4.0 | 12.5 | `daily-life` |
| `lit-title-card` | 文學 literature | GPT Image 2.6 | 0.75 | `methodology` |
| `lit-room-from-sentence` | 文學 literature | Soul Cinema | 0.12 | `methodology` |
| `lit-object-memory` | 文學 literature | Soul 2.0 | 0.12 | `daily-life` |
| `lit-vertical-adaptation` | 文學 literature | Wan 3.0 | 7.5 | `methodology` |
| `tech-object-hero` | 科技 tech | Nano Banana Pro | 2 | `methodology` |
| `tech-bench-macro` | 科技 tech | Soul 2.0 | 0.12 | `daily-life` |
| `tech-reveal-draft` | 科技 tech | Seedance 2.0 Mini | 5 | `methodology` |
| `tech-reveal-final` | 科技 tech | Seedance 2.5 | 35 | `methodology` |
| `scifi-street-plate` | 科幻 sci-fi | Soul Cinema | 0.12 | `methodology` |
| `scifi-signage-lock` | 科幻 sci-fi | Soul 2.0 | 0.12 | `methodology` |
| `scifi-street-walk` | 科幻 sci-fi | Kling 4.0 | 18.75 | `methodology` |
| `scifi-cabin-console` | 科幻 sci-fi | Cinema Studio 4.0 | 35 | `rnd` |
| `ugc-hands-problem` | UGC／廣告 | Soul 2.0 | 0.12 | `trends` |
| `ugc-howto-step` | UGC／廣告 | Wan 3.0 | 7.5 | `trends` |
| `ugc-packshot-space` | UGC／廣告 | Nano Banana Pro | 2 | `daily-life` |
| `ugc-marketing-studio-brief` | UGC／廣告 | Marketing Studio | 60 | `rnd` |
| `mv-portrait-hold` | 音樂錄影帶 music video | Soul 2.0 | 0.12 | `daily-life` |
| `mv-chorus-hit` | 音樂錄影帶 music video | Kling 4.0 Flash | 7.5 | `trends` |
| `mv-orbit-neon` | 音樂錄影帶 music video | Wan 3.0 | 15 | `daily-life` |
| `mv-performance-wide` | 音樂錄影帶 music video | Seedance 2.0 | 22.5 | `methodology` |
| `shot-ecu` | 鏡位 shot size | Soul 2.0 | 0.12 | `daily-life` |
| `shot-cu` | 鏡位 shot size | Soul 2.0 | 0.12 | `daily-life` |
| `shot-ms` | 鏡位 shot size | Soul 2.0 | 0.12 | `daily-life` |
| `shot-ws` | 鏡位 shot size | Soul Cinema | 0.12 | `methodology` |
| `shot-ots` | 鏡位 shot size | Soul Cinema | 0.12 | `methodology` |
| `shot-low-angle` | 鏡位 shot size | Soul 2.0 | 0.12 | `daily-life` |
| `move-locked-off` | 運鏡 camera move | Wan 3.0 | 7.5 | `daily-life` |
| `move-dolly-in` | 運鏡 camera move | Wan 3.0 | 7.5 | `daily-life` |
| `move-tracking` | 運鏡 camera move | Kling 4.0 Flash | 7.5 | `trends` |
| `move-telephoto` | 運鏡 camera move | Wan 3.0 | 7.5 | `methodology` |
| `move-arc-orbit` | 運鏡 camera move | Wan 3.0 | 7.5 | `methodology` |
| `move-whip` | 運鏡 camera move | Grok Video 1.5 Lite | 5 | `trends` |
| `move-drone` | 運鏡 camera move | Seedance 2.0 Mini | 5 | `trends` |
| `move-pov` | 運鏡 camera move | Wan 3.0 | 3.75 | `daily-life` |

## 檔案

- `by-domain/` 八個領域
- `by-shot/shot-sizes.md` 鏡位
- `by-shot/camera-moves.md` 運鏡

改這份庫時，編輯 `prompts/_render_library.py` 的 `ENTRIES`，再執行 `python3 prompts/_render_library.py`。不要只改產生的 Markdown，下一次重跑會蓋掉。
