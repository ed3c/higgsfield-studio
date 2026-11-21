# 缺口分析：現有倉庫 vs 八階段流程（2026-11-22）

比較基準：`main` 與 `image-prompt-test` 兩個分支。新東西都在 `industrial-pipeline` 分支，沒有合併進 `main`。

| 流程需要 | 原本有 | 缺口 | 本分支補上 |
| --- | --- | --- | --- |
| 官方 Agent 入口 | `skills/vendor/higgsfield-ai-skills` v0.14.0（MIT 快照） | 無 | 不動 |
| 提示詞 | `prompts/` 依領域與鏡位；`tests/image-prompt-test/` 的 T01–T12、S01–S14 | 沒有「整部片共用」的風格前綴 | 在預告片 `style-bible.md` 寫固定前綴（PURGA 對峙＋bleach bypass） |
| 點數帳 | `budget/track.py`、`ledger.csv`、`cost-table.csv`、`allocation.csv` | 只會月底加總，不會在生成前擋 | `pipeline/scheduler.py`：生成前檢查專案預算與當月 9,000 上限，付費 take 同步寫進 `ledger.csv` |
| 專案模板 | `projects/_template/`（短影用） | 沒有八階段的檔案 | `projects/_film-template/` |
| 01 逆向工程 | `skills/methodology-breakdown/`、`research/` | 沒有拆解報告格式 | `schemas/reference-report.md`、`style-bible.md` |
| 02 Story Bible | 無 | 全缺 | `schemas/story-bible.md`，Script Lock 門 |
| 03 Character/Location/Prop Bible | 無 | 全缺 | `schemas/character-bible.md`、`location-bible.md`、`prop-bible.md` |
| 04 Shot IR 與 Animatic Gate | `templates/` 有短影分鏡 | 沒有機器可讀的鏡頭規格，沒有預演門 | `schemas/shot-ir.schema.json`；`gate 04` 檢查關鍵幀與鏡長 ±1 秒 |
| 05 Take Registry | `generations.csv`（只有點數） | 沒有 take 狀態、generation id、QC 結果 | `schemas/take-registry.csv`；Draft→Select→Render→Repair→Promote |
| 06 後製 | `templates/` 字幕與平台輸出 | 沒有 Picture/Sound Lock | `pipeline/06-post-production.md`，`post-lock.md` 門 |
| 07 QC | `tests/image-prompt-test/rubric.md`（靜幀五維） | 沒有影片評分與機械檢查 | `qc/rubric.md`、`qc/creative_score.py`（六維平均 ≥ 8、每項 ≥ 7）、`qc/mech_check.py`（黑幀、削波、解析度、比例、編碼、幀率、片長、閃爍警告） |
| 08 交付 | `templates/` 平台輸出說明 | 沒有可檢查的規格 | `delivery/profiles.json`、`delivery/specs.md`（TikTok、IG Reels、X、YouTube Shorts、YouTube 4K、比賽） |
| 測試 | `budget/test_track.py` | 無 | `pipeline/test_scheduler.py`（14 個）、`qc/test_qc.py`（7 個，用 ffmpeg 合成的小片段） |

## 仍然沒做的
- 人物身份漂移與肢體異常的自動偵測：目前是人工檢查表。要自動化需要臉部比對模型，先不加依賴。
- CLI 串接 Cinema Studio 4.0：官方 skills 能呼叫模型，但每次都扣點，且 Director's Panel 的每個控制項是否可程式化還沒驗證。主鏡頭先在網站手動做，再用 `scheduler.py take` 登記。
- 響度（LUFS）量測：交給 Resolve。
