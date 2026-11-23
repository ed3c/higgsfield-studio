# 上游來源

本目錄的 `vendor/higgsfield-ai-skills/` 是官方技能庫的完整快照，不是 git submodule。

| 項目 | 內容 |
| --- | --- |
| 上游 | https://github.com/higgsfield-ai/skills |
| 授權 | MIT License。Copyright (c) 2026 Higgsfield AI |
| 授權全文 | [vendor/higgsfield-ai-skills/LICENSE](vendor/higgsfield-ai-skills/LICENSE) |
| 版本 | 0.14.0（見上游 `VERSION`） |
| commit | `27000402070db19d958789d05b3b52b6f4718d7c` |
| 納入日期 | 2026-11-21 |
| 檔案數 | 161（不含 `.git`） |

MIT 允許使用、複製、修改與再散布，條件是保留版權聲明與許可聲明。此快照未改上游檔案。不要把 API key、`credentials.json` 或帳號密鑰放進這個目錄。

## 為什麼用快照而不是 submodule

這個倉庫是個人製作環境。clone 之後就要能直接讀 `SKILL.md`，不依賴 `git submodule update`。更新時重新抓上游，整份覆蓋 `vendor/higgsfield-ai-skills/`，再改上表的版本與 commit。

```bash
git clone --depth 1 https://github.com/higgsfield-ai/skills.git /tmp/hf-skills
rm -rf skills/vendor/higgsfield-ai-skills
mkdir -p skills/vendor
cp -a /tmp/hf-skills skills/vendor/higgsfield-ai-skills
rm -rf skills/vendor/higgsfield-ai-skills/.git
```

覆蓋前先看上游 `LICENSE` 是否仍為 MIT。若授權變更，先停下來再決定要不要更新。

## 官方技能與本庫技能怎麼分

上游九個技能負責呼叫 Higgsfield（生成、Soul ID、產品攝影、Brandkit、市集卡片、網站、無臉解說、影片解說相容入口、YouTube 封面）。它們的預設模型偏貴（例如影片預設 Seedance 2.5）。

本庫自己的四個技能在 `skills/` 下一層，負責這位創作者的製作決策：日常再創作、趨勢二創、方法論拆解、草稿到定稿放大。它們約束點數桶與 9:16 短影流程，真正送出生成時改走官方 `higgsfield-generate` 等技能，並先看生成鍵上的點數。

## 社群庫只作參考，不納入

[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) 是社群提示技能庫，最終版 v3.42.0。上游 README 寫明 2026 年 11 月起不再維護（archived），模型規格快照停在 2026-09-26。對方 MIT 只涵蓋其有權授權的貢獻，並指出倉庫內另有第三方材料，見該庫 `THIRD_PARTY_NOTICES.md`。

本庫沒有複製該倉庫的提示詞、模板或規格表。方法論系列若要對照它公開描述過的 MCSLA 結構（Model、Camera、Subject、Look、Action），只把它當名詞表，並用官方 skills 與 `plan/monthly-usage-and-content-strategy.md` 的帳戶估價覆核。模型名稱以當下的 `higgsfield model get` 或生成鍵為準。


## ScrapeCreators — 外部研究來源（非 vendored）

- Repo: https://github.com/ScrapeCreators/social-media-research-skills
- License: MIT (Copyright 2026 ScrapeCreators)，由使用者環境透過 `npx skills add ScrapeCreators/social-media-research-skills` 安裝。
- 本庫只新增自有 `social-creator-intelligence` orchestration，不複製 13 個上游 Skill。
- 上游 Skill 呼叫獨立的 ScrapeCreators API，要求 `SCRAPECREATORS_API_KEY`；執行前釘選上游 commit、審查工具權限、確認 API 定價與配額。不得將 API key、回應中的私人資料或未授權媒體提交。
- 使用範圍是公開帳號、平台基線、留言/字幕與研究候選素材；無 key/配額時保留 NOT_RUN，不能猜數據。

## 圖片逆向 Skill 候選（非 vendored）

- https://github.com/huanmu-team/unimage — 忠實重製與 QC/repair
- https://github.com/Caph-dev/image-style-prompt-reverse-engineer — 可移植的風格提取
- https://github.com/niobium617/prompt-reverse-engineer-skill — 跨模型 Prompt 編譯

只比較讀取到的 Skill 文件架構，尚**未用 Higgsfield 免費圖片完成 A/B**。請查閱 `research/reverse-skill-benchmark/README.md` 與 `manifest.json` 的 NOT_RUN 紀錄。
