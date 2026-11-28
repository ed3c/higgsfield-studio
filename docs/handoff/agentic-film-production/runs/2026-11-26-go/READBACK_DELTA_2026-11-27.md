# 讀回差異（2026-11-27）— 追加，不覆寫 READBACK_2026-11-26.md

| ID | 原狀態（11-26） | 新狀態（11-27） | 依據 |
|---|---|---|---|
| H01 | BLOCKED（YT0 權利） | 取得完成：YT0–YT4 PASS（YT0 範圍＝Owner 接受風險、只限私下分析）| YT_S1_ACQUISITION_RESULT_2026-11-27.md |
| H02 | NOT_RUN | NOT_RUN（現在已有 S1 位元組，可開始）| — |
| H03 | PARTIAL / BLOCKED_BROWSER | 不變。Neon 選「metadata only, no download」；瀏覽器讀取由 parent 另外執行，本 session 不碰 | Neon 決定（parent 轉述）|
| H14 | BLOCKED（box 無 codex）| NOT_RUN — owner-executed on Neon's Mac（不在 box）| Neon 決定（parent 轉述）|
| H15 | BLOCKED（box 無 antigravity）| NOT_RUN — owner-executed on Neon's Mac | 同上 |
| H20 | BLOCKED（box 無 blender）| NOT_RUN — owner-executed on Neon's Mac | 同上 |
| H12 | NOT_RUN | NOT_RUN；新增已記錄授權：yt-dlp-ejs（Unlicense AND MIT AND ISC）、Deno（MIT）、openai-whisper 20250625 + large-v3 權重（MIT）| s1_tool_versions_2026-11-27.json |

Whisper 准入：openai-whisper large-v3（MIT），weights sha256 `e5b1a55b…dadb`。PASS 只限 H01 的取得範圍，Parent Goal 仍 OPEN。
