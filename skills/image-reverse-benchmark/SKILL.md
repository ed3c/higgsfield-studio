---
name: image-reverse-benchmark
description: |
  比較 Image-to-Prompt 逆向 Skills；僅可使用已在 Higgsfield 網站 UI 確認為 0 Credits 的 Unlimited 模型進行盲測。
  Use when: image prompt reverse benchmark, @tupacabra style, reverse skill A/B, Higgsfield website Unlimited benchmark.
  NOT for: MCP/API/CLI 生成、未確認免費權益就扣 Credits、無實際生成證據便宣告冠軍。
---

# Image Reverse Skill Benchmark — v2 entrypoint

**Owner:** Image Research Manager
**Consumers:** Film Director Manager, Prompt Compiler, Style Bible Manager
**Oracle:** [v2 完整規格](../../research/reverse-skill-benchmark/v2/BENCHMARK_SPEC_V2.md) + [manifest](../../research/reverse-skill-benchmark/v2/manifest_v2.json) + [validate_spec.py](../../research/reverse-skill-benchmark/v2/validate_spec.py)

## Workflow

1. 閱讀完整的 v2 spec、manifest、EXECUTION_PROMPT；先執行 `python3 research/reverse-skill-benchmark/v2/validate_spec.py`。
2. Source Gate：3 張合法可供研究的圖片（portrait/environment/prop-action），記來源、權利範圍與 SHA256。由 `social-creator-intelligence` 提供研究候選或合法預先選定參考。
3. Entitlement Gate：**只允許 higgsfield.ai 網站的普通生圖 UI**，逐次確認 GPT Image 2.6 Unlimited、1K、16:9、開關 ON、送出費用 0 Credits、生成後餘額未減。使用者 2026-11-20 截圖的日期欄位語義未確認；**2026-11-23 的有效權益目前 NOT_VERIFIED**。
4. 對三種候選 `huanmu-team/unimage`、`Caph-dev/image-style-prompt-reverse-engineer`、`niobium617/prompt-reverse-engineer-skill` 做版本/授權與執行腳本審查，釘選 commit。各自輸出固定 prompt，不得先看生成結果後改 prompt。
5. P1 `reconstruction`：3 cases × 3 Skills × 2 replicates = **18 images**；無 I2I 參考圖進入網站生成。2 位盲評者對所有取次獨立評分，不能挑最好看的。
6. P2 `style_transfer`：3 cases × **Caph + P1 最佳合格非 Caph** × 2 replicates = **12 images**。第二階段是選拔後兩強賽，不能宣稱未入選者在風格遷移上落敗。原創替換主體必須在 P1 前預先固定。
7. 視覺品質、hard fails、成本、來源、Prompt/生成圖哈希、意見分歧與模型限制全部入報告。無法達成 gates，維持 `NOT_RUN` 或 `PARTIAL_*`，不得有假分數或冠軍。

## Fail Closed / No Extra Spend

- 預算上限：**0 額外 Higgsfield Credits**，第三方付費 API 禁用。
- MCP/CLI/API/Canvas/Marketing Studio/Supercomputer 的模型試算和免費次數**不是**網站 Unlimited 權益證據；不要從網站改走這些介面。
- 網站過期、不提供 0-credit 路徑、或出現付費模式選項時：立即停止，不自動付款或重試。
- 不把媒體原檔、用戶 Session、Cookie、身份資訊、帳單截圖放入 Git；僅在 Git 保留已脫敏的來源證據及其哈希。
- 遵守 `budget/track.py` 的 80% 閘門與既有製片規則。v1 原始資料保留在 `research/reverse-skill-benchmark/`。

## Commands / deliverables

```bash
python3 research/reverse-skill-benchmark/v2/validate_spec.py
```

原始 template 在 `research/reverse-skill-benchmark/v2/`。完整影像生成要由有合法來源圖片與可操作網站 session 的 Agent 依 `EXECUTION_PROMPT.md` 執行；**這份 Spec/Lint 不是已完成的 30 張視覺 Benchmark**。
