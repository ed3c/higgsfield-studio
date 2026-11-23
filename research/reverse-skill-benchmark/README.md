# Image Reverse Benchmark — @tupacabra

**狀態：NOT_RUN (2026-11-23)。** 這不是已完成的 Higgsfield 圖片品質對照。

## 當前阻擋

2026-11-23 讀取目前 Higgsfield 連接的工作區：Ultra、普通 Credits 9,010、`free_trial.unlim_available=false`；`free_gens` 有 4 次但限制在動作/物件替換等影片功能，**沒有可用的免費一般圖片生成**。

當時對 `cinematic_studio_2_5` / `nano_banana_pro` 以 16:9、1K、單張詢價，各為 **2 credits/image**（浮動價，正式執行前重查）。本任務要求「免費圖片」，所以**沒有送出任何生成 job，沒有 A/B 視覺成績，沒有扣 Credits**。不可用 Ultra 方案已付費 Credits 假冒免費。

## 實驗矩陣

| 任務 | 圖片案例 | 候選 Skills | 嚴格控制 |
| --- | --- | --- | --- |
| reconstruction | 3 張不同的電影劇照（待合法取得） | unimage / Caph / niobium617 | 固定相同原圖、模型、畫幅/解析度、無 I2I reference |
| style_transfer | 同 3 張 + 固定原創替換主體 | unimage / Caph / niobium617 | 固定主體、模型、畫幅/解析度；不用原圖主體 |
| repair（第二階段） | 第一階段失敗案例 | unimage 與可比較修補方案 | 單獨統計額外生成數和成本，不參與初稿 A/B |

對每個 case/skill 兩次 render，兩位盲評者。6 個標準：composition、lighting、palette、detail、artifact_control、task_success，評 0–5。報告每個 case 的均值、失敗數、每張圖成本與完成率；配對不足不排名。小樣本是方向性證據，不應視為公開 leaderboard。

最小第一階段 = 2 task × 3 cases × 3 skills × 2 generations = **36 images**；以當時單價估算 72 credits，**不是免費**。免費額度不足時維持 NOT_RUN。

## 來源與安全

- 研究對象： https://x.com/tupacabra 。
- 資料研究： https://github.com/ScrapeCreators/social-media-research-skills 。
- 逆向候選： https://github.com/huanmu-team/unimage 、https://github.com/Caph-dev/image-style-prompt-reverse-engineer 、https://github.com/niobium617/prompt-reverse-engineer-skill 。
- 本倉庫原本就規定不將原始影片/影像或生成成品放 Git；保留來源 URL、必要的 SHA256、授權註記與可稽核的參數。
- 缺來源素材、權利範圍、免費額度、可用模型或一致的設定，均屬 NOT_RUN，不得靠語言模型幻想出比較成果。

## 重新開跑條件

1. 在當下工作區核對免費權益確實涵蓋目標 image model，並確認 count/期限；若不足 **36 張**，縮小 sample 必須另報低信心，不能稱完整試驗。
2. 對 3 張可合法做研究的劇照進行 SHA256 固定；取得同一套原圖輸入每個 Skill。
3. 固定 Higgsfield 的 model、aspect_ratio、resolution，保留各 Skill 原始輸出 prompt。
4. 只有官方確認 0-credit 的免費生成路徑才進入生成；否則停止而非改花 Ultra Credits。
5. 完成盲評後新增 `run-YYYY-MM-DD.md` 真實結果；不能修改這份歷史 NOT_RUN 記錄來掩蓋初次阻擋。
