#!/usr/bin/env python3
"""Render directions.json into Markdown docs and costs.csv. Prices come from budget/cost-table.csv."""
import csv, json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
price = {}
for r in csv.DictReader(open(ROOT / "budget/cost-table.csv", encoding="utf-8")):
    price[(r["model"], r["settings"])] = float(r["credits_numeric"]) if r["credits_numeric"] else None
CS4_5S = price[("Cinema Studio 4.0", "5 秒，720p")]          # 35 -> 7/s, min 5 s
GJ_15S = price[("Genjutsu Lite", "15 秒，720p")]             # 32 per clip up to 15 s
UPS = price[("ByteDance 影片放大", "4K，帶 5 秒時長參數，未帶來源影片")]  # 4 per shot
VO = price[("Seed Audio 1.0", "語音預設")]                   # 0.2 per line
SOUL = price[("Soul ID 訓練", "一次性")]                       # 25
TAKES, RESERVE = 2, 0.15
TOOL = {"cs4": "Cinema Studio 4.0 720p", "genjutsu": "Genjutsu Lite 720p"}
CONTEST = {"safe": "比賽可用（人物剪影、臉不可辨識）", "safe-if-replaced": "比賽可用，前提是人物整個換成虛構角色", "portfolio-only": "只能當作品集（保留 Neon 本人的臉）"}

def shot_cost(s):
    d = s["t"][1] - s["t"][0]
    return (max(5, d) * CS4_5S / 5 if s["tool"] == "cs4" else GJ_15S * math.ceil(d / 15)) * TAKES

data = json.load(open(HERE / "directions.json", encoding="utf-8"))
rows, summary = [], []
for D in data["directions"]:
    gen = sum(shot_cost(s) for s in D["shots"])
    ups = UPS * len(D["shots"])
    vo = VO * sum(1 for s in D["shots"] if s.get("vo"))
    soul = SOUL if D["id"] == "D4" else 0
    sub = gen + ups + vo + soul
    total = math.ceil(sub * (1 + RESERVE))
    dur = D["shots"][-1]["t"][1]
    D["_cost"] = dict(gen=gen, ups=ups, vo=vo, soul=soul, sub=sub, total=total, dur=dur)
    for s in D["shots"]:
        rows.append([D["id"], s["id"], s["t"][0], s["t"][1], s.get("src") or "", TOOL[s["tool"]], TAKES, shot_cost(s)])
    summary.append([D["id"], D["name_zh"], D["name_en"], dur, gen, ups, round(vo, 1), soul, round(sub, 1), total, D["contest"]])

with open(HERE / "costs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["direction", "shot", "start_s", "end_s", "source_tc", "tool", "takes", "credits"]); w.writerows(rows)
with open(HERE / "costs-summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["direction", "name_zh", "name_en", "seconds", "video", "upscale", "vo", "soul_id", "subtotal", "total_with_15pct_reserve", "contest"]); w.writerows(summary)

md = ["# 五個方向：風格、劇本、估點", "", "由 `build_docs.py` 從 `directions.json` 產生，別手改。估點規則：Cinema Studio 4.0 720p 每秒 7 點（最少 5 秒）、Genjutsu Lite 每段 15 秒內 32 點，每鏡 2 個 take；每鏡 4K 放大 4 點；AI 旁白每句 0.2 點；再加 15% 修補預備。關鍵幀靜圖在網站 Unlimited 跑，0 點。", ""]
md += ["| 方向 | 長度 | 影片 | 放大 | 旁白 | Soul ID | 合計（含 15%） | 比賽 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
for D in data["directions"]:
    c = D["_cost"]
    md.append(f"| {D['id']} {D['name_zh']} {D['name_en']} | {c['dur']} 秒 | {c['gen']:g} | {c['ups']:g} | {c['vo']:.1f} | {c['soul']:g} | **{c['total']}** | {CONTEST[D['contest']]} |")
for D in data["directions"]:
    c = D["_cost"]
    md += ["", f"## {D['id']}《{D['name_zh']} {D['name_en']}》", "", f"- 來源：{D['lineage']}", f"- 一句話：{D['logline_zh']}", f"- Logline: {D['logline_en']}", f"- 畫面：{D['look']}", f"- 水箱換成：{D['replaces_tank']}", f"- 怎麼用原片表演：{D['performance']}", f"- 比賽：{CONTEST[D['contest']]}", f"- 放進 CROSSING：{D['crossing_slot']}", "", "### 關鍵幀提示詞（網站 Unlimited，上傳對應 plate 當參考圖）", ""]
    for k in D["keyframes"]:
        md += [f"**{k['id']}**（{k['model']}，9:16，參考 `{k['plate']}`）", "", "```text", k["prompt"], "```", ""]
    md += [f"### 劇本（{c['dur']} 秒）", "", "| 鏡 | 時間 | 原片時間碼 | 畫面 | 旁白／字幕 | 工具 | 點數（2 take） |", "| --- | --- | --- | --- | --- | --- | ---: |"]
    for s in D["shots"]:
        vo = f"「{s['vo'][0]}」<br>“{s['vo'][1]}”" if s.get("vo") else "—"
        md.append(f"| {s['id']} | {s['t'][0]}–{s['t'][1]}s | {s.get('src') or '—（新鏡）'} | {s['zh']} | {vo} | {TOOL[s['tool']]} | {shot_cost(s):g} |")
    md += ["", f"聲音：{D['sound']}", "", f"估點：影片 {c['gen']:g}＋放大 {c['ups']:g}＋旁白 {c['vo']:.1f}＋Soul ID {c['soul']:g}＝{c['sub']:.1f}，加 15% 預備後 **{c['total']} 點**（月額度 9,000 的 {c['total']/90:.1f}%）。"]
(HERE / "directions.md").write_text("\n".join(md) + "\n", encoding="utf-8")
for s in summary: print(s)
