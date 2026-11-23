---
name: image-reverse-benchmark
description: |
  用相同參考圖片與 Higgsfield 圖像模型比較 image-to-prompt 逆向 Skills，保留生成證據、成本與盲評。
  Use when: image prompt reverse benchmark, @tupacabra style, reverse skill A/B, Higgsfield free image test.
  NOT for: 沒有免費額度時動用付費 credits、只看 README 就宣稱勝者、逐鏡複製受保護作品。
---

# Image Reverse Skill Benchmark

Owner: Image Research Manager。Consumer: Film Director Manager / Prompt Compiler。Oracle: 相同 reference、同模型、可查看的原圖/生成圖、獨立評分者及真實 cost/job id。

## 待比 Skills

- **Unimage** (https://github.com/huanmu-team/unimage): 忠實重製、空間關係、QC/repair；先停在首次 prompt，不准讓內建 loop 額外生成而污染 A/B。
- **Caph-dev/image-style-prompt-reverse-engineer** (https://github.com/Caph-dev/image-style-prompt-reverse-engineer): 風格提取與換主體；不要把去除主體資訊誤判為忠實重製的缺點。
- **niobium617/prompt-reverse-engineer-skill** (https://github.com/niobium617/prompt-reverse-engineer-skill): 多模型 prompt 編譯；必須產出相同目標 Higgsfield 模型的純文字 prompt。

以上為**候選**，不是測試結果。逐個檢查最新 commit、license、執行腳本與額外付費服務。

## 同條件 A/B（兩項任務分開）

1. `reconstruction`：每個候選對完全相同的 reference 產出一次初稿 prompt；都使用固定的 Higgsfield 模型、16:9、1K，**不把原始圖作為生成 reference**，避免以 image-to-image 隱藏 Prompt 差異。
2. `style_transfer`：每個候選提取同張 reference 的美學規則，再套入事先固定的**另一個原創題材**，測試跨題材保真。不能把原圖角色/文字/商標直接帶入。
3. 每任務至少三張不同場景的已授權 reference。每個 `case × skill` 至少兩個生成取次，再由兩位盲評者各自打分；模型若不支援 seed，就記錄不可重現來源。
4. 預先鎖定輸入圖 SHA256、Skill commit、Prompt JSON、模型、版本、解析度、畫幅、生成 job_id、cost/免費來源與輸出檔 SHA256。所有生成圖放 `projects/*/refs/` 或庫外，**不入 Git**。
5. 評分六維：composition、lighting、palette、detail、artifact_control、task_success（0–5）；在相同 case 比配對結果。將人物一致性/原創性等導演判斷另列不合格規則，不能平均掩蓋。
6. 不使用參考圖進行生成後修補直到第一輪盲測完成。第二輪 repair 效果是獨立試驗。

## Credit gate — 不可繞過

- 必須先查 Higgsfield 帳戶當下的 `free_trial.unlim_available`、`free_gens`、目標模型的 `supports_unlim` / `supports_free_gens`，**確認該圖片請求真的可以 0-credit 送出**。
- 免費權益缺失、只限影片/Genjutsu、生成 API 仍要付點、或平台回傳 credit/unlim choice 時，寫 **NOT_RUN / FREE_IMAGE_NOT_AVAILABLE**。不得自行從普通 Credits 付款，亦不得將「Ultra 訂閱 credits」稱為免費。
- 真正執行前再比對成本預估與用戶授權；`budget/track.py` 達 80% 停損亦生效。免費與付費成本分別記錄。
- API key、cookies、session 不得寫入 Git。

## 驗收

`research/reverse-skill-benchmark/manifest.json` 是固定測試規格；`ratings.csv` 沒有真實已驗證結果時，輸出僅為 `NOT_RUN`，**不得產生分數或 winner**。

只有全部相同 case 同模型/畫幅/解析度、兩個取次、兩名盲評者評分完成，才允許選出對應任務的優勝 Skill；若各自勝出不同任務，採用串接而不是一個總冠軍。
