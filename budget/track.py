#!/usr/bin/env python3
"""Sum monthly Higgsfield spend per bucket against the Ultra 9,000 allocation."""

from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

BUDGET_DIR = Path(__file__).resolve().parent
DEFAULT_ALLOCATION = BUDGET_DIR / "allocation.csv"
DEFAULT_LEDGER = BUDGET_DIR / "ledger.csv"
TAIPEI = ZoneInfo("Asia/Taipei")
WARN_RATIO = Decimal("0.80")
EXPECTED_TOTAL = Decimal("9000")
EXIT_OK = 0
EXIT_WARN = 2
EXIT_ERROR = 1


@dataclass(frozen=True)
class Bucket:
    bucket_id: str
    label_zh: str
    credits: Decimal
    share: Decimal


@dataclass(frozen=True)
class Spend:
    bucket_id: str
    credits: Decimal
    counted: bool
    reason: str


def parse_decimal(raw: str) -> Decimal:
    return Decimal(raw.strip())


def load_allocation(path: Path) -> list[Bucket]:
    buckets: list[Bucket] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"bucket", "label_zh", "credits", "share"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path} 缺少欄位 {sorted(required)}")
        for row in reader:
            buckets.append(
                Bucket(
                    bucket_id=row["bucket"].strip(),
                    label_zh=row["label_zh"].strip(),
                    credits=parse_decimal(row["credits"]),
                    share=parse_decimal(row["share"]),
                )
            )
    if not buckets:
        raise ValueError(f"{path} 沒有任何桶")
    return buckets


def current_month(now: datetime | None = None) -> str:
    moment = now if now is not None else datetime.now(TAIPEI)
    return moment.strftime("%Y-%m")


def is_refunded(raw: str) -> bool:
    return raw.strip().lower() in {"yes", "y", "true", "1"}


def load_spend(path: Path, month: str) -> tuple[list[Spend], list[str]]:
    spends: list[Spend] = []
    warnings: list[str] = []
    if not path.exists() or path.stat().st_size == 0:
        return spends, warnings
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return spends, warnings
        required = {"date", "bucket", "credits", "refunded"}
        if not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path} 缺少欄位 {sorted(required)}")
        for index, row in enumerate(reader, start=2):
            date = (row.get("date") or "").strip()
            if date == "" and not (row.get("credits") or "").strip():
                continue
            if not date.startswith(month):
                continue
            bucket_id = (row.get("bucket") or "").strip()
            raw_credits = (row.get("credits") or "").strip()
            try:
                credits = parse_decimal(raw_credits)
            except InvalidOperation:
                warnings.append(f"第 {index} 列點數無法解析，已略過：{raw_credits!r}")
                continue
            if is_refunded(row.get("refunded") or ""):
                spends.append(Spend(bucket_id, credits, False, "refunded"))
                continue
            spends.append(Spend(bucket_id, credits, True, "spent"))
    return spends, warnings


@dataclass(frozen=True)
class BucketReport:
    bucket: Bucket
    spent: Decimal

    @property
    def ratio(self) -> Decimal:
        if self.bucket.credits == 0:
            return Decimal("0")
        return self.spent / self.bucket.credits

    @property
    def warns(self) -> bool:
        return self.ratio >= WARN_RATIO


def build_report(
    buckets: list[Bucket], spends: list[Spend]
) -> tuple[list[BucketReport], Decimal, list[str]]:
    notes: list[str] = []
    known = {bucket.bucket_id for bucket in buckets}
    spent_by_bucket = {bucket.bucket_id: Decimal("0") for bucket in buckets}
    unknown = Decimal("0")
    for spend in spends:
        if not spend.counted:
            continue
        if spend.bucket_id not in known:
            unknown += spend.credits
            notes.append(f"未知的桶 {spend.bucket_id}：{spend.credits} 點已計入合計")
            continue
        spent_by_bucket[spend.bucket_id] += spend.credits
    reports = [
        BucketReport(bucket, spent_by_bucket[bucket.bucket_id]) for bucket in buckets
    ]
    total_spent = sum((item.spent for item in reports), Decimal("0")) + unknown
    return reports, total_spent, notes


def display_width(text: str) -> int:
    width = 0
    for char in text:
        width += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
    return width


def pad_right(text: str, width: int) -> str:
    return text + (" " * max(width - display_width(text), 0))


def format_report(
    month: str, reports: list[BucketReport], total_spent: Decimal, notes: list[str]
) -> str:
    lines = [
        f"月份 {month}（Asia/Taipei）",
        f"警戒線 {WARN_RATIO * 100:.0f}%",
        "",
        f"{pad_right('桶', 16)} {'已用':>10} {'分配':>10} {'占比':>8} 狀態",
    ]
    for item in reports:
        status = "警告" if item.warns else "正常"
        percent = (item.ratio * Decimal("100")).quantize(Decimal("0.1"))
        lines.append(
            f"{pad_right(item.bucket.label_zh, 16)} {item.spent:>10} {item.bucket.credits:>10} {percent:>7}% {status}"
        )
    total_ratio = total_spent / EXPECTED_TOTAL
    total_status = "警告" if total_ratio >= WARN_RATIO else "正常"
    total_percent = (total_ratio * Decimal("100")).quantize(Decimal("0.1"))
    lines.append(
        f"{'合計':<16} {total_spent:>10} {EXPECTED_TOTAL:>10} {total_percent:>7}% {total_status}"
    )
    if notes:
        lines.append("")
        lines.extend(notes)
    return "\n".join(lines)


def allocation_problems(buckets: list[Bucket]) -> list[str]:
    problems: list[str] = []
    total = sum((bucket.credits for bucket in buckets), Decimal("0"))
    if total != EXPECTED_TOTAL:
        problems.append(f"分配合計為 {total}，應為 {EXPECTED_TOTAL}")
    share = sum((bucket.share for bucket in buckets), Decimal("0"))
    if share != Decimal("1"):
        problems.append(f"佔比合計為 {share}，應為 1")
    return problems


def should_warn(reports: list[BucketReport], total_spent: Decimal) -> bool:
    if any(item.warns for item in reports):
        return True
    return (total_spent / EXPECTED_TOTAL) >= WARN_RATIO


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="核對 Higgsfield 每月點數桶")
    parser.add_argument("--month", help="YYYY-MM，預設為台北時間的當月")
    parser.add_argument("--allocation", type=Path, default=DEFAULT_ALLOCATION)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="即使達到 80% 也以結束碼 0 離開",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    month = args.month or current_month()
    try:
        buckets = load_allocation(args.allocation)
        problems = allocation_problems(buckets)
        if problems:
            print("\n".join(problems), file=sys.stderr)
            return EXIT_ERROR
        spends, warnings = load_spend(args.ledger, month)
        reports, total_spent, notes = build_report(buckets, spends)
    except (OSError, ValueError, InvalidOperation) as error:
        print(str(error), file=sys.stderr)
        return EXIT_ERROR
    print(format_report(month, reports, total_spent, warnings + notes))
    if should_warn(reports, total_spent) and not args.no_fail:
        print("已達分配額的 80%。停止新增定稿，改查 budget/ledger.csv。", file=sys.stderr)
        return EXIT_WARN
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
