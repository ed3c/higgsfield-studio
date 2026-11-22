# Handoff Audit — J4《ASYNC: SUCCESSION》+ Reusable Creative Production Factory

- 稽核日期：2026-11-22（Asia/Taipei, UTC+8），約 15:15–15:35
- 稽核者：Grok Bot（雲端 box，Linux；非 Neon 的 Mac）
- 依據契約：`docs/GROK_BOT_HANDOFF.md`（HOF-01…HOF-12）、`docs/GROK_BOT_SOURCE_MAP.csv`、`docs/LOCAL_REVIEW.md`、`projects/j4-async-succession/PROJECT.json`、`projects/j4-async-succession/archive/MEDIA_CUSTODY.md`、`studio_factory/README.md`、Draft PR #1 本文與留言
- 本文件為 **append-only 新檔**；未修改任何既有文件、提示詞、原始碼或歷史版本。
- 狀態只用 `PASS / FAIL / BLOCKED / NOT_RUN`。GitHub CI PASS ≠ 真實 Mac 影片播放 PASS ≠ 藝術品質 PASS。
- 本次 0 Higgsfield 點數；未呼叫任何 Higgsfield 生成；未發布影片；未擴大 Drive 分享；未合併 main；未 force-push。

## 0. 結論（READY_FOR_HUMAN_REVIEW / BLOCKED）

**BLOCKED**（交接層面）。雲端 box 上的資產與網站驗收全數通過，但：
1. Neon 的 Mac 在稽核時離線（`Your local machine isn't connected right now`），HOF-03 / HOF-12 及 Mac 路徑確認無法執行 → BLOCKED。
2. 發現一項來源完整性缺陷（HOF-07 FAIL）：公開 Git 的 32 個 CSV 版位存的是工具解析後的表格文字，不是原始 CSV 位元組。
3. 共用驗收工具 UI 寫死了 J4 專屬文案（HOF-09 FAIL，UI 層）。

## 1. HEAD 驗證（Step 1）

| 項目 | 值 |
| --- | --- |
| `git fetch --all` 後 PR #1 head (`origin/feat/creative-factory-managers-j4-archive-20261122`) | `f564073f64bf1298ae82e08167b474a97a87496b` |
| 基準 HEAD（Neon 指定） | `f564073f64bf1298ae82e08167b474a97a87496b` |
| 結果 | **一致**；未由 main 推斷 |
| PR #1 狀態 | OPEN, Draft, base=`main` |
| PR #1 CI（`gh pr checks 1`） | `browser-review` pass、`unittest` pass（CI 用 fixture，不是真實媒體驗收） |
| 檔案數（git ls-files @ f564073） | 263 |
| 注意 | 舊 `industrial-pipeline` 分支（含 `pipeline/build_animatic.py`）**不是** PR head 的祖先；PR head 不含 `pipeline/build_animatic.py` |

## 2. 私有資產驗證（Step 2a）

透過已授權 Google Drive 連線（唯讀）定位 `Higgsfield-Studio-Private-Assets/J4-ASYNC-SUCCESSION` 並下載到 box 私有路徑 `/workspace/j4-assets/`（不在 Git 內）。Drive 檔案 ID 不寫入本公開 repo。

| 檢查 | 期望（契約） | 實測 | 狀態 |
| --- | --- | --- | --- |
| ZIP 位元組數 | 76,407,296 | 76,407,296 | PASS |
| ZIP SHA-256（解壓前） | `4efe79aa…0ca3011e` | `4efe79aa309c193382a82e6c4c56654881df5dbba66df7cfc45df84f0ca3011e` | PASS |
| `review_web import-archive` | verified 267, missing [], mismatch [] | members 269（267 檔 + `MANIFEST/inventory.json` + `.csv`），verified 267, missing [], mismatch [] | PASS |
| 解壓後檔案數 `files/` | 267 | 267（另 2 個 MANIFEST 檔） | PASS |
| Drive 父資料夾 `j4_inventory_2026-11-22.json` vs ZIP 內 `MANIFEST/inventory.json` | 一致 | `cmp` 位元組完全相同；SHA-256 `40ad5010a5e5ae88dc1dab3f912c3968d5d98260a0e82711574d93312b0b095b`；`files_count`=267、`original_user_media_count`=5 | PASS |
| Drive 上 5 個獨立原始媒體的回讀雜湊 | 同 MEDIA_CUSTODY.md | 5/5 完全一致（見 `evidence-2026-11-22/drive_standalone_sha256.txt`） | PASS |
| ZIP 內 5 個原始媒體雜湊 | 同 MEDIA_CUSTODY.md | 5/5 一致 | PASS |
| Drive 權限（父資料夾、J4 資料夾、ZIP、IMG_7835.mp4） | 未分享 | 每個都只有 1 筆權限：owner（Neon 本人）；無 anyone/domain/其他使用者 | PASS |

檔案組成（267）：json 72、csv 50、md 47、py 42、png 16、zip 15、html 14、js 3、mp4 3、jpeg 2、txt 2、srt 1。inventory `kind`：text_or_code 231、binary_generated 31、user_original 5。

影片編碼（ffprobe）：IMG_7835/7836/7876 皆為 H.264 (avc1) 512×910 30fps + AAC；長度 58.13 s / 14.13 s / 29.03 s。

## 3. 本機驗收網站（Step 2b，在 box 上執行，不是 Mac）

指令（照 `docs/LOCAL_REVIEW.md`，只把路徑換成 box 私有路徑）：

```bash
python3 -m studio_factory.review_web serve --repo . --project j4-async-succession \
  --assets /workspace/j4-assets/J4 --db /workspace/j4-assets/reviews.sqlite3 --port 8765
# 輸出：J4 local review: http://127.0.0.1:8765 / assets available 267/267
```

綁定 127.0.0.1；未開 tunnel、未綁 0.0.0.0、未關 CSRF/Origin 保護。

### 3.1 HTTP 整合（`evidence-2026-11-22/http_probe.py`）

| 項目 | 結果 | 狀態 |
| --- | --- | --- |
| `/api/health` | 200 `READY / loopback / generation DISABLED` | PASS |
| 項目數 | shot 25、manager 17、resource 267（可用 267）、test 4 | PASS |
| 全檔下載並比對 SHA（mp4/jpeg/png/md/json/csv/html/zip 各 1） | 8/8 位元組雜湊與 inventory 一致；Content-Type 正確（video/mp4、image/jpeg、image/png、text/plain、application/json、text/csv、text/html、application/zip） | PASS |
| Range `bytes=0-1023` / `20000000-20001023` / `-1024` | 206 + 正確 `Content-Range`，各 1024 bytes | PASS |
| Range 超界 `bytes=999999999-` | 416 `bytes */36071278` | PASS |
| 錯誤 Host header | 403 | PASS |
| POST 無 CSRF / 錯誤 Origin | 403 / 403 | PASS |
| POST Pass / Fail / Defer（shot / manager / IMG_7835） | 200，寫入 SQLite | PASS |
| **重啟伺服器後** `/api/reviews` | 3 筆決策原樣保留（PASS/FAIL/DEFER） | PASS |
| 網站內建 4 個白名單測試 | core_contract PASS、budget PASS、inventory PASS（267/267）、shot_timeline PASS（90000 ms / 25 鏡） | PASS |

### 3.2 真實瀏覽器 E2E（Playwright + Google Chrome 156，headless，Linux）

`evidence-2026-11-22/browser_e2e.py`、`browser_viewers.py`；結果 JSON 同目錄。桌機 1440×960、手機 390×844（is_mobile, touch）。

| 項目 | 桌機 | 手機 | 狀態（box） |
| --- | --- | --- | --- |
| 分頁計數 | shot 25 / resource 267 / media 21 / html 14 / manager 17 / test 4 / all 313 | 同左 | PASS |
| Shot 清單 / 時間軸格數 | 25 / 25 | 25 / 25 | PASS |
| Manager 清單 | 17 | 17 | PASS |
| IMG_7835.mp4 播放 | play 2.5 s 後 currentTime 2.46、readyState 4、duration 58.13、512×910、無 error | 同 | PASS |
| Seek 到 42.0 s | currentTime 42、readyState 4、seeking=false | 同 | PASS |
| 圖片（IMG_7870.jpeg） | `<img>` naturalSize 864×1536、complete | 同 | PASS |
| Markdown（prop bible / prompt book） | 21 / 104 個標題節點，無 `<script>` | 同 | PASS |
| JSON（j4_shots.json） | 格式化顯示 65,136 字元 | 同 | PASS |
| CSV（j4_qc_matrix.csv） | 表格 7 欄表頭、24 列 | 同 | PASS |
| 歷史 HTML（前 3 個 review board） | sandbox=`allow-scripts` iframe，內容載入（1,016–1,556 字元） | 同 | PASS |
| UI 點 Defer → reload → 狀態與備註保留 | S05 保留 | S06 保留 | PASS |
| 水平溢出 | 無 | 無 | PASS |

UI 小缺陷（不影響上述 PASS，列為改善項）：
- **CSP 違規**：`app.js` 有 3 個 inline `style="…"`（`color:#8297a0`、`font-size:45px;color:#a7dac6`、`height:8px`），被自家 CSP `style-src 'self'` 擋下，console 反覆報錯；樣式失效但功能正常。
- 桌機首次載入有 1 個 404（推測 favicon）。
- 手機抽屜：390×844 時項目清單只剩約 117 px 高（約 2 列可見）；在搜尋框輸入時會自動選取並關閉抽屜。

截圖（存在 box `/workspace/j4-evidence/`，**未提交到公開 repo**，因為部分含 Neon 原始影像畫面；SHA-256 見 `evidence-2026-11-22/screenshots_sha256.txt`）：
`desktop_01_shot.png`、`desktop_02_managers.png`、`desktop_03_video_seek.png`、`desktop_04_{image,markdown,json,csv}.png`、`desktop_05_history_html.png`、`desktop_06_review_persist.png`、`desktop_07_*_details.png`，以及對應的 `mobile_*.png`、`mobile_00_sidebar_open.png`。

> 以上全部是 **box 上的 Linux Chrome** 證據，不能當作 Neon Mac（Safari/Chrome on macOS）的驗收。

## 4. Mac 實測（BLOCKED）

稽核時對 Mac（machine `8c580837…`）送出唯讀探查指令，回應：`Your local machine isn't connected right now (the Grok Bot desktop app must be open and online …)`。因此 Mac 上的 Repo、Assets、Review SQLite、Factory SQLite 實際路徑 **均未確認**。

Neon 需在 Mac 上執行（唯讀，不寫檔）並回傳輸出：

```bash
# 1) 路徑與版本
REPO="<你的 higgsfield-studio 路徑>"
git -C "$REPO" fetch --all && git -C "$REPO" rev-parse HEAD && git -C "$REPO" rev-parse --abbrev-ref HEAD
ls -la "$HOME/Higgsfield-Private" "$HOME/Higgsfield-Private/J4" "$REPO/.factory" 2>&1
find "$HOME/Higgsfield-Private/J4/files" -type f | wc -l        # 期望 267
shasum -a 256 "$HOME/Downloads/j4_all_available_resources_lossless_2026-11-22.zip"   # 期望 4efe79aa…3011e
shasum -a 256 "$HOME/Higgsfield-Private/J4/MANIFEST/inventory.json"                  # 期望 40ad5010…0b095b
ls -la "$HOME/Higgsfield-Private/reviews.sqlite3" "$REPO/.factory/registry.sqlite3"
sw_vers; python3 --version
```

若要完成 HOF-03 / HOF-12，再由 Neon 本人在 Mac 上執行 `docs/LOCAL_REVIEW.md` 的 import + serve，然後在 Safari 與 Chrome 中開 `http://127.0.0.1:8765`，逐項做：25 鏡、17 Managers、IMG_7835 播放/暫停/拖到 42 秒、圖片、MD/JSON/CSV、歷史 HTML、Pass/Fail/Defer → 重新整理仍在、iPhone 寬度（或 Safari 響應式模式）。截圖存在 `$HOME/Higgsfield-Private/evidence/`（私有），只把 SHA-256 回報。

## 5. HOF-01…HOF-12 缺口矩陣

| HOF | Source | Contract | Owner / Producer | Consumer | Verification Oracle | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 P0 | PR #1、`GROK_BOT_HANDOFF.md` | 確認 Bot 執行環境與權限；clone 正確分支並記錄 SHA；具 issue/PR 權限 | Grok Bot | Neon / 審核者 | `git rev-parse` = 基準；`gh pr view/checks` 可讀；能開 draft PR | HEAD `f564073…` = 基準；gh 可讀 PR/checks；本稽核 draft PR 已開（見 PR 連結） | PASS |
| 02 P0 | Drive `J4-ASYNC-SUCCESSION`、MEDIA_CUSTODY.md | Bot 能經授權讀 Drive；下載 ZIP 並重算 SHA-256 | Drive 連線 / Grok Bot | import-archive、review site | size 76,407,296 且 SHA `4efe79aa…`；import verified=267、missing=[]、mismatch=[] | §2 全表；`import_archive.log`；`drive_standalone_sha256.txt` | PASS |
| 03 P0 | `LOCAL_REVIEW.md`、`review_web.py`、`review_site/` | **在 Mac** localhost 瀏覽器完成端到端驗收 | Neon（Mac）+ review_web | Director / QC | Mac 上 Safari/Chrome 實測各項 + SQLite 重載保留 | box 上等效測試全過（§3），但 Mac 離線，未執行 | BLOCKED |
| 04 P0 | `GROK_BOT_HANDOFF.md` | 取得 owner 核准的檔案寫入範圍、受保護證據存放處、開 PR 權限；不合併、不付費 | Neon | Grok Bot | 書面授權 + 指定私有證據路徑 | t17u 授權「最小化 GitHub PR」→ PR 權限有；**Mac 寫入範圍與私有證據存放處（Drive 或 Mac 路徑）未指定** | BLOCKED |
| 05 P1 | `reviews.sqlite3` | 審核資料庫的安全備份與還原測試 | ReviewStore / Neon | QC、Delivery | 備份→還原→以還原檔啟動伺服器→決策一致 | box：sqlite backup API 還原 5/5 列一致、integrity ok、以還原檔啟動後提供相同 5 筆（`hof05_backup_restore.log`）。**但「安全的備份目的地」未設定**，Mac 的實際 DB 未備份 | BLOCKED |
| 06 P1 | PROJECT.json `source_transcript_status` | 取得完整逐字對話匯出 | Neon（原對話擁有者） | Provenance、Prompt | 逐字匯出檔 + 雜湊 | inventory `unavailable` 欄明載「No raw byte-exact export…」；v2.6 Prompt Book 非逐字 | BLOCKED |
| 07 P1 | ZIP 267 檔 vs Git archive、`pipeline/build_animatic.py` | 調和輔助建置程式、獨立原始來源、舊 UX 證據、legacy build_animatic schema；不得杜撰 | Provenance Manager | Shot / QC / Delivery | 逐檔比對 ZIP 原檔 vs Git 版位 | (a) v2_6 八檔中 7 檔語意相同，**`j4_qc_matrix.csv` 不同**；(b) Git 共 **32 個 CSV 版位**（v2_6 1 個 + 14 個 JSON 封存中 31 個）存的是 `<PARSED TEXT FOR SHEET…>` + pandas index 欄的解析稿，不是原始 CSV（清單：`parsed_sheet_csv_slots.txt`）；原始 CSV 只在私有 ZIP；(c) 42 個 `.py` 建置腳本與 3 個 `.js` 只在 ZIP；(d) PR head 不含 `pipeline/build_animatic.py`，schema 相容性未測（`hof07_zip_vs_git.log`） | FAIL |
| 08 P1 | QC matrix、Rights/Contest 規則 | 把藝術原創性、音樂、版權素材、肖像、權利、參賽資格、真實觀眾驗收與 source/CI 狀態分開 | Rights / QC Manager、Neon | Generation、Delivery | 各項有人審證據 | 文件層已分開（PROJECT.json `source_risk: UNREVIEWED`、gates BLOCKED）；但沒有任何權利、肖像、音樂、參賽、觀眾審核紀錄。已知風險：IMG_7835/7836/7876 為 Neon 本人拍攝，比賽規則禁止可辨識真人（含本人） | NOT_RUN |
| 09 P1 | `studio_factory/core.py`、`review_web.py`、`review_site/` | 第二部作品命名空間重用 shared 來源，且不洩漏 state/rights/budget | Portfolio Manager | 新作品 | 第二專案：可引用 shared、不可引用 J4、J4 gate 核准不外溢 | Registry 層（J4 seeded DB 的暫存副本）：film-two 引用 shared OK；引用 J4 artifact 被擋；J4 四 gate 設 APPROVED 後 film-two 仍 `generation BLOCKED: owner_approval`（`hof09_isolation_demo.log`）。**但共用驗收 UI 寫死 J4 文案**：`index.html` 時間軸圖例「63.700s · S18 全局斷點」「其餘 24 鏡」「90 秒鏡頭時間軸」、預設專案標題 J4；`review_web.py` `_find_shots` 退回 `j4_museum_v2_6/j4_shots.json`、User-Agent `J4Review/1.0`。另 `shared` 命名空間目前 0 筆已推廣的方法紀錄 | FAIL |
| 10 P2 | `GROK_BOT_HANDOFF.md` | 若需遠端操作：設計窄權限、已認證的私有存取（如 Tailscale）+ owner 核准的本機執行者；禁止公開 localhost proxy | Neon / 架構 | Grok Bot | 設計文件 + owner 核准 | 未撰寫；目前路徑是 Grok Bot 桌面 app 的本機工具（需 Mac 在線 + 每次核准），未開任何 tunnel | NOT_RUN |
| 11 P2 | Drive vault | 明定 Drive 物件保留、checksum/回讀、權限稽核、隱私與災難復原 | Asset / Provenance Manager、Neon | 所有作品 | 書面政策 + 定期回讀/權限稽核紀錄 | 本次已做一次性回讀（ZIP + 5 媒體 + inventory 全部雜湊一致）與權限稽核（owner-only）；**保留期、版本化、DR 政策文件不存在** | NOT_RUN |
| 12 P2 | 3 支 MP4、review site | 在目標 Mac 瀏覽器/裝置測 codec 與播放，產出可重現截圖與媒體收據 | Neon（Mac/iPhone） | Director / QC | macOS Safari + Chrome（及 iPhone）播放/seek 截圖 + 雜湊 | box Linux Chrome 156：H.264/AAC 播放與 seek 正常；**目標 Mac/裝置未測**（Mac 離線） | BLOCKED |

**統計**：PASS 2（01、02）· FAIL 2（07、09）· BLOCKED 5（03、04、05、06、12）· NOT_RUN 3（08、10、11）。

## 6. 架構審查（Step 4：共用 vs 每部作品獨立）

| 類別 | 應為 | 現況 | 判定 |
| --- | --- | --- | --- |
| 研究 | shared（已審） | `research/`（creators、prompt libraries）在 repo 根；J4 的 `SOURCE_REGISTER_v3_3.csv` 標為 `shared-candidate`，尚未推廣 | 部分 |
| 當代藝術方法 | shared（已審、method-only） | `ART_METHOD_SOURCES_v4_0.csv` 為 `shared-candidate`，版權未審；仍在 J4 封存內 | 缺口 |
| Optical IR 方法 | shared 方法 + 專案 IR | `j4_shot_optical_ir_v3_2`、`j4_illusion_ir_v3_3`、`j4_memory_arcs_v3_2` 全為 `project-overlay`；沒有抽離出的通用 Optical 方法 | 缺口 |
| Sound 方法 | shared 方法 + 專案 IR | `j4_sound_dramaturgy_overlay_v3_7`、`j4_sonic_object_registry_v3_9` 為 `project-overlay`；通用方法未抽離 | 缺口 |
| Prompt Templates | shared | `prompts/`、`templates/`、`skills/` 在 repo 根，可共用 | OK |
| 驗收工具 | shared，專案參數化 | `review_web.py --project/--assets/--db` 已參數化；UI 仍寫死 J4 文案（見 HOF-09） | 部分 |
| 故事、角色、原始影片、成本、權利、批准 | 每部作品私有 | `projects/<slug>/PROJECT.json`、`archive/`；媒體在私有 Drive；generation gate 以專案為單位且不外溢（已驗證） | OK |
| 成本 | 每部作品 + 帳戶總上限 | `budget/ledger.csv`、`allocation.csv` 是帳戶層級（9,000 點/月，80% 警戒）；`require_generation_gate` 需呼叫者傳入已花費數，沒有每部作品獨立 ledger | 部分 |
| 審核資料 | 每部作品獨立 DB | 文件建議每片一組 `--assets/--db`；`reviews` 表沒有 project 欄位，若共用同一 DB 會混在一起 | 部分 |
| 歷史保留 | 不覆蓋 | `publish` 需 `expected_previous`、舊 revision 保留（unit test 驗證）；本稽核未改任何舊檔 | OK |

## 7. 建議的下一步（皆需 Neon 另行核准，本 PR 不做）

1. **HOF-07 修復**（append-only）：把 ZIP 內 32 個原始 CSV 以新檔加入 `projects/j4-async-succession/archive/<ver>/original_csv/`，附 SHA-256，不覆蓋現有解析稿；並在 SOURCE_MAP 加新版本列。需先確認這些 CSV 可公開（皆為 J4 文字，無媒體）。
2. **HOF-09 修復**：把 `index.html` 時間軸圖例改由 `PROJECT.json`（例如新增 `global_sync_point_ms`、`sync_shot`）驅動；移除 `_find_shots` 的 J4 退回路徑；`reviews` 表加 `project` 欄。
3. UI：移除 3 個 inline style（改 class），補 favicon，手機抽屜清單最小高度。
4. Mac 上線後跑 §4 指令，回傳輸出 → 才能處理 HOF-03/04/05/12。
5. 指定私有證據與 DB 備份目的地（例如 Drive `Higgsfield-Studio-Private-Assets/J4-ASYNC-SUCCESSION/evidence/`），之後才能把截圖等含原始影像的證據上傳。

## 8. 證據索引（`docs/audits/evidence-2026-11-22/`，僅文字，無私有媒體）

| 檔案 | 內容 |
| --- | --- |
| `import_archive.log` | import-archive 輸出（verified 267） |
| `drive_standalone_sha256.txt` | Drive 5 個獨立媒體回讀雜湊 |
| `unittest.log` / `budget_test.log` / `seed_archive.log` | 15 tests OK / budget OK / seed created 132 |
| `server_run1.log` / `server_run2.log` / `server_restore.log` | 伺服器啟動輸出 |
| `http_probe.py`、`http_probe_run1.json`、`http_probe_run2_after_restart.json` | HTTP/Range/CSRF/持久化 |
| `site_whitelisted_tests.json` | 網站 4 個白名單測試 |
| `browser_e2e.py`、`browser_e2e_result.json`、`browser_viewers.py`、`browser_viewers_result.json` | Playwright 桌機/手機 |
| `screenshots_sha256.txt` | box 上截圖雜湊（截圖本身不提交） |
| `hof05_backup_restore.log`、`hof07_zip_vs_git.log`、`parsed_sheet_csv_slots.txt`、`hof09_isolation_demo.log` | 各 HOF 佐證 |

box 私有檔雜湊（未提交）：`reviews.sqlite3` `352a9bb23c329c5a9bf235baf56917358b5b64b03f1a11d261fadae9c3cdb721`、`registry.sqlite3`（seed 後）`5f06fcdfeee20eb6ed5e56f603dc56426d79062ae7d39daf00e444ca88fe346f`。box 審核 DB 中有 5 筆稽核探針決策（reviewer=`grok-bot-audit*`），只存在 box，不代表任何真實人審。

---

## Addendum 3：在 box 上用 Linux Chrome 做 GUI 稽核（2026-11-22 22:45–22:52 Asia/Taipei）

> 這段是追加內容，前面各節都沒有改。測試是在 Grok Bot 電腦（box）上用 **Linux Chrome** 做的，**不是 Safari**，也不是 Neon 的 Mac。截圖裡有 Neon 的原始影像，所以沒有提交。

**伺服器設定**
- 程式：worktree `/workspace/hs-pr1`，HEAD `f564073f64bf1298ae82e08167b474a97a87496b`
- 素材：`/workspace/j4-assets/J4`，267 個檔，已驗證雜湊
- 審核資料庫：`/workspace/j4-assets/reviews.gui-audit.sqlite3`，稽核前是全新的空資料庫
- 位址：只綁本機 `127.0.0.1:8765`
- 第一階段 PID 439057；第二階段重啟後 PID 448077

### 第一階段：GUI 操作（全部 PASS）

| # | 檢查 | 結果 | 狀態 |
| --- | --- | --- | --- |
| 1 | 計數 | 25 鏡、267 素材、21 可播放媒體、14 審核頁、17 Managers、4 個測試、全部 313 | PASS |
| 2 | 影片 | IMG_7835（0:58）可以播放，拖到 0:42 正常。IMG_7836（0:14）和 IMG_7876（0:29）可以播放。影片沒有靜音，但 agent 聽不到聲音。小問題：播放時時間顯示有時會停在 0:00 | PASS |
| 3 | 檔案檢視 | jpeg 完整顯示、沒有裁切；Markdown 的標題和 pre 區塊正常；JSON 有格式化（30 個鍵）；CSV 顯示為表格 | PASS |
| 4 | 歷史 HTML | `j4_art_illusion_review_board_v3_3.html` 在 iframe 裡顯示，S01–S05 下拉選單能用 | PASS |
| 5 | 審核寫入 | S02 標 PASS、art_direction 標 FAIL、IMG_7835.mp4 標 DEFER，備註都填 `gui-audit`；重新整理後三筆都還在 | PASS |
| 6 | 手機寬度 400px | 漢堡選單能用、影片能播、沒有水平捲動 | PASS |

Console 只有一個錯誤：`favicon.ico` 回 404。

### 第二階段：伺服器重啟後的持久化（PASS）

伺服器重啟後（新 PID 448077）做強制重新整理。「已審核」計數顯示 3，三筆決策都還在，時間戳是 14:49:15Z、14:49:29Z、14:49:37Z（台北時間 22:49:15、22:49:29、22:49:37）。

另外用 sqlite 直接查 `reviews` 資料表，確認有這 3 列：

| item_id | 決策 | 備註 | 時間（UTC） |
| --- | --- | --- | --- |
| `6bbe131773f31f3bee` | PASS | gui-audit | 2026-11-22T14:49:15.508644+00:00 |
| `72f41faf9c21cb1bb5` | FAIL | gui-audit | 2026-11-22T14:49:29.226947+00:00 |
| `494a1f9bdf298ccbd0` | DEFER | gui-audit | 2026-11-22T14:49:37.010735+00:00 |

這 3 筆都是稽核用的測試決策，不代表有人真的審過。

### 對 HOF 矩陣的影響

這次的結果記為 **box Chrome 的 GUI 與持久化證據**，HOF 狀態都不變：
- **HOF-03：** 仍是 BLOCKED。機器能驗的部分現在有三份證據：box 的 Playwright、Mac 的 headless Chrome、box 的 GUI Chrome。還缺 Safari 實測，以及 Neon 本人在 Mac 上確認畫面和聲音。
- **HOF-12：** 仍是 BLOCKED。Linux Chrome 和 macOS Chrome 的 H.264/AAC 播放都正常，但 Safari 和 iPhone 還沒測，也還沒有人確認聲音。

計數（同附錄 2）：PASS 3（01、02、04）· FAIL 2（07、09）· BLOCKED 4（03、05、06、12）· NOT_RUN 3（08、10、11）。新缺陷 G-13、G-14 仍是 FAIL。

新增兩個小的 UI 改善項：播放中時間顯示偶爾停在 0:00、缺少 favicon。
