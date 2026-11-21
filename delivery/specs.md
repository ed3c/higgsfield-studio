# 交付規格

機器可讀版：`profiles.json`，`qc/mech_check.py --profile <名稱>` 直接讀它。數值是 2026-11-22 的計畫目標，上傳前以平台當下的上傳頁為準。

| 名稱 | 解析度 | 編碼 | 片長 | 文字安全區（約） |
| --- | --- | --- | --- | --- |
| `tiktok` | 1080×1920 | H.264/HEVC，yuv420p，AAC | ≤ 10 分 | 上 150、下 420、右 140 px 不放字 |
| `instagram-reels` | 1080×1920 | H.264/HEVC，AAC | 計畫用 ≤ 3 分 | 上 220、下 420 px |
| `x-vertical` | 1080×1920 | H.264，AAC | ≤ 2:20（一般帳號） | 上 120、下 300 px |
| `youtube-shorts` | 1080×1920 | H.264 等 | ≤ 3 分 | 上 180、下 380、右 160 px |
| `youtube-master-4k` | 3840×2160 | H.264/HEVC/ProRes，48 kHz | 不限 | 5% title safe |
| `higgsfield-contest` | 任意比例，長邊 ≤ 3840 | MP4 或 MOV | 3:00–7:00 | 浮水印與 packshot 必須完整保留 |

## 共通
- 混音：串流平台 -14 LUFS integrated，true peak ≤ -1 dBTP。`mech_check.py` 只擋削波（峰值 ≥ -0.1 dBFS），響度要在 Resolve 裡量。
- 字幕：另出 `.srt`；燒進畫面的字只放在安全區內。
- 比賽版另需英文字幕或英文旁白，並以公開 YouTube 連結提交（官方規則 https://higgsfield.ai/contests/talent-contest?tab=rules ）。
