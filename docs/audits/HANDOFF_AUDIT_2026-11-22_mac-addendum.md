# Handoff Audit 附錄 — Mac 實機（2026-11-22 22:24–22:35 Asia/Taipei）

- 本檔為 append-only 附錄；**未修改** `HANDOFF_AUDIT_2026-11-22.md` 或任何既有檔。
- 主機：`MacBookPro.mymeshdevice.home`（user `neon`，macOS 26.6.2，Homebrew Python 3.15.0，Google Chrome 157.0.8103.79）。
- 授權：Neon 核准在這台 Mac 上全新安裝 J4（loopback only）。0 Higgsfield 點數、無生成、無發布、未改 Drive 分享、未合併 main。
- Mac 上的私有證據放在 `~/Higgsfield-Private/evidence/`，**不進 Git**；這裡只記雜湊與文字結果。
- 寫入的審核決策全部是測試資料：reviewer=`grok-bot-mac-audit`，備註都寫明「TEST DECISION … not a human review」。

## A. 實際路徑與 HEAD

| 項目 | Mac 路徑 | 狀態 |
| --- | --- | --- |
| Repo | `/Users/neon/Developer/higgsfield-studio`（分支 `feat/creative-factory-managers-j4-archive-20261122`，工作區乾淨） | 存在 |
| `git rev-parse HEAD` | `f564073f64bf1298ae82e08167b474a97a87496b`（= 基準） | PASS |
| `git ls-files docs/GROK_BOT_HANDOFF.md studio_factory/review_web.py` | 兩個都在 | PASS |
| `git ls-files projects/j4-async-succession/archive` | 25 個檔：MEDIA_CUSTODY.md、conversation_attachment_index.json、v2_6 八檔、v2_7…v4_0 的 14 個 `conversation_text_archive.json` | PASS |
| Assets root | `/Users/neon/Higgsfield-Private/J4`（已建立，**是空的**） | 未解壓 |
| Review SQLite | `/Users/neon/Higgsfield-Private/reviews.sqlite3`（伺服器建立，4096 B，SHA-256 `89a2318c76452be80e1d743f163f3dd96623b2b05604aa06985c6b5501238362`；量測時點，WAL 可能使雜湊隨後變動） | 存在（只有測試決策） |
| Factory SQLite | `/Users/neon/Developer/higgsfield-studio/.factory/registry.sqlite3`（`seed_archive` created 132；SHA-256 `9e24e5f6465b04222087ee2679c3758b790383d550558cd85fb6244016cce12f`；已被 `.gitignore` 忽略） | 存在 |
| Drive manifest | `/Users/neon/Higgsfield-Private/drive_manifest.json` | 不存在（選用；含私有 ID，未建立） |
| 私有證據 | `/Users/neon/Higgsfield-Private/evidence/` | 存在 |
| Playwright venv | `/Users/neon/Higgsfield-Private/.pwvenv`（使用者層級 venv，不在 repo 內，沒有系統層級安裝） | 存在 |

## B. 失敗與缺失（主機皆為 `MacBookPro.mymeshdevice.home`，HEAD 皆為 `f564073f64bf1298ae82e08167b474a97a87496b`）

| 完整路徑 | 錯誤原因 | 分類 |
| --- | --- | --- |
| `/Users/neon/Downloads/j4_all_available_resources_lossless_2026-11-22.zip` | box 到 Mac 的複製（CopyFromBox，來源是 box 上已驗證雜湊的副本）在約 49 秒時**被使用者中斷**；Mac 上沒有這個檔案。依規則不自動重試，也沒有改用擴大 Drive 分享的方式 | not-existing |
| `/Users/neon/Higgsfield-Private/J4/MANIFEST/inventory.json` | `ls: No such file or directory`；因為沒有 ZIP，無法執行 `import-archive` | not-extracted |
| `/Users/neon/Higgsfield-Private/J4/files` | 同上 | not-extracted |
| `/Users/neon/Developer/higgsfield-studio/budget/test_track.py`（→ `budget/track.py:207-210`） | `ValueError: badly formed help string`：`--no-fail` 的 help 文字「即使達到 80% 也以結束碼 0 離開」裡有未跳脫的 `%`，Python 3.15 的 argparse 會驗證格式字串。box 上的 Python 3.13 會通過 | 不屬於四類（Python 3.15 相容性缺陷） |
| `/Users/neon/Developer/higgsfield-studio/pipeline/build_animatic.py` | PR head 沒有這個檔（只在舊的 `industrial-pipeline` 分支 commit `f9887a1`），ZIP inventory 也沒有 | not-existing |
| `/Users/neon/Higgsfield-Private/drive_manifest.json` | 沒有建立（選用） | not-existing |

沒有發生 permission 或 wrong-path 類錯誤。

## C. 測試與還原

| 指令 | 結果 |
| --- | --- |
| `python3 -m unittest discover -s studio_factory/tests -v` | 15 tests OK（Python 3.15 只有 ResourceWarning，不影響結果） |
| `python3 budget/test_track.py` | **FAILED (errors=1)**，見 B 表 |
| `python3 -m studio_factory.seed_archive projects/j4-async-succession --db .factory/registry.sqlite3` | created 132 |
| `python3 -m studio_factory.archive …/v4_0/conversation_text_archive.json /tmp/j4-v4_0` | restored 14 files；`/tmp/j4-v4_0/j4_cross_modal_ir_v4_0.json` 存在，SHA-256 `7fcd03c9bcacdc7dbac9823d5cfe72d1fc17fa7369539a404ed2da5e561bb704`（box 還原的雜湊相同）。和 ZIP 原檔（`7a9549d2c7fc3be30dbb4a770987d13fd33964cb5246e8e6175f1b70cd847040`）位元組不同，但 JSON 語意相等。14 個檔案裡：1 個 HTML 位元組相同；10 個只差空白；**3 個 CSV 是解析稿**（`ART_METHOD_SOURCES_v4_0.csv`、`j4_blind_scorecard_v4_0.csv`、`j4_stimulus_manifest_v4_0.csv`），佐證 HOF-07 |

## D. 本機網站（Mac，loopback）

啟動指令（照 `docs/LOCAL_REVIEW.md`；以 nohup 放背景，**目前仍在執行**，PID 24925，`127.0.0.1:8765` LISTEN）：

```bash
cd ~/Developer/higgsfield-studio
python3 -m studio_factory.review_web serve --repo . --project j4-async-succession \
  --assets "$HOME/Higgsfield-Private/J4" --db "$HOME/Higgsfield-Private/reviews.sqlite3" --port 8765
# 輸出：J4 local review: http://127.0.0.1:8765 / assets available 0/0
```

| 檢查（Mac 上用 curl 或 Python urllib） | 結果 | 狀態 |
| --- | --- | --- |
| `GET /` | 200，6,591 B | PASS |
| `/api/health` | READY / loopback / generation DISABLED | PASS |
| 25 shots / 17 managers / 4 tests | 25 / 17 / 4 | PASS |
| 資源（267） | 0：沒有 assets | BLOCKED |
| Range 206（IMG_7835）、image/MD/JSON/CSV/歷史 HTML 端點 | 沒有 assets，無法測 | BLOCKED |
| 錯誤 Host / 錯誤 CSRF / 未知 media | 403 / 403 / 404 | PASS |
| POST Pass(S01) / Fail(第一個 Manager) / Defer(S02) | 200 ×3 | PASS |
| 重啟伺服器後 `/api/reviews` | 3 筆保留 | PASS |
| 網站白名單測試 | core_contract PASS、**budget FAIL**（Python 3.15）、shot_timeline PASS、**inventory「PASS」checked 0 / expected 0** | 見新缺陷 |

Headless Google Chrome 157（Mac，使用者 venv 裡的 Playwright 驅動已安裝的 Chrome.app）：

| 項目 | 桌機 1440×960 | 手機 390×844 |
| --- | --- | --- |
| 計數 | shot 25 / manager 17 / test 4 / resource 0 / all 46 | 同 |
| Shot 清單 / 時間軸 | 25 / 25 | 25 / 25 |
| Manager 清單 | 17 | 17 |
| UI 按 Defer → reload 後保留 | S03 保留 | S04 保留 |
| 水平溢出 / page error | 無 / 無 | 無 / 無 |

證據雜湊（Mac `~/Higgsfield-Private/evidence/`）：
`mac_desktop_shot.png 0098218799e7…`、`mac_desktop_managers.png 7a7b8966c6c3…`、`mac_desktop_review_persist.png f2c2d485ce6a…`、`mac_mobile_shot.png 1479621bab8c…`、`mac_mobile_managers.png 3b7f6857465f…`、`mac_mobile_review_persist.png 4dec41f05081…`、`mac_headless_result.json e3f9dc9849bd…`、`mac_probe_run1.json f66456f6ed9b…`、`mac_probe_run2_after_restart.json 838c06444009…`、`mac_probe.py 3151571b9f91…`、`mac_headless.py 3aeeb75d49a6…`。

## E. 新發現的缺陷（Mac 實測才出現）

- **G-13 FAIL：** `budget/track.py` 在 Python 3.15 會崩潰（`%` 沒有跳脫）。修法是把 help 字串改成 `80%%`。這會影響預算護欄，在 Mac 上 `track.py` CLI 無法執行。
- **G-14 FAIL：** 缺 assets 時出現「空驗收 PASS」。沒有 MANIFEST 時，伺服器顯示 `assets available 0/0`，inventory 測試回 `PASS checked 0 expected 0`。正確行為應該是期望值取自 `PROJECT.json` 或文件，也就是 267，並回 FAIL/BLOCKED。這是假 PASS 風險。

## F. 四方對照：GitHub vs Drive vs ZIP vs Mac runtime

| 資源 | GitHub（PR head f564073） | Drive（私有） | ZIP（box 驗證） | Mac runtime |
| --- | --- | --- | --- | --- |
| IMG_7835.mp4 | 只有雜湊（MEDIA_CUSTODY，EXTERNAL_ONLY） | 獨立檔，回讀雜湊相符 | `files/IMG_7835.mp4` 相符 | 無（not-extracted） |
| IMG_7836.mp4 | 只有雜湊 | 獨立檔，相符 | 相符 | 無 |
| IMG_7876.mp4 | 只有雜湊 | 獨立檔，相符 | 相符 | 無 |
| IMG_7870.jpeg | 只有雜湊 | 獨立檔，相符 | 相符 | 無 |
| IMG_7899.jpeg | 只有雜湊 | 獨立檔，相符 | 相符 | 無 |
| 267 檔完整交接 | 沒有原檔，只有 132 個文字版位，其中 32 個 CSV 是解析稿 | ZIP + inventory.json（與 ZIP 內 MANIFEST 位元組相同） | 267/267 verified | 0/267（ZIP 未到） |
| v2.7–v4.0 封存提示詞 | 14 個 JSON 封存，可還原；Mac 已還原 v4_0 共 14 檔 | 在 ZIP 內 | `j4_museum_v2_7…v4_0` 原檔 | Git 版有、ZIP 原檔無；`/tmp/j4-v4_0` 已還原 |
| reviews.sqlite3 | 無（設計上就不放） | 無 | 無 | `~/Higgsfield-Private/reviews.sqlite3`（只有測試決策；沒有備份） |
| .factory/registry.sqlite3 | 無（gitignored） | 無 | 無 | `~/Developer/higgsfield-studio/.factory/registry.sqlite3`（132） |
| drive_manifest.json | 無（禁止放） | 無 | 無 | 無（選用） |
| pipeline/build_animatic.py | PR head 沒有；只在 `industrial-pipeline@f9887a1` | 無 | 無 | 無 |
| 逐字 ChatGPT 對話 | 無（NOT_AVAILABLE_VERBATIM） | 無 | 無（inventory `unavailable` 註明） | 無 |
| 最終影片 / 混音 | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |

## G. 更新後的 HOF 狀態（取代主稽核 §5 的計數，主檔不改）

| HOF | 舊狀態 | 新狀態 | 理由 |
| --- | --- | --- | --- |
| 01 | PASS | PASS | Mac 的 HEAD 也是 f564073 |
| 02 | PASS | PASS | Bot 從 Drive 讀取並驗證雜湊（box）；Mac 副本未到，記在 HOF-03 |
| 03 | BLOCKED | BLOCKED | Mac 伺服器、25/17、persistence 都 PASS；但 Mac 上沒有 assets，影片、seek、圖片、文字檢視器都無法測；Safari GUI 也未測 |
| 04 | BLOCKED | **PASS** | Neon 核准 Mac 全新安裝的寫入範圍；私有證據放在 `~/Higgsfield-Private/evidence/`；PR 權限有；未合併、未付費 |
| 05 | BLOCKED | BLOCKED | Mac 的 DB 已存在，但沒有備份目的地，也沒做還原測試 |
| 06 | BLOCKED | BLOCKED | 沒有逐字對話 |
| 07 | FAIL | FAIL | Mac 還原 v4_0 再次確認 3 個解析稿 CSV |
| 08 | NOT_RUN | NOT_RUN | — |
| 09 | FAIL | FAIL | — |
| 10 | NOT_RUN | NOT_RUN | 目前透過桌面 app 執行本機指令，每次都需要核准；沒有 tunnel |
| 11 | NOT_RUN | NOT_RUN | — |
| 12 | BLOCKED | BLOCKED | Mac 上沒有媒體；Chrome 157 headless 只驗了版面 |

**計數：** PASS 3（01、02、04）· FAIL 2（07、09）· BLOCKED 4（03、05、06、12）· NOT_RUN 3（08、10、11）。另有新缺陷 G-13、G-14 FAIL。

## H. Neon 要做的事

1. **把 ZIP 放到 Mac。** 二擇一：
   - 允許重新從 box 複製到 `~/Downloads/`（約 73 MB）；或
   - 自己從 Drive `Higgsfield-Studio-Private-Assets/J4-ASYNC-SUCCESSION` 下載到 `~/Downloads/`。

   然後執行：
   ```bash
   shasum -a 256 ~/Downloads/j4_all_available_resources_lossless_2026-11-22.zip   # 必須 = 4efe79aa309c193382a82e6c4c56654881df5dbba66df7cfc45df84f0ca3011e
   cd ~/Developer/higgsfield-studio
   python3 -m studio_factory.review_web import-archive --archive ~/Downloads/j4_all_available_resources_lossless_2026-11-22.zip --destination "$HOME/Higgsfield-Private/J4"   # verified 267, missing [], mismatch []
   shasum -a 256 ~/Higgsfield-Private/J4/MANIFEST/inventory.json   # = 40ad5010a5e5ae88dc1dab3f912c3968d5d98260a0e82711574d93312b0b095b
   pkill -f "studio_factory.review_web serve"; nohup python3 -m studio_factory.review_web serve --repo . --project j4-async-succession --assets "$HOME/Higgsfield-Private/J4" --db "$HOME/Higgsfield-Private/reviews.sqlite3" --port 8765 >/dev/null 2>&1 &
   ```
2. **在 Safari 和 Chrome 開 `http://127.0.0.1:8765`，逐項勾選：**
   - [ ] 左側計數：鏡頭 25、素材與文件 267、可播放媒體 21、審核實驗頁 14、Domain Managers 17、測試執行 4
   - [ ] 「可播放媒體」→ IMG_7835.mp4：按播放有畫面和聲音 → 暫停 → 拖到 0:42 → 繼續播放（IMG_7836、IMG_7876 也各試一次）
   - [ ] 「全部項目」搜尋 IMG_7870.jpeg → 圖片完整顯示
   - [ ] j4_master_prompt_book.md → 標題和程式碼區塊正常
   - [ ] j4_shots.json → 格式化 JSON
   - [ ] j4_qc_matrix.csv → 7 欄表格
   - [ ] 「審核實驗頁」→ 任一 review board 在 iframe 裡顯示並可操作
   - [ ] 任選一鏡按 Pass、一個 Manager 按 Fail、一支影片按 Defer，寫備註 → ⌘R 重新整理 → 三筆都還在；關掉伺服器再啟動 → 仍然在
   - [ ] Safari「開發 → 進入響應式設計模式」選 iPhone 寬度（或直接用 iPhone 連同一台 Mac 是做不到的，因為只綁 loopback）：☰ 選單可開、清單可點、沒有水平捲動
   - [ ] 「測試執行」→ 4 個測試：inventory 應該顯示 267/267；budget 目前在 Python 3.15 會 FAIL（G-13）
   - [ ] 截圖存到 `~/Higgsfield-Private/evidence/`，並回報 `shasum -a 256`
3. 決定 Mac `reviews.sqlite3` 的備份目的地（HOF-05），以及要不要清掉 `grok-bot-mac-audit` 的測試決策。
