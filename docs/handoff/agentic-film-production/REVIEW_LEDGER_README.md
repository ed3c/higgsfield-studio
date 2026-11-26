# review_ledger.csv

欄位：item, reviewer, date, verdict, evidence_path, drive_id, sha256。每次有新的審查結果就**新增一列**；已有的列不改寫，狀態有變也新增一列。
Repo 版：`docs/handoff/agentic-film-production/review_ledger.csv`（不含私有內容）。Drive 私有版：`review_ledger.csv` id `1M4fbqyeIk15ZCfDOs3WjU5jpXI8XBoNO`（AFP 私有資料夾，只有 owner 可存取）。兩份內容相同；更新時先 commit repo 版，再用 Drive `update_file_content` 覆蓋同一個 file id。
