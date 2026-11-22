# Handoff Audit 附錄 2：Mac 素材匯入後重測（2026-11-22 22:36 起，Asia/Taipei）

本檔是 append-only 附錄，沒有修改 `HANDOFF_AUDIT_2026-11-22.md` 或 `HANDOFF_AUDIT_2026-11-22_mac-addendum.md`。

- **測試主機：** `MacBookPro.mymeshdevice.home`（使用者 neon）。macOS 26.6.2，Python 3.15.0，Google Chrome 157.0.8103.79。HEAD 為 `f564073f64bf1298ae82e08167b474a97a87496b`，工作區乾淨。
- **操作邊界：** 0 Higgsfield 點數、沒有生成、沒有發布、沒有更動 Drive 分享、沒有合併 main。
- **私有證據：** 放在 Mac 的 `~/Higgsfield-Private/evidence/`，本檔只記錄雜湊。

## 1. ZIP 與匯入

| 檢查 | 結果 | 狀態 |
| --- | --- | --- |
| ZIP 來源 | Neon 自己從私有 Drive 下載到 `/Users/neon/Downloads/j4_all_available_resources_lossless_2026-11-22.zip` | — |
| 大小 / SHA-256 | 76,407,296 / `4efe79aa309c193382a82e6c4c56654881df5dbba66df7cfc45df84f0ca3011e` | PASS |
| 匯入（照 `docs/LOCAL_REVIEW.md` 執行 `import-archive`，目的地 `~/Higgsfield-Private/J4`） | members 269，verified 267，missing []，mismatch [] | PASS |
| `~/Higgsfield-Private/J4/files` 檔案數 | 267 | PASS |
| `MANIFEST/inventory.json` SHA-256 | `40ad5010a5e5ae88dc1dab3f912c3968d5d98260a0e82711574d93312b0b095b`，和 Drive、box 上的一致 | PASS |
| 5 個原始媒體的雜湊 | 都和 MEDIA_CUSTODY.md 一致 | PASS |

## 2. 伺服器

- 已停掉舊的 PID 24925，用 nohup 在背景重新啟動 PID 43059，監聽 `127.0.0.1:8765`。指令和 LOCAL_REVIEW.md 相同，啟動訊息為 `assets available 267/267`。**伺服器保持執行中。**

## 3. Mac 本機 HTTP 測試（`mac_media_probe.py`）

| 檢查 | 結果 | 狀態 |
| --- | --- | --- |
| 項目數 | shot 25、manager 17、test 4、resource 267（可用 267） | PASS |
| IMG_7835 / 7836 / 7876 的 Range 請求：開頭、中段、結尾 1024 bytes | 都回 206，`Content-Range` 正確 | PASS |
| 同上，超出檔案範圍 | 都回 416 `bytes */<size>` | PASS |
| 3 支影片完整下載 | 200、`video/mp4`，SHA 和 inventory 一致 | PASS |
| IMG_7870.jpeg、IMG_7899.jpeg、j4_master_prompt_book.md、j4_shots.json、j4_qc_matrix.csv、j4_cross_modal_review_board_v4_0.html | 都回 200，Content-Type 正確，SHA 都一致 | PASS |
| 內建測試 | core_contract PASS、shot_timeline PASS、**inventory PASS（checked 267 / expected 267）**、**budget FAIL**（G-13，Python 3.15 的 argparse `%` 問題，和預期一致） | 見下 |
| 審核紀錄持久化 | 先前 5 筆 `grok-bot-mac-audit` 測試決策在重啟後都還在 | PASS |

## 4. Mac 上的 headless Google Chrome 157（`mac_headless_media.py`）

桌機用 1440×960，手機用 390×844（is_mobile、touch）。兩種尺寸的結果完全相同。

| 項目 | 結果 | 狀態 |
| --- | --- | --- |
| 計數 | shot 25 / resource 267 / media 21 / html 14 / manager 17 / test 4 / all 313 | PASS |
| IMG_7835 | 播放約 2.46 秒，readyState 4，長度 58.13 秒，512×910，沒有錯誤；seek 到 **42.0 秒**後 currentTime=42，readyState 4 | PASS |
| IMG_7836 | 播放正常；seek 到 10 秒正確（長度 14.13 秒） | PASS |
| IMG_7876 | 播放正常；seek 到 10 秒正確（長度 29.03 秒） | PASS |
| 圖片 IMG_7870 | naturalSize 864×1536，已載入完成 | PASS |
| Markdown（prompt book） | 104 個標題、79 個 pre 區塊，沒有 `<script>` | PASS |
| JSON（j4_shots.json） | 格式化顯示，65,136 字元 | PASS |
| CSV（j4_qc_matrix.csv） | 7 欄表頭、24 列 | PASS |
| 歷史 HTML | 列表 14 項；sandbox `allow-scripts` 的 iframe 有載入（1,556 字元） | PASS |
| 版面 | 沒有水平溢出，沒有 page error | PASS |

截圖 SHA-256（只存在 Mac 的私有目錄，沒有提交到 Git）：

| 檔案 | SHA-256 |
| --- | --- |
| mac_desktop_video_seek42.png | `403b9f4ced89c14e306f0c6385da5e5dafd70e59050cc22a3a9469f016f4b00c` |
| mac_mobile_video_seek42.png | `cdfa34e9f8af602cdbc9ab790c0cd6074e6d71d15d0c1601a733d940307add9d` |
| mac_desktop_image.png | `38c624760b265f1892f2653d30f912299daeb0d15e628c8dbb39fe171202ff6a` |
| mac_mobile_image.png | `fa09c01200eb19cf7afe1a404a50daf96c6d13adaadc749f17ea6f3f4f75fa96` |
| mac_desktop_markdown.png | `057925ccdf6cbcb5fe65cb1933387dec6cec52dec31eeaa0672de65246902a33` |
| mac_mobile_markdown.png | `c81443d20d698f2715dfa07dfdbad36572db967823a4d087872f57b78be16405` |
| mac_desktop_json.png | `6e6c94f25c2108dcd046990d4cf78f2cad8078d767630542075e089b47c65777` |
| mac_mobile_json.png | `075ed334e463c7b6e3f4b46bdeb0547a9e4cc67ec599140f70e80989788cc25b` |
| mac_desktop_csv.png | `60817586e984a878c7034125dab6ac3088b85ae9f347738e26df62acacb30131` |
| mac_mobile_csv.png | `3c800dc80d88d6fb1578cc0496e03a810b6398e8ea5690dca328d4a0df54cfc7` |
| mac_desktop_history_html.png | `64db618318dab19030cc1df6de3b291e73aa54d4bd3a30967294c56965ffe2cb` |
| mac_mobile_history_html.png | `bcc4d3cd1c4dc2db1f0d883b0d5c0d8fdda76f4408c0c4e8114879b5e0092442` |
| mac_import_archive.log | `dd9911f93a910e2f9a02a8dc8e3b757bf623d0ee963122d7cbb2f44979e6587f` |
| mac_media_probe.json | `48ead4d110b76e819e7e6f7e045fb1913f73166dbcde3af5ff1eab03e443614d` |
| mac_headless_media.json | `762c3845566a42e9c701127c4ae9438af8b52ef8763388e97c3b900ba1f1bd56` |
| mac_media_probe.py | `df1ecc45d14073e839f630ed81b1373d63988be2a219ecb7b8a7e40ded353b91` |
| mac_headless_media.py | `4c31cec9ac2bd0b27b9aa12e028c0f3e7cf0dc3a2e44b5a15c90eefd1b4ed060` |
| server_run3.log | `265b5cbc6f5ed77adc67a5b65f63052a052a07b41c9754df4c2fbe7be1d6489e` |

## 5. 更新後的 HOF 狀態

| HOF | 附錄 1 | 附錄 2 | 理由 |
| --- | --- | --- | --- |
| 03 | BLOCKED | BLOCKED | 機器能驗證的部分在 Mac 上全部 PASS（headless Chrome + HTTP）。仍缺兩項：**Safari** 實測，以及**人眼和人耳確認**（畫面、聲音、拖曳手感）。headless 測試不能算作人工驗收。 |
| 12 | BLOCKED | BLOCKED | macOS Chrome 157 的 H.264/AAC 播放和 seek 已確認。Safari 和 iPhone 裝置還沒測。 |
| 其他 | — | 不變 | — |

**計數：** PASS 3（01、02、04）· FAIL 2（07、09）· BLOCKED 4（03、05、06、12）· NOT_RUN 3（08、10、11）。

新缺陷的狀態：
- **G-13：** 仍是 FAIL（budget 測試在 Python 3.15 下失敗）。
- **G-14：** 仍是 FAIL。現在有素材時會正確回報 267/267，但程式邏輯沒改；素材不見時，還是會出現空清單也判 PASS 的情況。

## 6. 剩下要 Neon 本人確認的項目

1. 用 Safari 打開 `http://127.0.0.1:8765`，播放 IMG_7835，確認有畫面、**有聲音**，然後拖到 0:42 再繼續播放。
2. Safari 的響應式設計模式，切到 iPhone 寬度：☰ 選單、清單、影片都要能用。
3. 用 Chrome 和 Safari 各對一個項目按 Pass/Fail/Defer，重新整理後確認紀錄還在。另外決定要不要清除 `grok-bot-mac-audit` 留下的測試決策。
4. 截圖存到 `~/Higgsfield-Private/evidence/`，回報 `shasum -a 256`。
