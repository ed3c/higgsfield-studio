# 工業級 AI 電影製作流程

依據 Neon 2026-11-22 的需求（原文：[../plan/neon-industrial-pipeline-brief.md](../plan/neon-industrial-pipeline-brief.md)）與事實查核（[../plan/fact-check-2026-11-22.md](../plan/fact-check-2026-11-22.md)）。方法是 PURGA 的角色先行：先鎖角色與視覺方向，再在同一套系統裡長出世界與鏡頭。

原則只有一條：在 Animatic 通過之前，不做任何付費影片。

## 流程圖

```text
01 逆向工程 ─► 02 故事 ─► 03 視覺開發 ─► 04 預演 ══► 05 鏡頭製作 ─► 06 後製 ─► 07 QC ─► 08 交付
  免費          免費        免費（網站          免費       付費（Draft→Select    免費        免費      免費
                            Unlimited 靜幀）     ▲          →Render→Repair       (Resolve)
                                                 │          →Promote）
                                         Animatic Gate：
                                         過了才准 render
```

`══►` 是唯一會開始扣點的門。`pipeline/scheduler.py` 在程式裡擋住這道門。

## 八個階段與門檻

| # | 階段 | 交付物（放在專案資料夾） | 門檻（誰簽、看什麼） | 點數 |
| --- | --- | --- | --- | --- |
| 01 | [逆向工程](01-reverse-engineering.md) | `reference-report.md`、`style-bible.md` | 每個借來的技法都有來源連結；不抄角色、片段、品牌 | 0 |
| 02 | [故事開發](02-story-development.md) | `story-bible.md` | Script Lock：不靠特效也成立；三幕時間分配寫死 | 0 |
| 03 | [視覺開發](03-visual-development.md) | `character-bible.md`、`location-bible.md`、`prop-bible.md` | 每個角色有正、側、全身三張鎖定圖；導演確認 | 0（網站 Unlimited）；Soul ID 訓練另計 |
| 04 | [預演](04-previsualization.md) | `shots.json`、`animatic.md` | Timing Lock：每鏡有關鍵幀；鏡長加總等於目標片長 ±1 秒；導演看完整 Animatic | 0 |
| 05 | [鏡頭製作](05-shot-production.md) | `takes.csv` | 每鏡一個 promoted take；每次付費生成都有 generation id 與點數 | 主要支出 |
| 06 | [後製](06-post-production.md) | `post-lock.md` | Picture Lock 與 Sound Lock | 0 |
| 07 | [技術與創意 QC](07-qc.md) | `qc-report.json` | 六維平均 ≥ 8 且每項 ≥ 7；機械檢查全部 pass | 0 |
| 08 | [交付](08-delivery.md) | `delivery.md` | 各平台檔通過 `qc/mech_check.py`；來源紀錄完整 | 0 |

## 鏡頭的五種狀態

`Draft → Select → Render → Repair → Promote`。

- Draft：網站 Unlimited 靜幀，或單價 ≤ 5 點的試看。階段 02 通過後才可用。
- Select：導演從 draft 中挑一個。沒有 selected draft 的鏡頭不能 render。
- Render：只對 selected 的鏡頭做高品質生成。階段 04 通過、且專案預算與當月 9,000 上限都還夠，才放行。
- Repair：只修 QC 判 fail 的 take，優先局部修（Cinema Studio 4.0 Edit Video、Genjutsu Objects swap），不整段重做。
- Promote：QC pass 的 take 才能進最終時間軸。每鏡只留一個。

## 指令

```bash
python3 pipeline/scheduler.py plan projects/2026-11-proof-trailer      # 估點
python3 pipeline/scheduler.py status projects/2026-11-proof-trailer
python3 pipeline/scheduler.py gate projects/<slug> 02 --by Neon        # 簽門
python3 pipeline/scheduler.py take projects/<slug> --shot S01 --phase draft --surface web-unlimited --model "Nano Banana Pro" --credits 0
python3 pipeline/scheduler.py select projects/<slug> T0001
python3 pipeline/scheduler.py take projects/<slug> --shot S01 --phase render --surface web --model "Cinema Studio 4.0" --settings "5 秒，720p" --credits 35 --generation-id <id> --bucket methodology
python3 pipeline/scheduler.py qc projects/<slug> T0002 --result fail --reason "手指多一隻"
python3 pipeline/scheduler.py promote projects/<slug> T0003
python3 -m unittest discover -s pipeline -p 'test_*.py'
```

付費的 take 會同時寫進該專案的 `takes.csv` 與 `budget/ledger.csv`，`budget/track.py` 照舊能加總。

## 已知限制

- 點數單價取自 `budget/cost-table.csv` 的 2026-11-21 帳戶估價。送出前以生成鍵為準；不一致時記實際值。
- MCP、CLI、Canvas、Supercomputer 的生成一律扣點，網站 Unlimited 不適用（官方說明 https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work ）。排程器拒絕在這些入口登記 0 點的 take。
- 官方 CLI 與 skills 能呼叫 `cinematic_studio_video_4_0`，但 Director's Panel 的全部控制、共享專案與時間軸能否程式化，還沒逐項驗證。主鏡頭先在網站 Cinema Studio 手動做。
