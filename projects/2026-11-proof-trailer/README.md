# 《過境 CROSSING》：免費靜幀 Animatic

Neon 2026-11-22 的決定：先只用免費靜幀做 animatic，不花任何點數。不用 Higgsfield MCP、CLI 或 Canvas。

| 檔案 | 內容 |
| --- | --- |
| `stills-plan.json` | 41 則提示詞的唯一來源（19 張鎖定圖、16 張關鍵幀、5 張結束幀、1 張選做片名版） |
| `lock-sheets.md` | 角色、場景、道具的鎖定圖提示詞 |
| `keyframe-prompts.md` | S01–S16 關鍵幀與結束幀提示詞 |
| `run-sheet.md`、`run-sheet.csv` | 瀏覽器操作員照表跑：順序、模型、畫幅、要上傳的參考圖、檔名 |
| `selects.csv` | 每鏡選中的關鍵幀與結束幀；`build_animatic.py` 和 `gate 04` 都讀它 |
| `stills/` | 下載的靜幀（不進 git） |
| `renders/animatic.mp4` | Animatic 輸出（不進 git） |

## 流程

1. 照 `run-sheet.md` 在 higgsfield.ai 網站跑，生成鍵顯示 UNLIMITED 才按。每則先 1 張，不合格才第 2 張。
2. 選圖，把檔名寫進 `selects.csv`。
3. 出 animatic：

   ```bash
   python3 pipeline/build_animatic.py projects/2026-11-proof-trailer             # 正式
   python3 pipeline/build_animatic.py projects/2026-11-proof-trailer --placeholder  # 缺圖用灰卡
   ```

4. 改提示詞時改 `stills-plan.json`，再重產文件：`python3 pipeline/render_stills_plan.py projects/2026-11-proof-trailer`（不會覆蓋 `selects.csv`）。
