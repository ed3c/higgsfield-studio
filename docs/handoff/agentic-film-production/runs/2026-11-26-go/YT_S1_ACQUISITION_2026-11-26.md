# S1 YouTube 取得（§13）— 2026-11-26

來源：https://www.youtube.com/watch?v=onNBysMf9WM （S1，H01）

## 結論

**YT0 BLOCKED_SOURCE/RIGHTS。沒有下載任何媒體位元組。YT1–YT4 依 §13「前置未 PASS 則相依暫停」保持 NOT_RUN。H01 下載未完成。**

## 公開 metadata（唯讀，未請求媒體串流）

以匿名 curl 讀取公開 watch page 的 `ytInitialPlayerResponse`（watch page sha256 `8eab978b…4729`，原始 HTML 只存 box 私有目錄）。完整欄位見 `s1_public_metadata.json`。

| 欄位 | 觀察值 |
|---|---|
| 標題 | 展覧会ドキュメント「坂本龍一 with 高谷史郎｜設置音楽2　IS YOUR TIME」 |
| 頻道 | NTTインターコミュニケーション・センター [ICC]（`UCc6CCp_Wig8hpX2p6lyR2MQ`）|
| 長度 | 2333 秒（38:53）|
| 發佈 | 2018-04-06（UTC-7）|
| 可播放 | `OK`；`playableInEmbed=false`；oEmbed 回 401 |
| 字幕 | player response 沒有 `captions` 欄位（0 條字幕軌，含自動字幕）|
| 授權標示 | 頁面沒有 Creative Commons 標記 → 標準 YouTube 授權 |

## YT0–YT4

| Gate | 狀態 | 證據 | 解除條件 |
|---|---|---|---|
| YT0 Source | **BLOCKED** | URL/ID 已由 Neon 指定（t37u），但權利人為 NTT ICC，標準授權、embed 停用；沒有記錄任何權利人許可或官方下載途徑。§3 Rights 規定只取得自有或已授權來源，且須符合平台條款。`studio/source/yt_gates.py` 判定：`no rights.json` | Neon 提供權利依據（見下方問題），寫入私有 `rights.json` 後重跑 verifier |
| YT1 Video | NOT_RUN | 相依 YT0 | — |
| YT2 Audio | NOT_RUN | 相依 YT1 | — |
| YT3 SRT | NOT_RUN | 相依 YT1。另記事實：公開 player response 沒有官方或自動字幕，未來須走已准入的 Whisper ASR（目前沒有准入版本）| 准入 Whisper build（版本、權重授權、依賴）|
| YT4 Evidence | NOT_RUN | 相依 YT0–YT3 | — |

Verifier 原始輸出：`yt_gates_S1_2026-11-26.json`（exit code 3 = H01 未完成）。

## 給 Neon 的問題（YT0）

> S1 是 NTT ICC 頻道上的《坂本龍一 with 高谷史郎｜設置音楽2 IS YOUR TIME》展覽紀錄片（38:53，標準 YouTube 授權、停用嵌入、沒有字幕）。下載需要權利依據。你有下列哪一種嗎？
> (a) ICC 或權利人對下載與私下分析的書面許可；
> (b) ICC 官方提供的原檔或官方下載途徑；
> (c) 其他你能出示的授權依據。
> 若都沒有，S1 維持 BLOCKED_SOURCE/RIGHTS，只暫停 H01/H02，Passport Rush 軌道照常進行。

## 工具與授權（記錄，未執行下載）

| 工具 | 版本 | 授權 | 狀態 |
|---|---|---|---|
| yt-dlp | 2026.10.26（box `~/.local/bin`）| Unlicense（pip metadata `License-Expression`）| 已安裝；§13 建議的 `yt-dlp-ejs` 與 Deno 未安裝 → 完整 YouTube 支援未就緒 |
| pytubefix | 11.2.2（PyPI 最新）| MIT | 未安裝（YT0 未解除，不需要）|
| FFmpeg/ffprobe | 7.1.5-0+deb13u1（Debian）| 此 build 含 `--enable-gpl` → GPL；僅依 HF-Q01 Studio 外部工具例外使用 | 已安裝。註：t37u 提到的 FFmpeg 8.1.2 在 Mac，不在 box |
| Whisper | — | MIT（程式碼）；權重與依賴未審 | 沒有已准入版本 → NOT_RUN |
| Cobalt / LibreGet | — | AGPL-3.0 / GPL-3.0 | 依 t37u 與 permissive 政策排除 |

## 獨立 verifier

`studio/source/yt_gates.py` 是和取得步驟分開的驗收工具：用 ffprobe 與完整 ffmpeg decode 判 YT1/YT2、解析 SRT 判 YT3（編號、時間序、時長容差 2s、原語言與 provenance、取樣對齊紀錄）、重新計算 SHA-256 判 YT4。它不信任檔名、exit code 或 metadata。測試（`studio/tests/test_yt_gates.py`）用 lavfi 合成的測試片做正對照，另有缺音軌、SRT 亂序、hash 被改等負對照；合成片不是 S1，不構成 S1 的任何證據。

Drive：本輪沒有媒體位元組，所以沒有上傳 Drive，也沒有新分享。
