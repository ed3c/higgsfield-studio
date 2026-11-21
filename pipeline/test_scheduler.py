import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scheduler as s  # noqa: E402

COST_TABLE = "model,settings,credits_raw,credits_numeric\nCinema Studio 4.0,5 秒，720p,35,35\nSoul ID 訓練,一次性,25,25\n"


def make_project(root: Path, budget: int = 200, cap: int = 9000) -> Path:
    project = root / "film"
    project.mkdir()
    (project / "project.json").write_text(json.dumps({
        "id": "test-film", "bucket": "rnd", "budget_credits": budget, "monthly_cap": cap,
        "target_seconds": 10, "aspect_ratio": "9:16", "repair_reserve_ratio": 0.1,
        "extras": [{"label": "Soul ID", "model": "Soul ID 訓練", "settings": "一次性", "units": 1, "takes": 1}],
    }), encoding="utf-8")
    shots = [
        {"shot_id": f"S0{i}", "act": 1, "start_s": (i - 1) * 5, "duration_s": 5, "purpose": "p",
         "framing": "wide", "tool": "cinema-studio-4.0",
         "estimate": {"model": "Cinema Studio 4.0", "settings": "5 秒，720p", "units": 1, "takes": 2}}
        for i in (1, 2)
    ]
    (project / "shots.json").write_text(json.dumps(shots, ensure_ascii=False), encoding="utf-8")
    return project


def pass_stage(project: Path, stage: str) -> None:
    data = s.load_project(project)
    data["stages"][stage] = {"status": "passed", "by": "test"}
    s.save_project(project, data)


class SchedulerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project = make_project(self.root)
        self.ledger = self.root / "ledger.csv"
        self.cost = self.root / "cost.csv"
        self.cost.write_text(COST_TABLE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def take(self, **kw):
        args = dict(shot_id="S01", phase="draft", surface="web-unlimited", model="Nano Banana Pro",
                    credits=Decimal("0"), ledger=self.ledger, month="2026-11")
        args.update(kw)
        return s.add_take(self.project, **args)

    def test_plan_totals_shots_extras_and_reserve(self):
        result = s.plan(self.project, self.cost)
        self.assertEqual(result["shot_total"], Decimal("140"))
        self.assertEqual(result["extra_total"], Decimal("25"))
        self.assertEqual(result["reserve"], Decimal("14.00"))
        self.assertEqual(result["total"], Decimal("179.00"))

    def test_gates_cannot_be_skipped(self):
        for name in ("reference-report.md", "style-bible.md", "story-bible.md"):
            (self.project / name).write_text("x", encoding="utf-8")
        with self.assertRaises(s.GateError):
            s.approve_gate(self.project, "02", "Neon")
        s.approve_gate(self.project, "01", "Neon")
        s.approve_gate(self.project, "02", "Neon")
        self.assertTrue(s.stage_passed(s.load_project(self.project), "02"))

    def test_animatic_gate_needs_keyframes_and_timing(self):
        for stage in ("01", "02", "03"):
            pass_stage(self.project, stage)
        (self.project / "animatic.md").write_text("x", encoding="utf-8")
        problems = s.check_gate(self.project, "04")
        self.assertTrue(any("關鍵幀" in p for p in problems))
        shots = s.load_shots(self.project)
        for shot in shots:
            shot["keyframe"] = "k.png"
        (self.project / "shots.json").write_text(json.dumps(shots, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(s.check_gate(self.project, "04"), [])

    def test_draft_blocked_before_script_lock(self):
        with self.assertRaises(s.GateError):
            self.take()

    def test_render_blocked_before_animatic_gate(self):
        pass_stage(self.project, "02")
        draft = self.take()
        s.select_take(self.project, draft["take_id"])
        with self.assertRaisesRegex(s.GateError, "Animatic"):
            self.take(phase="render", surface="web", model="Cinema Studio 4.0", credits=Decimal("35"), generation_id="g1")

    def test_render_needs_selected_draft(self):
        for stage in ("02", "04"):
            pass_stage(self.project, stage)
        with self.assertRaisesRegex(s.GateError, "selected"):
            self.take(phase="render", surface="web", model="Cinema Studio 4.0", credits=Decimal("35"), generation_id="g1")

    def test_full_cycle_logs_credits_to_takes_and_ledger(self):
        for stage in ("02", "04"):
            pass_stage(self.project, stage)
        draft = self.take()
        s.select_take(self.project, draft["take_id"])
        render = self.take(phase="render", surface="web", model="Cinema Studio 4.0", settings="5 秒，720p",
                           credits=Decimal("35"), generation_id="g1")
        s.set_qc(self.project, render["take_id"], "fail", "手指")
        with self.assertRaises(s.GateError):
            s.promote_take(self.project, render["take_id"])
        repair = self.take(phase="repair", surface="web", model="Cinema Studio 4.0", credits=Decimal("35"), generation_id="g2")
        s.set_qc(self.project, repair["take_id"], "pass")
        s.promote_take(self.project, repair["take_id"])
        takes = s.load_takes(self.project)
        self.assertEqual(s.project_spent(takes), Decimal("70"))
        self.assertEqual([t["promoted"] for t in takes], ["", "", "yes"])
        ledger_rows = self.ledger.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(ledger_rows), 3)  # header + two paid takes
        self.assertEqual(s.month_spent(self.ledger, "2026-11"), Decimal("70"))

    def test_repair_requires_failed_render(self):
        for stage in ("02", "04"):
            pass_stage(self.project, stage)
        with self.assertRaisesRegex(s.GateError, "fail"):
            self.take(phase="repair", surface="web", model="Cinema Studio 4.0", credits=Decimal("35"), generation_id="g")

    def test_project_budget_enforced(self):
        for stage in ("02", "04"):
            pass_stage(self.project, stage)
        draft = self.take()
        s.select_take(self.project, draft["take_id"])
        with self.assertRaisesRegex(s.GateError, "專案預算"):
            self.take(phase="render", surface="web", model="Cinema Studio 4.0", credits=Decimal("250"), generation_id="g")

    def test_monthly_cap_enforced_from_ledger(self):
        project = self.root / "film"
        data = s.load_project(project)
        data["budget_credits"] = 100000
        s.save_project(project, data)
        s.append_ledger(self.ledger, {"date": "2026-11-20", "bucket": "rnd", "credits": "8980", "refunded": "no"})
        for stage in ("02", "04"):
            pass_stage(project, stage)
        draft = self.take()
        s.select_take(project, draft["take_id"])
        with self.assertRaisesRegex(s.GateError, "當月上限"):
            self.take(phase="render", surface="web", model="Cinema Studio 4.0", credits=Decimal("35"), generation_id="g")

    def test_automated_surfaces_cannot_be_free(self):
        pass_stage(self.project, "02")
        for surface in ("mcp", "cli", "canvas"):
            with self.assertRaisesRegex(s.GateError, "一律扣點"):
                self.take(surface=surface)

    def test_unlimited_must_be_zero_and_draft_is_cheap(self):
        pass_stage(self.project, "02")
        with self.assertRaises(s.GateError):
            self.take(credits=Decimal("2"))
        with self.assertRaisesRegex(s.GateError, "draft 單次上限"):
            self.take(surface="web", credits=Decimal("35"), generation_id="g")

    def test_paid_take_needs_generation_id(self):
        pass_stage(self.project, "02")
        with self.assertRaisesRegex(s.GateError, "generation_id"):
            self.take(surface="web", credits=Decimal("2"))

    def test_real_trailer_plan_is_valid(self):
        trailer = s.REPO / "projects" / "2026-11-proof-trailer"
        result = s.plan(trailer)
        self.assertEqual(len(result["shots"]), 16)
        self.assertAlmostEqual(result["seconds"], 90.0)
        self.assertLess(result["total"], Decimal("9000"))


if __name__ == "__main__":
    unittest.main()
