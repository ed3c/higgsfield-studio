# 專案模板

做一支片時，複製這個資料夾：

```bash
cp -a projects/_template projects/YYYY-MM-DD-slug
```

`YYYY-MM-DD` 用開拍當天（台北時間）。slug 用英文小寫與連字號。

| 路徑 | 內容 |
| --- | --- |
| `brief.md` | 這支片為什麼做、用哪個桶、不使用什麼 |
| `refs/` | 參考圖與實拍。git 忽略檔案本體，只保留 `.gitkeep` |
| `prompts-used.md` | 實際送出的提示詞與 `prompts/` 的 id |
| `generations.csv` | 每一次生成的點數。同一列追加到 `budget/ledger.csv` |
| `edit-notes.md` | 哪一鏡不過關、改了什麼 |
| `published.md` | 三平台連結與數據 |

成片放在 `exports/`，草稿成片放在 `renders/`。這兩個目錄不要提交。大檔用 Git LFS 或磁碟／雲端硬碟，說明在倉庫根目錄的 README。
