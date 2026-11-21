# 05 鏡頭製作

## 工具分工（依官方文件查核）
| 工具 | 用在 | 已查證的限制 |
| --- | --- | --- |
| Cinema Studio 4.0 | 主鏡頭 | 單次最長 30 秒；最多 50 個參考；網站最高 1080p，API 480p/720p；Director's Panel、Emotion Wheel、Extend、Edit Video |
| Soul ID / AI Cast / Elements | 角色與物件一致 | Soul ID 訓練一次性約 25 點 |
| Genjutsu / Genjutsu Lite | 動作遷移、局部替換 | 參考影片 4–30 秒；網站最多 30 張參考圖（API 1–8 張） |
| Canvas | 多模型對照 | 一律扣點，Unlimited 不適用 |
| Kling 4.0 等 | 便宜的插入鏡 | 依生成鍵 |

## 每個 take 必記
`takes.csv` 欄位見 [../schemas/take-registry.csv](../schemas/take-registry.csv)：shot_id、phase、surface、model、settings、prompt_version、refs、generation_id、credits、qc、qc_reason。

## 門檻：逐鏡 Acceptance
每鏡至少一個 take 通過 QC 並 promote。`gate 05` 會檢查每一鏡都有 promoted take。
