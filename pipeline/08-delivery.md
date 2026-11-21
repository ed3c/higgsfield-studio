# 08 交付

平台規格：[../delivery/specs.md](../delivery/specs.md)，機器可讀版 [../delivery/profiles.json](../delivery/profiles.json)。

## 產出
`delivery.md`：每個平台檔的檔名、`mech_check.py` 結果、字幕、封面、來源紀錄（每鏡的 generation id 對到 `takes.csv`）。

## 門檻
- 每個平台檔都通過 `qc/mech_check.py --profile <平台>`。
- 發布到任何公開平台前，要 Neon 明確同意。
