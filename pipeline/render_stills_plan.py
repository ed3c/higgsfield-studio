#!/usr/bin/env python3
"""Render a project's stills-plan.json into prompt docs, a browser run sheet and selects.csv.

Outputs (in the project folder): lock-sheets.md, keyframe-prompts.md, run-sheet.md,
run-sheet.csv, and selects.csv (only if it does not exist yet, so picks are never overwritten).
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RUN_FIELDS = ["order", "id", "model", "aspect", "resolution", "refs_to_upload", "filename",
              "filename_2nd", "credits_shown", "status", "note"]


def ref_file(ref: str, by_id: dict[str, dict]) -> str:
    if ref in by_id:
        return by_id[ref]["filename"] + "（或你選中的那張）"
    raise KeyError(f"未知的參考 {ref}")


def second(filename: str) -> str:
    stem, dot, ext = filename.rpartition(".")
    return f"{stem}_2.{ext}"


def render(project: Path) -> dict[str, int]:
    plan = json.loads((project / "stills-plan.json").read_text(encoding="utf-8"))
    items = sorted(plan["items"], key=lambda item: item["order"])
    by_id = {item["id"]: item for item in items}
    out = plan["output_dir"]

    def block(item: dict) -> list[str]:
        refs = [f"`{r}` → `{out}{by_id[r]['filename']}`" for r in item["refs"]]
        lines = [f"## {item['id']}　{item['title']}（{item['kind']}）", "",
                 f"- 模型：{item['model']}　畫幅：{item['aspect']}　{plan['resolution']}",
                 f"- 參考圖：{'；'.join(refs) if refs else '無'}",
                 f"- 檔名：`{out}{item['filename']}`（第二張 `{second(item['filename'])}`）"]
        if item.get("note"):
            lines.append(f"- 備註：{item['note']}")
        lines += ["", "```text", item["prompt"], "```", ""]
        return lines

    lock = ["# 鎖定圖提示詞（角色、場景、道具）", "",
            "先跑這 19 張，後面的關鍵幀要上傳它們當參考。角色與道具用 16:9 三視圖（只當參考，不進成片）；場景用 9:16，與成片同畫幅。", ""]
    shots = ["# 關鍵幀提示詞 S01–S16", "",
             "每鏡一張 `kf`（起始幀）；有運動的鏡頭另有 `ef`（結束幀）。S15 另有一張選做的片名版，是唯一允許出現文字的圖。全部 9:16。", "",
             "風格：PURGA 冷面（低地平線、主體很小、閃電當主光、近乎單色）與 NUREMBERG bleach bypass（冷灰冰藍、只有橘火與藍白光環兩個重點色、正中對稱），出自 `tests/image-prompt-test/style-pack.md` S01、S02、S13 v2、S14 v2。", ""]
    for item in items:
        (lock if item["group"] == "lock" else shots).extend(block(item))
    (project / "lock-sheets.md").write_text("\n".join(lock), encoding="utf-8")
    (project / "keyframe-prompts.md").write_text("\n".join(shots), encoding="utf-8")

    rows = []
    for item in items:
        rows.append({
            "order": item["order"], "id": item["id"], "model": item["model"], "aspect": item["aspect"],
            "resolution": plan["resolution"],
            "refs_to_upload": " | ".join(out + by_id[r]["filename"] for r in item["refs"]),
            "filename": out + item["filename"], "filename_2nd": out + second(item["filename"]),
            "credits_shown": "", "status": "", "note": item.get("note", ""),
        })
    with (project / "run-sheet.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RUN_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    md = ["# 瀏覽器執行表：《過境 CROSSING》免費靜幀", "",
          f"共 {len(items)} 則提示詞，每則一個模型。每則先生 1 張，不合格才生第 2 張，上限 {plan['max_candidates']} 張。",
          f"所以要生成的靜幀是 {len(items)}–{len(items) * plan['max_candidates']} 張。", "",
          "## 規則", "",
          "1. 只在 higgsfield.ai 網站上跑。不要用 MCP、CLI 或 Canvas，那些一律扣點。",
          "2. 每次按生成前看生成鍵：顯示 UNLIMITED 或 0 才按。上傳參考圖之後要再看一次，參考圖可能改變計價。只要顯示任何點數就停下，在 `credits_shown` 填數字、`status` 填 `blocked`。",
          f"3. 解析度 {plan['resolution']}；畫幅照下表。",
          "4. 參考圖欄寫的是之前已存下的檔名；若當時選了第二張，就上傳 `_2` 那張。",
          "5. 下載後照「檔名」欄改名，放進專案的 `stills/`（不進 git）。",
          "6. 內容過濾擋下的，`status` 填 `filtered`，改一個詞再試一次；仍被擋就跳過並回報。",
          "7. 跑完把每鏡選中的檔名填進 `selects.csv`。", "",
          "## 順序", "",
          "| # | id | 模型 | 畫幅 | 上傳參考 | 檔名 |", "| ---: | --- | --- | --- | --- | --- |"]
    for row in rows:
        md.append(f"| {row['order']} | {row['id']} | {row['model']} | {row['aspect']} | "
                  f"{row['refs_to_upload'].replace(' | ', '<br>') or '—'} | `{row['filename']}` |")
    md += ["", "提示詞全文：鎖定圖在 `lock-sheets.md`，關鍵幀在 `keyframe-prompts.md`。機器可讀版是 `run-sheet.csv`。"]
    (project / "run-sheet.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    selects = project / "selects.csv"
    if not selects.exists():
        with selects.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["shot_id", "keyframe", "endframe"])
            shot_ids = sorted({item["title"] for item in items if item["group"] == "shot"})
            for shot in shot_ids:
                kf = by_id.get(f"{shot}_kf")
                ef = by_id.get(f"{shot}_ef")
                writer.writerow([shot, out + kf["filename"] if kf else "", out + ef["filename"] if ef else ""])
    return {"prompts": len(items), "lock": sum(i["group"] == "lock" for i in items),
            "shot": sum(i["group"] == "shot" for i in items)}


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("projects/2026-11-proof-trailer")
    print(render(target))
