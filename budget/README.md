# 點數帳

Ultra 方案每月以 9,000 點計畫。分配與單價來自 [計畫](../plan/monthly-usage-and-content-strategy.md)（帳戶估價查詢日：台北時間 2026-11-21）。訂閱點數不會結轉。生成鍵上的數字若與本表不同，以生成鍵記帳。

## 檔案

| 檔案 | 作用 |
| --- | --- |
| `allocation.csv` | 五個桶。合計 9,000 |
| `ledger.csv` | 實際花費。一列一次生成 |
| `cost-table.csv` | 從計畫的三張單價表轉出 |
| `track.py` | 把當月花費加總，與分配比較，達到 80% 就警告 |
| `export_cost_table.py` | 計畫改價之後，重產 `cost-table.csv` |

## 怎麼記

每做完一次生成，在專案的 `generations.csv` 留副本，並把同一列追加到 `ledger.csv`。

```csv
date,bucket,model,settings,aspect_ratio,credits,project,outcome,refunded,prompt_id,note
2026-11-24,trends,Wan 3.0,5s 720p,9:16,7.5,2026-11-24-night-market,final,no,fashion-trend-cut,生成鍵與估價一致
```

- `date` 用 `YYYY-MM-DD`。追蹤器用台北時間的當月，也可用 `--month 2026-11`。
- `bucket` 只能是 `methodology`、`daily-life`、`trends`、`retry`、`rnd`。
- `refunded` 為 `yes` 時不計入花費。失敗任務若平台已退點，仍保留這一列。
- `outcome` 用 `draft`、`final`、`upscale`、`rejected`。

## 怎麼看

```bash
python3 budget/export_cost_table.py
python3 budget/track.py
python3 budget/track.py --month 2026-11
python3 budget/test_track.py
```

`track.py` 在任一桶或當月合計達到該分配額的 80% 時，於標準錯誤印出警告，並以結束碼 2 離開。未達警戒線時結束碼為 0。分配表加總不是 9,000 時結束碼為 1。

80% 是停用貴模型的線，不是月底目標。計畫的使用率目標仍是花掉 85–95%，把剩餘留給突發趨勢。警戒只表示這個桶不該再加定稿。
