#!/usr/bin/env python3
"""Cost-aware shot scheduler: stage gates, take registry, credit logging.

A project folder holds project.json (stages, budget), shots.json (Shot IR list)
and takes.csv (take registry). Paid takes are also appended to budget/ledger.csv
so budget/track.py keeps working.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "budget"))
import track  # noqa: E402

TAIPEI = ZoneInfo("Asia/Taipei")
DEFAULT_COST_TABLE = REPO / "budget" / "cost-table.csv"
DEFAULT_LEDGER = REPO / "budget" / "ledger.csv"
MONTHLY_CAP = Decimal("9000")
DRAFT_MAX_CREDITS = Decimal("5")
TIMING_TOLERANCE_S = 1.0
ALWAYS_PAID_SURFACES = {"mcp", "cli", "canvas", "supercomputer", "api"}
SURFACES = ALWAYS_PAID_SURFACES | {"web", "web-unlimited"}
PHASES = ("draft", "render", "repair")
TAKE_FIELDS = [
    "take_id", "shot_id", "phase", "surface", "model", "settings", "prompt_version",
    "refs", "generation_id", "credits", "qc", "qc_reason", "selected", "promoted",
    "created_at", "note",
]
LEDGER_FIELDS = [
    "date", "bucket", "model", "settings", "aspect_ratio", "credits", "project",
    "outcome", "refunded", "prompt_id", "note",
]
SHOT_REQUIRED = ["shot_id", "act", "start_s", "duration_s", "purpose", "framing", "tool", "estimate"]
ESTIMATE_REQUIRED = ["model", "settings", "units", "takes"]


@dataclass(frozen=True)
class Stage:
    stage_id: str
    name: str
    artifacts: tuple[str, ...]


STAGES = (
    Stage("01", "逆向工程", ("reference-report.md", "style-bible.md")),
    Stage("02", "故事開發 Script Lock", ("story-bible.md",)),
    Stage("03", "視覺開發 Asset Lock", ("character-bible.md", "location-bible.md", "prop-bible.md")),
    Stage("04", "預演 Timing Lock", ("shots.json", "animatic.md")),
    Stage("05", "鏡頭製作", ("takes.csv",)),
    Stage("06", "後製 Picture/Sound Lock", ("post-lock.md",)),
    Stage("07", "技術與創意 QC", ("qc-report.json",)),
    Stage("08", "交付", ("delivery.md",)),
)
STAGE_BY_ID = {stage.stage_id: stage for stage in STAGES}


class GateError(Exception):
    """A rule in the pipeline refused the action."""


def now_text() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


# ---------- project files ----------

def load_project(project: Path) -> dict:
    path = project / "project.json"
    if not path.exists():
        raise GateError(f"{path} 不存在")
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("stages", {})
    return data


def save_project(project: Path, data: dict) -> None:
    (project / "project.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_shots(project: Path) -> list[dict]:
    path = project / "shots.json"
    if not path.exists():
        return []
    shots = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(shots, list):
        raise GateError("shots.json 必須是陣列")
    return shots


def validate_shots(shots: list[dict]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for index, shot in enumerate(shots):
        label = shot.get("shot_id", f"#{index}")
        for key in SHOT_REQUIRED:
            if key not in shot:
                problems.append(f"{label} 缺少 {key}")
        estimate = shot.get("estimate", {})
        for key in ESTIMATE_REQUIRED:
            if key not in estimate:
                problems.append(f"{label} 的 estimate 缺少 {key}")
        if label in seen:
            problems.append(f"{label} 重複")
        seen.add(label)
        duration = shot.get("duration_s", 0)
        if not isinstance(duration, (int, float)) or duration <= 0 or duration > 30:
            problems.append(f"{label} 的 duration_s 必須在 0–30 秒")
    return problems


def load_takes(project: Path) -> list[dict]:
    path = project / "takes.csv"
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_takes(project: Path, takes: list[dict]) -> None:
    with (project / "takes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TAKE_FIELDS)
        writer.writeheader()
        for take in takes:
            writer.writerow({field: take.get(field, "") for field in TAKE_FIELDS})


def append_ledger(ledger: Path, row: dict) -> None:
    new = not ledger.exists() or ledger.stat().st_size == 0
    with ledger.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        if new:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in LEDGER_FIELDS})


# ---------- costs ----------

def load_cost_table(path: Path = DEFAULT_COST_TABLE) -> dict[tuple[str, str], Decimal]:
    table: dict[tuple[str, str], Decimal] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw = (row.get("credits_numeric") or "").strip()
            if not raw:
                continue
            table[(row["model"].strip(), row["settings"].strip())] = Decimal(raw)
    return table


def unit_cost(table: dict[tuple[str, str], Decimal], model: str, settings: str) -> Decimal:
    if model == "free":
        return Decimal("0")
    key = (model, settings)
    if key not in table:
        raise GateError(f"cost-table.csv 找不到 {model} / {settings}")
    return table[key]


def estimate_line(table: dict[tuple[str, str], Decimal], item: dict) -> Decimal:
    est = item["estimate"] if "estimate" in item else item
    cost = unit_cost(table, est["model"], est["settings"])
    return cost * Decimal(str(est["units"])) * Decimal(str(est["takes"]))


def plan(project: Path, cost_table: Path = DEFAULT_COST_TABLE) -> dict:
    data = load_project(project)
    shots = load_shots(project)
    problems = validate_shots(shots)
    if problems:
        raise GateError("；".join(problems))
    table = load_cost_table(cost_table)
    lines = []
    for shot in shots:
        lines.append({"id": shot["shot_id"], "act": shot["act"], "tool": shot["tool"],
                      "credits": estimate_line(table, shot)})
    extras = []
    for extra in data.get("extras", []):
        extras.append({"id": extra["label"], "credits": estimate_line(table, extra)})
    shot_total = sum((line["credits"] for line in lines), Decimal("0"))
    extra_total = sum((line["credits"] for line in extras), Decimal("0"))
    reserve_ratio = Decimal(str(data.get("repair_reserve_ratio", 0)))
    reserve = (shot_total * reserve_ratio).quantize(Decimal("0.01"))
    total = shot_total + extra_total + reserve
    seconds = sum(float(shot["duration_s"]) for shot in shots)
    return {"shots": lines, "extras": extras, "shot_total": shot_total,
            "extra_total": extra_total, "reserve": reserve, "total": total,
            "seconds": seconds, "budget": Decimal(str(data.get("budget_credits", 0))),
            "cap": Decimal(str(data.get("monthly_cap", MONTHLY_CAP)))}


# ---------- gates ----------

def stage_passed(data: dict, stage_id: str) -> bool:
    return data["stages"].get(stage_id, {}).get("status") == "passed"


def check_gate(project: Path, stage_id: str) -> list[str]:
    if stage_id not in STAGE_BY_ID:
        return [f"沒有階段 {stage_id}"]
    data = load_project(project)
    problems: list[str] = []
    previous = f"{int(stage_id) - 1:02d}"
    if previous in STAGE_BY_ID and not stage_passed(data, previous):
        problems.append(f"上一階段 {previous} 尚未通過")
    for artifact in STAGE_BY_ID[stage_id].artifacts:
        if not (project / artifact).exists():
            problems.append(f"缺少 {artifact}")
    if stage_id == "04" and (project / "shots.json").exists():
        shots = load_shots(project)
        problems.extend(validate_shots(shots))
        missing = [shot.get("shot_id", "?") for shot in shots if not shot.get("keyframe")]
        if missing:
            problems.append(f"這些鏡頭沒有關鍵幀：{', '.join(missing)}")
        target = float(data.get("target_seconds", 0))
        total = sum(float(shot.get("duration_s", 0)) for shot in shots)
        if abs(total - target) > TIMING_TOLERANCE_S:
            problems.append(f"鏡長加總 {total:g} 秒，目標 {target:g} 秒")
    if stage_id == "05":
        takes = load_takes(project)
        promoted = {take["shot_id"] for take in takes if take.get("promoted") == "yes"}
        missing = [shot["shot_id"] for shot in load_shots(project) if shot["shot_id"] not in promoted]
        if missing:
            problems.append(f"這些鏡頭沒有 promoted take：{', '.join(missing)}")
    if stage_id == "07" and (project / "qc-report.json").exists():
        sys.path.insert(0, str(REPO / "qc"))
        import creative_score  # noqa: E402
        report = json.loads((project / "qc-report.json").read_text(encoding="utf-8"))
        result = creative_score.evaluate(report.get("creative", {}))
        problems.extend(result["problems"])
        if report.get("mechanical_pass") is not True:
            problems.append("機械檢查未通過")
        if report.get("manual_checks_pass") is not True:
            problems.append("人工檢查（人物漂移、肢體、權利）未通過")
    return problems


def approve_gate(project: Path, stage_id: str, approver: str) -> None:
    if not approver.strip():
        raise GateError("簽門要寫導演名字")
    problems = check_gate(project, stage_id)
    if problems:
        raise GateError("；".join(problems))
    data = load_project(project)
    data["stages"][stage_id] = {"status": "passed", "by": approver, "at": now_text()}
    save_project(project, data)


# ---------- takes ----------

def next_take_id(takes: list[dict]) -> str:
    numbers = [int(take["take_id"][1:]) for take in takes if take.get("take_id", "").startswith("T")]
    return f"T{(max(numbers) + 1) if numbers else 1:04d}"


def project_spent(takes: list[dict]) -> Decimal:
    return sum((Decimal(take["credits"] or "0") for take in takes), Decimal("0"))


def month_spent(ledger: Path, month: str) -> Decimal:
    spends, _ = track.load_spend(ledger, month)
    return sum((spend.credits for spend in spends if spend.counted), Decimal("0"))


def add_take(project: Path, shot_id: str, phase: str, surface: str, model: str,
             credits: Decimal, settings: str = "", prompt_version: str = "",
             refs: str = "", generation_id: str = "", bucket: str = "",
             note: str = "", ledger: Path | None = DEFAULT_LEDGER,
             month: str | None = None) -> dict:
    data = load_project(project)
    shots = {shot["shot_id"]: shot for shot in load_shots(project)}
    takes = load_takes(project)
    if shot_id not in shots:
        raise GateError(f"shots.json 沒有 {shot_id}")
    if phase not in PHASES:
        raise GateError(f"phase 只能是 {', '.join(PHASES)}")
    if surface not in SURFACES:
        raise GateError(f"surface 只能是 {', '.join(sorted(SURFACES))}")
    if credits < 0:
        raise GateError("點數不能是負數")
    if surface in ALWAYS_PAID_SURFACES and credits == 0:
        raise GateError(f"{surface} 的生成一律扣點，不能登記 0 點")
    if surface == "web-unlimited" and credits != 0:
        raise GateError("web-unlimited 必須是 0 點；生成鍵若顯示點數，改用 surface=web")
    if phase == "draft":
        if not stage_passed(data, "02"):
            raise GateError("Script Lock（02）通過前不做 draft")
        if credits > DRAFT_MAX_CREDITS:
            raise GateError(f"draft 單次上限 {DRAFT_MAX_CREDITS} 點；高品質生成請走 select → render")
    if phase in {"render", "repair"}:
        if not stage_passed(data, "04"):
            raise GateError("Animatic Gate（04）通過前不准 render 或 repair")
        shot_takes = [take for take in takes if take["shot_id"] == shot_id]
        if phase == "render" and not any(take.get("selected") == "yes" for take in shot_takes):
            raise GateError(f"{shot_id} 還沒有 selected 的 draft")
        if phase == "repair" and not any(
            take["phase"] in {"render", "repair"} and take.get("qc") == "fail" for take in shot_takes
        ):
            raise GateError(f"{shot_id} 沒有 QC 判 fail 的 render，不能 repair")
    if credits > 0:
        budget = Decimal(str(data.get("budget_credits", 0)))
        spent = project_spent(takes)
        if spent + credits > budget:
            raise GateError(f"超出專案預算：已用 {spent}，本次 {credits}，預算 {budget}")
        if ledger is not None:
            cap = Decimal(str(data.get("monthly_cap", MONTHLY_CAP)))
            used = month_spent(ledger, month or track.current_month())
            if used + credits > cap:
                raise GateError(f"超出當月上限：已用 {used}，本次 {credits}，上限 {cap}")
        if not generation_id:
            raise GateError("付費 take 要填 generation_id，事後才能對帳")
    take = {
        "take_id": next_take_id(takes), "shot_id": shot_id, "phase": phase,
        "surface": surface, "model": model, "settings": settings,
        "prompt_version": prompt_version, "refs": refs, "generation_id": generation_id,
        "credits": str(credits), "qc": "", "qc_reason": "", "selected": "",
        "promoted": "", "created_at": now_text(), "note": note,
    }
    takes.append(take)
    save_takes(project, takes)
    if credits > 0 and ledger is not None:
        append_ledger(ledger, {
            "date": datetime.now(TAIPEI).strftime("%Y-%m-%d"),
            "bucket": bucket or data.get("bucket", ""), "model": model,
            "settings": settings, "aspect_ratio": data.get("aspect_ratio", ""),
            "credits": str(credits), "project": data.get("id", project.name),
            "outcome": phase, "refunded": "no", "prompt_id": prompt_version,
            "note": f"{take['take_id']} {shot_id} {generation_id}",
        })
    return take


def _find(takes: list[dict], take_id: str) -> dict:
    for take in takes:
        if take["take_id"] == take_id:
            return take
    raise GateError(f"找不到 {take_id}")


def select_take(project: Path, take_id: str) -> None:
    takes = load_takes(project)
    take = _find(takes, take_id)
    if take["phase"] != "draft":
        raise GateError("只能 select draft")
    for other in takes:
        if other["shot_id"] == take["shot_id"] and other["phase"] == "draft":
            other["selected"] = ""
    take["selected"] = "yes"
    save_takes(project, takes)


def set_qc(project: Path, take_id: str, result: str, reason: str = "") -> None:
    if result not in {"pass", "fail"}:
        raise GateError("QC 結果只能是 pass 或 fail")
    if result == "fail" and not reason.strip():
        raise GateError("fail 要寫原因")
    takes = load_takes(project)
    take = _find(takes, take_id)
    take["qc"] = result
    take["qc_reason"] = reason
    save_takes(project, takes)


def promote_take(project: Path, take_id: str) -> None:
    takes = load_takes(project)
    take = _find(takes, take_id)
    if take["phase"] not in {"render", "repair"}:
        raise GateError("只能 promote render 或 repair 的 take")
    if take.get("qc") != "pass":
        raise GateError("QC 沒 pass 不能 promote")
    for other in takes:
        if other["shot_id"] == take["shot_id"]:
            other["promoted"] = ""
    take["promoted"] = "yes"
    save_takes(project, takes)


# ---------- CLI ----------

def format_plan(result: dict) -> str:
    lines = [f"{'鏡頭':<8}{'幕':>3}  {'工具':<20}{'估點':>10}"]
    for line in result["shots"]:
        lines.append(f"{line['id']:<8}{line['act']:>3}  {line['tool']:<20}{line['credits']:>10}")
    for line in result["extras"]:
        lines.append(f"{'':8}{'':>3}  {line['id']:<20}{line['credits']:>10}")
    lines += [
        "",
        f"片長 {result['seconds']:g} 秒",
        f"鏡頭小計 {result['shot_total']}",
        f"其他 {result['extra_total']}",
        f"修補預備 {result['reserve']}",
        f"合計 {result['total']}（專案預算 {result['budget']}，每月上限 {result['cap']}，"
        f"占上限 {(result['total'] / result['cap'] * 100).quantize(Decimal('0.1'))}%）",
    ]
    return "\n".join(lines)


def format_status(project: Path) -> str:
    data = load_project(project)
    takes = load_takes(project)
    lines = [f"專案 {data.get('id', project.name)}"]
    for stage in STAGES:
        info = data["stages"].get(stage.stage_id, {})
        mark = "通過" if info.get("status") == "passed" else "未過"
        who = f"（{info.get('by')} {info.get('at')}）" if info.get("by") else ""
        lines.append(f"  {stage.stage_id} {stage.name}：{mark}{who}")
    lines.append(f"已登記 take {len(takes)} 個，花費 {project_spent(takes)} 點，"
                 f"預算 {data.get('budget_credits', 0)} 點")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="鏡頭排程器：階段門與點數紀錄")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan"); p.add_argument("project", type=Path)
    p.add_argument("--cost-table", type=Path, default=DEFAULT_COST_TABLE)
    p = sub.add_parser("status"); p.add_argument("project", type=Path)
    p = sub.add_parser("check"); p.add_argument("project", type=Path); p.add_argument("stage")
    p = sub.add_parser("gate"); p.add_argument("project", type=Path); p.add_argument("stage")
    p.add_argument("--by", required=True)
    p = sub.add_parser("take"); p.add_argument("project", type=Path)
    p.add_argument("--shot", required=True); p.add_argument("--phase", required=True)
    p.add_argument("--surface", required=True); p.add_argument("--model", required=True)
    p.add_argument("--credits", required=True); p.add_argument("--settings", default="")
    p.add_argument("--prompt-version", default=""); p.add_argument("--refs", default="")
    p.add_argument("--generation-id", default=""); p.add_argument("--bucket", default="")
    p.add_argument("--note", default=""); p.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p = sub.add_parser("select"); p.add_argument("project", type=Path); p.add_argument("take_id")
    p = sub.add_parser("qc"); p.add_argument("project", type=Path); p.add_argument("take_id")
    p.add_argument("--result", required=True); p.add_argument("--reason", default="")
    p = sub.add_parser("promote"); p.add_argument("project", type=Path); p.add_argument("take_id")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.command == "plan":
            print(format_plan(plan(args.project, args.cost_table)))
        elif args.command == "status":
            print(format_status(args.project))
        elif args.command == "check":
            problems = check_gate(args.project, args.stage)
            print("可以簽" if not problems else "\n".join(problems))
            return 0 if not problems else 1
        elif args.command == "gate":
            approve_gate(args.project, args.stage, args.by)
            print(f"階段 {args.stage} 已通過")
        elif args.command == "take":
            try:
                credits = Decimal(args.credits)
            except InvalidOperation as error:
                raise GateError(f"點數無法解析：{args.credits}") from error
            take = add_take(args.project, args.shot, args.phase, args.surface, args.model,
                            credits, args.settings, args.prompt_version, args.refs,
                            args.generation_id, args.bucket, args.note, args.ledger)
            print(f"已登記 {take['take_id']}（{take['shot_id']} {take['phase']} {take['credits']} 點）")
        elif args.command == "select":
            select_take(args.project, args.take_id); print(f"{args.take_id} 已 select")
        elif args.command == "qc":
            set_qc(args.project, args.take_id, args.result, args.reason); print("QC 已記錄")
        elif args.command == "promote":
            promote_take(args.project, args.take_id); print(f"{args.take_id} 已 promote")
    except (GateError, OSError, ValueError, KeyError) as error:
        print(f"拒絕：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
