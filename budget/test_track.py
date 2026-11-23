"""Tests for the monthly credit tracker."""

from __future__ import annotations

import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_cost_table import export_table
from track import (
    EXIT_WARN,
    Bucket,
    Spend,
    build_report,
    load_allocation,
    load_spend,
    main,
    should_warn,
)


class TrackTests(unittest.TestCase):
    def test_allocation_sums_to_nine_thousand(self) -> None:
        buckets = load_allocation(Path(__file__).resolve().parent / "allocation.csv")
        total = sum((bucket.credits for bucket in buckets), Decimal("0"))
        self.assertEqual(total, Decimal("9000"))

    def test_refunded_rows_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.csv"
            ledger.write_text(
                "date,bucket,credits,refunded\n"
                "2026-11-02,trends,7.5,no\n"
                "2026-11-03,trends,35,yes\n"
                "2026-12-01,trends,100,no\n",
                encoding="utf-8",
            )
            spends, warnings = load_spend(ledger, "2026-11")
        self.assertEqual(warnings, [])
        counted = [item for item in spends if item.counted]
        self.assertEqual(len(counted), 1)
        self.assertEqual(counted[0].credits, Decimal("7.5"))

    def test_warns_at_eighty_percent_of_a_bucket(self) -> None:
        buckets = [
            Bucket("trends", "趨勢二創", Decimal("100"), Decimal("1")),
        ]
        spends = [Spend("trends", Decimal("80"), True, "spent")]
        reports, total, notes = build_report(buckets, spends)
        self.assertEqual(notes, [])
        self.assertTrue(reports[0].warns)
        self.assertEqual(total, Decimal("80"))
        self.assertTrue(should_warn(reports, total))

    def test_main_warns_at_eighty_percent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.csv"
            ledger.write_text(
                "date,bucket,credits,refunded\n2026-11-02,trends,1584,no\n",
                encoding="utf-8",
            )
            allocation = Path(__file__).resolve().parent / "allocation.csv"
            code = main(
                [
                    "--month",
                    "2026-11",
                    "--allocation",
                    str(allocation),
                    "--ledger",
                    str(ledger),
                ]
            )
        self.assertEqual(code, EXIT_WARN)

    def test_cost_table_matches_plan_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "cost-table.csv"
            count = export_table(
                Path(__file__).resolve().parents[1] / "plan" / "monthly-usage-and-content-strategy.md",
                output,
            )
        self.assertEqual(count, 66)

    def test_unknown_bucket_counts_toward_total(self) -> None:
        buckets = [Bucket("rnd", "實驗研發", Decimal("630"), Decimal("0.07"))]
        spends = [Spend("nope", Decimal("10"), True, "spent")]
        _reports, total, notes = build_report(buckets, spends)
        self.assertEqual(total, Decimal("10"))
        self.assertEqual(len(notes), 1)

    def test_help_text_renders_on_strict_argparse(self) -> None:
        # Python 3.14+/3.15 argparse validates %-formatting in help strings (G-13).
        import contextlib, io
        import track
        out = io.StringIO()
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(out):
            track.parse_args(["--help"])
        self.assertIn("80%", out.getvalue())

if __name__ == "__main__":
    unittest.main()
