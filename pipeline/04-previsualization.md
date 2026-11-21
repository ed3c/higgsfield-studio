# 04 預演（Animatic Gate）

這是從「生成影片」轉成「製作電影」的分界線。

## 產出
- `shots.json`：每鏡一筆 Shot IR（格式見 [../schemas/shot-ir.schema.json](../schemas/shot-ir.schema.json)），含秒數、景別、構圖、工具、估點、關鍵幀檔名。
- `animatic.md`：Animatic 檔案位置（放 `renders/`，不進 git）、臨時音樂與旁白來源、導演意見。

## 做法
1. 每鏡用網站 Unlimited 生一張關鍵幀（免費）。
2. 在 DaVinci Resolve 免費版把關鍵幀照 `shots.json` 秒數排好，加臨時音效與旁白，做 Ken Burns 推拉。
3. 從頭看到尾，記下節奏、動機、鏡序問題，改到順。

## 門檻：Timing Lock
`scheduler.py gate <專案> 04` 會檢查：
- `animatic.md` 存在；
- 每鏡都有 `keyframe`；
- 鏡長加總等於 `project.json` 的 `target_seconds`，誤差 ±1 秒。
通過前，任何 `--phase render` 都會被拒絕。
