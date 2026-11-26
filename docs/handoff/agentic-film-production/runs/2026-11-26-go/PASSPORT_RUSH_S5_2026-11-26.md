# Passport Rush Full Project（§14）— 非瀏覽器部分，2026-11-26

URL：https://higgsfield.ai/@higgsfield.studio/projects/passport-rush （S5，H03/H04）

## 結論

**H03 PARTIAL：只取得公開 publication record。Elements、Prompts、模型參數、Canvas、Storyboard、Blender Previs、Timeline 都需要 Desktop Browser session。** 沒有下載任何媒體位元組，沒有生成、沒有 credits、沒有 GPU。

## 沒有重走的失敗路徑

- Higgsfield MCP `list_projects(search="Passport Rush")` 已在 11/26 回 0 筆 → 本輪不重跑。
- Higgsfield cloud sandbox 缺 Playwright → 本輪不重試。

## 本輪新做的兩條路

### 1. Higgsfield MCP schema 檢查（唯讀，未呼叫寫入工具）

`get_project`、`get_project_publication`、`resolve_project_assets`、`list_project_assets`、`get_project_asset_prompt/source` 都要求 `workspace_id` + `project_id`（UUID），讀的是**自己可存取的 workspace**。目錄裡沒有讀取他人公開 Cinema publication 的方法。下方取得的 `publication_id` 是公開 publication 的 ID，不等於 workspace project_id，所以沒有拿它去猜呼叫（handoff：不猜 UUID、public visibility ≠ workspace membership）。

### 2. 公開 HTTP（匿名 curl，desktop UA）

- 頁面 200，`x-clerk-auth-status: signed-out`。原始 HTML sha256 `1137…`（見下表），只存 box 私有目錄。
- 頁面是 TanStack SSR（`ssr:"data-only"`），伺服器端只嵌入 publication record；資產、prompt、canvas 在瀏覽器端串流載入。
- 沒有呼叫任何內部 API endpoint（handoff：不使用 private endpoints 繞過權限）。
- 對成片 `originalSrc` 只做 HTTP HEAD（200、`video/mp4`、17,401,468 bytes、Last-Modified 2026-09-28 19:18:44 GMT），**沒有下載內容**（license 未定）。
- `/@higgsfield.studio/projects/passport-rush/full-film`（featuredEpisodeSlug）回 404。

## 公開 publication record（由 importer 解析）

| 欄位 | 值 |
|---|---|
| publication_id | `5faf8c98-ab7b-4195-bfb6-073a6e985785` |
| title / type | Passport Rush / film |
| created_at | 2026-09-25T13:27:41Z |
| author | higgsfield.studio（Higgsfield Team badge）|
| snapshot_folder_id | `cc812686-3e0a-4334-aa24-f50eba31f56d`（source/root folder = null）|
| showPrompts / showCanvas | true / true |
| license | **null** |
| 報告的計數 | Generations「14 608」、Credits spent「0」、Size「0 B」、Views「0」（平台顯示值，未獨立驗證）|
| 成片 | 1 支，`29e131bd-…`，287.541667 s，1920×1080，HLS + MP4 locator |
| assets（SSR 列出）| 1（就是成片）|

## Coverage（`passport_rush_inventory_2026-11-26.json`）

| 類型 | 狀態 | 原因 |
|---|---|---|
| project | OBTAINED | publication record 已解析 |
| video | PARTIAL | 成片 locator 與尺寸／時長已記；未取位元組。成片 MP4 不等於 full project export |
| assets | PARTIAL | SSR 只列 1 件；snapshot folder 內容在瀏覽器端 |
| prompts | BROWSER_REQUIRED | showPrompts=true，但 prompt 不在伺服器 HTML |
| model_params | BROWSER_REQUIRED | 同上 |
| canvas | BROWSER_REQUIRED | showCanvas=true，但 canvas 不在伺服器 HTML |
| elements / storyboard / previs / timeline | BROWSER_REQUIRED | 伺服器 HTML 沒有；可能在 canvas/snapshot folder |
| audio | UNKNOWN | 沒有獨立音訊項；成片音軌要有位元組才能驗 |
| rights | UNKNOWN | license=null；公開可見不等於可重用（§3）|

import_status = PARTIAL；acceptance = NOT_RUN（需要獨立 Oracle 對完整授權 inventory 核對）。

## Generic Full Project Importer

- 程式：`studio/importer/full_project_importer.py`（CLI：`python3 -m studio.importer.full_project_importer --html … [--export-dir …] [--supplemental-archive …] --out …`）
- Schema：`schemas/full-project-inventory.v1.schema.json`
- 不寫死 Passport Rush：Higgsfield adapter 讀任何公開 publication 頁的 `project` record；`LocalExportAdapter` 讀 Owner 提供或官方匯出的資料夾（需 `export_manifest.json`，每檔重算 SHA-256，回報缺檔、多出檔、期望數量差；宣稱 OFFICIAL 但沒有官方匯出證據時降為 OWNER_EXPORT）；`ThirdPartyArchiveAdapter` 只放進 `supplemental_items`，**永遠不計入官方 coverage**。
- 不執行 JavaScript：`seroval_lite.py` 只解析資料字面值，遇到函式或串流就回報缺口。
- 不連網：importer 只讀已存檔的證據；取得行為另外記錄。
- 測試：`studio/tests/test_full_project_importer.py`（真實 fixture、其他 slug 的合成頁、無法解析頁、第三方 archive 不計分、Owner export 缺檔／多檔／降級）。單元測試不是獨立驗收。

## 需要 Desktop Browser session 的項目（請另外安排）

在已登入或公開的 desktop 瀏覽器開 URL 後，依序讀取並保存（截圖 + 頁面可匯出的檔案 + 每項的 ID）：

1. 頁面可見的分區與分頁清單（Overview / Assets / Prompts / Canvas / Elements / Episodes 等實際標籤），以及各區總數。
2. Assets：snapshot folder `cc812686-…` 的完整清單（捲動到底／分頁到底），每項 ID、類型、標題、時長、尺寸；記錄排除與缺漏。
3. Prompts：每個 placement 的原始 prompt 位元組、模型、參數（aspect、duration、seed 若有、reference 設定），和對應的 asset ID。
4. Canvas：節點與連線（若能匯出就匯出原檔；否則截圖 + 可見節點清單）。
5. Elements：名稱、類型（character/location/prop…）、版本、使用處。
6. Storyboard（2D 手繪分鏡）與 Blender Previs（場景檔、灰盒影片）是否公開、能否下載。
7. Timeline／Editing Room：是否公開、revision、鏡頭順序與 in/out。
8. 音訊：配樂／音效／對白是否以獨立檔存在。
9. 頁面上的授權或使用條款文字（license 欄位目前是 null）與「Download / Export」實際可用的按鈕。
10. 失敗取次（failure takes）是否可見。

每一項都記 URL、時間（UTC+8）、截圖 hash；有下載就算 SHA-256 並放 Drive 私有資料夾，再交給 `LocalExportAdapter`。

## 公開 HTML 雜湊

| 檔案 | sha256 |
|---|---|
| 0928a76f.html | `1137454d3ef2d47ee504a5e845e12794f332acecb3de2470533f0a556cb7f5e4` |
| 43ce8802.html | `a957612b06c7aa348e0b8807a5dc8b10781814dabbee250ed4f8103894c05cce` |
| higgsfield_publication_passport_rush_2026-11-26.ssr.txt | `fe7a3aa8b15da6436f081d79510c7efe30fa661a967ff73f948f7cb03f3c8f2e` |
