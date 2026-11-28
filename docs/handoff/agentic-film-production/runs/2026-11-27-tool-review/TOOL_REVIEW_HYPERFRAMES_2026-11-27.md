# HyperFrames：pin + 授權／依賴審查（僅審查，不執行）

Owner approval：同 REA-Video（2026-11-27 ~01:37 UTC+8）。Reviewer：Grok Bot（static source read；沒有 npm／bun install、沒有 `npx hyperframes`、沒有登入、沒有遙測）。

## Pin

| 項目 | 值 |
|---|---|
| Repo | https://github.com/heygen-com/hyperframes |
| Pin（審查時 HEAD） | `7c217d9fdf3e32c628953f7325ddd90e0ff94392`（2026-11-26T13:03:08Z = 2026-11-26 21:03 UTC+8） |
| LICENSE | Apache-2.0；blob `ae06b37e1c5116ccfaa615ac25ec1aabf5658d8c`；sha256 `4259155f…b8` |
| CLI package | `@hyperframes/cli` 0.9.99（Apache-2.0）；其他 workspace package 的 package.json 多半沒有寫 license 欄位（以根目錄 LICENSE 為準，需確認） |
| Lockfile | `bun.lock`（約 1,100 個 package）——沒有完整 SBOM；執行前必須產生 SBOM |

## 架構與 handoff 提到的 skills

`skills/`：hyperframes、hyperframes-cli、hyperframes-registry、media-use、reverse-any-video、style-sampling（另有 figma、slideshow、remotion-to-hyperframes）。

| Skill | 觀察 | 判定 |
|---|---|---|
| `/reverse-any-video` | 文件寫明「Reverse is a **HyperFrames Pro feature**」，`reverse start` 會檢查付費方案，拒絕時會給升級連結；目標是**把影片重建成可編輯的 HyperFrames 專案並逐格對照**，會**用 HeyGen 重拍畫面中的人物**，並使用雲端 render | **BLOCK（S1）**：付費＋帳號＋雲端（媒體外傳），而且產出的是衍生重製品，S1 的 rights 排除 derivative；也不符合「零付費」 |
| `/style-sampling` | 同樣是 Pro feature，由伺服器檢查方案；功能是做「新一集」內容 | BLOCK（目前範圍） |
| `/media-use` | 包含 HeyGen 付費 API 流程（`heygen/v3.ts`：Pro feature／billing subscribe） | HOLD |
| CLI `measure probe/cuts/events/frames/energy/look/sync` | 原始碼在 `packages/cli/src/commands/measure/*`，在本機呼叫 ffmpeg；measure 原始碼中**沒有看到 Pro／billing 檢查** | **ALLOW-CANDIDATE**：只限 measure，離線執行，並先關閉遙測 |

## 依賴與第三方

| 項目 | 授權 | 判定 |
|---|---|---|
| puppeteer-core + `@puppeteer/browsers` | Apache-2.0；**執行時會下載 Chromium**（BSD＋各種第三方） | HOLD（render 才需要；measure 不需要） |
| sharp（optional）+ `@img/sharp-libvips` | Apache-2.0 / **LGPL-3.0**（libvips 預編譯檔） | HOLD（copyleft binary） |
| mediabunny | **MPL-2.0**（CREDITS.md） | HOLD（weak copyleft，studio 使用） |
| GSAP（core 有 gsap-cdn 入口） | GSAP 自有的「Standard No Charge」授權，**不是 OSI** | HOLD（不能放進 core） |
| Parakeet TDT 0.6B v3（`models install parakeet`） | **CC-BY-4.0** 權重 | HOLD（S1 不需要） |
| ffmpeg（系統） | Q01 | ALLOW（Q01） |

## 網路、遙測、安裝 hook

- **遙測預設開啟**：`packages/cli/src/telemetry/*` 使用 PostHog，有 `showTelemetryNotice`、可在 config 關閉（`telemetryEnabled`）；skills 也要求在開始時跑 `npx hyperframes events --skill=…` beacon（可以拒絕）。對 S1：**必須先關閉遙測，也不能跑 beacon**。
- `auth`、`billing`、`cloud render`、`share` 都會連到 HeyGen 服務 → BLOCK（S1）。
- Workspace 的 package.json 沒有 `preinstall/postinstall` script（已逐一檢查 16 個 package）；但 bun install 會從 registry 抓約 1,100 個 package → 要先產生 SBOM。

## 結論（scoped）

| 範圍 | 判定 |
|---|---|
| HyperFrames reverse-any-video／style-sampling（Pro、HeyGen、雲端、衍生重製） | **BLOCK** for S1（付費＋外傳＋衍生物） |
| `hyperframes measure *`（本機 ffmpeg），在關閉遙測、離線、不登入的條件下 | **ALLOW-CANDIDATE**：可以作為 §10 step 2「HyperFrames reverse」比較的最小可行替代；但這**不等於** handoff 所說的 HyperFrames reverse skill，報告中要標清楚 |
| Render／Chromium／sharp／GSAP／mediabunny | HOLD |

執行前還需要：Neon 核准 measure-only 範圍、產生 bun.lock 的 SBOM 並逐項確認授權、設定好遙測關閉、斷網執行。
