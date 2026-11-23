# Skills

給代理與本人共用的製作技能。文件用繁體中文，模型名、畫幅、技能名保持英文。

## 自己的製作技能

| 技能 | 何時用 | 點數桶 |
| --- | --- | --- |
| [daily-life-remix](daily-life-remix/SKILL.md) | 把當天的生活素材重拍成短影或靜幀 | 日常再創作 |
| [trend-jacking](trend-jacking/SKILL.md) | 24–48 小時內接上 IG、TikTok、X 的趨勢 | 趨勢二創 |
| [methodology-breakdown](methodology-breakdown/SKILL.md) | 鏡前拆解一套工業級做法 | 方法論系列 |
| [draft-to-final-upscale](draft-to-final-upscale/SKILL.md) | 任何支柱的草稿、定稿、放大與記帳 | 依該支片的桶，重試走重試預備 |
| [social-creator-intelligence](social-creator-intelligence/SKILL.md) | 使用 ScrapeCreators 研究 @tupacabra / 創作者爆款、留言與作品線索 | 外部資料 API，須先核價 |
| [image-reverse-benchmark](image-reverse-benchmark/SKILL.md) | 使用相同參考劇照比較圖片逆向 Skills，免費圖片不存在就 NOT_RUN | 只允許已驗證 0-credit 的免費生成 |

送出任何生成之前先跑 `python3 budget/track.py`。任一桶或當月合計達到分配額的 80% 就停用貴模型。

圖片逆向 Benchmark v2 改用 **Higgsfield 網站 UI** 的零 Credits Unlimited 權益作為唯一可執行入口；網站權益仍需重新核對（`BLOCKED_ENTITLEMENT_RECHECK`）。API/MCP 不具同一免費資格。請以 [v2 規格](../research/reverse-skill-benchmark/v2/README.md) 為準；[v1 記錄](../research/reverse-skill-benchmark/README.md) 保留作歷史證據。

## 官方技能（vendored）

快照、授權與更新方式見 [UPSTREAM.md](UPSTREAM.md)。正文在 [vendor/higgsfield-ai-skills](vendor/higgsfield-ai-skills)。

| 技能 | 用途 |
| --- | --- |
| `higgsfield-generate` | 圖像、影片、3D、音訊、Marketing Studio、Virality Predictor |
| `higgsfield-soul-id` | 訓練可重用的 Soul Character，取得 `reference_id` |
| `higgsfield-product-photoshoot` | 產品靜幀。後端組提示詞，不要手寫最終 prompt |
| `higgsfield-brandkit` | 視覺識別系統 |
| `higgsfield-marketplace-cards` | 市集商品卡 |
| `higgsfield-websites` | 網站、app、遊戲 |
| `higgsfield-faceless-video` | 無出鏡解說 |
| `higgsfield-video-explainer` | 舊名稱入口，轉到 faceless-video |
| `higgsfield-youtube-thumbnail` | 封面。直式封面可借給 Reels / TikTok 封面構圖，但本頻道主輸出仍是 9:16 影片 |

官方 [COOKBOOK.md](vendor/higgsfield-ai-skills/COOKBOOK.md) 有兩條食譜：創辦人照片訓練 Soul 再做生活照與短片；從產品 URL 批次做 UGC。食譜裡的預設模型比本庫的趨勢桶貴。本庫趨勢與日常草稿改走 `plan/` 的便宜模型，方法論定稿才用 Cinema Studio 4.0 或 Seedance 2.5。

## 外部研究 Skills（不複製原始碼）

```bash
npx skills add ScrapeCreators/social-media-research-skills
# 外部 API，於自己的密鑰管理工具設置 SCRAPECREATORS_API_KEY
```

只在研究時啟用，先核對上游 SKILL.md、MIT 授權、API 定價與授權。上游不受本庫預算帳本管理；使用前須另行計入外部 API 費用。逆向候選不預先安裝為自動執行；詳見 [UPSTREAM.md](UPSTREAM.md) 和上述 Benchmark。

## 不要做的事

- 不要把 OSideMedia 的提示詞貼進專案。該庫已停止維護，見 [UPSTREAM.md](UPSTREAM.md)。
- 不要在 MCP、CLI、Canvas 上消耗只在 [higgsfield.ai](https://higgsfield.ai) 網站生效的 Unlimited 或免費次數。那些路徑都會扣點。
- 不要把密鑰寫進技能或提交到 git。
