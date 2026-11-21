# 瀏覽器執行表：《過境 CROSSING》免費靜幀

共 41 則提示詞，每則一個模型。每則先生 1 張，不合格才生第 2 張，上限 2 張。
所以要生成的靜幀是 41–82 張。

## 規則

1. 只在 higgsfield.ai 網站上跑。不要用 MCP、CLI 或 Canvas，那些一律扣點。
2. 每次按生成前看生成鍵：顯示 UNLIMITED 或 0 才按。上傳參考圖之後要再看一次，參考圖可能改變計價。只要顯示任何點數就停下，在 `credits_shown` 填數字、`status` 填 `blocked`。
3. 解析度 2K；畫幅照下表。
4. 參考圖欄寫的是之前已存下的檔名；若當時選了第二張，就上傳 `_2` 那張。
5. 下載後照「檔名」欄改名，放進專案的 `stills/`（不進 git）。
6. 內容過濾擋下的，`status` 填 `filtered`，改一個詞再試一次；仍被擋就跳過並回報。
7. 跑完把每鏡選中的檔名填進 `selects.csv`。

## 順序

| # | id | 模型 | 畫幅 | 上傳參考 | 檔名 |
| ---: | --- | --- | --- | --- | --- |
| 1 | C01 | Nano Banana Pro | 16:9 | — | `stills/CR_C01_lock_nbpro.png` |
| 2 | C02 | Nano Banana Pro | 16:9 | — | `stills/CR_C02_lock_nbpro.png` |
| 3 | C03 | Nano Banana Pro | 16:9 | — | `stills/CR_C03_lock_nbpro.png` |
| 4 | C04 | GPT Image 2.6 Flare | 16:9 | — | `stills/CR_C04_lock_flare.png` |
| 5 | C05 | GPT Image 2.6 Flare | 16:9 | — | `stills/CR_C05_lock_flare.png` |
| 6 | L01 | Seedream 5.0 Pro | 9:16 | — | `stills/CR_L01_lock_seedream.png` |
| 7 | L02 | GPT Image 2.6 Flare | 9:16 | — | `stills/CR_L02_lock_flare.png` |
| 8 | L03 | GPT Image 2.6 Flare | 9:16 | stills/CR_L02_lock_flare.png | `stills/CR_L03_lock_flare.png` |
| 9 | L04 | Seedream 5.0 Pro | 9:16 | — | `stills/CR_L04_lock_seedream.png` |
| 10 | L05 | GPT Image 2.6 Flare | 9:16 | — | `stills/CR_L05_lock_flare.png` |
| 11 | L06 | Nano Banana Pro | 9:16 | — | `stills/CR_L06_lock_nbpro.png` |
| 12 | L07 | Seedream 5.0 Pro | 9:16 | — | `stills/CR_L07_lock_seedream.png` |
| 13 | L08 | Nano Banana Pro | 9:16 | — | `stills/CR_L08_lock_nbpro.png` |
| 14 | P01 | Nano Banana Pro | 16:9 | — | `stills/CR_P01_lock_nbpro.png` |
| 15 | P02 | Seedream 5.0 Pro | 16:9 | — | `stills/CR_P02_lock_seedream.png` |
| 16 | P03 | GPT Image 2.6 Flare | 16:9 | — | `stills/CR_P03_lock_flare.png` |
| 17 | P04 | GPT Image 2.6 Flare | 16:9 | — | `stills/CR_P04_lock_flare.png` |
| 18 | P05 | Seedream 5.0 Pro | 16:9 | — | `stills/CR_P05_lock_seedream.png` |
| 19 | P06 | Nano Banana Pro | 16:9 | — | `stills/CR_P06_lock_nbpro.png` |
| 20 | S01_kf | Seedream 5.0 Pro | 9:16 | stills/CR_L01_lock_seedream.png<br>stills/CR_P01_lock_nbpro.png | `stills/CR_S01_kf_seedream.png` |
| 21 | S02_kf | Nano Banana Pro | 9:16 | stills/CR_C02_lock_nbpro.png<br>stills/CR_L01_lock_seedream.png<br>stills/CR_P01_lock_nbpro.png | `stills/CR_S02_kf_nbpro.png` |
| 22 | S03_kf | Seedream 5.0 Pro | 9:16 | stills/CR_L04_lock_seedream.png<br>stills/CR_P02_lock_seedream.png | `stills/CR_S03_kf_seedream.png` |
| 23 | S04_kf | GPT Image 2.6 Flare | 9:16 | stills/CR_C01_lock_nbpro.png<br>stills/CR_L02_lock_flare.png | `stills/CR_S04_kf_flare.png` |
| 24 | S04_ef | GPT Image 2.6 Flare | 9:16 | stills/CR_C01_lock_nbpro.png<br>stills/CR_S04_kf_flare.png | `stills/CR_S04_ef_flare.png` |
| 25 | S05_kf | GPT Image 2.6 Flare | 9:16 | stills/CR_C03_lock_nbpro.png<br>stills/CR_L05_lock_flare.png | `stills/CR_S05_kf_flare.png` |
| 26 | S06_kf | GPT Image 2.6 Flare | 9:16 | stills/CR_C05_lock_flare.png<br>stills/CR_L05_lock_flare.png<br>stills/CR_P04_lock_flare.png | `stills/CR_S06_kf_flare.png` |
| 27 | S07_kf | GPT Image 2.6 Flare | 9:16 | stills/CR_C03_lock_nbpro.png<br>stills/CR_P04_lock_flare.png | `stills/CR_S07_kf_flare.png` |
| 28 | S08_kf | Nano Banana Pro | 9:16 | stills/CR_L06_lock_nbpro.png<br>stills/CR_P06_lock_nbpro.png | `stills/CR_S08_kf_nbpro.png` |
| 29 | S09_kf | Nano Banana Pro | 9:16 | stills/CR_C01_lock_nbpro.png<br>stills/CR_C02_lock_nbpro.png<br>stills/CR_L02_lock_flare.png<br>stills/CR_P03_lock_flare.png | `stills/CR_S09_kf_nbpro.png` |
| 30 | S10_kf | GPT Image 2.6 Flare | 9:16 | stills/CR_C04_lock_flare.png<br>stills/CR_L03_lock_flare.png<br>stills/CR_P03_lock_flare.png | `stills/CR_S10_kf_flare.png` |
| 31 | S11_kf | Seedream 5.0 Pro | 9:16 | stills/CR_L01_lock_seedream.png<br>stills/CR_P01_lock_nbpro.png<br>stills/CR_C02_lock_nbpro.png | `stills/CR_S11_kf_seedream.png` |
| 32 | S11_ef | Seedream 5.0 Pro | 9:16 | stills/CR_S11_kf_seedream.png<br>stills/CR_P01_lock_nbpro.png | `stills/CR_S11_ef_seedream.png` |
| 33 | S12_kf | Seedream 5.0 Pro | 9:16 | stills/CR_L07_lock_seedream.png<br>stills/CR_P05_lock_seedream.png | `stills/CR_S12_kf_seedream.png` |
| 34 | S12_ef | Seedream 5.0 Pro | 9:16 | stills/CR_S12_kf_seedream.png<br>stills/CR_C04_lock_flare.png<br>stills/CR_P03_lock_flare.png | `stills/CR_S12_ef_seedream.png` |
| 35 | S13_kf | GPT Image 2.6 Flare | 9:16 | stills/CR_C01_lock_nbpro.png<br>stills/CR_C04_lock_flare.png<br>stills/CR_P03_lock_flare.png<br>stills/CR_P04_lock_flare.png | `stills/CR_S13_kf_flare.png` |
| 36 | S13_ef | GPT Image 2.6 Flare | 9:16 | stills/CR_C01_lock_nbpro.png<br>stills/CR_S13_kf_flare.png | `stills/CR_S13_ef_flare.png` |
| 37 | S14_kf | Nano Banana Pro | 9:16 | stills/CR_C02_lock_nbpro.png<br>stills/CR_L01_lock_seedream.png | `stills/CR_S14_kf_nbpro.png` |
| 38 | S14_ef | Nano Banana Pro | 9:16 | stills/CR_C02_lock_nbpro.png<br>stills/CR_S14_kf_nbpro.png | `stills/CR_S14_ef_nbpro.png` |
| 39 | S15_kf | Seedream 5.0 Pro | 9:16 | stills/CR_S12_kf_seedream.png<br>stills/CR_P05_lock_seedream.png | `stills/CR_S15_kf_seedream.png` |
| 40 | S15_title | GPT Image 2.6 Flare | 9:16 | stills/CR_S15_kf_seedream.png | `stills/CR_S15_title_flare.png` |
| 41 | S16_kf | Nano Banana Pro | 9:16 | stills/CR_L08_lock_nbpro.png<br>stills/CR_P01_lock_nbpro.png | `stills/CR_S16_kf_nbpro.png` |

提示詞全文：鎖定圖在 `lock-sheets.md`，關鍵幀在 `keyframe-prompts.md`。機器可讀版是 `run-sheet.csv`。
