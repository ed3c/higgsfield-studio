# Higgsfield 製作環境

台灣創作者的個人 Higgsfield 產製庫。方案是 Ultra，每月按 9,000 點計畫。成品是 IG Reels、TikTok 與 X 的短影和靜幀。

內容有三條：把日常生活重拍、接上這三個平台的趨勢，以及一套鏡前的方法論系列。方法論拆藝術、時裝、電影、文學、科技與科幻裡可模仿的做法。

文件用繁體中文。模型名、畫幅、技能名與欄位名保持英文。

## 目錄

| 路徑 | 內容 |
| --- | --- |
| `plan/` | 每月 9,000 點怎麼分，以及 2026-11-21 的帳戶估價 |
| `budget/` | 點數帳。`track.py` 依桶加總，達到分配額 80% 就警告 |
| `skills/` | 四個自有製作技能，加上官方 [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) v0.14.0 的 MIT 快照 |
| `prompts/` | 依領域與鏡位／運鏡整理的原創提示詞。預設 9:16 |
| `creators/` | 由 `research/creators.json` 產生的領域索引與十人學習隊列 |
| `research/` | 79 位創作者與公開提示庫的原始研究，保留不動 |
| `templates/` | 分鏡、口播、字幕、平台輸出、每週趨勢偵察 |
| `projects/_template/` | 一支片的資料夾。複製後再開始 |

## 快速開始

1. 讀 [plan/monthly-usage-and-content-strategy.md](plan/monthly-usage-and-content-strategy.md)。預算以該文件的帳戶估價為計畫值，送出前以生成鍵為準。
2. 看 [creators/study-queue.md](creators/study-queue.md)。研究流程，不複製成片。
3. 複製一支片的資料夾：

   ```bash
   cp -a projects/_template projects/YYYY-MM-DD-slug
   ```

4. 從 [prompts/README.md](prompts/README.md) 選一條模板，改 `{占位符}`，把 id 寫進該專案的 `prompts-used.md`。
5. 製作順序用 [skills/draft-to-final-upscale/SKILL.md](skills/draft-to-final-upscale/SKILL.md)。日常、趨勢、方法論各有一份技能。
6. 每次生成都追加到專案的 `generations.csv` 和 `budget/ledger.csv`，然後：

   ```bash
   python3 budget/track.py
   ```

結束碼 2 表示某個桶或當月合計已達 80%。這時停止新增定稿。

官方技能若要更新，照 [skills/UPSTREAM.md](skills/UPSTREAM.md)。不要把 API key 或 `credentials.json` 放進這個倉庫。

## 點數

| 桶 | 點數 | 佔比 |
| --- | ---: | ---: |
| 方法論系列 `methodology` | 2,520 | 28% |
| 日常再創作 `daily-life` | 2,250 | 25% |
| 趨勢二創 `trends` | 1,980 | 22% |
| 重試預備 `retry` | 1,620 | 18% |
| 實驗研發 `rnd` | 630 | 7% |

重試預備只補已經做完但不夠好的定稿，不用來開新題。網站上的 Unlimited 與免費次數不會跟著 MCP、CLI 或 Canvas 走，那些路徑都會扣點。

## 畫面不進 git

生成的影片、聲音，以及 `projects/*/refs/`、`renders/`、`exports/` 裡的檔案都不要提交。帳本只留 CSV 與 Markdown。

若一定要版本管理少數母帶或靜幀，用 Git LFS，或放在倉庫以外的硬碟或雲端。不要把 4K 原檔或失敗的取次放進 LFS。

```bash
git lfs install
git lfs track "projects/*/masters/*.mp4" "projects/*/stills/*.png"
```

`.gitignore` 已排除常見的影片與音訊副檔名。LFS 規則要另外寫進 `.gitattributes`，本庫預設不追蹤這些檔。

## 授權

`skills/vendor/higgsfield-ai-skills/` 是 Higgsfield AI 的官方技能庫快照，MIT，Copyright (c) 2026 Higgsfield AI，commit `27000402070db19d958789d05b3b52b6f4718d7c`。許可全文在該目錄的 `LICENSE`。

[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) 只當參考。上游寫明 2026 年 11 月起不再維護。本庫沒有收錄它的提示詞。

## Creator Image-Reverse Benchmark v2.0

- [執行規格與驗證腳本](research/reverse-skill-benchmark/v2/README.md)：研究 @tupacabra 視覺語法，使用 3 參考案例、3 逆向 Skills；P1 18 張忠實重建，P2 12 張風格遷移。
- [執行入口 Skill](skills/image-reverse-benchmark/SKILL.md)；[ScrapeCreators 情報入口](skills/social-creator-intelligence/SKILL.md)。
- **目前：BLOCKED_ENTITLEMENT_RECHECK / NOT_RUN。** 2026-11-20 的網站 Subscription 截圖不代表 2026-11-23 仍有效；網站 UI 必須再確認 Unlimited ON 及 0 Credits 才能生成。API/MCP 免費資格不等於網站權益。
- v1 原始紀錄保留在 [research/reverse-skill-benchmark/](research/reverse-skill-benchmark/)；不覆寫、不偽造測試成績，圖片素材不進 Git。

## 全創作者研究與 dot 交接

- [創作者與作品完整研究範圍](research/reverse-skill-benchmark/v2/CREATIVE_RESEARCH_SCOPE.md)：整合本對話提及的作品、既有 79 位創作者研究資料、跨領域 Managers、來源追溯與雙 Gate 驗收。
- [dot 可直接貼上的交接指令](research/reverse-skill-benchmark/v2/DOT_HANDOFF.md)：先讀完整 Scope 與 Benchmark v2，再進行網站 Unlimited 零 Credits 驗證。**此檔案不代表已將任務實際發送給 dot。**
