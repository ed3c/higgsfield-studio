# QC 評分卡

## A. 創意（六項等權，1–10）

項目名稱與定義沿用 Higgsfield Talent Contest 官方規則 9.4（https://higgsfield.ai/contests/talent-contest?tab=rules ）。通過線是我們自訂的：平均 ≥ 8，且每項 ≥ 7。

| 鍵 | 項目 | 看什麼 |
| --- | --- | --- |
| `directing` | Directing and Storytelling | 敘事清楚、情緒衝擊、電影觀點 |
| `visual` | Visual Quality | 構圖、攝影、跨鏡畫面一致 |
| `art_direction` | Art Direction | 世界觀、美術設計、視覺風格 |
| `sound` | Sound | 音效、音樂、人聲 |
| `editing` | Editing | 節奏、韻律、結構 |
| `originality` | Originality and Concept | 創意企圖、新意、善用媒材 |

```bash
python3 qc/creative_score.py qc-report.json
```

評分人先各自打分再對分數，不要先看別人的分數。AI 評分只當第二意見，導演保留最後決定。

## B. 機械檢查（pass/fail，不能用創意分數抵銷）

| 檢查 | 自動 | 規則 |
| --- | --- | --- |
| 黑幀 | `mech_check.py` | 片頭片尾 0.5 秒以外不得有 ≥ 0.1 秒的黑畫面 |
| 音訊削波 | `mech_check.py` | 峰值 < -0.1 dBFS |
| 解析度、比例 | `mech_check.py` | 符合 `delivery/profiles.json` |
| 編碼、像素格式、幀率、取樣率 | `mech_check.py` | 同上 |
| 片長 | `mech_check.py` | 在平台範圍內 |
| 亮度閃爍 | `mech_check.py`（警告） | 相鄰幀平均亮度跳動 > 40 的幀數；剪接點會誤報，人工確認 |
| 字幕安全區 | 人工 | 字只放在 `safe_area_px` 以內 |
| 人物身份漂移 | 人工 | 對照 `character-bible.md` 鎖定圖逐鏡看 |
| 肢體異常 | 人工 | 手指、關節、穿模 |
| 權利與來源 | 人工 | 每鏡 generation id 對得到 `takes.csv`；無真實品牌、真人肖像 |
