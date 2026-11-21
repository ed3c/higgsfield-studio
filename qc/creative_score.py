#!/usr/bin/env python3
"""Score the six equal-weight creative criteria: pass if average >= 8 and every item >= 7."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CRITERIA = ("directing", "visual", "art_direction", "sound", "editing", "originality")
AVERAGE_MIN = 8.0
ITEM_MIN = 7.0


def evaluate(scores: dict) -> dict:
    problems: list[str] = []
    values: list[float] = []
    for key in CRITERIA:
        if key not in scores:
            problems.append(f"缺少 {key}")
            continue
        value = float(scores[key])
        if not 1 <= value <= 10:
            problems.append(f"{key} 必須在 1–10")
        if value < ITEM_MIN:
            problems.append(f"{key} = {value:g}，低於 {ITEM_MIN:g}")
        values.append(value)
    average = sum(values) / len(values) if values else 0.0
    if values and average < AVERAGE_MIN:
        problems.append(f"平均 {average:.2f}，低於 {AVERAGE_MIN:g}")
    return {"average": round(average, 2), "pass": not problems, "problems": problems}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("用法：creative_score.py qc-report.json", file=sys.stderr)
        return 1
    report = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    result = evaluate(report.get("creative", report))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
