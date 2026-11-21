# 電影專案模板（八階段）

```bash
cp -a projects/_film-template projects/YYYY-MM-slug
python3 pipeline/scheduler.py status projects/YYYY-MM-slug
```

先填 `project.json` 的 `budget_credits`（Neon 核准的數字）與 `target_seconds`。之後照 `pipeline/README.md` 一階一階簽門。短影（單支 Reels）仍可用 `projects/_template/`。

`animatic.md`、`post-lock.md`、`qc-report.json`、`delivery.md` 在對應階段才建立，模板不預放，避免空檔案讓門檻誤過。
