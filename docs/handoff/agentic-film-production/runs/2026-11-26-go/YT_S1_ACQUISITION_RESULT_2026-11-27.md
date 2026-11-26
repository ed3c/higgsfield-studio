# S1 YouTube 取得結果（§13）— 2026-11-27

接續 `YT_S1_ACQUISITION_2026-11-26.md`（保留原 BLOCKED 紀錄，不覆寫）。

## 結論

**YT0–YT4 全部 PASS（`studio/source/yt_gates.py` 獨立判定，exit 0）。H01 取得完成；H02 完整逆向仍是另外的義務，NOT_RUN。**

## Gate 表

| Gate | 狀態 | 證據 |
|---|---|---|
| YT0 Source | PASS（範圍：私下分析） | `s1_rights_2026-11-27.json`：Neon 決定原文「軟體可以下載就下載」（經 parent session 轉述），接受權利風險；只限 download + private_analysis，排除再散布／發布／轉交／商用。**這不是 ICC 授權。** |
| YT1 Video | PASS | MKV：AV1 3840×2160 @29.97 + Opus 48 kHz 2ch，2333.388 s，與 info.json 2333 s 相符；ID 相符；完整 decode 0 錯誤，69,931 幀 = 2333.388×30000/1001（`s1_full_decode_summary_2026-11-27.txt`）|
| YT2 Audio | PASS | WAV pcm_s24le 48 kHz 2ch，2333.373 s；與 master 音軌差 −0.0147 s（容差 0.10 s，Opus 解碼前置／尾端差）|
| YT3 SRT | PASS（ASR，自動檢查） | `onNBysMf9WM.ja.srt`：UTF-8，300 cues，編號連續，時間遞增，最後一句結束 2268.24 s（< 媒體長度）。來源：沒有官方字幕，也沒有 YouTube 自動字幕 → Whisper large-v3（ja）。取樣對齊 8/8 通過（平均 0.931，位移 15 s 負對照 0.160）。這是自動檢查，不是人工聽打 |
| YT4 Evidence | PASS | `SHA256SUMS` 23 檔重算一致；QA_REPORT、media-probe、rights、tool_versions 齊備 |

## 檔案 SHA-256（私有，不進 Git）

| 檔案 | bytes | sha256 |
|---|---:|---|
| onNBysMf9WM.mkv | 937,391,090 | `7309020bcd547d4527f3fd9a36c585ac36fdb605b107b7b2242315b65b1ef45c` |
| onNBysMf9WM.audio.wav | 672,011,598 | `df7d39d676c5875c4b0e2b033ec2e58b96c91799a708791f84b719b2557b86aa` |
| onNBysMf9WM.ja.srt（過濾後）| 28,820 | `228d5a51faf7eb4f973c4abe466647c8696ce30c8d464c26468510cd738bb2bb` |
| onNBysMf9WM.ja.raw-asr.srt（Whisper 原始）| 30,670 | `2bc7b17dab59cdb678853aa44ed19a6b4787d31be2f1cca3caacc62efa3c8665` |
| Whisper large-v3 weights | 3,087,371,615 | `e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb`（與官方 URL 內嵌 hash 一致）|

完整清單：`s1_SHA256SUMS_2026-11-27.txt`。

## ASR 處理說明

- Whisper large-v3 在音樂／安靜段落產生典型幻覺（「ご視聴ありがとうございました」「おやすみなさい」「アーメン」「作詞・作曲・編曲 初音ミク」等），而且最後一句結束時間 2352.1 s 超過媒體長度。
- 依事先固定的規則（`studio/source/asr_postfilter.py`：R1 長度 ≥20 s 且 no_speech_prob ≥0.6；R2 已知幻覺句且 no_speech_prob ≥0.6；R3 no_speech_prob ≥0.85 且 avg_logprob ≤ −0.5）刪 26 段、保留 300 段，並把結束時間截到媒體長度。逐段刪除紀錄在 `s1_asr_postfilter_log_2026-11-27.json`。原始 Whisper 輸出原封保留。
- 已知副作用：R1 也刪了 1496.9 s 的「作品空間ですね」（27 s 視窗），可能是真的語句。
- 字幕內容仍有辨識錯誤（ASR 正常限制）。正式逆向前若需要逐字正確，需人工校對。

## 工具與授權

yt-dlp 2026.11.23（Unlicense）＋ yt-dlp-ejs 0.8.0（Unlicense AND MIT AND ISC）＋ Deno 2.9.8（MIT）；pytubefix 沒用到；FFmpeg 7.1.5 Debian GPL build（HF-Q01 外部工具例外）；openai-whisper 20250625（MIT，程式與權重）＋ torch 2.15.0+cpu。細節：`s1_tool_versions_2026-11-27.json`。

## Drive（私有、未分享）

資料夾：https://drive.google.com/drive/folders/1dk5YtJ0LDUVx4Hn-lvVo9rYu2KRV3WOJ （權限只有 owner；檔案 `shared:false`）

上傳工具單檔上限 100 MB，所以 MKV（10 片）與 WAV（7 片）以 `split -b 95M` 原樣切片上傳，沒有重新編碼。還原：`cat onNBysMf9WM.mkv.part* > onNBysMf9WM.mkv`，再對照 `SHA256SUMS`。各片 hash 在 `PARTS_SHA256SUMS`；本機已驗證 `cat` 合併後 sha256 與原檔一致。Drive 讀回：22 個檔名與 bytes 全部和本機一致（`s1_drive_readback_2026-11-27.json`）；Drive API 沒有回 md5，所以沒有做 Drive 端內容 hash 讀回。
