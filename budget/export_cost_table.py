#!/usr/bin/env python3
"""Turn the plan's credit tables into budget/cost-table.csv."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

BUDGET_DIR = Path(__file__).resolve().parent
PLAN = BUDGET_DIR.parent / "plan" / "monthly-usage-and-content-strategy.md"
OUTPUT = BUDGET_DIR / "cost-table.csv"

SECTIONS = {
    "圖像": "image",
    "影片": "video",
    "對口型、語音與後製": "audio-lipsync-post",
}

SOURCE_MAP = {
    "帳戶估價": "account-estimate",
    "官方頁面": "official-page",
    "估計": "estimate",
}


def section_rows(markdown: str, heading: str) -> list[list[str]]:
    marker = f"### {heading}\n"
    start = markdown.find(marker)
    if start < 0:
        raise ValueError(f"找不到小節 {heading}")
    rest = markdown[start + len(marker) :]
    next_heading = re.search(r"\n#{1,6} ", rest)
    block = rest[: next_heading.start()] if next_heading else rest
    rows: list[list[str]] = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"模型", "---"} or set(cells[0]) <= {"-"}:
            continue
        if all(set(cell) <= {"-", ":"} or cell == "" for cell in cells):
            continue
        if len(cells) != 4:
            raise ValueError(f"{heading} 的欄位數不是 4：{line}")
        rows.append(cells)
    if not rows:
        raise ValueError(f"{heading} 沒有資料列")
    return rows


def numeric_credits(raw: str) -> str:
    cleaned = raw.replace("約", "").strip()
    if re.fullmatch(r"\d+(\.\d+)?", cleaned):
        return cleaned
    return ""


def export_table(plan_path: Path, output_path: Path) -> int:
    markdown = plan_path.read_text(encoding="utf-8")
    written = 0
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "category",
                "model",
                "settings",
                "credits_raw",
                "credits_numeric",
                "source",
                "source_note",
                "plan",
            ],
        )
        writer.writeheader()
        for heading, category in SECTIONS.items():
            for model, settings, credits, source_zh in section_rows(markdown, heading):
                source = SOURCE_MAP.get(source_zh, "unknown")
                writer.writerow(
                    {
                        "category": category,
                        "model": model,
                        "settings": settings,
                        "credits_raw": credits,
                        "credits_numeric": numeric_credits(credits),
                        "source": source,
                        "source_note": source_zh,
                        "plan": "plan/monthly-usage-and-content-strategy.md",
                    }
                )
                written += 1
    return written


def main() -> int:
    count = export_table(PLAN, OUTPUT)
    print(f"wrote {count} rows to {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
