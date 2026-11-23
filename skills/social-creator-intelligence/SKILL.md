---
name: social-creator-intelligence
description: |
  以公開社群數據尋找創作者的異常高表現作品、留言需求、敘事與影像研究候選。
  Use when: creator research, outliers, comment mining, competitor, @tupacabra, TikTok, Instagram, YouTube, X, Reddit, LinkedIn.
  NOT for: 逆推圖片 Prompt、宣稱已抓取未實際取得的數據、未授權下載/轉發影片、直接送出付費生成。
---

# Social Creator Intelligence

Owner: Research Manager。Consumer: image-reverse-benchmark、trend-jacking、methodology-breakdown。Oracle: 來源 URL + 擷取時間 + 可核對的原始指標。

## 外部依賴

上游 [ScrapeCreators/social-media-research-skills](https://github.com/ScrapeCreators/social-media-research-skills)，MIT。透過 `npx skills add ScrapeCreators/social-media-research-skills` **安裝到執行 Agent 的環境**，並設置 `SCRAPECREATORS_API_KEY`（機密不得進 Git）。API 是外部有計費/限額的服務；本庫不 vendoring、不自動呼叫 API。安裝前審核 SKILL.md 與實際工具權限，將上游 commit 釘選在執行紀錄。

依序調用上游的 `creator-profile-teardown`、`outlier-post-finder`、`comment-mining`、`transcript-intelligence`；研究競品時再用 `competitor-social-research`、`ad-library-teardown`。原始 endpoint 的參數先核對當下 OpenAPI，勿假定 README 路徑永遠不變。

## 工作流程

1. 輸入帳號連結及平台，例如 https://x.com/tupacabra 。只處理公開資料。確認 URL/Handle 對應正確創作者。
2. 對每一個「帳號 × 平台 × 內容格式 × 時間窗」取至少 20 則（若可得）；記錄貼文 URL、發佈時間、擷取時間、views/likes/comments/reposts 等**原始欄位**及缺值。
3. 以各分組中位數建立 baseline。能得 views 時用 `views/median_views`；否則明確標識替代指標。不能把 X 與 TikTok 的指標相加比較。樣本 <10 標記 LOW_CONFIDENCE，median=0 不算 lift。
4. 優先研究 >2x 的異常表現；只把它當作「值得研究」的線索，**不是爆紅因果證明**。保留沒有被選中的樣本數和抽樣偏差。
5. 對候選抓取可存取的 transcript 與留言，區分 hook、評論裡的提問/抱怨、來源可核對的工具線索及主觀推測。
6. 產出研究記錄，並將少數有權研究的參考圖片/影片 URL 移交給 `image-reverse-benchmark`。不下載完整受保護影片作為可再散布資產；需要本地證據幀時先檢查合法使用範圍。
7. 供 `trend-jacking` / `methodology-breakdown` 消費時，只移交原創可運用的概念、節奏和構圖規則。保留「不可借用」欄位。

## 輸出契約

請寫在新研究路徑（例：`research/live/creator-intelligence/YYYY-MM-DD-tupacabra/`），不要覆寫 `research/creators.json` 等歷史來源。每次研究至少包含：

- `sources.json`: 每個 post 的平台、原始 URL、擷取時間、格式、指標、資料來源、missing fields。
- `outliers.csv`: account/platform/format/window/sample_n/median/metric/lift/confidence/URL。
- `audience.md`: 被檢索到的留言主題、樣本數、去重策略、實際可核對的來源（引述保留上下文）。
- `visual_candidates.json`: screenshot/video URL、創作者與授權狀態、選用理由、待驗證的視覺假說、移交狀態。
- `NOT_RUN.md`: 當 API key、授權、配額或資料不足時，寫出阻擋條件，不生成空想指標。

## Fail-closed

API 失效、無 API key、登入失敗、平台限流、版權不明或資料不足時停止對應路徑；不可杜撰數字或改用網路搜尋結果冒充完整帳號樣本。此 Skill **不呼叫 Higgsfield 生成**，且不得消耗 Higgsfield Credits。
