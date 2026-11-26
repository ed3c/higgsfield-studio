# Entry Point Readiness（t37u §5）— 2026-11-26

五個層次分開判：L1 規格已定義、L2 工具已存在、L3 實際接線、L4 Native Execution、L5 Independent Acceptance。空殼入口、Mock、單元測試都不算 L4/L5。查核地點是 Grok Bot box（不含 Neon 的 Mac）。「分支」指尚未合併 main 的既有分支。

| 能力 | L1 規格 | L2 工具 | L3 接線 | L4 Native | L5 獨立驗收 | 證據 |
|---|---|---|---|---|---|---|
| Source Ingestion | ✅ §3、§13 | ✅ yt-dlp 2026.10.26、ffmpeg 7.1.5；❌ yt-dlp-ejs/Deno、pytubefix、Whisper | ⚠️ 只有驗收端：`studio/source/yt_gates.py` | ❌ BLOCKED（S1 YT0 權利）| ❌ NOT_RUN | YT_S1_ACQUISITION_2026-11-26.md |
| Full Project Import | ✅ §4、§14 | ✅ `studio/importer/`（本 PR 新增）+ schema | ✅ Higgsfield publication HTML、本機 export、第三方 supplemental 三個 adapter | ⚠️ PARTIAL：跑在真實公開 Passport Rush HTML 上，只拿到 publication record | ❌ NOT_RUN（缺獨立 Oracle 與完整 inventory）| PASSPORT_RUSH_S5_2026-11-26.md |
| License Audit | ✅ §5、Soodles 安裝來源.md | ⚠️ 只有文字政策；沒有 SBOM／授權掃描工具 | ❌ | ❌ NOT_RUN（本輪只記 yt-dlp、pytubefix、FFmpeg 授權事實）| ❌ | READBACK §3 H12 |
| Film／Artwork／Project Reverse | ✅ §4 | ⚠️ main：`skills/image-reverse-benchmark`（圖片）；REA-Video、HyperFrames 等未安裝 | ❌ | ❌ NOT_RUN（無來源位元組）| ❌ | §5 候選表 |
| Methodology Distillation | ✅ §5、統一蒸餾架構 | ⚠️ main：`skills/methodology-breakdown`（文字）；Sybil 等未安裝 | ❌ | ❌ NOT_RUN | ❌ | Soodles @939875f |
| Skill Registry／Capability Router | ✅ §5、HF-Q04 | ❌ 無實作 | ❌ | ❌ | ❌ | — |
| Independent Blind Evals | ✅ §8 BENCHMARK_SPEC_V2 | ✅ `validate_spec.py`（main）；`compute_p1_scores.py`（box/PR #8）| ✅ P1 流程跑過 | ✅ P1 18 張實際評分 | ⚠️ INCONCLUSIVE：差 0.104 < 0.25；評審是兩個 agent，不是 §8 要求的兩位人類（GAP-EVAL-01）| PR #8；§8 |
| Elements／Blender Previs | ✅ §6 | ⚠️ Higgsfield MCP `elements_*` 在目錄；J4 `build_previs.py`/`verify_previs.py` 在 PR #9 archive；❌ box 無 Blender | ❌ | ❌ NOT_RUN | ❌ | `which blender` = none |
| Shot IR／Prompt Compiler | ✅ §6 | ⚠️ 分支：`schemas/higgsfield-shot-ir.v1.schema.json`、industrial-pipeline `schemas/shot-ir.schema.json`、PR #3 art-mechanism compiler | ⚠️ 僅在 J4 分支內 | ❌ 本契約 NOT_RUN | ❌ | `git diff origin/main...<branch>` |
| Codex CLI／Google Antigravity | ✅ §7 | ❌ box 上都沒有（`which codex/antigravity` = none）| ❌ | ❌ BLOCKED（只在 Mac；依 t25u 不在 Mac 操作）| ❌ | — |
| Google Colab／Higgsfield GPU | ✅ §7 | ⚠️ Higgsfield MCP 有 `gpu_my`/`gpu_rental_*`；Colab 無連接器 | ❌ | ❌ BLOCKED_BUDGET（沒有核准預算）| ❌ | — |
| MAGI-2／其他 Provider Adapters | ✅ §7 | ⚠️ Higgsfield MCP 目錄（先前 models_search 讀過 magi_2 參數）| ❌ 無 adapter | ❌ BLOCKED_BUDGET | ❌ | §7 |
| Editorial／Post-production | ✅ §6 | ⚠️ ffmpeg 有；❌ OpenTimelineIO、HyperFrames 未安裝；industrial-pipeline `build_animatic.py`（分支）| ❌ | ❌ NOT_RUN | ❌ | `import opentimelineio` 失敗 |
| Medium Compiler 本地可播放驗收 | ✅ §6 | ✅ ed3c/medium-compiler（main `6235a90`，public）| ❌ 未整合 | ❌ NOT_RUN | ❌ | gh api |

## 本輪新增的入口

只針對具名缺口新增兩個：
1. Full Project Import（§14 要求的 generic `FullProjectImporter`，原本不存在）。
2. YT0–YT4 獨立 verifier（§13 要求的獨立驗收，原本不存在）。

沒有新增 Manager、scheduler、Gateway、MCP server 或 GUI。Studio 的 gate/handoff 狀態仍歸 `studio_factory`（PR #1/#9，未合併 main）。
